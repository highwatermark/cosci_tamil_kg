#!/usr/bin/env python3
"""Build the original Tamil text of the five great epics and the five minor epics.

Writes (kg/core/):
  silappathikaram.jsonl         the patikam, the 30 kaathais and the closing pieces, one record each, whole
  silappathikaram_units.jsonl   reading units: akaval split at sense breaks (10-25 lines), each
                                embedded song (vari, kuravai, venba) as its own unit
  manimekalai.jsonl             the patikam and the 30 kaathais, one record each, whole
  manimekalai_units.jsonl       reading units of 10-25 lines at sense breaks
  civaka_cintamani.jsonl        one record per verse (1-3145), with ilampakam and padalam
  valayapathi.jsonl             the surviving verses (72), with the work that quotes each one
  kundalakesi.jsonl             the surviving verses (19)
  soolamani.jsonl, neelakesi.jsonl, naga_kumara_kaviyam.jsonl, udayana_kumara_kaviyam.jsonl,
  yasodhara_kaviyam.jsonl       one record per verse, with section (sarukkam or kandam)
  sangam_text_flags.jsonl       flags for these books are appended (earlier flags for them replaced)

Reads only Project Madurai e-texts already mirrored in data/text/:
  pmuni0046, pmuni0111_01, pmuni0111_02   Silappathikaram, the three kandams (text alone)
  pmuni0141                               Manimekalai (text alone)
  pmuni0664_01/_02, pmuni0670_01/_02, pmuni0672_01/_02/_03
                                          Civaka Cintamani with P. V. Somasundaranar's commentary
  pmuni0062                               Valayapathi, the collected fragments
  pmuni0507                               Kundalakesi, the collected fragments, with commentary
  pmuni0035_01 (verses 1-238, numbered), pmuni0035_02 (verses 1-826, unnumbered),
  pmuni0602_01, pmuni0602_02 (827-2130)   Soolamani
  pmuni0538                               Neelakesi
  pmuni0601                               Naga Kumara Kaviyam, with a modern prose rendering
  pmuni0597                               Udayana Kumara Kaviyam, with commentary
  pmuni0508_01, pmuni0508_02              Yasodhara Kaviyam, with Avvai Duraisamy Pillai's commentary

Copyright: only the verse lines are kept, with traditional facts (book, section, number, the rubric
of an embedded song). Commentary, prose renderings, modern headings, prefaces and translations are
never copied. Modern editorial headings over verses are not kept as text; where they are the only
padalam names a book has, they are stored as `heading` and marked as the editor's.

Reading units (silappathikaram_units.jsonl, manimekalai_units.jsonl) follow the Pattupattu rule in
scripts/build_sangam_core.py exactly (the same score_break and split_units are imported): units of
10 to 25 lines, greedy from the top, each end scored by how strongly the line closes a sentence,
choosing the end that maximises 10 * score - |length - 16|, never leaving fewer than 10 lines, a
remainder of 25 lines or fewer taken whole. A unit never crosses a block of the source (a change of
metre or a rubric such as வேறு, வெண்பா, உரைப்பாட்டு மடை). Embedded songs are not split: every
numbered song of a vari or kuravai, and every closing venba, is its own unit whatever its length
(a song longer than 25 lines is split by the same rule). Unit ids are <book>:<kaathai>:<start>-<end>
with the record's own line positions (1-based, inclusive).

Run: python3 -I scripts/build_epics_core.py [--text-dir DIR] [--out-dir DIR]
"""
import argparse
import importlib.util
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location("build_sangam_core", ROOT / "scripts" / "build_sangam_core.py")
_core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_core)
score_break = _core.score_break
split_units = _core.split_units
unicode_problems = _core.unicode_problems

TAMIL_CHAR = re.compile(r"[\u0B80-\u0BFF]")
NON_TAMIL = re.compile(r"[^\u0B80-\u0BFF]")
RIGHTS = {"tamil": "public_domain"}
EPIC_BOOKS = ("silappathikaram", "manimekalai", "civaka_cintamani", "valayapathi", "kundalakesi",
              "soolamani", "neelakesi", "naga_kumara_kaviyam", "udayana_kumara_kaviyam",
              "yasodhara_kaviyam")

flags = []


def flag(book, rid, kind, detail, line=None, text=None):
    rec = {"book": book, "id": rid, "kind": kind, "line": line, "detail": detail}
    if text is not None:
        rec["text"] = text
    flags.append(rec)


def body(text_dir, name):
    text = (text_dir / f"{name}.txt").read_text(encoding="utf-8")
    text = text.split("=== BODY ===", 1)[1].split("=== FOOTER ===", 1)[0]
    # A DEL character (U+007F) after a character is a typed backspace: '140\x7f5' is 145.
    return re.sub(r"[^\n]\x7f", "", text)


# Character repairs; each one is written to the flags file.
# U+0BA1 (஡) is unassigned: in these e-texts it is a leftover of the TSCII long-u sign, so
# 'து஡ணகத்து' is தூணகத்து and 'மூது஡ர்' is மூதூர். Other TSCII leftovers: '·' for ஃ, '¦’' + consonant
# for consonant + ெ, U+0BA2 (஢) after a consonant for the vowel sign ி (ந்஢தியது = நிதியது).
REPAIRS = (
    (re.compile(r"([\u0B95-\u0BB9])\u0BC1\u0BA1"), "\\1\u0BC2", "TSCII leftover ு + U+0BA1 read as ூ"),
    (re.compile(r"([\u0B95-\u0BB9])\u0BBE\u0BA1"), "\\1\u0BBE", "TSCII leftover U+0BA1 after ா removed"),
    (re.compile(r"([\u0B95-\u0BB9])\u0BCC(?=[\u0BBE-\u0BCD])"), "\\1\u0BC6\u0BB3",
     "ௌ before a vowel sign read as ெள (old fonts drew both alike: தௌிவு = தெளிவு)"),
    (re.compile(r"([\u0BBE-\u0BCC])\1"), "\\1", "doubled vowel sign reduced to one"),
    (re.compile(r"(?<=[\u0B95-\u0BB9]) (?=[\u0BBE-\u0BCD])"), "",
     "stray space before a vowel sign removed (வாய ிற் = வாயிற்)"),
    (re.compile(r"^>\s*"), "", "leftover HTML quote mark '>' at the start of the line removed"),
    (re.compile(r"\s*`\s*"), " ", "stray backtick removed"),
    (re.compile(r"([\u0B95-\u0BB9])\u0BCB\u0BCD"), "\\1\u0BC7\u0BB0\u0BCD",
     "ோ் read as ேர் (a TSCII conversion slip: the glyph of ர் was taken for ா், e.g. திண்டோ் = திண்டேர்)"),
    (re.compile(r"([\u0B95-\u0BB9])\u0BCA\u0BCD"), "\\1\u0BC6\u0BB0\u0BCD",
     "ொ் read as ெர் (the same TSCII slip)"),
    (re.compile(r"([\u0BBE-\u0BC2\u0BC6-\u0BC8])\u0BCD"), "\\1", "pulli after a vowel sign removed"),
    (re.compile(r"([\u0B95-\u0BB9])[\u0BCD\u0BBF\u0BC0]?\u0BA2"), "\\1\u0BBF",
     "TSCII leftover U+0BA2 read as the vowel sign ி (ந்஢தியது = நிதியது, கிளீ஢யும் = கிளியும்)"),
    (re.compile(r"([\u0B95-\u0BB9])\u0BCB¢"), "\\1\u0BC7\u0BB0\u0BBF",
     "TSCII leftover ோ¢ read as ேரி (போ¢ன்ப = பேரின்ப)"),
    (re.compile(r"([\u0B95-\u0BB9])\u0BCD?¢"), "\\1\u0BBF", "TSCII leftover ¢ read as the vowel sign ி"),
    (re.compile(r"¡;"), "ர்", "TSCII leftover '¡;' read as ர் (கண்டீ¡; = கண்டீர்)"),
    (re.compile(r"([\u0B95-\u0BB9])\s?¡(?!;)"), "\\1\u0BBE", "TSCII leftover ¡ read as ா (த¡னு = தானு)"),
    (re.compile(r"b([\u0B95-\u0BB9])"), "\\1\u0BC6",
     "TSCII leftover 'b' before a consonant read as ெ after it (bனன்றல் = னென்றல்)"),
    (re.compile(r"·"), "ஃ", "'·' is the old encoding of ஃ"),
    (re.compile(r"\u2022"), "ஃ", "'•' is the old encoding of ஃ"),
    (re.compile(r"¦’([\u0B95-\u0BB9])"), "\\1\u0BC6", "TSCII leftover '¦’' + consonant = consonant + ெ"),
    (re.compile(r"[\u200B-\u200D\uFEFF]"), "", "zero-width character removed"),
    (re.compile(r"\u0BCD\u0BCD+"), "\u0BCD", "doubled pulli reduced to one"),
    (re.compile(r"(?<=[\u0B80-\u0BFF]) (?=[\u0B95-\u0BB9]\u0BCD(?:\s|$|[,.;:!?]))"), "",
     "stray space before a dead consonant removed"),
)


