#!/usr/bin/env python3
"""Parse Avvaiyar's four short works into kg/core/avvaiyar.jsonl.

Works, in the catalogue's order (rows 2-5): Aathichudi, Kondrai Vendhan, Nalvazhi, Moodurai.
Units: each Aathichudi and Kondrai Vendhan line, each Nalvazhi and Moodurai verse. Each work's
invocation (kaappu / kadavul vazhthu) is kept as unit 0.

Sources, all in data/text/:
  pmuni0002  the four works (the base text), Aathichudi and Kondrai Vendhan grouped by letter
  pmuni0743  Arumuga Navalar's commentary (1822-1879) on all four works, with the editions'
             explanatory notes (Chennai, 1914-1921)
  pmuni0481  Ramabharathi's Aathichudi Venba: one venba per Aathichudi line, with a story
  pmuni0777  Sundara Shanmuganar's commentary (naya urai) on Nalvazhi (modern, in copyright)

The commentaries print the text themselves. Each is aligned to the base text by an
order-preserving alignment over letter bigram and trigram similarity, which tolerates
the sandhi and spelling differences between editions and refuses to cross matches.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "data" / "text"
OUT = ROOT / "kg" / "core" / "avvaiyar.jsonl"
NON_TAMIL = re.compile(r"[^஀-௿]")
TAMIL = re.compile(r"[஀-௿]")
RULE = re.compile(r"^\s*[-_–—.]{3,}\s*$")
MIN_MATCH = 0.2

WORKS = [  # key, Tamil title, heading in pmuni0002, traditional count (excluding the invocation)
    ("aathichudi", "ஆத்திசூடி", "1. ஆத்திசூடி", 108),
    ("kondrai_vendhan", "கொன்றை வேந்தன்", "2. கொன்றை வேந்தன்", 91),
    ("nalvazhi", "நல்வழி", "4. நல்வழி", 40),
    ("moodurai", "மூதுரை", "3. மூதுரை", 30),
]
# Aathichudi is traditionally counted as 108 lines, but this edition and Navalar's print 109
# (the vakara group carries both 'உத்தமனாய் இரு' and 'ஊருடன் கூடி வாழ்'); the base file is kept.
EXPECTED = {"aathichudi": 109, "kondrai_vendhan": 91, "nalvazhi": 40, "moodurai": 30}


def body(name):
    text = (TEXT / f"{name}.txt").read_text(encoding="utf-8")
    return text.split("=== BODY ===", 1)[1].split("=== FOOTER ===", 1)[0]


def grams(text):
    letters = NON_TAMIL.sub("", text)
    return {letters[i:i + 2] for i in range(len(letters) - 1)} | \
           {letters[i:i + 3] for i in range(len(letters) - 2)}


def similarity(a, b):
    return len(a & b) / (len(a | b) or 1)


def align(base, other):
    """Order-preserving alignment. base, other: lists of gram sets. Returns {i: (j, score)}."""
    n, m = len(base), len(other)
    sim = [[similarity(base[i], other[j]) for j in range(m)] for i in range(n)]
    best = [[0.0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            take = best[i + 1][j + 1] + sim[i][j] - MIN_MATCH if sim[i][j] >= MIN_MATCH else -1
            best[i][j] = max(take, best[i + 1][j], best[i][j + 1])
    pairs, i, j = {}, 0, 0
    while i < n and j < m:
        if sim[i][j] >= MIN_MATCH and best[i][j] == best[i + 1][j + 1] + sim[i][j] - MIN_MATCH:
            pairs[i] = (j, sim[i][j])
            i, j = i + 1, j + 1
        elif best[i][j] == best[i + 1][j]:
            i += 1
        else:
            j += 1
    # A single unmatched unit on each side between two matches (or at the ends) is the same
    # slot printed with a variant reading: pair it by position, with a score of 0.
    anchors = [(-1, -1)] + sorted((i, j) for i, (j, _) in pairs.items()) + [(n, m)]
    for (i0, j0), (i1, j1) in zip(anchors, anchors[1:]):
        if i1 - i0 == 2 and j1 - j0 == 2:
            pairs[i0 + 1] = (j0 + 1, 0.0)
    return pairs


def clean_line(line):
    return re.sub(r"\s*\d+\s*[.,]?\s*$", "", line.strip()).strip()


# ---------- base text ----------

def base_units(problems):
    lines = body("pmuni0002").split("\n")
    starts = {key: next(i for i, l in enumerate(lines) if l.strip() == head)
              for key, _, head, _ in WORKS}
    order = sorted(starts.values()) + [len(lines)]
    units = {}
    for key, title, head, _ in WORKS:
        start = starts[key]
        part = lines[start + 1:order[order.index(start) + 1]]
        if key in ("aathichudi", "kondrai_vendhan"):
            units[key] = line_units(key, part, problems)
        else:
            units[key] = verse_units(key, part, problems)
    return units


def line_units(key, part, problems):
    """Invocation, then letter-group headings ('உயிர் வருக்கம்') and numbered lines."""
    out, group, invocation, seen_lines = [], None, [], False
    for raw in part:
        line = raw.strip()
        if not line or line == "கடவுள் வாழ்த்து":
            continue
        m = re.match(r"^(\d+)\.\s*(.+)$", line)
        if m:
            seen_lines = True
            n = int(m.group(1))
            if n != len(out) + 1:
                problems.append(f"{key}: line printed {n} at position {len(out) + 1}")
            out.append({"number": len(out) + 1, "printed_number": n, "group": group,
                        "tamil": [m.group(2).strip()]})
        elif line.endswith("வருக்கம்"):
            group = line
        elif not seen_lines:
            invocation.append(line)
        else:
            problems.append(f"{key}: stray line {line!r}")
    return [{"number": 0, "printed_number": None, "group": "கடவுள் வாழ்த்து",
             "tamil": invocation}] + out


def verse_units(key, part, problems):
    """Quatrains separated by blank lines; the invocation first; numbers at the line ends."""
    paras, cur = [], []
    for raw in part + [""]:
        line = raw.strip()
        if line in ("கடவுள் வாழ்த்து", "நூல்"):
            line = ""
        if line:
            cur.append(line)
        elif cur:
            paras.append(cur)
            cur = []
    out = []
    for k, para in enumerate(paras):
        if len(para) != 4:
            problems.append(f"{key}: paragraph {k} has {len(para)} lines: {para[0]!r}")
        m = re.search(r"(\d+)\s*[.,]?\s*$", para[-1])
        printed = int(m.group(1)) if m else None
        if k and printed != k:
            problems.append(f"{key}: verse {k} printed as {printed}: {para[0]!r}")
        out.append({"number": k, "printed_number": printed if k else None,
                    "group": "கடவுள் வாழ்த்து" if k == 0 else None,
                    "tamil": [clean_line(l) for l in para]})
    return out


# ---------- Arumuga Navalar (pmuni0743) ----------

def section(lines, start_pat, end_pat):
    s = next(i for i, l in enumerate(lines) if re.search(start_pat, l))
    e = next(i for i in range(s + 1, len(lines)) if re.search(end_pat, lines[i]))
    return lines[s + 1:e]


TAG = re.compile(r"^[\[(]\s*(ப|க)\s*[-.]?\s*உ\s*[\])]?\s*")


def navalar_lines(part):
    """Aathichudi / Kondrai Vendhan: a line, then [ப-உ] word gloss and [க-உ] meaning, and notes."""
    entries, cur, field = [], None, None
    for raw in part:
        line = raw.strip()
        if not line or line in ("நூல்", "கடவுள் வாழ்த்து") or RULE.match(line) or "முற்றிற்று" in line:
            continue
        m = re.match(r"^(\d+)\.\s*([^\[(].*)$", line)
        tag = TAG.match(line)
        if m and not tag:
            cur = {"printed_number": int(m.group(1)), "text": [m.group(2).strip()],
                   "gloss": [], "meaning": [], "notes": []}
            entries.append(cur)
            field = "text"
        elif tag:
            if cur is None:
                cur = {"printed_number": 0, "text": [], "gloss": [], "meaning": [], "notes": []}
                entries.append(cur)
            field = "gloss" if tag.group(1) == "ப" else "meaning"
            rest = line[tag.end():].strip()
            inline = re.split(r"\[க\s*-+\s*(?:உ)?\s*\]", rest, maxsplit=1)  # '[க--]' mid-line
            cur[field].append(inline[0].strip())
            if len(inline) == 2:
                field = "meaning"
                cur[field].append(inline[1].strip())
        elif cur is None or (cur["printed_number"] == 0 and field in (None, "text")):
            if cur is None:
                cur = {"printed_number": 0, "text": [], "gloss": [], "meaning": [], "notes": []}
                entries.append(cur)
            if "மூலமும்" not in line:  # the section heading, not the invocation
                cur["text"].append(line)
            field = "text"
        elif field == "text" and cur["printed_number"] and not re.match(r"^\(.*\)$", line):
            field = "gloss"  # a gloss printed without its [ப-உ] tag
            cur["gloss"].append(line)
        elif field == "gloss" and not cur["meaning"]:
            cur["gloss"].append(line)  # a gloss wrapped onto a second line
        else:
            cur["notes"].append(line)
    return entries


def navalar_verses(part):
    """Nalvazhi / Moodurai: the quatrain, 'இ-ள்' word-by-word gloss, 'இ-ம்' gist, notes."""
    paras, cur = [], []
    for raw in part + [""]:
        line = raw.strip()
        if line and not RULE.match(line):
            cur.append(line)
        elif cur:
            paras.append(cur)
            cur = []
    gloss_pat = re.compile(r"^(இ\s*[-–]\s*ள்|இதன்\s*பொருள்)\s*[.:]?\s*")
    gist_pat = re.compile(r"^(இ\s*[-–]\s*ம்|இதனது\s*தாற்பரியம்)\s*[.:]?\s*")
    starts = [k for k, para in enumerate(paras) if k and gloss_pat.match(para[0])]
    entries = []
    for n, k in enumerate(starts):
        stop = starts[n + 1] - 1 if n + 1 < len(starts) else len(paras)
        entry = {"text": [clean_line(l) for l in paras[k - 1][-4:]],
                 "gloss": [], "meaning": [], "notes": []}
        field = "gloss"
        for para in paras[k:stop]:
            for line in para:
                if gist_pat.match(line):
                    field = "meaning"
                    entry["meaning"].append(gist_pat.sub("", line))
                elif field == "gloss":
                    entry["gloss"].append(gloss_pat.sub("", line))
                elif re.fullmatch(r"எ\s*-\s*ம்\.?", line) and entry["meaning"]:
                    entry["meaning"].append(line)
                else:
                    entry["notes"].append(line)
                    field = "notes"
            if field == "meaning":
                field = "notes"
        entry["notes"] = [l for l in entry["notes"]
                          if not re.search(r"முற்றிற்று", l) and l not in ("நூல்", "காப்பு.")]
        entries.append(entry)
    return entries


def navalar(units):
    lines = body("pmuni0743").split("\n")
    parts = {
        "aathichudi": navalar_lines(section(lines, r"^1\. ஔவையார் பாடல்கள் - ஆத்திசூடி",
                                            r"^கொன்றை வேந்தன் - மூலமும்")),
        "kondrai_vendhan": navalar_lines(section(lines, r"^ஆத்தி சூடி மூலமும் விளக்கவுரையும் முற்றிற்று",
                                                 r"^கொன்றை வேந்தன் மூலமும் விளக்கவுரையும் முற்றிற்று")),
        "nalvazhi": navalar_verses(section(lines, r"^3\. ஒளவையார் அருளிச்செய்த நல்வழி",
                                           r"^நல்வழியுரை முற்றிற்று")),
        "moodurai": navalar_verses(section(lines, r"^4\. ஒளவையார் அருளிச்செய்த வாக்குண்டாம்",
                                           r"^வாக்குண்டாமுரை")),
    }
    result, raw_counts = {}, {}
    for key, entries in parts.items():
        raw_counts[key] = len(entries)
        base = [grams(" ".join(u["tamil"])) for u in units[key]]
        other = [grams(" ".join(e["text"])) for e in entries]
        for i, (j, score) in align(base, other).items():
            e = entries[j]
            if not e["meaning"] and e["gloss"]:  # '[க--]' inside a wrapped gloss line
                parts_ = re.split(r"\[க\s*-+\s*(?:உ)?\s*\]", " ".join(e["gloss"]), maxsplit=1)
                if len(parts_) == 2:
                    e["gloss"], e["meaning"] = [parts_[0].strip()], [parts_[1].strip()]
            result[(key, i)] = ({"text": e["text"], "gloss": " ".join(e["gloss"]) or None,
                                 "meaning": " ".join(e["meaning"]) or None,
                                 "notes": " ".join(e["notes"]) or None}, score)
    return result, raw_counts


# ---------- Ramabharathi, Aathichudi Venba (pmuni0481) ----------

def ramabharathi(units):
    text = body("pmuni0481").split("### நூல்.", 1)[1]
    blocks, cur = [], []
    for raw in text.split("\n") + ["___"]:
        if RULE.match(raw):
            if any(l.strip() for l in cur):
                blocks.append(cur)
            cur = []
        else:
            cur.append(raw)
    entries, closing = [], []
    for block in blocks:
        paras, p = [], []
        for raw in block + [""]:
            if raw.strip():
                p.append(raw.strip())
            elif p:
                paras.append(p)
                p = []
        if len(paras) < 2 or len(paras[1]) < 4:
            continue
        sutra = paras[0][0].rstrip(".")
        if sutra == "வாழி":  # the closing benediction, not a reading of an Aathichudi line
            closing.append(" / ".join(paras[1][:4]))
            continue
        venba = paras[1][:4]
        m = re.search(r"\((\d+)\)\s*$", venba[-1])
        rest = [line for para in paras[2:] for line in para]
        story_title = None
        if rest and rest[0].rstrip(".").replace(" ", "").endswith("கதை") and len(rest[0]) < 40:
            story_title = rest.pop(0).rstrip(".")
        entries.append({"sutra": sutra, "printed_number": int(m.group(1)) if m else None,
                        "venba": [re.sub(r"\s*\(\d+\)\s*$", "", l).replace("\u200c", "")
                                  for l in venba],
                        "story_title": story_title,
                        "story": " ".join(rest) or None})  # or a pointer such as 'இதன் கதையை ... காண்க'
    base = [grams(" ".join(u["tamil"])) for u in units["aathichudi"]]
    other = [grams(e["sutra"]) for e in entries]
    result = {}
    for i, (j, score) in align(base, other).items():
        if i == 0:
            continue  # Ramabharathi's own kaappu is not a reading of Avvaiyar's
        result[("aathichudi", i)] = (entries[j], score)
    if closing:
        print(f"ramabharathi: closing benediction left out: {closing[0][:40]!r}")
    return result, entries


# ---------- Sundara Shanmuganar, Nalvazhi naya urai (pmuni0777) ----------

def shanmuganar(units):
    lines = body("pmuni0777").split("\n")
    blocks, cur = [], []
    for raw in lines + ["---"]:
        if RULE.match(raw):
            if cur:
                blocks.append(cur)
            cur = []
        elif raw.strip():
            cur.append(raw.strip())
    entries = []
    for block in blocks:
        block = [l for l in block if not l.startswith("#") and l != "கடவுள் வாழ்த்து"]
        tl = [l for l in block if TAMIL.search(l)]
        if len(tl) < 5:
            continue
        end = next((k for k in range(4) if re.search(r"\d+\s*$", tl[k])), 3)
        if end < 3:
            print(f"shanmuganar: verse printed on {end + 1} lines: {tl[0]!r}")
        verse = tl[:end + 1]
        prose = " ".join(l for l in block[block.index(verse[-1]) + 1:] if l != ".")
        entries.append({"text": [clean_line(l) for l in verse], "prose": prose})
    base = [grams(" ".join(u["tamil"])) for u in units["nalvazhi"]]
    other = [grams(" ".join(e["text"])) for e in entries]
    result = {}
    for i, (j, score) in align(base, other).items():
        if entries[j]["prose"]:
            result[("nalvazhi", i)] = (entries[j]["prose"], score)
    return result, len(entries)


def main():
    problems = []
    units = base_units(problems)
    for key, *_ in WORKS:
        got = sum(1 for u in units[key] if u["number"])
        status = "ok" if got == EXPECTED[key] else "MISMATCH"
        print(f"{key}: {got} units plus invocation (expected {EXPECTED[key]}) {status}")
    nav, nav_raw = navalar(units)
    ram, ram_entries = ramabharathi(units)
    shan, shan_raw = shanmuganar(units)
    weak = []
    counts = {"navalar": {}, "ramabharathi": 0, "shanmuganar": 0}
    seq = 0
    with open(OUT, "w", encoding="utf-8") as out:
        for key, title, _, _ in WORKS:
            for i, u in enumerate(units[key]):
                seq += 1
                n = nav.get((key, i))
                r = ram.get((key, i))
                s = shan.get((key, i))
                for name, hit in (("navalar", n), ("ramabharathi", r), ("shanmuganar", s)):
                    if hit and hit[1] < 0.4:
                        weak.append(f"{key}:{u['number']} {name} score={hit[1]:.2f} "
                                    f"base={' '.join(u['tamil'])[:40]!r}")
                if n:
                    counts["navalar"][key] = counts["navalar"].get(key, 0) + 1
                record = {"id": f"avvaiyar:{key}:{u['number']}", "seq": seq, "work": key,
                          "work_tamil": title, "number": u["number"],
                          "printed_number": u["printed_number"],
                          "invocation": u["number"] == 0, "group": u["group"],
                          "tamil": u["tamil"],
                          "navalar": n[0] if n else None,
                          "ramabharathi": None, "shanmuganar": s[0] if s else None,
                          "match": {name: round(hit[1], 2) for name, hit in
                                    (("navalar", n), ("ramabharathi", r), ("shanmuganar", s)) if hit}}
                if key == "aathichudi" and r:
                    counts["ramabharathi"] += 1
                    e = r[0]
                    record["ramabharathi"] = {"sutra": e["sutra"], "venba": e["venba"],
                                              "printed_number": e["printed_number"],
                                              "story_title": e["story_title"], "story": e["story"]}
                if s:
                    counts["shanmuganar"] += 1
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
    used = {id(r[0]) for r in ram.values()}
    unused = [e["sutra"] for e in ram_entries if id(e) not in used]
    print(f"records={seq}")
    print(f"navalar raw entries={nav_raw} aligned={counts['navalar']}")
    print(f"ramabharathi raw entries={len(ram_entries)} aligned={counts['ramabharathi']} "
          f"unaligned={unused}")
    print(f"shanmuganar raw entries={shan_raw} aligned={counts['shanmuganar']}")
    for p in problems:
        print("SOURCE:", p)
    for w in weak:
        print("WEAK:", w)


if __name__ == "__main__":
    main()
