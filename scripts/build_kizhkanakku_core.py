#!/usr/bin/env python3
"""Build the original Tamil text of sixteen works of the Pathinenkilkanakku.

The Kural and the Naladiyar are already in kg/core/ (parse_kural.py, parse_naladiyar.py). This
script adds the other sixteen, one file per work, one record per verse:

  kg/core/<book>.jsonl              see BOOKS below for the sixteen keys
  kg/core/sangam_text_flags.jsonl   this script's flags are appended, each tagged with its book;
                                    flags of other books already in the file are kept as they are

Base text: the Project Madurai e-texts mirrored in data/text/ (read as build_sangam_core.py does):
  pmuni0024  Acharakkovai                 pmuni0036  Pazhamozhi Nanuru
  pmuni0025  Innaa Narpathu, Iniyavai      pmuni0047  Nanmanikkadigai
             Narpathu, Kalavazhi Narpathu, pmuni0048  Thirikadugam
             Muthumozhikkanchi             pmuni0051  Kainnilai (Innilai, in the same file, is
  pmuni0027  Ainthinai Aimpathu, Ainthinai            not one of the eighteen and is skipped)
             Ezhupathu, Thinaimozhi Aimpathu pmuni0056 Thinaimalai Nurraimpathu
  pmuni0029  Kar Narpathu, Elathi, Sirupanchamoolam

Cross-checks (optional; each is skipped with a note if its folder is not given or absent):
  --site-dir   the sangamtamil.com cache (its data/texts/<id>.js). The site's texts are built from
               the same Project Madurai files, so a difference is either a parse slip on one side
               or a change between Project Madurai revisions. Only the Tamil verse lines are read;
               the site's English and prose are never read or copied.
  --tvu-dir    tamilvu.org verse pages saved as <library>-<subid>.html (l2200 Thirikadugam, l2300
               Muthumozhikkanchi, l2400 Innaa, l2500 Iniyavai, l2600 Kalavazhi, l2700 Kar,
               l2900 Nanmanikkadigai). Used only to arbitrate numbering and verse boundaries, and
               to say which side a reading difference agrees with. The tamilvu text is word-split
               (பிரித்த பாடம்), so it is compared letter-for-letter with spaces and punctuation removed.

Record fields: id (<book>:N), book, number (N; 0 for an invocation), kind (invocation, payiram,
verse), source_number (the number Project Madurai prints, where it differs from N or is absent),
section (a work's own division: the thinai of the akam works, the ten tens of Muthumozhikkanchi),
chapter and chapter_no (Pazhamozhi's 34 headings), thinai (akam works only), thurai (Kar Narpathu
only; the old commentary's situation label, with இதுவுமது resolved), author, tamil (lines),
line_count, tamil_source, rights. A payiram (preface verse, not by the author) is kept as
<book>:payiram with number null.

Copyright: only the verse lines and plain facts (author, section, thinai, the old thurai labels)
are kept. Project Madurai's modern headings for each verse (Acharakkovai, Thirikadugam), its metre
labels, editorial notes and dates, and every commentary and translation are left out.

Run: python3 -I scripts/build_kizhkanakku_core.py [--text-dir DIR] [--out-dir DIR]
                                                  [--site-dir DIR] [--tvu-dir DIR]
"""
import argparse
import html
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
RIGHTS = {"tamil": "public_domain"}
THINAI = ("குறிஞ்சி", "முல்லை", "மருதம்", "பாலை", "நெய்தல்")
VARIANT_MARK = re.compile(r"[@%&]")