def repair(book, rid, n, line):
    for pat, rep, why in REPAIRS:
        new = pat.sub(rep, line)
        if new != line:
            flag(book, rid, "repaired", why, n, f"{line} -> {new}")
            line = new
    return line


def tidy(line):
    line = unicodedata.normalize("NFC", line).replace("\t", " ")
    line = re.sub(r"\s+", " ", line).strip()
    line = re.sub(r"\s*-{3,}\s*$", "", line)  # a rule printed at the end of the last line
    return line.strip()


def check_lines(book, rid, lines, refrain=False):
    for i, l in enumerate(lines, 1):
        for p in unicode_problems(l):
            flag(book, rid, "unicode", p, i, l)
        if not TAMIL_CHAR.search(l):
            flag(book, rid, "empty_line", "line has no Tamil letters", i, l)
        if re.search(r"(?:^|[\s'‘“(])[\u0B95-\u0BB9]\u0BCD(?=\s|$)", l):
            flag(book, rid, "spelling", "a lone dead consonant stands as a word (letter lost?)", i, l)
        if re.search(r"(?:^|\s)[\u0BBE-\u0BCD]", l):
            flag(book, rid, "lost_vowel_sign", "a vowel sign stands at the start of a word "
                 "(its consonant lost)", i, l)
        if re.search(r"(?:^|\s)(?:கை|பொய்|பொருள்?|துடி|வடி)[யள]?டு(?:\s|$)", l):
            flag(book, rid, "lost_vowel_sign", "word ending -யடு/-ளடு: possibly -யொடு/-ளொடு with the "
                 "vowel sign ொ lost (the Project Madurai fault found in the Purananuru); not repaired, "
                 "since அடு 'to slay' ends the same way", i, l)
    for i in range(1, len(lines)):
        if lines[i] == lines[i - 1] and len(NON_TAMIL.sub("", lines[i])) > 6:
            if refrain:
                flag(book, rid, "refrain", "same line twice in a row: a refrain of this song form "
                     "(checked against the source; kept)", i + 1, lines[i])
            else:
                flag(book, rid, "duplicate_line", "same line printed twice in a row", i + 1, lines[i])


def letters(text):
    return NON_TAMIL.sub("", text)


def grams(text):
    t = letters(text)
    return {t[i:i + 3] for i in range(len(t) - 2)}


def similarity(a, b):
    a, b = grams(a), grams(b)
    return len(a & b) / (len(a | b) or 1)


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as out:
        for r in records:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")


TRAIL_NUM = re.compile(r"^(.*?[\u0B80-\u0BFF.,;:!?'\"’”)\]0-9-])\s+(\d{1,4})\s*\.?\s*$|"
                       r"^(.*?[\u0B80-\u0BFF.,;:!?'\"’”)\]-])(\d{1,4})\s*\.?\s*$")


def split_num(line):
    """'... தழீஇப் 10' -> ('... தழீஇப்', 10)."""
    line = re.sub(r"\s*-{3,}\s*$", "", line)
    m = TRAIL_NUM.match(line)
    if not m:
        return line, None
    text, num = (m.group(1), m.group(2)) if m.group(1) is not None else (m.group(3), m.group(4))
    if not TAMIL_CHAR.search(text):
        return line, None
    return text.rstrip(), int(num)


# --------------------------------------------------------------------------------------------
# Silappathikaram

SIL_FILES = ("pmuni0046", "pmuni0111_01", "pmuni0111_02")
KANDAMS = (("புகார்க் காண்டம்", 1, 10), ("மதுரைக் காண்டம்", 11, 23), ("வஞ்சிக் காண்டம்", 24, 30))
# Rubrics printed between the lines: they name the metre or the kind of song that follows, or say
# who speaks. They are kept as block labels, never as verse lines.
SIL_LABELS = {
    "வேறு", "வெண்பா", "நேரிசை வெண்பா", "பாட்டுமடை", "பாட்டு மடை", "உரைப்பாட்டு மடை",
    "உரைப்பாட்டுமடை", "உரைப் பாட்டு மடை", "கருப்பம்", "கொளு", "கட்டு", "எடுத்துக் காட்டு",
    "கூத்துள் படுதல்", "பாட்டு", "ஒன்றன் பகுதி", "ஆடுநர்ப் புகழ்தல்", "உள்வரி வாழ்த்து",
    "முன்னிலைப் பரவல்", "படர்க்கைப் பரவல்", "கட்டுரை", "கொளுச் சொல்", "வாழ்த்து", "அம்மானை வரி",
    "கந்துக வரி", "ஊசல் வரி", "வள்ளைப் பாட்டு", "தேவந்தி ஐயையைக் காட்டி யரற்றியது", "பதிகம்",
}
SIL_LABEL_RE = re.compile(r"^(?:\(.*\)|வேறு\s*\(.*\)|\S+\s*(?:சொல்|அரற்று|யரற்று|கூற்று)|"
                          r"(?:\d\.\s*)?(?:புகார்|மதுரை|வஞ்சி)க் காண்டம்)$")
# The songs of these kaathais carry song numbers instead of line numbers. In the kaathais of
# pmuni0111_01 (12, 17 and the venbas of 20) the number stands on the first line of the song;
# elsewhere on its last line.
SIL_SONG_HEAD = {12, 17, 20}
SIL_SONG_KAATHAIS = (7, 12, 17, 24, 29)
SIL_SHORT = {
    0: "patikam", 1: "mangala_vazhthu_padal", 2: "manaiyaram_paduththa_kaathai",
    3: "arangetru_kaathai", 4: "anthimalai_sirappucey_kaathai", 5: "indira_vizhavoor_eduththa_kaathai",
    6: "kadalaadu_kaathai", 7: "kaanal_vari", 8: "venil_kaathai", 9: "kanaaththiram_uraiththa_kaathai",
    10: "naadukaan_kaathai", 11: "kaadukaan_kaathai", 12: "vettuva_vari",
    13: "puranjeri_iruththa_kaathai", 14: "oorkaan_kaathai", 15: "adaikkala_kaathai",
    16: "kolaikkala_kaathai", 17: "aaychiyar_kuravai", 18: "thunba_maalai", 19: "oorsoozh_vari",
    20: "vazhakkurai_kaathai", 21: "vanjina_maalai", 22: "azharpadu_kaathai", 23: "katturai_kaathai",
    24: "kunrak_kuravai", 25: "kaatchik_kaathai", 26: "kaalkot_kaathai", 27: "neerppadaik_kaathai",
    28: "nadukar_kaathai", 29: "vaazhththuk_kaathai", 30: "varantharu_kaathai",
}


def is_label(s, labels=SIL_LABELS, label_re=SIL_LABEL_RE):
    t = s.strip().rstrip(".").strip()
    return t in labels or bool(label_re.match(t))


