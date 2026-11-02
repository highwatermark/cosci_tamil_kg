#!/usr/bin/env python3
"""Build the Kural graph from the validated chapter marks.

Writes kg/kural/nodes.jsonl and kg/kural/edges.jsonl, plus
kg/core/verse_text_flags.jsonl, which compares the verse text of the base edition
with Kalaignar's and with agents' reports, so that likely corruptions can be reviewed.
The base text is never changed.
"""
import difflib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = ROOT / "kg" / "core"
THEMES_DIR = ROOT / "kg" / "themes"
OUT_DIR = ROOT / "kg" / "kural"
MIN_EDITION_MATCH = 0.45
WORD_END_TOLERANCE = 2
MIN_MATCH_LETTERS = 3
REPORTED_TEXT_ISSUE = re.compile(r"verse text|verse reads|kural\\.jsonl|kg/core|verse's|corrupt|misprint|typo", re.I)
COMMENTARY_ISSUE = re.compile(r"parimelazhagar|manakkudavar|kalaignar|gloss|commentary|pope", re.I)
NON_TAMIL = re.compile(r"[^஀-௿]")


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")


def grams(text):
    letters = NON_TAMIL.sub("", text)
    return {letters[i:i + 3] for i in range(len(letters) - 2)}


def edition_verses(doc_names, verses):
    """Find each verse's own text in another edition: its most similar line pair."""
    index, verse_grams = {}, {}
    for number, verse in verses.items():
        verse_grams[number] = grams("".join(verse["tamil"]))
        for gram in verse_grams[number]:
            index.setdefault(gram, set()).add(number)
    best = {}
    for doc in doc_names:
        text = (ROOT / "data" / "text" / f"{doc}.txt").read_text(encoding="utf-8")
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        for first, second in zip(lines, lines[1:]):
            candidate = grams(first + second)
            if not 12 <= len(candidate) <= 90:
                continue
            counts = {}
            for gram in candidate:
                for number in index.get(gram, ()):
                    counts[number] = counts.get(number, 0) + 1
            for number in sorted(counts, key=counts.get, reverse=True)[:2]:
                score = len(candidate & verse_grams[number]) / len(candidate | verse_grams[number])
                if score >= MIN_EDITION_MATCH and score > best.get(number, (0,))[0]:
                    best[number] = (score, [re.sub(r"^\d+\.\s*|[\s.]*\(?\d+\)?$", "", first),
                                            re.sub(r"[\s.]*\(?\d+\)?$", "", second)])
    return {number: pair for number, (_, pair) in best.items()}


def agent_reported_verses():
    """Verses whose text the marking agents reported as faulty in a chapter's source issues."""
    reported = {}
    for path in sorted((THEMES_DIR / "kural").glob("ch*.json")):
        chapter = json.loads(path.read_text(encoding="utf-8"))
        numbers = {int(key) for key in chapter["verses"]}
        for issue in chapter.get("source_issues", []):
            if REPORTED_TEXT_ISSUE.search(issue):
                for number in map(int, re.findall(r"\b\d{1,4}\b", issue)):
                    if number in numbers:
                        reported.setdefault(number, []).append(issue)
    regrade = json.loads((OUT_DIR / "link_audit.json").read_text(encoding="utf-8"))
    for link in regrade["links"]:
        issue = link.get("text_issue")
        if not issue or COMMENTARY_ISSUE.search(issue):
            continue
        for number in {int(n) for n in re.findall(r"\b\d{1,4}\b", issue)} & {link["a"], link["b"]}:
            if issue not in reported.get(number, []):
                reported.setdefault(number, []).append(issue)
    return reported


def suspect_words(base, other):
    """Base words missing from the other edition, allowing for sound changes where words join.

    Those changes alter a word's start or end, so a word passes if its start, end or
    middle occurs in the other edition."""
    other_letters = NON_TAMIL.sub("", "".join(other))
    suspects = []
    for word in " ".join(base).split():
        letters = NON_TAMIL.sub("", word)
        tolerance = WORD_END_TOLERANCE
        parts = [letters[:-tolerance], letters[tolerance:], letters[tolerance:-tolerance]]
        parts = [part for part in parts if len(part) >= MIN_MATCH_LETTERS]
        if parts and not any(part in other_letters for part in parts):
            suspects.append(word)
    return suspects


def text_flags(verses):
    """List verses to review. Kalaignar's edition is the independent witness here, because
    the Parimelazhagar file shares the base edition's errors. This is triage, not proof:
    a difference may be a real textual variant."""
    kalaignar = edition_verses(["pmuni0612"], verses)
    reported = agent_reported_verses()
    flags = []
    for number, verse in sorted(verses.items()):
        other = kalaignar.get(number)
        suspects = suspect_words(verse["tamil"], other) if other else []
        issues = reported.get(number, [])
        flags.append({"verse": number, "base": verse["tamil"], "kalaignar_edition": other,
                      "suspect_words": suspects, "agent_reports": issues,
                      "review": bool(suspects or issues or not other)})
    write_jsonl(CORE_DIR / "verse_text_flags.jsonl", flags)
    return {f["verse"]: f for f in flags}


