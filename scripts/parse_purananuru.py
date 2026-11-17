#!/usr/bin/env python3
"""Parse the Purananuru into kg/core/purananuru.jsonl, one record per poem.

Sources, all in data/text/:
  pmuni0057            the 400 poems (398 survive; 267 and 268 are lost), each with a modern title
                       and a colophon: poet, patron, thinai, thurai, sometimes a note (the base text)
  pmuni0494_01..03     Avvai S. Duraisamy Pillai's text and commentary, poems 1-200 (1947)
  pmuni0531_01..03     the same, poems 201-400

Duraisamy Pillai's poem sections are found by their 'N. heading' lines in sequence; within each
section the poem is told from the prose by its short lines and by letter trigrams against the
base text, which tolerates his older, sandhi-joined spelling. Everything else in the section
(introduction, his colophon sentence, உரை, விளக்கம்) is kept as his commentary.

Run: python3 -I scripts/parse_purananuru.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "data" / "text"
OUT = ROOT / "kg" / "core" / "purananuru.jsonl"
LOST = {267, 268}
DP_FILES = (("pmuni0494_01", 1, 60), ("pmuni0494_02", 61, 130), ("pmuni0494_03", 131, 200),
            ("pmuni0531_01", 201, 270), ("pmuni0531_02", 271, 340), ("pmuni0531_03", 341, 400))
NON_TAMIL = re.compile(r"[^஀-௿]")
ZERO_WIDTH = re.compile(r"[​-‍﻿]")
UNKNOWN = "தெரிந்தில"

# Colophon labels in the base text, with the field each one fills.
LABELS = [
    (r"பாடியவர்|பாடியோர்|பாடியவன்|பாடினோர்", "poet"),
    (r"பாடப்\s?பட்டோ(?:ன்|ர்)", "patron"),
    (r"திணை", "thinai"),
    (r"துறை", "thurai"),
    (r"குறிப்பு|சிறப்பு", "note"),
]
LABEL_RE = re.compile(r"(" + "|".join(p for p, _ in LABELS) + r")\s*[:;]")
HEADER_START = re.compile(r"^(?:\(|பாடி|பாடப்|பாடினோர்|திணை|துறை|குறிப்பு|சிறப்பு)")


def body(name):
    text = (TEXT / f"{name}.txt").read_text(encoding="utf-8")
    return text.split("=== BODY ===", 1)[1].split("=== FOOTER ===", 1)[0]


def grams(text):
    letters = NON_TAMIL.sub("", text)
    return {letters[i:i + 3] for i in range(len(letters) - 2)}


def similarity(a, b):
    return len(a & b) / (len(a | b) or 1)


def field_of(label):
    return next(f for p, f in LABELS if re.fullmatch(p, label))


def clean(value):
    value = re.sub(r"\s+", " ", value).strip(" .,;:")
    return value or None


def parse_colophon(header_lines):
    """Join the header lines and cut them at each 'label:'. Unknown values become null."""
    joined = " ".join(l for l in header_lines if not l.startswith("("))
    fields = {"poet": None, "patron": None, "thinai": None, "thurai": None, "note": None}
    hits = list(LABEL_RE.finditer(joined))
    for k, m in enumerate(hits):
        end = hits[k + 1].start() if k + 1 < len(hits) else len(joined)
        value = clean(joined[m.end():end])
        name = field_of(m.group(1))
        if value and UNKNOWN in value:  # keep what precedes a '... தெரிந்தில' sentence
            known = []
            for part in value.split("."):
                if UNKNOWN in part or re.match(r"^\s*(திணை|துறை)", part):
                    break
                known.append(part)
            value = clean(".".join(known)) if known else None
        if name == "note" and fields["note"] and value:
            value = fields["note"] + " " + value
        if fields[name] and value and name != "note":  # a second reading, e.g. 'திணை: வஞ்சியும்'
            value = f"{fields[name]}; {value}"
        if value or not fields[name]:
            fields[name] = value
    notes = [l.strip("() ") for l in header_lines if l.startswith("(")]
    if notes:
        fields["note"] = " ".join(filter(None, [fields["note"]] + notes))
    return fields


def norm(line):
    return NON_TAMIL.sub("", line)


def drop_strays(n, chunk, all_lines, problems):
    """Drop a blank-separated block of the poem whose lines are printed again elsewhere in the
    text (poem 64 carries nine lines of poem 326). Single-block poems are never touched."""
    blocks, cur = [], []
    for l in chunk + [""]:
        if l:
            cur.append(l)
        elif cur:
            blocks.append(cur)
            cur = []
    if len(blocks) < 2:
        return [l for b in blocks for l in b]
    counts = {}
    for l in all_lines:
        k = norm(l)
        if len(k) > 8:
            counts[k] = counts.get(k, 0) + 1
    kept = []
    for b in blocks:
        dup = sum(1 for l in b if counts.get(norm(l), 0) > 1)
        if len(b) >= 3 and dup >= len(b) - 2:
            problems.append(f"base {n}: dropped {len(b)} stray lines also printed in another poem, "
                            f"starting {b[0]!r}")
            continue
        kept.extend(b)
    return kept


def base_poems(problems):
    lines = [l.rstrip().replace("·", "ஃ") for l in body("pmuni0057").split("\n")]
    starts, expected = [], 1
    for i, line in enumerate(lines):
        m = re.match(r"^\s*(\d{1,3})\s*\.\s*(.*)$", line)
        if m and int(m.group(1)) in (expected, expected + 2) and expected <= 400:
            n = int(m.group(1))
            if n != expected:
                if not set(range(expected, n)) <= LOST:
                    problems.append(f"base: number jumps from {expected - 1} to {n}")
            starts.append((n, i, m.group(2).strip()))
            expected = n + 1
    poems = {}
    for k, (n, i, title) in enumerate(starts):
        end = starts[k + 1][1] if k + 1 < len(starts) else len(lines)
        chunk = [l.strip() for l in lines[i + 1:end]]
        # Header: label lines (and their wrapped continuations) before the first blank line.
        first_blank = next((j for j, l in enumerate(chunk) if not l), len(chunk))
        for j in range(first_blank):
            if chunk[j].startswith("ணை"):  # 'திணை' typed without its first letter
                chunk[j] = "தி" + chunk[j]
        header, j = [], 0
        while j < first_blank:
            line = chunk[j]
            later_label = any(HEADER_START.match(l) for l in chunk[j + 1:first_blank])
            if HEADER_START.match(line):
                header.append(line)
            elif header and (later_label or first_blank - j <= 2):  # a wrapped label value
                header.append(line)
            else:
                break
            j += 1
        verse = drop_strays(n, chunk[j:], lines, problems)
        trailing = [l for l in verse if re.match(r"^(267|புறநானூறு முற்றும்)", l)]
        verse = [l for l in verse if l not in trailing]
        if verse and all(set(l) <= set("?. ") for l in verse):
            problems.append(f"base {n}: poem text missing (only {' '.join(verse)!r})")
            verse = []
        fields = parse_colophon(header)
        poems[n] = {"id": f"purananuru:{n}", "number": n, "title": title.rstrip() or None,
                    **fields, "colophon_raw": " ".join(header) or None, "tamil": verse}
        if not header:
            problems.append(f"base {n}: no colophon (poet, patron, thinai, thurai)")
        if any(re.search(r"\.\s?\.\s?\.", l) for l in verse):
            problems.append(f"base {n}: lacunae ('. . .') in the poem lines")
    return poems


def repair(poems, problems):
    """Poem 99's last two lines are lines 3-4 of poem 100, displaced in the base text."""
    tail = poems[99]["tamil"][-2:]
    if tail and tail[0].startswith("வட்கர் போகிய") and not any(
            l.startswith("வட்கர்") for l in poems[100]["tamil"]):
        poems[99]["tamil"] = poems[99]["tamil"][:-2]
        poems[100]["tamil"][2:2] = tail
        problems.append("base 99/100: moved 2 lines ('வட்கர் போகிய...', 'உச்சிக் கொண்ட...') "
                        "from the end of 99 to lines 3-4 of 100, where Duraisamy Pillai has them")
    else:
        problems.append("base 99/100: expected displacement not found; no repair made")