def sil_pieces(text_dir):
    """Cut the three files into pieces: patikam, kaathais 1-30, the kandam katturais and the
    nool katturai. Each piece is a list of raw items ('blank'|'label'|'line'|'note', text)."""
    pieces, cur = [], None
    expected = 1
    for name in SIL_FILES:
        lines = body(text_dir, name).split("\n")
        cur = None
        note = None
        for i, raw in enumerate(lines):
            s = raw.strip()
            s = s.replace("< br>", "\n").replace("<br>", "\n")
            if note is not None:
                note.append(s)
                if "]" in s:
                    cur["items"].append(("note", " ".join(note)))
                    note = None
                continue
            m = re.match(r"^(?:###\s*)?(\d{1,2})\.\s*(.+)$", s)
            if m and int(m.group(1)) == expected and (s.startswith("###") or expected == 1) \
                    and not (expected == 1 and cur is None and "காண்டம்" in m.group(2)):
                cur = {"n": expected, "title": m.group(2).strip(), "source": name, "items": []}
                pieces.append(cur)
                expected += 1
                continue
            if s == "பதிகம்" and not pieces:
                cur = {"n": 0, "title": "பதிகம்", "source": name, "items": []}
                pieces.append(cur)
                continue
            if s.startswith("###") and ("முற்றிற்று" in s or "முற்றும்" in s):
                cur = None
                continue
            if s == "### நூற் கட்டுரை":
                cur = {"n": "nool_katturai", "title": "நூற் கட்டுரை", "source": name, "items": []}
                pieces.append(cur)
                continue
            if s.lstrip("#( ").rstrip(") ").strip() == "கட்டுரை" and cur is not None:
                ahead = lines[i + 1:i + 30]
                if any(re.search(r"காண்ட(?:ம்)?\s*முற்றிற்று\.?\s*\d", a) for a in ahead):
                    kandam = next(k for k, lo, hi in KANDAMS if lo <= cur["n"] <= hi) \
                        if isinstance(cur["n"], int) else None
                    cur = {"n": "katturai", "kandam": kandam, "title": "கட்டுரை", "source": name,
                           "items": []}
                    pieces.append(cur)
                    continue
            if cur is None or s.startswith("###"):
                continue
            if s.startswith("["):
                note = [s]
                if "]" in s:
                    cur["items"].append(("note", s))
                    note = None
                continue
            if not s or re.fullmatch(r"-{3,}", s):
                cur["items"].append(("blank", ""))
                continue
            for part in s.split("\n"):
                part = part.strip()
                if not part:
                    continue
                if part != s:
                    flag("silappathikaram", f"silappathikaram:{cur['n']}", "repaired",
                         "HTML line break '< br>' left in the "
                         "e-text; the text around it taken as separate lines", None, s)
                if is_label(part):
                    cur["items"].append(("label", part.rstrip(".").strip()))
                else:
                    cur["items"].append(("line", part))
    return pieces


# Short lines that the e-text prints on two lines but that its own line numbers (and the standard
# lineation) count as one line: joined, so that the printed numbers fall on the right lines.
HALF_LINES = {
    ("silappathikaram", 1): (("முரசுஇயம்பின, முருகுஅதிர்ந்தன,", "முறைஎழுந்தன பணிலம்,வெண்குடை"),
                             ("அரசுஎழுந்ததொர் படிஎழுந்தன,", "அகலுள்மங்கல அணிஎழுந்தது.")),
}


def join_half_lines(book, rid, key, items):
    for a, b in HALF_LINES.get(key, ()):
        for i in range(len(items) - 1):
            if items[i] == ("line", a) and items[i + 1] == ("line", b):
                items[i:i + 2] = [("line", a + " " + b)]
                flag(book, rid, "repaired", f"joined '{a}' and '{b}' into one line, as the printed "
                     "line numbers count them", None, a + " " + b)
                break
        else:
            flag(book, rid, "lineation", f"half-lines {a!r} / {b!r} not found; nothing joined")
    return items


def sil_piece_record(p, book="silappathikaram"):
    n = p["n"]
    if isinstance(n, int):
        p["items"] = join_half_lines(book, f"{book}:{n}", (book, n), p["items"])
    if n == "katturai":
        short = {"புகார்க் காண்டம்": "pukar", "மதுரைக் காண்டம்": "madurai",
                 "வஞ்சிக் காண்டம்": "vanchi"}[p["kandam"]] + "_kandam_katturai"
        rid, kind, kandam = f"{book}:{short}", "kandam_katturai", p["kandam"]
        title = f"{p['kandam']} கட்டுரை"
    elif n == "nool_katturai":
        rid, kind, kandam, short, title = f"{book}:nool_katturai", "nool_katturai", None, \
            "nool_katturai", "நூற் கட்டுரை"
    else:
        short = SIL_SHORT[n]
        rid = f"{book}:{n}"
        kind = "patikam" if n == 0 else "kaathai"
        kandam = next((k for k, lo, hi in KANDAMS if lo <= n <= hi), None)
        title = re.sub(r"\s+", " ", p["title"])
    tamil, para_start, printed, blocks, songs, notes = [], [], [], [], [], []
    label, block_start, after_break = None, 1, True
    pending_labels = []
    last_song, song_open = 0, None
    head = n in SIL_SONG_HEAD

    def close_block():
        if len(tamil) >= block_start:
            blocks.append({"label": " / ".join(pending_labels) or None, "start": block_start,
                           "end": len(tamil)})

    for kind_i, text in p["items"]:
        if kind_i == "blank":
            after_break = True
            continue
        if kind_i == "note":
            notes.append(text)
            continue
        if kind_i == "label":
            if pending_labels and len(tamil) < block_start:
                pending_labels.append(text)
            else:
                close_block()
                if head and song_open is not None:
                    songs[-1]["end"] = len(tamil)
                    song_open = None
                pending_labels = [text]
                block_start = len(tamil) + 1
            after_break = True
            continue
        line, num = split_num(text)
        line = tidy(line)
        if not line:
            continue
        line = repair(book, rid, len(tamil) + 1, line)
        tamil.append(line)
        para_start.append(after_break)
        after_break = False
        pos = len(tamil)
        if num is None:
            continue
        is_line_no = abs(num - pos) <= 2 and (num % 5 == 0 or num >= pos - 2) and not songs
        if not is_line_no and n in SIL_SONG_KAATHAIS + (20,) and num != last_song + 1 and num != 1 \
                and songs:
            flag(book, rid, "numbering", f"song number {num} printed after song {last_song}; read as "
                 f"{last_song + 1}", pos, line)
            num = last_song + 1
        if not is_line_no and (num == last_song + 1 or num == 1):
            if head:
                if song_open is not None:
                    songs[-1]["end"] = pos - 1
                songs.append({"n": num, "start": pos, "end": None})
                song_open = num
            else:
                prev_end = songs[-1]["end"] if songs and songs[-1]["end"] >= block_start else block_start - 1
                songs.append({"n": num, "start": max(prev_end, block_start - 1) + 1, "end": pos})
            last_song = num
        elif num % 5 == 0 or (abs(num - pos) <= 2 and not songs):
            printed.append((pos, num))
        else:
            flag(book, rid, "numbering", f"number {num} on line {pos} fits neither the line count "
                 f"nor the song count (last song {last_song})", pos, line)
    close_block()
    if head and song_open is not None:
        songs[-1]["end"] = len(tamil)
    # A song whose start fell before its block (tail numbering after a label) is clipped.
    for s in songs:
        blk = next(b for b in blocks if b["start"] <= s["end"] <= b["end"])
        s["start"] = max(s["start"], blk["start"])
        s["block_label"] = blk["label"]
    return {
        "id": rid, "book": book, "number": n if isinstance(n, int) else None, "kind": kind,
        "short_name": short, "title": title, "kandam": kandam,
        "line_count": len(tamil), "printed_last_line": None,
        "blocks": blocks, "songs": songs or None, "tamil": tamil,
        "tamil_source": p["source"], "rights": RIGHTS,
    }, printed, para_start, notes


def check_printed(book, rid, printed):
    bad = [(pos, num) for pos, num in printed if pos != num]
    if bad:
        pos, num = bad[0]
        flag(book, rid, "lineation", f"printed line number {num} stands on line {pos}"
             + (f" ({len(bad)} numbers off; first shown)" if len(bad) > 1 else ""), pos)
    return bad


def units_for(rec, para_start, song_kaathai, numbered=frozenset()):
    """Reading units for one whole record (see the module docstring)."""
    book, n = rec["book"], rec["number"] if rec["number"] is not None else rec["short_name"]
    tamil, out = rec["tamil"], []

    def emit(s, e, kind, label, song=None):
        out.append({
            "id": f"{book}:{n}:{s + 1}-{e}", "record_id": rec["id"], "book": book,
            "number": rec["number"], "short_name": rec["short_name"], "start": s + 1, "end": e,
            "line_count": e - s, "kind": kind, "block_label": label, "song": song,
            "break_score": score_break(tamil[e - 1]), "tamil": tamil[s:e], "rights": RIGHTS,
        })

    def cut(s, e, kind, label, song=None):
        if e - s <= 25:
            emit(s, e, kind, label, song)
        else:
            for a, b in split_units(tamil, s, e):
                emit(a, b, kind, label, song)

    songs = rec["songs"] or []
    for blk in rec["blocks"]:
        bs, be = blk["start"] - 1, blk["end"]
        inside = [s for s in songs if bs < s["end"] <= be]
        label = blk["label"]
        if inside:
            pos = bs
            for s in inside:
                if s["start"] - 1 > pos:
                    gap_units(pos, s["start"] - 1, label, para_start, song_kaathai, cut, numbered)
                cut(s["start"] - 1, s["end"], "song", s.get("block_label"), s["n"])
                pos = s["end"]
            if pos < be:
                gap_units(pos, be, label, para_start, song_kaathai, cut, numbered)
        else:
            gap_units(bs, be, label, para_start, song_kaathai, cut, numbered)
    return out


