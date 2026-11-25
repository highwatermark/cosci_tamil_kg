#!/usr/bin/env python3
"""Show a chapter of any ingested book, validate its marks, and print a reading index.

  book_marks.py tirumanthiram chapters          list chapters with verse ranges
  book_marks.py tirumanthiram show 12 13        print those chapters' verses and witnesses
  book_marks.py tirumanthiram check [12 13]     validate kg/themes/tirumanthiram/chNNN.json
  book_marks.py index OUT                       one line per marked verse of every finished book
  book_marks.py akananuru show 3                the Sangam books (akananuru, purananuru, pattupattu)
  book_marks.py pattupattu check [1 2]          use the same commands; see SANGAM below
  book_marks.py akananuru check 3 --marks DIR   check DIR/ch003.json instead of kg/themes/akananuru/
  book_marks.py kuruntokai show 1               the rest of Ettuthogai, the Pathinenkilkanakku and the
  book_marks.py silappathikaram check 3         epics use the same commands; see NEW below for each
                                                book's field set (akam, puram, devotional, ethics,
                                                narrative) and chapters

Chapters are numbered 1..N in the book's order (BOOKS below says how a record maps to one).
Links may point within the book (a number, as 13 or "13") or to another book as "kural:N", "naladiyar:N",
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


def within(target):
    """A within-book link target: an integer, or the same number as a digit string ("13")."""
    return (isinstance(target, int) and not isinstance(target, bool)) or (isinstance(target, str) and target.isdigit())


def target_ok(target, verses, finished):
    if within(target):
        return int(target) in verses
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
    """One line per marked verse of every marked book, for agents linking a new book to them.

    Books with a built graph (kg/<book>/nodes.jsonl) are read from it; every other book is read from
    its marking files, kg/themes/<book>/chNNN.json, for each book this script registers (the Siddhar
    songs, the Sangam books and the NEW books). The key is the one a link uses: <book>:<key>.
    """
    lines, concepts, graphed = [], {}, []
    for folder in ("kural", "naladiyar", "tirumanthiram", "thiruppugazh"):
        if not (ROOT / "kg" / folder / "nodes.jsonl").exists():
            continue
        graphed.append(folder)
        for n in read_jsonl(ROOT / "kg" / folder / "nodes.jsonl"):
            if n["type"] == "Verse":
                lines.append((f"{folder}:{n['number']}", n["reading"]))
        for e in read_jsonl(ROOT / "kg" / folder / "edges.jsonl"):
            if e["p"] == "EXPRESSES":
                concepts.setdefault(e["s"], []).append(e["o"].split(":")[1])
    counts = {b: sum(1 for k, _ in lines if k.startswith(b + ":")) for b in graphed}
    for book in [*BOOKS, *SANGAM, *NEW]:
        if book in graphed or not (THEMES / book).is_dir():
            continue
        n = 0
        for path in sorted((THEMES / book).glob("ch[0-9]*.json")):
            try:
                marked = json.loads(path.read_text(encoding="utf-8")).get("verses", {})
            except json.JSONDecodeError:
                print(f"index: skipped {path} (not valid JSON)", file=sys.stderr); continue
            for key, mark in marked.items():
                if not isinstance(mark, dict):
                    continue
                ref = key if key.startswith(f"{book}:") else f"{book}:{key}"
                lines.append((ref, squeeze(mark.get("reading"))))
                concepts[ref] = [c for c in mark.get("concepts") or [] if isinstance(c, str)]
                n += 1
        if n:
            counts[book] = n
    with open(out, "w", encoding="utf-8") as f:
        for ref, reading in lines:
            f.write(f"{ref} | {', '.join(concepts.get(ref, []))} | {reading}\n")
    print(f"index: {len(lines)} verses (" + ", ".join(f"{b} {n}" for b, n in counts.items()) + ")")


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
    if within(target):
        return book != "pattupattu" and int(target) in verses
    t = str(target)
    if t.startswith("pattupattu:"):
        return pattupattu_range_ok(t)
    m = re.fullmatch(r"([a-z_]+):(\d+)", t)
    if bool(m) and m.group(1) in SANGAM_LINK_BOOKS and int(m.group(2)) in finished[m.group(1)]:
        return True
    return new_target_ok(t)  # a verse of one of the newly registered books (NEW below)


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
    if ap in ("akam", "mixed") and book not in NO_THURAI_AKAM and not ta:
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


# --------------------------------------------------------------------------------------------
# The rest of Ettuthogai, the Pathinenkilkanakku and the epics (docs/corpus-groups.md)
#
# Every book below has a FIELD SET, which says what a verse mark holds and what check enforces:
#
#   akam        exactly the Akananuru fields (docs/sangam-marking-brief.md); `colophon` copies the
#               core record's thinai and thurai (for the Pathinenkilkanakku akam works the thinai
#               is the section the work files the verse under; thurai is null where there is none)
#   puram       exactly the Purananuru fields
#   devotional  the Sangam fields without the thurai_akam requirement (Paripadal). A song may be
#               marked whole (key "5", "thirattu:1") or, because the songs are long, as reading
#               units the marker cuts: keys "paripadal:<song>:<start>-<end>" that cover the song's
#               lines 1..N with no gap or overlap, each UNIT_LINES long (6-30; a song too short to
#               cut is marked whole). A song is marked either whole or in units, not both.
#   ethics      docs/ethics-marking-brief.md: house fields, `domain` (+ `domain_note`), `items`
#               [{thing, claim, line, domain?}] and `count_word` for the counted works (a count
#               that differs from ITEM_COUNTS is a warning, not an error), `pazhamozhi` {proverb,
#               lines, literal, story {kind, who, act, tradition?}, applied_to} for Pazhamozhi,
#               `norm` {historical, kinds, note}; link extras `item` and `list_adds` (required on
#               links to the Kural or Naladiyar)
#   narrative   docs/epic-marking-brief.md: house fields, `speaker` {who, form, line, addressee},
#               `agents` [{id, form, line}], `event`, `claims` [{claim, school, school_detail?,
#               line, stance, voiced_by}], `echoes` [{b, line, words, kind, marked}], a chapter-level
#               `cast` [{id, tamil, role}] that defines every id used; link extra `gains` {a, b}
#               (required on links outside the epics)
#
# A verse key is the part of the core id after "<book>:" ("12", "0b", "payiram", "patikam:2",
# "thirattu:3"). Silappathikaram and Manimekalai are marked by the reading units of their
# _units files, keyed by the full unit id ("silappathikaram:3:1-24"), one chapter per kaathai
# (split into balanced chapters of at most SANGAM_UNITS_MAX units); as for the Pattupattu a
# marker may move a unit boundary inside the chapter, with a `unit_note`. Links may point to any
# verse of any book here as "<book>:<key>", or to a line span of a unit book or a Paripadal song
# as "<book>:<record>:<start>-<end>". Every link needs `note` and `teaches` as in the Sangam brief.

# book: (field set, chapter scheme). Schemes: ("number", 20) runs of 20 verse numbers (invocation
# and payiram in chapter 1; a stray last run under 5 verses joins the one before); ("key", fields,
# most, keep) runs of the key fields, a run longer than `keep` split into balanced chapters of at
# most `most`; ("songs",) Paripadal; ("units",) one kaathai; ("whole",) the book is one chapter.
NEW = {
    "natrinai": ("akam", ("number", 20)),
    "kuruntokai": ("akam", ("number", 20)),
    "ainkurunuru": ("akam", ("key", ("decade",), 10, 10)),
    "kalittokai": ("akam", ("key", ("section",), 20, 20)),
    "patitruppattu": ("puram", ("key", ("decade",), 11, 11)),
    "paripadal": ("devotional", ("songs",)),
    "kar_narpathu": ("akam", ("key", ("section",), 24, 30)),
    "ainthinai_aimpathu": ("akam", ("key", ("section",), 24, 30)),
    "thinaimozhi_aimpathu": ("akam", ("key", ("section",), 24, 30)),
    "ainthinai_ezhupathu": ("akam", ("key", ("section",), 24, 30)),
    "thinaimalai_nootraimpathu": ("akam", ("key", ("section",), 24, 30)),
    "kainnilai": ("akam", ("key", ("section",), 24, 30)),
    "kalavazhi_narpathu": ("puram", ("number", 20)),
    "nanmanikkadigai": ("ethics", ("number", 20)),
    "innaa_narpathu": ("ethics", ("number", 20)),
    "iniyavai_narpathu": ("ethics", ("number", 20)),
    "thirikadugam": ("ethics", ("number", 20)),
    "acharakkovai": ("ethics", ("number", 20)),
    "pazhamozhi_nanooru": ("ethics", ("key", ("chapter_no",), 20, 20)),
    "sirupanchamoolam": ("ethics", ("number", 20)),
    "muthumozhikkanchi": ("ethics", ("key", ("section_no",), 10, 10)),
    "elathi": ("ethics", ("number", 20)),
    "silappathikaram": ("narrative", ("units",)),
    "manimekalai": ("narrative", ("units",)),
    "civaka_cintamani": ("narrative", ("key", ("section_number",), 25, 25)),
    "soolamani": ("narrative", ("key", ("section_number",), 25, 25)),
    "neelakesi": ("narrative", ("key", ("section_number",), 25, 25)),
    "naga_kumara_kaviyam": ("narrative", ("key", ("section_number",), 25, 25)),
    "udayana_kumara_kaviyam": ("narrative", ("key", ("section_number",), 25, 25)),
    "yasodhara_kaviyam": ("narrative", ("key", ("section_number",), 25, 25)),
    "valayapathi": ("narrative", ("key", (), 25, 25)),     # the epic brief: runs of 25
    "kundalakesi": ("narrative", ("whole",)),
}
NO_THURAI_AKAM = {"pattupattu", "paripadal"}   # Sangam-field books where thurai_akam is not required
# ethics brief, "Expected counts": items per verse (a differing count warns); None = items optional
ITEM_COUNTS = {"thirikadugam": {3}, "nanmanikkadigai": {4}, "innaa_narpathu": {4}, "iniyavai_narpathu": {3, 4},
               "sirupanchamoolam": {5, 6}, "elathi": {6, 5}, "muthumozhikkanchi": {1}}
DOMAINS = {"king", "householder", "ascetic", "all", "ritual-conduct"}
NORM_KINDS = {"purity", "caste", "gender", "ritual", "diet"}
STORY_KINDS = {"named", "exemplum", "general"}
SCHOOLS = {"jain", "buddhist", "vedic", "saiva", "vaishnava", "ajivika", "general", "lokayata"}
SCHOOL_DETAILS = {"sankhya", "vaisheshika", "nyaya", "mimamsa", "vedanta", "lokayata"}
STANCES = {"asserted", "refuted", "reported"}
ECHO_KINDS = {"quote", "echo"}
CAST_ID = re.compile(r"[a-z][a-z0-9_]*")
INTRO_KINDS = {"invocation", "payiram"}         # with no section of their own, they join the nearest run
SONG_LINES = 150                                # a Paripadal chapter: at most two songs, at most this many lines
SHORT_SONG = 15                                 # fragments shorter than this are grouped together
_NEW_CACHE = {}


def key_of(book, record):
    return str(record["id"]).split(":", 1)[1]


def core_records(book):
    if book not in _NEW_CACHE:
        _NEW_CACHE[book] = [r for r in read_jsonl(CORE / f"{book}.jsonl") if r.get("tamil")]
    return _NEW_CACHE[book]


def unit_records(book):
    if (book, "units") not in _NEW_CACHE:
        _NEW_CACHE[(book, "units")] = [u for u in read_jsonl(CORE / f"{book}_units.jsonl") if u.get("tamil")]
    return _NEW_CACHE[(book, "units")]


def new_title(book, rec, first, last):
    if book == "patitruppattu":
        return f"{rec['decade']}ஆம் பத்து, {rec.get('patron') or ''}".strip(", ") if rec.get("decade") else "fragments"
    if book == "ainkurunuru":
        return " ".join(x for x in (rec.get("section"), rec.get("decade_title"), f"decade {rec.get('decade')}") if x)
    name = rec.get("chapter") or rec.get("section") or rec.get("title") or book
    return f"{name} {first}-{last}" if first != last else str(name)


def load_new(book):
    """{key: verse record with chapter_seq}, {chapter: {title, verses, record[, span]}}."""
    if ("loaded", book) in _NEW_CACHE:
        return _NEW_CACHE[("loaded", book)]
    scheme = NEW[book][1]
    verses, chapters = {}, {}

    def add(block, title, record, span=None, keys=None):
        c = len(chapters) + 1
        keys = keys or [key_of(book, r) for r in block]
        chapters[c] = {"title": title, "verses": keys, "record": record} | ({"span": span} if span else {})
        for k, r in zip(keys, block):
            verses[k] = r | {"chapter_seq": c}

    records = core_records(book)
    if scheme[0] == "units":
        by_record, core = {}, {r["id"]: r for r in records}
        for u in unit_records(book):
            by_record.setdefault(u["record_id"], []).append(u)
        for rid, units in by_record.items():
            rec = core[rid]
            blocks = balanced(units, SANGAM_UNITS_MAX)
            for i, block in enumerate(blocks, 1):
                title = rec["title"] + (f" ({i}/{len(blocks)})" if len(blocks) > 1 else "")
                add(block, title, rec, (key_of(book, rec), block[0]["start"], block[-1]["end"]), [u["id"] for u in block])
    elif scheme[0] == "songs":
        groups = []
        for r in records:
            short = r["line_count"] < SHORT_SONG
            g = groups[-1] if groups else None
            if g and g["short"] and short and len(g["rs"]) < 20:
                g["rs"].append(r)
            elif g and not g["short"] and not short and len(g["rs"]) < 2 and g["lines"] + r["line_count"] <= SONG_LINES:
                g["rs"].append(r)
            else:
                groups.append({"short": short, "rs": [r], "lines": 0})
            groups[-1]["lines"] += r["line_count"]
        for g in groups:
            rs = g["rs"]
            add(rs, " / ".join(dict.fromkeys(r.get("title") or "திரட்டு" for r in rs)) + f" ({', '.join(key_of(book, r) for r in rs)})", rs[0])
    elif scheme[0] == "whole":
        add(records, records[0].get("section") or book, records[0])
    elif scheme[0] == "number":
        size = scheme[1]
        runs = {}
        for r in records:  # an invocation or payiram (number 0 or none) goes with chapter 1
            runs.setdefault(max(int(r["number"] or 0) - 1, 0) // size, []).append(r)
        blocks = [runs[k] for k in sorted(runs)]
        if len(blocks) > 1 and len(blocks[-1]) < 5:  # a stray last poem (Kuruntokai 401) joins the run before
            tail = blocks.pop()
            blocks[-1] = blocks[-1] + tail
        for block in blocks:
            nums = [key_of(book, r) for r in block if r.get("number") is not None]
            add(block, f"{block[0].get('title') or book} {nums[0]}-{nums[-1]}", block[0])
    else:
        _, fields, most, keep = scheme
        keys = [tuple(r.get(f) for f in fields) for r in records]
        if fields:  # an invocation or payiram with no section joins the nearest run (the next, else the last)
            real = [i for i, r in enumerate(records) if not (r.get("kind") in INTRO_KINDS and all(x is None for x in keys[i]))]
            for i, r in enumerate(records):
                if i not in real and real:
                    j = next((j for j in real if j > i), real[-1])
                    keys[i] = keys[j]
        runs = []
        for k, r in zip(keys, records):
            if not runs or runs[-1][0] != k:
                runs.append((k, []))
            runs[-1][1].append(r)
        for k, rs in runs:
            blocks = [rs] if len(rs) <= keep else balanced(rs, most)
            rec = next((r for r in reversed(rs) if r.get("kind") not in INTRO_KINDS), rs[0])
            for i, block in enumerate(blocks, 1):
                title = new_title(book, rec, key_of(book, block[0]), key_of(book, block[-1]))
                add(block, title + (f" ({i}/{len(blocks)})" if len(blocks) > 1 else ""), rec)
    _NEW_CACHE[("loaded", book)] = (verses, chapters)
    return verses, chapters


def new_keys(book):
    """Every verse key of a registered book, and its line-addressable records {record key: line count}."""
    if ("keys", book) not in _NEW_CACHE:
        records = core_records(book)
        _NEW_CACHE[("keys", book)] = ({key_of(book, r) for r in records},
                                       {key_of(book, r): r["line_count"] for r in records})
    return _NEW_CACHE[("keys", book)]


def span_ok(book, rest):
    """rest = "<record>:<start>-<end>", a line span inside a record of a unit book or a Paripadal song."""
    m = re.fullmatch(r"(.+):(\d+)-(\d+)", rest)
    if not m or book not in NEW or NEW[book][1][0] not in ("units", "songs"):
        return False
    count = new_keys(book)[1].get(m.group(1))
    return bool(count) and 1 <= int(m.group(2)) <= int(m.group(3)) <= count


def new_target_ok(target):
    m = re.fullmatch(r"([a-z_]+):(.+)", str(target))
    if not m or m.group(1) not in NEW:
        return False
    book, rest = m.groups()
    return rest in new_keys(book)[0] or span_ok(book, rest)


def new_text(book, key, v):
    """The record a mark is checked against: lines numbered as show prints them, and the colophon."""
    rec = v
    if NEW[book][1][0] == "units":
        rec = next(r for r in core_records(book) if r["id"] == v["record_id"])
        lines = {i: rec["tamil"][i - 1] for i in range(v["start"], v["end"] + 1)}
    else:
        lines = dict(enumerate(v["tamil"], 1))
    return {"number": None, "kind": v.get("kind"), "lines": lines,
            "colophon": {"thinai": rec.get("thinai"), "thurai": rec.get("thurai")}}


def show_new(book, numbers):
    verses, chapters = load_new(book)
    flags = sangam_flags(book)
    fields, scheme = NEW[book][0], NEW[book][1][0]
    for c in numbers:
        ch = chapters[c]
        rec = ch["record"]
        if scheme == "units":
            rk, a, b = ch["span"]
            print(f"# Chapter {c}: {ch['title']} ({book}:{rk}, lines {a}-{b}, {len(ch['verses'])} units)")
            print(f"KAATHAI: {rec.get('title')} | kandam: {rec.get('kandam') or '-'} | lines {rec['line_count']}"
                  f" (printed last line {rec.get('printed_last_line')})")
            if rec.get("blocks"):
                print("BLOCKS: " + "; ".join(f"{x.get('label') or '-'} {x['start']}-{x['end']}" for x in rec["blocks"]))
        else:
            print(f"# Chapter {c}: {ch['title']} ({book} {ch['verses'][0]} .. {ch['verses'][-1]}, {len(ch['verses'])} verses)"
                  + f"  [field set: {fields}]")
        for key in ch["verses"]:
            v = verses[key]
            if scheme == "units":
                print(f"\n## {key}  ({v.get('block_label') or v.get('kind')})  break score {v['break_score']}")
                first, own = v["start"], [f for f in flags.get(v["record_id"], []) if f.get("line") and v["start"] <= f["line"] <= v["end"]]
            else:
                print(f"\n## {key}  ({v['id']}, {v.get('kind') or 'verse'})")
                first, own = 1, flags.get(v["id"], [])
                if fields in ("akam", "puram", "devotional"):
                    print(f"COLOPHON: thinai: {v.get('thinai')} | thurai: {v.get('thurai')} | poet: {v.get('poet') or v.get('author')}"
                          f" | patron: {v.get('patron')}" + (f" | decade: {v['decade']} {v.get('decade_title') or ''}" if v.get("decade") else "")
                          + (f" | subject: {v.get('title')} | music: {v.get('music')} | pan: {v.get('pan')}" if book == "paripadal" else ""))
                elif v.get("section") or v.get("chapter"):
                    print(f"SECTION: {v.get('chapter') or v.get('section')}")
                if book == "paripadal" and v["line_count"] >= 2 * UNIT_LINES[0]:
                    print(f"(mark whole as \"{key}\", or in units paripadal:{key}:<start>-<end> of {UNIT_LINES[0]}-{UNIT_LINES[1]} lines covering 1-{v['line_count']})")
            for i, line in enumerate(v["tamil"], first):
                print(f"{i:4} {line}")
            for f in own:
                print(f"FLAG {f['kind']}" + (f" line {f['line']}" if f.get("line") else "") + f": {squeeze(f.get('detail'))}")


def new_chapter_keys(book, c, ch, verses, marked, errors):
    """Match marked keys to the chapter; returns {key: text}. Handles units and Paripadal song units."""
    scheme = NEW[book][1][0]
    texts = {}
    if scheme == "units":
        rk, lo, hi = ch["span"]
        rec = ch["record"]
        core = set(ch["verses"])
        unit = re.compile(re.escape(f"{book}:{rk}:") + r"(\d+)-(\d+)")
        spans = []
        for key, mark in marked.items():
            m = unit.fullmatch(key)
            if not m:
                errors.append(f"ch{c}: {key} is not a unit id of {book}:{rk}"); continue
            s, e = int(m.group(1)), int(m.group(2))
            spans.append((s, e, key))
            if key not in core:
                if not (UNIT_LINES[0] <= e - s + 1 <= UNIT_LINES[1]):
                    errors.append(f"ch{c}: adjusted unit {key} must have {UNIT_LINES[0]}-{UNIT_LINES[1]} lines")
                if not squeeze(mark.get("unit_note") if isinstance(mark, dict) else ""):
                    errors.append(f"ch{c}: adjusted unit {key} needs a unit_note saying where the sense break is")
            if 1 <= s <= e <= rec["line_count"]:
                texts[key] = new_text(book, key, {"record_id": rec["id"], "start": s, "end": e})
        cover(c, spans, lo, hi, errors)
        return texts
    expected = set(ch["verses"])
    if scheme == "songs":
        whole, cut = set(), {}
        song = re.compile(r"paripadal:(.+):(\d+)-(\d+)")
        for key, mark in marked.items():
            m = song.fullmatch(key)
            if key in expected:
                whole.add(key)
                texts[key] = new_text(book, key, verses[key])
            elif m and m.group(1) in expected:
                s, e = int(m.group(2)), int(m.group(3))
                cut.setdefault(m.group(1), []).append((s, e, key))
                v = verses[m.group(1)]
                if not (UNIT_LINES[0] <= e - s + 1 <= UNIT_LINES[1]):
                    errors.append(f"ch{c}: unit {key} must have {UNIT_LINES[0]}-{UNIT_LINES[1]} lines")
                if 1 <= s <= e <= v["line_count"]:
                    texts[key] = {"number": None, "kind": v.get("kind"), "lines": {i: v["tamil"][i - 1] for i in range(s, e + 1)},
                                  "colophon": {"thinai": v.get("thinai"), "thurai": v.get("thurai")}}
            else:
                errors.append(f"ch{c}: {key} is not a song of this chapter or a unit paripadal:<song>:<start>-<end> of one")
        for k in sorted(expected):
            if k in whole and k in cut:
                errors.append(f"ch{c}: song {k} is marked both whole and in units")
            elif k in cut:
                cover(c, cut[k], 1, verses[k]["line_count"], errors)
            elif k not in whole:
                errors.append(f"ch{c}: song {k} is not marked")
        return texts
    if set(marked) != expected:
        errors.append(f"ch{c}: verses differ: {sorted(expected ^ set(marked))[:10]}")
    for key in marked:
        if key in expected:
            texts[key] = new_text(book, key, verses[key])
    return texts


def cover(c, spans, lo, hi, errors):
    spans = sorted(spans)
    at = lo
    for s, e, key in spans:
        if s != at:
            errors.append(f"ch{c}: units must cover lines {lo}-{hi} with no gap or overlap (at {key}, expected start {at})")
            return
        at = e + 1
    if at != hi + 1:
        errors.append(f"ch{c}: units must cover lines {lo}-{hi}; they stop at {at - 1}")


def check_new(book, numbers):
    verses, chapters = load_new(book)
    fields = NEW[book][0]
    vocabulary = {c["id"] for c in json.loads(CONCEPTS.read_text(encoding="utf-8"))}
    marks_dir = MARKS_DIR or THEMES / book
    if not numbers:
        numbers = sorted(int(p.stem[2:]) for p in marks_dir.glob("ch*.json"))
    errors, warnings = [], []
    for c in numbers:
        path = marks_dir / f"ch{c:03d}.json"
        if c not in chapters:
            errors.append(f"ch{c}: no such chapter"); continue
        if not path.exists():
            errors.append(f"ch{c}: no marks file"); continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"ch{c}: not valid JSON ({e})"); continue
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
        if not isinstance(marked, dict):
            errors.append(f"ch{c}: verses must be an object keyed by verse"); continue
        cast = check_cast(c, data.get("cast"), errors) if fields == "narrative" else None
        texts = new_chapter_keys(book, c, chapters[c], verses, marked, errors)
        for key, mark in marked.items():
            if key not in texts:
                continue
            where = f"ch{c} verse {key}"
            if fields in ("akam", "puram", "devotional"):
                check_sangam_mark(book, where, mark, texts[key], known, errors, None)
            elif fields == "ethics":
                check_ethics_mark(book, where, mark, texts[key], known, errors, warnings)
            else:
                check_narrative_mark(where, mark, texts[key], known, errors, cast)
        check_links(book, c, data.get("links", []), texts, marked, errors)
    if warnings:
        print("\n".join(f"warning: {w}" for w in warnings))
    print("\n".join(errors) if errors else f"{len(numbers)} chapters valid")
    return not errors


def link_book(target):
    m = re.match(r"([a-z_]+):", str(target))
    return m.group(1) if m else None


def check_links(book, c, links, texts, marked, errors):
    if not isinstance(links, list):
        errors.append(f"ch{c}: links must be a list"); return
    fields, per_verse = NEW[book][0], {}
    for link in links:
        if not isinstance(link, dict):
            errors.append(f"ch{c}: link is not an object"); continue
        a, b = link.get("a"), link.get("b")
        where = f"ch{c} link {a}-{b}"
        if link.get("type") not in LINK_TYPES:
            errors.append(f"{where}: unknown type {link.get('type')}")
        if str(a) not in texts:
            errors.append(f"{where}: `a` is not a verse of this chapter")
        per_verse[str(a)] = per_verse.get(str(a), 0) + 1
        if within(b):  # a verse of this book (13 or "13"); a unit book's links name the unit or span
            ok = NEW[book][1][0] != "units" and str(int(b)) in new_keys(book)[0]
        else:
            ok = new_target_ok(b) or sangam_target_ok("akananuru", str(b), {}, finished_numbers())
        if not ok:
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
        other = book if within(b) else link_book(b)
        if fields == "ethics":
            if "item" in link:
                items = (marked.get(str(a)) or {}).get("items") if isinstance(marked.get(str(a)), dict) else None
                if not isinstance(link["item"], int) or not isinstance(items, list) or not 1 <= link["item"] <= len(items):
                    errors.append(f"{where}: item must be the 1-based position of one of {a}'s items")
            if other in ("kural", "naladiyar") and len(squeeze(link.get("list_adds")).split()) < 4:
                errors.append(f"{where}: a link to the {other.capitalize()} needs list_adds: what the list does that the {other} verse does not")
        elif fields == "narrative" and other not in {k for k, v in NEW.items() if v[0] == "narrative"}:
            g = link.get("gains")
            if not isinstance(g, dict) or not squeeze(g.get("a")) or not squeeze(g.get("b")):
                errors.append(f"{where}: a link outside the epics needs gains {{a, b}}: what each side gains")
    errors.extend(f"ch{c} verse {a}: at most three links per verse" for a, n in per_verse.items() if n > 3)


def finished_numbers():
    if "finished" not in _NEW_CACHE:
        _NEW_CACHE["finished"] = {b: {int(r[f]) for r in read_jsonl(CORE / core)} for b, (core, f) in FINISHED.items()}
    return _NEW_CACHE["finished"]


def cite(text, err):
    """on_line(form, line, what, after=0) and in_text(words, what): Tamil cited in a mark must be in the
    verse; `after` lets a phrase run on into that many following lines."""
    lines = text["lines"]
    whole = tamil_only(" ".join(lines.values()))

    def on_line(form, line, what, after=0):
        if not isinstance(form, str) or not tamil_only(form):
            err(f"{what} {form!r} must be Tamil words as written in the verse")
        elif not isinstance(line, int) or line not in lines:
            err(f"{what} {form!r}: line {line} is not a line of this verse")
        elif tamil_only(form) not in tamil_only(" ".join(lines.get(i, "") for i in range(line, line + after + 1))):
            err(f"{what} {form!r} is not on line {line}" + (f" (or the {after} after it)" if after else ""))

    def in_text(words, what):
        for w in words if isinstance(words, list) else [words]:
            if not isinstance(w, str) or not tamil_only(w) or tamil_only(w) not in whole:
                err(f"{what} {w!r} is not in the verse")
    return on_line, in_text


def check_house(mark, known, err):
    if not isinstance(mark.get("reading"), str) or not mark["reading"].strip():
        err("no reading")
    concepts = mark.get("concepts", [])
    if not isinstance(concepts, list) or not 1 <= len(concepts) <= MAX_CONCEPTS:
        err(f"needs 1 to {MAX_CONCEPTS} concepts"); concepts = []
    for x in concepts:
        if x not in known:
            err(f"unknown concept {x}")
    if mark.get("nuance") is not None and not isinstance(mark.get("nuance"), str):
        err("nuance must be a string")
    if mark.get("uncertain") is not None and not isinstance(mark.get("uncertain"), bool):
        err("uncertain must be true or false")
    if mark.get("positions") or mark.get("contested"):
        err("no commentary is in the corpus: no positions or contested")


def text_str(x):
    return isinstance(x, str) and bool(x.strip())


def check_ethics_mark(book, where, mark, text, known, errors, warnings):
    err = lambda msg: errors.append(f"{where}: {msg}")
    if not isinstance(mark, dict):
        return err("mark is not an object")
    check_house(mark, known, err)
    on_line, in_text = cite(text, err)
    numbered = text.get("kind") not in INTRO_KINDS
    if mark.get("domain") not in DOMAINS:
        err(f"domain must be one of {sorted(DOMAINS)}")
    if mark.get("domain_note") is not None and not text_str(mark.get("domain_note")):
        err("domain_note must be a clause")
    counted = book in ITEM_COUNTS
    items = mark.get("items")
    if items is None:
        if counted and numbered:
            err("items is required: one {thing, claim, line} per counted thing")
        items = []
    elif not isinstance(items, list):
        err("items must be a list of {thing, claim, line}"); items = []
    for item in items:
        if not isinstance(item, dict) or set(item) - {"thing", "claim", "line", "domain"}:
            err("items entry must be an object of thing, claim, line (and domain)"); continue
        on_line(item.get("thing"), item.get("line"), "items thing", after=1)
        if not text_str(item.get("claim")):
            err(f"items thing {item.get('thing')!r} has no claim")
        if "domain" in item and item["domain"] not in DOMAINS:
            err(f"items domain must be one of {sorted(DOMAINS)}")
    if counted and numbered and mark.get("items") is not None and not items:
        err("items must list at least one thing")
    if counted and numbered and items and len(items) not in ITEM_COUNTS[book]:
        warnings.append(f"{where}: {len(items)} items; the table expects {' or '.join(map(str, sorted(ITEM_COUNTS[book])))} (say in nuance how you divided them)")
    if book == "pazhamozhi_nanooru" and mark.get("items"):
        warnings.append(f"{where}: Pazhamozhi does not count; its verses use pazhamozhi, not items")
    if counted and numbered and book != "muthumozhikkanchi" and "count_word" not in mark:
        err("count_word is required: the verse's own count word as written, or null")
    cw = mark.get("count_word")
    if cw is not None:
        in_text([cw], "count_word")
    pz = mark.get("pazhamozhi")
    if book == "pazhamozhi_nanooru" and numbered and pz is None:
        err("pazhamozhi is required: {proverb, lines, literal, story, applied_to}")
    if pz is not None:
        if book != "pazhamozhi_nanooru":
            err("pazhamozhi belongs to Pazhamozhi Nanooru only")
        elif not isinstance(pz, dict):
            err("pazhamozhi must be {proverb, lines, literal, story, applied_to}")
        else:
            lines = pz.get("lines")
            if not isinstance(lines, list) or not lines or not all(isinstance(i, int) and i in text["lines"] for i in lines):
                err("pazhamozhi lines must list the verse lines the proverb spans")
            else:
                on_line(pz.get("proverb"), min(lines), "pazhamozhi proverb", after=max(lines) - min(lines))
            for k in ("literal", "applied_to"):
                if not text_str(pz.get(k)):
                    err(f"pazhamozhi needs {k}")
            story = pz.get("story")
            if not isinstance(story, dict) or story.get("kind") not in STORY_KINDS:
                err(f"pazhamozhi story needs kind ({'/'.join(sorted(STORY_KINDS))})")
            else:
                if story.get("who") is not None:
                    in_text([story["who"]], "pazhamozhi story who")
                if not text_str(story.get("act")):
                    err("pazhamozhi story needs act")
                if story.get("tradition") is not None and not text_str(story.get("tradition")):
                    err("pazhamozhi story tradition must be a clause or absent")
    norm = mark.get("norm")
    if norm is not None:
        if not isinstance(norm, dict) or norm.get("historical") is not True:
            err("norm must be {historical: true, kinds, note}")
        else:
            kinds = norm.get("kinds")
            if not isinstance(kinds, list) or not kinds or any(k not in NORM_KINDS for k in kinds):
                err(f"norm kinds must be one or more of {sorted(NORM_KINDS)}")
            if not text_str(norm.get("note")):
                err("norm needs a note")
    extra = set(mark) - {"reading", "nuance", "concepts", "uncertain", "domain", "domain_note", "items",
                         "count_word", "pazhamozhi", "norm"}
    if extra:
        err(f"fields not in the ethics field set: {sorted(extra)}")


def check_cast(c, cast, errors):
    """The chapter's cast list; returns the set of ids (with narrator)."""
    ids = {"narrator"}
    if not isinstance(cast, list):
        errors.append(f"ch{c}: cast must be a list of {{id, tamil, role}}"); return ids
    for p in cast:
        if not isinstance(p, dict) or not isinstance(p.get("id"), str) or not CAST_ID.fullmatch(p["id"]):
            errors.append(f"ch{c}: cast entry needs an id of lowercase romanized letters: {p}"); continue
        if p["id"] in ids:
            errors.append(f"ch{c}: cast id {p['id']} is defined twice")
        ids.add(p["id"])
        if not tamil_only(p.get("tamil")) or not text_str(p.get("role")):
            errors.append(f"ch{c}: cast {p['id']} needs tamil and role")
    return ids


