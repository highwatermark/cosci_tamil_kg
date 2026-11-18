#!/usr/bin/env python3
"""Build the Naladiyar graph from its chapter marks and link grades.

Writes kg/naladiyar/nodes.jsonl and kg/naladiyar/edges.jsonl. Verse ids are naladiyar:N, and links
to the Kural point at kural:N, the ids used in kg/kural/. Concepts are the shared ones in
kg/themes/concepts.json, so concept:<id> nodes are the same across books.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKS_DIR = ROOT / "kg" / "themes" / "naladiyar"
OUT_DIR = ROOT / "kg" / "naladiyar"
COMMENTATORS = ("mudaliar", "shanmuganar")


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")


def ref(target):
    return target if str(target).startswith("kural:") else f"naladiyar:{target}"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    verses = {r["verse"]: r for r in read_jsonl(ROOT / "kg" / "core" / "naladiyar.jsonl")}
    audit = json.loads((OUT_DIR / "link_audit.json").read_text(encoding="utf-8"))
    grades = {(ref(g["a"]), ref(g["b"])): g for g in audit["links"]}
    nodes, edges = [], []
    for name in COMMENTATORS:
        nodes.append({"id": f"commentator:{name}", "type": "Commentator", "label": name})
    for path in sorted(MARKS_DIR.glob("ch*.json")):
        chapter = json.loads(path.read_text(encoding="utf-8"))
        number = chapter["chapter_no"]
        first = next(int(k) for k in chapter["verses"])
        chapter_id = f"naladiyar-chapter:{number}"
        nodes.append({"id": chapter_id, "type": "Chapter", "book": "naladiyar", "number": number,
                      "title": verses[first]["chapter"], "section": verses[first]["section"],
                      "theme": chapter["chapter_theme"], "status": "proposed",
                      "structure_note": chapter.get("structure_note", ""),
                      "source_issues": chapter.get("source_issues", [])})
        for key, mark in chapter["verses"].items():
            n = int(key)
            verse_id = f"naladiyar:{n}"
            pope = verses[n].get("pope")
            nodes.append({"id": verse_id, "type": "Verse", "book": "naladiyar", "number": n,
                          "tamil": verses[n]["tamil"], "pope": pope["text"] if pope else "",
                          "reading": mark["reading"], "nuance": mark.get("nuance", ""),
                          "contested": bool(mark.get("contested")),
                          "uncertain": bool(mark.get("uncertain")), "status": "proposed"})
            edges.append({"s": verse_id, "p": "IN_CHAPTER", "o": chapter_id})
            for rank, concept in enumerate(mark["concepts"], 1):
                edges.append({"s": verse_id, "p": "EXPRESSES", "o": f"concept:{concept}", "rank": rank,
                              "basis": "interpretation", "status": "proposed"})
            for position in mark.get("positions", []):
                edges.append({"s": f"commentator:{position['by']}", "p": "READS", "o": verse_id,
                              "position": position["position"], "quote": position["quote"],
                              "basis": "commentator", "status": "proposed"})
        for link in chapter.get("links", []):
            s, o = ref(link["a"]), ref(link["b"])
            grade = grades.get((s, o), {})
            edge = {"s": s, "p": link["type"].upper(), "o": o, "note": link["note"],
                    "basis": "interpretation", "status": "proposed",
                    "audit": grade.get("grade", "not_audited"), "source": "naladiyar_marks",
                    "cross_book": o.startswith("kural:")}
            if grade.get("better_type"):
                edge["audit_better_type"] = grade["better_type"]
            edges.append(edge)
    write_jsonl(OUT_DIR / "nodes.jsonl", nodes)
    write_jsonl(OUT_DIR / "edges.jsonl", edges)
    links = [e for e in edges if "note" in e]
    print(f"nodes={len(nodes)} edges={len(edges)} links={len(links)} "
          f"not_audited={sum(e['audit'] == 'not_audited' for e in links)}")


if __name__ == "__main__":
    main()