def dp_poet(colophon, previous_poet):
    """'... X-ஐ Y பாடியது': Y is the poet. 'அவர்' means the previous poem's poet."""
    if not colophon:
        return None
    m = re.search(r"([^.]*?)\s*பாடியது", colophon)
    if not m:
        return None
    words = m.group(1).split()
    cut = max((i + 1 for i, w in enumerate(words) if re.search(r"(னை|ரை|யை|னைக்|ரைக்|யைக்|சென்ற)$", w)), default=0)
    poet = " ".join(words[cut:]) or None
    return previous_poet if poet == "அவர்" else poet


def dp_sections(problems):
    """Yield (number, file, heading, lines) for each poem section of Duraisamy Pillai."""
    for name, lo, hi in DP_FILES:
        lines = [ZERO_WIDTH.sub("", l).rstrip() for l in body(name).split("\n")]
        tail = next((i for i, l in enumerate(lines) if l.startswith("This file was last updated")),
                    len(lines))
        lines = lines[:tail]  # drop Project Madurai's closing note
        if lines and "முற்றுப்பெற்றன" in " ".join(lines[-4:]):  # the book's closing line
            while lines and "புறநானூறு மூலமும்" not in lines[-1]:
                lines.pop()
            lines = lines[:-1]
        start = next((i for i, l in enumerate(lines)
                      if l.startswith("###") and "மூலமும் உரையும்" in l), 0)
        heads, expected = [], lo
        for i in range(start, len(lines)):
            s = lines[i].strip()
            m = re.match(r"^(?:#+\s*)?(\d{1,3})\s*\.?\s*(\S.*)?$", s)
            if m and len(s) < 120 and expected <= int(m.group(1)) <= min(expected + 2, hi):
                n = int(m.group(1))
                if n != expected:
                    problems.append(f"{name}: no heading for {list(range(expected, n))}")
                heads.append((n, i, (m.group(2) or "").strip()))
                expected = n + 1
        if expected <= hi:
            problems.append(f"{name}: headings stop at {expected - 1}, expected up to {hi}")
        for k, (n, i, heading) in enumerate(heads):
            end = heads[k + 1][1] if k + 1 < len(heads) else len(lines)
            yield n, name, heading, lines[i + 1:end]


