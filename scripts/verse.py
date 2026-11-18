#!/usr/bin/env python3
"""Print verses from any marked book: Tamil, reading, nuance and concepts.

    verse.py kural:1061 naladiyar:42 tirumanthiram:1823 thiruppugazh:355

Readings come from each book's built graph (kg/<book>/nodes.jsonl), so a book must be built first.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ("kural", "naladiyar", "tirumanthiram", "thiruppugazh")


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def main():
    wanted = sys.argv[1:]
    if not wanted:
        sys.exit(__doc__)
    books = {w.split(":")[0] for w in wanted}
    unknown = books - set(BOOKS)
    if unknown:
        sys.exit(f"unknown book: {', '.join(sorted(unknown))}; use one of {', '.join(BOOKS)}")
    nodes, concepts, chapters = {}, {}, {}
    for book in books:
        for n in read_jsonl(ROOT / "kg" / book / "nodes.jsonl"):
            if n["type"] in ("Verse", "Chapter"):
                nodes[n["id"]] = n
        for e in read_jsonl(ROOT / "kg" / book / "edges.jsonl"):
            if e["p"] == "EXPRESSES":
                concepts.setdefault(e["s"], []).append(e["o"].split(":")[1])
            elif e["p"] == "IN_CHAPTER":
                chapters[e["s"]] = e["o"]
    for w in wanted:
        n = nodes.get(w)
        if not n:
            print(f"## {w}: not found\n"); continue
        ch = nodes.get(chapters.get(w), {})
        print(f"## {w} (chapter {ch.get('number')}, {ch.get('title')})")
        print("\n".join(n["tamil"]))
        pope = n.get("pope")
        if pope:
            print("Pope:", pope["gloss"] if isinstance(pope, dict) else pope)
        print("Reading:", n["reading"])
        if n.get("nuance"):
            print("Nuance:", n["nuance"])
        print("Concepts:", ", ".join(concepts.get(w, [])))
        if n.get("uncertain"):
            print("(marked uncertain)")
        print()


if __name__ == "__main__":
    main()
