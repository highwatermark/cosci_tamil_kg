#!/usr/bin/env python3
"""Show a chapter of any ingested book, validate its marks, and print a reading index.

  book_marks.py tirumanthiram chapters          list chapters with verse ranges
  book_marks.py tirumanthiram show 12 13        print those chapters' verses and witnesses
  book_marks.py tirumanthiram check [12 13]     validate kg/themes/tirumanthiram/chNNN.json
  book_marks.py index OUT                       one line per marked verse of every finished book

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
}
SPLIT = {"thiruppugazh": 15}
FINISHED = {"kural": ("kural.jsonl", "verse"), "naladiyar": ("naladiyar.jsonl", "verse"),
            "tirumanthiram": ("tirumanthiram.jsonl", "number")}


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
        print(f"# Chapter {c}: {ch['title']} ({where}verses {ch['verses'][0]}-{ch['verses'][-1]})")
        for n in ch["verses"]:
            v = verses[n]
            print(f"\n## {n}\n" + "\n".join(v["tamil"]))
            for field in ("variants", "sengalvaraya_parallels", "corrupt_lines", "corrupt_chars", "heading_variants"):
                if v.get(field):
                    print(f"{field.upper()}: {squeeze(json.dumps(v[field], ensure_ascii=False))}")
            for field in witnesses:
                print(f"{field.upper()}:", squeeze(str(v.get(field))) or "(none)")


def target_ok(target, verses, finished):
    if isinstance(target, int):
        return target in verses
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
    for book, folder in (("kural", "kural"), ("naladiyar", "naladiyar"), ("tirumanthiram", "tirumanthiram")):
        for n in read_jsonl(ROOT / "kg" / folder / "nodes.jsonl"):
            if n["type"] == "Verse":
                lines.append((book, n["number"], n["reading"]))
    concepts = {}
    for folder in ("kural", "naladiyar", "tirumanthiram"):
        for e in read_jsonl(ROOT / "kg" / folder / "edges.jsonl"):
            if e["p"] == "EXPRESSES":
                concepts.setdefault(e["s"], []).append(e["o"].split(":")[1])
    with open(out, "w", encoding="utf-8") as f:
        for book, number, reading in lines:
            f.write(f"{book}:{number} | {', '.join(concepts.get(f'{book}:{number}', []))} | {reading}\n")
    print(f"index: {len(lines)} verses")


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    if sys.argv[1] == "index":
        return index(sys.argv[2])
    book, command, numbers = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3:]]
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
