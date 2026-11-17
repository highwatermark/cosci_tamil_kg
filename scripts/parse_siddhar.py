#!/usr/bin/env python3
"""Parse the Siddhar songs (சித்தர் பாடல்கள்) into kg/core/siddhar.jsonl.

The book is a corpus of many small works by many poets, spread over these files in data/text/:
  pmuni0074     Pathrakiriyar, Meynjanap pulambal (base text)
  pmuni0155     'Ekkalak kanni', an anonymous palm-leaf recension of the same pulambal (1953 ed.)
  pmuni0076     Collection I: Azhuganni, Ramadevar, Kaduveli, Kudhambai, Sattaimuni,
                Thirumular Njanam, Thiruvalluvar Njanam
  pmuni0083     Pattinathar, Thiruppadal thirattu (part I)
  pmuni0270     Pattinathar part II (1887 edition of A. Ramaswamy): four Thirumurai-11 works and
                the Thiruppadal thirattu, with the editor's variant readings
  pmuni0276_01  Pattinathar part III: Arutpulambal 1-4
  pmuni0276_02  Pattinathar part IV: Puranamalai, Nenjodu magizhdal, Udarkootru vannam
  pmuni0269     Sivavakkiyar, Sivavakkiyam, with word glosses
  pmuni0212     Collection 4: Agappei, Idaikkadar (with end-note glosses), Konganar Valaik kummi
  pmuni0701     Valaik kummi, anonymous palm-leaf edition (R. Kumaravel, 2007)
  pmuni0857     Collection 8: Pambatti, Sangili, Thirikona Siddhar
  pmuni0858     Collection 9: Mouna Siddhar, Punnakku, Kanjamalai, Nondi Siddhar
  pmuni0859     Collection 10: Kakapusundar, Agasthiyar, Romarishi, Valmiki, Subramaniar Njanam
  pmuni0853_02  Madurai Valaisami, Njanak kummi

Each work is cut out of its file by line range and split into numbered units (stanza, kanni or
couplet, as the file numbers them). The same song often appears in two files; units are matched
across files by letter trigrams (rare trigrams only, so refrains do not count) and kept once, with
every source listed. pmuni0127_02 (Thirumurai 11) is read only to mark the Thirumurai overlap.
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "data" / "text"
OUT = ROOT / "kg" / "core" / "siddhar.jsonl"
NON_TAMIL = re.compile(r"[^஀-௿]")
TAMIL = re.compile(r"[஀-௿]")
SAME_MATCH, SAME_WORK_MATCH, CROSS_MATCH = 0.25, 0.2, 0.3
SEPARATOR = re.compile(r"^(?:[-=_*\s]{2,}|[-=_*.\s]{4,})$")
STRAY_LATIN = re.compile(r"(?<=[஀-௿])f(?=\s|$)")  # a stray Latin f typed after a Tamil letter
TRAILING_NO = re.compile(r"^(.*?[^\d\s.])[\s.]*(\d{1,4})\s*\.?\s*$")
SPLIT_NO = re.compile(r"^(.*?[^\d\s.])[\s.]*(\d{1,2}) (\d)\s*\.?\s*$")  # '1 1' printed for 11
LEADING_NO = re.compile(r"^(\d{1,4})\.\s+(?=\S)")
INLINE_MARK = re.compile(r"\s*\[\d+\]\s*")
HEADWORDS = re.compile(
    r"(காப்பு|நூல்|விருத்தம்|வெண்பா|கலித்துறை|கலித் துறை|கொச்சகம்|ஆசிரியப்பா|கண்ணி|கண்ணிகள்|கும்மி|"
    r"பல்லவி|அனுபல்லவி|சரணம்|சரணங்கள்|வேறு|துதி|சிந்து|தாழிசை|குறவஞ்சிப்பா|செந்துறை|"
    r"கூற்று|கிளத்தல்|வணக்கம்|ஞானம்|நிலை|திருவிசைப்பா|திருச்சிற்றம்பலம்)[.\s)]*$")
METRE = re.compile(r"(விருத்தம்|வெண்பா|கலித்துறை|கலித் துறை|கொச்சகம்|ஆசிரியப்பா|கண்ணி|கண்ணிகள்|கும்மி|"
                   r"சிந்து|தாழிசை|செந்துறை|குறவஞ்சிப்பா|பல்லவி|சரணங்கள்|சரணம்|வேறு)[.\s)]*$")
DROP_LINES = re.compile(r"^(உ|சிவமயம்,?|கணபதிதுணை\.?|திருச்சிற்றம்பலம்\.?|\(முடிந்தது\).*|.*முற்றிற்று.*|"
                        r".*முற்றுப்பெற்றது.*|முற்றும்|ஞானக்கும்மி)$")

# file, first line, end line (exclusive), poet, work key, work title, options
SEGMENTS = [
    ("pmuni0074", 27, 727, "பத்திரகிரியார்", "meynjanap-pulambal", "மெய்ஞ்ஞானப் புலம்பல்", {}),
    ("pmuni0155", 47, 651, "பத்திரகிரியார்", "meynjanap-pulambal", "எக்காலக் கண்ணி (மெய்ஞ்ஞானப் புலம்பல்)", {}),
    ("pmuni0083", 38, 261, "பட்டினத்தார்", "thiruvekambamalai", "திருவேகம்பமாலை", {}),
    ("pmuni0083", 261, 363, "பட்டினத்தார்", "thiruthillai", "திருத்தில்லை", {}),
    ("pmuni0083", 363, 422, "பட்டினத்தார்", "koyil-thiruvagaval-1", "முதலாவது கோயிற்றிருவகவல்", {"poem": True}),
    ("pmuni0083", 422, 470, "பட்டினத்தார்", "koyil-thiruvagaval-2", "இரண்டாவது கோயிற்றிருவகவல்", {"poem": True}),
    ("pmuni0083", 470, 535, "பட்டினத்தார்", "koyil-thiruvagaval-3", "மூன்றாவது கோயிற்றிருவகவல்", {"poem": True}),
    ("pmuni0083", 535, 622, "பட்டினத்தார்", "kachchi-thiruvagaval", "நான்காவது கச்சித் திருவகவல்", {"poem": True}),
    ("pmuni0083", 622, 739, "பட்டினத்தார்", "thiruppadal-thirattu", "திருப்பாடல் திரட்டு (தலப் பாடல்கள்)", {}),
    ("pmuni0083", 739, 976, "பட்டினத்தார்", "arutpulambal-1", "அருட்புலம்பல் - முதல்வன் முறையீடு", {}),
    ("pmuni0083", 976, 1126, "பட்டினத்தார்", "arutpulambal-2", "அருட்புலம்பல் - மகடூ முன்னிலை", {}),
    ("pmuni0276_01", 38, 263, "பட்டினத்தார்", "arutpulambal-1", "அருட்புலம்பல் - முதல்வன் முறையீடு", {}),
    ("pmuni0276_01", 265, 622, "பட்டினத்தார்", "arutpulambal-2", "அருட்புலம்பல் - மகடூ முன்னிலை", {}),
    ("pmuni0276_01", 622, 670, "பட்டினத்தார்", "arutpulambal-3", "அருட்புலம்பல் - இறந்தகாலத்திரங்கல்", {}),
    ("pmuni0276_01", 670, 862, "பட்டினத்தார்", "arutpulambal-4", "அருட்புலம்பல் - நெஞ்சொடுபுலம்பல்", {}),
    ("pmuni0276_02", 37, 347, "பட்டினத்தார்", "puranamalai", "பூரணமாலை", {}),
    ("pmuni0276_02", 350, 450, "பட்டினத்தார்", "nenjodu-magizhdal", "நெஞ்சொடுமகிழ்தல்", {}),
    ("pmuni0276_02", 456, 587, "பட்டினத்தார்", "udarkootru-vannam", "உடற்கூற்றுவண்ணம்", {"carry": True}),
    ("pmuni0270", 1786, 2496, "பட்டினத்தார்", "thiruppadal-thirattu", "திருப்பாடல் திரட்டு (தலப் பாடல்கள்)", {}),
    ("pmuni0270", 44, 785, "பட்டினத்தார்", "thiruvidaimaruthur-mummanikkovai", "திருவிடைமருதூர் மும்மணிக்கோவை", {"thirumurai": True}),
    ("pmuni0270", 785, 988, "பட்டினத்தார்", "thirukkazhumala-mummanikkovai", "திருக்கழுமல மும்மணிக்கோவை", {"thirumurai": True, "carry": True}),
    ("pmuni0270", 988, 1509, "பட்டினத்தார்", "thiruvekambamudaiyar-thiruvandhadhi", "திருவேகம்பமுடையார் திருவந்தாதி", {"thirumurai": True}),
    ("pmuni0270", 1509, 1786, "பட்டினத்தார்", "thiruvotriyur-oru-pa-oru-pahdu", "திருவொற்றியூர்த்தொகை (ஒருபா ஒருபஃது)", {"thirumurai": True, "carry": True}),
    ("pmuni0269", 27, 2747, "சிவவாக்கியர்", "sivavakkiyam", "சிவவாக்கியம்", {"gloss_dash": True, "hold": {1356}}),
    ("pmuni0076", 38, 280, "அழுகணிச் சித்தர்", "azhuganni", "அழுகணிச் சித்தர் பாடல்கள்", {}),
    ("pmuni0076", 280, 375, "இராமதேவர்", "ramadevar-pujavidhi", "இராமதேவர் பூஜாவிதி", {}),
    ("pmuni0076", 375, 558, "கடுவெளிச் சித்தர்", "kaduveli-anandakkalippu", "கடுவெளிச் சித்தர் ஆனந்தக் களிப்பு", {}),
    ("pmuni0076", 558, 693, "குதம்பைச் சித்தர்", "kudhambai", "குதம்பைச் சித்தர் பாடல்கள்", {}),
    ("pmuni0076", 693, 752, "சட்டைமுனி", "sattaimuni-njanam", "சட்டைமுனி ஞானம்", {}),
    ("pmuni0076", 752, 835, "திருமூல நாயனார்", "thirumular-njanam", "திருமூல நாயனார் ஞானம்", {}),
    ("pmuni0076", 835, 948, "திருவள்ளுவர்", "thiruvalluvar-njanam", "திருவள்ளுவர் ஞானம்", {}),
    ("pmuni0212", 39, 517, "அகப்பேய்ச் சித்தர்", "agappei", "அகப்பேய்ச் சித்தர் பாடல்கள்", {"endnotes": 491}),
    ("pmuni0212", 537, 1127, "இடைக்காட்டுச் சித்தர்", "idaikkadar", "இடைக்காட்டுச் சித்தர் பாடல்கள்", {"endnotes": 1105}),
    ("pmuni0212", 1143, 1721, "கொங்கணச் சித்தர்", "valaik-kummi", "வாலைக் கும்மி", {}),
    ("pmuni0701", 241, 826, "கொங்கணச் சித்தர்", "valaik-kummi", "வாலைக் கும்மி (ஆசிரியர் தெரியாத சுவடி)", {}),
    ("pmuni0857", 34, 776, "பாம்பாட்டிச் சித்தர்", "pambatti", "பாம்பாட்டிச் சித்தர் பாடல்", {}),
    ("pmuni0857", 776, 961, "சங்கிலிச் சித்தர்", "sangili", "சங்கிலிச் சித்தர் பாடல்", {}),
    ("pmuni0857", 961, 1236, "திரிகோணச் சித்தர்", "thirikonar", "திரிகோணச் சித்தர் பாடல் (கலிவெண்பா)", {}),
    ("pmuni0858", 36, 101, "மௌனச் சித்தர் (வகுளிநாதர்)", "mounachiddhar", "மௌனச்சித்தர் பாடல்", {}),
    ("pmuni0858", 101, 184, "புண்ணாக்குச் சித்தர்", "punnakku", "புண்ணாக்குச் சித்தர் பாடல்", {}),
    ("pmuni0858", 184, 316, "கஞ்சமலைச் சித்தர்", "kanjamalai", "கஞ்சமலைச் சித்தர் பாடல்", {"carry": True, "flush_after": {187}}),
    ("pmuni0858", 316, 486, "நொண்டிச் சித்தர் (மச்சேந்திர நாதர்)", "nondi", "நொண்டிச் சித்தர் பாடல்", {}),
    ("pmuni0859", 37, 755, "காகபுசுண்டர்", "kakapusundar-njanam", "காகபுசுண்டர் ஞானம்", {}),
    ("pmuni0859", 755, 1218, "அகஸ்தியர்", "agasthiyar-njanam", "அகஸ்தியர் ஞானம்", {}),
    ("pmuni0859", 1218, 1341, "உரோம ரிஷி", "romarishi-njanam", "உரோம ரிஷி ஞானம்", {}),
    ("pmuni0859", 1341, 1488, "வால்மீகர்", "valmiki-sutra-njanam", "வால்மீகர் சூத்திர ஞானம்", {}),
    ("pmuni0859", 1488, 1790, "சுப்பிரமணியர்", "subramaniar-njanam", "சுப்பிரமணியர் ஞானம்", {}),
    ("pmuni0853_02", 37, 963, "மதுரை வாலைசாமி", "njanak-kummi", "ஞானக்கும்மி", {}),
]
# Works whose poet is a legendary or canonical name rather than a known Siddhar author.
ATTRIBUTED = {"thirumular-njanam", "thiruvalluvar-njanam", "agasthiyar-njanam", "romarishi-njanam",
              "valmiki-sutra-njanam", "subramaniar-njanam", "kakapusundar-njanam", "ramadevar-pujavidhi",
              "valaik-kummi", "sattaimuni-njanam"}


def file_lines(name):
    return (TEXT / f"{name}.txt").read_text(encoding="utf-8").split("\n")


def grams(text):
    letters = NON_TAMIL.sub("", text)
    return {letters[i:i + 3] for i in range(len(letters) - 2)}


class Unit:
    def __init__(self, seg, line, heading):
        self.seg, self.line, self.heading = seg, line, list(heading)
        self.tamil, self.notes, self.glosses, self.number = [], [], [], None


def subheading(heading, line):
    """A metre name sits under the current part heading; any other heading replaces the part."""
    parts = [h for h in heading[1:] if not METRE.search(h)]
    if METRE.search(line):
        return heading[:1] + parts + [line]
    return heading[:1] + [line]


def parse_segment(lines, seg, problems):
    name, start, end, poet, key, title, opt = seg
    units, heading, pending, in_notes, last_gloss = [], [], None, False, None

    def nonblank_after(i):
        for j in range(i + 1, end - 1):
            if lines[j].strip():
                return lines[j].strip()
        return ""

    def flush(i):
        nonlocal pending, in_notes
        if pending and pending.tamil and opt.get("poem"):
            pending.number = 1
            units.append(pending)
        elif pending and pending.tamil:
            problems.append(f"{name}:{pending.line} [{key}] unit without a number "
                            f"({len(pending.tamil)} lines: {pending.tamil[0][:40]})")
            units.append(pending)
        elif pending and pending.notes and units:
            units[-1].notes += pending.notes
        pending, in_notes = None, False

    def close(number):
        nonlocal pending, in_notes
        pending.number = number
        units.append(pending)
        pending, in_notes = None, False

    for i in range(start - 1, end - 1):
        line = lines[i].strip()
        ln = i + 1
        if not line:
            if pending and not (opt.get("carry") or opt.get("poem") or pending.line in opt.get("hold", ())):
                flush(i)
            continue
        if opt.get("endnotes") and ln >= opt["endnotes"]:
            m = re.match(r"^(\d{1,4})\.\s*(.+)$", line)
            if m:
                target = [u for u in units if u.number == int(m.group(1))]
                if target:
                    target[-1].glosses.append(m.group(2).strip())
                    last_gloss = target[-1]
                else:
                    problems.append(f"{name}:{ln} [{key}] end note for missing verse {m.group(1)}")
            elif not SEPARATOR.match(line) and last_gloss is not None:
                last_gloss.glosses[-1] += " " + line
            continue
        if line.startswith("#"):
            flush(i)
            heading = [line.lstrip("#").strip()]
            continue
        if SEPARATOR.match(line):
            if pending and nonblank_after(i).startswith("["):
                in_notes = True
            else:
                flush(i)
            continue
        if DROP_LINES.match(line):
            continue
        if STRAY_LATIN.search(line):
            problems.append(f"{name}:{ln} [{key}] stray Latin 'f' removed: {line[:40]}")
            line = STRAY_LATIN.sub("", line)
        if pending and re.search(r"\S\s*-{3,}$", line):  # 'verse line ----' before variant notes
            line = re.sub(r"\s*-{3,}$", "", line)
            pending.tamil.append(line)
            in_notes = nonblank_after(i).startswith("[")
            continue
        if pending and re.match(r"^\d+\.\s*\S+=", line):  # '1. துரு=ஆராய்ச்சி ...' editor's note
            m = TRAILING_NO.match(line)
            pending.notes.append(re.sub(r"[\s.]*\d+\s*$", "", line) if m else line)
            if m:
                close(int(m.group(2)))
            continue
        if ln in opt.get("flush_after", ()):
            pending = pending or Unit(seg, ln, heading)
            pending.tamil.append(line)
            flush(i)
            continue
        lacuna = re.match(r"^[.\s…]+?(\d+)$", line)
        if lacuna:  # '... ... ... 49': the verse is lost, only its number is printed
            pending = Unit(seg, ln, heading)
            problems.append(f"{name}:{ln} [{key}] verse {lacuna.group(1)} is printed as dots only (lost)")
            pending.tamil = []
            close(int(lacuna.group(1)))
            continue
        if line.isdigit():  # a paragraph number on its own line
            if pending and pending.tamil:
                close(int(line))
            continue
        m = SPLIT_NO.match(line) or TRAILING_NO.match(line)
        # '[n] reading ... என்றும் பாடம்' is a variant note; '[n] verse text' is a verse line that
        # carries a note marker; '[word - meaning]' in Sivavakkiyam is a gloss.
        marker_verse = re.match(r"^\[\d+\]", line) and not in_notes and not re.search(r"பாடம்|=| - ", line)
        if line.startswith("[") and (pending or opt.get("gloss_dash")) and not marker_verse:
            text = (m.group(1) if m else line).strip()
            if opt.get("gloss_dash"):
                text = text.strip("[] ")
                if pending is None and units:
                    units[-1].glosses.append(text)
                    continue
                pending.glosses.append(text)
            else:
                pending.notes.append(text)
            if m:
                close(int(m.group(2)))
            continue
        if in_notes:
            pending.notes.append((m.group(1) if m else line).strip())
            if m:
                close(int(m.group(2)))
            continue
        if pending is None and opt.get("gloss_dash") and " - " in line and len(line) <= 80 and units:
            gm = re.match(r"^(\d+)\.\s*(.+)$", line)
            target = [u for u in units if gm and u.number == int(gm.group(1))] or units[-1:]
            target[-1].glosses.append(gm.group(2) if gm else line)
            continue
        if ln in opt.get("hold", ()):
            pending = Unit(seg, ln, heading)
            pending.tamil.append(line)
            continue
        if pending is None and len(line) <= 45 and not m and (
                not nonblank_after(i) or not lines[i + 1].strip() or HEADWORDS.search(line)):
            if opt.get("gloss_dash") and " - " in line:
                gm = re.match(r"^(\d+)\.\s*(.+)$", line)
                target = [u for u in units if gm and u.number == int(gm.group(1))] or units[-1:]
                target[-1].glosses.append(gm.group(2) if gm else line)
            else:
                heading = subheading(heading, line.rstrip(".").strip())
            continue
        if pending is None and m and len(m.group(1)) <= 15:  # 'ஞானம் - 2': a numbered heading
            heading = subheading(heading, line)
            continue
        if pending is None:
            pending = Unit(seg, ln, heading)
            lead = LEADING_NO.match(line)
            if lead and not opt.get("poem"):
                line = line[lead.end():]
        if opt.get("poem"):
            pending.tamil.append(INLINE_MARK.sub(" ", re.sub(r"[\s.]*\d+\s*$", "", line)).strip())
            continue
        if m:
            text, number = m.group(1), int(m.group(2))
            if m.re is SPLIT_NO:
                joined = int(m.group(2) + m.group(3))
                if units and units[-1].number is not None and joined == units[-1].number + 1:
                    number = joined
                    problems.append(f"{name}:{ln} [{key}] number printed '{m.group(2)} {m.group(3)}', read {joined}")
                else:
                    text, number = f"{m.group(1)} {m.group(2)}", int(m.group(3))
            if text.strip():
                pending.tamil.append(INLINE_MARK.sub(" ", text).strip())
            close(number)
        else:
            pending.tamil.append(INLINE_MARK.sub(" ", line).strip())
    if opt.get("poem") and pending:
        close(1)
    flush(end)
    return units


def check_numbers(units, key, problems):
    """Numbering runs restart at 1 (or 0); inside a run each number should be the last plus one."""
    run, prev = 1, None
    for k, u in enumerate(units):
        n = u.number
        u.printed = n
        src = f"{u.seg[0]}:{u.line}"
        if n is None:
            nxt = next((v.number for v in units[k + 1:k + 2]), None)
            if prev is not None and nxt == prev + 2:
                u.number = n = prev + 1
                problems.append(f"{src} [{key}] no number printed; {n} inferred from its neighbours")
            else:
                u.run = run
                continue
        if prev is not None and n <= 1 and prev >= 1:
            run += 1
        elif prev is not None and n != prev + 1:
            nxt = next((v.number for v in units[k + 1:k + 2]), None)
            if (n > prev + 1 and str(n).startswith(str(prev + 1)) and len(str(n)) > len(str(prev + 1))) \
                    or nxt == prev + 2:
                problems.append(f"{src} [{key}] number misprinted {n}, read {prev + 1}")
                u.number = n = prev + 1
            else:
                problems.append(f"{src} [{key}] number {n} follows {prev}")
        u.run, prev = run, n


def main():
    problems, units, cache = [], [], {}
    for seg in SEGMENTS:
        if seg[0] not in cache:
            cache[seg[0]] = file_lines(seg[0])
        seg_units = parse_segment(cache[seg[0]], seg, problems)
        check_numbers(seg_units, seg[4], problems)
        for k, u in enumerate(seg_units):
            u.prev = seg_units[k - 1] if k else None
        units += seg_units

    # Duplicates: the same poet's song in another file, by letter-trigram Jaccard. Editions differ
    # in sandhi and spelling (pmuni0270 runs words together), so the bar is low but the match must
    # be the best one among that poet's units. The same text under another poet's name is not
    # merged: it is kept under each name and cross-linked as a parallel.
    for u in units:
        u.grams = grams(" ".join(u.tamil))
        u.parallels = []
    index = defaultdict(set)
    kept, merged = [], 0
    for u in units:
        cands = Counter(k for g in u.grams for k in index[g])
        best, score, cross = None, 0.0, []
        for k, _ in cands.most_common(60):
            other = kept[k]
            if u.seg[0] in {s["file"] for s in other.sources}:
                continue
            s = len(u.grams & other.grams) / (len(u.grams | other.grams) or 1)
            # A different poet, or a separate canonical work (the Thirumurai-11 poems): link only.
            own = u.seg[6].get("thirumurai") or other.seg[6].get("thirumurai")
            if other.seg[3] != u.seg[3] or (own and other.seg[4] != u.seg[4]):
                if s >= CROSS_MATCH:
                    cross.append(other)
            elif s > score:
                best, score = other, s
        src = {"file": u.seg[0], "line": u.line, "work": u.seg[5], "number": u.printed}
        bar = SAME_WORK_MATCH if best is not None and best.seg[4] == u.seg[4] else SAME_MATCH
        if best is not None and score >= bar - 1e-9:
            best.sources.append(src | {"match": round(score, 2)})
            u.holder = best
            best.glosses += [g for g in u.glosses if g not in best.glosses]
            best.notes += [n for n in u.notes if n not in best.notes]
            for o in cross:
                if o not in best.parallels:
                    best.parallels.append(o)
                    o.parallels.append(best)
            merged += 1
            continue
        u.sources = [src]
        u.holder = u
        for o in cross:
            u.parallels.append(o)
            o.parallels.append(u)
        for g in u.grams:
            index[g].add(len(kept))
        kept.append(u)

    # Same text twice inside one file: report, keep both.
    for u in kept:
        u.repeat = None
    by_file = defaultdict(list)
    for k, u in enumerate(kept):
        by_file[u.seg[0]].append(k)
    for name, ks in by_file.items():
        for a_i, a in enumerate(ks):
            for b in ks[a_i + 1:]:
                ua, ub = kept[a], kept[b]
                if len(ua.grams) > 20 and len(ub.grams) > 20:
                    s = len(ua.grams & ub.grams) / len(ua.grams | ub.grams)
                    if s >= 0.5:
                        problems.append(f"{name}:{ub.line} [{ub.seg[4]}] repeats {name}:{ua.line} "
                                        f"(score {s:.2f}); both kept")

    # Thirumurai 11 overlap: Pattinathar's five works there (pmuni0127_02 lines 58-2874) are
    # numbered 'NNN text'; a unit matching one of those verses gets its Thirumurai number.
    th = file_lines("pmuni0127_02")
    blocks, cur = [], []
    for line in th[57:2874] + [""]:
        if line.strip() and not line.startswith("#"):
            cur.append(line.strip())
        elif cur:
            m = re.match(r"^(\d{3,4})\s", cur[0])
            if m:
                blocks.append((int(m.group(1)), grams(" ".join(cur))))
            elif blocks:
                blocks[-1] = (blocks[-1][0], blocks[-1][1] | grams(" ".join(cur)))
            cur = []
    th_index = defaultdict(set)
    for k, (_, b) in enumerate(blocks):
        for g in b:
            th_index[g].add(k)
    for u in kept:
        u.thirumurai = []
        cands = Counter(k for g in u.grams for k in th_index[g])
        scored = sorted(((len(u.grams & blocks[k][1]) / (len(u.grams | blocks[k][1]) or 1), blocks[k][0])
                         for k, _ in cands.most_common(6)), reverse=True)
        if scored and scored[0][0] >= 0.3:
            u.thirumurai = [scored[0][1]]
    for seg in SEGMENTS:
        if seg[6].get("thirumurai"):
            us = [u for u in kept if u.seg[4] == seg[4]]
            hit = sum(1 for u in us if u.thirumurai)
            problems.append(f"{seg[0]} [{seg[4]}] {hit} of {len(us)} units found in Thirumurai 11 "
                            f"(pmuni0127_02)")
    for u in kept:
        if u.thirumurai and not u.seg[6].get("thirumurai"):
            problems.append(f"{u.seg[0]}:{u.line} [{u.seg[4]}] also in Thirumurai 11 as {u.thirumurai}")

    # Ids: work key plus the number; a run index when the work restarts its numbering.
    runs = defaultdict(set)
    for u in kept:
        runs[u.seg[4]].add(getattr(u, "run", 1))
    seen, unnumbered = set(), Counter()
    for u in kept:
        u.uid = None
    order = {}
    for seg in SEGMENTS:
        order.setdefault(seg[4], len(order))
    # Canonical order: the work's base file in its own order; a unit found only in another file
    # goes right after the base unit that holds its predecessor in that file.
    base = {}
    for seg in SEGMENTS:
        base.setdefault(seg[4], seg[0])
    position = {id(u): k for k, u in enumerate(kept)}

    def sort_key(u):
        if u.seg[0] == base[u.seg[4]]:
            return (order[u.seg[4]], position[id(u)], 0, 0)
        p = u.prev
        while p is not None and p.holder.seg[0] != base[u.seg[4]]:
            p = p.prev
        anchor = position[id(p.holder)] if p is not None else -1
        return (order[u.seg[4]], anchor, 1, position[id(u)])
    kept.sort(key=sort_key)
    for u in kept:
        key = u.seg[4]
        primary = u.seg[0] == next(s[0] for s in SEGMENTS if s[4] == key)
        if u.number is None:
            unnumbered[key, u.seg[0]] += 1
            label = f"u{unnumbered[key, u.seg[0]]}"
        else:
            label = str(u.number)
            if len(runs[key]) > 1:
                label = f"{u.run}.{u.number}"
        if not primary:
            label = f"{u.seg[0].replace('pmuni', '')}-{label}"
        uid = f"siddhar:{key}:{label}"
        while uid in seen:
            uid += "b"
        seen.add(uid)
        u.uid = uid
    with open(OUT, "w", encoding="utf-8") as out:
        for seq, u in enumerate(kept, 1):
            key = u.seg[4]
            record = {
                "id": u.uid, "seq": seq, "siddhar": u.seg[3], "work": key,
                "work_title": next(s[5] for s in SEGMENTS if s[4] == key),
                "number": u.number, "run": getattr(u, "run", 1),
                "section": [h for h in u.heading[1:] if h] or None,
                "tamil": u.tamil,
                "glosses": u.glosses or None,
                "variant_notes": u.notes or None,
                "attribution": "attributed" if key in ATTRIBUTED else "traditional",
                "thirumurai_11": u.thirumurai or None,
                "sources": u.sources,
                "parallels": [o.uid for o in u.parallels] or None,
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    counts = Counter(u.seg[4] for u in kept)
    print(f"units={len(kept)} parsed={len(units)} merged_duplicates={merged}")
    print(f"glosses={sum(1 for u in kept if u.glosses)} variant_notes={sum(1 for u in kept if u.notes)} "
          f"multi_source={sum(1 for u in kept if len(u.sources) > 1)} "
          f"thirumurai_11={sum(1 for u in kept if u.thirumurai)} "
          f"parallels={sum(1 for u in kept if u.parallels)}")
    for key in order:
        print(f"  {key}: {counts[key]}")
    print(f"problems ({len(problems)}):")
    for p in problems:
        print("  " + p)


if __name__ == "__main__":
    main()
