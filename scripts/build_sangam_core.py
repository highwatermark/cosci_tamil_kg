#!/usr/bin/env python3
"""Build the original Tamil text of the Akananuru and the Pattupattu, and check the Purananuru.

Writes:
  kg/core/akananuru.jsonl         the invocation (number 0) and poems 1-400, one record per poem
  kg/core/pattupattu.jsonl        the ten idylls, one record per poem with all its lines
  kg/core/pattupattu_units.jsonl  each idyll split into reading units of 10-25 lines
  kg/core/sangam_text_flags.jsonl misprints, repairs and checks for all three books

Reads only Project Madurai e-texts already mirrored in data/text/ (as parse_purananuru.py does):
  pmuni0229                 Akananuru, the text alone (base text for the verses)
  pmuni0490_01, _02         Akananuru 1-120 with M. Rajaram's commentary (colophons only)
  pmuni0523_01, _02         Akananuru 121-300 with N. M. Venkatasami Nattar's commentary (colophons only)
  pmuni0534                 Akananuru 301-400, the same (colophons only)
  pmuni0067 0063 0064 0069 0071 0070 0073 0077 0078
                            nine of the idylls, each with a colophon (poet, patron, thinai, thurai)
  pmuni0488                 Mullaippattu, U. V. Swaminatha Aiyar's text; only the verse block and
                            the poet's name from the closing colophon line are taken
  pmuni0057                 Purananuru, to check kg/core/purananuru.jsonl against

Copyright: only the verse lines and the traditional colophon facts are kept (poet, patron, thinai,
thurai, section, metre). Commentary, word meanings, modern headings and translations are never
copied. The commentary files are read only to find each poem's colophon and to compare line counts.

How the Pattupattu are split into reading units (pattupattu_units.jsonl)
-----------------------------------------------------------------------
Marking and linking need verse-sized pieces, so each idyll is cut into units of 10 to 25 lines.
A unit never crosses a section of the source (only Thirumurugatruppadai has them: the six abodes).
Inside a section the cut is greedy from the top. For a unit starting at line s, every end line e
with a unit length of 10-25 lines is scored by how strongly line e closes a sentence:
  3  the line ends in . ! ? or ; (only the punctuated texts have these), or its last word ends in
     the closing particle -ஏ (a consonant with ே, e.g. கிழவோனே, தொழிலே) or -ஓ (ோ, e.g. கொல்லோ);
     in Sangam verse these particles close a sentence or a whole speech
  2  the last word closes a quotation or a naming (என, எனா, எனக், என்று, என்ப, and the
     sandhi forms யென, வென, னென, ரென, லென, ளென, டென, றென), or the line ends in :
     or the last word is a vocative that closes an address (பொருந, பாண, விறலி, இரவல, கூத்த,
     பெரும, குரிசில், நெடுந்தகை, மகிழ்ந, தோழி, நெஞ்சே, அன்னாய்)
  1  the last word closes a comparison (அன்ன, போல, போலக், ஆங்கு, அற்றே, கடுப்ப, ஏய்ப்ப) or one
     member of a series of clauses (a word ending in -உம், e.g. பிறழவும்), or the line ends in ,
  0  anything else
The chosen end maximises 10 * score - |length - 16|, so a strong break wins and, among equal
breaks, the length nearest 16 lines wins. An end is not allowed if it would leave fewer than 10
lines in the section; a section remainder of 25 lines or fewer is taken whole. Unit ids are
pattupattu:<n>:<start>-<end> with the poem's own line numbers (1-based, inclusive).

Run: python3 -I scripts/build_sangam_core.py [--text-dir DIR] [--out-dir DIR]
"""
import argparse
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TAMIL_CHAR = re.compile(r"[\u0B80-\u0BFF]")
NON_TAMIL = re.compile(r"[^\u0B80-\u0BFF]")
ALLOWED_PUNCT = set(" .,;:!?'\"‘’“”-–—()")
VOWEL_SIGNS = set("\u0BBE\u0BBF\u0BC0\u0BC1\u0BC2\u0BC6\u0BC7\u0BC8\u0BCA\u0BCB\u0BCC\u0BCD\u0BD7")
CONSONANTS = set(chr(c) for c in range(0x0B95, 0x0BBA))
LINE_MARK = re.compile(r"(?:[\s.\-]*?)(\d(?: ?\d){0,2})[\s.\-]*$")
ZERO_WIDTH = re.compile(r"[\u200B-\u200D\uFEFF]")
RIGHTS = {"tamil": "public_domain", "colophon": "public_domain"}

# Akananuru: the three traditional sections, and the thinai fixed by the poem's number
# ('ஒன்றுமூன் றைந்தேழொன் பான்பாலை ...': odd = palai, 2 and 8 = kurinji, 4 = mullai,
# 6 = marutham, 10 = neythal, counting the last digit).
AKAM_SECTIONS = ((1, 120, "களிற்றியானைநிரை"), (121, 300, "மணிமிடைபவளம்"), (301, 400, "நித்திலக்கோவை"))
THINAI_BY_DIGIT = {1: "பாலை", 3: "பாலை", 5: "பாலை", 7: "பாலை", 9: "பாலை", 2: "குறிஞ்சி",
                   8: "குறிஞ்சி", 4: "முல்லை", 6: "மருதம்", 0: "நெய்தல்"}
