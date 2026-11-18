#!/usr/bin/env python3
"""Parse the Saiva Thirumurai (all but Tiruvasagam and Tirumanthiram) into kg/core/thirumurai.jsonl.

Sources, all in data/text/ (Project Madurai editions):
  Thirumurai 1-3  Sambandar's Thevaram   pmuni0150 0151 | 0157 0162 | 0173 0179
  Thirumurai 4-6  Appar's Thevaram       pmuni0181 0182 | 0186 0188 | 0192 0196
  Thirumurai 7    Sundarar's Thevaram    pmuni0207 0211
  Thirumurai 8    Thirukkovaiyar         pmuni0054
  Thirumurai 9    Thiruvisaippa, Thiruppallandu   pmuni0092
  Thirumurai 11   the forty works        pmuni0127_01 0127_02 (pmuni0126 is an older copy of 0127_01)
  Thirumurai 12   Periya Puranam         pmuni0209 0215 0218 0224 0225 0226 0227
  Translation     Kausalya Hart, Appar's Thevaram in English, pasurams 1-1000 (4.1-4.104)   pmuni0999
  Commentaries    on Thirumurugattruppadai (11.5.9): Nachinarkkiniyar pmuni0493,
                  S. Vaiyapuri Pillai pmuni0735, Sundara Shanmuganar pmuni0774
  Left out        pmuni0126 (older TSCII-converted copy of pmuni0127_01), pmuni0106 (catalogued as
                  Sambandar's pathigams but holds an essay on the Kuttrala Kuravanji)

Every unit is a verse. Its place comes from the headings (pathigam, poem, purana); its number
within the place is its position there, cross-checked against the number the source prints at
the end of the verse and the running number it prints at the start. Mismatches are printed.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "data" / "text"
OUT = ROOT / "kg" / "core" / "thirumurai.jsonl"

TAMIL = re.compile(r"[஀-௯]")
JUNK = re.compile(r"[௿​-‍﻿]")
# A verse opens with its running number: '12 குறி...', '13. கா...', '004மதி...', or a bare '4.'.
START = re.compile("^(\\d{1,4})(?:\\s*[.,](?!\\d)|\\s+|(?=[\"\u201c\u2018'\\[]?[\u0b80-\u0bef])|$)\\s*(.*)$")
# ... and closes with its place number: '1.1.1', '2.1', '01', '.. 21'.
TRAILER = re.compile(r"^(.*?)[\s.]*(?<![\d(])(\d{1,3}(?:\.\d{1,3}){0,2})\.?\s*$")
MARKERS = ("திருச்சிற்றம்பலம்", "உள்ளுறை அட்டவணை", "பொருள் அடக்கம்", "கொளு", "-----")
FORMS = ("குறுந்தொகை", "நேரிசை", "விராகம்", "தாண்டகம்", "விருத்தம்", "இருக்குக்குறள்",
         "முக்கால்", "இயமகம்", "வினாவுரை", "சக்கரமாற்று", "ஈரடி", "மொழிமாற்று", "மாலைமாற்று",
         "ஏகபாதம்", "கோமூத்திரி", "தாளச்சதி", "பதிகம்", "பத்து", "வைப்பு", "மதிமுத்தம்",
         "தீர்த்தது", "எழுகூற்றிருக்கை", "திருப்பதிகம்")

PROBLEMS = defaultdict(list)


def problem(part, message):
    PROBLEMS[part].append(message)


def body(name):
    text = (TEXT / f"{name}.txt").read_text(encoding="utf-8")
    return JUNK.sub("", text.split("=== BODY ===", 1)[1].split("=== FOOTER ===", 1)[0])


def tamil_text(s):
    return bool(TAMIL.search(s))


def is_marker(s):
    return s.startswith("#") or any(s.startswith(m) for m in MARKERS)


# A footnote marker followed by a space opens a note; one glued to a word marks a verse line.
NOTE_LINE = re.compile(r"^(?:\(\s*\*+\s*\)\s|\(\s*\*+\s|\*+\s|\*+$|\(\s*\*+\s*\)$)")
MARKED_VERSE_LINE = re.compile(r"^(?:\(\*+\)|[*#]+)(?=[஀-௯])")
FLAG = "\x00"


def verses_in(lines, blank_closes=True, bare_start=True, dotted=False):
    """Split a section's lines into verses.

    Returns (verses, other): each verse has start (the printed running number), trailer (the
    printed place number or None), lines and notes; other holds the lines outside verses.
    Footnotes ('(*) ...', '* ...', or a marked paragraph after a verse) go to the verse's notes.
    """
    verses, other, cur, pending, footnote = [], [], None, None, None

    def close():
        nonlocal cur, pending
        if cur and cur["lines"]:
            verses.append(cur)
            pending = cur if not cur["trailer"] else None
        elif cur:
            other.extend(cur["raw"])
        cur = None

    def end_footnote():
        nonlocal footnote
        if footnote is not None and footnote["text"]:
            footnote["verse"]["notes"].append(" ".join(footnote["text"]))
        footnote = None

    for raw in lines:
        s = re.sub(r"^[-–]\s*(?=\d)", "", raw.strip())  # '- 786 வரங்க...'
        s = re.sub(r"(\d)\.{2,}(\d)", r"\1.\2", s)  # '4.71..1'
        if not s:
            if cur and blank_closes and cur["lines"] and not cur.get("long"):
                close()
            continue
        if footnote is not None:
            t = TRAILER.match(s)
            m0 = START.match(s)
            if m0 and tamil_text(m0.group(2)) or is_marker(s):
                end_footnote()
            else:
                if t and "." in t.group(2):
                    footnote["text"].append(t.group(1).strip())
                    footnote["verse"]["trailer"] = t.group(2)
                    end_footnote()
                    pending = None
                else:
                    footnote["text"].append(s.lstrip("*#() ").strip())
                continue
        if is_marker(s) and not MARKED_VERSE_LINE.match(s):
            close()
            pending = None
            other.append(s)
            continue
        if cur is None and pending is not None and (NOTE_LINE.match(s) or MARKED_VERSE_LINE.match(s)):
            footnote = {"verse": pending, "text": []}
            t = TRAILER.match(s)
            if t and "." in t.group(2):
                footnote["text"].append(t.group(1).lstrip("*#() ").strip())
                pending["trailer"] = t.group(2)
                end_footnote()
                pending = None
            else:
                footnote["text"].append(s.lstrip("*#() ").strip())
            continue
        m = START.match(s)
        if m and re.fullmatch(r"\d+\.?", m.group(2)) and bare_start:  # '431 431'
            m = START.match(m.group(1))
        if m and (tamil_text(m.group(2)) or (bare_start and m.group(2) == "")
                  or re.match(r"^-{4,}\s+-{4,}", m.group(2))) \
                and not re.match(r"^(?:\(\s*\d|-(?!---))", m.group(2)):
            close()
            pending = None
            cur = {"start": int(m.group(1)), "trailer": None, "lines": [], "notes": [], "raw": [s]}
            s = m.group(2).strip()
            if not s:
                continue
        if cur is None:
            other.append(s)
            continue
        if NOTE_LINE.match(s):
            note = s
            t = TRAILER.match(s)
            if t and "." in t.group(2):
                note, cur["trailer"] = t.group(1).strip(), t.group(2)
            cur["notes"].append(note.lstrip("*#() ").strip())
            if cur["trailer"]:
                close()
            continue
        # Long poems print a line count every five lines: '... நின்றனை 05', '... (10)'.
        lm = re.match(r"^(.*?[஀-௯].*?)\s*(?:\.{2,})?\s*\(?\s*(?<![.\d])(\d{1,3})\s*\)?\s*$", s)
        if lm and int(lm.group(2)) % 5 == 0 and int(lm.group(2)) == len(cur["lines"]) + 1 \
                and int(lm.group(2)) >= 5:
            cur["lines"].append(lm.group(1).rstrip(" ."))
            cur["long"] = True
            continue
        flag = FLAG if MARKED_VERSE_LINE.match(s) else ""
        s = MARKED_VERSE_LINE.sub("", s)
        t = TRAILER.match(s)
        if t and dotted and "." not in t.group(2):  # a line-end reference mark, not the verse number
            s, t = re.sub(r"\s+\d{1,4}(?:-\d{1,2})?\s*$", "", s), None
        if t and (tamil_text(t.group(1)) or t.group(1) == "") and not re.search(r"\(\s*\d+\s*\)\s*$", s):
            if t.group(1):
                cur["lines"].append(flag + t.group(1).rstrip())
            cur["trailer"] = t.group(2)
            close()
            continue
        cur["lines"].append(flag + s)
    close()
    end_footnote()
    # A marked line can open a footnote inside the verse: lines past the section's usual
    # verse length, in a verse that carries a mark or a note, are the footnote.
    plain = Counter(len(v["lines"]) for v in verses
                    if not v["notes"] and not any(l.startswith(FLAG) for l in v["lines"]))
    if plain:
        usual = plain.most_common(1)[0][0]
        for v in verses:
            marked = v["notes"] or any(l.startswith(FLAG) for l in v["lines"])
            if marked and len(v["lines"]) > usual:
                v["notes"].append(" ".join(l.lstrip(FLAG + "*#() ") for l in v["lines"][usual:]))
                v["lines"] = v["lines"][:usual]
    for v in verses:
        v["lines"] = [l.lstrip(FLAG) for l in v["lines"]]
        # a place number the trailer pattern could not read ('... தாரே.3.1232') is cut off the line
        if v["lines"]:
            m = re.match(r"^(.*[஀-௯)!?])[\s.]*(\d{1,2}(?:\.\d{1,4}){1,2})\.?\s*$", v["lines"][-1])
            if m:
                v["lines"][-1] = m.group(1)
                v["trailer"] = v["trailer"] or m.group(2)
        v["lines"] = [re.sub(r"\s*\(\*+\)\s*|(?<=\S)[*#]+(?=\S)|^[*#]+", "", l).strip() for l in v["lines"]]
        v["lines"] = [l for l in v["lines"] if l]
        v.pop("raw")
        v.pop("long", None)
    return verses, other


def sections(text, heading):
    """Split body text at lines matching heading; returns [(match, lines)]."""
    out, cur = [], None
    for line in text.split("\n"):
        m = heading.match(line.strip())
        if m:
            cur = (m, [])
            out.append(cur)
        elif re.match(r"^#+\s", line) or re.match(r"^#{2,}", line):
            cur = None
        elif cur:
            cur[1].append(line)
    return out


# --------------------------------------------------------------------------- Thevaram

THEVARAM = {1: ("pmuni0150", "pmuni0151"), 2: ("pmuni0157", "pmuni0162"),
            3: ("pmuni0173", "pmuni0179"), 4: ("pmuni0181", "pmuni0182"),
            5: ("pmuni0186", "pmuni0188"), 6: ("pmuni0192", "pmuni0196"),
            7: ("pmuni0207", "pmuni0211")}
POETS = {1: "திருஞானசம்பந்தர்", 2: "திருஞானசம்பந்தர்", 3: "திருஞானசம்பந்தர்",
         4: "திருநாவுக்கரசர்", 5: "திருநாவுக்கரசர்", 6: "திருநாவுக்கரசர்",
         7: "சுந்தரமூர்த்தி நாயனார்"}
PATHIGAM_HEAD = re.compile(r"^#{2,4}\s*(\d)\s*\.\s*0*(\d{1,3})\s*\.?\s*(.*)$")


GENERAL = re.compile(r"பதிகம்$|^தனி|^பொது|^குறைந்த$|^பசுபதி$|^சரக்கறை$|^ஆருயிர்|^நெஞ்சம்|தசபுராணம்|"
                     r"சிவனெனுமோசை|இருக்குக்குறள்$")


def split_title(title):
    """'திருவீழிமிழலை - திருவிராகம்' -> place 'திருவீழிமிழலை', form 'திருவிராகம்'."""
    title = re.sub(r"\(\s*\d+\s*-\s*\d+\s*\)", "", title).replace("*", "").strip(" -")
    parts = [p.strip() for p in re.split(r"\s*-\s*", title) if p.strip()]
    form = None
    if len(parts) > 1 and parts[-1].replace(" ", "").endswith(FORMS):
        form = parts.pop()
    place = " - ".join(parts).replace("()", "").strip()
    if GENERAL.search(place):
        place = None  # a general (பொது) pathigam: the title names the hymn, not a temple
    return place, form


def deity(note_lines):
    text = " ".join(note_lines)
    sw = re.search(r"சுவாமி\s*(?:பெயர்|யின் பெயர்)?\s*[-:–]\s*([^;.,]+)", text)
    dv = re.search(r"தேவி\s*(?:யார்|யின் பெயர்)?\s*[-:–]\s*([^;.,]+)", text)
    return (sw.group(1).strip() if sw else None), (dv.group(1).strip() if dv else None)


def toc_titles(name):
    """The contents list before the first pathigam: '1.14 திருக்கொடுங்குன்றம் (141-151)'."""
    titles = {}
    for line in body(name).split("\n"):
        s = line.strip()
        if s.startswith("###"):
            break
        m = re.match(r"^(\d)\s*\.\s*0*(\d{1,3})\s*\.?\s*([^(]+?)\s*(?:\(.*)?(?:மின்பதிப்பு)?$", s)
        if m:
            titles[(int(m.group(1)), int(m.group(2)))] = m.group(3).replace("மின்பதிப்பு", "").strip()
    return titles


LOST = re.compile(r"சிதை|மறைந்து|கிடைக்க(?:வில்லை|ப்பெற)|காணப்படவில்லை")


def lost_numbers(notes):
    """'... 7,8,9-ம் செய்யுட்கள் சிதைந்து போயின. 5.78.7-9' -> {7, 8, 9}."""
    out = set()
    for n in notes:
        dotted = re.findall(r"\d\.\d{1,3}\.(\d{1,2})(?:\s*-\s*(\d{1,3}))?", n)
        pairs = dotted or re.findall(r"(?<![\d.])(\d{1,2})(?:\s*-\s*(\d{1,2})(?!\d))?", n)
        if dotted:
            pairs += re.findall(r"(?<![\d.])(\d{1,2})(?:\s*-\s*(\d{1,2})(?!\d))?(?=\s*-?\s*ம்)", n)
        for a, b in pairs:
            if b and int(b) > 30 and int(b[0]) > int(a):  # '4.79.6-91' for 6-9
                b = b[0]
            if int(a) <= 30 and (not b or int(b) <= 30):
                out |= set(range(int(a), int(b or a) + 1))
    return out


def number_verses(printed, lost, starts=None):
    """Number a pathigam's verses from the numbers printed at their ends.

    If the printed maximum, less the verses the edition says are lost, accounts for every verse,
    the numbers follow from that (this repairs misprints such as 1,2,6,7,8,6,7,9 with 8 lost).
    Otherwise each verse takes its printed number when it moves forward plausibly, else its position.
    """
    msgs, n = [], len(printed)
    top = n + len(lost) + 1
    fixed, prev = [], 0
    for x in printed:  # '4.16' for 4.1.6, '1.513' for 1.51.3: keep the tail that fits
        if x is not None and x > top:
            tails = [int(str(x)[k:]) for k in range(1, len(str(x)))]
            fit = [t for t in tails if prev < t <= prev + 4]
            x = fit[0] if fit else x
        fixed.append(x)
        prev = x if x is not None and x <= top else prev + 1
    printed = fixed
    real = [x for x in printed if x is not None and x <= 40]
    if real:
        expected = [k for k in range(1, max(real) + 1) if k not in lost]
        if len(expected) == n:
            for k, (x, e) in enumerate(zip(printed, expected), 1):
                if x is None:
                    msgs.append(f"verse {e}: no number printed at its end")
                elif x != e:
                    msgs.append(f"verse {e}: printed as {x}")
            return expected, msgs
    numbers, last = [], 0
    for i, x in enumerate(printed):
        want = last + 1
        if x is None:
            msgs.append(f"verse {want}: no number printed at its end; numbered by position")
            x = want
        elif x > want and set(range(want, x)) <= lost:
            pass
        elif x <= last or x > last + 4:
            msgs.append(f"printed {x} after {last}; numbered {want} by position")
            x = want
        elif x > want:
            # The editions say so when verses are lost; an unexplained gap is a misprint.
            msgs.append(f"verse {want}: printed as {x}; no loss is noted, so numbered by position")
            x = want
        numbers.append(x)
        last = x
    return numbers, msgs


def drop_numbered_footnotes(verses, part, where):
    """A footnote can open with its own number ('4 1 தரைத்தேவர் ...'); fold it into the verse before."""
    kept = []
    for v in verses:
        prev = kept[-1] if kept else None
        if prev and abs(v["start"] - (prev["start"] + 1)) > 5 and not (v["trailer"] and v["trailer"].count(".") == 2):
            prev["notes"].append(" ".join(v["lines"]))
            problem(part, f"{where}: text numbered {v['start']} after verse {prev['start']} read as a footnote")
            continue
        kept.append(v)
    return kept


def toc_ranges(name, book):
    ranges = {}
    for line in body(name).split("\n"):
        if line.startswith("###"):
            break
        m = re.match(r"^\s*(\d)\s*\.\s*0*(\d{1,3})\D.*?\(\s*(\d+)\s*-\s*(\d+)\s*\)", line)
        if m and int(m.group(1)) == book:
            ranges[int(m.group(2))] = (int(m.group(3)), int(m.group(4)))
    return ranges


def parse_thevaram():
    units = []
    for book, files in THEVARAM.items():
        part = f"thevaram {book}"
        found = []  # (pathigam, verse, verse dict, file, heading pathigam, pan)
        groups, lost_by_p = defaultdict(list), defaultdict(set)
        titles, notes_by_p = {}, defaultdict(list)
        for name in files:
            toc = toc_titles(name)
            for (b, p), t in toc.items():
                if b == book:
                    titles.setdefault(p, t)
            for m, lines in sections(body(name), PATHIGAM_HEAD):
                b, ph = int(m.group(1)), int(m.group(2))
                if b != book:
                    problem(part, f"{name}: heading '{m.group(0).strip()}' names book {b}")
                    continue
                title = m.group(3).strip()
                sub = []
                while lines and not lines[0].strip():
                    lines = lines[1:]
                # A line under the heading can carry the form or another name for the place.
                while lines and lines[0].strip() and not START.match(lines[0].strip()) \
                        and not lines[0].strip().startswith(("பண்", "திருச்சிற்றம்பலம்")):
                    sub.append(lines[0].strip().lstrip("*"))
                    lines = lines[1:]
                pan = None
                for l in lines[:6]:
                    pm = re.match(r"^பண்\s*[-:–]\s*(.+)$", l.strip())
                    if pm:
                        pan = pm.group(1).strip()
                body_lines = [l for l in lines if not re.match(r"^\s*பண்\s*[-:–]", l)]
                verses, other = drop_numbered_footnotes(verses_in(body_lines)[0], part, f"{book}.{ph}"), \
                    verses_in(body_lines)[1]
                titles[ph] = title  # the heading wins over the contents list
                lost_notes = [o for o in other if LOST.search(o)]
                for v in verses:
                    lost_notes += [n for n in v["notes"] if LOST.search(n)]
                    v["notes"] = [n for n in v["notes"] if not LOST.search(n)]
                lost = lost_numbers(lost_notes)
                info = {"pan": pan, "sub": sub, "lost": lost,
                        "notes": [o for o in other if not is_marker(o) and tamil_text(o)
                                  and not LOST.search(o)] + lost_notes}
                notes_by_p[ph].append(info)
                sec_p = ph
                for v in verses:
                    tr = [int(x) for x in v["trailer"].split(".")] if v["trailer"] else []
                    if len(tr) == 3 and tr[1] != sec_p:
                        # Trust the printed pathigam only where its own heading is missing.
                        if tr[0] == book and tr[1] == sec_p + 1 and tr[1] not in heads(name):
                            problem(part, f"{name}: no heading for {book}.{tr[1]}; split it off "
                                          f"{book}.{sec_p} by the verse numbers")
                            sec_p = tr[1]
                        else:
                            problem(part, f"{book}.{sec_p}: verse printed as {v['trailer']}")
                    printed = tr[-1] if tr else None
                    groups[sec_p].append((v, printed, name, ph, pan))
                    lost_by_p[sec_p] |= lost
        for p, group in groups.items():
            numbers, msgs = number_verses([g[1] for g in group], lost_by_p[p],
                                          [g[0]["start"] for g in group])
            for m in msgs:
                problem(part, f"{book}.{p}: {m}")
            for vn, (v, printed, name, ph, pan) in zip(numbers, group):
                found.append((p, vn, v, name, ph, pan))
        found.sort(key=lambda x: (x[0], x[1]))
        prev_printed, running = None, 0
        seen = set()
        for p, vn, v, name, ph, pan in found:
            if (p, vn) in seen:
                problem(part, f"{book}.{p}.{vn}: printed twice; kept the first")
                continue
            seen.add((p, vn))
            running += 1
            if prev_printed is not None and v["start"] != prev_printed + 1:
                problem(part, f"{book}.{p}.{vn}: running number printed {v['start']} after {prev_printed}")
            prev_printed = v["start"]
            title = titles.get(p, "")
            thalam, form = split_title(title)
            infos = notes_by_p.get(p, [{}])
            sub = [s for i in infos for s in i.get("sub", [])]
            pnotes = [s for i in infos for s in i.get("notes", [])]
            if not form:
                form = next((s for s in sub if s.replace(" ", "").endswith(FORMS)), None)
            swami, devi = deity(pnotes)
            units.append({
                "id": f"thirumurai:{book}.{p}.{vn}", "thirumurai": book, "pathigam": p, "verse": vn,
                "number": running, "printed_number": v["start"],
                "work": "தேவாரம்", "poet": POETS[book], "thalam": thalam,
                "pathigam_title": title.replace("*", "").strip(), "form": form,
                "pan": pan or next((i["pan"] for i in infos if i.get("pan")), None),
                "swami": swami, "devi": devi, "tamil": v["lines"],
                "notes": v["notes"] or None, "pathigam_notes": pnotes or None,
                "lost_verses": sorted({x for i in infos for x in i.get("lost", ())}) or None,
                "source": name})
        per_p = Counter(u["pathigam"] for u in units if u["thirumurai"] == book)
        for name in files:
            for p, (lo, hi) in toc_ranges(name, book).items():
                if per_p.get(p, 0) != hi - lo + 1:
                    problem(part, f"{book}.{p}: contents list gives {lo}-{hi} ({hi - lo + 1}), "
                                  f"parsed {per_p.get(p, 0)}")
        ps = sorted({p for p, *_ in found})
        missing = sorted(set(range(1, ps[-1] + 1)) - set(ps))
        if missing:
            problem(part, f"pathigams with no verses: {missing}")
    return units


_HEADS = {}


def heads(name):
    if name not in _HEADS:
        _HEADS[name] = {int(m.group(2)) for m, _ in sections(body(name), PATHIGAM_HEAD)}
    return _HEADS[name]


APPENDIX_HEAD = re.compile(r"^(?:#{2,4}\s*)?(\d)\.\s+([஀-௯][^()]*?)\s*$")


def parse_thevaram_appendix():
    """Three pathigams recovered after the canon was fixed, printed after 3.125 in pmuni0179."""
    text = body("pmuni0179").split("### பிற்சேர்க்கை", 1)[1]
    text = text.split("## திருஞானசம்பந்தசுவாமிகள்", 1)[0]
    chunks, cur = [], None
    for line in text.split("\n"):
        s = line.strip()
        m = APPENDIX_HEAD.match(s)
        # '1. திருவிடைவாய்' opens a pathigam; '2. ஒவ்வாத என்பே ...' is a verse (it has a trailer later)
        if m and (s.startswith("#") or cur is None):
            cur = (int(m.group(1)), m.group(2).strip(), [])
            chunks.append(cur)
        elif cur:
            cur[2].append(line)
    units = []
    for k, title, lines in chunks:
        pan = next((re.sub(r"^பண்\s*[-:–]\s*", "", l.strip()) for l in lines
                    if re.match(r"^\s*பண்\s*[-:–]", l)), None)
        verses, other = verses_in([l for l in lines if not re.match(r"^\s*பண்\s*[-:–]", l)])
        numbers, msgs = number_verses([int(v["trailer"].split(".")[-1]) if v["trailer"] else None
                                       for v in verses], set())
        for m in msgs:
            problem("thevaram 3 appendix", f"A{k}: {m}")
        notes = [o for o in other if tamil_text(o) and not is_marker(o)]
        for vn, v in zip(numbers, verses):
            units.append({
                "id": f"thirumurai:3.A{k}.{vn}", "thirumurai": 3, "pathigam": None, "appendix": k,
                "verse": vn, "number": None, "printed_number": v["start"],
                "work": "தேவாரம் (பிற்சேர்க்கை)", "poet": POETS[3], "thalam": title,
                "pathigam_title": title, "pan": pan, "tamil": v["lines"], "notes": v["notes"] or None,
                "pathigam_notes": notes or None, "source": "pmuni0179"})
    return units


# --------------------------------------------------------------------------- Hart (Appar, English)

def parse_hart():
    """Kausalya Hart's English for Appar: '### Padiham N. Place', then pasurams numbered 1-1000."""
    padiham, entries, cur = None, {}, None
    for line in body("pmuni0999").split("\n"):
        s = line.strip()
        m = re.match(r"^###\s*Padiham\s+(\d+)\.?\s*(.*)$", s)
        if m:
            padiham, cur = (int(m.group(1)), m.group(2).strip()), None
            continue
        if padiham is None or not s or s.startswith("---"):
            continue
        m = re.match(r"^(\d{1,4})\s*\.\s*(?=\S)(.*)$", s)
        if m and not TAMIL.search(s):
            n = int(m.group(1))
            if n in entries:
                problem("hart", f"pasuram {n} printed twice; kept the first")
                cur = None
                continue
            cur = entries[n] = {"padiham": padiham[0], "place": padiham[1], "lines": [m.group(2).strip()]}
        elif cur is not None and not s.startswith("#"):
            cur["lines"].append(s)
    missing = sorted(set(range(1, 1001)) - set(entries))
    if missing:
        problem("hart", f"pasurams not found: {missing}")
    return entries


