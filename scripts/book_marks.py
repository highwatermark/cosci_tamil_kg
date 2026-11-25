#!/usr/bin/env python3
"""Show a chapter of any ingested book, validate its marks, and print a reading index.

  book_marks.py tirumanthiram chapters          list chapters with verse ranges
  book_marks.py tirumanthiram show 12 13        print those chapters' verses and witnesses
  book_marks.py tirumanthiram check [12 13]     validate kg/themes/tirumanthiram/chNNN.json
  book_marks.py index OUT                       one line per marked verse of every finished book
  book_marks.py akananuru show 3                the Sangam books (akananuru, purananuru, pattupattu)
  book_marks.py pattupattu check [1 2]          use the same commands; see SANGAM below
  book_marks.py akananuru check 3 --marks DIR   check DIR/ch003.json instead of kg/themes/akananuru/

Chapters are numbered 1..N in the book's order (BOOKS below says how a record maps to one).
Links may point within the book (an integer) or to another book as "kural:N", "naladiyar:N",
"tirumanthiram:N" or "<book>:N". Long runs of one heading are split into chapters of at most
SPLIT[book] verses, so a marking file stays a manageable size. Verses with no text are not marked. The schema is kg/themes/SCHEMA.md; commentators are listed per book.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "kg" / "core"
THEMES = ROOT / "kg" / "themes"
CONCEPTS = THEMES / "concepts.json"
LINK_TYPES = {"tension", "agrees", "develops", "qualifies", "same_image", "parallel_domain"}
MAX_CONCEPTS = 4
# book: (core file, number field, chapter key fields, chapter title field, witnesses {field: max quote words})
BOOKS = {
    "tirumanthiram": ("tirumanthiram.jsonl", "number", ("tantra", "chapter_no"), "chapter", {}),
    "thiruppugazh": ("thiruppugazh.jsonl", "number", ("heading",), "heading", {}),
    # Siddhar units are keyed by seq (their global order), since the works' own numbers restart and
    # some units are unnumbered; show prints each unit's own id beside it.
    "siddhar": ("siddhar.jsonl", "seq", ("work", "run"), "work_title", {}),
}
SPLIT = {"thiruppugazh": 15, "siddhar": 25}
FINISHED = {"kural": ("kural.jsonl", "verse"), "naladiyar": ("naladiyar.jsonl", "verse"),
            "tirumanthiram": ("tirumanthiram.jsonl", "number"), "thiruppugazh": ("thiruppugazh.jsonl", "number"),
            "siddhar": ("siddhar.jsonl", "seq"), "purananuru": ("purananuru.jsonl", "number"),
            "akananuru": ("akananuru.jsonl", "number")}


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def squeeze(text):
    return re.sub(r"\s+", " ", text or "").strip()


def load(book):
    core, number_field, chapter_fields, title_field, witnesses = BOOKS[book]
    records = [r for r in read_jsonl(CORE / core) if r.get("tamil")]
    runs = []  # consecutive records sharing a chapter key
    for r in records:
        key = tuple(str(r[f]) for f in chapter_fields)
        if not runs or runs[-1][0] != key:
            runs.append((key, []))
        runs[-1][1].append(r)
    size = SPLIT.get(book)
    verses, chapters = {}, {}
    for key, rs in runs:
        blocks = [rs[i:i + size] for i in range(0, len(rs), size)] if size else [rs]
        for i, block in enumerate(blocks, 1):
            c = len(chapters) + 1
            title = block[0][title_field] + (f" ({i}/{len(blocks)})" if len(blocks) > 1 else "")
            chapters[c] = {"title": title, "verses": [], "record": block[0]}
            for r in block:
                n = int(r[number_field])
                verses[n] = r | {"chapter_seq": c}
                chapters[c]["verses"].append(n)
    return verses, chapters, witnesses


def show(book, numbers):
    verses, chapters, witnesses = load(book)
    for c in numbers:
        ch = chapters[c]
        rec = ch["record"]
        where = f"tantra {rec.get('tantra')} {rec.get('tantra_name') or ''}, " if "tantra" in rec else ""
        if "siddhar" in rec:
            where = f"{rec['siddhar']}, {rec['work']}, "
        print(f"# Chapter {c}: {ch['title']} ({where}verses {ch['verses'][0]}-{ch['verses'][-1]})")
        for n in ch["verses"]:
            v = verses[n]
            own = f"  ({v['id']}" + (f", {' / '.join(v['section'])}" if v.get("section") else "") + ")" if "seq" in v else ""
            print(f"\n## {n}{own}\n" + "\n".join(v["tamil"]))
            for field in ("variants", "sengalvaraya_parallels", "corrupt_lines", "corrupt_chars", "heading_variants",
                          "glosses", "variant_notes", "parallels", "attribution"):
                if field == "attribution" and v.get(field) == "traditional":
                    continue
                if v.get(field):
                    print(f"{field.upper()}: {squeeze(json.dumps(v[field], ensure_ascii=False))}")
            for field in witnesses:
                print(f"{field.upper()}:", squeeze(str(v.get(field))) or "(none)")


def target_ok(target, verses, finished):
    if isinstance(target, int):
        return target in verses
    if str(target).startswith("pattupattu:"):
        return pattupattu_range_ok(target)
    m = re.fullmatch(r"([a-z_]+):(\d+)", str(target))
    return bool(m) and m.group(1) in finished and int(m.group(2)) in finished[m.group(1)]


def check(book, numbers):
    verses, chapters, witnesses = load(book)
    finished = {b: {int(r[f]) for r in read_jsonl(CORE / core)} for b, (core, f) in FINISHED.items()}
    vocabulary = {c["id"] for c in json.loads(CONCEPTS.read_text(encoding="utf-8"))}
    marks_dir = THEMES / book
    if not numbers:
        numbers = sorted(int(p.stem[2:]) for p in marks_dir.glob("ch*.json"))
    errors = []
    for c in numbers:
        path = marks_dir / f"ch{c:03d}.json"
        if not path.exists():
            errors.append(f"ch{c}: no marks file"); continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("chapter_no") != c:
            errors.append(f"ch{c}: wrong chapter_no")
        if not data.get("chapter_theme"):
            errors.append(f"ch{c}: no chapter_theme")
        known = set(vocabulary)
        for concept in data.get("new_concepts", []):
            if not all(concept.get(k) for k in ("id", "tamil", "gloss", "label_source")):
                errors.append(f"ch{c}: incomplete new concept {concept}")
            known.add(concept.get("id"))
        expected = {str(n) for n in chapters[c]["verses"]}
        marked = data.get("verses", {})
        if set(marked) != expected:
            errors.append(f"ch{c}: verses differ: {sorted(expected ^ set(marked))[:10]}")
        for key, mark in marked.items():
            where = f"ch{c} verse {key}"
            if not mark.get("reading"):
                errors.append(f"{where}: no reading")
            concepts = mark.get("concepts", [])
            if not 1 <= len(concepts) <= MAX_CONCEPTS:
                errors.append(f"{where}: needs 1 to {MAX_CONCEPTS} concepts")
            errors += [f"{where}: unknown concept {x}" for x in concepts if x not in known]
            for position in mark.get("positions", []):
                name = position.get("by")
                if name not in witnesses:
                    errors.append(f"{where}: unknown commentator {name}"); continue
                quote = squeeze(position.get("quote"))
                if quote not in squeeze(str(verses[int(key)].get(name))) or len(quote.split()) > witnesses[name]:
                    errors.append(f"{where}: bad quote for {name}")
        for link in data.get("links", []):
            where = f"ch{c} link {link.get('a')}-{link.get('b')}"
            if link.get("type") not in LINK_TYPES:
                errors.append(f"{where}: unknown type {link.get('type')}")
            if link.get("a") not in verses or not target_ok(link.get("b"), verses, finished):
                errors.append(f"{where}: unknown verse")
            if not link.get("note"):
                errors.append(f"{where}: no note")
    print("\n".join(errors) if errors else f"{len(numbers)} chapters valid")
    return not errors


def index(out):
    """One line per marked verse of the finished books, for agents linking a new book to them."""
    lines = []
    for book, folder in (("kural", "kural"), ("naladiyar", "naladiyar"), ("tirumanthiram", "tirumanthiram"), ("thiruppugazh", "thiruppugazh")):
        for n in read_jsonl(ROOT / "kg" / folder / "nodes.jsonl"):
            if n["type"] == "Verse":
                lines.append((book, n["number"], n["reading"]))
    concepts = {}
    for folder in ("kural", "naladiyar", "tirumanthiram", "thiruppugazh"):
        for e in read_jsonl(ROOT / "kg" / folder / "edges.jsonl"):
            if e["p"] == "EXPRESSES":
                concepts.setdefault(e["s"], []).append(e["o"].split(":")[1])
    with open(out, "w", encoding="utf-8") as f:
        for book, number, reading in lines:
            f.write(f"{book}:{number} | {', '.join(concepts.get(f'{book}:{number}', []))} | {reading}\n")
    print(f"index: {len(lines)} verses")


# --------------------------------------------------------------------------------------------
# The Sangam books: Akananuru, Purananuru and the Pattupattu
# (docs/sangam-marking-brief.md is the schema; the checks below enforce it)
#
# Akananuru and Purananuru chapters are runs of 20 poem numbers (the Akananuru invocation, poem 0,
# goes with chapter 1); a verse key is the poem number. Pattupattu chapters are runs of at most
# SANGAM_UNITS_MAX reading units of one idyll, balanced in size; a verse key is the unit's full id
# (pattupattu:<poem>:<start>-<end>, the poem's own line numbers). A marker may move a unit boundary
# to a sense break inside the chapter's line span, if the moved unit carries a `unit_note`.

SANGAM = {"akananuru": "akananuru.jsonl", "purananuru": "purananuru.jsonl", "pattupattu": "pattupattu_units.jsonl"}
SANGAM_CHAPTER = 20
SANGAM_UNITS_MAX = 24
UNIT_LINES = (6, 30)          # an adjusted Pattupattu unit must stay within this many lines
PATTU_ID = re.compile(r"pattupattu:(\d+):(\d+)-(\d+)")
AKAM_THINAI = {"kurinji", "mullai", "marutham", "neythal", "paalai", "kaikkilai", "perunthinai"}
PURAM_THINAI = {"vetchi", "karanthai", "vanji", "kaanchi", "uzhinai", "nochchi", "thumbai", "vaakai",
                "paadaan", "pothuviyal", "kaikkilai", "perunthinai"}
LAND_OF = {"kurinji": "kurinji", "mullai": "mullai", "marutham": "marutham", "neythal": "neythal", "paalai": "paalai"}
URI = {"punarthal", "pirithal", "irutthal", "irangal", "oodal"}
EVIDENCE_BASIS = {"uri", "karu", "mutal", "thurai", "content"}
# porul 1.20: தெய்வம் உணாவே மா மரம் புள் பறை செய்தி யாழின் பகுதியொடு ... அவ் வகை பிறவும்
KARU_KINDS = {"deyvam", "unavu", "maa", "maram", "pul", "parai", "seythi", "yaazh", "pira"}
KARU_ROLES = {"scene", "ullurai", "iraicchi", "simile", "ornament", "gift_food", "absent"}
COMPARISON_BASIS = {"vinai", "payan", "mey", "uru"}
COMPARISON_TYPES = {"explicit", "metaphor", "juxtaposition", "ullurai"}
# porul 6.4 to 6.11: the four causes of each of the eight feelings
MEYPPADU = {
    "nakai": {"எள்ளல்", "இளமை", "பேதைமை", "மடன்"},
    "azhugai": {"இளிவு", "இழவு", "அசைவு", "வறுமை"},
    "ilivaral": {"மூப்பு", "பிணி", "வருத்தம்", "மென்மை"},
    "marutkai": {"புதுமை", "பெருமை", "சிறுமை", "ஆக்கம்"},
    "accham": {"அணங்கு", "விலங்கு", "கள்வர்", "இறை"},
    "perumitham": {"கல்வி", "தறுகண்", "புகழ்மை", "கொடை"},
    "vekuli": {"உறுப்பறை", "குடிகோள்", "அலை", "கொலை"},
    "uvagai": {"செல்வம்", "புலன்", "புணர்வு", "விளையாட்டு"},
}
# porul 8.181 (speakers in kalavu), 8.182 (in karpu), 4.52 (go-betweens), plus the heart and the rest
AKAM_PERSONS = {"thalaivan", "thalaivi", "thozhi", "sevili", "nartaay", "paarppaan", "paangan", "paanan",
                "koothan", "virali", "parathai", "arivar", "kandor", "ilaiyar", "virunthinar", "ur",
                "nenju", "pira"}
STAGES = {"kalavu", "karpu", None}
ENTITY_TYPES = {"king", "patron", "battle", "town", "river", "hill", "herostone"}
MARKS_DIR = None              # set by --marks DIR, to check files outside kg/themes/<book>
SANGAM_LINK_BOOKS = ("kural", "naladiyar", "tirumanthiram", "thiruppugazh", "siddhar", "purananuru", "akananuru")
_PATTU_LINES = {}


def pattupattu_poems():
    if not _PATTU_LINES:
        for p in read_jsonl(CORE / "pattupattu.jsonl"):
            _PATTU_LINES[p["number"]] = p
    return _PATTU_LINES


def pattupattu_range_ok(target):
    m = PATTU_ID.fullmatch(str(target))
    if not m:
        return False
    poem, start, end = (int(g) for g in m.groups())
    p = pattupattu_poems().get(poem)
    return bool(p) and 1 <= start <= end <= p["line_count"]


def tamil_only(text):
    return re.sub(r"[^஀-௿]", "", text or "")


def balanced(items, most):
    k = -(-len(items) // most)
    base, extra = divmod(len(items), k)
    out, i = [], 0
    for j in range(k):
        size = base + (1 if j < extra else 0)
        out.append(items[i:i + size])
        i += size
    return out


def load_sangam(book):
    records = [r for r in read_jsonl(CORE / SANGAM[book]) if r.get("tamil")]
    verses, chapters = {}, {}
    if book == "pattupattu":
        poems = pattupattu_poems()
        by_poem = {}
        for u in records:
            by_poem.setdefault(u["number"], []).append(u)
        for n in sorted(by_poem):
            blocks = balanced(by_poem[n], SANGAM_UNITS_MAX)
            for i, block in enumerate(blocks, 1):
                c = len(chapters) + 1
                p = poems[n]
                title = p["title"] + (f" ({i}/{len(blocks)})" if len(blocks) > 1 else "")
                chapters[c] = {"title": title, "verses": [u["id"] for u in block], "record": p,
                               "span": (n, block[0]["start"], block[-1]["end"])}
                for u in block:
                    verses[u["id"]] = u | {"chapter_seq": c}
        return verses, chapters
    for r in records:
        n = int(r["number"])
        c = max(n - 1, 0) // SANGAM_CHAPTER + 1
        if c not in chapters:
            chapters[c] = {"title": "", "verses": [], "record": r}
        chapters[c]["verses"].append(n)
        verses[n] = r | {"chapter_seq": c}
    for c, ch in chapters.items():
        first = next((verses[n] for n in ch["verses"] if verses[n].get("section")), verses[ch["verses"][0]])
        name = first.get("section") or {"purananuru": "புறநானூறு"}.get(book, book)
        ch["title"] = f"{name} {ch['verses'][0]}-{ch['verses'][-1]}"
    return verses, chapters


def sangam_flags(book):
    flags = {}
    for f in read_jsonl(CORE / "sangam_text_flags.jsonl"):
        if f.get("book") == book:
            flags.setdefault(f["id"], []).append(f)
    return flags


def colophon_of(book, v):
    """The colophon facts a mark must copy: the poem's own, or for a Pattupattu unit its idyll's."""
    rec = pattupattu_poems()[v["number"]] if book == "pattupattu" else v
    return {"thinai": rec.get("thinai"), "thurai": rec.get("thurai")}


def show_sangam(book, numbers):
    verses, chapters = load_sangam(book)
    flags = sangam_flags(book)
    for c in numbers:
        ch = chapters[c]
        if book == "pattupattu":
            p = ch["record"]
            n, a, b = ch["span"]
            print(f"# Chapter {c}: {ch['title']} (pattupattu:{n}, lines {a}-{b}, {len(ch['verses'])} units)")
            print(f"COLOPHON (whole poem): thinai: {p.get('thinai')} | thurai: {p.get('thurai')} | "
                  f"poet: {p.get('poet')} | patron: {p.get('patron')} | metre: {p.get('metre')}")
            if p.get("sections"):
                print("SECTIONS: " + "; ".join(f"{s['name']} from line {s['start']}" for s in p["sections"]))
        else:
            print(f"# Chapter {c}: {ch['title']} ({book} poems {ch['verses'][0]}-{ch['verses'][-1]})")
        for key in ch["verses"]:
            v = verses[key]
            if book == "pattupattu":
                print(f"\n## {key}" + (f"  ({v['section']})" if v.get("section") else "") + f"  break score {v['break_score']}")
                first = v["start"]
                own = [f for f in flags.get(v["poem_id"], []) if f.get("line") and v["start"] <= f["line"] <= v["end"]]
            else:
                print(f"\n## {key}  ({v['id']})")
                print(f"COLOPHON: thinai: {v.get('thinai')} | thurai: {v.get('thurai')} | poet: {v.get('poet')} | patron: {v.get('patron')}")
                first = 1
                own = flags.get(v["id"], [])
                if v.get("filled_from_duraisamy_pillai"):
                    print(f"FILLED_FROM_DURAISAMY_PILLAI: lines {v['filled_from_duraisamy_pillai']}")
            for i, line in enumerate(v["tamil"], first):
                print(f"{i:4} {line}")
            for f in own:
                print(f"FLAG {f['kind']}" + (f" line {f['line']}" if f.get("line") else "") + f": {squeeze(f.get('detail'))}")


def check_sangam(book, numbers):
    verses, chapters = load_sangam(book)
    finished = {b: {int(r[f]) for r in read_jsonl(CORE / core)} for b, (core, f) in FINISHED.items()}
    vocabulary = {c["id"] for c in json.loads(CONCEPTS.read_text(encoding="utf-8"))}
    commentary = {}
    if book == "purananuru":  # modern commentary in the core file: marks must not copy it
        commentary = {n: tamil_only((v.get("duraisamy_pillai") or {}).get("commentary")) for n, v in verses.items()}
    marks_dir = MARKS_DIR or THEMES / book
    if not numbers:
        numbers = sorted(int(p.stem[2:]) for p in marks_dir.glob("ch*.json"))
    errors = []
    for c in numbers:
        path = marks_dir / f"ch{c:03d}.json"
        if c not in chapters:
            errors.append(f"ch{c}: no such chapter"); continue
        if not path.exists():
            errors.append(f"ch{c}: no marks file"); continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("chapter_no") != c:
            errors.append(f"ch{c}: wrong chapter_no")
        if not data.get("chapter_theme"):
            errors.append(f"ch{c}: no chapter_theme")
        known = set(vocabulary)
        for concept in data.get("new_concepts", []):
            if not all(concept.get(k) for k in ("id", "tamil", "gloss", "label_source")):
                errors.append(f"ch{c}: incomplete new concept {concept}")
            known.add(concept.get("id"))
        marked = data.get("verses", {})
        texts = check_keys(book, c, chapters[c], verses, marked, errors)
        for key, mark in marked.items():
            if key in texts:
                check_sangam_mark(book, f"ch{c} verse {key}", mark, texts[key], known, errors, commentary.get(texts[key].get("number")))
        own = set(texts)
        for link in data.get("links", []):
            where = f"ch{c} link {link.get('a')}-{link.get('b')}"
            a, b = link.get("a"), link.get("b")
            if link.get("type") not in LINK_TYPES:
                errors.append(f"{where}: unknown type {link.get('type')}")
            if str(a) not in own:
                errors.append(f"{where}: `a` is not a verse of this chapter")
            if not sangam_target_ok(book, b, verses, finished):
                errors.append(f"{where}: unknown verse {b}")
            if str(a) == str(b) or f"{book}:{a}" == str(b):
                errors.append(f"{where}: links a verse to itself")
            if not link.get("note"):
                errors.append(f"{where}: no note")
            teaches = squeeze(link.get("teaches"))
            if len(teaches.split()) < 6:
                errors.append(f"{where}: `teaches` must say in a sentence what the pairing teaches")
            elif teaches == squeeze(link.get("note")):
                errors.append(f"{where}: `teaches` repeats the note")
    print("\n".join(errors) if errors else f"{len(numbers)} chapters valid")
    return not errors


def check_keys(book, c, ch, verses, marked, errors):
    """Match the marked verse keys to the chapter; returns {key: record with text and line numbers}."""
    texts = {}
    if book != "pattupattu":
        expected = {str(n) for n in ch["verses"]}
        if set(marked) != expected:
            errors.append(f"ch{c}: verses differ: {sorted(expected ^ set(marked))[:10]}")
        for key in marked:
            if key in expected:
                v = verses[int(key)]
                texts[key] = v | {"lines": dict(enumerate(v["tamil"], 1)), "colophon": colophon_of(book, v)}
        return texts
    n, lo, hi = ch["span"]
    poem = pattupattu_poems()[n]
    core = set(ch["verses"])
    spans = []
    for key, mark in marked.items():
        m = PATTU_ID.fullmatch(key)
        if not m or int(m.group(1)) != n:
            errors.append(f"ch{c}: {key} is not a unit id of pattupattu:{n}"); continue
        s, e = int(m.group(2)), int(m.group(3))
        spans.append((s, e, key))
        if key not in core:
            if not (UNIT_LINES[0] <= e - s + 1 <= UNIT_LINES[1]):
                errors.append(f"ch{c}: adjusted unit {key} must have {UNIT_LINES[0]}-{UNIT_LINES[1]} lines")
            if not squeeze(mark.get("unit_note") if isinstance(mark, dict) else ""):
                errors.append(f"ch{c}: adjusted unit {key} needs a unit_note saying where the sense break is")
        lines = {i: poem["tamil"][i - 1] for i in range(max(s, 1), min(e, poem["line_count"]) + 1)}
        texts[key] = {"number": n, "lines": lines, "colophon": colophon_of(book, {"number": n})}
    spans.sort()
    at = lo
    for s, e, key in spans:
        if s != at:
            errors.append(f"ch{c}: units must cover lines {lo}-{hi} with no gap or overlap (at {key}, expected start {at})")
            break
        at = e + 1
    else:
        if at != hi + 1:
            errors.append(f"ch{c}: units must cover lines {lo}-{hi}; they stop at {at - 1}")
    return texts


def sangam_target_ok(book, target, verses, finished):
    if isinstance(target, int):
        return book != "pattupattu" and target in verses
    t = str(target)
    if t.startswith("pattupattu:"):
        return pattupattu_range_ok(t)
    m = re.fullmatch(r"([a-z_]+):(\d+)", t)
    return bool(m) and m.group(1) in SANGAM_LINK_BOOKS and int(m.group(2)) in finished[m.group(1)]


def check_sangam_mark(book, where, mark, text, known, errors, commentary):
    err = lambda msg: errors.append(f"{where}: {msg}")
    lines = text["lines"]
    whole = tamil_only(" ".join(lines.values()))

    def on_line(form, line, what):
        if not isinstance(line, int) or line not in lines:
            err(f"{what} {form!r}: line {line} is not a line of this verse")
        elif not tamil_only(form) or tamil_only(form) not in tamil_only(lines[line]):
            err(f"{what} {form!r} is not on line {line}")

    def in_text(words, what):
        for w in words or []:
            if not tamil_only(w) or tamil_only(w) not in whole:
                err(f"{what} {w!r} is not in the verse")

    if not isinstance(mark, dict):
        return err("mark is not an object")
    # house fields
    if not mark.get("reading"):
        err("no reading")
    concepts = mark.get("concepts", [])
    if not 1 <= len(concepts) <= MAX_CONCEPTS:
        err(f"needs 1 to {MAX_CONCEPTS} concepts")
    errors.extend(f"{where}: unknown concept {x}" for x in concepts if x not in known)
    if mark.get("positions") or mark.get("contested"):
        err("no commentary is in the corpus: no positions or contested")
    if commentary:
        for field in ("reading", "nuance"):
            words = squeeze(mark.get(field)).split()
            for i in range(len(words) - 5):
                run = tamil_only("".join(words[i:i + 6]))
                if len(run) > 20 and run in commentary:
                    err(f"{field} repeats the modern commentary"); break
    # colophon: sourced facts, copied exactly
    col = mark.get("colophon")
    if not isinstance(col, dict) or col.get("thinai") != text["colophon"]["thinai"] or col.get("thurai") != text["colophon"]["thurai"]:
        err("colophon must copy the core record's thinai and thurai exactly (null where it has none)")
    # akam / puram, inferred thinai and its evidence
    ap = mark.get("akam_puram")
    if ap not in {"akam", "puram", "mixed"}:
        err("akam_puram must be akam, puram or mixed")
    thinai = mark.get("thinai")
    allowed = AKAM_THINAI if ap == "akam" else PURAM_THINAI if ap == "puram" else AKAM_THINAI | PURAM_THINAI
    if thinai is None:
        if not mark.get("uncertain"):
            err("thinai is null but the verse is not marked uncertain")
    elif thinai not in allowed:
        err(f"thinai {thinai!r} is not a {ap} thinai")
    ev = mark.get("thinai_evidence")
    if thinai is not None:
        if not isinstance(ev, dict) or ev.get("basis") not in EVIDENCE_BASIS or not ev.get("words"):
            err(f"thinai_evidence needs basis ({'/'.join(sorted(EVIDENCE_BASIS))}) and words")
        elif ev.get("basis") != "thurai":
            in_text(ev.get("words"), "thinai_evidence word")
    if not isinstance(mark.get("mixed"), bool):
        err("mixed must be true or false")
    # uri
    uri = mark.get("uri")
    if uri is not None and uri not in URI:
        err(f"unknown uri {uri!r}")
    if ap == "akam" and uri is None:
        err("an akam verse needs an uri")
    if ap == "puram" and uri is not None:
        err("uri is defined only for akam (porul 1.16)")
    # mutal: land, season, hour
    mutal = mark.get("mutal")
    if mutal is not None:
        if not isinstance(mutal, dict) or not isinstance(mutal.get("negated"), bool):
            err("mutal must be null or {land, season, hour, negated}")
        else:
            for k in ("land", "season", "hour"):
                in_text(mutal.get(k), f"mutal.{k} word")
    # karu
    karu = mark.get("karu")
    if not isinstance(karu, list):
        err("karu must be a list (empty if the verse names no native thing)"); karu = []
    roles = {}
    for item in karu:
        if not isinstance(item, dict):
            err("karu item is not an object"); continue
        on_line(item.get("form", ""), item.get("line"), "karu")
        if not item.get("stem"):
            err(f"karu {item.get('form')!r} has no stem")
        if item.get("kind") not in KARU_KINDS:
            err(f"karu {item.get('form')!r}: kind must be one of {sorted(KARU_KINDS)}")
        if item.get("role") not in KARU_ROLES:
            err(f"karu {item.get('form')!r}: role must be one of {sorted(KARU_ROLES)}")
        if item.get("land") is not None and item.get("land") not in LAND_OF:
            err(f"karu {item.get('form')!r}: land must be one of the five landscapes")
        roles.setdefault(item.get("role"), []).append(item)
    if mark.get("mixed") is True and thinai in LAND_OF:
        if not any(i.get("land") and i["land"] != thinai for i in karu if isinstance(i, dict)):
            err("mixed is true but no karu item names another land")
    # comparisons
    comps = mark.get("comparisons")
    if not isinstance(comps, list):
        err("comparisons must be a list"); comps = []
    for comp in comps:
        if not isinstance(comp, dict):
            err("comparison is not an object"); continue
        basis = comp.get("basis")
        bases = basis if isinstance(basis, list) else [basis]
        if not 1 <= len(bases) <= 2 or any(b not in COMPARISON_BASIS for b in bases):
            err(f"comparison basis must be one or two of {sorted(COMPARISON_BASIS)} (porul 7.1, 7.2)")
        if comp.get("type") not in COMPARISON_TYPES:
            err(f"comparison type must be one of {sorted(COMPARISON_TYPES)}")
        in_text([comp.get("vehicle", "")], "comparison vehicle")
        marker = comp.get("marker")
        if comp.get("type") == "explicit":
            if not marker or marker == "none":
                err("an explicit comparison needs its marker")
            else:  # a vowel-initial marker loses its vowel in sandhi (இயன்றன்ன = இயன்று + அன்ன)
                core = tamil_only(marker)
                if core[:1] in "அஆஇஈஉஊஎஏஐஒஓஔ":
                    core = core[1:]
                if not core or core not in whole:
                    err(f"comparison marker {marker!r} is not in the verse")
        elif marker not in (None, "none"):
            err(f"a {comp.get('type')} comparison has no marker; use explicit")
        if not comp.get("tenor"):
            err("comparison has no tenor")
    if roles.get("simile") and not any(isinstance(x, dict) and x.get("type") == "explicit" for x in comps):
        err("a karu item has role simile but no explicit comparison is listed")
    # meyppadu: at most two, each with a cause from porul 6.4-6.11
    meyp = mark.get("meyppadu")
    if not isinstance(meyp, list) or len(meyp) > 2:
        err("meyppadu must be a list of at most two"); meyp = []
    for m in meyp:
        if not isinstance(m, dict) or m.get("feeling") not in MEYPPADU:
            err(f"meyppadu feeling must be one of {sorted(MEYPPADU)}"); continue
        if m.get("cause") not in MEYPPADU[m["feeling"]]:
            err(f"meyppadu {m['feeling']}: cause must be one of {sorted(MEYPPADU[m['feeling']])}")
    # akam thurai as a speech situation
    ta = mark.get("thurai_akam")
    if ap in ("akam", "mixed") and book != "pattupattu" and not ta:
        err("an akam verse needs thurai_akam")
    for t in ta or []:
        if not isinstance(t, dict):
            err("thurai_akam item is not an object"); continue
        for k in ("speaker", "addressee"):
            if t.get(k) not in AKAM_PERSONS:
                err(f"thurai_akam {k} must be one of {sorted(AKAM_PERSONS)}")
        if t.get("overhearer") is not None and t.get("overhearer") not in AKAM_PERSONS:
            err("thurai_akam overhearer must be null or a person code")
        occ = t.get("occasion")
        if not isinstance(occ, dict) or occ.get("stage") not in STAGES:
            err("thurai_akam occasion needs stage (kalavu, karpu or null) and words")
        elif occ.get("words") and text["colophon"]["thurai"]:
            if tamil_only(occ["words"]) not in tamil_only(text["colophon"]["thurai"]):
                err("thurai_akam occasion words must be copied from the colophon thurai")
    # puram thurai, normalised, with the colophon form it came from
    pt = mark.get("puram_thurai")
    if ap in ("puram", "mixed") and pt is None:
        err("a puram verse needs puram_thurai (an empty list when the colophon has none)")
    for t in pt or []:
        if not isinstance(t, dict) or not t.get("name"):
            err("puram_thurai item needs a name"); continue
        form = t.get("colophon_form")
        if form is not None and tamil_only(form) not in tamil_only(text["colophon"]["thurai"] or ""):
            err(f"puram_thurai colophon_form {form!r} is not in the colophon")
    # named entities
    for ent in mark.get("entities") or []:
        if not isinstance(ent, dict) or ent.get("type") not in ENTITY_TYPES:
            err(f"entity type must be one of {sorted(ENTITY_TYPES)}"); continue
        on_line(ent.get("name", ""), ent.get("line"), f"entity {ent['type']}")
    # experimental: ullurai and iraicchi
    ul = mark.get("ullurai")
    if ul is not None:
        if not isinstance(ul, dict) or ul.get("experimental") is not True:
            err("ullurai must be null or an object with experimental: true")
        else:
            if ap == "puram":
                err("ullurai is an akam device (porul 1.49); a puram verse's hidden image goes in comparisons")
            vehicle = ul.get("vehicle") or []
            if not vehicle:
                err("ullurai needs its vehicle")
            for v in vehicle:
                on_line((v or {}).get("form", ""), (v or {}).get("line"), "ullurai vehicle")
                if not any(tamil_only(v.get("form", "")) == tamil_only(k.get("form", "")) for k in roles.get("ullurai", [])):
                    err(f"ullurai vehicle {v.get('form')!r} must also be a karu item with role ullurai")
            if any(k.get("kind") == "deyvam" for k in roles.get("ullurai", [])):
                err("a deity cannot carry ullurai (porul 1.50)")
            pairs = ul.get("pairs") or []
            if len(pairs) < 2 or not all(isinstance(p, dict) and p.get("scene") and p.get("situation") for p in pairs):
                err("ullurai needs at least two pairs of {scene, situation}")
            for p in pairs:
                if isinstance(p, dict) and p.get("scene"):
                    in_text([p["scene"]], "ullurai pair scene")
            anchor = ul.get("anchor") or ""
            source = whole + tamil_only(text["colophon"]["thurai"] or "")
            if not tamil_only(anchor) or tamil_only(anchor) not in source:
                err("ullurai anchor must be Tamil words from the verse or its colophon thurai that name the tenor's situation")
            if not ul.get("tenor") or not ul.get("speaker_fit"):
                err("ullurai needs tenor and speaker_fit (porul 7.26-7.29)")
    elif roles.get("ullurai"):
        err("a karu item has role ullurai but ullurai is null")
    ir = mark.get("iraicchi")
    if ir is not None:
        if not isinstance(ir, dict) or ir.get("experimental") is not True:
            err("iraicchi must be null or an object with experimental: true")
        else:
            if ap == "puram":
                err("iraicchi stands beside the uri of akam (porul 5.33); not on a puram verse")
            car = ir.get("carrier") or {}
            on_line(car.get("form", ""), car.get("line"), "iraicchi carrier")
            if not any(tamil_only(car.get("form", "")) == tamil_only(k.get("form", "")) for k in roles.get("iraicchi", [])):
                err("iraicchi carrier must also be a karu item with role iraicchi")
            if ir.get("deletion_test") is not True:
                err("iraicchi needs deletion_test: true (the stated sense survives without the carrier)")
            if not ir.get("sense") or not ir.get("act"):
                err("iraicchi needs act (what the thing does) and sense (what it implies for the people)")
    elif roles.get("iraicchi"):
        err("a karu item has role iraicchi but iraicchi is null")
    if ul and ir and isinstance(ul, dict) and isinstance(ir, dict):
        if any(tamil_only((ir.get("carrier") or {}).get("form", "")) == tamil_only((v or {}).get("form", "")) for v in ul.get("vehicle") or []):
            err("one thing cannot be both the ullurai vehicle and the iraicchi carrier")


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    if sys.argv[1] == "index":
        return index(sys.argv[2])
    if "--marks" in sys.argv:  # check a Sangam chapter kept elsewhere (e.g. a test in the scratchpad)
        global MARKS_DIR
        i = sys.argv.index("--marks")
        MARKS_DIR = Path(sys.argv[i + 1])
        del sys.argv[i:i + 2]
    book, command, numbers = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3:]]
    if book in SANGAM:
        if command == "chapters":
            _, chapters = load_sangam(book)
            for c, ch in chapters.items():
                print(f"{c}\t{ch['verses'][0]} .. {ch['verses'][-1]}\t{len(ch['verses'])}\t{ch['title']}")
        elif command == "show":
            show_sangam(book, numbers)
        elif command == "check":
            sys.exit(0 if check_sangam(book, numbers) else 1)
        return
    if command == "chapters":
        _, chapters, _ = load(book)
        for c, ch in chapters.items():
            print(f"{c}\t{ch['verses'][0]}-{ch['verses'][-1]}\t{len(ch['verses'])}\t{ch['title']}")
    elif command == "show":
        show(book, numbers)
    elif command == "check":
        sys.exit(0 if check(book, numbers) else 1)


if __name__ == "__main__":
    main()
