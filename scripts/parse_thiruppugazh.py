#!/usr/bin/env python3
"""Parse Arunagirinathar's Thiruppugazh into kg/core/thiruppugazh.jsonl.

Sources, all in data/text/ (Project Madurai, from the kaumaram.com e-text, songs in four parts):
  pmuni0180  part 1, songs 1-330
  pmuni0187  part 2, songs 331-670
  pmuni0189  part 3, songs 671-1000
  pmuni0191  part 4, songs 1001-1326
There is no translation or commentary of the Thiruppugazh in the corpus; only the text.

Each song is headed '### பாடல் N ( thalam )', then a raga/tala line, sometimes a tala breakdown,
the santham (the 'தனதன' rhythm pattern), and the verse in blank-separated line groups.

The printed numbers are not reliable: several are misprinted (a number printed twice, the next one
skipped, digits split by a space, a letter for a digit), two headings lost their '###' in the
conversion, two songs are printed twice, and some headings are printed twice. The traditional
number is therefore taken from the song's position, and checked against each part's printed range.
Every disagreement between the printed and positional number is printed.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "data" / "text"
OUT = ROOT / "kg" / "core" / "thiruppugazh.jsonl"
PARTS = [("pmuni0180", 1, 1, 330), ("pmuni0187", 2, 331, 670),
         ("pmuni0189", 3, 671, 1000), ("pmuni0191", 4, 1001, 1326)]
TOTAL = 1326

HEAD = re.compile(r"^(?:###\s*)?பாடல்\s+([0-9][0-9 ]*[0-9த]?)\s*(.*)$")
TAMIL = re.compile(r"[஀-௿]")
NON_TAMIL = re.compile(r"[^஀-௿]")
# Letters of the santham syllables (தன, தான, தந்த, தத்த, தய்ய, தனண, திமி, தகிட ...).
SANTHAM_CHARS = set("தனநமகடயணஞிீாுெேைொோ்")

# Headings that name a kind of song or a section, not a temple.
NOT_PLACES = {"விநாயகர் துதி": "invocation", "விநாயகர்": "invocation", "நூல்": "opening",
              "பொதுப்பாடல்கள்": "general", "புதிய பாடல்கள்": "new",
              "க்ஷேத்திரக் கோவை": "list of shrines", "ஆறு திருப்பதி": "six shrines",
              "குன்றுதோறாடல்": "all hills", "திருவெழுகூற்றிருக்கை": "figured poem"}
# Conversion debris in temple names (TSCII to Unicode). Only spellings we are sure of.
NAME_FIXES = {"திருவர்ருர்": "திருவாரூர்", "திருவாருர்": "திருவாரூர்", "திருப்பேர்ருர்": "திருப்பேரூர்",
              "உ த்தர§ம்ருர்": "உத்தரமேரூர்", "உ த்தரகோசமங்கை": "உத்தரகோசமங்கை",
              "பூவர்ளுர்": "பூவாளூர்", "சிங்கை - காங்கேயம் -": "சிங்கை - காங்கேயம்",
              "ஸ்ரீ முஷ்டம்": "ஸ்ரீமுஷ்டம்"}
CORRUPT = re.compile(r"[¡-ÿ஡஢஥஧]")


def body(name):
    text = (TEXT / f"{name}.txt").read_text(encoding="utf-8")
    return text.split("=== BODY ===", 1)[1].split("=== FOOTER ===", 1)[0]


def clean_name(raw):
    name = raw.strip().lstrip("-").strip().strip("()").strip()
    name = name.replace("ு¡", "ூ").replace("ு஡", "ூ")
    return NAME_FIXES.get(name, name)


def is_santham(line):
    letters = [c for c in line.replace("......", "") if TAMIL.search(c)]
    return bool(letters) and sum(c in SANTHAM_CHARS for c in letters) / len(letters) >= 0.97


def is_meta(line):
    s = line.strip()
    return (s.startswith("ராகம்") or s.startswith("தாளம்") or s.startswith("(") or
            s.startswith("எடுப்பு") or s == "அமைப்பு" or
            bool(re.search(r"[0-9]", s)) or not TAMIL.search(s))


def songs_in(name):
    """Yield (printed_number, heading_text, lines) for each heading in the file, in order."""
    current = None
    for line in body(name).split("\n"):
        s = line.strip()
        m = HEAD.match(s)
        if m:
            printed, rest = m.group(1).replace(" ", ""), m.group(2)
            # A bare repeat of the heading just printed: skip it, keep its spelling as a variant.
            if not s.startswith("###") and current and not any(l.strip() for l in current[2]):
                current[3].append(rest.strip())
                continue
            if current:
                yield current
            current = [printed, rest, [], []]
            continue
        if current:
            current[2].append(line.rstrip())
    if current:
        yield current


def split_song(lines):
    """Return raga, tala, notes, santham lines, verse lines, and any problems."""
    blocks, block = [], []
    for line in lines + [""]:
        s = line.strip()
        if s and not re.fullmatch(r"[-*\s]+", s):
            block.append(s)
        elif block:
            blocks.append(block)
            block = []
    raga = tala = None
    notes, santham, verse, problems = [], [], [], []
    for b in blocks:
        rest = []
        for s in b:
            if s.startswith("ராகம்"):
                parts = s.split(";", 1)
                raga = parts[0].split("-", 1)[-1].strip() or None
                if len(parts) > 1:
                    tala = parts[1].split("-", 1)[-1].strip() or None
            elif s.startswith("தாளம்"):
                tala = s.split("-", 1)[-1].strip() or None
            elif not verse and not santham and is_meta(s):
                notes.append(s)
            else:
                rest.append(s)
        if not rest:
            continue
        if not verse and all(is_santham(s) or is_meta(s) for s in rest):
            santham.extend(rest)
        else:
            verse.append(rest)
    if raga and set(raga) <= set(". "):
        raga = None
    if tala and set(tala) <= set(". "):
        tala = None
    if not santham:
        problems.append("no santham found")
    lines_out = [s for b in verse for s in b]
    while lines_out and re.fullmatch(r"\(?[0-9][0-9-]*\)?", lines_out[-1]):
        notes.append(lines_out.pop())  # reference codes such as '(0507-0000-2442)' after a song
    if not lines_out:
        problems.append("no verse lines")
    if any(is_santham(s) for s in lines_out[:1]):
        problems.append("first verse line looks like santham")
    return raga, tala, notes, santham, lines_out, problems


def grams(text):
    letters = NON_TAMIL.sub("", text)
    return {letters[i:i + 3] for i in range(len(letters) - 2)}


def main():
    records, issues = [], []
    for name, part, first, last in PARTS:
        prev_text, raw = None, list(songs_in(name))
        kept = []
        for k, (printed, heading, lines, variants) in enumerate(raw):
            raga, tala, notes, santham, verse, problems = split_song(lines)
            text = "\n".join(verse)
            if prev_text is not None and text == prev_text:
                issues.append(f"{name}: song printed '{printed}' repeats the song before it word for "
                              f"word; dropped")
                # If the next heading skips a number, the repeat stands in for a lost song: keep
                # its place with an empty record so the traditional numbers stay right.
                before = kept[-1][0]
                after = raw[k + 1][0] if k + 1 < len(raw) else None
                if before.isdigit() and after and after.isdigit() and int(after) == int(before) + 2:
                    issues.append(f"{name}: song {int(before) + 1} is missing from the source (its "
                                  f"place holds a second copy of {before}); kept as an empty record")
                    kept.append((str(int(before) + 1), heading, None, None, None, [], [], [],
                                 ["text missing in source"]))
                continue
            prev_text = text
            kept.append((printed, heading, variants, raga, tala, notes, santham, verse, problems))
        if len(kept) != last - first + 1:
            issues.append(f"{name}: {len(kept)} songs, expected {last - first + 1} ({first}-{last})")
        for i, (printed, heading, variants, raga, tala, notes, santham, verse,
                problems) in enumerate(kept):
            n = first + i
            if printed != str(n):
                issues.append(f"song {n}: printed number '{printed}'")
            label = clean_name(heading)
            kind = NOT_PLACES.get(label, "place")
            corrupt = sum(len(CORRUPT.findall(l)) for l in verse)
            for p in problems:
                if p == "text missing in source":
                    continue
                issues.append(f"song {n}: {p}")
            records.append({
                "id": f"thiruppugazh:{n}", "number": n, "printed_number": None if "text missing in source" in problems else printed,
                "part": part, "source": name,
                "heading": label, "heading_raw": heading.strip(),
                "heading_variants": variants or None,
                "kind": kind, "thalam": label if kind == "place" else None,
                "raga": raga, "tala": tala, "tala_notes": notes or None,
                "santham": santham, "tamil": verse,
                "corrupt_chars": corrupt or None,
                "missing": True if "text missing in source" in problems else None,
            })
    numbers = [r["number"] for r in records]
    if numbers != list(range(1, TOTAL + 1)):
        issues.append(f"numbering broken: {len(numbers)} songs")
    # Order of temples: each place should form one run (song groups are kept together).
    runs, last_label = {}, None
    for r in records:
        if r["heading"] != last_label:
            runs.setdefault(r["heading"], []).append(r["number"])
            last_label = r["heading"]
    for label, starts in runs.items():
        if len(starts) > 1 and label not in ("விநாயகர்", "விநாயகர் துதி"):
            issues.append(f"heading '{label}' occurs in separate runs starting at {starts}")
    with open(OUT, "w", encoding="utf-8") as out:
        for r in records:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")
    for line in issues:
        print("CHECK", line)
    places = {r["thalam"] for r in records if r["thalam"]}
    print(f"songs={len(records)} places={len(places)} "
          f"general={sum(r['kind'] == 'general' for r in records)} "
          f"with_raga={sum(bool(r['raga']) for r in records)} "
          f"lines={sum(len(r['tamil']) for r in records)} "
          f"songs_with_corrupt_chars={sum(bool(r['corrupt_chars']) for r in records)}")


if __name__ == "__main__":
    main()
