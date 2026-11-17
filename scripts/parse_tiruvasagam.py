#!/usr/bin/env python3
"""Parse the Tiruvasagam (Thirumurai 8, Manikkavasagar) into kg/core/tiruvasagam.jsonl.

Sources, all in data/text/:
  pmuni0003_01  hymns 1-10 (Tamil, the base text)
  pmuni0003_02  hymns 11-51 (Tamil)
  pmuni0094     G.U. Pope's English translation (1900), hymns 1-10
  pmuni0222     G.U. Pope's English translation (1900), hymns 11-51
  pmuni0659     Kausalya Hart's English translation (modern; rights: modern)

Units follow Project Madurai's running numbers (1-661): hymns 1-4 (the akavals) are one unit
each, every later stanza is one unit. The base text ends each stanza with that running number.

Hart ends each stanza with the same running number in brackets, so she aligns by number.
Pope prints no Tamil; he ends each stanza with a running line count in parentheses, (4), (8) ...
so his stanza index within a hymn is that count divided by the hymn's step. Where a count is
missing, the merged chunk is split at Pope's Roman-numeral stanza headings if it can be.
As a check, every Pope stanza is compared with Hart's stanzas of the same hymn by shared English
words, and stanzas whose best Hart match is a different stanza are printed.
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "data" / "text"
OUT = ROOT / "kg" / "core" / "tiruvasagam.jsonl"
AKAVALS = 4
LAST = 661
ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
LATIN = re.compile(r"(?<=[஀-௿])[A-Za-z]+|[A-Za-z]+(?=[஀-௿])")
PLACE_FIX = [("த்தில்", "ம்"), ("யில்", ""), ("ரில்", "ர்"), ("ில்", "்")]
STOP = set("the a an of and to in is my me you your i he his him o that with who for on as are be not "
           "thou thy thee it this all by at was were from but have has so or no".split())


def body(name):
    text = (TEXT / f"{name}.txt").read_text(encoding="utf-8")
    return text.split("=== BODY ===", 1)[1].split("=== FOOTER ===", 1)[0]


def roman(s):
    total = 0
    for a, b in zip(s, s[1:] + " "):
        x = ROMAN[a]
        total += -x if b != " " and ROMAN[b] > x else x
    return total


def place_of(note):
    m = re.search(r"([^\s(]+)\s*அருளி?யது", note)  # 'அருளயது' is misprinted once (hymn 3)
    if not m or m.group(1) == "வாசகர்":
        return None
    word = m.group(1)
    for suffix, repl in PLACE_FIX:
        if word.endswith(suffix):
            return word[: -len(suffix)] + repl
    return word


# ---------------------------------------------------------------- Tamil base text

def base_units():
    units, problems = {}, []
    lines = (body("pmuni0003_01") + "\n" + body("pmuni0003_02")).split("\n")
    hymn = None
    buf = []
    expected = AKAVALS + 1
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        i += 1
        head = re.match(r"^###\s+(\d+)\.\s*(.+)$", line)
        if head or line.startswith("### திருவாசகம் முற்றிற்று"):
            if hymn and hymn["no"] <= AKAVALS:
                units[hymn["no"]] = akaval_unit(hymn, buf)
            buf = []
            if not head:
                hymn = None
                continue
            no = int(head.group(1))
            title, _, subtitle = head.group(2).partition(" - ")
            hymn = {"no": no, "title": title.strip(), "subtitle": subtitle.strip() or None,
                    "note": None, "place": None, "decad": None, "decad_no": None, "count": 0}
            continue
        if hymn is None or not line or line.startswith("#") or line in ("Back", "திருச்சிற்றம்பலம்"):
            continue
        nxt = next((l.strip() for l in lines[i:i + 3] if l.strip()), "")
        if hymn["note"] is None and not buf and not line.startswith("(") and nxt.startswith("(") \
                and hymn["subtitle"] is None:
            hymn["subtitle"] = line  # hymn 23 prints its subtitle on its own line
            continue
        if line.startswith("(") and not buf and hymn["count"] == 0:
            note = line
            while ")" not in note and i < len(lines):
                note += " " + lines[i].strip()
                i += 1
            if hymn["note"] is None:
                hymn["note"] = note.strip("() ")
                hymn["place"] = place_of(note)
            else:  # hymn 7 gives its metre in a second parenthesis
                hymn["note"] += "; " + note.strip("() ")
            continue
        if LATIN.search(line):
            problems.append(f"tamil: stray Latin letters removed in hymn {hymn['no']}: {line}")
            line = LATIN.sub("", line)
        decad = re.match(r"^(\d+)\.\s*(\S.*?)\s*(\((.+)\))?$", line)
        if hymn["no"] == 5 and decad and not buf:
            hymn["decad_no"], hymn["decad"] = int(decad.group(1)), decad.group(2)
            hymn["decad_metre"] = decad.group(4)
            continue
        if hymn["no"] <= AKAVALS:
            buf.append(re.sub(r"\s+\d+\s*$", "", line))
            continue
        end = re.match(r"^(.*?)\s*(\d+)\s*$", line)
        if end and int(end.group(2)) >= expected and int(end.group(2)) <= expected + 2:
            n = int(end.group(2))
            if n != expected:
                problems.append(f"tamil: expected {expected}, found {n} in hymn {hymn['no']}")
            buf.append(end.group(1).strip())
            hymn["count"] += 1
            units[n] = {
                "number": n, "hymn": hymn["no"], "verse_in_hymn": hymn["count"],
                "hymn_title": hymn["title"], "hymn_subtitle": hymn["subtitle"],
                "place": hymn["place"], "hymn_note": hymn["note"],
                "tamil": buf,
            }
            if hymn["no"] == 5:
                units[n]["decad_no"] = hymn["decad_no"]
                units[n]["decad"] = hymn["decad"]
                units[n]["decad_metre"] = hymn.get("decad_metre")
            buf = []
            expected = n + 1
        else:
            buf.append(line)
    return units, problems


def akaval_unit(hymn, buf):
    return {"number": hymn["no"], "hymn": hymn["no"], "verse_in_hymn": 1,
            "hymn_title": hymn["title"], "hymn_subtitle": hymn["subtitle"],
            "place": hymn["place"], "hymn_note": hymn["note"], "tamil": buf}


# ---------------------------------------------------------------- Hart

def hart():
    """Stanzas end with '[N]' (Project Madurai's running number); hymns 1-4 are whole sections."""
    found, problems = {}, []
    lines = body("pmuni0659").split("\n")
    section, buf, prev = None, [], AKAVALS
    for line in lines:
        s = line.strip()
        head = re.match(r"^###\s+(\d+)\.\s", s)
        if s.startswith("###"):
            if section and section <= AKAVALS:
                found[section] = clean_hart(buf)
            section = int(head.group(1)) if head else None
            buf = []
            continue
        if s in ("SUBHAM",) or re.match(r"^This file was last updated", s):
            continue
        if section is None:
            continue
        if section <= AKAVALS:
            buf.append(re.sub(r"\s+\d+$", "", s))  # line numbers
            continue
        m = re.search(r"\[(\d+)\]\s*$", s)
        buf.append(re.sub(r"\s*\[\d+\]\s*$", "", s))
        if not m:
            continue
        n = int(m.group(1))
        missing = n - prev - 1
        stanzas = split_numbered(buf)
        if missing == 0:
            found[n] = clean_hart(stanzas[-1] if stanzas else buf)
        elif len(stanzas) >= missing + 1:
            for k, st in enumerate(stanzas[-(missing + 1):]):
                found[prev + 1 + k] = clean_hart(st)
            problems.append(f"hart: no marker for {list(range(prev + 1, n))}; split at stanza numbers")
        else:
            found[n] = clean_hart(buf)
            problems.append(f"hart: no marker for {list(range(prev + 1, n))}; could not split")
        buf, prev = [], n
    return found, problems


def split_numbered(buf):
    """Split a chunk at lines starting with a local stanza number ('8. ...')."""
    out, cur = [], None
    for s in buf:
        if re.match(r"^\d+\.\s*\S", s) and not re.match(r"^\d+\.\d", s):
            cur = [s]
            out.append(cur)
        elif cur is not None:
            cur.append(s)
    return out


def clean_hart(buf):
    keep = [s for s in buf if s and not re.match(r"^\d+\.\d+\.?\s", s)
            and not re.fullmatch(r"\d+(\s*-\s*\d+)?|-+", s)]  # line ranges, rules
    text = " ".join(keep)
    text = re.sub(r"^\d+\.\s*", "", text.strip())
    return " ".join(text.split()) or None


# ---------------------------------------------------------------- Pope

def pope_hymns():
    hymns, cur = {}, None
    for name in ("pmuni0094", "pmuni0222"):
        for line in body(name).split("\n"):
            m = re.match(r"^(#+\s*)?hymn\s+([IVXL]+|\d+)\b", line.strip(), re.I)
            if m:
                g = m.group(2)
                cur = int(g) if g.isdigit() else roman(g.upper())
                hymns[cur] = []
                continue
            if re.match(r"^#+\s*END OF TIRUVACAGAM", line.strip()):
                cur = None
            if cur:
                hymns[cur].append(line.rstrip())
    return hymns


MARK = re.compile(r"^(.*?)\s*(\(\s*(\d+)\s*\)|(\d+))\s*\.?\s*$")
HEAD = re.compile(r"^\s*([IVXLC]+)\s*\.\s*(.*)$")


def pope(units):
    """Returns {number: {"title", "text"}} and a list of problems."""
    per_hymn = Counter(u["hymn"] for u in units.values())
    first = {}
    for n, u in sorted(units.items()):
        first.setdefault(u["hymn"], n)
    found, problems = {}, []
    for h, lines in pope_hymns().items():
        marks = [int(m.group(3)) for m in (MARK.match(l.strip()) for l in lines) if m and m.group(3)]
        if not marks:
            problems.append(f"pope: hymn {h} has no line counts")
            continue
        if h <= AKAVALS:
            found[h] = pope_akaval(lines)
            continue
        step = min(b - a for a, b in zip([0] + marks, marks) if b > a)
        last_k, buf = 0, []
        for line in lines:
            s = line.strip()
            m = MARK.match(s)
            k = None
            if m:
                value = int(m.group(3) or m.group(4))
                if value % step == 0 and last_k < value // step <= last_k + 3 and \
                        (m.group(3) or value // step == last_k + 1):
                    k = value // step
            if k is None:
                buf.append(s)
                continue
            buf.append(m.group(1).strip())
            chunks = split_roman(buf)
            want = k - last_k
            numbered = [c[2] for c in chunks]
            if len(chunks) > want and numbered == list(range(last_k + 1, last_k + len(chunks) + 1)):
                problems.append(f"pope: hymn {h} line count ({value}) disagrees with Roman headings "
                                f"{numbered}; followed the headings")
                want, k = len(chunks), last_k + len(chunks)
                pieces = chunks
            elif want == 1:
                pieces = [chunks[-1] if chunks else ("", trim_intro(buf), None)]
            elif len(chunks) >= want:
                pieces = chunks[-want:]
                problems.append(f"pope: hymn {h} no line count for stanza(s) "
                                f"{list(range(last_k + 1, k))}; split at Roman headings")
            else:
                pieces = [None] * (want - 1) + [chunks[-1] if chunks else ("", trim_intro(buf), None)]
                problems.append(f"pope: hymn {h} stanzas {last_k + 1}-{k} merged; "
                                f"stanza(s) {list(range(last_k + 1, k))} left null")
            for j, piece in enumerate(pieces):
                idx = last_k + 1 + j
                if piece is None:
                    continue
                if idx > per_hymn[h]:
                    problems.append(f"pope: hymn {h} stanza {idx} beyond Tamil count {per_hymn[h]}")
                    continue
                title, text = piece[:2]
                found[first[h] + idx - 1] = {"title": title or None, "text": " ".join(text.split())}
            last_k, buf = k, []
        tail = [c for c in split_roman(buf) if c[1].strip()]
        if tail and last_k < per_hymn[h]:
            for title, text, _ in tail[: per_hymn[h] - last_k]:
                last_k += 1
                found[first[h] + last_k - 1] = {"title": title or None, "text": " ".join(text.split())}
                problems.append(f"pope: hymn {h} stanza {last_k} has no closing line count; taken from "
                                f"the end of the hymn")
        if last_k != per_hymn[h]:
            problems.append(f"pope: hymn {h} has {last_k} stanzas, Tamil has {per_hymn[h]}")
    return found, problems


def split_roman(buf):
    """Split at Roman-numeral headings; each piece is (title, text, numeral value)."""
    out = []
    for s in buf:
        m = HEAD.match(s)
        if m and len(s) < 120:
            out.append([m.group(2).strip(), [], roman(m.group(1))])
        elif out and not re.fullmatch(r"-+", s):
            out[-1][1].append(s)
    return [(t, "\n".join(x for x in body_ if x), r) for t, body_, r in out]


def trim_intro(buf):
    """Without a heading, keep the last blank-separated block that is verse, not prose or caps."""
    blocks, cur = [], []
    for s in buf + [""]:
        if s:
            cur.append(s)
        elif cur:
            blocks.append(cur)
            cur = []
    verse = [b for b in blocks if not any(len(x) > 200 for x in b) and not all(x.isupper() for x in b)]
    return "\n".join(verse[-1]) if verse else "\n".join(buf)


def pope_akaval(lines):
    """From the block holding the first line count to the last line count; drop notes and headings."""
    marks = [i for i, l in enumerate(lines) if MARK.match(l.strip()) and MARK.match(l.strip()).group(3)]
    start = marks[0]
    while start > 0 and lines[start - 1].strip():
        start -= 1
    text = []
    end = marks[-1] + 1
    while end < len(lines) and lines[end].strip() and not lines[end].startswith("#"):
        end += 1  # the closing lines after the last count
    for l in lines[start:end]:
        s = l.strip()
        if len(s) > 200 or re.match(r"^Lines\s+\d", s) or re.fullmatch(r"[.\s]*", s):
            continue
        m = MARK.match(s)
        text.append(m.group(1) if m and m.group(3) else s)
    return {"title": None, "text": " ".join(" ".join(text).split())}


# ---------------------------------------------------------------- cross-check

def words(text):
    return {w for w in re.findall(r"[a-z]+", (text or "").lower()) if w not in STOP and len(w) > 2}


def cross_check(units, pope_found, hart_found):
    """Pope vs Hart within each hymn: is Pope's stanza most like Hart's stanza of the same number?"""
    off = []
    by_hymn = {}
    for n, u in units.items():
        by_hymn.setdefault(u["hymn"], []).append(n)
    for h, ns in by_hymn.items():
        if h <= AKAVALS:
            continue
        for n in ns:
            if n not in pope_found or n not in hart_found:
                continue
            pw = words(pope_found[n]["text"])

            def sim(m):
                hw = words(hart_found.get(m))
                return len(pw & hw) / (len(pw | hw) or 1)
            best = max(ns, key=sim)
            if best != n and sim(best) > sim(n) + 0.02:
                off.append((n, best, round(sim(n), 3), round(sim(best), 3)))
    return off


def main():
    units, problems = base_units()
    missing = [n for n in range(1, LAST + 1) if n not in units]
    if missing:
        problems.append(f"tamil: missing units {missing}")
    order = sorted(units)
    if order != list(range(1, len(order) + 1)):
        problems.append("tamil: units out of order")
    for n in order:
        for t in units[n]["tamil"]:
            if t.startswith("(") or re.search(r"[A-Za-z]", t):
                problems.append(f"tamil: unit {n} has a non-verse line: {t}")
    hart_found, hp = hart()
    pope_found, pp = pope(units)
    problems += hp + pp
    with open(OUT, "w", encoding="utf-8") as out:
        for n in order:
            u = units[n]
            record = {
                "id": f"tiruvasagam:{n}",
                "number": n,
                "thirumurai": 8,
                "hymn": u["hymn"],
                "verse_in_hymn": u["verse_in_hymn"],
                "ref": f"8.{u['hymn']}.{u['verse_in_hymn']}",
                "hymn_title": u["hymn_title"],
                "hymn_subtitle": u["hymn_subtitle"],
            }
            for key in ("decad_no", "decad", "decad_metre"):
                if key in u:
                    record[key] = u[key]
            record |= {
                "place": u["place"],
                "hymn_note": u["hymn_note"],
                "unit": "akaval (whole hymn)" if u["hymn"] <= AKAVALS else "stanza",
                "tamil": u["tamil"],
                "pope": pope_found.get(n),
                "hart": hart_found.get(n),
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    counts = Counter(units[n]["hymn"] for n in order)
    print(f"units={len(units)} hymns={len(counts)} pope={len(pope_found)} hart={len(hart_found)}")
    print("stanzas per hymn:", " ".join(f"{h}:{c}" for h, c in sorted(counts.items())))
    print("thiruvempavai (hymn 7):", [n for n in order if units[n]["hymn"] == 7])
    for p in problems:
        print("PROBLEM", p)
    for n, best, s1, s2 in cross_check(units, pope_found, hart_found):
        print(f"CHECK pope {n} closer to hart {best} ({s1} vs {s2})")


if __name__ == "__main__":
    main()
