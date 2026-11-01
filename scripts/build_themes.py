#!/usr/bin/env python3
"""Build the theme layer of the knowledge graph and a readable review file.

Reads kg/core/kural.jsonl, kg/themes/pilot_source.json and, when present,
kg/themes/blind_grades.json. The build stops if a quote is not found exactly
in the cited text, or if a claim has no stated basis.

Writes:
  kg/themes/nodes.jsonl  kg/themes/edges.jsonl
  kg/themes/THREADS.md   threads, with evidence, for human review
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT_DIR = ROOT / "data" / "text"
THEMES_DIR = ROOT / "kg" / "themes"
BASES = {"text", "commentator", "interpretation"}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    source = load(THEMES_DIR / "pilot_source.json")
    blind = load(THEMES_DIR / "blind_readings.json")["readings"]
    grades_path = THEMES_DIR / "blind_grades.json"
    grades = load(grades_path)["grades"] if grades_path.exists() else {}
    kural = {f"kural:{r['verse']}": r for r in
             (json.loads(line) for line in
              (ROOT / "kg" / "core" / "kural.jsonl").read_text(encoding="utf-8").splitlines())}
    errors = []
    texts = {}

    def find(doc, quote, what):
        if doc not in texts:
            texts[doc] = (TEXT_DIR / f"{doc}.txt").read_text(encoding="utf-8")
        pattern = r"\s+".join(re.escape(part) for part in quote.split())
        match = re.search(pattern, texts[doc])
        if not match:
            errors.append(f"{what}: quote not found in {doc}: {quote}")
            return -1
        return match.start()

    concepts = {c["id"]: c for c in source["concepts"]}
    nodes, edges = [], []
    passages = {}
    for concept in source["concepts"]:
        nodes.append({"id": f"concept:{concept['id']}", "type": "Concept", "layer": "themes",
                      "status": "proposed", **{k: v for k, v in concept.items() if k != "id"}})
    for passage in source["passages"]:
        offset = find(passage["doc"], passage["quote"], passage["id"])
        passages[passage["id"]] = {**passage, "offset": offset}
        nodes.append({"id": passage["id"], "type": "Passage", "layer": "themes", **passage,
                      "offset": offset})

    def require_passage(reference, what):
        if reference in passages:
            return
        if reference in kural:
            record = kural[reference]
            quote = f"{record['tamil'][0]} {record['tamil'][1]}"
            offset = find("pmuni0001", quote, reference)
            passages[reference] = {"id": reference, "doc": "pmuni0001", "quote": quote,
                                   "work": f"திருக்குறள் {record['verse']}", "offset": offset}
            nodes.append({"id": reference, "type": "Passage", "layer": "themes",
                          **passages[reference], "chapter": record["chapter"],
                          "pope": record["pope"]})
            return
        errors.append(f"{what}: unknown passage {reference}")

    for reference, marked in source["verse_marks"].items():
        require_passage(reference, "verse mark")
        reading = blind.get(reference, {})
        grade = grades.get(reference, {})
        for concept_id in marked:
            if concept_id not in concepts:
                errors.append(f"{reference}: unknown concept {concept_id}")
            edges.append({"s": reference, "p": "EXPRESSES", "o": f"concept:{concept_id}",
                          "layer": "themes", "basis": "interpretation", "status": "proposed"})
        if reading:
            edges.append({"s": reference, "p": "READ_AS", "value": reading["reading"],
                          "layer": "themes", "basis": "interpretation", "status": "proposed",
                          "grade": grade.get("grade", "ungraded"),
                          "grade_reason": grade.get("reason", "")})

    for thread in source["threads"]:
        nodes.append({"id": thread["id"], "type": "Thread", "layer": "themes", "status": "proposed",
                      "title": thread["title"], "question": thread["question"],
                      "open_questions": thread["open_questions"]})
        for concept_id in thread["concepts"]:
            if concept_id not in concepts:
                errors.append(f"{thread['id']}: unknown concept {concept_id}")
            edges.append({"s": thread["id"], "p": "ABOUT", "o": f"concept:{concept_id}",
                          "layer": "themes", "status": "proposed"})
        for stance in thread["stances"]:
            require_passage(stance["passage"], thread["id"])
            if stance["basis"] not in BASES:
                errors.append(f"{thread['id']}: bad basis {stance['basis']}")
            edges.append({"s": thread["id"], "p": "HAS_STANCE", "o": stance["passage"],
                          "position": stance["position"], "basis": stance["basis"],
                          "layer": "themes", "status": "proposed"})
        for relation in thread["relations"]:
            require_passage(relation["a"], thread["id"])
            require_passage(relation["b"], thread["id"])
            if relation["basis"] not in BASES:
                errors.append(f"{thread['id']}: bad basis {relation['basis']}")
            edges.append({"s": relation["a"], "p": relation["type"].upper(), "o": relation["b"],
                          "thread": thread["id"], "note": relation["note"],
                          "basis": relation["basis"], "layer": "themes", "status": "proposed"})

    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(f"{len(errors)} theme marks failed validation; nothing written")

    def write_jsonl(path, records):
        with open(path, "w", encoding="utf-8") as out:
            for record in records:
                out.write(json.dumps(record, ensure_ascii=False) + "\n")

    write_jsonl(THEMES_DIR / "nodes.jsonl", nodes)
    write_jsonl(THEMES_DIR / "edges.jsonl", edges)

    lines = ["# Theme threads for review", "",
             "All entries are proposed. `text` means the verse says it directly, `commentator` "
             "means a named commentator says it, and `interpretation` is Claude's own reading, "
             "for a human reader to judge.", ""]
    for thread in source["threads"]:
        lines += [f"## {thread['title']}", "", f"*{thread['question']}*", "", "### Positions", ""]
        for stance in thread["stances"]:
            passage = passages[stance["passage"]]
            lines += [f"- **{passage['work']}** — {passage['quote']}",
                      f"  - {stance['position']} (`{stance['basis']}`)"]
        lines += ["", "### How they relate", ""]
        for relation in thread["relations"]:
            first, second = passages[relation["a"]]["work"], passages[relation["b"]]["work"]
            label = relation["type"].replace("_", " ")
            lines.append(f"- **{first} / {second}: {label}.** {relation['note']} "
                         f"(`{relation['basis']}`)")
        lines += ["", "### Open questions", ""]
        lines += [f"- {question}" for question in thread["open_questions"]]
        lines.append("")
    (THEMES_DIR / "THREADS.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"nodes={len(nodes)} edges={len(edges)} passages={len(passages)} "
          f"threads={len(source['threads'])} graded={len(grades)}")


if __name__ == "__main__":
    main()
