"""Blind grading packets for marked Sangam chapters (docs/sangam-grader-brief.md).

Usage (from the repository root):
  python3 -I scripts/make_sangam_packets.py OUTDIR BOOK:CH [BOOK:CH ...] [--seed N]
  e.g. python3 -I scripts/make_sangam_packets.py /tmp/out akananuru:3 akananuru:12 pattupattu:1

BOOK is akananuru, purananuru or pattupattu; CH is the chapter number of kg/themes/BOOK/chNNN.json.

Part A: every link of those chapters, shuffled, in packets of at most PER_PACKET, with hidden
calibration links of known grade mixed in (CAL_PER_40 per 40 links, rounded up). Calibration links
are graded Kural and Naladiyar links; their note is split into a note and a `teaches` sentence (its
last sentence) so they look like Sangam links. Each end prints its Tamil and marked reading; a Sangam
end also its colophon, text flags and the marker's thinai, akam/puram and uri; a Kural or Naladiyar
end also Pope's rendering. The Purananuru's modern title, note and commentary are never printed.

Part B: every akam (or mixed) poem of those chapters, shuffled and spread over the packets, with
only its numbered Tamil and its colophon, for a blind re-tag of ullurai and iraicchi.

Writes OUTDIR/packet_N.md and OUTDIR/key.json (one entry per item, with the proposer's tags and,
for calibration links, the known grade). Grades go in OUTDIR/graded/packet_N.<grader>.json and are
scored by scripts/score_sangam_grades.py.
"""
import json
import math
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "kg" / "core"
THEMES = ROOT / "kg" / "themes"
SANGAM = ("akananuru", "purananuru", "pattupattu")
NODE_BOOKS = ("kural", "naladiyar", "tirumanthiram", "thiruppugazh", "siddhar")
PER_PACKET = 40
CAL_PER_40 = 4
CAL_MIX = ["sound", "sound", "weak", "forced"]
PATTU_ID = re.compile(r"pattupattu:(\d+):(\d+)-(\d+)")
GROUP = {"akananuru": "ettuthogai_akam", "purananuru": "ettuthogai_puram", "pattupattu": "pattupattu",
         "kural": "ethics", "naladiyar": "ethics",
         "tirumanthiram": "devotional", "thiruppugazh": "devotional", "siddhar": "devotional"}
BOOK_NAME = {"akananuru": "Akananuru", "purananuru": "Purananuru", "pattupattu": "Pattupattu"}