def attach_hart(units):
    """Her running numbers follow the same edition as Project Madurai's Thirumurai 4, so a pasuram
    goes to the Tamil verse with that running number, kept only when that verse lies in her padiham,
    the one after (her padiham 92 covers 4.92 and 4.93, so later ones sit one behind) or, at a
    boundary, the one before."""
    entries = parse_hart()
    by_number = {u["number"]: u for u in units if u["thirumurai"] == 4}
    matched = 0
    for n, e in sorted(entries.items()):
        u = by_number.get(n)
        p = e["padiham"]
        if u is None or u["pathigam"] not in (p - 1, p, p + 1):
            problem("hart", f"pasuram {n} (padiham {p}): no Tamil verse in that place; left out")
            continue
        if u["pathigam"] == p - 1:
            problem("hart", f"pasuram {n}: printed under padiham {p}, matched to {u['id']} by its number")
        if u["pathigam"] == p + 1 and p < 92:
            problem("hart", f"pasuram {n}: printed under padiham {p}, matched to {u['id']} by its number")
        u["hart"] = " ".join(e["lines"])
        matched += 1
    return matched


# --------------------------------------------------------------------------- Thirukkovaiyar (8)

ORDINAL_ATHIKARAM = re.compile(r"^\S+\s*அதிகாரம்\s*$")