def is_verse_block(block):
    return len(block) >= 2 and max(len(l) for l in block) < 90 and \
        not any(re.match(r"^(உரை|விளக்கம்)\s*:", l) for l in block)


def strip_line_number(line):
    return re.sub(r"\s*\(?\d{1,3}\)?\s*\.?\s*$", "", line).strip()


def duraisamy(poems, problems):
    found, scores = {}, {}
    for n, name, heading, lines in dp_sections(problems):
        if n in LOST:
            continue
        lines = [l for l in lines if not re.fullmatch(r"\s*-{3,}\s*", l) and not l.startswith("###")]
        blocks, cur = [], []
        for l in lines + [""]:
            if l.strip():
                cur.append(l.strip())
            elif cur:
                blocks.append(cur)
                cur = []
        base = grams(" ".join(poems[n]["tamil"])) if n in poems and poems[n]["tamil"] else None
        verse_idx, best = [], 0.0
        sims = {b: (similarity(grams(" ".join(blk)), base) if base is not None else None)
                for b, blk in enumerate(blocks) if is_verse_block(blk)}
        if base is not None and sims:
            top = max(sims, key=sims.get)
            if sims[top] >= 0.2:
                best = sims[top]
                # The poem may be split by a blank line: take the adjacent verse blocks that match.
                lo = hi = top
                while lo - 1 in sims and sims[lo - 1] >= 0.2:
                    lo -= 1
                while hi + 1 in sims and sims[hi + 1] >= 0.2:
                    hi += 1
                verse_idx = list(range(lo, hi + 1))
        elif sims:  # no base text: take the first verse-like block
            verse_idx = [min(sims)]
        if not verse_idx:
            problems.append(f"{name} {n}: poem lines not found in the section")
        tamil = [strip_line_number(l) for b in verse_idx for l in blocks[b]]
        rest = [" ".join(blk) for b, blk in enumerate(blocks) if b not in verse_idx]
        before_urai = rest[:next((i for i, p in enumerate(rest) if re.match(r"^உ[ரற]ை\s*:", p)), len(rest))]
        colophon = next((p for p in before_urai if re.match(r"^\W*(திண|தின)", p) or
                         (len(p) < 400 and "பாடியது" in p)), None)
        found[n] = {"source": name, "heading": heading or None, "tamil": tamil or None,
                    "colophon": colophon, "commentary": "\n".join(rest) or None}
        scores[n] = round(best, 3) if base is not None else None
    return found, scores