THINAI_NAMES = "பாலை|குறிஞ்சி|முல்லை|மருதம்|நெய்தல்"

# Pattupattu: traditional order, source file, short name, and the standard line count.
PATTU = (
    (1, "pmuni0067", "thirumurugatruppadai", "திருமுருகாற்றுப்படை", 317),
    (2, "pmuni0063", "porunaratruppadai", "பொருநராற்றுப்படை", 248),
    (3, "pmuni0064", "sirupanatruppadai", "சிறுபாணாற்றுப்படை", 269),
    (4, "pmuni0069", "perumpanatruppadai", "பெரும்பாணாற்றுப்படை", 500),
    (5, "pmuni0488", "mullaippattu", "முல்லைப்பாட்டு", 103),
    (6, "pmuni0071", "maduraikkanchi", "மதுரைக்காஞ்சி", 782),
    (7, "pmuni0070", "nedunalvadai", "நெடுநல்வாடை", 188),
    (8, "pmuni0073", "kurinjippattu", "குறிஞ்சிப்பாட்டு", 261),
    (9, "pmuni0077", "pattinappalai", "பட்டினப்பாலை", 301),
    (10, "pmuni0078", "malaipadukadam", "மலைபடுகடாம்", 583),
)
PATTU_LABELS = {"பாடியவர்": "poet", "பாடப்பட்டவன்": "patron", "திணை": "thinai", "துறை": "thurai",
                "பாவகை": "metre", "மொத்த அடிகள்": "source_line_count", "மொத்த வரிகள்": "source_line_count"}

# Character repairs made in the verse lines; each one is written to the flags file.
# '·' is an old encoding of ஃ (as in parse_purananuru.py). '¦’' is a TSCII leftover for the
# vowel sign ெ written before the next consonant (பெரி¦’தன்று = பெரிதென்று).
REPAIRS = (
    (re.compile(r"·"), "ஃ", "'·' is the old encoding of ஃ"),
    (re.compile(r"¦’([\u0B95-\u0BB9])"), "\\1\u0BC6", "TSCII leftover '¦’' + consonant = consonant + ெ"),
    (re.compile(r"[\u200B-\u200D\uFEFF]"), "", "zero-width character removed"),
    # U+0BA1 is unassigned: an encoding leftover in two Akananuru words (3: ஞான்றே, 70: ஞாழல்;
    # both read so in the commentary editions).
    (re.compile(r"ஞா\u0BA1ன்றே"), "ஞான்றே", "unassigned U+0BA1 removed (read ஞான்றே)"),
    (re.compile(r"ஞ்\u0BA1ழ"), "ஞாழ", "unassigned U+0BA1 after ஞ் read as ஞா (ஞாழல்)"),
    # A word cannot begin with a dead consonant: 'கண்டோ ர்' and 'எ ன்ஆம்' are one word split
    # by a stray space (a typing artifact of the old fonts).
    (re.compile(r"(?<=[\u0B80-\u0BFF]) (?=[\u0B95-\u0BB9]\u0BCD)"), "",
     "stray space before a dead consonant removed (e.g. கண்டோ ர் = கண்டோர்)"),
)

flags = []


def flag(book, rid, kind, detail, line=None, text=None):
    rec = {"book": book, "id": rid, "kind": kind, "line": line, "detail": detail}
    if text is not None:
        rec["text"] = text
    flags.append(rec)


def body(text_dir, name):
    text = (text_dir / f"{name}.txt").read_text(encoding="utf-8")
    return text.split("=== BODY ===", 1)[1].split("=== FOOTER ===", 1)[0]


def split_mark(line):
    """'... தழீஇப் . 10' -> ('... தழீஇப்', 10). Lines without a trailing number get None.
    A few Akananuru lines end in '.<poem>-<line>' (e.g. 'நமக்கே. .129-18'): the line number is kept."""
    m = re.search(r"[\s.]*\.(\d{1,3})-(\d{1,3})[\s.]*$", line)
    if m and TAMIL_CHAR.search(line[:m.start()]):
        return line[:m.start()].rstrip(" .-").strip(), int(m.group(2))
    m = LINE_MARK.search(line)
    if not m or not TAMIL_CHAR.search(line[:m.start()]):
        return line.strip(), None
    rest = line[:m.start()].rstrip(" .-")
    return rest.strip(), int(m.group(1).replace(" ", ""))


def tidy(line):
    """Strip padding dots and spaces left by the line numbers; keep the text's own punctuation."""
    line = re.sub(r"\s+", " ", line).strip()
    line = re.sub(r"(?:\s+\.)+$", "", line)  # stray ' .' padding at the end
    line = re.sub(r"^\.\s*", "", line)
    return line


def repair(book, rid, n, line):
    for pat, rep, why in REPAIRS:
        new = pat.sub(rep, line)
        if new != line:
            flag(book, rid, "repaired", why, n, f"{line} -> {new}")
            line = new
    return line


