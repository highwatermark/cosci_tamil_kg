#!/usr/bin/env python3
"""Parse Tirumular's Tirumanthiram (the tenth Thirumurai) into kg/core/tirumanthiram.jsonl.

Sources, all in data/text/ (Project Madurai, one running verse number 1-3047):
  pmuni0004      preface (paayiram, 1-112), first tantra (113-336), second tantra (337-548)
  pmuni0009_01   third tantra (549-883)
  pmuni0009_02   fourth tantra, but only 884-1154 (the file stops there; 1155-1418 are absent)
  pmuni0009_03   fifth tantra (1419-1572) and sixth tantra (1573-1703)
  pmuni0010_01   seventh tantra (1704-2121)
  pmuni0010_02   eighth tantra (2122-2648)
  pmuni0010_03   ninth tantra (2649-3047)
  pmuni0395_01   V. S. Sengalvaraya Pillai's table of parallels (1951), keyed by verse number

Catalog rows 35/36 name the same pmuni0009 files, and rows 37/38 the same pmuni0010 files.

Verse numbers appear as '12.', '.549..', '1419' and '74' (missing its full stop). Chapter
headings appear as '1.. title', '.1.. title', '1. title', '8.1 title' (sections of the ninth
tantra's chapter 8) and once '2, title'. Variant readings follow some verses as '.(1). word',
'(1) word' or '[1] word'; their markers inside the verse lines are removed and kept apart.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "data" / "text"
OUT = ROOT / "kg" / "core" / "tirumanthiram.jsonl"
TANTRA_NAMES = {0: "பாயிரம்", 1: "முதல் தந்திரம்", 2: "இரண்டாம் தந்திரம்", 3: "மூன்றாம் தந்திரம்",
                4: "நான்காம் தந்திரம்", 5: "ஐந்தாம் தந்திரம்", 6: "ஆறாம் தந்திரம்",
                7: "ஏழாம் தந்திரம்", 8: "எட்டாம் தந்திரம்", 9: "ஒன்பதாம் தந்திரம்"}
# (file, tantra, the line that opens it); a tantra starts at its marker line
FILES = [("pmuni0004", [(0, "### பாயிரம்"), (1, "### திருமந்திரம் - முதல் தந்திரம்"),
                        (2, "### இரண்டாந் தந்திரம்")]),
         ("pmuni0009_01", [(3, "மூன்றாம் தந்திரம் (செய்யுட்கள்")]),
         ("pmuni0009_02", [(4, "நான்காம் தந்திரம் (செய்யுட்கள்")]),
         ("pmuni0009_03", [(5, "ஐந்தாம் தந்திரம் (1419"), (6, "திருமந்திரம் - ஆறாம் தந்திரம்")]),
         ("pmuni0010_01", [(7, "ஏழாம் தந்திரம்")]),
         ("pmuni0010_02", [(8, "எட்டாம் தந்திரம் (சுப்பிராமேம்)")]),
         ("pmuni0010_03", [(9, "ஒன்பதாம் தந்திரம்")])]
TRADITIONAL_LAST = 3047

TAMIL = re.compile(r"[஀-௿]")
NON_TAMIL = re.compile(r"[^஀-௿]")
VERSE_NO = re.compile(r"^\.?(\d{1,4})\.{0,2}$")
VERSE_WITH_TEXT = re.compile(r"^(\d{3,4})\.{1,2}\s*([஀-௿].*)$")  # '997. தம்பனம்', '526..தெளிவுறு ...'
HEADING = re.compile(r"^\.?(\d{1,2})(?:\.(\d{1,2})(?=\s)|\.{1,2}|,|(?=\s))\s*(.*[஀-௿].*)$")
# Misprinted verse numbers: (file, printed number, number printed just before it) -> true number.
# Each sits in an unbroken run, e.g. 2685, 2686, '2667', 2688.
MISPRINTS = {("pmuni0010_01", 2014, 2103): 2104,
             ("pmuni0010_03", 2667, 2686): 2687,
             ("pmuni0010_03", 2943, 2842): 2843,
             ("pmuni0010_03", 2944, 2843): 2844,
             ("pmuni0010_03", 2707, 2906): 2907,
             ("pmuni0010_03", 2903, 3002): 3003,
             ("pmuni0010_03", 2904, 3003): 3004,
             ("pmuni0010_03", 2905, 3004): 3005,
             ("pmuni0010_03", 3219, 3018): 3019}
VARIANT = re.compile(r"^\.?[(\[]\d+[)\]]\.?\s*")
MARKER = re.compile(r"\s*\.?\(\d+\)\.?\s*|\s*\[\d+\]\s*")
RANGE = re.compile(r"\s*\(\s*(\d+)\s*-\s*(\d+)\s*\)\s*\)?\s*$")
END = ("முற்றிற்று", "முடிவு பெற்றது", "திருச்சிற்றம்பலம்")
LOCAL_NO = re.compile(r"\s+(\d{1,3})\.?$")


def body(name):
    text = (TEXT / f"{name}.txt").read_text(encoding="utf-8")
    return text.split("=== BODY ===", 1)[1].split("=== FOOTER ===", 1)[0]


def strip_markers(line):
    return re.sub(r"\s{2,}", " ", MARKER.sub(" ", line)).strip()


def finish(verse, raw, problems):
    """Split the lines gathered after a verse number into verse lines, variant readings and any
    stray lines. A line opening with a marker such as '.(1).' is a verse line while the verse has
    fewer than four lines (the marker points at a variant), and a variant reading after that."""
    tamil, variants, extra = [], [], []
    for line in raw:
        if not TAMIL.search(line):
            continue
        if len(tamil) < 4 and not (VARIANT.match(line) and tamil and LOCAL_NO.search(tamil[-1])):
            tamil.append(line)
        elif VARIANT.match(line):
            variants.append(VARIANT.sub("", line).strip())
        else:
            extra.append(line)
    if tamil:
        m = LOCAL_NO.search(tamil[-1])
        if m:
            verse["chapter_verse"] = int(m.group(1))
            tamil[-1] = tamil[-1][:m.start()].rstrip()
    verse["tamil_source"] = [strip_markers(l) for l in tamil]
    verse["tamil"] = [repair(l) for l in verse["tamil_source"]]
    if verse["tamil"] == verse["tamil_source"]:
        del verse["tamil_source"]
    verse["variants"] = variants or None
    if extra:
        verse["extra_lines"] = extra
        problems.append(f"{verse['number']}: extra lines {extra}")
    if len(tamil) != 4:
        problems.append(f"{verse['number']}: {len(tamil)} lines in {verse['source']} {tamil}")
    bad = [l for l in verse["tamil"] if re.search(r"[A-Za-z\\஢]", l)]
    if bad:
        verse["corrupt_lines"] = bad
        problems.append(f"{verse['number']}: corrupt characters {bad}")


def repair(line):
    """Undo two known TSCII conversion faults: 'ரி' printed as 'ா஢' and 'ளி' as 'ௌi'."""
    line = line.replace("ொ஢", "ெரி").replace("ோ஢", "ேரி").replace("ா஢", "ரி")
    return line.replace("ௌi", "ெளி").replace("ஔi", "ஒளி")


def new_verse(n, tantra, chapter, section, name, subheading):
    return {"id": f"tirumanthiram:{n}", "number": n, "tantra": tantra,
            "tantra_name": TANTRA_NAMES[tantra],
            "chapter_no": chapter[0] if chapter else None,
            "chapter": chapter[1] if chapter else None,
            "section_no": section[0] if section else None,
            "section": section[1] if section else None,
            "subheading": subheading, "chapter_verse": None, "source": name}


def parse():
    """Walk each file line by line. A verse runs from its number to the next number, heading,
    separator or end line. Short lines left over after a verse's four lines are the unnumbered
    sub-headings of the next verse (the eight limbs of yoga, the eight siddhis...)."""
    verses, problems = {}, []
    for name, starts in FILES:
        tantra, chapter, section, current, raw, pending, last = None, None, None, None, [], [], 0
        subheading = None

        def close():
            nonlocal current, raw, subheading, pending
            if current:
                finish(current, raw, problems)
                extra = current.get("extra_lines") or []
                if extra and all(len(l.split()) <= 2 and len(l) > 2 and not re.search(r"\d", l) for l in extra):
                    subheading = " ".join(extra)
                    del current["extra_lines"]
                    problems.remove(f"{current['number']}: extra lines {extra}")
            elif len([l for l in pending if TAMIL.search(l)]) >= 3 and chapter:
                n = max(verses, default=0) + 1  # a verse whose number was dropped
                current = new_verse(n, tantra, chapter, section, name, subheading)
                current["number_inferred"] = True
                verses[n] = current
                finish(current, pending, problems)
                problems.append(f"{n}: number missing in {name}, inferred from its neighbours")
                subheading = None
            elif pending and all(VARIANT.match(l) for l in pending):
                problems.append(f"variant reading of the chapter title {chapter}: {pending}")
            elif pending and all(len(l.split()) <= 3 for l in pending):
                subheading = " ".join(pending)
            elif pending:
                problems.append(f"dropped in {name}: {pending}")
            current, raw, pending = None, [], []

        for line in body(name).split("\n"):
            line = line.strip()
            marker = next((t for t, s in starts if line.startswith(s)), None)
            if marker is not None:
                close()
                tantra, chapter, section, pending = marker, None, None, []
                continue
            if tantra is None or not line:
                continue
            number, inline = VERSE_NO.match(line), VERSE_WITH_TEXT.match(line)
            head = None if number or inline else HEADING.match(line)
            if number or inline or head or line.startswith(("#", "---")) or any(e in line for e in END):
                close()
            if number or inline:
                printed = int((number or inline).group(1))
                n = MISPRINTS.get((name, printed, last), printed)
                if n != printed:
                    problems.append(f"{n}: printed as {printed} in {name} (corrected)")
                last = n
                expected = max(verses, default=0) + 1
                if n in verses:
                    problems.append(f"{n}: doubled in {name}, second copy skipped")
                    continue
                if n != expected:
                    problems.append(f"{n}: out of sequence in {name} (expected {expected})")
                current = new_verse(n, tantra, chapter, section, name, subheading)
                subheading = None
                verses[n] = current
                if inline:
                    text = inline.group(2).strip()
                    if len(text.split()) <= 2:
                        current["subheading"] = text
                    else:
                        raw.append(text)
            elif head:
                title = head.group(3).replace(".(.", "(").replace(".).", ")").replace(".)", ")")
                title = strip_markers(title).strip().rstrip(".").strip()
                rng = RANGE.search(title)
                if rng:
                    title = title[:rng.start()].strip()
                if head.group(2):  # '8.1 title': a section inside chapter 8, which has no heading
                    if not chapter or chapter[0] != int(head.group(1)):
                        chapter = (int(head.group(1)), title)
                    section = (int(head.group(2)), title)
                else:
                    chapter, section = (int(head.group(1)), title), None
                subheading = None
            elif current is not None:
                raw.append(line)
            elif chapter is not None and not line.startswith(("#", "---")) and \
                    not any(e in line for e in END):
                pending.append(line)
        close()
    return verses, problems


def grams(text):
    letters = NON_TAMIL.sub("", text)
    return {letters[i:i + 3] for i in range(len(letters) - 2)}


def parallels(verses):
    """Sengalvaraya Pillai's 'ஒப்புமைப் பகுதி': rows 'verse-no  Tirumanthiram phrase  source  parallel'.

    A row starts with the verse number; the lines after it, until the next number, add further
    parallels to the same verse. The quoted phrase is checked against the verse by trigrams, since
    his numbering follows the Kasi Mutt edition, not necessarily Project Madurai's."""
    text = body("pmuni0395_01")
    text = text.split("### ஒப்புமைப் பகுதி", 1)[1]
    rows, current = {}, None
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith(("[", "செய்யுள் எண்")):
            continue
        if line.startswith("---"):
            break
        m = re.match(r"^(\d{1,4})\s+(.+)$", line)
        if m:
            current = int(m.group(1))
            rows.setdefault(current, []).append(m.group(2))
        elif current is not None:
            rows[current].append(line)
    aligned, mismatched = {}, []
    for n, entries in rows.items():
        phrase = grams(entries[0][:60])
        score = lambda m: len(phrase & grams(" ".join(verses[m]["tamil"]))) / (len(phrase) or 1)
        if n in verses and score(n) >= 0.2:
            aligned.setdefault(n, []).extend(entries)
            continue
        near = [m for m in range(n - 20, n + 21) if m in verses]
        best = max(near, key=score, default=None)
        if best is not None and score(best) >= 0.5:
            aligned.setdefault(best, []).extend(entries)
            mismatched.append((n, f"numbered {n} in the table, matched to {best} ({score(best):.2f})"))
        else:
            mismatched.append((n, "verse not in corpus" if n not in verses else
                               f"phrase overlap {score(n):.2f}, left out"))
    return aligned, mismatched


def main():
    verses, problems = parse()
    missing = [n for n in range(1, TRADITIONAL_LAST + 1) if n not in verses]
    par, mismatched = parallels(verses)
    with open(OUT, "w", encoding="utf-8") as out:
        for n in sorted(verses):
            record = verses[n] | {"sengalvaraya_parallels": par.get(n)}
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    runs, start = [], None
    for n in missing + [None]:
        if start is None:
            start = prev = n
        elif n == prev + 1:
            prev = n
        else:
            runs.append(f"{start}-{prev}" if start != prev else str(start))
            start = prev = n
    for p in problems:
        print("PROBLEM", p)
    for n, why in mismatched:
        print("PARALLEL UNALIGNED", n, why)
    per_tantra = {}
    for v in verses.values():
        per_tantra[v["tantra"]] = per_tantra.get(v["tantra"], 0) + 1
    print(f"verses={len(verses)} missing={len(missing)} ({', '.join(r for r in runs if r != 'None')}) "
          f"per_tantra={per_tantra} sengalvaraya={len(par)}")


if __name__ == "__main__":
    main()
