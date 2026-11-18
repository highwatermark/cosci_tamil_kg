#!/usr/bin/env python3
"""Candidate link hints for one book against every built book.

    link_hints.py BOOK OUT

For each verse of BOOK, list the verses that share the most weight with it, a quota per book (OWN
from its own book, OTHER from each other book, so cross-book candidates are not crowded out): shared concepts weighted by rarity (inverse document frequency), plus shared
rare Tamil words at half weight. These are hints only: real links still have to be read and judged.
Existing links are not shown. Output lines look like:
    tirumanthiram:725 | tirumanthiram:1729 (yaakkai/உடம்பினை), ... || kural:1001 (...), ... || ...
"""
import collections
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ("kural", "naladiyar", "tirumanthiram", "thiruppugazh")
# Words of four or more letters. A piece that starts with a vowel sign or with a letter Tamil words
# do not begin with (ற ன ண ழ ள ங ஞ ட) is the tail of a word split by the rhythm, not a word.
WORD = re.compile(r"(?<![஀-௿])[அ-ஹ][஀-௿]{3,}")
NOT_INITIAL = set("றனணழளஙஞட")
MAX_WORD_DF = 25  # a word in more verses than this is too common to hint anything
OWN, OTHER = 8, 4


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def main():
    book, out = sys.argv[1], sys.argv[2]
    concepts, words = collections.defaultdict(set), {}
    for b in BOOKS:
        folder = ROOT / "kg" / b
        if not (folder / "nodes.jsonl").exists():
            continue
        for n in read_jsonl(folder / "nodes.jsonl"):
            if n["type"] == "Verse":
                # Join the rhythm's split pieces before taking words.
                text = re.sub(r"\.{2,}|\s+", " ", " ".join(n["tamil"]))
                words[n["id"]] = {w for w in WORD.findall(text) if w[0] not in NOT_INITIAL}
        for e in read_jsonl(folder / "edges.jsonl"):
            if e["p"] == "EXPRESSES":
                concepts[e["s"]].add(e["o"])
    total = len(words)
    cdf, wdf = collections.Counter(), collections.Counter()
    for v in words:
        cdf.update(concepts[v]); wdf.update(words[v])
    cidf = {c: math.log(total / n) for c, n in cdf.items()}
    widf = {w: math.log(total / n) for w, n in wdf.items() if n <= MAX_WORD_DF}
    by_concept, by_word = collections.defaultdict(list), collections.defaultdict(list)
    def shared(v, o):
        # The two rarest things the pair shares, so a reader can judge the hint without looking it up.
        items = [(cidf[c], c.split(":")[1]) for c in concepts[v] & concepts[o]]
        items += [(widf[w] / 2, w) for w in words[v] & words[o] if w in widf]
        return "/".join(x for _, x in sorted(items, reverse=True)[:2])
    for v in words:
        for c in concepts[v]:
            by_concept[c].append(v)
        for w in words[v]:
            if w in widf:
                by_word[w].append(v)
    lines = []
    for v in (x for x in words if x.startswith(book + ":")):
        score = collections.Counter()
        for c in concepts[v]:
            for o in by_concept[c]:
                score[o] += cidf[c]
        for w in words[v]:
            if w in widf:
                for o in by_word[w]:
                    score[o] += widf[w] / 2
        score.pop(v, None)
        groups = []
        for b in (book,) + tuple(x for x in BOOKS if x != book):
            best = [(o, s) for o, s in score.most_common() if o.startswith(b + ":")][:OWN if b == book else OTHER]
            if best:
                groups.append(", ".join(f"{o} ({shared(v, o)})" for o, s in best))
        lines.append(f"{v} | " + " || ".join(groups))
    Path(out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(lines)} verses -> {out}")


if __name__ == "__main__":
    main()
