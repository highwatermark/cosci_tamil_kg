#!/usr/bin/env python3
"""Git clean filter: blank quotations from modern, in-copyright commentaries.

The working copy keeps the full text; the blob git commits has it blanked. Wired up in
.gitattributes as `filter=strip-modern`; enable it once per clone with

  git config filter.strip-modern.clean "python3 -I scripts/git_strip_modern_commentary.py"
  git config filter.strip-modern.smudge cat
  git config filter.strip-modern.required false

Modern commentators: Kalaignar (M. Karunanidhi) on the Kural, and V. Mahadeva Mudaliar and
Sundara Shanmuganar on the Naladiyar, Nalvazhi and Thirumurugaatruppadai. Parimelazhagar,
Manakkudavar, Arumuga Navalar and Pope are public domain and pass through untouched.

Reads stdin, writes stdout, deterministic and idempotent. The format is sniffed:
  JSON Lines  each line is re-dumped with the separators and ensure_ascii it already uses
  JSON        re-dumped with the file's own indentation
  text / .md  bullet quotations credited to a modern commentator are replaced
What is blanked:
  - a field named after a modern commentator (kalaignar, mudaliar, shanmuganar,
    sundara_shanmuganar): a string becomes "", a dict has its text/quote fields blanked
  - in any dict whose identity fields (s, by, id, author, doc, source, work, commentator)
    name a modern commentator or his source file: the quote, quotes and text fields
English paraphrase and analysis (position, note, nuance, reason) is the project's own and stays.
"""
import json
import re
import sys

NAME = re.compile(r"kalaignar|mudaliar|shanmuganar", re.I)
DOCS = re.compile(r"\bpmuni0(?:612|518|778|774|777)\b")
TAMIL_NAMES = re.compile(r"கலைஞர்|கருணாநிதி|சண்முகனார்|மகாதேவ முதலியார்")
ID_KEYS = ("s", "by", "id", "author", "doc", "source", "work", "commentator")
BLANK_KEYS = ("quote", "quotes", "text")
OMITTED = "[quotation omitted: in copyright]"


def modern_key(key):
    return bool(NAME.search(key)) and not key.endswith("_edition")


def modern_value(value):
    return isinstance(value, str) and bool(
        re.search(r"(?:^|:)(?:kalaignar|mudaliar|shanmuganar|sundara_shanmuganar)(?::|$)", value, re.I)
        or DOCS.search(value) or TAMIL_NAMES.search(value))


def blank(value):
    if isinstance(value, str):
        return ""
    if isinstance(value, list):
        return []
    return value


def blank_fields(d):
    for k in BLANK_KEYS:
        if k in d and d[k]:
            d[k] = blank(d[k])


def strip(obj):
    """Blank modern quotations in place; returns obj."""
    if isinstance(obj, dict):
        if any(modern_value(obj.get(k)) for k in ID_KEYS):
            blank_fields(obj)
        for k, v in obj.items():
            if modern_key(k):
                if isinstance(v, str):
                    obj[k] = ""
                elif isinstance(v, dict):
                    blank_fields(v)
                    strip(v)
                elif isinstance(v, list) and all(isinstance(x, str) for x in v):
                    obj[k] = []
                else:
                    strip(v)
            else:
                strip(v)
    elif isinstance(obj, list):
        for x in obj:
            strip(x)
    return obj


def dump_like(obj, original, styles):
    """Dump obj in the first style that reproduces `original` exactly, or None."""
    for style in styles:
        try:
            if json.dumps(json.loads(original), **style) == original:
                return json.dumps(obj, **style)
        except (ValueError, TypeError):
            continue
    return None


LINE_STYLES = [dict(ensure_ascii=a, separators=s) for a in (False, True) for s in ((", ", ": "), (",", ":"))]
DOC_STYLES = [dict(ensure_ascii=a, indent=i) for i in (2, 1, 4, 3, "\t") for a in (False, True)] + LINE_STYLES


def substitute(original, before, after):
    """Fallback when no json.dumps style reproduces the source: swap changed string literals."""
    changes = []

    def collect(a, b, key=None):
        if isinstance(a, dict):
            for k in a:
                collect(a[k], b[k], k)
        elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
            for x, y in zip(a, b):
                collect(x, y, key)
        elif a != b:
            changes.append((key, a, b))

    collect(before, after)
    text = original
    for key, old, new in changes:
        olds = old if isinstance(old, list) else [old]
        for o in olds:
            if not isinstance(o, str):
                continue
            for ascii_ in (False, True):
                lit = json.dumps(o, ensure_ascii=ascii_)
                if isinstance(old, list):
                    text = re.sub(r"(\s*)" + re.escape(lit) + r",?", "", text)
                else:
                    text = re.sub(r'("' + re.escape(key) + r'"\s*:\s*)' + re.escape(lit),
                                  lambda m: m.group(1) + json.dumps(new), text)
    return text


def clean_json_text(original, styles):
    try:
        obj = json.loads(original)
    except ValueError:
        return None
    before = json.loads(original)
    after = strip(obj)
    if after == before:
        return original
    out = dump_like(after, original, styles)
    return out if out is not None else substitute(original, before, after)


def clean_jsonl(text):
    lines = text.split("\n")
    if not any(l.strip() for l in lines):
        return None
    out = []
    for line in lines:
        body = line.rstrip("\r")
        if not body.strip():
            out.append(line)
            continue
        cleaned = clean_json_text(body, LINE_STYLES)
        if cleaned is None:
            return None
        out.append(cleaned + line[len(body):])
    return "\n".join(out)


def clean_json(text):
    body = text.rstrip("\n")
    cleaned = clean_json_text(body, DOC_STYLES)
    return None if cleaned is None else cleaned + text[len(body):]


BULLET = re.compile(r"^(\s*[-*] \*\*[^*\n]*\*\*) — (?!\[quotation omitted)(.+)$", re.M)


def clean_text(text):
    def repl(m):
        head = m.group(1)
        if NAME.search(head) or TAMIL_NAMES.search(head):
            return f"{head} — {OMITTED}"
        return m.group(0)
    return BULLET.sub(repl, text)


def clean(text):
    stripped = text.lstrip()
    if stripped[:1] in ("{", "["):
        for fn in (clean_jsonl, clean_json):
            out = fn(text)
            if out is not None:
                return out
    return clean_text(text)


def main():
    data = sys.stdin.buffer.read()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        sys.stdout.buffer.write(data)
        return
    sys.stdout.buffer.write(clean(text).encode("utf-8"))


if __name__ == "__main__":
    main()