def gap_units(s, e, label, para_start, song_kaathai, cut, numbered=frozenset()):
    """Lines outside the numbered songs. In a kaathai of songs a blank line separates stanzas, and
    each stanza is a song of its own, unless the lines carry printed line numbers (then they are
    akaval, and the blank lines only follow the numbers); elsewhere the lines are akaval or a
    short closing poem."""
    akaval = any(s < pos <= e for pos in numbered)
    kind = "song" if (song_kaathai and not akaval) or (label and ("வெண்பா" in label or "வரி" in label)) \
        else "verse"
    if song_kaathai and not akaval:
        starts = [i for i in range(s, e) if para_start[i] or i == s] + [e]
        for a, b in zip(starts, starts[1:]):
            cut(a, b, kind, label)
    else:
        cut(s, e, kind, label)


def build_silappathikaram(text_dir):
    pieces = sil_pieces(text_dir)
    records, units = [], []
    got = [p["n"] for p in pieces]
    want = [0] + list(range(1, 11)) + ["katturai"] + list(range(11, 24)) + ["katturai"] \
        + list(range(24, 31)) + ["katturai", "nool_katturai"]
    if got != want:
        flag("silappathikaram", "silappathikaram", "structure", f"pieces found {got}; expected {want}")
    for p in pieces:
        rec, printed, para_start, notes = sil_piece_record(p)
        rid = rec["id"]
        bad = check_printed("silappathikaram", rid, printed)
        if printed:
            rec["printed_last_line"] = printed[-1][1]
            if printed[-1][0] == len(rec["tamil"]) and printed[-1][1] != len(rec["tamil"]):
                flag("silappathikaram", rid, "line_count", f"{len(rec['tamil'])} lines, but the last "
                     f"line is numbered {printed[-1][1]}")
        for note in notes:
            m = re.findall(r"(\d+)\s*முதல்\s*(\d+)|(\d+)\s*ஆம்", note)
            spans = [f"{a}-{b}" if a else c for a, b, c in m]
            flag("silappathikaram", rid, "editor_note", "modern editor's note stripped: it says many "
                 "commentators take these lines as later interpolations: " + ", ".join(spans))
            rec["interpolation_note_lines"] = spans
        song_kaathai = rec["number"] in SIL_SONG_KAATHAIS
        check_lines("silappathikaram", rid, rec["tamil"], refrain=song_kaathai or rec["number"] == 18)
        rec["song_kaathai"] = song_kaathai
        records.append(rec)
        units += units_for(rec, para_start, song_kaathai, frozenset(pos for pos, _ in printed))
    return records, units


# --------------------------------------------------------------------------------------------
# Manimekalai

MANI_SHORT = {
    0: "patikam", 1: "vizhavarai_kaathai", 2: "ooralar_uraiththa_kaathai", 3: "malarvanam_pukka_kaathai",
    4: "palikkarai_pukka_kaathai", 5: "manimekala_theyvam_vanthu_thonriya_kaathai",
    6: "chakkaravaalak_kottam_uraiththa_kaathai", 7: "thuyilezhuppiya_kaathai",
    8: "manipallavaththu_thuyarutra_kaathai", 9: "peedikai_kandu_pirappunarntha_kaathai",
    10: "manthiram_koduththa_kaathai", 11: "paaththiram_petra_kaathai", 12: "aravanar_thozhutha_kaathai",
    13: "aaputhiran_thiram_ariviththa_kaathai", 14: "paaththira_marabu_kooriya_kaathai",
    15: "paaththiram_kondu_pichai_pukka_kaathai", 16: "aathirai_pichaiyitta_kaathai",
    17: "ulaga_aravi_pukka_kaathai", 18: "udayakumaran_ambalam_pukka_kaathai",
    19: "siraikkottam_arakkottam_aakkiya_kaathai", 20: "udayakumaranai_kaanchanan_vaalaal_erintha_kaathai",
    21: "kanthirpaavai_varuvathu_uraiththa_kaathai", 22: "sirai_sey_kaathai", 23: "sirai_vidu_kaathai",
    24: "aaputhiran_naadu_adaintha_kaathai", 25: "aaputhiranodu_manipallavam_adaintha_kaathai",
    26: "vanchi_maanagar_pukka_kaathai", 27: "samayak_kanakkar_tham_thiram_ketta_kaathai",
    28: "kachchi_maanagar_pukka_kaathai", 29: "thavaththiram_poondu_tharumam_ketta_kaathai",
    30: "bavaththiram_arukenap_paavai_notra_kaathai",
}


def build_manimekalai(text_dir):
    book = "manimekalai"
    lines = body(text_dir, "pmuni0141").split("\n")
    pieces, cur, expected = [], None, 1
    for raw in lines:
        s = raw.strip()
        if s == "## மணிமேகலை":
            cur = {"n": 0, "title": "பதிகம்", "items": []}
            pieces.append(cur)
            continue
        m = re.match(r"^###\s*(\d{1,2})?\.?\s*(.+)$", s)
        if m and cur is not None:
            n = int(m.group(1)) if m.group(1) else expected
            if n != expected:
                flag(book, book, "structure", f"heading {s!r} where kaathai {expected} was expected")
            if not m.group(1):
                flag(book, f"{book}:{n}", "heading", f"the heading of kaathai {n} lacks its number "
                     f"in the e-text: {m.group(2)!r}")
            cur = {"n": n, "title": m.group(2).strip(), "items": []}
            pieces.append(cur)
            expected = n + 1
            continue
        if cur is None or not s or s.startswith("(ஆசிரியர்"):
            continue
        if s.startswith(("This page", "This webpage", "Feel free")):
            cur = None
            continue
        cur["items"].append(s)
    records, units = [], []
    for p in pieces:
        n = p["n"]
        rid = f"{book}:{n}"
        tamil, printed = [], []
        for s in p["items"]:
            m = re.match(r"^(.*?)\s*(\d{2,3})-(\d{3,4})\s*$", s)
            text, mark = (m.group(1), (int(m.group(2)), m.group(3))) if m else (s, None)
            text = tidy(text)
            if not text:
                continue
            tamil.append(repair(book, rid, len(tamil) + 1, text))
            if mark:
                k, ln = mark
                if k != n:
                    flag(book, rid, "numbering", f"line mark {k}-{ln} carries kaathai number {k}; "
                         f"read as {n:02d}-{ln}", len(tamil), tamil[-1])
                if len(ln) == 3:
                    printed.append((len(tamil), int(ln)))
                else:
                    flag(book, rid, "numbering", f"malformed line mark {k}-{ln} (ignored)",
                         len(tamil), tamil[-1])
        check_printed(book, rid, printed)
        check_lines(book, rid, tamil)
        last = printed[-1] if printed else None
        if last and last[0] == len(tamil) and last[1] != len(tamil):
            flag(book, rid, "line_count", f"{len(tamil)} lines, but the last line is numbered {last[1]}")
        if not last or last[0] != len(tamil):
            flag(book, rid, "lineation", "the last line carries no line mark", len(tamil))
        rec = {
            "id": rid, "book": book, "number": n, "kind": "patikam" if n == 0 else "kaathai",
            "short_name": MANI_SHORT[n], "title": re.sub(r"\s+", " ", p["title"]),
            "line_count": len(tamil), "printed_last_line": last[1] if last else None,
            "blocks": [{"label": None, "start": 1, "end": len(tamil)}], "songs": None,
            "tamil": tamil, "tamil_source": "pmuni0141", "rights": RIGHTS,
        }
        records.append(rec)
        units += units_for(rec, [False] * len(tamil), False)
    return records, units


# --------------------------------------------------------------------------------------------
# Verse epics: shared parsing

COMMENTARY_START = re.compile(r"^(?:\(?\s*(?:இதன்\s*)?பொருள்\s*\)?\s*[:：]|\(?இ\s*-\s*ள்|\(?வி\s*-\s*ம்|"
                              r"விளக்கம்\s*[:：)]|\(விளக்கம்\)|உரை\s*[:：]|\(இதன் பொருள்\)|குறிப்பு\s*[:：])")


HEADING_WORDS = re.compile(r"^\s*(?:இதுவுமது|இதுவும் அடுத்த|அவையடக்கம்|அவை அடக்கம்|பதிகம்|"
                           r"கடவுள் வாழ்த்து|வேறு\b|.*\bகுளகம்\s*$|.*சருக்கம்\s*$)")


def verse_like(s, max_len=75):
    """A line that can be a verse line: Tamil, not too long, not commentary."""
    t = s.strip()
    return bool(t) and TAMIL_CHAR.search(t) and len(t) <= max_len and not COMMENTARY_START.match(t) \
        and not t.startswith(("###", "(", "[", "--", "*", "†"))