def parse_kovaiyar():
    """400 kattalaik kalitturai, each under a numbered turai (situation) title and followed by
    its kolu. The printed verse numbers run out of order in places (34 for 30, 37 twice ...),
    so verses are counted by position and mismatches printed."""
    lines = [l.strip() for l in body("pmuni0054").split("\n")]
    units, iyal, athikaram, n = [], None, None, 0
    i = 0
    while i < len(lines):
        s = lines[i]
        if re.match(r"^(களவியல்|கற்பியல்)", s):
            iyal = re.split(r"[\s(]", s)[0]
        if ORDINAL_ATHIKARAM.match(s) and i + 1 < len(lines):
            m = re.match(r"^(\d+)\s*\.\s*(.+)$", lines[i + 1])
            if m:
                athikaram = (int(m.group(1)), m.group(2).strip())
                i += 2
                continue
        tm = re.match(r"^(\d+)\s*\.?\s*([஀-௯].*)?$", s)
        block, end = [], None
        for size in (4, 5, 3):  # a verse is four lines; a few are broken over five or run to three
            cand = lines[i + 1:i + 1 + size]
            e = re.match(r"^(.*[஀-௯)])[\s.]*?(\d{1,3})\s*$", cand[-1]) if len(cand) == size else None
            if e and all(cand) and all(TAMIL.search(x) for x in cand) \
                    and not any(re.search(r"\d\s*$", x) for x in cand[:-1]):
                block, end = cand, e
                break
        if tm and athikaram and end:
            n += 1
            if int(end.group(2)) != n:
                problem("kovaiyar", f"verse {n}: printed as {end.group(2)}")
            verse = block[:-1] + [end.group(1).rstrip(" .")]
            if len(verse) != 4:
                problem("kovaiyar", f"verse {n}: printed over {len(verse)} lines")
            kolu, k = [], i + 1 + len(block)
            if k < len(lines) and lines[k].startswith("கொளு"):
                k += 1
                while k < len(lines) and lines[k]:
                    kolu.append(re.sub(r"\s*\d+\s*\.?\s*$", "", lines[k]))
                    k += 1
            else:
                problem("kovaiyar", f"verse {n}: no kolu")
            units.append({
                "id": f"thirumurai:8.kovai.{n}", "thirumurai": 8, "pathigam": athikaram[0],
                "verse": n, "number": n, "printed_number": int(end.group(2)),
                "work": "திருக்கோவையார்", "poet": "மாணிக்கவாசகர்", "iyal": iyal,
                "athikaram": athikaram[0], "athikaram_title": athikaram[1],
                "turai_no": int(tm.group(1)), "turai": (tm.group(2) or "").strip() or None,
                "tamil": verse, "kolu": kolu or None, "source": "pmuni0054"})
            i = k
            continue
        i += 1
    if n != 400:
        problem("kovaiyar", f"found {n} verses, expected 400")
    return units


