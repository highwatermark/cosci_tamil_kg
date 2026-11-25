#!/usr/bin/env python3
"""Build the original Tamil text of six Ettuthogai anthologies, checked against sangamtamil.com.

Writes (one record per poem, the same fields as kg/core/akananuru.jsonl):
  kg/core/natrinai.jsonl        invocation (0) and poems 1-400 (234 is lost)
  kg/core/kuruntokai.jsonl      invocation (0) and poems 1-401
  kg/core/ainkurunuru.jsonl     poems 1-500 (129 and 130 are lost), `section` = the hundred
  kg/core/patitruppattu.jsonl   poems 11-90 (decades 2-9), the eight patikams, and the fragments
  kg/core/paripadal.jsonl       the 22 songs and the fragments (Paripadal thirattu)
  kg/core/kalittokai.jsonl      poems 1-150 (1 is the invocation), `section` = the kali
  kg/core/sangam_text_flags.jsonl  this script's entries for these six books are replaced; the
                                entries of every other book are kept as they are

Base text: the Project Madurai e-texts mirrored in data/text/:
  pmuni0296 Natrinai, pmuni0110 Kuruntokai, pmuni0028 Ainkurunuru, pmuni0038 Patitruppattu,
  pmuni0087 Paripadal and Paripadal thirattu, pmuni0221 Kalittokai.

Witness: the sangamtamil.com verse files (data/verses/<book>.js of the cached crawl, given with
--stc-dir). Only the Tamil verse lines and the thinai label are read. The site's English
translations, English situation notes and romanized names are never read into a record.

What the cross-check does, for each poem:
  1. Our lines (after the character repairs below) are aligned with the site's lines by a
     dynamic programme on letter similarity (difflib ratio of the Tamil letters), allowing a
     line on one side only, and one line on one side against two on the other (a different
     line break). Paripadal is aligned against the whole site text, because the site's units
     do not follow the traditional numbering.
  2. Each aligned pair is classed: `same` (the same Tamil letters; spacing and punctuation
     ignored), `spelling` (the same consonant skeleton once vowels, vowel signs and the usual
     sandhi alternations are set aside: e.g. our செங்கோ லம்பிற் against the site's செங்கோல்
     அம்பின்), or `reading` (a real difference of letters).
  3. Repairs taken from the site, each logged in the record's `variants` and in the flags:
     - the lost vowel sign ொ after ய or ள (the -ஒடு fault found in the Purananuru: யடு for யொடு).
       Natrinai and Paripadal have no யொ or ளொ at all, so there the sign is restored wherever
       the site's line has the word with ொ or ோ;
     - words with encoding junk (TSCII leftovers, unassigned code points) that the generic
       rules below cannot mend: the word is replaced by the site's word(s);
     - a line the site has and we lack, inside the poem (not facing a line of ours): the site's
       line is supplied (`line_sources` says so).
     Everything else keeps our reading; the site's reading is stored in `variants`.

Character repairs (before the cross-check; logged in the flags):
  · -> ஃ; TSCII leftovers for ரி: (ா|஡|¡)(஢|¢) -> ரி and (ொ|ௌ)(஢|¢) -> ெரி (கடும்பா஢ =
  கடும்பரி, தொ¢ய = தெரிய, தௌ¢மே = தெரிமே); ¦’+consonant -> consonant+ெ; zero-width characters;
  the asterisks around the phrase that names a Patitruppattu poem; a stray space before a dead
  consonant.

Copyright: only verse lines and the traditional colophon facts (poet, patron, thinai, thurai,
the speaker label, the decade and poem names, metre and music of Paripadal) are kept. The
e-texts' modern notes, headings inside Paripadal songs and source remarks are not copied.

Run: python3 -I scripts/build_ettuthogai_core.py [--text-dir DIR] [--stc-dir DIR] [--out-dir DIR]
"""
import argparse
import difflib
import importlib.util
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STC_DEFAULT = Path("/private/tmp/claude-501/-Users-harilakshmanan-Cursor-cosci-knowledge-graph/"
                   "56dc2695-7ba3-4110-8a35-77dd53b3fdc5/scratchpad/sangamtamil_crawl")

_spec = importlib.util.spec_from_file_location("build_sangam_core", ROOT / "scripts" / "build_sangam_core.py")
core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(core)

BOOKS = ("natrinai", "kuruntokai", "ainkurunuru", "patitruppattu", "paripadal", "kalittokai")
RIGHTS = {"tamil": "public_domain", "colophon": "public_domain"}
TAMIL_CHAR = core.TAMIL_CHAR
VOWEL_SIGNS = core.VOWEL_SIGNS
CONSONANTS = core.CONSONANTS
THINAI = ("குறிஞ்சி", "முல்லை", "மருதம்", "நெய்தல்", "பாலை")
STC_THINAI = {"kurinji": "குறிஞ்சி", "mullai": "முல்லை", "marutam": "மருதம்", "marutham": "மருதம்",
              "neytal": "நெய்தல்", "neythal": "நெய்தல்", "palai": "பாலை"}
# Usual line counts of the poems (the anthologies' own definition), used as a sanity check.
LINE_RANGE = {"natrinai": (8, 13), "kuruntokai": (4, 9), "ainkurunuru": (3, 6),
              "patitruppattu": (5, 57), "paripadal": (32, 140), "kalittokai": (11, 80)}

REPAIRS = (
    (re.compile(r"·"), "ஃ", "'·' is the old encoding of ஃ"),
    (re.compile(r"ொ[\u0BA2¢]"), "ெரி", "TSCII leftover: ொ + '¢' = ெ + ரி"),
    (re.compile(r"ோ[\u0BA2¢]"), "ேரி", "TSCII leftover: ோ + '¢' = ே + ரி (போ஢சை = பேரிசை)"),
    (re.compile(r"\u0BA1ண"), "ரீ", "TSCII leftover for ரீ (ஒ஡ணஇய = ஒரீஇய)"),
    (re.compile(r"ௌ[\u0BA2¢]"), "ெளி", "TSCII leftover: ௌ + '¢' = ெ + ளி"),
    (re.compile(r"ௌி"), "ெளி", "TSCII leftover: ௌ + ி = ெளி (தௌிய = தெளிய)"),
    (re.compile(r"ௌ (?=ள)"), "ெள்", "TSCII leftover: 'ௌ ' before ள = ெள் (தௌ ளிதின் = தெள்ளிதின்)"),
    (re.compile(r"ௌ (?=[\u0B85-\u0BB9])"), "ெளி", "TSCII leftover: 'ௌ ' = ெளி (தௌ ர்ப்ப = தெளிர்ப்ப)"),
    (re.compile(r"[ா\u0BA1¡][\u0BA2¢]"), "ரி", "TSCII leftover for ரி"),
    (re.compile(r"¦’([\u0B95-\u0BB9])"), "\\1\u0BC6", "TSCII leftover '¦’' + consonant = consonant + ெ"),
    (re.compile(r"[\u200B-\u200D\uFEFF]"), "", "zero-width character removed"),
    (re.compile(r"\*"), "", "asterisk marking the poem's name removed"),
    (re.compile(r"(?<=[\u0BBE-\u0BCC]) (?=[\u0B95-\u0BB9]\u0BCD(?:[^\u0B80-\u0BFF]|$))"), "",
     "stray space before a final dead consonant removed (கண்டோ ர் = கண்டோர்)"),
)

flags = []


def flag(book, rid, kind, detail, line=None, text=None):
    rec = {"book": book, "id": rid, "kind": kind, "line": line, "detail": detail}
    if text is not None:
        rec["text"] = text
    flags.append(rec)