def blocks_after(lines, i):
    """Paragraphs (runs of non-blank lines) from index i on: yields (start, end) pairs."""
    n = len(lines)
    while i < n:
        while i < n and not lines[i].strip():
            i += 1
        if i >= n:
            return
        j = i
        while j < n and lines[j].strip():
            j += 1
        yield i, j
        i = j


def join_halves(book, rid, verse, want=4, any_length=False):
    """A four-line stanza printed in eight half-lines (as some volumes of the e-text do) is joined
    back into four lines."""
    if len(verse) == 2 * want and (any_length or all(len(letters(x)) <= 40 for x in verse)):
        flag(book, rid, "repaired", f"stanza printed in {len(verse)} half-lines; joined into {want} lines")
        return [verse[k] + " " + verse[k + 1] for k in range(0, len(verse), 2)]
    return verse


def split_kural_pairs(book, rid, verse):
    """Four short (kural) lines printed two to a line, the pair split by a comma (Cintamani
    565-580, Soolamani 1298-1302): split back into four lines."""
    if len(verse) == 2 and all(x.count(",") == 1 for x in verse):
        flag(book, rid, "repaired", "four short lines printed two to a line (separated by a comma); "
             "split into four lines")
        return [y.strip() for x in verse for y in x.split(",")]
    return verse