# --------------------------------------------------------------------------- Ninth Thirumurai

NINTH_POET = re.compile(r"^(?:#{2,4}\s*)?(?:(\d+)\.\s*)?(.+?)\s*அருளிய\s*(திருவிசைப்பா|திருப்பல்லாண்டு)\s*"
                        r"\(\s*(\d+)\s*-\s*(\d+)\s*\)\s*$")


def parse_ninth():
    """Poets' sections; pathigam titles ('1. கோயில் - ஒளி வளர் விளக்கே'); verses as a bare running
    number line, the lines, and 'pathigam.verse' at the end."""
    text = body("pmuni0092").split("### ஒன்பதாம் திருமுறை : திருவிசைப்பா", 1)[1]
    lines = text.split("\n")
    poets, cur = [], None
    for line in lines:
        m = NINTH_POET.match(line.strip())
        if m:
            cur = {"poet": m.group(2).strip(), "work": m.group(3),
                   "range": (int(m.group(4)), int(m.group(5))), "lines": []}
            poets.append(cur)
        elif cur is not None:
            cur["lines"].append(line)
    units, running, pathigam_running = [], 0, 0
    for p in poets:
        ls = p["lines"]
        # A title is a line after a blank whose next non-blank line is a bare verse number.
        chunks, title, buf = [], None, []
        for k, line in enumerate(ls):
            s = line.strip()
            nxt = next((x.strip() for x in ls[k + 1:] if x.strip()), "")
            prev_blank = k == 0 or not ls[k - 1].strip()
            if s and prev_blank and TAMIL.search(s) and re.fullmatch(r"\d{1,3}\s*\.?", nxt) \
                    and not re.search(r"\d+\.\d+\s*$", s):
                if title is not None:
                    chunks.append((title, buf))
                title, buf = s, []
            else:
                buf.append(line)
        if title is not None:
            chunks.append((title, buf))
        for k, (title, buf) in enumerate(chunks, 1):
            pathigam_running += 1
            verses, other = verses_in(buf)
            printed = [int(v["trailer"].split(".")[-1]) if v["trailer"] else None for v in verses]
            numbers, msgs = number_verses(printed, set(), [v["start"] for v in verses])
            for m in msgs:
                problem("ninth", f"{p['poet']} pathigam {k}: {m}")
            for v in verses:
                if v["trailer"] and "." in v["trailer"] and int(v["trailer"].split(".")[0]) != k:
                    problem("ninth", f"{p['poet']} pathigam {k}: verse printed as {v['trailer']}")
            ttl = re.sub(r"^\d+\.\s*", "", title).strip()
            place = re.split(r"\s*-+\s*", ttl)[0].strip()
            for vn, v in zip(numbers, verses):
                running += 1
                units.append({
                    "id": f"thirumurai:9.{pathigam_running}.{vn}", "thirumurai": 9,
                    "pathigam": pathigam_running, "verse": vn, "number": running,
                    "printed_number": v["start"], "work": p["work"], "poet": p["poet"],
                    "poet_pathigam": k, "thalam": place, "pathigam_title": ttl,
                    "tamil": v["lines"], "notes": v["notes"] or None, "source": "pmuni0092"})
        got = [u for u in units if u["poet"] == p["poet"] and u["work"] == p["work"]]
        lo, hi = p["range"]
        if len(got) != hi - lo + 1:
            problem("ninth", f"{p['poet']} ({p['work']}): heading gives {lo}-{hi} ({hi - lo + 1}), "
                             f"parsed {len(got)}")
    return units