# key, Tamil title, source file, start line, end line, author, standard count of numbered verses
BOOKS = (
    ("nanmanikkadigai", "நான்மணிக்கடிகை", "pmuni0047", r"^### விளம்பிநாகனாரின்",
     r"^நான்மணிக்கடிகை முற்றிற்று", "விளம்பிநாகனார்", 104),
    ("innaa_narpathu", "இன்னா நாற்பது", "pmuni0025", r"^1\. இன்னா நாற்பது",
     r"^இன்னா நாற்பது முற்றிற்று", "கபிலர்", 40),
    ("iniyavai_narpathu", "இனியவை நாற்பது", "pmuni0025", r"^2\. இனியவை நாற்பது",
     r"^இனியவை நாற்பது முற்றிற்று", "பூதஞ்சேந்தனார்", 40),
    ("kar_narpathu", "கார் நாற்பது", "pmuni0029", r"^1\. கார் மதுரைக்",
     r"^கார் நாற்பது முற்றிற்று", "மதுரைக் கண்ணங்கூத்தனார்", 40),
    ("kalavazhi_narpathu", "களவழி நாற்பது", "pmuni0025", r"^3\. களவழி நாற்பது",
     r"^களவழி நாற்பது முற்றிற்று", "பொய்கையார்", 41),
    ("ainthinai_aimpathu", "ஐந்திணை ஐம்பது", "pmuni0027", r"^1\. மாறன் பொறையனார் அருளிய",
     r"^ஐந்திணை ஐம்பது முற்றிற்று", "மாறன் பொறையனார்", 50),
    ("thinaimozhi_aimpathu", "திணைமொழி ஐம்பது", "pmuni0027", r"^### கண்ணன் சேந்தனார்",
     r"^திணை மொழி ஐம்பது முற்றிற்று", "கண்ணன் சேந்தனார்", 50),
    ("ainthinai_ezhupathu", "ஐந்திணை எழுபது", "pmuni0027", r"^### 2\. மூவாதியார்",
     r"^ஐந்திணை எழுபது முற்றிற்று", "மூவாதியார்", 70),
    ("thinaimalai_nootraimpathu", "திணைமாலை நூற்றைம்பது", "pmuni0056", r"^### திணைமாலை",
     r"^திணைமாலை நூற்றைம்பது முற்றிற்று", "கணிமேதாவியார்", 153),
    ("thirikadugam", "திரிகடுகம்", "pmuni0048", r"^### நல்லாதனாரின்",
     r"^திரிகடுகம் முற்றிற்று", "நல்லாதனார்", 100),
    ("acharakkovai", "ஆசாரக்கோவை", "pmuni0024", r"^### பெருவாயின்",
     r"^ஆசாரக் கோவை முற்றிற்று", "பெருவாயின் முள்ளியார்", 100),
    ("pazhamozhi_nanooru", "பழமொழி நானூறு", "pmuni0036", r"^### பழமொழி நானூறு - ",
     r"^பழமொழி நானூறு முற்றிற்று", "முன்றுறை அரையனார்", 400),
    ("sirupanchamoolam", "சிறுபஞ்சமூலம்", "pmuni0029", r"^### 3\. காரியாசான்",
     r"^சிறுபஞ்சமூலம் முற்றிற்று", "காரியாசான்", 96),
    ("muthumozhikkanchi", "முதுமொழிக்காஞ்சி", "pmuni0025", r"^4\. முதுமொழிக் காஞ்சி",
     r"^முதுமொழிக்காஞ்சி முற்றிற்று", "மதுரைக் கூடலூர் கிழார்", 100),
    ("elathi", "ஏலாதி", "pmuni0029", r"^### 2\. கணிமேதையார்",
     r"^ஏலாதி முற்றிற்று", "கணிமேதையார்", 80),
    ("kainnilai", "கைந்நிலை", "pmuni0051", r"^### 2\. புல்லங்காடனாரின்",
     r"^கைந்நிலை முற்றிற்று", "புல்லங்காடனார்", 60),
)
AKAM = {"kar_narpathu", "ainthinai_aimpathu", "thinaimozhi_aimpathu", "ainthinai_ezhupathu",
        "thinaimalai_nootraimpathu", "kainnilai"}
# Thinai of each akam work by verse number, from the work's own arrangement (Kar Narpathu is a
# mullai work throughout; the others run in five blocks, in the order of the source's headings).
THINAI_BLOCKS = {
    "ainthinai_aimpathu": ((1, 10, "முல்லை"), (11, 20, "குறிஞ்சி"), (21, 30, "மருதம்"),
                           (31, 40, "பாலை"), (41, 50, "நெய்தல்")),
    "thinaimozhi_aimpathu": ((1, 10, "குறிஞ்சி"), (11, 20, "பாலை"), (21, 30, "முல்லை"),
                             (31, 40, "மருதம்"), (41, 50, "நெய்தல்")),
    "ainthinai_ezhupathu": ((1, 14, "குறிஞ்சி"), (15, 28, "முல்லை"), (29, 42, "பாலை"),
                            (43, 56, "மருதம்"), (57, 70, "நெய்தல்")),
    "kainnilai": ((1, 12, "குறிஞ்சி"), (13, 24, "பாலை"), (25, 36, "முல்லை"),
                  (37, 48, "மருதம்"), (49, 60, "நெய்தல்")),
    "kar_narpathu": ((1, 40, "முல்லை"),),
}
# The source numbers some invocations and prefaces as verses; source number -> our number.
# Nanmanikkadigai: tamilvu (l2900) and the standard count give two invocation verses (Project
# Madurai 1 and 2) and 104 verses (Project Madurai 3-106). Sirupanchamoolam: Project Madurai
# numbers the invocation 1 and the preface 98, so its verses 2-97 are 1-96 here.
RENUMBER = {"nanmanikkadigai": -2, "sirupanchamoolam": -1}

SITE_IDS = {
    "nanmanikkadigai": "nanmanikkadigai", "innaa_narpathu": "innaa-narpathu",
    "iniyavai_narpathu": "iniyavai-narpathu", "kar_narpathu": "kar-narpathu",
    "kalavazhi_narpathu": "kalavali-narpathu", "ainthinai_aimpathu": "ainthinai-aimpathu",
    "thinaimozhi_aimpathu": "thinaimozhi-aimpathu", "ainthinai_ezhupathu": "ainthinai-ezhupathu",
    "thinaimalai_nootraimpathu": "thinaimalai-nurraimpathu", "thirikadugam": "thirikadugam",
    "acharakkovai": "acharakkovai", "pazhamozhi_nanooru": "palamoli-nanuru",
    "sirupanchamoolam": "sirupanchamoolam", "muthumozhikkanchi": "muthumozhikkanchi",
    "elathi": "elathi", "kainnilai": "kainnilai",
}
TVU_LIBS = {"thirikadugam": "2200", "muthumozhikkanchi": "2300", "innaa_narpathu": "2400",
            "iniyavai_narpathu": "2500", "kalavazhi_narpathu": "2600", "kar_narpathu": "2700",
            "nanmanikkadigai": "2900"}