def assigned(ch):
    try:
        unicodedata.name(ch)
        return True
    except ValueError:
        return False


def letters(s):
    return "".join(ch for ch in s if "\u0B80" <= ch <= "\u0BFF" and assigned(ch))


# Consonant skeleton: drop vowels, vowel signs and pulli, and fold the sandhi alternations of
# the two spelling conventions (joined sandhi against split base forms).
SANDHI_FOLD = str.maketrans({"ற": "ன", "ண": "ன", "ங": "ம", "ஞ": "ம", "ந": "ம", "ட": "ள",
                             "ல": "ள", "ழ": "ள", "ர": "ள"})


SANDHI_JOIN = (("ள்ந", "ண்ண"), ("ல்ந", "ன்ன"), ("ள்த", "ட்ட"), ("ல்த", "ற்ற"), ("ம்ப", "ம்ப"))


def skeleton(s):
    out = []
    t = letters(s)
    for a, b in SANDHI_JOIN:
        t = t.replace(a, b)
    for ch in t:
        if ch in CONSONANTS:
            out.append(ch)
    sk = "".join(out).translate(SANDHI_FOLD)
    sk = re.sub(r"(.)\1+", r"\1", sk)  # doubled consonants (சேஎய், புணர்ச்சி) fold
    sk = sk.replace("ய", "").replace("வ", "")  # glides inserted between vowels
    return sk


_ratio_cache = {}


def sim(a, b):
    key = (a, b)
    if key not in _ratio_cache:
        if not a or not b:
            _ratio_cache[key] = 0.0
        else:
            _ratio_cache[key] = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
    return _ratio_cache[key]


def body_lines(text_dir, name):
    return core.body(text_dir, name).split("\n")


def repair_line(book, rid, n, line):
    for pat, rep, why in REPAIRS:
        new = pat.sub(rep, line)
        if new != line:
            if why.startswith("asterisk"):
                line = new
                continue
            flag(book, rid, "repaired", why, n, f"{line} -> {new}")
            line = new
    return re.sub(r"\s+", " ", line).strip()


def blank_free(lines):
    return [l for l in lines if l.strip()]


def unit(book, n, rid=None, **kw):
    u = {"book": book, "number": n, "id": rid or f"{book}:{n}", "kind": "poem", "section": None,
         "decade": None, "title": None, "poet": None, "patron": None, "thinai": None,
         "thurai": None, "note": None, "colophon": [], "raw": [], "marks": [], "stc_key": n}
    u.update(kw)
    return u


def add_line(u, s):
    s = re.sub(r"(?:\s*-){3,}\s*$", " ...", s)  # a run of dashes marks lost text
    s = re.sub(r"^(\d{1,3})\s+(?=\S.*\s\1$)", "", s)  # a line number printed at both ends
    if " = " in s:  # an editor's gloss (பஃறோல் = பல்தோல்), not verse
        u.setdefault("dropped_glosses", []).append(s)
        return
    if re.fullmatch(r"\d{1,3}", s.strip()):  # a line number alone: it belongs to the line above
        if u["raw"]:
            u["marks"].append((len(u["raw"]), int(s)))
        return
    text, num = core.split_mark(s)
    text = core.tidy(text)
    if not text:
        return
    u["raw"].append(text)
    if num is not None:
        u["marks"].append((len(u["raw"]), num))


# --------------------------------------------------------------------------------------------
# Parsers: each returns a list of units in reading order

def parse_natrinai(text_dir):
    L = body_lines(text_dir, "pmuni0296")
    units = []
    i0 = next(i for i, l in enumerate(L) if l.strip() == "கடவுள் வாழ்த்து")
    j = next(i for i in range(i0, len(L)) if L[i].strip() == "பாரதம் பாடிய பெருந்தேவனார்")
    inv = unit("natrinai", 0, kind="invocation", title="கடவுள் வாழ்த்து", poet="பெருந்தேவனார்",
               colophon=["poet: பாரதம் பாடிய பெருந்தேவனார்"])
    for l in L[i0 + 1:j]:
        if l.strip():
            add_line(inv, l.strip())
    units.append(inv)
    heads = []
    for i, l in enumerate(L):
        m = re.match(rf"^(\d{{1,3}})\s*[.]?\s*-?\s*({'|'.join(THINAI)})\s*(?:[-=]\s*(.*)|(\(\?\)))?$", l.strip())
        if m and (not heads or heads[-1][0] < int(m.group(1)) <= heads[-1][0] + 3):
            heads.append((int(m.group(1)), i, m.group(2), (m.group(3) or m.group(4) or "").strip()))
        elif re.match(r"^234\s*-", l.strip()):
            heads.append((234, i, None, None))
    for k, (n, i, thinai, poet) in enumerate(heads):
        end = heads[k + 1][1] if k + 1 < len(heads) else len(L)
        if n == 234:
            flag("natrinai", "natrinai:234", "missing_poem", "poem 234 is lost; the e-text prints two "
                 "verses proposed by modern scholars as the lost poem (not adopted)")
            continue
        seg = L[i + 1:end]
        blocks, cur = [], []
        for l in seg:
            if l.strip():
                cur.append(l.strip())
            elif cur:
                blocks.append(cur)
                cur = []
        if cur:
            blocks.append(cur)
        u = unit("natrinai", n, thinai=thinai)
        u["colophon"].append(f"heading: {L[i].strip()}")
        if poet in ("(?)", "?"):
            u["note"] = "poet's name not preserved"
        elif poet == "":
            u["note"] = "the base text names no poet"
            flag("natrinai", u["id"], "colophon", "heading gives no poet and no '(?)'", None, L[i].strip())
        else:
            u["poet"] = poet.rstrip(".")
        u["verse_blocks"] = blocks[:1]
        u["thurai_blocks"] = blocks[1:]
        for l in blocks[0] if blocks else []:
            add_line(u, l)
        if len(blocks) > 1:
            u["thurai"] = " ".join(" ".join(b) for b in blocks[1:])
        units.append(u)
    return units


def parse_kuruntokai(text_dir):
    L = body_lines(text_dir, "pmuni0110")
    units = []
    i0 = next(i for i, l in enumerate(L) if l.strip() == "கடவுள் வாழ்த்து")
    cur = unit("kuruntokai", 0, kind="invocation", title="கடவுள் வாழ்த்து", stc_key=None)
    units.append(cur)
    for l in L[i0 + 1:]:
        s = l.strip()
        if not s:
            continue
        m = re.match(r"^(\d{1,3})\.\s*(\S+)\s*-\s*(.+)$", s)
        if m:
            thinai = m.group(2)
            cur = unit("kuruntokai", int(m.group(1)), thinai=thinai, thurai=m.group(3).strip())
            cur["colophon"].append(f"heading: {s}")
            if thinai not in THINAI:
                fixed = difflib.get_close_matches(thinai, THINAI, 1, 0.5)
                flag("kuruntokai", cur["id"], "colophon", f"thinai printed {thinai!r}; read as "
                     f"{fixed[0] if fixed else None!r}")
                cur["thinai"] = fixed[0] if fixed else None
            units.append(cur)
            continue
        if s.startswith("-") and not TAMIL_CHAR.search(s) and set(s) <= set("-. "):
            cur["colophon"].append(f"poet: {s}")
            cur["note"] = "poet's name not preserved"
            continue
        if s.startswith("-") and TAMIL_CHAR.search(s):
            name = s.strip("-. ")
            cur["colophon"].append(f"poet: {name}")
            if cur["number"] == 0:
                cur["poet"] = re.sub(r"^பாரதம் பாடிய\s*", "", name)
            else:
                cur["poet"] = name
            continue
        if s.startswith("குறுந்தொகை முற்றிற்று") or set(s) <= set("-~ "):
            continue
        add_line(cur, s)
    return units