def dp_thinai_thurai(colophon, previous):
    """Read thinai and thurai from his colophon; 'அவை'/'அது' means 'as in the previous poem'."""
    if not colophon:
        return None, None
    head = colophon.split(".")[0]
    joined = head.replace(" ", "")
    if re.match(r"^திண\S*?துறையு", joined) and re.search(r"(அவை|மவை|அது|மது|மறை)$", joined):
        return previous
    th = re.search(r"திணை\s*[-–:]\s*(.+?)(?=[;.]|\s*துறை|$)", head)
    tu = re.search(r"துறை\s*[-–:]\s*([^;.]+)", colophon)
    t1 = re.sub(r"\s*(த்திணை|டிணை|திணை)$", "", th.group(1).strip()) if th else None
    if t1 in ("அது", "அவை"):  # 'thinai: the same'
        t1 = previous[0]
    return (t1 or None), (tu.group(1).strip() if tu else None)


def main():
    problems = []
    poems = base_poems(problems)
    repair(poems, problems)
    dp, scores = duraisamy(poems, problems)
    previous, filled = (None, None), []
    for n in sorted(dp):
        cur = dp_thinai_thurai(dp[n]["colophon"], previous)
        if cur != (None, None):
            previous = cur
        dp[n]["thinai"], dp[n]["thurai"] = cur
    with open(OUT, "w", encoding="utf-8") as out:
        for n in sorted(poems):
            p = poems[n]
            d = dp.get(n)
            p["tamil_source"] = "pmuni0057"
            p["filled_from_duraisamy_pillai"] = []
            if d:
                if not p["tamil"] and d["tamil"]:
                    p["tamil"], p["tamil_source"] = d["tamil"], d["source"]
                    p["filled_from_duraisamy_pillai"].append("tamil")
                if p["colophon_raw"] is None:  # no colophon at all in the base text
                    poet = dp_poet(d["colophon"], poems.get(n - 1, {}).get("poet"))
                    if poet:
                        p["poet"] = poet
                        p["filled_from_duraisamy_pillai"].append("poet")
                    if d["heading"] and poet and d["heading"].replace(" ", "") != poet.replace(" ", ""):
                        p["patron"] = d["heading"]
                        p["filled_from_duraisamy_pillai"].append("patron")
                for f in ("thinai", "thurai"):
                    if not p[f] and d[f] and UNKNOWN not in (p["colophon_raw"] or ""):
                        p[f] = d[f]
                        p["filled_from_duraisamy_pillai"].append(f)
                if p["filled_from_duraisamy_pillai"]:
                    filled.append((n, p["filled_from_duraisamy_pillai"]))
                p["duraisamy_pillai"] = {k: d[k] for k in ("source", "heading", "tamil",
                                                           "colophon", "commentary")}
            else:
                p["duraisamy_pillai"] = None
            p["rights"] = {"tamil": "public_domain", "colophon": "public_domain", "title": "modern",
                           "note": "modern", "duraisamy_pillai": "modern"}
            out.write(json.dumps(p, ensure_ascii=False) + "\n")
    expected = set(range(1, 401)) - LOST
    missing, extra = expected - set(poems), set(poems) - expected
    low = sorted((s, n) for n, s in scores.items() if s is not None and s < 0.35)
    print(f"poems={len(poems)} (expected {len(expected)}) missing={sorted(missing)} extra={sorted(extra)}")
    print(f"duraisamy_pillai={len(dp)} with_poem_lines={sum(1 for d in dp.values() if d['tamil'])} "
          f"with_commentary={sum(1 for d in dp.values() if d['commentary'])}")
    print(f"poet={sum(1 for p in poems.values() if p['poet'])} "
          f"patron={sum(1 for p in poems.values() if p['patron'])} "
          f"thinai={sum(1 for p in poems.values() if p['thinai'])} "
          f"thurai={sum(1 for p in poems.values() if p['thurai'])}")
    print(f"filled from Duraisamy Pillai: {filled}")
    print(f"low base/DP poem similarity (<0.35): {low}")
    for line in problems:
        print("PROBLEM:", line)


if __name__ == "__main__":
    main()