def read_jsonl(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def usage(msg=None):
    if msg:
        print("error:", msg, file=sys.stderr)
    print(__doc__.split("\n\n")[1], file=sys.stderr)
    sys.exit(2)


def parse_args(argv):
    seed, rest = 31, []
    i = 0
    while i < len(argv):
        if argv[i] == "--seed":
            if i + 1 >= len(argv):
                usage("--seed needs a number")
            seed = int(argv[i + 1])
            i += 2
            continue
        rest.append(argv[i])
        i += 1
    if len(rest) < 2:
        usage()
    out, chs = Path(rest[0]), []
    for spec in rest[1:]:
        m = re.fullmatch(r"(akananuru|purananuru|pattupattu):(\d+)", spec)
        if not m:
            usage(f"bad chapter {spec!r}: want BOOK:CH with BOOK one of {', '.join(SANGAM)}")
        chs.append((m.group(1), int(m.group(2))))
    return out, chs, seed


def ref(book, x):
    """A link end as a full verse id."""
    if isinstance(x, int) or (isinstance(x, str) and x.isdigit()):
        return f"{book}:{int(x)}"
    return str(x)


def book_of(vid):
    return vid.split(":")[0]


class Corpus:
    def __init__(self):
        self.core = {b: {} for b in SANGAM}
        for b in ("akananuru", "purananuru"):
            for r in read_jsonl(CORE / f"{b}.jsonl"):
                if r.get("tamil"):
                    self.core[b][r["id"]] = r
        for u in read_jsonl(CORE / "pattupattu_units.jsonl"):
            self.core["pattupattu"][u["id"]] = u
        self.poems = {p["number"]: p for p in read_jsonl(CORE / "pattupattu.jsonl")}
        self.flags = {}
        for f in read_jsonl(CORE / "sangam_text_flags.jsonl"):
            self.flags.setdefault(f["id"], []).append(f)
        self.marks = {}
        for b in SANGAM:
            for p in sorted((THEMES / b).glob("ch*.json")) if (THEMES / b).exists() else []:
                d = json.loads(p.read_text(encoding="utf-8"))
                for k, v in d.get("verses", {}).items():
                    self.marks[ref(b, k)] = v
        self.nodes = {}
        for b in NODE_BOOKS:
            for n in read_jsonl(ROOT / "kg" / b / "nodes.jsonl"):
                if n.get("type") == "Verse":
                    self.nodes[n["id"]] = n
        self.tm = {r["number"]: r for r in read_jsonl(CORE / "tirumanthiram.jsonl")}
        self.tp = {r["number"]: r for r in read_jsonl(CORE / "thiruppugazh.jsonl")}

    def sangam_text(self, vid):
        """(numbered lines, colophon dict, flag lines) for a Sangam verse id."""
        b = book_of(vid)
        if b == "pattupattu":
            m = PATTU_ID.fullmatch(vid)
            if not m:
                raise KeyError(vid)
            poem, a, z = (int(g) for g in m.groups())
            p = self.poems[poem]
            lines = list(enumerate(p["tamil"][a - 1:z], a))
            col = {k: p.get(k) for k in ("thinai", "thurai", "poet", "patron")}
            title = f"{p['title']}, lines {a}-{z}"
            flags = [f for f in self.flags.get(p["id"], []) if f.get("line") and a <= f["line"] <= z]
        else:
            r = self.core[b][vid]
            lines = list(enumerate(r["tamil"], 1))
            col = {k: r.get(k) for k in ("thinai", "thurai", "poet", "patron")}
            title = f"{BOOK_NAME[b]} {r['number']}" + (f", {r['section']}" if r.get("section") else "")
            flags = self.flags.get(vid, [])
        flag_lines = [f"FLAG {f['kind']}" + (f" line {f['line']}" if f.get("line") else "")
                      + f": {' '.join(str(f.get('detail') or '').split())}" for f in flags]
        return title, lines, col, flag_lines

    def block(self, vid):
        b = book_of(vid)
        if b in SANGAM:
            title, lines, col, flag_lines = self.sangam_text(vid)
            out = [f"### {vid} ({title})",
                   colophon_line(col)]
            out += [f"{i:4} {t}" for i, t in lines]
            out += flag_lines
            m = self.marks.get(vid)
            if m is None:
                out.append("Marked reading: (this verse is not yet marked)")
                return out
            out.append(f"Marked reading: {m['reading']}")
            if m.get("nuance"):
                out.append(f"Marker's nuance: {m['nuance']}")
            facts = [f"akam/puram: {m.get('akam_puram')}", f"marker's thinai: {m.get('thinai')}"]
            if m.get("uri"):
                facts.append(f"uri: {m['uri']}")
            out.append("Marker's fields: " + "; ".join(facts))
            if m.get("uncertain"):
                out.append("The marker flagged this verse's sense as uncertain.")
            return out
        n = self.nodes[vid]
        num = int(vid.split(":")[1])
        if b == "kural":
            head = f"Kural {num}"
        elif b == "naladiyar":
            head = f"Naladiyar {num}"
        elif b == "tirumanthiram":
            r = self.tm.get(num, {})
            head = f"Tirumanthiram {num} (tantra {r.get('tantra')}, {r.get('chapter')})"
        elif b == "thiruppugazh":
            head = f"Thiruppugazh {num} ({self.tp.get(num, {}).get('heading')})"
        else:
            head = f"Siddhar {num} ({n.get('siddhar')}, {n.get('work_title')})"
        out = [f"### {vid}: {head}", "Tamil: " + " / ".join(n["tamil"])]
        if b in ("kural", "naladiyar") and n.get("pope"):
            p = n["pope"]
            out.append("Pope: " + (p.get("gloss") or " / ".join(p.get("couplet", [])) if isinstance(p, dict) else p))
        out.append(f"Marked reading: {n.get('reading')}")
        if n.get("nuance"):
            out.append(f"Marker's nuance: {n['nuance']}")
        if n.get("uncertain"):
            out.append("The marker flagged this verse's sense as uncertain.")
        return out

    def exists(self, vid):
        b = book_of(vid)
        if b in SANGAM:
            try:
                self.sangam_text(vid)
                return True
            except (KeyError, IndexError):
                return False
        return vid in self.nodes


def colophon_line(col):
    return "COLOPHON: " + " | ".join(f"{k}: {col[k] if col[k] is not None else '-'}" for k in ("thinai", "thurai", "poet", "patron"))


def split_note(note):
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z])", note.strip())
    if len(parts) < 2:
        return None
    return " ".join(parts[:-1]), parts[-1]


def calibration_pool(rng):
    pool = {g: [] for g in ("sound", "weak", "forced", "wrong")}
    for b in ("kural", "naladiyar"):
        for e in read_jsonl(ROOT / "kg" / b / "edges.jsonl"):
            if "audit" not in e or "note" not in e or e["audit"] not in pool:
                continue
            if b == "naladiyar" and not e.get("cross_book"):
                continue
            sp = split_note(e["note"])
            if sp:
                pool[e["audit"]].append(e | {"_note": sp[0], "_teaches": sp[1]})
    for g in pool:
        rng.shuffle(pool[g])
    return pool