# --------------------------------------------------------------------------- Eleventh Thirumurai

ELEVENTH_TOC = re.compile(r"^(\d{1,2})\s*\.\s*(\d{1,2})\s+(.+?)\s+(\d{1,3})\s*\(?\s*(\d{1,4})"
                          r"(?:\s*-\s*(\d{1,4}))?\s*\)?\s*$")
ELEVENTH_HEAD = re.compile(r"^(?:#{2,4}\s*)?(\d{1,2})\s*\.\s*(\d{1,2})\.?\s+(.+?)\s*அருளிச்\s*செய்த\s*(.*)$")


def parse_eleventh():
    """Forty-odd works in pmuni0127_01/02, each headed 'P.W <poet> அருளிச் செய்த <title>'; verses
    'N. ...' with N the running number and the verse's place in its work at the end."""
    units, running = [], 0
    for name in ("pmuni0127_01", "pmuni0127_02"):
        lines = body(name).split("\n")
        toc, poets, toc_end = {}, {}, 0
        for k, line in enumerate(lines):
            s = line.strip()
            if ELEVENTH_HEAD.match(s):
                toc_end = k
                break
            m = ELEVENTH_TOC.match(re.sub(r"\(\s+", "(", s))
            if m:
                lo = int(m.group(5))
                hi = int(m.group(6)) if m.group(6) else lo
                toc[(int(m.group(1)), int(m.group(2)))] = (m.group(3).strip(), int(m.group(4)), lo, hi)
                continue
            m = re.match(r"^(\d{1,2})\s*\.?\s+([஀-௯][^(]*?)\s*(?:பாசுரங்கள்)?\s*(?:\(.*)?$", s)
            if m and not re.match(r"^\d+\s*\.\s*\d", s):
                poets[int(m.group(1))] = m.group(2).replace("பாசுரங்கள்", "").strip()
        works, cur = [], None
        for line in lines[toc_end:]:
            s = line.strip()
            m = ELEVENTH_HEAD.match(s)
            if m:
                cur = {"key": (int(m.group(1)), int(m.group(2))), "poet": m.group(3).strip(),
                       "title_line": m.group(4).strip(), "lines": []}
                works.append(cur)
            elif cur is not None:
                if re.match(r"^#{2,4}\s*\d{1,2}\s*\.\s*[஀-௯]", s):  # '### 6. கல்லாடதேவ நாயனார் பாசுரம்'
                    continue
                cur["lines"].append(line)
        for w in works:
            key = w["key"]
            ttl, count, lo, hi = toc.get(key, (w["title_line"], None, None, None))
            body_lines = w["lines"]
            while body_lines and not body_lines[0].strip():
                body_lines = body_lines[1:]
            if body_lines and not START.match(body_lines[0].strip()) and TAMIL.search(body_lines[0]):
                body_lines = body_lines[1:]  # the title, when it runs onto the next line
            body_lines = [l for l in body_lines  # poet headings: '3. ஐயடிகள் ... பாசுரங்கள் (145 -168)'
                          if not re.match(r"^\s*\d{1,2}\s*\.?\s+.*பாசுரங்?க?ள?்?\s*\(", l)]
            raw, other = verses_in(body_lines, blank_closes=False)
            # Verses open with their running number; a smaller number is a section heading inside
            # a long poem ('2 திருச்சீரலைவாய்' in Thirumurugattruppadai) and stays with its poem.
            verses, held = [], []
            for v in raw:
                if abs(v["start"] - (running + len(verses) + 1)) > 3:
                    if verses:
                        verses[-1]["lines"] += v["lines"]
                        verses[-1]["trailer"] = v["trailer"] or verses[-1]["trailer"]
                    else:
                        held += v["lines"]
                    problem("eleventh", f"{key[0]}.{key[1]}: '{v['start']} {v['lines'][0][:30]}' read as a "
                                        f"heading inside a poem, not a verse")
                    continue
                if held:
                    v["lines"] = held + v["lines"]
                    held = []
                verses.append(v)
            printed = [int(v["trailer"].split(".")[-1]) if v["trailer"] else None for v in verses]
            numbers, msgs = number_verses(printed, set(), [v["start"] for v in verses])
            label = f"{key[0]}.{key[1]}"
            for m in msgs:
                problem("eleventh", f"{label} {ttl}: {m}")
            if count is not None and len(verses) != count:
                problem("eleventh", f"{label} {ttl}: contents list gives {count} ({lo}-{hi}), "
                                    f"parsed {len(verses)}")
            for vn, v in zip(numbers, verses):
                running += 1
                units.append({
                    "id": f"thirumurai:11.{label}.{vn}", "thirumurai": 11, "pathigam": None,
                    "work_no": label, "verse": vn, "number": running, "printed_number": v["start"],
                    "work": ttl, "poet": poets.get(key[0], w["poet"]),
                    "tamil": v["lines"], "notes": v["notes"] or None, "source": name})
    return units