def apply_audits(edges):
    """Record audit grades on the links they cover. Unaudited links have no grade."""
    grades = {}
    sample = json.loads((THEMES_DIR / "audit_kural.json").read_text(encoding="utf-8"))
    for link in sample["links"]:
        grades[(link["s"], link["o"])] = link["grade"]
    focused = json.loads((OUT_DIR / "thread_audit.json").read_text(encoding="utf-8"))
    for link in focused["links"]:
        grades[(f"kural:{link['a']}", f"kural:{link['b']}")] = link["grade"]
    better = {}
    regrade = json.loads((OUT_DIR / "link_audit.json").read_text(encoding="utf-8"))
    for link in regrade["links"]:
        pair = (f"kural:{link['a']}", f"kural:{link['b']}")
        grades.setdefault(pair, link["grade"])
        if link.get("better_type"):
            better[pair] = link["better_type"]
    for edge in edges:
        if "note" in edge:
            edge["audit"] = grades.get((edge["s"], edge["o"]), "not_audited")
            if (edge["s"], edge["o"]) in better:
                edge["audit_better_type"] = better[(edge["s"], edge["o"])]


def write_thread_review(threads, edge_pairs, verses):
    lines = ["# Kural threads for review", "",
             "These threads were drawn from tensions marked across all 133 chapters, then audited "
             "link by link. Only links graded sound appear here, and claims were rewritten to fit "
             "them. A separate AI did the grading: no Tamil scholar has reviewed this.", ""]
    for thread in threads:
        grade = thread["audit_grade"].replace("_", " ")
        lines += [f"## {thread['title']}", "", thread["claim"], "", f"*Audit: {grade}.*", ""]
        for first, second in thread["links"]:
            link = edge_pairs[(f"kural:{first}", f"kural:{second}")]
            for number in (first, second):
                lines.append(f"- **{number}** ({verses[number]['chapter']}): "
                             + " / ".join(verses[number]["tamil"]))
            lines += [f"  - {link['note']}", ""]
    (OUT_DIR / "THREADS.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    verses = {r["verse"]: r for r in read_jsonl(CORE_DIR / "kural.jsonl")}
    flags = text_flags(verses)
    concepts = json.loads((THEMES_DIR / "concepts.json").read_text(encoding="utf-8"))
    nodes, edges = [], []
    for concept in concepts:
        nodes.append({"id": f"concept:{concept['id']}", "type": "Concept", "status": "proposed",
                      **{k: v for k, v in concept.items() if k != "id"}})
    for name in ("parimelazhagar", "manakkudavar", "kalaignar"):
        nodes.append({"id": f"commentator:{name}", "type": "Commentator", "label": name})

    for path in sorted((THEMES_DIR / "kural").glob("ch*.json")):
        chapter = json.loads(path.read_text(encoding="utf-8"))
        chapter_id = f"chapter:{chapter['chapter_no']}"
        first = next(int(key) for key in chapter["verses"])
        nodes.append({"id": chapter_id, "type": "Chapter", "number": chapter["chapter_no"],
                      "title": verses[first]["chapter"], "section": verses[first]["section"],
                      "theme": chapter["chapter_theme"], "status": "proposed",
                      "structure_note": chapter.get("structure_note", ""),
                      "source_issues": chapter.get("source_issues", [])})
        for key, mark in chapter["verses"].items():
            number = int(key)
            verse_id = f"kural:{number}"
            nodes.append({"id": verse_id, "type": "Verse", "number": number,
                          "tamil": verses[number]["tamil"], "pope": verses[number]["pope"],
                          "reading": mark["reading"], "nuance": mark.get("nuance", ""),
                          "contested": bool(mark.get("contested")),
                          "uncertain": bool(mark.get("uncertain")),
                          "text_needs_review": flags[number]["review"], "status": "proposed"})
            edges.append({"s": verse_id, "p": "IN_CHAPTER", "o": chapter_id})
            for rank, concept_id in enumerate(mark["concepts"], 1):
                edges.append({"s": verse_id, "p": "EXPRESSES", "o": f"concept:{concept_id}",
                              "rank": rank, "basis": "interpretation", "status": "proposed"})
            for position in mark.get("positions", []):
                edges.append({"s": f"commentator:{position['by']}", "p": "READS", "o": verse_id,
                              "position": position["position"], "quote": position["quote"],
                              "basis": "commentator", "status": "proposed"})
        for link in chapter.get("links", []):
            edges.append({"s": f"kural:{link['a']}", "p": link["type"].upper(),
                          "o": f"kural:{link['b']}", "note": link["note"],
                          "basis": "interpretation", "status": "proposed"})
    apply_audits(edges)
    edge_pairs = {(e["s"], e["o"]): e for e in edges if "note" in e}
    threads = json.loads((OUT_DIR / "threads.json").read_text(encoding="utf-8"))
    missing = []
    for thread in threads:
        nodes.append({"id": thread["id"], "type": "Thread", "title": thread["title"],
                      "claim": thread["claim"], "basis": "interpretation", "status": "proposed",
                      "audit_grade": thread["audit_grade"]})
        for first, second in thread["links"]:
            link = edge_pairs.get((f"kural:{first}", f"kural:{second}"))
            if link is None:
                missing.append(f"{thread['id']}: no link {first}-{second}")
                continue
            edges.append({"s": thread["id"], "p": "INCLUDES_LINK", "o": f"kural:{first}",
                          "other": f"kural:{second}", "type": link["p"]})
    if missing:
        raise SystemExit("\n".join(missing))
    write_thread_review(threads, edge_pairs, verses)
    write_jsonl(OUT_DIR / "nodes.jsonl", nodes)
    write_jsonl(OUT_DIR / "edges.jsonl", edges)
    print(f"nodes={len(nodes)} edges={len(edges)} "
          f"text_review={sum(f['review'] for f in flags.values())}")


if __name__ == "__main__":
    main()
