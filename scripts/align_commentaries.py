#!/usr/bin/env python3
"""Align each commentary to the Kural's verses by matching the verse's text.

Commentaries use different layouts, spellings and even verse orders, so numbers
are unreliable. A verse is matched by the similarity of its Tamil to two
consecutive lines, or one line holding the whole couplet. Where a verse occurs
more than once, as in an index, the strongest match wins, and a line carrying the
verse's own number counts as strong evidence.

Writes kg/core/commentaries.jsonl and prints coverage for each commentary.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT_DIR = ROOT / "data" / "text"
KURAL = ROOT / "kg" / "core" / "kural.jsonl"
OUT = ROOT / "kg" / "core" / "commentaries.jsonl"
COMMENTARIES = {
    "parimelazhagar": ["pmuni0450_01", "pmuni0450_02", "pmuni0450_03", "pmuni0450_04"],
    "manakkudavar": ["pmuni0650"],
    "kalaignar": ["pmuni0612"],
}
THRESHOLD = 0.5
LABELLED_THRESHOLD = 0.35
LABEL_BONUS = 1.0
AMBIGUITY_MARGIN = 0.08
ENTRY_BREAK = re.compile(r"^(-{3,}|#+ |\d{1,4}[.)] ?\S)")
NON_TAMIL = re.compile(r"[^஀-௿]")


def grams(text):
    letters = NON_TAMIL.sub("", text)
    return {letters[i:i + 3] for i in range(len(letters) - 2)}


def similarity(first, second):
    return len(first & second) / len(first | second) if first and second else 0.0


def align(doc_names, verses):
    """Return {verse: {"doc", "match", "text"}}."""
    best = {}
    for doc in doc_names:
        text = (TEXT_DIR / f"{doc}.txt").read_text(encoding="utf-8")
        lines = text.partition("=== BODY ===")[2].partition("=== FOOTER ===")[0].split("\n")
        index = defaultdict(set)
        verse_grams = {}
        for number, verse in verses.items():
            verse_grams[number] = grams(" ".join(verse["tamil"]))
            for gram in verse_grams[number]:
                index[gram].add(number)

        hits = []
        for position, line in enumerate(lines):
            if not NON_TAMIL.sub("", line):
                continue
            following = lines[position + 1] if position + 1 < len(lines) else ""
            for span, candidate in ((2, line + " " + following), (1, line)):
                candidate_grams = grams(candidate)
                if len(candidate_grams) < 12:
                    continue
                counts = defaultdict(int)
                for gram in candidate_grams:
                    for number in index.get(gram, ()):
                        counts[number] += 1
                if not counts:
                    continue
                ranked = sorted(counts, key=counts.get, reverse=True)[:5]
                scored = sorted(((similarity(candidate_grams, verse_grams[n]), n) for n in ranked),
                                reverse=True)
                score, number = scored[0]
                labelled = number in {int(x) for x in re.findall(r"\d{1,4}", candidate)}
                if score < (LABELLED_THRESHOLD if labelled else THRESHOLD):
                    continue
                if not labelled and len(scored) > 1 and score - scored[1][0] < AMBIGUITY_MARGIN:
                    continue
                hits.append((position, span, number, score + (LABEL_BONUS if labelled else 0)))
                break

        hits = [hit for i, hit in enumerate(hits)
                if not (i and hits[i - 1][0] == hit[0] - 1 and hits[i - 1][2] == hit[2]
                        and hits[i - 1][1] == 2)]
        for i, (position, span, number, score) in enumerate(hits):
            end = hits[i + 1][0] if i + 1 < len(hits) else len(lines)
            segment = lines[position + span:end]
            for offset, line in enumerate(segment):
                if ENTRY_BREAK.match(line.strip()):
                    segment = segment[:offset]
                    break
            body = "\n".join(segment).strip()
            if not body:
                continue
            current = best.get(number)
            # The strongest match wins, so an index or a poem that quotes the verse loses.
            if current is None or (score, len(body)) > (current["match"], len(current["text"])):
                best[number] = {"doc": doc, "match": round(score, 3), "text": body}
    return best


def main():
    verses = {r["verse"]: r for r in map(json.loads, KURAL.read_text(encoding="utf-8").splitlines())}
    aligned = {name: align(docs, verses) for name, docs in COMMENTARIES.items()}
    with open(OUT, "w", encoding="utf-8") as out:
        for number in sorted(verses):
            record = {"verse": number}
            for name in COMMENTARIES:
                if number in aligned[name] and aligned[name][number]["text"]:
                    record[name] = aligned[name][number]
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    for name, found in aligned.items():
        usable = [n for n, item in found.items() if item["text"]]
        missing = sorted(set(verses) - set(usable))
        print(f"{name}: {len(usable)}/{len(verses)} aligned; missing {missing[:40]}")


if __name__ == "__main__":
    main()
