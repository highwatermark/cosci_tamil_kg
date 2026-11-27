"""Build a blinded Tamil relation packet or score locked predictions against prior AI grades."""
import csv
import hashlib
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KG = HERE.parents[2] / "kg"
BOOKS = ("tirumanthiram", "thiruppugazh")
SEED = 20261124


def rows(path):
    with path.open() as f:
        return list(map(json.loads, f))


def cases():
    rng = random.Random(SEED)
    nodes = {}
    for book in (*BOOKS, "kural", "naladiyar"):
        for node in rows(KG / book / "nodes.jsonl"):
            if node["type"] == "Verse":
                nodes[node["id"]] = node["tamil"]
    sample = []
    for book in BOOKS:
        edges = rows(KG / book / "edges.jsonl")
        for grade, count in (("sound", 4), ("weak", 3), ("forced", 1)):
            pool = sorted((e for e in edges if e.get("audit") == grade),
                          key=lambda e: (e["s"], e["o"], e["p"]))
            sample.extend(rng.sample(pool, count))
    rng.shuffle(sample)
    packet, key = [], []
    for i, e in enumerate(sample, 1):
        case = f"C{i:02}"
        packet.append(dict(case=case, a=nodes[e["s"]], b=nodes[e["o"]],
                           relation=e["p"], claim=e["note"]))
        key.append(dict(case=case, source=e["s"], target=e["o"], grade=e["audit"]))
    return packet, key


def score(key, predictions):
    with predictions.open() as f:
        answers = list(csv.DictReader(f))
    labels = {r["case"]: r["decision"] for r in answers}
    assert len(answers) == len(labels) == len(key) and set(labels) == {k["case"] for k in key}
    assert set(labels.values()) <= {"accept", "hold"}
    counts = dict(tp=0, fp=0, tn=0, fn=0)
    for k in key:
        truth = k["grade"] == "sound"
        pred = labels[k["case"]] == "accept"
        counts[{(True, True): "tp", (False, True): "fp",
                (False, False): "tn", (True, False): "fn"}[truth, pred]] += 1
    return counts


if __name__ == "__main__":
    packet, key = cases()
    if sys.argv[1:] == ["packet"]:
        (HERE / "packet.json").write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n")
    elif sys.argv[1:] == ["score"]:
        assert json.loads((HERE / "packet.json").read_text()) == packet
        print("packet_sha256", hashlib.sha256((HERE / "packet.json").read_bytes()).hexdigest())
        with (HERE / "prior_grades.csv").open("w") as f:
            writer = csv.DictWriter(f, fieldnames=key[0])
            writer.writeheader()
            writer.writerows(key)
        for name in ["baseline", "evidence_first"]:
            print(name, score(key, HERE / (name + ".csv")))
    else:
        sys.exit("Use packet or score")
