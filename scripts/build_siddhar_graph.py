#!/usr/bin/env python3
"""Build the Siddhar graph from its chapter marks and link grades.

Writes kg/siddhar/nodes.jsonl and kg/siddhar/edges.jsonl. Verse ids are siddhar:N, where N is the
unit's seq (its running number in kg/core/siddhar.jsonl); each verse node also carries the unit's own
id (siddhar:<work>:<label>), poet and work. Chapters are siddhar-chapter:N (book_marks.py's running
numbers, 1..142). Links to other books point at kural:N, naladiyar:N, tirumanthiram:N and
thiruppugazh:N. There is no commentary in the corpus, so there are no READS edges.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKS_DIR = ROOT / "kg" / "themes" / "siddhar"
OUT_DIR = ROOT / "kg" / "siddhar"


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")


def ref(target):
    return target if isinstance(target, str) and ":" in target else f"siddhar:{target}"


def main():
    units = {r["seq"]: r for r in read_jsonl(ROOT / "kg" / "core" / "siddhar.jsonl")}
    grades = {}
    if (OUT_DIR / "link_audit.json").exists():
        audit = json.loads((OUT_DIR / "link_audit.json").read_text(encoding="utf-8"))
        grades = {(ref(g["a"]), ref(g["b"])): g for g in audit["links"]}
    nodes, edges = [], []
    for path in sorted(MARKS_DIR.glob("ch*.json")):
        chapter = json.loads(path.read_text(encoding="utf-8"))
        number = chapter["chapter_no"]
        first = units[min(int(k) for k in chapter["verses"])]
        chapter_id = f"siddhar-chapter:{number}"
        nodes.append({"id": chapter_id, "type": "Chapter", "book": "siddhar", "number": number,
                      "title": first["work_title"], "section": first["siddhar"], "work": first["work"],
                      "theme": chapter["chapter_theme"], "status": "proposed",
                      "structure_note": chapter.get("structure_note", ""),
                      "source_issues": chapter.get("source_issues", [])})
        for key, mark in chapter["verses"].items():
            n = int(key)
            u = units[n]
            verse_id = f"siddhar:{n}"
            nodes.append({"id": verse_id, "type": "Verse", "book": "siddhar", "number": n,
                          "unit_id": u["id"], "siddhar": u["siddhar"], "work": u["work"], "work_title": u["work_title"],
                          "attribution": u.get("attribution"),
                          "tamil": u["tamil"], "pope": "",
                          "reading": mark["reading"], "nuance": mark.get("nuance", ""),
                          "contested": False, "uncertain": bool(mark.get("uncertain")),
                          "text_needs_review": False, "status": "proposed"})
            edges.append({"s": verse_id, "p": "IN_CHAPTER", "o": chapter_id})
            for rank, concept in enumerate(mark["concepts"], 1):
                edges.append({"s": verse_id, "p": "EXPRESSES", "o": f"concept:{concept}", "rank": rank,
                              "basis": "interpretation", "status": "proposed"})
        for link in chapter.get("links", []):
            s, o = ref(link["a"]), ref(link["b"])
            grade = grades.get((s, o), {})
            edge = {"s": s, "p": link["type"].upper(), "o": o, "note": link["note"],
                    "basis": "interpretation", "status": "proposed", "pass": "marking",
                    "audit": grade.get("grade", "not_audited"), "source": "siddhar_marks",
                    "cross_book": not o.startswith("siddhar:")}
            if grade.get("better_type"):
                edge["audit_better_type"] = grade["better_type"]
            if grade.get("text_issue"):
                edge["audit_text_issue"] = grade["text_issue"]
            edges.append(edge)
    OUT_DIR.mkdir(exist_ok=True)
    write_jsonl(OUT_DIR / "nodes.jsonl", nodes)
    write_jsonl(OUT_DIR / "edges.jsonl", edges)
    links = [e for e in edges if "note" in e]
    print(f"nodes={len(nodes)} edges={len(edges)} links={len(links)} "
          f"not_audited={sum(e['audit'] == 'not_audited' for e in links)}")


if __name__ == "__main__":
    main()