def tags_of(m):
    u, i = m.get("ullurai"), m.get("iraicchi")
    return {"ullurai_present": bool(u), "iraicchi_present": bool(i),
            "ullurai_vehicle": [[v.get("form"), v.get("line")] for v in (u or {}).get("vehicle", [])] if u else None,
            "iraicchi_carrier": [i["carrier"].get("form"), i["carrier"].get("line")] if i and i.get("carrier") else None,
            "ullurai": u, "iraicchi": i}


def main():
    out, chs, seed = parse_args(sys.argv[1:])
    rng = random.Random(seed)
    corpus = Corpus()
    props, poems = [], []
    for book, c in chs:
        p = THEMES / book / f"ch{c:03d}.json"
        if not p.exists():
            usage(f"{p} does not exist")
        d = json.loads(p.read_text(encoding="utf-8"))
        for l in d.get("links", []):
            a, b = ref(book, l["a"]), ref(book, l["b"])
            for v in (a, b):
                if not corpus.exists(v):
                    sys.exit(f"error: {p.name}: link end {v} not found in the corpus")
            ga, gb = GROUP[book_of(a)], GROUP[book_of(b)]
            props.append({"a": a, "b": b, "type": l["type"].lower(), "note": l["note"],
                          "teaches": l.get("teaches"), "kind": "proposal", "book": book, "chapter": c,
                          "target_book": book_of(b), "group_a": ga, "group_b": gb,
                          "within_group": ga == gb})
        for k, v in d.get("verses", {}).items():
            if v.get("akam_puram") in ("akam", "mixed"):
                poems.append({"id": ref(book, k), "kind": "retag", "book": book, "chapter": c,
                              "akam_puram": v.get("akam_puram")} | tags_of(v))
    if not props and not poems:
        sys.exit("error: nothing to grade in those chapters")
    rng.shuffle(props)
    rng.shuffle(poems)
    n = max(1, math.ceil(len(props) / PER_PACKET))
    link_packets = [props[i::n] for i in range(n)]
    # spread the poems so a poem's marked reading is not printed in Part A of its own packet, if possible
    poem_packets = [[] for _ in range(n)]
    for q in poems:
        free = [i for i in range(n) if all(q["id"] not in (l["a"], l["b"]) for l in link_packets[i])]
        i = min(free or range(n), key=lambda i: len(poem_packets[i]))
        poem_packets[i].append(q | {"reading_in_own_packet": not free})
    pool = calibration_pool(rng)
    out.mkdir(parents=True, exist_ok=True)
    key, mixi = [], 0
    for pi, (pk, pp) in enumerate(zip(link_packets, poem_packets), 1):
        ncal = math.ceil(CAL_PER_40 * len(pk) / PER_PACKET) if pk else 0
        for _ in range(ncal):
            g = CAL_MIX[mixi % len(CAL_MIX)]
            mixi += 1
            e = pool[g].pop() if pool[g] else pool["weak"].pop()
            ga, gb = GROUP[book_of(e["s"])], GROUP[book_of(e["o"])]
            pk.append({"a": e["s"], "b": e["o"], "type": e["p"].lower(), "note": e["_note"],
                       "teaches": e["_teaches"], "kind": "calibration", "known": e["audit"],
                       "teaches_derived": True, "book": book_of(e["s"]), "target_book": book_of(e["o"]),
                       "group_a": ga, "group_b": gb, "within_group": ga == gb})
        rng.shuffle(pk)
        lines = [f"# Packet {pi}", "",
                 f"Part A: {len(pk)} links. Part B: {len(pp)} poems.",
                 "Write one JSON object: {\"links\": [one object per LINK, in order], "
                 "\"poems\": [one object per POEM, in order]}, in the formats of docs/sangam-grader-brief.md.", ""]
        lines += [f"# Part A: links ({len(pk)})", ""]
        for j, l in enumerate(pk, 1):
            lines += [f"## LINK {l['a']} -> {l['b']} type={l['type'].upper()}",
                      f"Note: {l['note']}", f"Teaches: {l['teaches']}", ""]
            lines += corpus.block(l["a"]) + [""] + corpus.block(l["b"]) + [""]
            key.append(l | {"packet": pi, "part": "A", "order": j})
        if pp:
            lines += [f"# Part B: blind re-tag of ullurai and iraicchi ({len(pp)} poems)", ""]
            for j, q in enumerate(pp, 1):
                title, tl, col, _ = corpus.sangam_text(q["id"])
                lines += [f"## POEM {q['id']} ({title})",
                          colophon_line(col)]
                lines += [f"{i:4} {t}" for i, t in tl] + [""]
                key.append(q | {"packet": pi, "part": "B", "order": j})
        (out / f"packet_{pi}.md").write_text("\n".join(lines), encoding="utf-8")
        print(f"packet_{pi}.md: {len(pk)} links ({ncal} calibration), {len(pp)} poems")
    (out / "key.json").write_text(json.dumps(key, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(props)} proposed links and {len(poems)} akam poems in {n} packets -> {out}")


if __name__ == "__main__":
    main()