AINKURU_HUNDREDS = (("மருதம்", "ஓரம்போகியார்"), ("நெய்தல்", "அம்மூவனார்"), ("குறிஞ்சி", "கபிலர்"),
                    ("பாலை", "ஓதலாந்தையார்"), ("முல்லை", "பேயனார்"))


def parse_ainkurunuru(text_dir):
    L = [l.strip() for l in body_lines(text_dir, "pmuni0028")]
    start = next(i for i, l in enumerate(L) if l.startswith("-------"))
    units, cur, expected, titles = [], None, 1, {}
    nonblank = [i for i in range(start + 1, len(L)) if L[i]]
    for k, i in enumerate(nonblank):
        s = L[i]
        nxt = L[nonblank[k + 1]] if k + 1 < len(nonblank) else ""
        m = re.match(r"^(\d{1,3})(?:\.\s*(.*)|\s*)$", s)
        if s.startswith("This webpage") or s.startswith("Feel free"):
            break
        if re.match(r"^\d{1,3}\.\s*கிடைக்காத பாடல்", s):
            lost = int(s.split(".")[0])
            flag("ainkurunuru", f"ainkurunuru:{lost}", "missing_poem", "poem lost (the base text: "
                 "கிடைக்காத பாடல்)")
            expected = lost + 1
            cur = None
            continue
        is_title = (s.rstrip(". ").endswith("பத்து") and len(s.split()) <= 8
                    and re.match(r"^\d{1,3}(\.|\s*$)", nxt))
        if is_title:
            title = re.sub(r"^\d{1,2}\.\s*", "", s).rstrip(". ").strip()
            nm = re.match(r"^(\d{1,3})", nxt)
            titles[(int(nm.group(1)) - 1) // 10 + 1] = (title, s)
            continue
        if m and (int(m.group(1)) == expected or (int(m.group(1)) > expected and int(m.group(1)) <= expected + 3
                                                  and (not m.group(2) or TAMIL_CHAR.search(m.group(2) or "")))):
            n = int(m.group(1))
            for lost in range(expected, n):
                if True:
                    flag("ainkurunuru", f"ainkurunuru:{lost}", "missing_poem", "poem not found in the base text")
            expected = n + 1
            h = (n - 1) // 100
            cur = unit("ainkurunuru", n, section=AINKURU_HUNDREDS[h][0], thinai=AINKURU_HUNDREDS[h][0],
                       poet=AINKURU_HUNDREDS[h][1], decade=(n - 1) // 10 + 1)
            units.append(cur)
            if m.group(2):
                add_line(cur, m.group(2))
            continue
        if cur is None:
            continue
        if "முற்றிற்று" in s or set(s) <= set("-~ "):
            continue
        add_line(cur, s)
    for u in units:
        t = titles.get(u["decade"])
        u["title"] = None
        u["decade_title"] = t[0] if t else None
        u["colophon"] = [f"hundred: {u['section']} (poet {u['poet']}, by the traditional division)"]
        if t:
            u["colophon"].append(f"decade {u['decade']}: {t[1]}")
    for d in range(1, 51):
        if d not in titles:
            flag("ainkurunuru", f"ainkurunuru:{(d - 1) * 10 + 1}", "colophon",
                 f"the e-text prints no title for decade {d} (poems {(d - 1) * 10 + 1}-{d * 10})")
    return units


def patron_name(s):
    s = s.strip(" .")
    return re.sub(r"னை(?:க்|ப்)?$", "ன்", s)


def parse_patitruppattu(text_dir):
    L = [l.strip() for l in body_lines(text_dir, "pmuni0038")]
    units, cur, state, patron, poet = [], None, None, None, None
    decade_info = {}
    frag_at = next(i for i, l in enumerate(L) if l.startswith("### பத்தாம் பத்து"))
    COL = re.compile(r"^(பெயர்|துறை|தூக்கு|வண்ணம்)\s*[-:]\s*(.+)$")
    for i, s in enumerate(L[:frag_at]):
        if not s or set(s) <= set("~-* "):
            continue
        if s.startswith("### "):
            state = "between"
            continue
        if m := re.match(r"^பாடப்பட்டோன்\s*:\s*(.+)$", s):
            patron = m.group(1)
            continue
        if m := re.match(r"^பாடியவர்\s*:\s*(.+)$", s):
            poet = m.group(1)
            continue
        if m := re.match(r"^பாட்டு\s*-\s*(\d+)$", s):
            n = int(m.group(1))
            d = (n - 1) // 10 + 1
            decade_info.setdefault(d, (patron, poet))
            cur = unit("patitruppattu", n, decade=d, patron=patron_name(patron) if patron else None,
                       poet=repair_line("patitruppattu", f"patitruppattu:{n}", None, poet) if poet else None)
            cur["colophon"] += [f"patron: {patron}", f"poet: {cur['poet']}"]
            units.append(cur)
            state = "verse"
            continue
        if s == "(பதிகம்)":
            d = cur["decade"]
            p, q = decade_info.get(d, (None, None))
            cur = unit("patitruppattu", None, rid=f"patitruppattu:patikam:{d}", kind="patikam",
                       decade=d, title="பதிகம்", stc_key=None, patron=patron_name(p) if p else None,
                       poet=repair_line("patitruppattu", f"patitruppattu:patikam:{d}", None, q) if q else None)
            units.append(cur)
            state = "patikam"
            continue
        if state == "verse" and (m := COL.match(s)):
            key, val = m.group(1), m.group(2).strip()
            cur["colophon"].append(f"{key}: {val}")
            if key == "பெயர்":
                cur["title"] = re.sub(r"\s*\((?:அடி\s*)?\d+\)\s*$", "", val).strip()
            elif key == "துறை":
                cur["thurai"] = val
            elif key == "தூக்கு":
                cur["metre"] = val
            elif key == "வண்ணம்":
                cur["vannam"] = val
            continue
        if state == "verse" and cur and cur["kind"] == "poem":
            if cur["colophon"][2:]:  # text after the colophon: kept with the colophon
                cur["colophon"].append(f"also: {s}")
                flag("patitruppattu", cur["id"], "colophon", "a line after the colophon, not verse; "
                     "kept in colophon_raw", None, s)
                continue
            add_line(cur, s)
            continue
        if state == "patikam":
            if cur.get("names") and not cur.get("names_open"):  # after the list of names
                if s.startswith("[") or "முற்றிற்று" in s:
                    continue
                if s.startswith("பாடிப்பெற்ற பரிசில்") or "வீற்றிருந்தான்" in s or not cur["colophon"]:
                    cur["colophon"].append(s)
                else:
                    cur["colophon"][-1] += " " + s
                continue
            if s.startswith("அவைதாம்") or cur.get("names_open"):
                cur["names_open"] = "இவை பாட்டின் பதிகம்" not in s
                cur.setdefault("names", []).append(s)
                continue
            if s.startswith("பாடிப்பெற்ற பரிசில்") or s.endswith("வீற்றிருந்தான்.") or "வீற்றிருந்தான்" in s:
                cur["colophon"].append(s)
                continue
            if s.startswith("[") or "முற்றிற்று" in s:
                continue
            add_line(cur, s)
    for u in units:
        if u["kind"] == "patikam":
            names = " ".join(u.pop("names", []))
            u.pop("names_open", None)
            u["colophon"].insert(0, names)
            u["poem_names"] = [x.strip(" .:") for x in
                               re.sub(r"^அவைதாம்\s*:\s*", "", names).split("இவை பாட்டின் பதிகம்")[0].split(",")]
    # fragments of the lost decades, quoted in commentaries
    cur = None
    for s in L[frag_at:]:
        if s.startswith("This webpage"):
            break
        if m := re.match(r"^\((\d)\)$", s):
            k = int(m.group(1))
            cur = unit("patitruppattu", None, rid=f"patitruppattu:fragment:{k}", kind="fragment",
                       title=None, stc_key=None, fragment=k)
            units.append(cur)
            continue
        if cur is None or not s or s.startswith("*") or set(s) <= set("~ "):
            continue
        if s.startswith("(") and s.endswith(")") or s.startswith("(") and not cur["raw"] == []:
            cur["colophon"].append(f"quoted in: {s.strip('()')}")
            continue
        if cur["colophon"] and cur["colophon"][-1].startswith("quoted in") and not s.endswith(")"):
            if s.startswith("'"):
                cur["colophon"].append(s)
                continue
        if s.endswith(")") and cur["colophon"]:
            cur["colophon"][-1] += " " + s.strip("()")
            continue
        if s.startswith("'"):
            cur["colophon"].append(f"mention: {s}")
            continue
        add_line(cur, s)
    out = []
    for u in units:
        if u["kind"] == "fragment" and not u["raw"]:
            flag("patitruppattu", u["id"], "missing_poem", "fragment known only by a mention in a "
                 "commentary; no verse text (not recorded)")
            continue
        if u["kind"] == "fragment":
            u["colophon"] = [c for c in u["colophon"] if c]
        out.append(u)
    return out


ORDINALS = {"ஐந்தாம்": 5, "ஆறாம்": 6, "எட்டாம்": 8, "ஒன்பதாம்": 9, "பத்தாம்": 10, "பதினோராம்": 11,
            "பனிரெண்டாம்": 12, "பன்னிரண்டாம்": 12, "பதிமூன்றாம்": 13}


def parse_paripadal(text_dir):
    L = [l.rstrip() for l in body_lines(text_dir, "pmuni0087")]
    start = next(i for i, l in enumerate(L) if re.match(r"^1\.\s*திருமால்", l.strip()))
    thir = next(i for i, l in enumerate(L) if l.strip() == "பரிபாடல்-திரட்டு")
    units = []

    def segments(lo, hi, fragment):
        heads = []
        for i in range(lo, hi):
            s = L[i].strip()
            m = re.match(r"^(\d{1,2})\.\s*(திருமால்|செவ்வேள்|வையை|மதுரை)\s*$", s)
            if m:
                heads.append((int(m.group(1)), m.group(2), i))
            elif fragment and (m := re.match(r"^(\S+)\s+பாடல்$", s)) and m.group(1) in ORDINALS:
                heads.append((ORDINALS[m.group(1)], None, i))
        return heads

    for fragment, lo, hi in ((False, start, thir), (True, thir + 1, len(L))):
        heads = segments(lo, hi, fragment)
        for k, (n, subject, i) in enumerate(heads):
            end = heads[k + 1][2] if k + 1 < len(heads) else hi
            if fragment:
                u = unit("paripadal", None, rid=f"paripadal:thirattu:{n}", kind="fragment",
                         title=subject, stc_key=None, fragment=n)
            else:
                u = unit("paripadal", n, title=subject)
            u["colophon"].append(f"subject: {subject}" if subject else "subject: (not given)")
            blocks, cur = [], []
            in_paren = False
            for l in L[i + 1:end]:
                s = l.strip()
                # an editor's prose note in brackets (the situation of the song, or where a
                # fragment is quoted): not verse
                if in_paren or (s.startswith("(") and not core.split_mark(s)[1]):
                    in_paren = not re.search(r"\)\.?$", s)
                    u.setdefault("dropped_notes", 0)
                    u["dropped_notes"] += 1
                    continue
                s = s.replace("_", "").strip()
                if not s or set(s) <= set("-~"):
                    if cur:
                        blocks.append(cur)
                        cur = []
                    continue
                cur.append(s)
            if cur:
                blocks.append(cur)
            dropped = []
            in_note = False
            for b in blocks:
                if in_note or (b[0].startswith("(") and not TAMIL_CHAR.search(b[0][:1] or "x")):
                    pass
                if b[0].startswith("(இ") or b[0].startswith("(இது") or in_note:
                    # an editor's note on where the fragment is quoted
                    in_note = not b[-1].endswith(")")
                    continue
                if b[0].startswith("(பரிபாடல் திரட்டு முற்றிற்று"):
                    continue
                if len(b) == 1 and b[0].startswith("இப் பகுதி"):
                    continue
                if b[0].startswith("இப் பகுதி"):
                    continue
                if all(re.match(r"^(பாடியவர்|இசையமைத்தவர்|இசை|பண்)\s*::?", x) for x in b):
                    for x in b:
                        key, val = re.split(r"\s*::?\s*", x, maxsplit=1)
                        u["colophon"].append(f"{key}: {val}")
                        if key == "பாடியவர்":
                            u["poet"] = val
                        elif key == "இசையமைத்தவர்":
                            u["music"] = val
                        elif key == "பண்":
                            u["pan"] = val
                    continue
                if b == ["கடவுள் வாழ்த்து"]:
                    continue
                marked = any(core.split_mark(x)[1] is not None for x in b)
                if len(b) <= 2 and not marked and all(len(x.split()) <= 5 for x in b) and k_is_heading(b):
                    dropped.append(" / ".join(b))
                    continue
                for x in b:
                    add_line(u, x)
            if dropped:
                u["dropped_headings"] = dropped
            units.append(u)
    return units


def k_is_heading(b):
    """A modern section heading inside a Paripadal song: a short block with no line number and
    no verse punctuation at the end."""
    return all(not re.search(r"[,;:!?.\-–—‘’'\"]$", x) for x in b)


KALI_SECTIONS = (("பாலை", "பாலைக்கலி"), ("குறிஞ்சி", "குறிஞ்சிக்கலி"), ("மருத", "மருதக்கலி"),
                 ("முல்லை", "முல்லைக்கலி"), ("நெய்தல்", "நெய்தற்கலி"))


def parse_kalittokai(text_dir):
    L = [l.strip() for l in body_lines(text_dir, "pmuni0221")]
    start = next(i for i, l in enumerate(L) if l == "கடவுள் வாழ்த்து")
    units, cur, expected = [], None, 1
    section = thinai = poet = None
    raw_head = None
    for s in L[start + 1:]:
        if not s:
            continue
        if s.startswith("### "):
            if "முற்றும்" in s:
                break
            raw_head = s[4:]
            for key, name in KALI_SECTIONS:
                if key in s:
                    section, thinai = name, (key if key != "மருத" else "மருதம்")
            continue
        if m := re.match(r"^ஆசிரியர்\s*:\s*(.+)$", s):
            poet = m.group(1).strip()
            usual = {"மருதநிலங்கன்": "மருதன் இளநாகனார்", "நல்லாந்துவனார்": "நல்லந்துவனார்"}.get(poet)
            if usual:
                flag("kalittokai", None, "colophon", f"the base text names the poet of {section} "
                     f"{poet!r}; the usual attribution is {usual!r} (base kept)")
            continue
        m = re.match(r"^(\d{1,3})\s+(\S.*)$", s)
        if m and int(m.group(1)) == expected:
            n = expected
            expected += 1
            if n == 1:
                cur = unit("kalittokai", 1, kind="invocation", title="கடவுள் வாழ்த்து",
                           note="the base text names no poet (usually ascribed to நல்லந்துவனார்)")
            else:
                cur = unit("kalittokai", n, section=section, thinai=thinai, poet=poet)
                cur["colophon"] = [f"section: {raw_head}", f"poet: {poet}"]
            units.append(cur)
            add_line(cur, m.group(2))
            continue
        if m and TAMIL_CHAR.search(m.group(2)):
            flag("kalittokai", cur["id"] if cur else None, "numbering",
                 f"line starts with an unexpected number {m.group(1)} (expected {expected})", None, s)
        if cur is not None:
            add_line(cur, s)
    return units


PARSERS = {"natrinai": parse_natrinai, "kuruntokai": parse_kuruntokai,
           "ainkurunuru": parse_ainkurunuru, "patitruppattu": parse_patitruppattu,
           "paripadal": parse_paripadal, "kalittokai": parse_kalittokai}
SOURCES = {"natrinai": "pmuni0296", "kuruntokai": "pmuni0110", "ainkurunuru": "pmuni0028",
           "patitruppattu": "pmuni0038", "paripadal": "pmuni0087", "kalittokai": "pmuni0221"}
STC_FILES = {"natrinai": "natrinai", "kuruntokai": "kuruntokai", "ainkurunuru": "aingurunuru",
             "patitruppattu": "paditruppallu", "paripadal": "paripadal", "kalittokai": "kalith-thogai"}


# --------------------------------------------------------------------------------------------
# sangamtamil.com

def load_stc(stc_dir, book):
    path = stc_dir / "data" / "verses" / f"{STC_FILES[book]}.js"
    s = path.read_text(encoding="utf-8")
    i = s.index("=") + 1
    data = json.JSONDecoder().raw_decode(s[i:].lstrip())[0]
    out = {}
    for v in data["verses"]:
        lines = []
        for l in v.get("verse_text", "").split("\n"):
            l = l.strip().replace("*", "")
            if not TAMIL_CHAR.search(l) or l.startswith("("):
                continue
            if re.search(r"[A-Za-z]", l):  # an English note mixed into the verse
                continue
            # the site's own speaker labels and headings (தோழி (தலைவியிடம்):, 'கபிலர், குறிஞ்சி,
            # தோழி தலைவியிடம் சொன்னது'): not verse
            if (l.rstrip().endswith(":") and len(l.split()) <= 8) or \
                    re.search(r"(சொன்னது|கூறியது|சொல்லியது)\.?$", l):
                continue
            lines.append(re.sub(r"\s+", " ", l))
        out[v["verse_number"]] = {"lines": lines, "thinai": STC_THINAI.get((v.get("thinai") or "").lower())}
    return out


# --------------------------------------------------------------------------------------------
# Alignment

def align(P, S, free_ends=False):
    """Align our lines P with the site's lines S (both lists of letter strings).
    Steps: ('match', i, j), ('ours', i, None), ('stc', None, j), ('join', i, j) our i = site j+j+1,
    ('split', i, j) our i+i+1 = site j. With free_ends, site lines before the first and after the
    last of ours cost nothing (for Paripadal, aligned against the whole site text)."""
    nP, nS = len(P), len(S)
    INF = float("inf")
    cost = [[INF] * (nS + 1) for _ in range(nP + 1)]
    back = [[None] * (nS + 1) for _ in range(nP + 1)]
    cost[0][0] = 0.0
    if free_ends:
        for j in range(1, nS + 1):
            cost[0][j] = 0.0
            back[0][j] = ("skip", 0, j - 1)
    GAP = 0.75
    for i in range(nP + 1):
        for j in range(nS + 1):
            c0 = cost[i][j]
            if c0 == INF:
                continue
            steps = []
            if i < nP and j < nS:
                steps.append(("match", 1, 1, 1.0 - sim(P[i], S[j])))
            if i < nP:
                steps.append(("ours", 1, 0, GAP))
            if j < nS:
                steps.append(("stc", 0, 1, GAP if not (free_ends and i == nP) else 0.0))
            if i < nP and j + 1 < nS:
                steps.append(("join", 1, 2, 0.15 + 1.0 - sim(P[i], S[j] + S[j + 1])))
            if i + 1 < nP and j < nS:
                steps.append(("split", 2, 1, 0.15 + 1.0 - sim(P[i] + P[i + 1], S[j])))
            for name, di, dj, c in steps:
                if c0 + c < cost[i + di][j + dj]:
                    cost[i + di][j + dj] = c0 + c
                    back[i + di][j + dj] = (name, i, j)
    out, i, j = [], nP, nS
    while i or j:
        name, pi, pj = back[i][j]
        if name != "skip" and not (free_ends and name == "stc" and pi == nP):
            out.append((name, pi if name != "stc" else None, pj if name != "ours" else None))
        i, j = pi, pj
    return out[::-1]


def eye_skip(p, s1, s2):
    """Our line p begins like site line s1 and ends like the next site line s2, and is
    shorter than the two together: the copyist's eye skipped from one line to the next."""
    k = 8
    return (len(p) < 0.85 * (len(s1) + len(s2)) and len(s1) >= k and len(s2) >= k
            and sim(p[:k], s1[:k]) >= 0.7 and sim(p[-k:], s2[-k:]) >= 0.7
            and sim(p[-k:], s1[-k:]) < 0.7)


def classify(a, b):
    if letters(a) == letters(b):
        return "same"
    if skeleton(a) == skeleton(b):
        return "spelling"
    return "reading"


ODU = re.compile(r"([யள])டு(?=ம்|[^\u0B80-\u0BFF]|$)")


def fix_lost_o(line, stc_line):
    """Restore ொ after ய/ள where the site's line confirms it. Returns (line, [(old, new)])."""
    st = letters(stc_line)
    changes = []
    words = line.split(" ")
    for k, w in enumerate(words):
        lw = letters(w)
        if not lw:
            continue
        cands = []
        for m in re.finditer(r"[யள](?![\u0BBE-\u0BCD\u0BD7])", w):
            for sign in ("ொ", "ோ"):
                cands.append(w[:m.end()] + sign + w[m.end():])
        for c in cands:
            if letters(c) in st and lw not in st:
                changes.append((w, c))
                words[k] = c
                break
        else:
            m = ODU.search(w)
            if m and re.search(m.group(1) + "[ொோ]டு" + ("ம்" if w[m.end():].startswith("ம்") else "")
                               + r"(?![\u0B80-\u0BFF])", stc_line):
                c = w[:m.start()] + m.group(1) + "ொடு" + w[m.end():]
                changes.append((w, c))
                words[k] = c
    return " ".join(words), changes


def junk_word(w):
    w = w.strip("'‘’“”\"(")
    if re.match(r"^[\u0B95-\u0BB9]\u0BCD", w):  # a word cannot begin with a dead consonant
        return True
    if re.search(r"[ஜஷஸஹஶ]", w):  # grantha letters do not occur in Sangam verse
        return True
    for m in re.finditer(r"([\u0B95-\u0BB9])\u0BCD([\u0B95-\u0BB9])\u0BCD([\u0B95-\u0BB9])", w):
        if m.group(1) not in "யரழ":  # three dead consonants in a row: only after ய், ர், ழ்
            return True
    return any(not ("\u0B80" <= ch <= "\u0BFF") and ch not in core.ALLOWED_PUNCT for ch in w) or \
        any("\u0B80" <= ch <= "\u0BFF" and not assigned(ch) for ch in w) or \
        any(ch in VOWEL_SIGNS and (k == 0 or w[k - 1] not in CONSONANTS) and ch != "\u0BD7"
            for k, ch in enumerate(w))


def fix_junk(line, stc_line):
    """Replace words carrying encoding junk by the site's words for the same letters."""
    if not any(junk_word(w) for w in line.split()):
        return line, []
    pw = line.split(" ")
    sw = stc_line.split(" ")
    # letter index -> word index for both lines
    pl, pmap = [], []
    for k, w in enumerate(pw):
        for ch in letters(w):
            pl.append(ch)
            pmap.append(k)
    sl, smap = [], []
    for k, w in enumerate(sw):
        for ch in letters(w):
            sl.append(ch)
            smap.append(k)
    ops = difflib.SequenceMatcher(None, "".join(pl), "".join(sl), autojunk=False).get_opcodes()
    changes = []
    new = list(pw)
    for k, w in enumerate(pw):
        if not junk_word(w):
            continue
        idx = [x for x, wk in enumerate(pmap) if wk == k]
        if not idx:
            new[k] = ""
            changes.append((w, ""))
            continue
        a, b = idx[0], idx[-1] + 1
        js = set()
        for tag, i1, i2, j1, j2 in ops:
            if i2 <= a or i1 >= b:
                if not (tag == "insert" and a <= i1 <= b):
                    continue
            if tag == "equal":
                lo, hi = max(i1, a), min(i2, b)
                js.update(range(j1 + lo - i1, j1 + hi - i1))
            else:
                js.update(range(j1, j2))
        words = sorted({smap[j] for j in js if j < len(smap)})
        if not words:
            continue
        W = set(range(words[0], words[-1] + 1))
        # PM letter index -> site letter index (equal stretches only)
        p2s = {}
        for tag, i1, i2, j1, j2 in ops:
            if tag == "equal":
                for t in range(i2 - i1):
                    p2s[i1 + t] = j1 + t
        lo_k, hi_k = k, k
        for step in (-1, 1):
            kk = k + step
            while 0 <= kk < len(pw) and new[kk] == pw[kk]:
                ix = [x for x, wk in enumerate(pmap) if wk == kk]
                if ix and all(x in p2s and smap[p2s[x]] in W for x in ix):
                    lo_k, hi_k = min(lo_k, kk), max(hi_k, kk)
                    kk += step
                else:
                    break
        rep = " ".join(sw[words[0]:words[-1] + 1])
        old = " ".join(pw[lo_k:hi_k + 1])
        for kk in range(lo_k, hi_k + 1):
            new[kk] = ""
        new[k] = rep
        changes.append((old, rep))
    return " ".join(x for x in new if x), changes


# --------------------------------------------------------------------------------------------
# Build

def build_book(book, text_dir, stc):
    units = PARSERS[book](text_dir)
    lost_o = book in ("natrinai", "paripadal")
    stats = Counter()
    records = []
    stc_used = set()
    stc_all = None
    if book == "paripadal":
        stc_all = []
        for k in sorted(stc):
            stc_all += [(k, l) for l in stc[k]["lines"]]
    for u in units:
        rid = u["id"]
        if book == "paripadal" and u["marks"]:
            drop_extra_lines(u, stc_all)
        tamil = [repair_line(book, rid, i, l) for i, l in enumerate(u["raw"], 1)]
        tamil = [l for l in tamil if l]
        lacunae = []
        dots = [i for i, l in enumerate(tamil, 1) if not TAMIL_CHAR.search(l) and re.fullmatch(r"[.\s…]+", l)]
        if dots and u["marks"] and any(p != n for p, n in u["marks"]):
            shift = lambda p: p - sum(1 for d in dots if d < p)
            if all(shift(p) == n for p, n in u["marks"]):
                for d in dots:
                    lacunae.append(d - 1 - sum(1 for e in dots if e < d))
                tamil = [l for i, l in enumerate(tamil, 1) if i not in dots]
                u["marks"] = [(shift(p), n) for p, n in u["marks"]]
                flag(book, rid, "lacuna", f"{len(dots)} line(s) of dots (lost text) removed; the source's "
                     "line numbers do not count them; the gap is after line(s) "
                     f"{sorted(set(lacunae))} (field `lacunae`)")
        variants, line_sources = [], {}
        site = None
        if book == "paripadal" and u["kind"] in ("poem", "fragment"):
            site = paripadal_window(tamil, stc_all)
        elif u["stc_key"] is not None and u["stc_key"] in stc:
            site = stc[u["stc_key"]]["lines"]
            stc_used.add(u["stc_key"])
        cmp = None
        if site:
            P = [letters(l) for l in tamil]
            S = [letters(l) for l in site]
            steps = align(P, S, free_ends=(book == "paripadal"))
            # a 'join' that is not an eye-skip is one of our lines against one site line, plus a
            # line the site has and we lack
            fixed_steps = []
            for kind, i, j in steps:
                if kind == "join" and book != "paripadal" and not eye_skip(P[i], S[j], S[j + 1]) \
                        and abs(sim(P[i], S[j]) - sim(P[i], S[j + 1])) > 0.3:
                    if sim(P[i], S[j]) >= sim(P[i], S[j + 1]):
                        fixed_steps += [("match", i, j), ("stc", None, j + 1)]
                    else:
                        fixed_steps += [("stc", None, j), ("match", i, j + 1)]
                else:
                    fixed_steps.append((kind, i, j))
            steps = fixed_steps
            out = []
            cmp = Counter()
            k = 0
            while k < len(steps):
                kind, i, j = steps[k]
                if kind == "match":
                    a, b = tamil[i], site[j]
                    c = classify(a, b)
                    if sim(P[i], S[j]) < 0.5:
                        c = "unlike"
                    new = a
                    notes = []
                    if c in ("reading", "spelling") or any(junk_word(w) for w in a.split()):
                        new, ch1 = fix_junk(new, b)
                        if ch1:
                            notes += [f"{x} -> {y}" for x, y in ch1]
                            flag(book, rid, "repaired", "word with encoding junk or a lost first "
                                 "letter replaced by the sangamtamil.com reading", len(out) + 1, "; ".join(notes))
                        if lost_o:
                            new, ch2 = fix_lost_o(new, b)
                            if ch2:
                                n2 = [f"{x} -> {y}" for x, y in ch2]
                                notes += n2
                                flag(book, rid, "repaired", "lost vowel sign ொ restored (the -ஒடு "
                                     "fault), as read by sangamtamil.com", len(out) + 1, "; ".join(n2))
                        c2 = classify(new, b)
                        if new != a:
                            c = c2 if c2 != "same" else "repaired"
                    cmp[c] += 1
                    out.append(new)
                    if c != "same":
                        v = {"line": len(out), "kind": c, "stc": b, "kept": "pm"}
                        if notes:
                            v["kept"] = "pm, repaired from stc"
                            v["pm"] = a
                            v["repairs"] = notes
                        variants.append(v)
                elif kind == "ours":
                    cmp["pm_only"] += 1
                    out.append(tamil[i])
                    variants.append({"line": len(out), "kind": "pm_only", "stc": None, "kept": "pm"})
                elif kind == "stc":
                    # a line the site has and we lack: supply it, unless it faces a line of ours
                    # that the alignment left unmatched (a strongly different line)
                    prev_k = steps[k - 1][0] if k else None
                    next_k = steps[k + 1][0] if k + 1 < len(steps) else None
                    near = "".join(P[x] for x in (steps[k - 1][1] if k else None,
                                                   steps[k + 1][1] if k + 1 < len(steps) else None)
                                   if x is not None)
                    if near and S[j] and (S[j] in near or sim(S[j], near) > 0.9
                                          or (len(skeleton(S[j])) >= 3 and skeleton(S[j]) in skeleton(near))):
                        # the site breaks one of our lines in two: not a missing line
                        cmp["line_break"] += 1
                        variants.append({"line": len(out) + 0.5, "kind": "line_break", "stc": site[j],
                                         "kept": "pm"})
                    elif book == "paripadal" or prev_k == "ours" or next_k == "ours":
                        cmp["stc_only"] += 1
                        if book != "paripadal":
                            variants.append({"line": len(out) + 0.5, "kind": "stc_only", "stc": site[j],
                                             "kept": "not supplied (faces an unmatched line of ours)"})
                    else:
                        cmp["supplied"] += 1
                        out.append(site[j])
                        line_sources[len(out)] = "sangamtamil.com"
                        variants.append({"line": len(out), "kind": "supplied", "stc": site[j],
                                         "kept": "stc"})
                        flag(book, rid, "supplied", "line missing from the base text; supplied from "
                             "sangamtamil.com", len(out), site[j])
                elif kind == "join" and sim(P[i], S[j] + S[j + 1]) < 0.85 and book != "paripadal" \
                        and eye_skip(P[i], S[j], S[j + 1]):
                    # our one line holds the start of one line and the end of the next: an
                    # eye-skip; the site's two lines are taken
                    cmp["supplied"] += 1
                    out.append(site[j])
                    line_sources[len(out)] = "sangamtamil.com"
                    out.append(site[j + 1])
                    line_sources[len(out)] = "sangamtamil.com"
                    variants.append({"line": len(out) - 1, "kind": "eye_skip", "pm": tamil[i],
                                     "stc": site[j] + " / " + site[j + 1], "kept": "stc"})
                    flag(book, rid, "supplied", "eye-skip: our line joins the start of one line to the "
                         "end of the next; the two lines are taken from sangamtamil.com", len(out) - 1,
                         f"{tamil[i]} -> {site[j]} / {site[j + 1]}")
                elif kind == "join":
                    cmp["line_break"] += 1
                    out.append(tamil[i])
                    variants.append({"line": len(out), "kind": "line_break",
                                     "stc": site[j] + " / " + site[j + 1], "kept": "pm"})
                elif kind == "split":
                    cmp["line_break"] += 1
                    out.append(tamil[i])
                    out.append(tamil[i + 1])
                    variants.append({"line": len(out) - 1, "kind": "line_break",
                                     "stc": site[j], "kept": "pm"})
                k += 1
            tamil = out
            stats.update(cmp)
            if cmp["pm_only"]:
                pm_only = [v["line"] for v in variants if v["kind"] == "pm_only"]
                flag(book, rid, "not_in_stc", f"line(s) {pm_only} not in sangamtamil.com", pm_only[0])
            if cmp["unlike"]:
                for v in variants:
                    if v["kind"] == "unlike":
                        flag(book, rid, "variant", "line differs strongly from sangamtamil.com "
                             f"({v['stc']!r}); ours kept", v["line"], tamil[v["line"] - 1])
        elif u["kind"] == "poem":
            flag(book, rid, "no_stc", "poem not in sangamtamil.com")
        # lines that still hold a dropped vowel sign (the base text has no யொ or ளொ at all):
        # restored by rule; flagged, since no site line confirms them
        if lost_o:
            for i, l in enumerate(tamil, 1):
                if ODU.search(l) and line_sources.get(str(i)) is None and line_sources.get(i) is None:
                    new = ODU.sub(lambda m: m.group(1) + "ொடு", l)
                    flag(book, rid, "vowel_sign_o", "யடு/ளடு at a word end restored to யொடு/ளொடு "
                         "by rule (the base text never writes யொ or ளொ); sangamtamil.com does not "
                         "confirm it here", i, f"{l} -> {new}")
                    tamil[i - 1] = new
                    variants.append({"line": i, "kind": "rule", "stc": None, "kept": "pm, repaired by rule",
                                     "pm": l})
        # junk left where no site line could be compared: removed, and flagged
        for i, l in enumerate(tamil, 1):
            new = "".join(ch for ch in l if not ("\u0B80" <= ch <= "\u0BFF" and not assigned(ch))
                          and not ("A" <= ch <= "Z" or "a" <= ch <= "z"))
            new = re.sub(r"\s+", " ", new).strip()
            if new != l:
                flag(book, rid, "repaired", "stray character (unassigned code point or Latin letter) "
                     "removed; no sangamtamil.com line to compare", i, f"{l} -> {new}")
                tamil[i - 1] = new
        # checks
        for i, l in enumerate(tamil, 1):
            probs = sorted(set(core.unicode_problems(l)))
            if probs:
                flag(book, rid, "unicode", "; ".join(probs), i, l)
            if not TAMIL_CHAR.search(l):
                flag(book, rid, "empty_line", "line has no Tamil letters", i, l)
            if re.search(r"(?:^|[\s'‘“(])[\u0B95-\u0BB9]\u0BCD", l):
                flag(book, rid, "spelling", "a word begins with a dead consonant (letter lost?)", i, l)
            if re.search(r"\.\.|- -", l):
                flag(book, rid, "lacuna", "the line has a gap (dots or dashes in the source)", i, l)
        for i in range(1, len(tamil)):
            if letters(tamil[i]) == letters(tamil[i - 1]):
                flag(book, rid, "duplicate_line", "same line printed twice in a row", i + 1, tamil[i])
        lo, hi = LINE_RANGE[book]
        if u["kind"] in ("poem",) and not lo <= len(tamil) <= hi:
            flag(book, rid, "line_count", f"{len(tamil)} lines; the anthology's poems have {lo}-{hi}")
        if book == "natrinai" and u["marks"] == [(len(u["raw"]), u["number"])]:
            u["marks"] = []  # the poem's own number printed after its last line
        if u["marks"]:
            bad = [(p, n) for p, n in u["marks"] if p != n]
            last = u["marks"][-1]
            if bad and not line_sources:
                flag(book, rid, "lineation", f"printed line number {bad[0][1]} stands on line {bad[0][0]}"
                     + (f" ({len(bad)} numbers off)" if len(bad) > 1 else ""), bad[0][0])
            if last[0] == len(u["raw"]) and last[1] != len(tamil):
                flag(book, rid, "line_count", f"{len(tamil)} lines, but the source numbers its last line "
                     f"{last[1]}")
        thinai = u["thinai"]
        if site and u["stc_key"] in stc and stc[u["stc_key"]]["thinai"] and thinai and \
                stc[u["stc_key"]]["thinai"] != thinai and u["kind"] == "poem":
            flag(book, rid, "thinai", f"sangamtamil.com gives {stc[u['stc_key']]['thinai']!r}; the base "
                 f"text gives {thinai!r} (base kept)")
        if u["kind"] == "poem" and not u["poet"] and not u["note"]:
            flag(book, rid, "colophon", "no poet in the base text")
        rec = {
            "id": rid, "number": u["number"], "section": u["section"], "kind": u["kind"],
            "title": u["title"], "poet": u["poet"], "patron": u["patron"], "thinai": thinai,
            "thurai": u["thurai"], "note": u["note"],
            "colophon_raw": " | ".join(c for c in u["colophon"] if c) or None,
            "tamil": tamil, "line_count": len(tamil),
            "tamil_source": SOURCES[book],
        }
        if lacunae:
            u["lacunae"] = sorted(set(lacunae))
        for extra in ("decade", "decade_title", "fragment", "metre", "vannam", "music", "pan",
                      "poem_names", "lacunae", "dropped_headings", "dropped_glosses"):
            if u.get(extra) is not None:
                rec[extra] = u[extra]
        rec["line_sources"] = {str(k): v for k, v in line_sources.items()} or None
        rec["stc_compared"] = bool(site)
        rec["variants"] = variants
        rec["rights"] = RIGHTS
        records.append(rec)
    if book in ("natrinai", "kuruntokai", "ainkurunuru", "kalittokai"):
        nums = [r["number"] for r in records]
        if nums != sorted(nums):
            out_of_order = [n for a, n in zip(nums, nums[1:]) if n < a]
            flag(book, None, "numbering", f"the base text prints poems out of order (around "
                 f"{out_of_order}); records are written in numerical order")
            records.sort(key=lambda r: r["number"])
    if book != "paripadal":
        for k in sorted(set(stc) - stc_used):
            flag(book, f"{book}:{k}", "stc_only_poem", "sangamtamil.com has this poem; the base text "
                 "does not (not supplied)")
    cross_duplicates(book, records)
    return records, stats


# The endings of the e-text's modern Paripadal headings (prose nouns: '... கூறுதல்', '... வகை',
# '... காட்சி'); used only inside a stretch that the line numbers show to hold surplus lines.
HEADING_END = re.compile(r"(?:தல்|கூறல்|செயல்|வகை|காட்சி|சிறப்பு|சிறப்புக்கள்|நிகழ்ச்சி|அழகு|கூற்று|"
                         r"எனல்|முதலியன|விளங்கியமை|கண்டவை|வழி|பெருமை|தோற்றம்|பொருள்கள்|இன்மை|"
                         r"ஆடல்|மொழிகள்|விலகலும்|கற்பம்|நிலைகள்|பரங்குன்றம்|கூறியது|அடையாதோரும்|"
                         r"வெளிப்பாடும்|ஒடுக்கமும்|பெயரியல்புகள்|வியூகம்|வசை|பாட்டு)\s*$")


def drop_extra_lines(u, stc_all):
    """Paripadal: the e-text puts modern headings inside the songs, some run into the verse
    blocks. Its line numbers (every fifth line) say how many verse lines each stretch has, so in
    a stretch with too many lines the surplus lines that look least like any line of the site's
    text (and carry no number) are the headings."""
    site = [letters(l) for _, l in stc_all]
    g_site = set()
    for l in site:
        g_site |= {l[i:i + 3] for i in range(len(l) - 2)}

    window = [letters(l) for l in (paripadal_window(u["raw"], stc_all) or [])]

    def verse_likeness(line):
        g = grams(line)
        score = len(g & g_site) / max(1, len(g))
        lt = letters(line)
        if window and max(sim(lt, w) for w in window) >= 0.6:  # the site has this line
            score += 2.0
        if re.search(r"[,;:!?.\-–—‘’'\"]\s*$", line):  # headings carry no verse punctuation
            score += 2.0
        if re.search(r"[கசதப]\u0BCD\s*$", line):  # a doubled stop at the end runs on to the next line
            score += 2.0
        if HEADING_END.search(line) and len(line.split()) >= 2:
            score -= 3.0
        return score

    marked = {p for p, _ in u["marks"]}
    drop = set()
    prev_p, prev_n = 0, 0
    for p, n in u["marks"]:
        surplus = (p - prev_p) - (n - prev_n)
        if surplus > 0:
            cands = [k for k in range(prev_p + 1, p) if k not in marked]
            cands = [k for k in cands if verse_likeness(u["raw"][k - 1]) < 0.5]
            cands.sort(key=lambda k: verse_likeness(u["raw"][k - 1]))
            drop.update(cands[:surplus])
        prev_p, prev_n = p, n
    if not drop:
        return
    u.setdefault("dropped_headings", [])
    u["dropped_headings"] += [u["raw"][k - 1] for k in sorted(drop)]
    for k in sorted(drop):
        flag("paripadal", u["id"], "heading_dropped", "a line taken for a modern heading (no line "
             "number, not in sangamtamil.com, and the source's line numbers leave no room for it); "
             "check by eye", k, u["raw"][k - 1])
    keep = [k for k in range(1, len(u["raw"]) + 1) if k not in drop]
    newpos = {k: i for i, k in enumerate(keep, 1)}
    u["raw"] = [u["raw"][k - 1] for k in keep]
    u["marks"] = [(newpos[p], n) for p, n in u["marks"] if p in newpos]


def grams(text):
    t = letters(text)
    return {t[i:i + 3] for i in range(len(t) - 2)}


def paripadal_window(tamil, stc_all):
    """The run of site lines that holds this song: the site lines that share most of their
    letter trigrams with the song, widened by a few lines on each side."""
    g = grams(" ".join(tamil))
    hit = [k for k, (_, l) in enumerate(stc_all)
           if len(letters(l)) >= 6 and len(grams(l) & g) >= 0.6 * max(1, len(grams(l)))]
    if len(hit) < max(1, len(tamil) // 4):
        return None
    lo, hi = max(0, hit[0] - 3), min(len(stc_all), hit[-1] + 4)
    if hi - lo > 2 * len(tamil) + 20:  # scattered hits: keep the densest stretch
        best, bi = 0, 0
        for k in range(len(hit)):
            n = sum(1 for h in hit[k:] if h - hit[k] <= len(tamil) + 10)
            if n > best:
                best, bi = n, k
        lo = max(0, hit[bi] - 3)
        hi = min(len(stc_all), hit[bi] + len(tamil) + 14)
    return [l for _, l in stc_all[lo:hi]]


def cross_duplicates(book, records):
    seen = defaultdict(list)
    for r in records:
        for i, l in enumerate(r["tamil"], 1):
            k = letters(l)
            if len(k) >= 14:
                seen[k].append((r["id"], i, l))
    for k, places in seen.items():
        ids = {p[0] for p in places}
        if 1 < len(ids) <= 3:
            flag(book, places[0][0], "repeated_line", "the same line appears in "
                 + ", ".join(f"{p[0]} line {p[1]}" for p in places), places[0][1], places[0][2])


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as out:
        for r in records:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")


STANDARD = {
    "natrinai": "400 poems and the invocation; 234 is lost (399 + 1)",
    "kuruntokai": "401 poems and the invocation (401 + 1)",
    "ainkurunuru": "500 poems; 129 and 130 are lost (498)",
    "patitruppattu": "decades 2-9 survive: 80 poems (11-90) and 8 patikams; decades 1 and 10 lost",
    "paripadal": "22 of the 70 songs survive, with fragments (Paripadal thirattu)",
    "kalittokai": "150 poems, the first being the invocation",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text-dir", type=Path, default=ROOT / "data" / "text")
    ap.add_argument("--stc-dir", type=Path, default=STC_DEFAULT)
    ap.add_argument("--out-dir", type=Path, default=ROOT / "kg" / "core")
    ap.add_argument("--books", default=",".join(BOOKS))
    args = ap.parse_args()
    if not (args.stc_dir / "data" / "verses").is_dir():
        raise SystemExit(f"sangamtamil.com crawl not found at {args.stc_dir}; pass --stc-dir")
    books = args.books.split(",")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    summary = {}
    for book in books:
        stc = load_stc(args.stc_dir, book)
        records, stats = build_book(book, args.text_dir, stc)
        write_jsonl(args.out_dir / f"{book}.jsonl", records)
        kinds = Counter(r["kind"] for r in records)
        summary[book] = (kinds, stats, sum(r["line_count"] for r in records))
    fpath = args.out_dir / "sangam_text_flags.jsonl"
    keep = []
    if fpath.exists():
        keep = [l for l in fpath.read_text(encoding="utf-8").splitlines()
                if l.strip() and json.loads(l)["book"] not in books]
    with open(fpath, "w", encoding="utf-8") as out:
        for l in keep:
            out.write(l + "\n")
        for f in flags:
            out.write(json.dumps(f, ensure_ascii=False) + "\n")
    for book, (kinds, stats, nlines) in summary.items():
        print(f"{book}: {dict(kinds)}, {nlines} lines; standard: {STANDARD[book]}")
        print("   vs sangamtamil.com:", dict(stats))
    print("flags:", dict(Counter((f["book"], f["kind"]) for f in flags)))


if __name__ == "__main__":
    main()