# --------------------------------------------------------------------------- Periya Puranam (12)

PURANAM_FILES = ("pmuni0209", "pmuni0215", "pmuni0218", "pmuni0224", "pmuni0225", "pmuni0226",
                 "pmuni0227")
PURANA_HEAD = re.compile(r"^#{2,4}\s*(\d{1,2})\s*\.\s*(\d{1,2})\s*\.?\s+(.+?)\s*$")
SARUKKAM_HEAD = re.compile(r"^#{2,4}\s*(?:சருக்கம்\s*)?(\d{1,2})\s*[.:]?\s*(?:[(/]\s*)?"
                           r"([஀-௯][^()/:]*?சருக்கம்)")


SARUKKAMS = {1: "திருமலைச் சருக்கம்", 2: "தில்லை வாழ் அந்தணர் சருக்கம்", 3: "இலை மலிந்த சருக்கம்",
             4: "மும்மையால் உலகாண்ட சருக்கம்", 5: "திருநின்ற சருக்கம்", 6: "வம்பறா வரிவண்டுச் சருக்கம்",
             7: "வார்கொண்ட வனமுலையாள் சருக்கம்", 8: "பொய்யடிமை இல்லாத புலவர் சருக்கம்",
             9: "கறைக்கண்டன் சருக்கம்", 10: "கடல் சூழ்ந்த சருக்கம்", 11: "பத்தராய்ப் பணிவார் சருக்கம்",
             12: "மன்னிய சீர்ச் சருக்கம்", 13: "வெள்ளானைச் சருக்கம்"}


