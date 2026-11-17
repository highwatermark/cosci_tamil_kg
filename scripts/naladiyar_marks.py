#!/usr/bin/env python3
"""Show a Naladiyar chapter's sources, and validate its marks.

  naladiyar_marks.py show 14      print the chapter's quatrains, Pope and both commentaries
  naladiyar_marks.py check 14 15  validate those chapters' marks in kg/themes/naladiyar/
  naladiyar_marks.py check        validate every chapter that has marks

A chapter file is kg/themes/naladiyar/ch014.json. The schema is kg/themes/SCHEMA.md, with two
differences: verse keys are Naladiyar numbers, and a link's `b` may name a Kural verse as
"kural:N". Commentators are mudaliar (1924) and shanmuganar (1970, modern: short quotes only).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = ROOT / "kg" / "core"
MARKS_DIR = ROOT / "kg" / "themes" / "naladiyar"
CONCEPTS = ROOT / "kg" / "themes" / "concepts.json"
COMMENTATORS = ("mudaliar", "shanmuganar")
LINK_TYPES = {"tension", "agrees", "develops", "qualifies", "same_image", "parallel_domain"}
MAX_QUOTE_WORDS = {"mudaliar": 30, "shanmuganar": 14}
MAX_CONCEPTS = 4
KURAL_VERSES = 1330


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def squeeze(text):
    return re.sub(r"\s+", " ", text or "").strip()


def load():
    return {r["verse"]: r for r in read_jsonl(CORE_DIR / "naladiyar.jsonl")}


def show(chapter_no, verses):
    numbers = [n for n, v in verses.items() if v["chapter_no"] == chapter_no]
    print(f"# Chapter {chapter_no}: {verses[numbers[0]]['chapter']} ({verses[numbers[0]]['section']})")
    for n in numbers:
        v = verses[n]
        print(f"\n## {n}\n" + "\n".join(v["tamil"]))
        pope = v.get("pope")
        print("POPE:", f"{pope['title']} || {pope['text']}" if pope else "(not aligned)")
        for name in COMMENTATORS:
            print(f"{name.upper()}:", squeeze(v.get(name)) or "(not aligned)")


def link_target_ok(target, verses):
    if isinstance(target, int):
        return target in verses
    m = re.fullmatch(r"kural:(\d+)", str(target))
    return bool(m) and 1 <= int(m.group(1)) <= KURAL_VERSES


def check(chapter_no, verses, vocabulary):
    errors = []
    path = MARKS_DIR / f"ch{chapter_no:03d}.json"
    if not path.exists():
        return [f"ch{chapter_no}: no marks file"]
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("chapter_no") != chapter_no:
        errors.append(f"ch{chapter_no}: wrong chapter_no")
    if not data.get("chapter_theme"):
        errors.append(f"ch{chapter_no}: no chapter_theme")
    known = set(vocabulary)
    for concept in data.get("new_concepts", []):
        if not all(concept.get(k) for k in ("id", "tamil", "gloss", "label_source")):
            errors.append(f"ch{chapter_no}: incomplete new concept {concept}")
        known.add(concept.get("id"))
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
            quote = squeeze(position.get("quote"))
            source = squeeze(verses[int(key)].get(name)) if key.isdigit() else ""
            if not quote or not position.get("position"):
                errors.append(f"{where}: {name} needs a position and a quote")
            elif quote not in source:
                errors.append(f"{where}: quote not in {name}: {quote}")
            elif len(quote.split()) > MAX_QUOTE_WORDS[name]:
                errors.append(f"{where}: quote too long for {name}")
    for link in data.get("links", []):
        where = f"ch{chapter_no} link {link.get('a')}-{link.get('b')}"
        if link.get("type") not in LINK_TYPES:
            errors.append(f"{where}: unknown type {link.get('type')}")
        if link.get("a") not in verses or not link_target_ok(link.get("b"), verses):
            errors.append(f"{where}: unknown verse")
        if not link.get("note"):
            errors.append(f"{where}: no note")
    return errors


def main():
    verses = load()
    if len(sys.argv) < 2 or sys.argv[1] not in ("show", "check"):
        sys.exit(__doc__)
    chapters = [int(x) for x in sys.argv[2:]]
    if sys.argv[1] == "show":
        for chapter_no in chapters:
            show(chapter_no, verses)
        return
    if not chapters:
        chapters = sorted(int(p.stem[2:]) for p in MARKS_DIR.glob("ch*.json"))
    vocabulary = {c["id"] for c in json.loads(CONCEPTS.read_text(encoding="utf-8"))}
    errors = [e for c in chapters for e in check(c, verses, vocabulary)]
    print("\n".join(errors) if errors else f"{len(chapters)} chapters valid")
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
