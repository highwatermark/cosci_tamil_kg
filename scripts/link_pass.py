#!/usr/bin/env python3
"""Inputs for the systematic link pass described in docs/link-pass-plan.md.

    link_pass.py index OUT    one line per verse: number, chapter, concepts and reading
    link_pass.py hints OUT    each verse's best word-overlap matches, as hints only
    link_pass.py verse N...   the Tamil, Pope's gloss and commentary openings for verses

Neither output contains existing links, so proposers can't copy them.
"""
import collections
import itertools
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HINTS_PER_VERSE = 10
MAX_DOCUMENT_FREQUENCY = 60
COMMENTARY_CHARS = 400
NON_TAMIL = re.compile(r"[^஀-௿ ]")
STOP_WORDS = set("the a an of to and in is are be by for that this it its as with on or not one who "
                 "what their his her he she they them than but from at into when which those so no "
                 "does do has have was were will can may only also if more most even own all "
                 "any".split())


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def load():
    nodes = read_jsonl(ROOT / "kg" / "kural" / "nodes.jsonl")
    verses = {n["number"]: n for n in nodes if n["type"] == "Verse"}
    chapters = {n["number"]: n["title"] for n in nodes if n["type"] == "Chapter"}
    concepts = collections.defaultdict(list)
    for edge in read_jsonl(ROOT / "kg" / "kural" / "edges.jsonl"):
        if edge["p"] == "EXPRESSES":
            concepts[int(edge["s"].split(":")[1])].append(edge["o"].split(":")[1])
    return verses, chapters, concepts


def write_index(out):
    verses, chapters, concepts = load()
    lines = []
    for number in sorted(verses):
        chapter = (number - 1) // 10 + 1
        lines.append(f"{number} | ch{chapter} {chapters[chapter]} | {', '.join(concepts[number])} | "
                     f"{verses[number]['reading']}")
    Path(out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"index: {len(lines)} verses")


def features(verses, concepts):
    """Three bags per verse: concepts, English reading words, and Tamil word stems."""
    commentaries = {c["verse"]: c for c in read_jsonl(ROOT / "kg" / "core" / "commentaries.jsonl")}
    reading, tamil = {}, {}
    for number, verse in verses.items():
        words = re.findall(r"[a-z]+", (verse["reading"] + " " + verse["nuance"]).lower())
        reading[number] = {w.rstrip("s") for w in words if w not in STOP_WORDS and len(w) > 2}
        entry = commentaries.get(number, {})
        text = " ".join(verse["tamil"]) + " " + " ".join(
            (entry.get(name) or {}).get("text", "")[:COMMENTARY_CHARS]
            for name in ("parimelazhagar", "kalaignar"))
        tamil[number] = {w[:4] for w in NON_TAMIL.sub(" ", text).split() if len(w) >= 4}
    return [{n: set(concepts[n]) for n in verses}, reading, tamil]


def write_hints(out):
    verses, _, concepts = load()
    total = len(verses)
    scores = collections.Counter()
    for bags in features(verses, concepts):
        frequency = collections.Counter(item for bag in bags.values() for item in bag)
        weight = {item: math.log(total / count) ** 2 for item, count in frequency.items()
                  if count <= MAX_DOCUMENT_FREQUENCY}
        norm = {n: math.sqrt(sum(weight.get(i, 0) for i in bag)) or 1 for n, bag in bags.items()}
        for a, b in itertools.combinations(sorted(verses), 2):
            shared = sum(weight.get(item, 0) for item in bags[a] & bags[b])
            if shared:
                scores[(a, b)] += shared / (norm[a] * norm[b])
    best = collections.defaultdict(list)
    for (a, b), score in scores.items():
        best[a].append((score, b))
        best[b].append((score, a))
    lines = [f"{n}: " + " ".join(str(other) for _, other in sorted(best[n], reverse=True)
                                 [:HINTS_PER_VERSE]) for n in sorted(verses)]
    Path(out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"hints: {len(lines)} verses")


def show_verses(numbers):
    """Print the Tamil, Pope's gloss and the start of two commentaries for each verse."""
    verses = {v["verse"]: v for v in read_jsonl(ROOT / "kg" / "core" / "kural.jsonl")}
    commentaries = {c["verse"]: c for c in read_jsonl(ROOT / "kg" / "core" / "commentaries.jsonl")}
    for number in map(int, numbers):
        verse, entry = verses[number], commentaries.get(number, {})
        print(f"## {number} ({verse['chapter']})\n" + " / ".join(verse["tamil"]))
        print("Pope: " + verse["pope"]["gloss"])
        for name in ("parimelazhagar", "kalaignar"):
            text = (entry.get(name) or {}).get("text", "").replace("\n", " ")
            if text:
                print(f"{name}: {text[:COMMENTARY_CHARS]}{' …' if len(text) > COMMENTARY_CHARS else ''}")
        print()


if __name__ == "__main__":
    if sys.argv[1] == "verse":
        show_verses(sys.argv[2:])
    else:
        {"index": write_index, "hints": write_hints}[sys.argv[1]](sys.argv[2])