def verse_lines(ref):
    """The Tamil lines of kural:N or naladiyar:N, or None."""
    m = re.fullmatch(r"(kural|naladiyar):(\d+)", str(ref))
    if not m:
        return None
    if m.group(1) not in _NEW_CACHE:
        _NEW_CACHE[m.group(1)] = {int(r["verse"]): r["tamil"] for r in read_jsonl(CORE / f"{m.group(1)}.jsonl")}
    return _NEW_CACHE[m.group(1)].get(int(m.group(2)))


def echo_matches(words, cited):
    """At least four of the echo's words are the cited verse's, or it holds a whole line of it
    (compared without spaces and punctuation, so word division and sandhi may differ)."""
    source = tamil_only(" ".join(cited))
    own = [tamil_only(w) for w in words.split() if len(tamil_only(w)) > 1]
    if sum(1 for w in own if w in source) >= 4:
        return True
    joined = tamil_only(words)
    return any(tamil_only(line) and (tamil_only(line) in joined or joined == tamil_only(line)) for line in cited)


def check_narrative_mark(where, mark, text, known, errors, cast):
    err = lambda msg: errors.append(f"{where}: {msg}")
    if not isinstance(mark, dict):
        return err("mark is not an object")
    check_house(mark, known, err)
    on_line, in_text = cite(text, err)

    def form_line(obj, what):
        if obj.get("form") is not None:
            on_line(obj.get("form"), obj.get("line"), what)
        elif obj.get("line") is not None and obj.get("line") not in text["lines"]:
            err(f"{what}: line {obj.get('line')} is not a line of this verse")

    sp = mark.get("speaker")
    if not isinstance(sp, dict):
        err("speaker must be {who, form, line, addressee}")
    else:
        if sp.get("who") not in cast:
            err(f"speaker who {sp.get('who')!r} must be narrator or an id in the chapter's cast")
        form_line(sp, "speaker form")
        if sp.get("addressee") is not None and sp.get("addressee") not in cast:
            err(f"speaker addressee {sp.get('addressee')!r} must be null or an id in the cast")
    agents = mark.get("agents")
    if not isinstance(agents, list):
        err("agents must be a list ([] when no one acts)"); agents = []
    for a in agents:
        if not isinstance(a, dict) or a.get("id") not in cast:
            err(f"agent {a.get('id') if isinstance(a, dict) else a!r} must be {{id, form, line}} with an id in the cast"); continue
        form_line(a, f"agent {a['id']} form")
    if "event" not in mark:
        err("event is required (null for pure description, praise or argument)")
    elif mark["event"] is not None and not text_str(mark["event"]):
        err("event must be one line or null")
    claims = mark.get("claims")
    if not isinstance(claims, list):
        err("claims must be a list ([] when the unit states none)"); claims = []
    for cl in claims:
        if not isinstance(cl, dict) or not text_str(cl.get("claim")):
            err("claims entry needs claim"); continue
        what = f"claim {cl['claim'][:30]!r}"
        if cl.get("school") not in SCHOOLS:
            err(f"{what}: school must be one of {sorted(SCHOOLS)}")
        if cl.get("school_detail") is not None and cl.get("school_detail") not in SCHOOL_DETAILS:
            err(f"{what}: school_detail must be one of {sorted(SCHOOL_DETAILS)}")
        if cl.get("stance") not in STANCES:
            err(f"{what}: stance must be one of {sorted(STANCES)}")
        if cl.get("line") not in text["lines"]:
            err(f"{what}: line {cl.get('line')} is not a line of this verse")
        if cl.get("voiced_by") not in cast:
            err(f"{what}: voiced_by {cl.get('voiced_by')!r} must be narrator or an id in the cast")
    echoes = mark.get("echoes")
    if echoes is not None and not isinstance(echoes, list):
        err("echoes must be a list"); echoes = []
    for e in echoes or []:
        if not isinstance(e, dict):
            err("echoes entry is not an object"); continue
        cited = verse_lines(e.get("b"))
        if cited is None:
            err(f"echo b {e.get('b')!r} must be kural:N or naladiyar:N")
        if e.get("kind") not in ECHO_KINDS:
            err(f"echo kind must be one of {sorted(ECHO_KINDS)}")
        on_line(e.get("words"), e.get("line"), "echo words", after=3)
        if e.get("marked") is not None:
            line = e.get("line") if isinstance(e.get("line"), int) else 0
            near = [i for i in text["lines"] if i >= line - 3]  # the introducing words may come a few lines before
            start = min(near) if near else line
            on_line(e.get("marked"), start, "echo marked", after=6)
        if cited and isinstance(e.get("words"), str) and not echo_matches(e["words"], cited):
            err(f"echo words do not match {e.get('b')}: need a run of four of its words or a whole line")
    extra = set(mark) - {"reading", "nuance", "concepts", "uncertain", "speaker", "agents", "event", "claims",
                         "echoes", "unit_note"}
    if extra:
        err(f"fields not in the narrative field set: {sorted(extra)}")


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
    if book in NEW:
        if command == "chapters":
            _, chapters = load_new(book)
            for c, ch in chapters.items():
                print(f"{c}\t{ch['verses'][0]} .. {ch['verses'][-1]}\t{len(ch['verses'])}\t{ch['title']}")
        elif command == "show":
            show_new(book, numbers)
        elif command == "check":
            sys.exit(0 if check_new(book, numbers) else 1)
        return
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