def strip_heading(book, rid, verse, want=4):
    """Drop an editor's heading printed directly above the verse, without a blank line: one line
    more than the stanza has, much shorter than the verse lines."""
    if len(verse) == want + 1:
        rest = sorted(len(letters(x)) for x in verse[1:])
        med = rest[len(rest) // 2]
        if len(letters(verse[0])) < 0.6 * med or "[" in verse[0] or verse[0].startswith("வேறு"):
            flag(book, rid, "heading_removed", "a modern heading printed on the line above the verse "
                 "was not taken as verse", 0)
            return verse[1:]
    return verse


def section_of(n, table):
    for k, (name, lo, hi) in enumerate(table):
        if lo <= n <= hi:
            return k, name
    return None, None


def verse_record(book, n, tamil, source, section_table, section_kind, extra=None):
    k, name = section_of(n, section_table)
    rec = {"id": f"{book}:{n}", "book": book, "number": n, "section_number": k, "section": name,
           "section_kind": section_kind, "padalam": None, "line_count": len(tamil), "tamil": tamil,
           "tamil_source": source, "rights": RIGHTS}
    if extra:
        rec.update(extra)
    return rec


def drop_repeats(book, records):
    """A verse printed twice under two numbers: the second copy stands where a verse is lost, so
    it is not kept as that verse."""
    out = []
    for r in records:
        if out and letters(" ".join(r["tamil"])) == letters(" ".join(out[-1]["tamil"])):
            flag(book, r["id"], "duplicate_verse", f"the e-text prints verse {out[-1]['number']} again "
                 f"under the number {r['number']}; verse {r['number']} itself is lost there "
                 "(record omitted)")
            continue
        out.append(r)
    return out


def finish_verses(book, records, expected_total, stanza_lines=None):
    """Checks shared by the verse epics: sequence, duplicates, characters, stanza length."""
    nums = [r["number"] for r in records]
    want = list(range(nums[0], nums[0] + expected_total)) if nums else []
    missing = sorted(set(want) - set(nums))
    dup = [n for n, c in Counter(nums).items() if c > 1]
    if missing:
        flag(book, book, "missing_verse", f"{len(missing)} verse numbers missing: {compress(missing)}")
    if dup:
        flag(book, book, "duplicate_verse", f"verse numbers twice: {compress(sorted(dup))}")
    if nums != sorted(nums):
        flag(book, book, "order", "verse numbers out of order")
    seen = {}
    for r in records:
        check_lines(book, r["id"], r["tamil"])
        if stanza_lines and r["line_count"] not in stanza_lines:
            flag(book, r["id"], "stanza_length", f"{r['line_count']} lines (expected "
                 f"{' or '.join(map(str, sorted(stanza_lines)))})")
        key = letters(" ".join(r["tamil"]))
        if key in seen and len(key) > 20:
            flag(book, r["id"], "duplicate_verse", f"same text as {seen[key]}")
        seen.setdefault(key, r["id"])
    return missing, dup


def compress(nums):
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(str(nums[i]) if i == j else f"{nums[i]}-{nums[j]}")
        i = j + 1
    return ", ".join(out)


def source_lines(text_dir, name):
    """The e-text's lines, NFC, with footnote marks such as '[1]' removed."""
    out = []
    for l in body(text_dir, name).split("\n"):
        l = unicodedata.normalize("NFC", l).replace("\u00a0", " ")
        l = re.sub(r"[\u200B-\u200D\uFEFF]", "", l)
        l = re.sub(r"[*†‡§$+]+", "", l)  # marks that point to variant readings in the commentary
        out.append(re.sub(r"\[\d{1,2}\]", "", l))
    return out


def typo_of(num, expected):
    """True when the printed number differs from the expected one by one digit typed, dropped or
    changed (145 printed 1405, 64 printed 6, 706 printed 7096)."""
    a, b = str(num), str(expected)
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if abs(len(a) - len(b)) != 1:
        return False
    short, long_ = (a, b) if len(a) < len(b) else (b, a)
    return any(long_[:k] + long_[k + 1:] == short for k in range(len(long_)))


def head_numbered(book, files, text_dir, start=1, last=None, max_len=75, inline_ok=True,
                  skip_until=None):
    """Verses whose number stands before the verse ('12. first line' or '12.' on its own line),
    each followed by commentary or a prose rendering. The parse is driven by the expected next
    number, so numbered footnotes and lists in the commentary are not taken for verses.
    Returns {n: (lines, source, preceded_by_veru)}."""
    out, expected = {}, start
    for name in files:
        lines = source_lines(text_dir, name)
        i0 = 0
        if skip_until:
            i0 = next((i for i, l in enumerate(lines) if skip_until(l, name)), 0)
        i = i0
        prev_end = None
        while i < len(lines):
            s = lines[i].strip()
            m = re.match(r"^(\d{1,4})\s*\.?\s*(.*)$", s)
            if not m or (last and expected > last):
                i += 1
                continue
            got = int(m.group(1))
            if got == expected + 1 and expected > start and prev_end is not None \
                    and not any(re.match(rf"^{expected + 1}\s*\.?(?:\s|$)", x.strip())
                                for x in lines[i + 1:i + 80]):
                # the number of the verse before this one is not printed: an unnumbered stanza
                # between the last verse and this one is that verse
                between = []
                for bs, be in blocks_after(lines[:i], prev_end):
                    blk = [x.strip() for x in lines[bs:be]]
                    while blk and re.fullmatch(r"\(.*\)\.?", blk[0]):
                        blk = blk[1:]
                    if len(blk) >= 3 and all(verse_like(x, max_len) for x in blk):
                        between.append(blk)
                if len(between) == 1:
                    flag(book, f"{book}:{expected}", "numbering", "the e-text prints this verse without "
                         f"its number; it stands between {expected - 1} and {got}")
                    out[expected] = (between[0], name, False)
                else:
                    flag(book, f"{book}:{expected}", "gap", f"the e-text goes from verse {expected - 1} "
                         f"to {got}")
                expected = got
            if got != expected:
                # a misprinted verse number: accepted when the next number follows soon after
                nxt = re.compile(rf"^{expected + 1}\s*\.?(?:\s|$)")
                ahead = [x.strip() for x in lines[i + 1:i + 80]]
                own = re.compile(rf"^{expected}\s*\.?(?:\s|$)")
                if expected > start + 1 and typo_of(got, expected) \
                        and any(nxt.match(x) for x in ahead) and not any(own.match(x) for x in ahead) \
                        and (got != expected + 1 or sum(1 for x in ahead if nxt.match(x)) >= 1):
                    flag(book, f"{book}:{expected}", "numbering", f"verse printed with the number "
                         f"{got}; read as {expected} (the next verse is {expected + 1})", None, s[:60])
                else:
                    i += 1
                    continue
            rest = m.group(2).strip()
            # block A: the rest of this line and the lines after it up to a blank line
            a = [rest] if rest else []
            j = i + 1
            while j < len(lines) and lines[j].strip():
                a.append(lines[j].strip())
                j += 1
            verse = None
            if rest and not inline_ok:
                a = a[1:]
            if 0 < len(a) < 4:
                nb = next(iter(blocks_after(lines, j)), None)
                if nb:
                    blk = [x.strip() for x in lines[nb[0]:nb[1]]]
                    while blk and re.fullmatch(r"\(.*\)\.?", blk[0]):
                        blk = blk[1:]
                    if len(blk) >= 4 and all(verse_like(x, max_len) for x in blk[:4]) \
                            and not re.match(r"^\d", blk[0]):
                        a = []  # a two- or three-line heading; the verse is the next block
            if ((len(a) >= 4 and all(verse_like(x, max_len) for x in a[:4])) or
                              (len(a) >= 2 and all(verse_like(x, max_len) for x in a[:2])
                               and sum(len(x) for x in a[:2]) / 2 >= 22)):
                k = next((t for t, x in enumerate(a) if not verse_like(x, max_len)), len(a))
                verse = a[:k]
            else:
                for bs, be in blocks_after(lines, j):
                    blk = [x.strip() for x in lines[bs:be]]
                    while blk and (re.fullmatch(r"\(?\d+\)?", blk[0]) or blk[0] in ("வேறு",) or
                                   re.fullmatch(r"\(.*\)\.?", blk[0])):
                        blk = blk[1:]  # a number, வேறு, or a metre label such as (கலி விருத்தம்)
                    if not blk:
                        continue
                    if len(blk) >= 2 and all(verse_like(x, max_len) for x in blk[:2]):
                        k = next((t for t, x in enumerate(blk) if not verse_like(x, max_len)), len(blk))
                        verse = blk[:k]
                        j = be
                        break
                    if len(blk) <= 2 and all(len(x) < 60 for x in blk):
                        continue  # an editor's heading
                    break
            if not verse:
                i += 1
                continue
            veru = any(lines[t].strip() == "வேறு" for t in range(max(i0, i - 3), i))
            out[expected] = (verse, name, veru)
            expected += 1
            i = j
            prev_end = j
    return out


def tail_numbered(book, files, text_dir, start=1, last=None, max_len=75, skip_until=None,
                  stop=None):
    """Verses whose number stands at the end of the last line ('... என்பவே. 7'). The verse is
    the run of verse lines just above the numbered line. Returns {n: (lines, source, veru)}."""
    out, expected = {}, start
    for name in files:
        lines = source_lines(text_dir, name)
        i0 = 0
        if skip_until:
            i0 = next((i for i, l in enumerate(lines) if skip_until(l, name)), 0)
        prev_i = i0 - 1
        for i in range(i0, len(lines)):
            s = lines[i].strip()
            if stop and stop(s, name):
                break
            text, num = split_num(s)
            end = i
            bare = re.fullmatch(r"\(?(\d{1,4})\)?\.?", s)
            if bare and int(bare.group(1)) == expected and i > i0 and verse_like(lines[i - 1], max_len) \
                    and split_num(lines[i - 1].strip())[1] is None:
                # the number printed on a line of its own under the verse
                text, num, end = lines[i - 1].strip(), expected, i - 1
            while num is not None:  # a footnote number printed before the verse number
                t2, n2 = split_num(text)
                if n2 is None:
                    break
                text = t2
            if num is None or (last and expected > last) or re.search(r"\d", text):
                continue
            if num != expected:
                # a misprinted number (1405 for 145): accepted when the next printed number is
                # the one after, and the expected number is not printed further on
                ahead = [split_num(x.strip())[1] for x in lines[i + 1:i + 60]]
                ahead = [x for x in ahead if x is not None]
                if expected < num <= expected + 10 and ahead and ahead[0] == num + 1 \
                        and expected not in ahead and TAMIL_CHAR.search(text):
                    # the numbers jump. An unnumbered stanza between the last verse and this one
                    # is the missing verse when one number is missing; otherwise the verses
                    # between are not in the e-text.
                    k = end - 1
                    while k > prev_i and lines[k].strip() and split_num(lines[k].strip())[1] is None:
                        k -= 1
                    between = [lines[bs:be] for bs, be in blocks_after(lines[:k + 1], prev_i + 1)]
                    between = [[x.strip() for x in b] for b in between]
                    between = [[x for x in b if verse_like(x, max_len)] for b in between]
                    between = [b for b in between if len(b) >= 3]
                    if num == expected + 1 and len(between) == 1:
                        flag(book, f"{book}:{expected}", "numbering", "the e-text prints this verse "
                             f"without its number; it stands between {expected - 1} and {num}")
                        out[expected] = (between[0], name, False)
                    else:
                        flag(book, f"{book}:{expected}", "gap", f"the e-text goes from verse "
                             f"{expected - 1} to {num}", None, s[-60:])
                    expected = num
                elif not ahead or not (expected + 1 in ahead[:2] or expected + 2 in ahead[1:3]) \
                        or expected in ahead or num < 1 or not typo_of(num, expected) \
                        or not verse_like(text, max_len) \
                        or not TAMIL_CHAR.search(text) or expected == start:
                    continue
                else:
                    flag(book, f"{book}:{expected}", "numbering", f"verse printed with the number "
                         f"{num}; read as {expected} (the next verse is {expected + 1})", None, s[-60:])
            verse = [text]
            j = end - 1
            while j >= i0 and lines[j].strip() and verse_like(lines[j], max_len) \
                    and split_num(lines[j].strip())[1] is None and len(verse) < 12 \
                    and not HEADING_WORDS.search(lines[j]):
                verse.insert(0, lines[j].strip())
                j -= 1
            if len(verse) < 2:
                continue
            veru = any(lines[t].strip() == "வேறு" for t in range(max(i0, j - 2), j + 1))
            out[expected] = (verse, name, veru)
            expected += 1
            prev_i = i
    return out


# --------------------------------------------------------------------------------------------
# Civaka Cintamani

CINTAMANI_FILES = ("pmuni0664_01", "pmuni0664_02", "pmuni0670_01", "pmuni0670_02", "pmuni0672_01",
                   "pmuni0672_02", "pmuni0672_03")
# The thirteen ilampakams and their verses, as the edition's own table of contents gives them
# (verses 1-29: the invocation, the modesty verses and the patikam).
CINTAMANI_SECTIONS = (
    ("கடவுள் வாழ்த்து, பதிகம்", 1, 29), ("நாமகள் இலம்பகம்", 30, 408),
    ("கோவிந்தையார் இலம்பகம்", 409, 492), ("காந்தருவதத்தையார் இலம்பகம்", 493, 850),
    ("குணமாலையார் இலம்பகம்", 851, 1165), ("பதுமையார் இலம்பகம்", 1166, 1411),
    ("கேமசரியார் இலம்பகம்", 1412, 1556), ("கனகமாலையார் இலம்பகம்", 1557, 1888),
    ("விமலையார் இலம்பகம்", 1889, 1994), ("சுரமஞ்சரியார் இலம்பகம்", 1995, 2101),
    ("மண்மகள் இலம்பகம்", 2102, 2326), ("பூமகள் இலம்பகம்", 2327, 2377),
    ("இலக்கணையார் இலம்பகம்", 2378, 2598), ("முத்தி இலம்பகம்", 2599, 3145),
)


def clean_verse(book, rid, verse):
    out = []
    for i, l in enumerate(verse, 1):
        l = re.sub(r"\s+\d{1,2}\.\d{1,3}\.?\s*$", "", l)  # a sarukkam.verse mark such as 7.1
        l = re.sub(r"^\d{1,4}\.?\s*", "", l)  # a verse number or footnote mark before the line
        l = re.sub(r"^\[|\]$", "", l.strip())  # a bracket left from an editor's note
        text, num = split_num(l)
        while num is not None:
            l = text
            text, num = split_num(l)
        l = re.sub(r"\s+\d{1,2}\.$", "", l)  # the sarukkam part of a mark such as '7. 100'
        l = re.sub(r"[*†‡]+", "", l)
        l = tidy(l)
        if l:
            out.append(repair(book, rid, i, l))
    return out


def build_civaka_cintamani(text_dir):
    book = "civaka_cintamani"
    raw = head_numbered(book, CINTAMANI_FILES, text_dir, start=1, last=3145,
                        skip_until=lambda l, name: "பாகம் 1 (பாடல்கள்" in l or name != "pmuni0664_01")
    records = []
    for n in sorted(raw):
        verse, src, veru = raw[n]
        rid = f"{book}:{n}"
        verse = clean_verse(book, rid, verse)
        verse = join_halves(book, rid, verse, any_length=True)
        verse = split_kural_pairs(book, rid, verse)
        records.append(verse_record(book, n, verse, src, CINTAMANI_SECTIONS, "இலம்பகம்",
                                    {"metre_change_before": veru}))
    finish_verses(book, records, 3145, stanza_lines={4})
    return records


# --------------------------------------------------------------------------------------------
# Valayapathi and Kundalakesi: the surviving verses, known only from quotations

def valayapathi_source(n):
    if n == 0:
        return "தொல்காப்பியம் செய்யுளியல் உரைகள் (இளம்பூரணர், நச்சினார்க்கினியர்); யாப்பருங்கல விருத்தியுரை"
    if n <= 66:
        return "புறத்திரட்டு"
    if n <= 69:
        return "சிலப்பதிகாரம், அடியார்க்கு நல்லார் உரை"
    return "யாப்பருங்கல விருத்தியுரை"


def build_valayapathi(text_dir):
    book = "valayapathi"
    lines = source_lines(text_dir, "pmuni0062")
    start = next(i for i, l in enumerate(lines) if "வளையாபதியிற் கிடைத்துள்ள செய்யுள்கள்" in l)
    lines = lines[start:]
    records = []
    # the invocation: the first verse block after the heading கடவுள் வாழ்த்து
    i = next(i for i, l in enumerate(lines) if l.strip() == "கடவுள் வாழ்த்து")
    for bs, be in blocks_after(lines, i + 1):
        blk = [x.strip() for x in lines[bs:be]]
        if blk[0].startswith("[") or not all(verse_like(x) for x in blk):
            continue
        rid = f"{book}:0"
        records.append(verse_record(book, 0, clean_verse(book, rid, blk), "pmuni0062", (), None,
                                    {"kind": "invocation", "quoted_in": valayapathi_source(0)}))
        break
    raw = head_numbered(book, ("pmuni0062",), text_dir, start=1, last=71, inline_ok=False,
                        skip_until=lambda l, name: "வளையாபதியிற் கிடைத்துள்ள" in l)
    for n in sorted(raw):
        verse, src, _ = raw[n]
        rid = f"{book}:{n}"
        records.append(verse_record(book, n, clean_verse(book, rid, verse), src, (), None,
                                    {"kind": "verse", "quoted_in": valayapathi_source(n)}))
    for r in records:
        r.pop("section_number"), r.pop("section_kind"), r.pop("padalam")
        r["section"] = None
    finish_verses(book, records, 72)
    return records


def build_kundalakesi(text_dir):
    book = "kundalakesi"
    raw = head_numbered(book, ("pmuni0507",), text_dir, start=1, last=19, inline_ok=False,
                        skip_until=lambda l, name: l.strip() == "1. கடவுள் வாழ்த்து")
    records = []
    for n in sorted(raw):
        verse, src, _ = raw[n]
        rid = f"{book}:{n}"
        verse = join_halves(book, rid, clean_verse(book, rid, verse))
        records.append(verse_record(book, n, verse, src, (), None,
                                    {"kind": "invocation" if n == 1 else "verse"}))
    for r in records:
        r.pop("section_number"), r.pop("section_kind"), r.pop("padalam")
        r["section"] = None
    finish_verses(book, records, 19)
    return records


# --------------------------------------------------------------------------------------------
# Soolamani

SOOLAMANI_SECTIONS = (
    ("பாயிரம்", 1, 6), ("நாட்டுச் சருக்கம்", 7, 35), ("நகரச் சருக்கம்", 36, 69),
    ("குமாரகாலச் சருக்கம்", 70, 118), ("இரதநூபுரச் சருக்கம்", 119, 238),
    ("மந்திரசாலைச் சருக்கம்", 239, 430), ("தூதுவிடு சருக்கம்", 431, 572),
    ("சீயவதைச் சருக்கம்", 573, 826), ("கல்யாணச் சருக்கம்", 827, 1130),
    ("அரசியற் சருக்கம்", 1131, 1554), ("சுயம்வரச் சருக்கம்", 1555, 1839),
    ("துறவுச் சருக்கம்", 1840, 2068), ("முத்திச் சருக்கம்", 2069, 2130),
)


def unnumbered_stanzas(text_dir, name, start_at):
    """Stanzas of an e-text that prints no verse numbers: paragraphs of three or more verse lines,
    after an editor's one-line heading glued on top is taken off. Also returns the paragraph
    index of each sarukkam heading, to check the count against the table of contents."""
    lines = source_lines(text_dir, name)
    i0 = next(i for i, l in enumerate(lines) if start_at(l))
    stanzas, heads = [], []
    for bs, be in blocks_after(lines, i0):
        blk = [x.strip() for x in lines[bs:be] if x.strip() and not re.fullmatch(r"-{3,}", x.strip())]
        if not blk or blk[0].startswith("###"):
            continue
        if any("சருக்கம்" in x and len(x) < 40 for x in blk) and len(blk) <= 4:
            head = next((x for x in blk if "சருக்கம்" in x and "முற்றி" not in x and "முடிந்த" not in x), None)
            if head:
                heads.append((len(stanzas), head))
            continue
        veru = False
        while blk and (len(blk) > 4 or len(blk) == 1 or blk[0].startswith("வேறு")) and \
                (len(blk[0]) < 28 or blk[0].startswith("வேறு")) and not split_num(blk[0])[1]:
            veru = veru or blk[0].startswith("வேறு")
            blk = blk[1:]
        if len(blk) >= 3 and all(verse_like(x) for x in blk):
            stanzas.append((blk, veru))
    return stanzas, heads


def build_soolamani(text_dir):
    book = "soolamani"
    first = tail_numbered(book, ("pmuni0035_01",), text_dir, start=1, last=238)
    second, heads = unnumbered_stanzas(text_dir, "pmuni0035_02", lambda l: l.strip() == "பாயிரம்")
    rest = tail_numbered(book, ("pmuni0602_01", "pmuni0602_02"), text_dir, start=827, last=2130)
    # pmuni0035_02 must agree with pmuni0035_01 on 1-238 for its stanza count to number 239-826.
    agree = sum(1 for n in range(1, 239) if n in first and n - 1 < len(second)
                and similarity(" ".join(first[n][0]), " ".join(second[n - 1][0])) > 0.6)
    if agree < 230:
        flag(book, book, "alignment", f"pmuni0035_02 stanzas agree with pmuni0035_01 on only "
             f"{agree} of 238 verses; 239-826 not numbered by position")
    for pos, head in heads:
        k, name = section_of(pos + 1, SOOLAMANI_SECTIONS)
        if name and head.replace(" ", "")[-12:] not in name.replace(" ", "") and \
                not any(h.replace(" ", "") in head.replace(" ", "") for h, lo, hi in SOOLAMANI_SECTIONS
                        if lo == pos + 1):
            flag(book, f"{book}:{pos + 1}", "section", f"pmuni0035_02 heading {head!r} stands before "
                 f"stanza {pos + 1}, which the table of contents does not start a sarukkam with")
    records, witness_variants = [], []
    for n in range(1, 2131):
        rid = f"{book}:{n}"
        if n in first:
            verse, src, veru = first[n]
            if n - 1 < len(second):
                a, b2 = letters(" ".join(verse)), letters(" ".join(second[n - 1][0]))
                if similarity(a, b2) < 0.6:
                    flag(book, rid, "witness_differs", "pmuni0035_02 reads this verse differently")
                elif a != b2:
                    witness_variants.append(n)
        elif n <= 826 and n - 1 < len(second):
            (verse, veru), src = second[n - 1], "pmuni0035_02"
        elif n in rest:
            verse, src, veru = rest[n]
        else:
            continue
        verse = join_halves(book, rid, strip_heading(book, rid, clean_verse(book, rid, verse)),
                            any_length=True)
        verse = split_kural_pairs(book, rid, verse)
        records.append(verse_record(book, n, verse, src, SOOLAMANI_SECTIONS,
                                    "சருக்கம்", {"metre_change_before": veru}))
    if witness_variants:
        flag(book, book, "witness_variant", f"{len(witness_variants)} of verses 1-238 differ in some "
             "letters between pmuni0035_01 (kept) and pmuni0035_02: " + compress(witness_variants))
    records = drop_repeats(book, records)
    if len(second) != 826:
        flag(book, book, "count", f"pmuni0035_02 has {len(second)} stanzas; verses 1-826 expected")
    finish_verses(book, records, 2130, stanza_lines={4})
    return records


# --------------------------------------------------------------------------------------------
# Neelakesi

NEELAKESI_SECTIONS = (
    ("கடவுள் வாழ்த்து", 1, 9), ("தருமவுரைச் சருக்கம்", 10, 149),
    ("குண்டலகேசி வாதச் சருக்கம்", 150, 231), ("அர்க்கசந்திர வாதச் சருக்கம்", 232, 266),
    ("மொக்கல வாதச் சருக்கம்", 267, 462), ("புத்த வாதச் சருக்கம்", 463, 658),
    ("ஆசீவக வாதச் சருக்கம்", 659, 729), ("சாங்கிய வாதச் சருக்கம்", 730, 782),
    ("வைசேடிக வாதச் சருக்கம்", 783, 823), ("வேத வாதச் சருக்கம்", 824, 853),
    ("பூத வாதச் சருக்கம்", 854, 894),
)


def build_neelakesi(text_dir):
    book = "neelakesi"
    raw = tail_numbered(book, ("pmuni0538",), text_dir, start=1, last=894,
                        skip_until=lambda l, name: l.strip() == "1. கடவுள் வாழ்த்து" or
                        l.strip().startswith("நல்லார் வணங்கப்"))
    records = []
    for n in sorted(raw):
        verse, src, veru = raw[n]
        rid = f"{book}:{n}"
        verse = split_kural_pairs(book, rid, join_halves(book, rid, strip_heading(
            book, rid, clean_verse(book, rid, verse))))
        records.append(verse_record(book, n, verse, src, NEELAKESI_SECTIONS, "சருக்கம்",
                                    {"metre_change_before": veru}))
    records = drop_repeats(book, records)
    finish_verses(book, records, 894, stanza_lines={4, 5})
    return records


# --------------------------------------------------------------------------------------------
# Naga Kumara Kaviyam, Udayana Kumara Kaviyam, Yasodhara Kaviyam

NAGA_SECTIONS = (("முதல் சருக்கம்", 1, 39), ("இரண்டாம் சருக்கம்", 40, 73),
                 ("மூன்றாம் சருக்கம்", 74, 101), ("நான்காம் சருக்கம்", 102, 144),
                 ("ஐந்தாம் சருக்கம்", 145, 170))


def invocation_before(text_dir, name, marker, book):
    """An unnumbered invocation (காப்பு) printed before verse 1: the first verse block after the
    marker line."""
    lines = source_lines(text_dir, name)
    i = next((k for k, l in enumerate(lines) if l.strip() == marker), None)
    if i is None:
        return None
    for bs, be in blocks_after(lines, i + 1):
        blk = [x.strip() for x in lines[bs:be]]
        if len(blk) >= 3 and all(verse_like(x, 90) for x in blk):
            return [split_num(x)[0] for x in blk]
        if len(blk) > 2:
            return None
    return None


def build_naga_kumara_kaviyam(text_dir):
    book = "naga_kumara_kaviyam"
    raw = head_numbered(book, ("pmuni0601",), text_dir, start=1, last=170, max_len=90,
                        skip_until=lambda l, name: l.strip() == "### நாக குமார காவியம்")
    records = []
    lines = source_lines(text_dir, "pmuni0601")
    k0 = max(i for i, l in enumerate(lines) if l.strip() == "### நாக குமார காவியம்")
    kappu = None
    for bs, be in blocks_after(lines, k0 + 1):
        blk = [x.strip() for x in lines[bs:be]]
        if len(blk) >= 4 and all(verse_like(x, 90) for x in blk):
            kappu = blk
            break
    if kappu:
        rid = f"{book}:0"
        rec = verse_record(book, 0, clean_verse(book, rid, kappu), "pmuni0601", NAGA_SECTIONS, "சருக்கம்",
                           {"kind": "invocation"})
        rec["section"], rec["section_number"] = "காப்பு", None
        records.append(rec)
        flag(book, rid, "count", "the invocation (காப்பு) before verse 1 is not in the traditional "
             "count of 170; kept as number 0")
    for n in sorted(raw):
        verse, src, veru = raw[n]
        rid = f"{book}:{n}"
        verse = join_halves(book, rid, clean_verse(book, rid, verse))
        records.append(verse_record(book, n, verse, src, NAGA_SECTIONS, "சருக்கம்",
                                    {"kind": "verse", "metre_change_before": veru}))
    records = drop_repeats(book, records)
    finish_verses(book, [r for r in records if r["number"]], 170, stanza_lines={4})
    return records


UDAYANA_SECTIONS = (("பாயிரம்", 1, 4), ("உஞ்சைக் காண்டம்", 5, 120), ("இலாவாண காண்டம்", 121, 150),
                    ("மகத காண்டம்", 151, 185), ("வத்தவ காண்டம்", 186, 241),
                    ("நரவாகன காண்டம்", 242, 302), ("துறவுக் காண்டம்", 303, 367))


def build_udayana_kumara_kaviyam(text_dir):
    book = "udayana_kumara_kaviyam"
    raw = head_numbered(book, ("pmuni0597",), text_dir, start=1, last=367, max_len=90,
                        skip_until=lambda l, name: l.startswith("### உதயணகுமார காவியம் -- செய்யுளும்"))
    records = []
    for n in sorted(raw):
        verse, src, veru = raw[n]
        rid = f"{book}:{n}"
        verse = join_halves(book, rid, clean_verse(book, rid, verse))
        records.append(verse_record(book, n, verse, src, UDAYANA_SECTIONS, "காண்டம்",
                                    {"metre_change_before": veru}))
    records = drop_repeats(book, records)
    finish_verses(book, records, 367, stanza_lines={4})
    return records


YASODHARA_SECTIONS = (("பாயிரம்", 1, 4), ("முதற் சருக்கம்", 5, 73), ("இரண்டாஞ் சருக்கம்", 74, 160),
                      ("மூன்றாஞ் சருக்கம்", 161, 226), ("நான்காஞ் சருக்கம்", 227, 261),
                      ("ஐந்தாஞ் சருக்கம்", 262, 330))


def build_yasodhara_kaviyam(text_dir):
    book = "yasodhara_kaviyam"
    raw = tail_numbered(book, ("pmuni0508_01", "pmuni0508_02"), text_dir, start=1, last=330,
                        skip_until=lambda l, name: "மூலமும் உரையும்" in l or name != "pmuni0508_01")
    records = []
    for n in sorted(raw):
        verse, src, veru = raw[n]
        rid = f"{book}:{n}"
        verse = join_halves(book, rid, strip_heading(book, rid, clean_verse(book, rid, verse)))
        records.append(verse_record(book, n, verse, src, YASODHARA_SECTIONS, "சருக்கம்",
                                    {"metre_change_before": veru}))
    records = drop_repeats(book, records)
    finish_verses(book, records, 330, stanza_lines={4})
    return records


# --------------------------------------------------------------------------------------------

STANDARD = {  # traditional count of verses (verse epics) or lines (the two akaval epics)
    "silappathikaram": None, "manimekalai": None, "civaka_cintamani": 3145, "valayapathi": 72,
    "kundalakesi": 19, "soolamani": 2130, "neelakesi": 894, "naga_kumara_kaviyam": 170,
    "udayana_kumara_kaviyam": 367, "yasodhara_kaviyam": 330,
}


def merge_flags(path, ours):
    """Keep the flags of other books in the shared flags file; replace those of these books."""
    old = []
    if path.exists():
        old = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    kept = [f for f in old if f.get("book") not in EPIC_BOOKS]
    write_jsonl(path, kept + ours)
    return len(kept)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text-dir", type=Path, default=ROOT / "data" / "text")
    ap.add_argument("--out-dir", type=Path, default=ROOT / "kg" / "core")
    args = ap.parse_args()
    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)

    sil, sil_units = build_silappathikaram(args.text_dir)
    mani, mani_units = build_manimekalai(args.text_dir)
    write_jsonl(out / "silappathikaram.jsonl", sil)
    write_jsonl(out / "silappathikaram_units.jsonl", sil_units)
    write_jsonl(out / "manimekalai.jsonl", mani)
    write_jsonl(out / "manimekalai_units.jsonl", mani_units)
    for name, recs, units in (("silappathikaram", sil, sil_units), ("manimekalai", mani, mani_units)):
        lengths = Counter(u["line_count"] for u in units)
        print(f"{name}: {len(recs)} records, {sum(r['line_count'] for r in recs)} lines; "
              f"{len(units)} units ({sum(1 for u in units if u['kind'] == 'song')} songs), "
              f"lengths {min(lengths)}-{max(lengths)}")
    for name in EPIC_BOOKS[2:]:
        recs = globals()[f"build_{name}"](args.text_dir)
        write_jsonl(out / f"{name}.jsonl", recs)
        numbered = [r for r in recs if r["number"] or name in ("valayapathi",)]
        print(f"{name}: {len(recs)} records ({len(numbered)} counted; standard {STANDARD[name]}), "
              f"{sum(r['line_count'] for r in recs)} lines")
    kept = merge_flags(out / "sangam_text_flags.jsonl", flags)
    print(f"flags: {len(flags)} for these books (kept {kept} of other books)")
    print(dict(Counter((f["book"], f["kind"]) for f in flags)))


if __name__ == "__main__":
    main()
