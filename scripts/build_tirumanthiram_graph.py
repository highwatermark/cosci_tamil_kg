#!/usr/bin/env python3
"""Build the Tirumanthiram graph from its chapter marks and link grades.

Writes kg/tirumanthiram/nodes.jsonl and kg/tirumanthiram/edges.jsonl. Verse ids are tirumanthiram:N
(the edition's verse numbers) and chapters tirumanthiram-chapter:N (running numbers 1..224). Links to
other books point at kural:N and naladiyar:N, the ids used in their graphs. Concepts are the shared
ones in kg/themes/concepts.json. There is no commentary in the corpus, so there are no READS edges.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKS_DIR = ROOT / "kg" / "themes" / "tirumanthiram"
OUT_DIR = ROOT / "kg" / "tirumanthiram"


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")


def ref(target):
    return target if isinstance(target, str) and ":" in target else f"tirumanthiram:{target}"


def main():
    verses = {r["number"]: r for r in read_jsonl(ROOT / "kg" / "core" / "tirumanthiram.jsonl")}
    audit = json.loads((OUT_DIR / "link_audit.json").read_text(encoding="utf-8"))
    grades = {(ref(g["a"]), ref(g["b"])): g for g in audit["links"]}
    nodes, edges = [], []
    for path in sorted(MARKS_DIR.glob("ch*.json")):
        chapter = json.loads(path.read_text(encoding="utf-8"))
        number = chapter["chapter_no"]
        first = verses[min(int(k) for k in chapter["verses"])]
        chapter_id = f"tirumanthiram-chapter:{number}"
        nodes.append({"id": chapter_id, "type": "Chapter", "book": "tirumanthiram", "number": number,
                      "title": first["chapter"], "section": first.get("tantra_name") or "பாயிரம்",
                      "tantra": first["tantra"], "theme": chapter["chapter_theme"], "status": "proposed",
                      "structure_note": chapter.get("structure_note", ""),
                      "source_issues": chapter.get("source_issues", [])})
        for key, mark in chapter["verses"].items():
            n = int(key)
            verse_id = f"tirumanthiram:{n}"
            nodes.append({"id": verse_id, "type": "Verse", "book": "tirumanthiram", "number": n,
                          "tamil": verses[n]["tamil"], "pope": "",
                          "reading": mark["reading"], "nuance": mark.get("nuance", ""),
                          "contested": False, "uncertain": bool(mark.get("uncertain")),
                          "text_needs_review": bool(verses[n].get("corrupt_lines")), "status": "proposed"})
            edges.append({"s": verse_id, "p": "IN_CHAPTER", "o": chapter_id})
            for rank, concept in enumerate(mark["concepts"], 1):
                edges.append({"s": verse_id, "p": "EXPRESSES", "o": f"concept:{concept}", "rank": rank,
                              "basis": "interpretation", "status": "proposed"})
        for link in chapter.get("links", []):
            s, o = ref(link["a"]), ref(link["b"])
            grade = grades.get((s, o), {})
            edge = {"s": s, "p": link["type"].upper(), "o": o, "note": link["note"],
                    "basis": "interpretation", "status": "proposed",
                    "audit": grade.get("grade", "not_audited"), "source": "tirumanthiram_marks",
                    "cross_book": not o.startswith("tirumanthiram:")}
            if grade.get("better_type"):
                edge["audit_better_type"] = grade["better_type"]
            if grade.get("text_issue"):
                edge["audit_text_issue"] = grade["text_issue"]
            edges.append(edge)
    write_jsonl(OUT_DIR / "nodes.jsonl", nodes)
    write_jsonl(OUT_DIR / "edges.jsonl", edges)
    links = [e for e in edges if "note" in e]
    print(f"nodes={len(nodes)} edges={len(edges)} links={len(links)} "
          f"not_audited={sum(e['audit'] == 'not_audited' for e in links)}")


if __name__ == "__main__":
    main()
