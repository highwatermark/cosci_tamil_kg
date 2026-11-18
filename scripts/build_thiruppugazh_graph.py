#!/usr/bin/env python3
"""Build the Thiruppugazh graph from its chapter marks and link grades.

Writes kg/thiruppugazh/nodes.jsonl and kg/thiruppugazh/edges.jsonl. Song ids are thiruppugazh:N and
chapters thiruppugazh-chapter:N (running numbers 1..261, shrine headings split into runs of at most
15 songs). Links to other books point at kural:N, naladiyar:N and tirumanthiram:N. Concepts are the
shared ones in kg/themes/concepts.json. There is no commentary in the corpus, so no READS edges.
A chapter's section groups the shrines: the opening invocations, the six abodes of Murugan, other
shrines, and the general songs.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKS_DIR = ROOT / "kg" / "themes" / "thiruppugazh"
OUT_DIR = ROOT / "kg" / "thiruppugazh"
SIX_ABODES = {"திருப்பரங்குன்றம்", "திருச்செந்தூர்", "பழநி", "சுவாமி மலை", "திருத்தணிகை", "குன்றுதோறாடல்",
              "ஆறு திருப்பதி", "பழமுதிர்சோலை"}


def section(r):
    if r["kind"] in ("invocation", "opening"):
        return "காப்பு, நூல்"
    if r["heading"] in SIX_ABODES:
        return "அறுபடை வீடு"
    if r["kind"] in ("general", "new"):
        return "பொதுப்பாடல்கள்"
    return "பிற தலங்கள்"


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")


def ref(target):
    return target if isinstance(target, str) and ":" in target else f"thiruppugazh:{target}"


def main():
    verses = {r["number"]: r for r in read_jsonl(ROOT / "kg" / "core" / "thiruppugazh.jsonl")}
    audit = json.loads((OUT_DIR / "link_audit.json").read_text(encoding="utf-8"))
    grades = {(ref(g["a"]), ref(g["b"])): g for g in audit["links"]}
    nodes, edges = [], []
    for path in sorted(MARKS_DIR.glob("ch*.json")):
        chapter = json.loads(path.read_text(encoding="utf-8"))
        number = chapter["chapter_no"]
        first = verses[min(int(k) for k in chapter["verses"])]
        chapter_id = f"thiruppugazh-chapter:{number}"
        nodes.append({"id": chapter_id, "type": "Chapter", "book": "thiruppugazh", "number": number,
                      "title": first["heading"], "section": section(first), "part": first["part"],
                      "theme": chapter["chapter_theme"], "status": "proposed",
                      "structure_note": chapter.get("structure_note", ""),
                      "source_issues": chapter.get("source_issues", [])})
        for key, mark in chapter["verses"].items():
            n = int(key)
            verse_id = f"thiruppugazh:{n}"
            nodes.append({"id": verse_id, "type": "Verse", "book": "thiruppugazh", "number": n,
                          "tamil": verses[n]["tamil"], "pope": "",
                          "reading": mark["reading"], "nuance": mark.get("nuance", ""),
                          "contested": False, "uncertain": bool(mark.get("uncertain")),
                          "text_needs_review": bool(verses[n].get("corrupt_chars")), "status": "proposed"})
            edges.append({"s": verse_id, "p": "IN_CHAPTER", "o": chapter_id})
            for rank, concept in enumerate(mark["concepts"], 1):
                edges.append({"s": verse_id, "p": "EXPRESSES", "o": f"concept:{concept}", "rank": rank,
                              "basis": "interpretation", "status": "proposed"})
        for link in chapter.get("links", []):
            s, o = ref(link["a"]), ref(link["b"])
            grade = grades.get((s, o), {})
            edge = {"s": s, "p": link["type"].upper(), "o": o, "note": link["note"],
                    "basis": "interpretation", "status": "proposed",
                    "audit": grade.get("grade", "not_audited"), "source": "thiruppugazh_marks",
                    "cross_book": not o.startswith("thiruppugazh:")}
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
