"""Prepare independent reader prompts and join completed assessments against the source."""
import argparse
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAMES = ("philology", "voice")
FIELDS = ("reading", "alternative", "limit", "anchor")


def load(path):
    return json.loads(path.read_text())


def validate(packet, reviews):
    ids = [row["case"] for row in packet]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate packet IDs")
    for role, results in reviews.items():
        if [row["case"] for row in results] != ids:
            raise ValueError(f"{role}: case identifiers or order differ from packet")
        for src, row in zip(packet, results):
            if any(not isinstance(row.get(k), str) or not row[k].strip() for k in FIELDS):
                raise ValueError(f"{role}: missing reading evidence for {src['case']}")
            if not any(row["anchor"] in line for line in src["tamil"]):
                raise ValueError(f"{role}: unmatched Tamil anchor for {src['case']}")
            if row.get("confidence") not in {"high", "medium", "low"}:
                raise ValueError(f"{role}: invalid confidence for {src['case']}")


def prompt_text(role, packet):
    return ((HERE / (role + ".md")).read_text().strip()
            + "\nReturn JSON only. Work from this packet in a fresh session without tools.\n"
            + json.dumps(packet, ensure_ascii=False, indent=2))


def run_reader(role, packet, model):
    with tempfile.TemporaryDirectory() as temp:
        answer = Path(temp) / "answer.json"
        command = ["codex", "exec", "--ephemeral", "--ignore-user-config", "--sandbox",
                   "read-only", "--skip-git-repo-check", "-C", temp, "-o", str(answer)]
        if model:
            command += ["--model", model]
        subprocess.run(command + ["-"], input=prompt_text(role, packet), text=True,
                       stdout=subprocess.DEVNULL, check=True)
        return load(answer)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    prompt = sub.add_parser("prompt")
    prompt.add_argument("reader", choices=NAMES)
    prompt.add_argument("packet", type=Path)
    run = sub.add_parser("run", help="Launch two fresh Codex CLI sessions")
    run.add_argument("packet", type=Path)
    run.add_argument("--model")
    join = sub.add_parser("join")
    join.add_argument("packet", type=Path)
    for name in NAMES:
        join.add_argument(name, type=Path)
    args = parser.parse_args()
    packet = load(args.packet)
    if args.mode == "prompt":
        print(prompt_text(args.reader, packet))
        return
    if args.mode == "run":
        with ThreadPoolExecutor(max_workers=len(NAMES)) as pool:
            jobs = {role: pool.submit(run_reader, role, packet, args.model) for role in NAMES}
            reviews = {role: job.result() for role, job in jobs.items()}
    else:
        reviews = {role: load(getattr(args, role)) for role in NAMES}
    validate(packet, reviews)
    pairs = [dict(src, **{role: rows[i] for role, rows in reviews.items()})
             for i, src in enumerate(packet)]
    print(json.dumps(pairs, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