def unicode_problems(line):
    """Return a list of problems: non-Tamil characters, unassigned Tamil code points, and
    vowel signs or pulli that do not follow a consonant."""
    out = []
    for i, ch in enumerate(line):
        if "\u0B80" <= ch <= "\u0BFF":
            try:
                unicodedata.name(ch)
            except ValueError:
                out.append(f"unassigned Tamil code point U+{ord(ch):04X}")
                continue
            if ch in VOWEL_SIGNS and ch != "\u0BD7":
                prev = line[i - 1] if i else ""
                if prev not in CONSONANTS:
                    out.append(f"vowel sign or pulli U+{ord(ch):04X} not after a consonant")
        elif ch not in ALLOWED_PUNCT:
            out.append(f"non-Tamil character {ch!r} (U+{ord(ch):04X})")
    return out


def check_lines(book, rid, lines):
    for i, l in enumerate(lines, 1):
        for p in unicode_problems(l):
            flag(book, rid, "unicode", p, i, l)
        if not TAMIL_CHAR.search(l):
            flag(book, rid, "empty_line", "line has no Tamil letters", i, l)
        if re.search(r"(?:^|[\s'‘“(])[\u0B95-\u0BB9]\u0BCD", l):
            flag(book, rid, "spelling", "a word begins with a dead consonant (letter lost?)", i, l)
    for i in range(1, len(lines)):
        if lines[i] == lines[i - 1]:
            flag(book, rid, "duplicate_line", "same line printed twice in a row", i + 1, lines[i])


def check_marks(book, rid, marks, total_expected=None):
    """marks: (position, printed number). Each printed number should equal the line's position."""
    bad = [(pos, num) for pos, num in marks if pos != num]
    if bad:
        pos, num = bad[0]
        flag(book, rid, "lineation", f"printed line number {num} stands on line {pos}"
             + (f" ({len(bad)} numbers off)" if len(bad) > 1 else ""), pos)
    return bad


def grams(text):
    letters = NON_TAMIL.sub("", text)
    return {letters[i:i + 3] for i in range(len(letters) - 2)}


def similarity(a, b):
    a, b = grams(a), grams(b)
    return len(a & b) / (len(a | b) or 1)


# --------------------------------------------------------------------------------------------
# Akananuru

def akam_base(text_dir):
    lines = body(text_dir, "pmuni0229").split("\n")
    start = max(i for i, l in enumerate(lines) if l.strip() == "## அகநானுறு")
    poems, cur, expected = {}, None, 0
    for raw in lines[start + 1:]:
        s = raw.strip()
        if not s or s.startswith("### ") or s.startswith("This page"):
            continue
        m = re.match(r"^(\d{1,3})\s+(\S.*)$", s)
        misnumbered = (m and cur is not None and int(m.group(1)) == expected - 1
                       and len(poems[cur]["raw"]) >= 3 and TAMIL_CHAR.search(m.group(2)))
        if m and (int(m.group(1)) == expected or misnumbered) and expected <= 400:
            if misnumbered:
                flag("akananuru", f"akananuru:{expected}", "numbering", f"poem {expected} is printed "
                     f"with the number {m.group(1)}; read as {expected}", 1, s)
            cur = expected
            poems[cur] = {"raw": [], "marks": []}
            expected += 1
            s = m.group(2)
        elif m and cur is not None and TAMIL_CHAR.search(m.group(2)):
            flag("akananuru", f"akananuru:{cur}", "numbering",
                 f"line starts with an unexpected number {m.group(1)} (expected poem {expected})", None, s)
        if cur is None:
            continue
        text, num = split_mark(s)
        text = tidy(text)
        if not text:
            continue
        poems[cur]["raw"].append(text)
        if num is not None:
            poems[cur]["marks"].append((len(poems[cur]["raw"]), num))
    return poems