def parse_puranam():
    """Sarukkam and purana headings; verses 'NNNN ...' ending 'sarukkam.purana.verse'."""
    groups, titles, sarukkams, order = defaultdict(list), {}, {}, []
    for name in PURANAM_FILES:
        text = body(name)
        for line in text.split("\n"):  # contents list: '2.01 தில்லை வாழ் அந்தணர் புராணம் (350-359)'
            s = line.strip()
            if s.startswith("#") and PURANA_HEAD.match(s):
                break
            m = re.match(r"^(\d{1,2})\s*\.\s*(\d{1,2})\s+(.+?)\s*\(", s)
            if m:
                titles.setdefault((int(m.group(1)), int(m.group(2))), m.group(3).strip())
        file_heads = {(int(m.group(1)), int(m.group(2)))
                      for m in (PURANA_HEAD.match(l.strip()) for l in text.split("\n")) if m}
        key, chunk, chunks = None, [], []
        for line in text.split("\n"):
            s = line.strip()
            sm = SARUKKAM_HEAD.match(s)
            pm = PURANA_HEAD.match(s)
            if sm and "முற்றிற்று" not in s and "புராணம்" not in s:
                sarukkams[int(sm.group(1))] = sm.group(2).strip()
            if pm and "முற்றிற்று" not in s and "சருக்கம்" not in pm.group(3):
                chunks.append((key, chunk))
                key = (int(pm.group(1)), int(pm.group(2)))
                titles[key] = re.sub(r"\s*\(.*$", "", pm.group(3)).split("/")[0].strip()
                chunk = []
            elif s.startswith("#") and ("சருக்கம்" in s or "முற்றிற்று" in s):
                chunks.append((key, chunk))
                key, chunk = None, []
            else:
                chunk.append(line)
        chunks.append((key, chunk))
        for key, chunk in chunks:
            verses, other = verses_in(chunk, dotted=True)
            sec = key
            for v in verses:
                tr = [int(x) for x in v["trailer"].split(".")] if v["trailer"] else []
                if len(tr) == 3 and (tr[0], tr[1]) != sec:
                    if sec is None or (tr[0], tr[1]) not in file_heads:
                        if sec is not None:
                            problem("puranam", f"{name}: no heading for {tr[0]}.{tr[1]}; "
                                               f"taken from the verse numbers")
                        sec = (tr[0], tr[1])
                    else:
                        problem("puranam", f"{sec[0]}.{sec[1]}: verse printed as {v['trailer']}")
                hm = re.match(r"^(\d{1,2})\s+(.+?புராணம்)", v["lines"][0]) if len(v["lines"]) == 1 else None
                if hm:  # '11 1 பத்தாராய்ப் பணிவார் புராணம் (4147-4154' heads 11.1 without a '#'
                    titles[(v["start"], int(hm.group(1)))] = hm.group(2).strip()
                    continue
                if sec is None:
                    problem("puranam", f"{name}: '{v['start']} {' '.join(v['lines'])[:40]}' outside any purana "
                                       f"(a contents line); left out")
                    continue
                if sec not in groups:
                    order.append(sec)
                groups[sec].append((v, tr[-1] if tr else None, name))
    units, running = [], 0
    for sec in sorted(order):
        group = []
        for g in groups[sec]:
            if group and g[0]["lines"] == group[-1][0]["lines"]:
                problem("puranam", f"{sec[0]}.{sec[1]}: verse printed {g[0]['start']} repeats the one "
                                   f"before; dropped")
                continue
            group.append(g)
        numbers, msgs = number_verses([g[1] for g in group], set(), [g[0]["start"] for g in group])
        for m in msgs:
            problem("puranam", f"{sec[0]}.{sec[1]}: {m}")
        for vn, (v, printed, name) in zip(numbers, group):
            running += 1
            heading = None
            if v["lines"] and re.match(r"^சுந்தர\s*மூர்த்தி\s*சுவாமிகள்\s*துதி", v["lines"][0]):
                heading, v["lines"] = v["lines"][0], v["lines"][1:]
            units.append({
                "id": f"thirumurai:12.{sec[0]}.{sec[1]}.{vn}", "thirumurai": 12, "pathigam": None,
                "heading": heading,
                "sarukkam": sec[0], "sarukkam_title": SARUKKAMS[sec[0]], "purana": sec[1],
                "purana_title": titles.get(sec) or SARUKKAMS[sec[0]], "verse": vn,
                "number": running, "printed_number": v["start"], "work": "பெரிய புராணம்",
                "poet": "சேக்கிழார்", "tamil": v["lines"], "notes": v["notes"] or None, "source": name})
    return units


