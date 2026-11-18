#!/usr/bin/env python3
"""Build site/nilai.html from the template and the appendix data drawn from the graph.

    build.py    regenerates site/appendix.json from kg/ and writes site/nilai.html
"""
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ("kural", "naladiyar", "tirumanthiram", "thiruppugazh")


def appendix():
    concepts = {c["id"]: c for c in json.loads((ROOT / "kg/themes/concepts.json").read_text(encoding="utf-8"))}
    counts = collections.defaultdict(lambda: [0] * len(BOOKS))
    matrix, grades, verses, seen = collections.Counter(), collections.Counter(), collections.Counter(), set()
    for i, book in enumerate(BOOKS):
        for line in (ROOT / f"kg/{book}/nodes.jsonl").read_text(encoding="utf-8").splitlines():
            if json.loads(line)["type"] == "Verse":
                verses[book] += 1
        for line in (ROOT / f"kg/{book}/edges.jsonl").read_text(encoding="utf-8").splitlines():
            e = json.loads(line)
            if e["p"] == "EXPRESSES":
                counts[e["o"].split(":")[1]][i] += 1
            elif "note" in e and (e["s"], e["o"]) not in seen:
                seen.add((e["s"], e["o"]))
                grades[e["audit"]] += 1
                if e["audit"] == "sound":
                    a, b = sorted((e["s"].split(":")[0], e["o"].split(":")[0]), key=BOOKS.index)
                    matrix[f"{a}|{b}"] += 1
    rows = [[k, concepts[k]["tamil"], concepts[k]["gloss"], v]
            for k, v in sorted(counts.items(), key=lambda kv: -sum(kv[1])) if k in concepts]
    return {"verses": dict(verses), "links": sum(grades.values()), "grades": dict(grades),
            "matrix": dict(matrix), "concepts": rows}


def main():
    data = appendix()
    (ROOT / "site/appendix.json").write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    html = (ROOT / "site/nilai.template.html").read_text(encoding="utf-8")
    html = html.replace("/*APPENDIX*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    (ROOT / "site/nilai.html").write_text(html, encoding="utf-8")
    # A full document for local preview; the published artifact gets its own skeleton.
    (ROOT / "site/preview.html").write_text('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"></head><body>'
        + html + "</body></html>", encoding="utf-8")
    print(f"site/nilai.html: {len(html.encode())} bytes, {len(data['concepts'])} concepts, {data['links']} links")


if __name__ == "__main__":
    main()