def akam_colophons(text_dir):
    """Colophons (thinai, thurai, poet) and the commentary's copy of the verse, per poem."""
    out = {}

    def take_block(sec, poet_at):
        """Verse block = the non-blank lines just above the poet line."""
        j = poet_at - 1
        while j >= 0 and not sec[j].strip():
            j -= 1
        block = []
        while j >= 0 and sec[j].strip():
            block.insert(0, sec[j].strip())
            j -= 1
        return block

    def poet_from(sec, i):
        parts = [re.sub(r"^[-\s]+(\d+\s*)?", "", sec[i].strip())]
        k = i + 1
        if not TAMIL_CHAR.search(parts[0]):  # dots: the name is lost
            return parts[0]
        while k < len(sec) and sec[k].strip() and not sec[k].strip().startswith(("-", "(", "குறிப்பு")):
            parts.append(sec[k].strip())
            k += 1
        return " ".join(parts).strip()

    # 1-120 and the invocation: '### செய்யுள் N', 'திணை: ..', 'துறை: ..', verse, '--poet.'
    for name in ("pmuni0490_01", "pmuni0490_02"):
        lines = [ZERO_WIDTH.sub("", l) for l in body(text_dir, name).split("\n")]
        heads = [(int(m.group(1)), i) for i, l in enumerate(lines)
                 if (m := re.match(r"^### செய்யுள் (\d+)\s*$", l.strip()))]
        stop = next((i for i, l in enumerate(lines) if "முதற்குறிப்பு அகரவரிசை" in l), len(lines))
        if name == "pmuni0490_01":
            heads.insert(0, (0, next(i for i, l in enumerate(lines) if l.startswith("கார்விரி")) - 1))
        for k, (n, i) in enumerate(heads):
            end = heads[k + 1][1] if k + 1 < len(heads) else stop
            sec = lines[i:end]
            rec = {"source": name, "thinai": None, "thurai": None, "poet": None, "verse": []}
            for j, l in enumerate(sec[:8]):
                if (m := re.match(r"^திணை\s*[:;]\s*(.+)$", l.strip())) and not rec["thinai"]:
                    rec["thinai"] = m.group(1).strip(" .")
                if (m := re.match(r"^துறை\s*[:;]\s*(.+)$", l.strip())) and not rec["thurai"]:
                    rec["thurai"] = m.group(1).strip()
            at = next((j for j, l in enumerate(sec) if re.match(r"^-+[\s-]*[^\s-]", l.strip())
                       and (TAMIL_CHAR.search(l) or "...." in l)), None)
            if at is not None:
                rec["poet"] = poet_from(sec, at)
                rec["verse"] = take_block(sec, at)
            out[n] = rec
    # 121-400: 'N. thinai', '[thurai]', verse, '- poet.'
    for name in ("pmuni0523_01", "pmuni0523_02", "pmuni0534"):
        lines = [ZERO_WIDTH.sub("", l) for l in body(text_dir, name).split("\n")]
        heads = [(int(m.group(1)), m.group(2), i) for i, l in enumerate(lines)
                 if (m := re.match(rf"^(\d{{3}})\s*\.\s*({THINAI_NAMES})\s*$", l.strip()))]
        for k, (n, thinai, i) in enumerate(heads):
            end = heads[k + 1][2] if k + 1 < len(heads) else len(lines)
            sec = lines[i:end]
            rec = {"source": name, "thinai": thinai, "thurai": None, "poet": None, "verse": []}
            j = 1
            while j < len(sec) and not sec[j].strip():
                j += 1
            if j < len(sec) and sec[j].strip().startswith("["):
                t, j = sec[j].strip(), j + 1
                while "]" not in t and j < len(sec) and sec[j].strip():
                    t += " " + sec[j].strip()
                    j += 1
                rec["thurai"] = t.strip("[] ")
            at = next((j for j, l in enumerate(sec) if j > 1 and re.match(r"^-+[\s-]*[^\s-]", l.strip())
                       and (TAMIL_CHAR.search(l) or "...." in l)), None)
            if at is not None:
                rec["poet"] = poet_from(sec, at)
                rec["verse"] = take_block(sec, at)
            if n in out:
                flag("akananuru", f"akananuru:{n}", "colophon", f"two commentary sections numbered {n}")
            out[n] = rec
    return out


def clean_poet(raw):
    if not raw:
        return None, None
    note = None
    m = re.search(r"\(([^)]*)\)", raw)
    if m:
        note = m.group(1).strip()
        raw = raw[:m.start()] + raw[m.end():]
    if "#" in raw:  # '#' marks a footnote in the commentary files: 'குன்றியனார்#. # 1. சேரமானந்தையார்'
        raw, rest = raw.split("#", 1)
        rest = re.sub(r"[#\d.]+", " ", rest).strip()
        if rest:
            note = f"{note}; {rest}" if note else rest
    raw = re.sub(r"\d+", "", raw).replace("'", "")
    return re.sub(r"\s+", " ", raw).strip(" .-") or None, note


def comm_line(line):
    """A verse line of a commentary edition, without its footnote digits and line number."""
    text, _ = split_mark(line)
    return tidy(re.sub(r"\d+", "", text))


def align(base, comm):
    """Align base lines with the commentary edition's lines. Returns a list of steps:
    ('match', i, j), ('split', i, j) base line i = comm lines j and j+1,
    ('missing', None, j) comm line j absent from base, ('extra', i, None), ('merge', i, j)
    base lines i and i+1 = comm line j."""
    nb, nc = len(base), len(comm)
    INF = float("inf")
    cost = [[INF] * (nc + 1) for _ in range(nb + 1)]
    back = [[None] * (nc + 1) for _ in range(nb + 1)]
    cost[0][0] = 0.0
    for i in range(nb + 1):
        for j in range(nc + 1):
            c0 = cost[i][j]
            if c0 == INF:
                continue
            steps = []
            if i < nb and j < nc:
                steps.append(("match", 1, 1, 1 - similarity(base[i], comm[j])))
            if i < nb and j + 1 < nc and len(base[i].split()) > 1:
                a, b = split_at_words(base[i], comm[j], comm[j + 1])
                steps.append(("split", 1, 2, 0.3 + (1 - similarity(a, comm[j]))
                              + (1 - similarity(b, comm[j + 1]))))
            if i + 1 < nb and j < nc:
                steps.append(("merge", 2, 1, 1.3 - similarity(base[i] + " " + base[i + 1], comm[j])))
            if j < nc:
                steps.append(("missing", 0, 1, 0.95))
            if i < nb:
                steps.append(("extra", 1, 0, 0.95))
            for name, di, dj, c in steps:
                if c0 + c < cost[i + di][j + dj]:
                    cost[i + di][j + dj] = c0 + c
                    back[i + di][j + dj] = (name, i, j)
    out, i, j = [], nb, nc
    while i or j:
        name, pi, pj = back[i][j]
        out.append((name, pi if name != "missing" else None, pj if name != "extra" else None))
        i, j = pi, pj
    return out[::-1]