# Thirumurugattruppadai (11.5.9) is also the first of the Sangam Pathuppattu, and three editions
# with commentary are in the corpus. The commentary runs over the whole poem, which is one unit
# here, so each goes whole onto the agaval (thirumurai:11.5.9.1); the ten venbas after it are
# later additions that these editions do not comment on.
MURUGU_COMMENTARIES = {"nachinarkkiniyar": "pmuni0493", "vaiyapuri_pillai": "pmuni0735",
                       "sundara_shanmuganar": "pmuni0774"}


def attach_murugu(units):
    agaval = next(u for u in units if u["id"] == "thirumurai:11.5.9.1")
    for field, name in MURUGU_COMMENTARIES.items():
        text = "\n".join(l.strip() for l in body(name).split("\n") if l.strip())
        agaval[field] = {"source": name, "text": text}
    return len(MURUGU_COMMENTARIES)


def main():
    units = parse_thevaram() + parse_thevaram_appendix()
    hart = attach_hart(units)
    units += parse_kovaiyar() + parse_ninth() + parse_eleventh() + parse_puranam()
    attach_murugu(units)
    for u in units:
        u.setdefault("hart", None)
        for field in MURUGU_COMMENTARIES:
            u.setdefault(field, None)
    units.sort(key=lambda u: (u["thirumurai"], u.get("appendix") or 0))  # stable: keeps verse order
    counts = Counter(u["thirumurai"] for u in units)
    places = Counter(b for b, p in {(u["thirumurai"], u.get("pathigam") or u.get("work_no")
                                     or u.get("appendix") or (u.get("sarukkam"), u.get("purana")))
                                    for u in units})
    for b in (9, 11, 12):  # printed running numbers that do not follow on (books 1-7 checked above)
        prev = None
        for u in (x for x in units if x["thirumurai"] == b):
            if prev is not None and u.get("printed_number") != prev + 1:
                problem(f"running numbers {b}", f"{u['id']}: printed {u.get('printed_number')} after {prev}")
            prev = u.get("printed_number") or (prev or 0) + 1
    for b in sorted(counts):
        print(f"thirumurai {b}: units={counts[b]} places={places[b]}")
    print(f"total={len(units)} hart={hart} murugu_commentaries={len(MURUGU_COMMENTARIES)} (on one unit)")
    for part, msgs in PROBLEMS.items():
        print(f"--- {part}: {len(msgs)} problems")
        for m in msgs:
            print("   ", m)
    ids = Counter(u["id"] for u in units)
    dup = [i for i, c in ids.items() if c > 1]
    if dup:
        print("DUPLICATE IDS", dup[:20])
    with open(OUT, "w", encoding="utf-8") as out:
        for u in units:
            out.write(json.dumps(u, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
