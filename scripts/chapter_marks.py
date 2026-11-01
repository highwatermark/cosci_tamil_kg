#!/usr/bin/env python3
"""Show a Kural chapter's sources, and validate its marks.

  chapter_marks.py show 38      print the chapter's verses and commentaries
  chapter_marks.py check 38 39  validate those chapters' marks in kg/themes/kural/
  chapter_marks.py check        validate every chapter that has marks

A chapter file is kg/themes/kural/ch038.json. See kg/themes/SCHEMA.md.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = ROOT / "kg" / "core"
MARKS_DIR = ROOT / "kg" / "themes" / "kural"
CONCEPTS = ROOT / "kg" / "themes" / "concepts.json"
COMMENTATORS = ("parimelazhagar", "manakkudavar", "kalaignar")
LINK_TYPES = {"tension", "agrees", "develops", "qualifies", "same_image", "parallel_domain"}
MAX_QUOTE_WORDS = {"parimelazhagar": 30, "manakkudavar": 30, "kalaignar": 14}
MAX_CONCEPTS = 4
VERSES_PER_CHAPTER = 10


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def squeeze(text):
    return re.sub(r"\s+", " ", text).strip()


def load_sources():
    verses = {r["verse"]: r for r in read_jsonl(CORE_DIR / "kural.jsonl")}
    commentaries = {r["verse"]: r for r in read_jsonl(CORE_DIR / "commentaries.jsonl")}
    return verses, commentaries


def show(chapter_no, verses, commentaries):
    numbers = [n for n, v in verses.items() if v["chapter_no"] == chapter_no]
    print(f"# Chapter {chapter_no}: {verses[numbers[0]]['chapter']} ({verses[numbers[0]]['section']})")
    for number in numbers:
        verse = verses[number]
        print(f"\n## {number}\n{verse['tamil'][0]}\n{verse['tamil'][1]}")
        print("POPE:", " / ".join(verse["pope"]["couplet"]), "||", verse["pope"]["gloss"])
        for name in COMMENTATORS:
            entry = commentaries[number].get(name)
            print(f"{name.upper()}:", squeeze(entry["text"]) if entry else "(not aligned)")


def check(chapter_no, verses, commentaries, vocabulary):
    errors = []
    path = MARKS_DIR / f"ch{chapter_no:03d}.json"
    if not path.exists():
        return [f"ch{chapter_no}: no marks file"], set()
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("chapter_no") != chapter_no:
        errors.append(f"ch{chapter_no}: wrong chapter_no")
    if not data.get("chapter_theme"):
        errors.append(f"ch{chapter_no}: no chapter_theme")
    known = set(vocabulary)
    new_ids = set()
    for concept in data.get("new_concepts", []):
        if not all(concept.get(key) for key in ("id", "tamil", "gloss", "label_source")):
            errors.append(f"ch{chapter_no}: incomplete new concept {concept}")
        new_ids.add(concept.get("id"))
    known |= new_ids

    expected = {str(n) for n, v in verses.items() if v["chapter_no"] == chapter_no}
    marked = data.get("verses", {})
    if set(marked) != expected:
        errors.append(f"ch{chapter_no}: verses differ: {sorted(expected ^ set(marked))}")
    for key, mark in marked.items():
        where = f"ch{chapter_no} verse {key}"
        if not mark.get("reading"):
            errors.append(f"{where}: no reading")
        concepts = mark.get("concepts", [])
        if not 1 <= len(concepts) <= MAX_CONCEPTS:
            errors.append(f"{where}: needs 1 to {MAX_CONCEPTS} concepts")
        errors += [f"{where}: unknown concept {c}" for c in concepts if c not in known]
        positions = mark.get("positions", [])
        if mark.get("contested") and len({p.get("by") for p in positions}) < 2:
            errors.append(f"{where}: contested needs positions from two commentators")
        for position in positions:
            name = position.get("by")
            if name not in COMMENTATORS:
                errors.append(f"{where}: unknown commentator {name}")
                continue
            quote = squeeze(position.get("quote", ""))
            entry = commentaries[int(key)].get(name) if key.isdigit() else None
            if not quote or not position.get("position"):
                errors.append(f"{where}: {name} needs a position and a quote")
            elif not entry or quote not in squeeze(entry["text"]):
                errors.append(f"{where}: quote not in {name}: {quote}")
            elif len(quote.split()) > MAX_QUOTE_WORDS[name]:
                errors.append(f"{where}: quote too long for {name}")
    for link in data.get("links", []):
        where = f"ch{chapter_no} link {link.get('a')}-{link.get('b')}"
        if link.get("type") not in LINK_TYPES:
            errors.append(f"{where}: unknown type {link.get('type')}")
        if link.get("a") not in verses or link.get("b") not in verses:
            errors.append(f"{where}: unknown verse")
        if not link.get("note"):
            errors.append(f"{where}: no note")
    return errors, new_ids


def main():
    verses, commentaries = load_sources()
    if len(sys.argv) < 2 or sys.argv[1] not in ("show", "check"):
        sys.exit(__doc__)
    chapters = [int(x) for x in sys.argv[2:]]
    if sys.argv[1] == "show":
        for chapter_no in chapters:
            show(chapter_no, verses, commentaries)
        return
    if not chapters:
        chapters = sorted(int(p.stem[2:]) for p in MARKS_DIR.glob("ch*.json"))
    vocabulary = {c["id"] for c in json.loads(CONCEPTS.read_text(encoding="utf-8"))}
    all_errors = []
    for chapter_no in chapters:
        errors, _ = check(chapter_no, verses, commentaries, vocabulary)
        all_errors += errors
    print("\n".join(all_errors) if all_errors else f"{len(chapters)} chapters valid")
    if all_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