def split_at_words(line, first, second):
    """Split a base line that holds two lines at the word boundary that best matches them."""
    words = line.split()
    best, cut = -1.0, 1
    for k in range(1, len(words)):
        v = similarity(" ".join(words[:k]), first) + similarity(" ".join(words[k:]), second)
        if v > best:
            best, cut = v, k
    return " ".join(words[:cut]), " ".join(words[cut:])


def mend(rid, tamil, comm, intended):
    """Repair a base poem whose own printed line count (intended) disagrees with its lines, when
    the commentary edition has that many lines: split joined lines and supply missing ones.
    Returns (lines, supplied line numbers) or None when the two witnesses do not agree."""
    if len(comm) != intended or len(tamil) == intended:
        return None
    steps = align(tamil, comm)
    if any(k in ("extra", "merge") for k, _, _ in steps):
        return None
    out, supplied, notes = [], [], []
    for kind, i, j in steps:
        if kind == "match":
            out.append(tamil[i])
        elif kind == "split":
            a, b = split_at_words(tamil[i], comm[j], comm[j + 1])
            if not a or not b:
                return None
            out += [a, b]
            notes.append(f"line {len(out) - 1}: split '{tamil[i]}' into two lines, as printed in the "
                          "commentary edition")
        elif kind == "missing":
            out.append(comm[j])
            supplied.append(len(out))
            notes.append(f"line {len(out)}: missing from the base text; supplied from the commentary "
                          f"edition: '{comm[j]}'")
    if len(out) != intended:
        return None
    for note in notes:
        flag("akananuru", rid, "repaired", note)
    return out, supplied


def build_akananuru(text_dir):
    base = akam_base(text_dir)
    cols = akam_colophons(text_dir)
    records, tamil_by_n = [], {}
    for n in range(0, 401):
        rid = f"akananuru:{n}"
        if n not in base:
            flag("akananuru", rid, "missing_poem", "poem not found in the base text")
            continue
        b = base[n]
        c = cols.get(n)
        tamil = [repair("akananuru", rid, i, l) for i, l in enumerate(b["raw"], 1)]
        marks = list(b["marks"])
        last = marks[-1] if marks else None
        intended = last[1] if last and last[0] == len(tamil) else None
        # A stray copy of the previous poem's first line (122 opens with 121's first line).
        if n and n - 1 in base and tamil and tamil[0] == tamil_by_n.get(n - 1, [None])[0] \
                and intended == len(tamil) - 1:
            flag("akananuru", rid, "repaired", f"dropped line 1 '{tamil[0]}': a stray copy of the "
                 f"first line of poem {n - 1}; the printed line numbers then fit", 1)
            tamil = tamil[1:]
            marks = [(pos - 1, num) for pos, num in marks]
        supplied = []
        if intended and intended != len(tamil) and c and c["verse"]:
            fixed = mend(rid, tamil, [comm_line(l) for l in c["verse"]], intended)
            if fixed:
                tamil, supplied = fixed
                marks = [(intended, intended)]
            elif len(c["verse"]) == len(tamil):
                flag("akananuru", rid, "lineation", f"the last line is numbered {intended}, but the "
                     f"poem has {len(tamil)} lines, as in the commentary edition: a misprinted number",
                     len(tamil))
                marks = marks[:-1]
            else:
                flag("akananuru", rid, "line_count", f"{len(tamil)} lines, but the last line is "
                     f"numbered {intended}; the commentary edition has {len(c['verse'])}; not repaired")
                marks = marks[:-1]
        check_lines("akananuru", rid, tamil)
        check_marks("akananuru", rid, marks)
        if intended is None:
            flag("akananuru", rid, "lineation", "last line carries no line count", len(tamil))
        tamil_by_n[n] = tamil
        section = next(((name, lo, hi) for lo, hi, name in AKAM_SECTIONS if lo <= n <= hi), None)
        thinai = THINAI_BY_DIGIT[n % 10] if n else None
        poet, poet_note = clean_poet(c["poet"] if c else None)
        if n == 0:
            poet = poet and re.sub(r"^பாரதம் பாடிய\s*", "", poet)
        if c is None:
            flag("akananuru", rid, "colophon", "no colophon section in the commentary files")
        else:
            if n and c["thinai"] and c["thinai"] != thinai:
                flag("akananuru", rid, "thinai", f"commentary gives {c['thinai']!r}; the numbering "
                     f"rule gives {thinai!r} (rule value kept)")
            if not poet and c["poet"] is not None:
                flag("akananuru", rid, "colophon", "poet's name not preserved: the commentary edition "
                     f"prints dots ({c['poet']!r})")
                poet_note = "poet's name not preserved"
            elif not poet:
                flag("akananuru", rid, "colophon", "poet not found in the commentary colophon")
            if c["verse"]:
                sim = similarity(" ".join(tamil), " ".join(c["verse"]))
                if sim < 0.3:
                    flag("akananuru", rid, "alignment", f"commentary verse differs from the base "
                         f"text (letter-trigram similarity {sim:.2f})")
                if len(c["verse"]) != len(tamil) and not supplied:
                    flag("akananuru", rid, "line_count", f"base text has {len(tamil)} lines, the "
                         f"commentary edition ({c['source']}) has {len(c['verse'])}")
            else:
                flag("akananuru", rid, "colophon", "verse block not found in the commentary section")
        colophon_raw = None
        if c:
            colophon_raw = " | ".join(f"{k}: {c[k]}" for k in ("thinai", "thurai", "poet") if c[k])
        records.append({
            "id": rid, "number": n,
            "section": section[0] if section else None,
            "kind": "invocation" if n == 0 else "poem",
            "title": "கடவுள் வாழ்த்து" if n == 0 else None,
            "poet": poet, "patron": None,
            "thinai": thinai, "thurai": c["thurai"] if c else None,
            "note": poet_note,
            "colophon_raw": colophon_raw,
            "tamil": tamil, "line_count": len(tamil),
            "tamil_source": "pmuni0229",
            "lines_from_commentary_edition": supplied,
            "colophon_source": c["source"] if c else None,
            "rights": RIGHTS,
        })
    return records


