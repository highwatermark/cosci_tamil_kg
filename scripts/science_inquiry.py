"""Validate the consciousness and measurement graph, or retrieve Tamil passages for review."""
import argparse
import json
import unicodedata
from collections import Counter
from pathlib import Path

KG = Path(__file__).resolve().parents[1] / "kg"
DATA = KG / "science/consciousness"
CORE = KG / "core"


def rows(path):
    with path.open(encoding="utf-8") as stream:
        yield from (json.loads(line) for line in stream if line.strip())


def units(book=None):
    for path in sorted(CORE.glob("*.jsonl")):
        name = path.stem.removesuffix("_units")
        if book and name != book:
            continue
        # Where a long poem is also divided into reading units, index the units once.
        if path.stem == name and (CORE / f"{name}_units.jsonl").exists():
            continue
        for record in rows(path):
            lines = record.get("tamil")
            if not isinstance(lines, list) or not lines or not all(isinstance(x, str) for x in lines):
                continue
            ident = record.get("id")
            if ident is None and name in {"kural", "naladiyar"}:
                ident = f"{name}:{record['verse']}"
            if ident:
                yield ident, lines


def folded(text):
    return "".join(
        ch for ch in unicodedata.normalize("NFC", text) if unicodedata.category(ch)[0] in "LMN")


def validate():
    sources = list(rows(DATA / "sources.jsonl"))
    by_source = {s["id"]: s for s in sources}
    assert len(by_source) == len(sources)
    assert all(s["url"].startswith("https://") and s["kind"] and s["claim"] for s in sources)
    edges = list(rows(DATA / "comparisons.jsonl"))
    questions = list(rows(DATA / "inquiries.jsonl"))
    used = {r["verse"] for r in questions}
    used.update(e[k] for e in edges for k in ("s", "o") if e[k] not in by_source)
    evidence = {i: lines for i, lines in units() if i in used}
    assert used == evidence.keys(), f"Unknown Tamil IDs: {used-evidence.keys()}"
    def check_anchor(i, anchor):
        assert anchor and any(anchor in line for line in evidence[i]), (i, anchor)
    for e in edges:
        assert e["comparison"] and e["limit"]
        if e["o"] in evidence:
            check_anchor(e["o"], e["target_anchor"])
        assert e["status"] in {"proposed", "withheld"}
        if e["s"] in evidence:
            check_anchor(e["s"], e["anchor"])
    for q in questions:
        check_anchor(q["verse"], q["anchor"])
        assert all(q[k] for k in ("topic","evidence","question","next_test","missing"))
    print(f"{len(sources)} sourced claims, {len(edges)} comparisons {dict(Counter(e['status'] for e in edges))}, "
          f"{len(questions)} research questions. All Tamil anchors verified.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    scan = sub.add_parser("scan", help="Count overlapping Tamil seed matches by field")
    scan.add_argument("--book")
    find = sub.add_parser("find", help="Any of the literal Tamil expressions, ignoring printed spacing")
    find.add_argument("terms", nargs="+")
    find.add_argument("--book")
    args = parser.parse_args()
    if args.cmd == "check":
        validate()
        return
    if args.cmd == "scan":
        lenses = json.loads((DATA / "search_lenses.json").read_text())
        keys = {name: [folded(t) for t in terms] for name, terms in lenses.items()}
        counts = Counter()
        books = Counter()
        total_hits = 0
        for ident, lines in units(args.book):
            books[ident.split(":")[0]] += 1
            text = folded(" ".join(lines))
            hits = [name for name, terms in keys.items() if any(t in text for t in terms)]
            counts.update(hits)
            total_hits += bool(hits)
        print(json.dumps(dict(units=sum(books.values()), books=len(books), any_match=total_hits,
                              by_lens={name: counts[name] for name in keys},
                              units_by_book=books), ensure_ascii=False, indent=2))
        return
    terms = {t: folded(t) for t in args.terms}
    if not all(terms.values()):
        parser.error("Enter a nonempty Tamil expression")
    for ident, lines in units(args.book):
        text = folded(" ".join(lines))
        matched = [t for t, key in terms.items() if key in text]
        if matched:
            print(json.dumps(dict(id=ident, matched=matched, tamil=lines), ensure_ascii=False))


if __name__ == "__main__":
    main()
