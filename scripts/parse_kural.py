#!/usr/bin/env python3
"""Parse the Thirukkural into one record per verse, with Pope's translation.

Writes kg/core/kural.jsonl. Stops if any of the 1,330 verses is missing.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT_DIR = ROOT / "data" / "text"
OUT = ROOT / "kg" / "core" / "kural.jsonl"
VERSES = 1330
VERSE_END = re.compile(r"^(.*?)[\s.]*?(\d{1,4})\s*$")
# The source prints the section heading where these chapters' titles belong.
TITLE_FIXES = {116: "பிரிவாற்றாமை"}
SECTIONS = ((380, "அறத்துப்பால்"), (1080, "பொருட்பால்"), (1330, "காமத்துப்பால்"))


def body(name):
    text = (TEXT_DIR / f"{name}.txt").read_text(encoding="utf-8")
    return text.partition("=== BODY ===")[2].partition("=== FOOTER ===")[0]


def clean_title(line):
    return re.sub(r"^[#,\s\d.]*", "", line).strip()


def parse_tamil():
    """Couplets are two lines, so position repairs the source's numbering typos."""
    verses, repairs = {}, []
    lines = [line for line in body("pmuni0001").split("\n") if line.strip()]
    expected, last_end = 1, None

    def add(number, first, second, title_index):
        chapter_no = (number - 1) // 10 + 1
        verses[number] = {"verse": number, "chapter_no": chapter_no,
                          "section": next(name for end, name in SECTIONS if number <= end),
                          "tamil": [first.strip(), re.sub(r"[\s.]*\d+$", "", second.strip())]}
        if number % 10 == 1:
            verses[number]["chapter"] = TITLE_FIXES.get(chapter_no, clean_title(lines[title_index]))

    for index, line in enumerate(lines):
        match = VERSE_END.match(line)
        if not match or not match.group(1):
            continue
        label, text = int(match.group(2)), match.group(1)
        if label == expected + 1:
            add(expected, lines[index - 3], lines[index - 2], index - 4)
            repairs.append(f"tamil {expected}: number missing in source")
            expected += 1
        elif label == expected - 1 and last_end == index - 2:
            repairs.append(f"tamil {expected}: labelled {label} in source")
            label = expected
        if label != expected:
            continue
        add(expected, lines[index - 1], text, index - 2)
        last_end = index
        expected += 1
    return verses, repairs


def parse_pope():
    """Each entry is a numbered couplet and a one-line gloss, so three lines."""
    entries, current, expected, repairs = {}, None, 1, []
    for line in body("pmuni0153").split("\n"):
        stripped = line.strip()
        match = re.fullmatch(r"(\d{1,4})\.?", stripped)
        if match and int(match.group(1)) == expected + 1 and current and len(current) >= 6:
            entries[expected] = current[3:]
            del current[3:]
            repairs.append(f"pope {expected}: number missing in source")
            expected += 1
        if match and int(match.group(1)) == expected:
            current = entries[expected] = []
            expected += 1
        elif current is not None and stripped and not stripped.startswith("#"):
            current.append(stripped)
    return entries, repairs


def main():
    tamil, tamil_repairs = parse_tamil()
    pope, pope_repairs = parse_pope()
    missing = [n for n in range(1, VERSES + 1) if n not in tamil or n not in pope]
    if missing:
        sys.exit(f"missing {len(missing)} verses, first {missing[:10]}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    chapter = None
    with open(OUT, "w", encoding="utf-8") as out:
        for n in range(1, VERSES + 1):
            record = tamil[n]
            chapter = record.get("chapter", chapter)
            record["chapter"] = chapter
            lines = pope[n]
            record["pope"] = {"couplet": lines[:2], "gloss": " ".join(lines[2:3])}
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"wrote {VERSES} verses; repairs: {tamil_repairs + pope_repairs}")


if __name__ == "__main__":
    main()