# --------------------------------------------------------------------------------------------
# Pattupattu

def pattu_lines(text_dir, name):
    """Return (colophon dict, colophon_raw, verse lines, marks, sections) for one idyll."""
    lines = body(text_dir, name).split("\n")
    col, col_raw, sections = {}, [], []
    if name == "pmuni0488":  # UVS's Mullaippattu: the block after the title line
        i = next(i for i, l in enumerate(lines) if l.strip() == "முல்லைப்பாட்டு")
        verse_raw = []
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        while j < len(lines) and lines[j].strip():
            verse_raw.append(lines[j])
            j += 1
        closing = next((l for l in lines if "பாடிய முல்லைப்பாட்டி" in l), "")
        m = re.match(r"^(.*?)\s*பாடிய முல்லைப்பாட்டி", closing.strip())
        if m:
            col = {"poet": m.group(1).strip(), "thinai": "முல்லை"}
            col_raw = [m.group(0) + "..."]
    else:
        heads = [i for i, l in enumerate(lines) if "::" in l]
        for i in heads:
            label, value = [p.strip() for p in lines[i].split("::", 1)]
            col_raw.append(lines[i].strip())
            if label in PATTU_LABELS:
                col[PATTU_LABELS[label]] = value
        sep = heads[-1]  # the verse starts after the last colophon line (a rule line is skipped)
        end = next((i for i in range(sep, len(lines)) if "முற்றிற்று" in lines[i]
                    or lines[i].startswith(("This page", "This webpage"))), len(lines))
        verse_raw = lines[sep + 1:end]
    verse, marks = [], []
    for raw in verse_raw:
        s = raw.strip()
        if not s or re.fullmatch(r"-{3,}", s):
            continue
        m = re.match(r"^(\d)\.\s*(\S.*)$", s)
        if m and len(s) < 30:  # Thirumurugatruppadai's six abodes
            sections.append({"name": m.group(2).strip(), "start": len(verse) + 1})
            continue
        if re.fullmatch(r"\.?\s*[\u0B80-\u0BFF]+(?: [\u0B80-\u0BFF]+){0,2}\s*:", s) and \
                not re.search(r"\u0BC7\s*:$", s):
            continue  # a modern subheading such as 'முனிவர்:' or 'அருவி :'
        text, num = split_mark(s)
        text = tidy(text)
        if not text:
            continue
        verse.append(text)
        if num is not None:
            marks.append((len(verse), num))
    return col, col_raw, verse, marks, sections


def score_break(line):
    s = line.rstrip(" '\"’”)")
    if not s:
        return 0
    if s[-1] in ".!?;":
        return 3
    word = s.split()[-1].strip("-–,:;!?.'\"‘’“”")
    if re.search(r"[\u0B95-\u0BB9]\u0BC7$|[\u0B95-\u0BB9]\u0BCB$", word) and len(word) > 2:
        return 3
    if re.search(r"(?:^|[யவனரலளடற])(?:என|எனா|எனக்|என்று|என்ப)$|^(?:என|எனா|எனக்|என்று|என்ப)$", word) \
            or re.search(r"(?:யென|வென|னென|ரென|லென|ளென|டென|றென|யெனக்|வெனக்|னெனக்|ரெனக்|ளெனக்)$", word):
        return 2
    if s[-1] == ":":
        return 2
    if re.fullmatch(r"(?:பொருந|பாண|விறலி|இரவல|கூத்த|பெரும|குரிசில்|நெடுந்தகை|மகிழ்ந|தோழி|நெஞ்சே|அன்னாய்)", word):
        return 2  # a vocative closes the address that it ends
    if re.search(r"(?:அன்ன|போல|போலக்|ஆங்கு|அற்றே|கடுப்ப|ஏய்ப்ப|யன்ன|ன்னா|போலப்)$", word):
        return 1
    if s[-1] == "," or re.search(r"[\u0B95-\u0BB9]\u0BC1ம்$", word):
        return 1  # '-உம்' closes one member of a series of clauses
    return 0


def split_units(lines, start, end):
    """Units for lines[start:end] (0-based, end exclusive); returns (s, e) pairs, 0-based."""
    units, s = [], start
    while s < end:
        left = end - s
        if left <= 25:
            units.append((s, end))
            break
        best, best_e = None, None
        for length in range(10, 26):
            e = s + length
            if end - e < 10:
                continue
            v = 10 * score_break(lines[e - 1]) - abs(length - 16)
            if best is None or v > best:
                best, best_e = v, e
        units.append((s, best_e))
        s = best_e
    return units


