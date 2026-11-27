#!/usr/bin/env python3
"""Merge every chapter's new_concepts into kg/themes/concepts.json, the shared concept vocabulary.

- An id already in concepts.json is never renamed or redefined; a chapter that declares it again is
  left as it is (its declaration is redundant).
- A new id is added once, from its first declaration in corpus order (book, then chapter), with
  first_book and the number of verses that use it.
- A new id that is a near-duplicate of another (a second spelling of one word, or the same idea under
  a nearer word) is mapped to the kept id (ALIASES below), which records it under `aliases`. Marks
  that use the mapped id are rewritten to the kept one, and the chapter's declaration of the mapped id
  is dropped, so `book_marks.py check` finds every concept in concepts.json.

Usage: python3 -I scripts/merge_concepts.py [--dry-run]
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES = ROOT / "kg" / "themes"
CONCEPTS = THEMES / "concepts.json"
SKIP = {"sangam_grading", "siddhar_layers", "tholkappiyam_pilot"}

# mapped id -> kept id. Second spellings first, then the same idea under another word.
ALIASES = {
    "nimiththam": "nimittam",        # நிமித்தம், the omen
    "pul": "nimittam",               # the omen bird: an omen read from a creature's cry
    "punal_aadal": "punalaadal",     # புனல் ஆடல், the river-flood festival
    "punalaattu": "punalaadal",
    "paththini": "pathini",          # பத்தினி
    "kunam": "gunam",                # குணம், quality against substance
    "pagudhi": "pakuthi",            # பகுதி, the Sankhya's prakriti
    "poli": "aabaasam",              # a false semblance in an argument
    "samayavaadham": "vaadhu",       # formal debate between schools
    "aadal": "koothu",               # dance as a learned art
    "vatham": "nonbu",               # the vow of restraint
    "serukku": "agandhai",           # pride that blinds (existing id)
}


def chapter_files():
    for d in sorted(p for p in THEMES.iterdir() if p.is_dir() and p.name not in SKIP):
        for f in sorted(d.glob("ch*.json")):
            yield d.name, f


def dump_like(original, data):
    """Re-serialise in the file's own layout, or None if no layout reproduces it."""
    for indent in (1, 2, None):
        for tail in ("", "\n"):
            if json.dumps(json.loads(original), ensure_ascii=False, indent=indent) + tail == original:
                return json.dumps(data, ensure_ascii=False, indent=indent) + tail
    return None


def remap(ids):
    out = []
    for x in ids:
        y = ALIASES.get(x, x)
        if y not in out:
            out.append(y)
    return out


def main():
    dry = "--dry-run" in sys.argv
    concepts = json.loads(CONCEPTS.read_text(encoding="utf-8"))
    known = {c["id"]: c for c in concepts}
    assert not set(ALIASES) & set(known), "an existing id may not be mapped away"
    first, uses = {}, Counter()
    for book, f in chapter_files():
        d = json.loads(f.read_text(encoding="utf-8"))
        for nc in d.get("new_concepts") or []:
            first.setdefault(nc["id"], (book, nc))
        for v in (d.get("verses") or {}).values():
            if isinstance(v, dict):
                uses.update(v.get("concepts") or [])
    added = []
    for cid, (book, nc) in first.items():
        if cid in known or cid in ALIASES:
            continue
        rec = {"id": cid, "tamil": nc["tamil"], "gloss": nc["gloss"], "label_source": nc.get("label_source", ""),
               "first_book": book}
        known[cid] = rec
        concepts.append(rec)
        added.append(cid)
    for old, new in ALIASES.items():
        if old in first and new in known:
            al = known[new].setdefault("aliases", [])
            if old not in al:
                al.append(old)
    missing = sorted(x for x in uses if ALIASES.get(x, x) not in known)
    # rewrite the marks
    changed, regex_files, verses_changed = [], [], 0
    for book, f in chapter_files():
        text = f.read_text(encoding="utf-8")
        if not any(f'"{a}"' in text for a in ALIASES):
            continue
        d = json.loads(text)
        hit = 0
        for v in (d.get("verses") or {}).values():
            if isinstance(v, dict) and any(c in ALIASES for c in v.get("concepts") or []):
                v["concepts"] = remap(v["concepts"])
                hit += 1
        decl = d.get("new_concepts") or []
        keep = [nc for nc in decl if nc.get("id") not in ALIASES]
        if not hit and len(keep) == len(decl):
            continue
        if "new_concepts" in d:
            d["new_concepts"] = keep
        out = dump_like(text, d)
        if out is None:  # rewrite only inside the concepts arrays; leave the declaration
            regex_files.append(str(f.relative_to(ROOT)))

            def fix(m):
                ids = remap(json.loads(m.group(2)))
                return m.group(1) + json.dumps(ids, ensure_ascii=False)
            out = re.sub(r'("concepts"\s*:\s*)(\[[^\]]*\])', fix, text)
        verses_changed += hit
        changed.append(str(f.relative_to(ROOT)))
        if not dry:
            f.write_text(out, encoding="utf-8")
    if not dry:
        CONCEPTS.write_text(json.dumps(concepts, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"concepts {len(concepts) - len(added)} -> {len(concepts)} (+{len(added)}); "
          f"aliases {len([a for a in ALIASES if a in first])}; files rewritten {len(changed)} "
          f"({len(regex_files)} by array only), verses {verses_changed}; used ids missing {missing}")
    print("added:", " ".join(added))


if __name__ == "__main__":
    main()
