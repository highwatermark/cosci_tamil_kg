#!/usr/bin/env python3
"""Parse a translator's couplets from a PDF text dump into data/private/, which git ignores.

    parse_private_translation.py subramuniyaswami DUMP.txt

DUMP.txt comes from scripts/pdftext.swift. The translation is in copyright, so its text
stays on this machine: the graph records a translator's position in our own words only.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = re.compile(r"=== PAGE (\d+) \(\d+ chars\) ===\n")
CHAPTER_HEAD = re.compile(r"CHAPTER (\d+)\b")
HEAD_CHARS = 40


def subramuniyaswami(dump):
    """Chapter pages open with 'CHAPTER n', then each couplet follows its verse number."""
    parts = PAGE.split(dump)[1:]
    verses, problems = {}, []
    for page_no, text in zip(parts[::2], parts[1::2]):
        head = CHAPTER_HEAD.search(text[:HEAD_CHARS])
        if not head:
            continue
        chapter = int(head.group(1))
        wanted = set(range(chapter * 10 - 9, chapter * 10 + 1))
        current = None
        for line in text.split("\n")[1:]:
            line = line.strip()
            if line.isdigit() and int(line) in wanted and int(line) not in verses:
                current = int(line)
                verses[current] = []
            elif current and line:
                verses[current].append(line)
        missing = sorted(n for n in wanted if not verses.get(n))
        if missing:
            problems.append(f"page {page_no}, chapter {chapter}: no text for {missing}")
    return verses, problems


def main():
    name, dump_path = sys.argv[1], sys.argv[2]
    verses, problems = {"subramuniyaswami": subramuniyaswami}[name](
        Path(dump_path).read_text(encoding="utf-8"))
    out = ROOT / "data" / "private" / f"{name}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as handle:
        for number in sorted(verses):
            handle.write(json.dumps({"verse": number, "text": verses[number]},
                                    ensure_ascii=False) + "\n")
    print(f"{name}: {len(verses)} verses, {len(problems)} problems")
    print("\n".join(problems))


if __name__ == "__main__":
    main()