# Single readings corrected from a second witness: (id, line, wrong, right, why).
TEXT_FIXES = (
    ("pattupattu:4:perumpanatruppadai", 467, "ந்நிலை யணுகல்", "யந்நிலை யணுகல்",
     "first letter lost in the 2021 e-text; the 2000 version of pmuni0069 on projectmadurai.org "
     "reads யந்நிலை"),
)


def text_fixes(rid, verse):
    for fid, n, wrong, right, why in TEXT_FIXES:
        if fid == rid:
            if verse[n - 1].startswith(wrong):
                flag("pattupattu", rid, "repaired", why, n, f"{verse[n - 1]} -> {right}{verse[n - 1][len(wrong):]}")
                verse[n - 1] = right + verse[n - 1][len(wrong):]
            else:
                flag("pattupattu", rid, "lineation", f"expected reading {wrong!r} not found on line {n}")
    return verse


# Pattinappalai 210: two short (kural) half-lines that both the Project Madurai text and
# U. V. Swaminatha Aiyar's edition (pmuni0479) print on two lines but number as one line, 210.
# They are joined so that the line numbers stay the standard ones (301 lines).
HALF_LINES = {"pattupattu:9:pattinappalai": ("கொள்வதூஉ மிகைகொளாது", "கொடுப்பதூஉங் குறைகொடாது")}


def join_half_lines(rid, verse, marks):
    pair = HALF_LINES.get(rid)
    if not pair:
        return verse, marks
    for i in range(len(verse) - 1):
        if verse[i] == pair[0] and verse[i + 1] == pair[1]:
            flag("pattupattu", rid, "repaired", f"joined the half-lines '{pair[0]}' and '{pair[1]}' "
                 "into line " + str(i + 1) + ", which both editions number as one line", i + 1)
            verse = verse[:i] + [pair[0] + " " + pair[1]] + verse[i + 2:]
            marks = [(pos - 1 if pos > i + 1 else pos, num) for pos, num in marks]
            return verse, marks
    flag("pattupattu", rid, "lineation", f"expected half-lines {pair} not found; nothing joined")
    return verse, marks


def build_pattupattu(text_dir):
    poems, units = [], []
    for n, name, short, title, standard in PATTU:
        rid = f"pattupattu:{n}:{short}"
        col, col_raw, verse, marks, sections = pattu_lines(text_dir, name)
        verse = [repair("pattupattu", rid, i, l) for i, l in enumerate(verse, 1)]
        verse, marks = join_half_lines(rid, verse, marks)
        verse = text_fixes(rid, verse)
        check_lines("pattupattu", rid, verse)
        check_marks("pattupattu", rid, marks)
        src_count = col.get("source_line_count")
        if len(verse) != standard:
            flag("pattupattu", rid, "line_count", f"{len(verse)} lines; the standard count is {standard}")
        if src_count and int(src_count) != len(verse):
            flag("pattupattu", rid, "line_count", f"the e-text's colophon says {src_count} lines; "
                 f"{len(verse)} parsed")
        if marks and marks[-1][0] != len(verse) and len(verse) != standard:
            flag("pattupattu", rid, "lineation", "last line carries no line count", len(verse))
        poems.append({
            "id": rid, "number": n, "short_name": short, "title": title,
            "poet": col.get("poet"), "patron": col.get("patron"),
            "thinai": col.get("thinai"), "thurai": col.get("thurai"), "metre": col.get("metre"),
            "line_count": len(verse), "standard_line_count": standard,
            "colophon_raw": " | ".join(col_raw) or None,
            "sections": sections or None,
            "tamil": verse, "tamil_source": name, "rights": RIGHTS,
        })
        bounds = [s["start"] - 1 for s in sections] or [0]
        if bounds[0] != 0:
            bounds.insert(0, 0)
        bounds.append(len(verse))
        for k in range(len(bounds) - 1):
            sec_name = next((s["name"] for s in sections if s["start"] - 1 == bounds[k]), None)
            for s, e in split_units(verse, bounds[k], bounds[k + 1]):
                units.append({
                    "id": f"pattupattu:{n}:{s + 1}-{e}", "poem_id": rid, "number": n,
                    "short_name": short, "start": s + 1, "end": e, "line_count": e - s,
                    "section": sec_name, "break_score": score_break(verse[e - 1]),
                    "tamil": verse[s:e], "rights": RIGHTS,
                })
    return poems, units


# --------------------------------------------------------------------------------------------
# Purananuru (read-only check of kg/core/purananuru.jsonl)