# Character repairs made in the verse lines; each one is flagged.
REPAIRS = (
    (re.compile(r"·"), "ஃ", "'·' is the old encoding of ஃ"),
    (re.compile(r"[\u200B-\u200D\uFEFF]"), "", "zero-width character removed"),
    (re.compile(r"(?<=[\u0B80-\u0BFF]) (?=[\u0B95-\u0BB9]\u0BCD)"), "",
     "stray space before a dead consonant removed (e.g. நட்டோ ன் = நட்டோன்)"),
    (re.compile(r"\|"), "", "stray '|' removed"),
    (re.compile(r"(?<=[\u0B95-\u0BB9])\u0BC6\u0BB3(?=\u0BB5)"), "\u0BCC",
     "ௌ written as ெ + ள (பெளவம் = பௌவம், வெளவான் = வௌவான்)"),
)

# Single-letter misprints in the base text, each read so by tamilvu (the only arbiter for these
# works) and each a non-word or a slip in the source: (book, number, line, source, repaired).
# Other differences from tamilvu, where both readings are words, are flagged and not changed.
TVU_REPAIRS = (
    ("thirikadugam", 1, 2, "தெடார்ச்சியும்", "தொடர்ச்சியும்"),
    ("thirikadugam", 96, 3, "சொய்வான்", "செய்வான்"),
    ("kar_narpathu", 4, 4, "வாடம பசலை", "வாடும் பசலை"),
    ("nanmanikkadigai", 6, 2, "பிறானக்", "பிறனைக்"),
    ("nanmanikkadigai", 14, 1, "கிளைக்குழம்", "கிளைக்குழாம்"),
    ("iniyavai_narpathu", 5, 3, "யார்மட்டும்", "யார்மாட்டும்"),
    ("iniyavai_narpathu", 34, 2, "சோர்வின்றச்", "சோர்வின்றிச்"),
    ("muthumozhikkanchi", 61, 2, "பேரறவி னோன்இனிது", "பேரறிவி னோன்இனிது"),
    ("kalavazhi_narpathu", 37, 2, "முத்தடைக்", "முத்துடைக்"),
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


def book_lines(text_dir, name, start, end):
    lines = body(text_dir, name).split("\n")
    s = next(i for i, l in enumerate(lines) if re.search(start, l.strip()))
    e = next(i for i in range(s + 1, len(lines)) if re.search(end, lines[i].strip()))
    return lines[s + 1:e]


def blocks(lines):
    """Split on blank lines, and also before a heading that the source runs into a verse."""
    out, cur = [], []
    for l in lines:
        l = l.replace("\u00a0", " ").rstrip()
        if re.fullmatch(r"\s*-+\s*", l):
            continue  # a rule printed under a section's last verse
        if cur and (THINAI_HEAD.match(l.strip()) or INVOCATION.match(l.strip())
                    or PAYIRAM.match(l.strip()) or LEAD_NUM.match(l.strip())):
            out.append(cur)
            cur = []
        if l.strip():
            cur.append(l.strip())
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


TRAIL_NUM = re.compile(r"[\s.]*(?:\(\s*(\d{1,3})\s*\)|(\d{1,3}))\s*\.?\s*$")


def trailing_number(line):
    """'... வினை. 5' / '... ஆய். 50.' / '... ஈண்டு. (1)' -> (text, 5). No number -> (line, None)."""
    m = TRAIL_NUM.search(line)
    if not m or not TAMIL_CHAR.search(line[:m.start()]):
        return line, None
    return line[:m.start()], int(m.group(1) or m.group(2))


def tidy(line):
    line = re.sub(r"\s+", " ", line).strip()
    line = re.sub(r"\s+([,.;:!?])", r"\1", line)
    return line.strip()


def unicode_problems(line):
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
            flag(book, rid, "lacuna", "line has no Tamil letters (a gap in the manuscripts)", i, l)
        elif re.search(r"\.{3,}|(?:\. ){2,}", l):
            flag(book, rid, "lacuna", "line is partly lost (dots in the source)", i, l)
        if re.search(r"(?:^|[\s'\u2018\u201c\-])[\u0B95-\u0BB9]\u0BCD", l):
            flag(book, rid, "lost_vowel_sign", "a word begins with a dead consonant "
                 "(a letter or vowel sign lost?)", i, l)
        if re.search(r"(?:^|\s)[\u0BBE-\u0BCD]", l):
            flag(book, rid, "lost_vowel_sign", "a vowel sign stands after a space", i, l)
    for i in range(1, len(lines)):
        if lines[i] == lines[i - 1] and TAMIL_CHAR.search(lines[i]):
            flag(book, rid, "duplicate_line", "same line printed twice in a row", i + 1, lines[i])


# --------------------------------------------------------------------------------------------
# Parsing. Each work is read block by block (blocks are separated by blank lines). Heading lines
# at the top of a block change the state (invocation, preface, section, thinai, chapter, a
# leading verse number); the remaining lines are the verse. Variant readings (lines starting
# with @ % &, keyed to the same marks inside the verse) are flagged, not stored in the verse.

SKIP_LINE = re.compile(r"^(?:நூல்|ஆசிரியர்.*|பதினெண் கீழ்க்கணக்கு.*|\(.*\)\.?|இடம்\s*[-:].*|நிலம்\s*[-:].*|ஒழுக்கம்.*|-+|காலம்.*)$")
INVOCATION = re.compile(r"^(?:கடவுள் வாழ்த்து|கடவுள் வணக்கம்|காப்பு)$")
PAYIRAM = re.compile(r"^(?:சிறப்புப் |தற்சிறப்புப் )?பாயிரம்$")
LOST = re.compile(r"^(\d+)\s*,\s*(\d+)\s*-?\s*இரண்டு பாடல்")
THINAI_HEAD = re.compile(r"^(?:(\d+)\s*[.,]\s*)?(" + "|".join(THINAI) + r")$")
LEAD_NUM = re.compile(r"^(\d{1,3})\s*\.?$")
LEAD_BOOKS = ("kainnilai", "pazhamozhi_nanooru", "acharakkovai", "thirikadugam")
LEAD_HEAD = re.compile(r"^(\d{1,3})\s*[.,]*\s+(\S.*)$")


class Verse:
    def __init__(self):
        self.lines, self.variants, self.number, self.kind = [], [], None, "verse"
        self.section = self.thinai = self.chapter = self.chapter_no = self.thurai = None
        self.src_line = None


def parse_book(key, lines):
    """Return (verses, lost numbers, notes)."""
    out, lost = [], []
    state = {"section": None, "thinai": None, "chapter": None, "chapter_no": None,
             "thurai": None, "pending": None}
    for blk in blocks(lines):
        v = Verse()
        heads = []
        lead = None
        body_lines = []
        if key == "acharakkovai":
            # the modern heading can run over two lines; the metre label ends it
            m = next((i for i, x in enumerate(blk) if re.match(r"^\(.*வெண்பா\s*\)$", x)), None)
            if m is not None and LEAD_HEAD.match(blk[0]):
                blk = [blk[0]] + blk[m + 1:]
        for l in blk:
            if body_lines:
                if VARIANT_MARK.match(l):
                    v.variants.append(l)
                elif key == "kainnilai" and l.startswith("("):
                    pass  # Project Madurai's modern thurai note under some verses: not kept
                else:
                    body_lines.append(l)
                continue
            if INVOCATION.match(l):
                state["pending"] = "invocation"
            elif PAYIRAM.match(l):
                state["pending"] = "payiram"
            elif LOST.match(l):
                m = LOST.match(l)
                lost.extend([int(m.group(1)), int(m.group(2))])
            elif re.match(r"^(\d+)\s*,\s*(\d+)\s+இரண்டு பாடல்களும் மறைந்தன", l):
                m = re.match(r"^(\d+)\s*,\s*(\d+)", l)
                lost.extend([int(m.group(1)), int(m.group(2))])
            elif THINAI_HEAD.match(l) and key != "pazhamozhi_nanooru":
                t = THINAI_HEAD.match(l).group(2)
                heads.append(("thinai", t))
            elif key == "muthumozhikkanchi" and re.match(r"^\d+\.\s*\S+\s*பத்து$", l):
                m = re.match(r"^(\d+)\.\s*(.+)$", l)
                state["section"] = m.group(2).replace("அறிவுப்பத்து", "அறிவுப் பத்து")
                state["chapter_no"] = int(m.group(1))
            elif LEAD_NUM.match(l) and key in LEAD_BOOKS:
                lead = int(LEAD_NUM.match(l).group(1))
            elif LEAD_HEAD.match(l) and key == "pazhamozhi_nanooru":
                m = LEAD_HEAD.match(l)
                state["chapter_no"], state["chapter"] = int(m.group(1)), m.group(2).strip()
            elif re.match(r"^(\d+)\.(\S.*)$", l) and key == "pazhamozhi_nanooru":
                m = re.match(r"^(\d+)\.(\S.*)$", l)
                state["chapter_no"], state["chapter"] = int(m.group(1)), m.group(2).strip()
            elif LEAD_HEAD.match(l) and key in ("acharakkovai", "thirikadugam"):
                lead = int(LEAD_HEAD.match(l).group(1))  # the modern heading is not kept
            elif SKIP_LINE.match(l) or l.startswith("###"):
                pass
            elif key == "kar_narpathu" and not body_lines and _is_thurai(blk, l):
                heads.append(("thurai", l))
            elif VARIANT_MARK.match(l):
                if out:
                    out[-1].variants.append(l)
            else:
                body_lines.append(l)
        for kind, val in heads:
            if kind == "thinai":
                if key in ("kainnilai",) and val == "பாலை" and state["thinai"] == "மருதம்":
                    flag(key, f"{key}:49", "thinai", "the source heads verses 49-60 'பாலை'; "
                         "the work's order (and the verses' shore scenes) make them நெய்தல்")
                    val = "நெய்தல்"
                state["thinai"] = state["section"] = val
            elif kind == "thurai":
                state["thurai"] = val if not state["thurai"] or not val.startswith("இதுவுமது") \
                    else state["thurai"]
        if key == "kar_narpathu":
            th = [h[1] for h in heads if h[0] == "thurai"]
            if th:
                text = " ".join(th)
                if text != "இதுவுமது":
                    state["thurai"] = text
        if not body_lines:
            continue
        if key == "muthumozhikkanchi":
            out.extend(_muthumozhi(body_lines, state))
            continue
        last, num = trailing_number(body_lines[-1])
        if (key in LEAD_BOOKS and lead is None and num is None and not state["pending"]
                and out and out[-1].kind == "verse" and out[-1].number is not None
                and len(out[-1].lines) < 3):
            # a blank line inside a verse: the lines belong to the verse above
            flag(key, f"{key}:{out[-1].number}", "lineation", "blank line inside the verse in "
                 "the source; the lines after it are kept with the verse",
                 len(out[-1].lines) + 1, body_lines[0])
            out[-1].lines.extend(body_lines)
            continue
        if lead is not None:
            if num is not None:
                if num != lead % 10 and num != lead:
                    flag(key, f"{key}:{lead}", "numbering", f"stray number {num} after the verse "
                         f"numbered {lead}", len(body_lines), body_lines[-1])
                body_lines[-1] = last
            num = lead
        elif num is not None:
            body_lines[-1] = last
        v.lines = body_lines
        v.number = num
        if state["pending"]:
            v.kind = state["pending"]
            state["pending"] = None
        v.section, v.thinai = state["section"], state["thinai"]
        v.chapter, v.chapter_no = state["chapter"], state["chapter_no"]
        v.thurai = state["thurai"] if key == "kar_narpathu" else None
        out.append(v)
    return out, lost


def _is_thurai(blk, l):
    """Kar Narpathu: the lines above the four verse lines are the old thurai label."""
    verse = [x for x in blk if not VARIANT_MARK.match(x)]
    if len(verse) < 4 and trailing_number(verse[-1])[1] is None:
        return True  # a label standing alone above the next block
    return len(verse) > 4 and verse.index(l) < len(verse) - 4


def _muthumozhi(body_lines, state):
    out = []
    for l in body_lines:
        m = re.match(r"^(\d+)\.\s*(.+)$", l)
        if m:
            v = Verse()
            v.number = int(m.group(1))
            v.lines = [m.group(2)]
            v.section, v.chapter_no = state["section"], state["chapter_no"]
            out.append(v)
        elif out:
            out[-1].lines.append(l)
    return out


def clean_line(key, rid, i, line, variants_out):
    marks = VARIANT_MARK.findall(line)
    if marks:
        variants_out.append((i, "".join(marks)))
        line = VARIANT_MARK.sub("", line)
    line = tidy(line)
    for pat, rep, why in REPAIRS:
        new = tidy(pat.sub(rep, line))
        if new != line:
            flag(key, rid, "repaired", why, i, f"{line} -> {new}")
            line = new
    return line


def fix_kalavazhi_32(tamil, key, rid):
    """Kalavazhi 32: the source prints '[தீர்ந்த' at the end of line 1; it ends line 2
    ('... செவ்வந்தாள் - பொய்தீர்ந்த'), as in tamilvu."""
    if len(tamil) > 1 and tamil[0].endswith("[தீர்ந்த"):
        old = list(tamil)
        tamil[0] = tamil[0][: -len("[தீர்ந்த")].rstrip()
        tamil[1] = tamil[1].rstrip() + "தீர்ந்த"
        flag(key, rid, "repaired", "word printed at the end of the line above, marked '[', "
             "moved to the end of line 2 (tamilvu: 'பொய் தீர்ந்த')", 1,
             f"{' / '.join(old[:2])} -> {' / '.join(tamil[:2])}")
    return tamil


def build_book(text_dir, spec):
    key, title, src, start, end, author, standard = spec
    verses, lost = parse_book(key, book_lines(text_dir, src, start, end))
    records = []
    prev = 0
    inv_count = 0
    shift = RENUMBER.get(key, 0)
    for v in verses:
        src_no = v.number
        if v.kind == "invocation" or (key == "nanmanikkadigai" and src_no in (1, 2)):
            inv_count += 1
            n = 0
            rid = f"{key}:0" if inv_count == 1 else f"{key}:0b"
            kind = "invocation"
        elif v.kind == "payiram" or (key == "sirupanchamoolam" and src_no == 98):
            n, rid, kind = None, f"{key}:payiram", "payiram"
        else:
            kind = "verse"
            if src_no is None:
                n = prev + 1
                flag(key, f"{key}:{n}", "numbering", f"verse printed without a number; numbered "
                     f"{n} by its place after {prev}")
            else:
                n = src_no + shift
                if n <= prev and (prev + 1) % 100 == n:
                    flag(key, f"{key}:{prev + 1}", "numbering", f"printed number {src_no} is a "
                         f"misprint for {prev + 1 - shift}")
                    src_no, n = prev + 1 - shift, prev + 1
            if n != prev + 1:
                miss = [x for x in range(prev + 1, n) if x not in lost]
                if miss:
                    flag(key, f"{key}:{n}", "gap", f"numbering jumps from {prev} to {n}: "
                         f"{', '.join(map(str, miss))} missing in the source")
            prev = n
            rid = f"{key}:{n}"
        var_marks = []
        tamil = [clean_line(key, rid, i, l, var_marks) for i, l in enumerate(v.lines, 1)]
        tamil = [l for l in tamil if l]
        if tamil and tamil[-1].endswith("."):
            tamil[-1] = tamil[-1][:-1].rstrip()  # the source's full stop after some verses only
        if key == "kalavazhi_narpathu" and n == 32:
            tamil = fix_kalavazhi_32(tamil, key, rid)
        for bk, num, li, old, new in TVU_REPAIRS:
            if bk == key and num == n and kind == "verse":
                if old in tamil[li - 1]:
                    before = tamil[li - 1]
                    tamil[li - 1] = before.replace(old, new)
                    flag(key, rid, "repaired", f"misprint {old} read {new}, as tamilvu", li,
                         f"{before} -> {tamil[li - 1]}")
                else:
                    flag(key, rid, "repair_not_applied", f"expected {old} in line {li}", li)
        if v.variants or var_marks:
            flag(key, rid, "source_variant", "Project Madurai prints variant readings, keyed by "
                 "@ % & in the verse: " + " | ".join(v.variants),
                 var_marks[0][0] if var_marks else None,
                 " / ".join(f"line {i}: {m}" for i, m in var_marks))
        thinai = None
        if key in AKAM and kind == "verse":
            blocks_ = THINAI_BLOCKS.get(key)
            if blocks_:
                thinai = next((t for a, b, t in blocks_ if a <= n <= b), None)
                if v.thinai and v.thinai != thinai and key != "kar_narpathu":
                    flag(key, rid, "thinai", f"source heading {v.thinai}, arrangement {thinai}")
            else:
                thinai = v.thinai
        rec = {
            "id": rid, "book": key, "number": n, "kind": kind,
        }
        if src_no is not None and (src_no != n or kind != "verse"):
            rec["source_number"] = src_no
        if kind == "invocation" and key == "nanmanikkadigai":
            rec["invocation_part"] = inv_count
        rec["title"] = title
        if key == "muthumozhikkanchi" and kind == "verse":
            rec["section"], rec["section_no"] = v.section, v.chapter_no
        elif key in AKAM and kind == "verse":
            rec["section"] = thinai
        if key == "pazhamozhi_nanooru" and kind == "verse":
            rec["chapter_no"], rec["chapter"] = v.chapter_no, v.chapter
        if key in AKAM:
            rec["thinai"] = thinai
        if key == "kar_narpathu" and kind == "verse":
            rec["thurai"] = v.thurai
        rec["author"] = None if kind == "payiram" else author
        rec["tamil"] = tamil
        rec["line_count"] = len(tamil)
        rec["tamil_source"] = src
        rec["rights"] = RIGHTS
        check_lines(key, rid, tamil)
        records.append(rec)
    for n in lost:
        flag(key, f"{key}:{n}", "lost", "the source says this verse is lost in the tradition")
    return records, lost


def cross_duplicates(key, records):
    seen = defaultdict(list)
    for r in records:
        for i, l in enumerate(r["tamil"], 1):
            k = NON_TAMIL.sub("", l)
            if len(k) >= 14:
                seen[k].append((r["id"], i, l))
    for k, places in seen.items():
        ids = {p[0] for p in places}
        if len(ids) > 1:
            flag(key, places[0][0], "repeated_line", "the same line appears in "
                 + ", ".join(f"{p[0]} line {p[1]}" for p in places), places[0][1], places[0][2])


# --------------------------------------------------------------------------------------------
# Cross-checks

def letters(s):
    return NON_TAMIL.sub("", s)


def load_site(site_dir, site_id):
    path = site_dir / "data" / "texts" / f"{site_id}.js"
    if not path.exists():
        return None
    t = path.read_text(encoding="utf-8")
    d = json.JSONDecoder().raw_decode(t[t.index("=") + 1:].lstrip())[0]
    out = []
    for v in d.get("verses", []):
        lines = [l for l in str(v.get("text", "")).split("\n") if l.strip()]
        out.append({"n": v.get("n"), "lines": lines})
    return out


def load_tvu(tvu_dir, lib):
    """Return [(number, lines)] in page order; an unnumbered verse cell (an invocation) has 0."""
    out = []
    cell = re.compile(r"<td[^>]*class=['\"]?(pno|poem)['\"]?[^>]*>((?:(?!<td|</td>).)*)</td>", re.S)
    pages = sorted(tvu_dir.glob(f"{lib}-*.html"), key=lambda p: int(p.stem.split("-")[1]))
    for page_no, p in enumerate(pages):
        b = p.read_bytes().decode("utf-8", "replace")
        num = None
        for m in cell.finditer(b):
            kind, inner = m.group(1), m.group(2)
            if kind == "pno":
                d = re.search(r"(\d+)", re.sub(r"<[^>]+>", "", inner))
                if d and "song_no" not in inner:
                    num = int(d.group(1))
                continue
            t = re.sub(r"<center>.*?</center>", "", inner, flags=re.S)
            t = re.sub(r"<font color='006600'>.*?</font>", "", t, flags=re.S)
            t = re.sub(r"<br\s*/?>", "\n", t)
            t = html.unescape(re.sub(r"<[^>]+>", "", t))
            lines = [l.strip() for l in t.split("\n") if TAMIL_CHAR.search(l)]
            while lines and (" " not in lines[0] or lines[0].startswith("(")
                             or lines[0] == "கடவுள் வாழ்த்து"):
                lines.pop(0)  # the page's title, poet and heading above an invocation
            if num is not None and lib == "2300":
                num += 10 * page_no  # Muthumozhikkanchi: each page numbers its ten 1-10
            if lines:
                out.append((num if num is not None else 0, lines))
            num = None
    return out


def similarity(a, b):
    from difflib import SequenceMatcher
    return SequenceMatcher(None, a, b, autojunk=False).ratio()


def compare_site(key, records, site):
    """Line-by-line comparison with the site. Returns counts for the report.

    The site's verse is first aligned to ours line by line (difflib over the lines' letters), so
    a heading run into the site's verse, or a line the site lost, does not shift the rest."""
    from difflib import SequenceMatcher
    ours = {}
    for r in records:
        if r["kind"] == "verse" or r.get("source_number") is not None:
            ours[r.get("source_number", r["number"])] = r
    stats = Counter()
    site_ns = set()
    adds, split = [], []
    for sv in site:
        n = sv["n"]
        site_ns.add(n)
        r = ours.get(n)
        if r is None:
            stats["site_only"] += 1
            flag(key, f"{key}:site{n}", "site_diff", f"the site has a verse {n} we do not",
                 None, " / ".join(sv["lines"]))
            continue
        a = [letters(l) for l in r["tamil"]]
        b = [letters(re.sub(r"\d+\s*$", "", l)) for l in sv["lines"]]
        ja, jb = "".join(a), "".join(b)
        if ja == jb:
            stats["same"] += 1
            if len(a) != len(b):
                stats["lineation"] += 1
                split.append(r["number"])
            continue
        sim = similarity(ja, jb)
        if sim < 0.6 and ja not in jb:
            stats["different_verse"] += 1
            flag(key, r["id"], "site_diff", f"the site's verse {n} is a different verse "
                 f"(similarity {sim:.2f})", None, " / ".join(sv["lines"]))
            continue
        extra, lacking, differ = [], [], []
        for op, i1, i2, j1, j2 in SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if op == "equal":
                continue
            if op == "insert":
                extra.extend(sv["lines"][j1:j2])
            elif op == "delete":
                lacking.extend(range(i1, i2))
            else:
                pairs = list(zip(range(i1, i2), range(j1, j2)))
                for i, j in pairs:
                    if similarity(a[i], b[j]) >= 0.5:
                        differ.append((i, j))
                    else:
                        lacking.append(i)
                        extra.append(sv["lines"][j])
                lacking.extend(range(i1 + len(pairs), i2))
                extra.extend(sv["lines"][j1 + len(pairs):j2])
        if extra and not lacking and not differ:
            stats["site_adds_text"] += 1
            adds.append(r["number"] if r["number"] is not None else r["id"])
            continue
        if extra:
            stats["site_adds_text"] += 1
            adds.append(r["number"] if r["number"] is not None else r["id"])
        if lacking:
            stats["site_lacks_lines"] += 1
            flag(key, r["id"], "site_diff", "the site's text lacks line(s) "
                 + ", ".join(str(i + 1) for i in lacking), lacking[0] + 1,
                 " / ".join(r["tamil"][i] for i in lacking))
        if differ:
            stats["reading"] += 1
            for i, j in differ:
                flag(key, r["id"], "site_diff", "reading differs from the site", i + 1,
                     f"ours: {r['tamil'][i]} | site: {sv['lines'][j]}")
    if adds:
        flag(key, key, "site_diff", "the site's text also carries non-verse lines (Project "
             "Madurai's headings, thurai labels, metre labels or notes run into the verse) in "
             + ", ".join(map(str, adds)))
    if split:
        flag(key, key, "site_diff", "same letters, lines split differently on the site (it drops "
             "the lines that are wholly lost, or joins lines) in " + ", ".join(map(str, split)))
    for r in records:
        sn = r.get("source_number", r["number"])
        if r["kind"] == "verse" and sn not in site_ns:
            stats["ours_only"] += 1
            flag(key, r["id"], "site_diff", "the site lacks this verse")
    return stats


def vowel_sign_diffs(key, r, t):
    """Flag places where tamilvu has a vowel sign that our line lacks, or the other e/o sign.
    The tamilvu text is word-split, so most other differences are sandhi, not error."""
    from difflib import SequenceMatcher
    eo = {"\u0BC6", "\u0BC7", "\u0BCA", "\u0BCB"}
    for i, (ol, tl) in enumerate(zip(r["tamil"], t), 1):
        a, c = letters(ol), letters(tl)
        for op, i1, i2, j1, j2 in SequenceMatcher(None, a, c, autojunk=False).get_opcodes():
            lost = op == "insert" and j2 - j1 == 1 and c[j1] in VOWEL_SIGNS and c[j1] != "\u0BCD"
            swap = (op == "replace" and i2 - i1 == 1 and j2 - j1 == 1 and {a[i1], c[j1]} <= eo)
            if lost or swap:
                flag(key, r["id"], "misprint_candidate", "tamilvu has " + (
                     "a vowel sign here that the source lacks" if lost else
                     "the other e/o vowel sign") + f"; tamilvu: {tl}", i, ol)
                break


def compare_tvu(key, records, tvu):
    stats = Counter()
    by_n = {}
    inv = [lines for n, lines in tvu if n == 0]
    for n, lines in tvu:
        if n:
            by_n[n] = lines
    for r in records:
        if r["kind"] == "verse":
            t = by_n.get(r["number"])
        elif r["kind"] == "invocation":
            part = r.get("invocation_part", 1) - 1
            t = inv[part] if part < len(inv) else None
        else:
            continue
        if t is None:
            stats["missing_in_tvu"] += 1
            flag(key, r["id"], "tvu_check", "no verse with this number in tamilvu")
            continue
        a, b = letters("".join(r["tamil"])), letters("".join(t))
        sim = similarity(a, b)
        if sim < 0.6:
            stats["different_verse"] += 1
            flag(key, r["id"], "tvu_check", f"tamilvu's verse {r['number']} is a different verse "
                 f"(similarity {sim:.2f})", None, " / ".join(t))
        elif a == b:
            stats["same"] += 1
        else:
            stats["close"] += 1
            vowel_sign_diffs(key, r, t)
        if len(t) != len(r["tamil"]) and sim >= 0.6:
            flag(key, r["id"], "line_count", f"{len(r['tamil'])} lines; tamilvu has {len(t)} "
                 "(a line lost in the source?)", None, "tamilvu: " + " / ".join(t))
    extra = sorted(set(by_n) - {r["number"] for r in records if r["kind"] == "verse"})
    for n in extra:
        stats["tvu_only"] += 1
        flag(key, f"{key}:{n}", "tvu_check", "tamilvu has this verse; the base text does not",
             None, " / ".join(by_n[n]))
    return stats


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as out:
        for r in records:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text-dir", type=Path, default=ROOT / "data" / "text")
    ap.add_argument("--out-dir", type=Path, default=ROOT / "kg" / "core")
    ap.add_argument("--site-dir", type=Path, default=None)
    ap.add_argument("--tvu-dir", type=Path, default=None)
    args = ap.parse_args()

    keys = [b[0] for b in BOOKS]
    results = {}
    for spec in BOOKS:
        key = spec[0]
        recs, lost = build_book(args.text_dir, spec)
        cross_duplicates(key, recs)
        ids = Counter(r["id"] for r in recs)
        for i, c in ids.items():
            if c > 1:
                flag(key, i, "duplicate_id", f"id occurs {c} times")
        results[key] = (spec, recs, lost)

    report = {}
    for key, (spec, recs, lost) in results.items():
        site_stats = tvu_stats = None
        if args.site_dir and args.site_dir.exists():
            site = load_site(args.site_dir, SITE_IDS[key])
            if site is not None:
                site_stats = compare_site(key, recs, site)
        if args.tvu_dir and args.tvu_dir.exists() and key in TVU_LIBS:
            tvu = load_tvu(args.tvu_dir, TVU_LIBS[key])
            if tvu:
                tvu_stats = compare_tvu(key, recs, tvu)
        report[key] = (site_stats, tvu_stats)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for key, (spec, recs, lost) in results.items():
        write_jsonl(args.out_dir / f"{key}.jsonl", recs)
    flags_path = args.out_dir / "sangam_text_flags.jsonl"
    kept = []
    if flags_path.exists():
        for l in flags_path.read_text(encoding="utf-8").splitlines():
            if l.strip() and json.loads(l).get("book") not in keys:
                kept.append(l)
    with open(flags_path, "w", encoding="utf-8") as out:
        for l in kept:
            out.write(l + "\n")
        for f in flags:
            out.write(json.dumps(f, ensure_ascii=False) + "\n")

    for key, (spec, recs, lost) in results.items():
        verses = [r for r in recs if r["kind"] == "verse"]
        inv = sum(1 for r in recs if r["kind"] == "invocation")
        pay = sum(1 for r in recs if r["kind"] == "payiram")
        std = spec[6]
        print(f"{key:<26} {len(verses):>3} verses (standard {std}{', lost ' + str(sorted(lost)) if lost else ''})"
              f" + {inv} invocation + {pay} payiram; site {dict(report[key][0] or {})}; "
              f"tvu {dict(report[key][1] or {})}")
    print("flags:", dict(Counter((f["book"], f["kind"]) for f in flags)))


if __name__ == "__main__":
    main()
