#!/usr/bin/env python3
"""Parse the Naladiyar into kg/core/naladiyar.jsonl.

Sources, all in data/text/:
  pmuni0016  the 400 quatrains, with book and chapter headings (the base text)
  pmuni0711  G.U. Pope's English translation, with a Tamil summary line per quatrain
  pmuni0518  V. Mahadeva Mudaliar's word glosses (1924), numbered by quatrain
  pmuni0778  Sundara Shanmuganar's commentary (1970), matched to quatrains by their text

Pope and Shanmuganar print the quatrains themselves, so each is aligned to the base text by
letter trigrams, which tolerates spelling differences between editions.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "data" / "text"
OUT = ROOT / "kg" / "core" / "naladiyar.jsonl"
BOOKS = {"1": "அறத்துப்பால்", "2": "பொருட்பால்", "3": "காமத்துப்பால்"}
NON_TAMIL = re.compile(r"[^஀-௿]")
TAMIL = re.compile(r"[஀-௿]")
MIN_MATCH = 0.45


def body(name):
    text = (TEXT / f"{name}.txt").read_text(encoding="utf-8")
    return text.split("=== BODY ===", 1)[1].split("=== FOOTER ===", 1)[0]


def grams(text):
    letters = NON_TAMIL.sub("", text)
    return {letters[i:i + 3] for i in range(len(letters) - 2)}


def similarity(a, b):
    return len(a & b) / (len(a | b) or 1)


def base_verses():
    verses, chapter = {}, None
    lines = body("pmuni0016").split("\n")
    start = next(i for i, l in enumerate(lines) if l.strip().startswith("1.1 "))
    i = start
    while i < len(lines):
        line = lines[i].strip()
        head = re.match(r"^(\d)\.(\d+)\s+(.+)$", line)
        verse = re.match(r"^(\d+)\.\s+(.+)$", line)
        if head:
            number = int(head.group(2))
            book = "3" if number >= 38 else head.group(1)  # chapter 39 is misprinted as 2.39
            chapter = (number, head.group(3).strip(), BOOKS[book])
        elif verse and chapter and int(verse.group(1)) == len(verses) + 1:  # book headings also look like 'N. word'
            n = int(verse.group(1))
            quatrain = [verse.group(2).strip()] + [lines[i + k].strip() for k in (1, 2, 3)]
            verses[n] = {"verse": n, "chapter_no": chapter[0], "chapter": chapter[1],
                         "section": chapter[2], "tamil": quatrain}
            i += 3
        i += 1
    return verses


def blocks(text):
    return [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]


def pope(verses):
    """Each block: optional 'N. Tamil summary', four Tamil lines, an English title, the translation."""
    vg = {n: grams(" ".join(v["tamil"])) for n, v in verses.items()}
    found = {}
    for block in blocks(body("pmuni0711")):
        lines = block.split("\n")
        tamil = [l for l in lines if TAMIL.search(l)]
        english = [l.strip() for l in lines if not TAMIL.search(l) and l.strip()]
        if len(tamil) < 4 or len(english) < 2:
            continue
        quatrain = [l for l in tamil if not re.match(r"^\d+\.", l.strip())][:4]
        g = grams(" ".join(quatrain))
        n, score = max(((n, similarity(g, vg[n])) for n in vg), key=lambda x: x[1])
        if score >= MIN_MATCH and score > found.get(n, (0,))[0]:
            found[n] = (score, {"title": english[0], "text": " ".join(english[1:])})
    return {n: p for n, (s, p) in found.items()}


def mudaliar():
    """Word glosses: lines 'N. word - meaning. word - meaning.' after each chapter's quatrains."""
    glosses = {}
    for line in body("pmuni0518").split("\n"):
        m = re.match(r"^(\d{1,3})\.\s*(.+)$", line.strip())
        if m and " - " in m.group(2) or (m and "-" in m.group(2) and len(m.group(2)) > 60):
            n = int(m.group(1))
            if 1 <= n <= 400 and len(m.group(2)) > len(glosses.get(n, "")):
                glosses[n] = m.group(2).strip()
    return glosses


def shanmuganar(verses):
    """Commentary paragraphs follow each quatrain. Match the quatrain, keep the prose after it."""
    vg = {n: grams(" ".join(v["tamil"])) for n, v in verses.items()}
    bs = blocks(body("pmuni0778"))
    found = {}
    for i, block in enumerate(bs):
        lines = [l for l in block.split("\n") if TAMIL.search(l)]
        if not 3 <= len(lines) <= 6:
            continue
        g = grams(" ".join(lines[:4]))
        if len(g) < 30:
            continue
        n, score = max(((n, similarity(g, vg[n])) for n in vg), key=lambda x: x[1])
        if score < MIN_MATCH or score <= found.get(n, (0,))[0]:
            continue
        prose = []
        for nxt in bs[i + 1:i + 4]:
            nl = [l for l in nxt.split("\n") if TAMIL.search(l)]
            if 3 <= len(nl) <= 6 and similarity(grams(" ".join(nl[:4])), vg[n]) < 0.2 and \
                    max(similarity(grams(" ".join(nl[:4])), vg[m]) for m in vg) >= MIN_MATCH:
                break
            prose.append(" ".join(nxt.split()))
        if prose:
            found[n] = (score, " ".join(prose))
    return {n: t for n, (s, t) in found.items()}


def main():
    verses = base_verses()
    assert sorted(verses) == list(range(1, 401)), f"missing {set(range(1, 401)) - set(verses)}"
    translations, glosses, shan = pope(verses), mudaliar(), shanmuganar(verses)
    with open(OUT, "w", encoding="utf-8") as out:
        for n in sorted(verses):
            record = verses[n] | {"pope": translations.get(n), "mudaliar": glosses.get(n),
                                  "shanmuganar": shan.get(n)}
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    chapters = len({v["chapter_no"] for v in verses.values()})
    print(f"verses={len(verses)} chapters={chapters} pope={len(translations)} "
          f"mudaliar={len(glosses)} shanmuganar={len(shan)}")


if __name__ == "__main__":
    main()