def check_purananuru(text_dir, path):
    recs = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines()]
    nums = [r["number"] for r in recs]
    expected = [n for n in range(1, 401) if n not in (267, 268)]
    report = {"records": len(recs), "numbers_in_order": nums == expected,
              "ids_match": all(r["id"] == f"purananuru:{r['number']}" for r in recs),
              "lines": sum(len(r["tamil"]) for r in recs)}
    src = body(text_dir, "pmuni0057").replace("·", "ஃ")
    src_norm = NON_TAMIL.sub("", src)
    # Lines changed by scripts/repair_purananuru.py are logged in purananuru_repairs.jsonl, so
    # they are not reported as missing from pmuni0057; the readings it keeps are flagged.
    repairs_path = path.with_name("purananuru_repairs.jsonl")
    repairs = ([json.loads(l) for l in repairs_path.read_text(encoding="utf-8").splitlines()]
               if repairs_path.exists() else [])
    repaired = set()
    for x in repairs:
        if x["action"] == "changed" and x["field"] == "tamil":
            for l in (x["new"] if isinstance(x["new"], list) else [x["new"]]):
                repaired.add((x["poem"], l))
    not_in_source, unicode_bad, empty = [], [], []
    for r in recs:
        rid = r["id"]
        if not r["tamil"]:
            empty.append(rid)
            flag("purananuru", rid, "empty_poem", "no verse lines")
        for i, l in enumerate(r["tamil"], 1):
            for p in unicode_problems(l):
                unicode_bad.append(rid)
                flag("purananuru", rid, "unicode", p, i, l)
            if re.search(r"(?:^|[\s'‘“(])[\u0B95-\u0BB9]\u0BCD", l):
                flag("purananuru", rid, "spelling", "a word begins with a dead consonant (stray space "
                     "or lost letter)", i, l)
            k = NON_TAMIL.sub("", l)
            if r.get("tamil_source") == "pmuni0057" and k and k not in src_norm \
                    and (rid, l) not in repaired:
                not_in_source.append((rid, i))
                flag("purananuru", rid, "not_in_source", "line not found in pmuni0057", i, l)
        for i in range(1, len(r["tamil"])):
            if r["tamil"][i] == r["tamil"][i - 1]:
                flag("purananuru", rid, "duplicate_line", "same line printed twice in a row", i + 1)
        d = r.get("duraisamy_pillai") or {}
        if d.get("tamil") and abs(len(d["tamil"]) - len(r["tamil"])) > 1:
            flag("purananuru", rid, "line_count", f"{len(r['tamil'])} lines; Duraisamy Pillai's "
                 f"edition has {len(d['tamil'])}")
    cross_duplicates("purananuru", recs)
    for x in repairs:
        if x["action"] == "kept":
            readings = "; ".join(f"{k}: {v}" for k, v in (x.get("readings") or {}).items())
            flag("purananuru", x["poem"], x["kind"], f"our reading kept ({x['field']}); "
                 + readings + (f" ({x['note']})" if x.get("note") else "") + f" [{x['id']}]",
                 x.get("line"), x["old"] if x["field"] == "tamil" else None)
    report.update(not_in_source=len(not_in_source), unicode_problem_poems=len(set(unicode_bad)),
                  empty=empty, repairs_changed=sum(1 for x in repairs if x["action"] == "changed"),
                  repairs_kept=sum(1 for x in repairs if x["action"] == "kept"))
    return report


def cross_duplicates(book, records, key="tamil"):
    """A line (of 12+ letters) printed in two different poems: often a real shared formula, but
    also how displaced lines show up (Purananuru 64/326)."""
    seen = defaultdict(list)
    for r in records:
        for i, l in enumerate(r[key], 1):
            k = NON_TAMIL.sub("", l)
            if len(k) >= 12:
                seen[k].append((r["id"], i, l))
    for k, places in seen.items():
        ids = {p[0] for p in places}
        if len(ids) > 1:
            flag(book, places[0][0], "repeated_line", "the same line appears in "
                 + ", ".join(f"{p[0]} line {p[1]}" for p in places), places[0][1], places[0][2])


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as out:
        for r in records:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text-dir", type=Path, default=ROOT / "data" / "text")
    ap.add_argument("--out-dir", type=Path, default=ROOT / "kg" / "core")
    ap.add_argument("--skip-purananuru", action="store_true")
    args = ap.parse_args()

    akam = build_akananuru(args.text_dir)
    cross_duplicates("akananuru", akam)
    poems, units = build_pattupattu(args.text_dir)
    cross_duplicates("pattupattu", poems)
    pur = None
    if not args.skip_purananuru:
        pur = check_purananuru(args.text_dir, ROOT / "kg" / "core" / "purananuru.jsonl")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.out_dir / "akananuru.jsonl", akam)
    write_jsonl(args.out_dir / "pattupattu.jsonl", poems)
    write_jsonl(args.out_dir / "pattupattu_units.jsonl", units)
    write_jsonl(args.out_dir / "sangam_text_flags.jsonl", flags)

    numbered = [r for r in akam if r["number"] > 0]
    print(f"akananuru: {len(numbered)} poems + invocation, {sum(r['line_count'] for r in akam)} lines; "
          f"poet {sum(1 for r in akam if r['poet'])}, thurai {sum(1 for r in akam if r['thurai'])}")
    print("  sections:", dict(Counter(r["section"] for r in numbered)))
    print("  thinai:", dict(Counter(r["thinai"] for r in numbered)))
    for p in poems:
        mark = "ok" if p["line_count"] == p["standard_line_count"] else "DIFFERS"
        print(f"pattupattu {p['number']:>2} {p['short_name']:<22} {p['line_count']:>4} lines "
              f"(standard {p['standard_line_count']}) {mark}")
    lengths = Counter(u["line_count"] for u in units)
    print(f"units: {len(units)}, lengths {min(lengths)}-{max(lengths)}, "
          f"break scores {dict(Counter(u['break_score'] for u in units))}")
    if pur:
        print("purananuru:", pur)
    print("flags:", dict(Counter((f["book"], f["kind"]) for f in flags)))


if __name__ == "__main__":
    main()
