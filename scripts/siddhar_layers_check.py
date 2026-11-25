#!/usr/bin/env python3
"""Validate the Siddhar reading-layer pilot files (docs/siddhar-layers-brief.md).

  siddhar_layers_check.py            check every kg/themes/siddhar_layers/chNNN.json and print counts
  siddhar_layers_check.py 72 87      check those chapters only (links to other pilot chapters are
                                     still resolved against every layer file present)

The cipher-key, body-place and stance vocabularies are read from the brief's tables, so the brief is
the single source for them. The double-reading lexicon (cipher_lexicon.json) is checked too: its
corpus counts are recounted and its `uses` must match the layer readings' `lexicon` citations
exactly. Standard library only; run with python3 -I.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))  # -I drops the script's own directory from sys.path
import book_marks  # noqa: E402

LAYER_DIR = ROOT / "kg" / "themes" / "siddhar_layers"
BRIEF = ROOT / "docs" / "siddhar-layers-brief.md"
AUDIT = ROOT / "kg" / "siddhar" / "link_audit.json"
LEXICON = LAYER_DIR / "cipher_lexicon.json"
LEX_STATUS = {"proposed", "accepted", "rejected"}
LAYERS = ("literal", "breath", "alchemy", "consciousness", "social")
CONF = {"low": 0, "med": 1, "high": 2}
LINK_TYPES = book_marks.LINK_TYPES | {"shared_key"}
MODES = {"senses", "inference", "teacher_or_book", "direct_experience"}
STANCES = {"relies", "rejects", "reports"}
BASES = {"named", "key"}
VERDICTS = {"holds_literal", "holds_on_layer", "cipher_artefact", "stock_attack", "generic", "misread"}
ACTIONS = {"kept", "renoted", "dropped", "out_of_scope"}
ORIGINS = {"kept", "renoted", "new"}
OTHER_BOOKS = book_marks.FINISHED
# Words that would turn a historical claim into instructions.
DOSAGE = re.compile(r"\b(dose|dosage|grams?|ounces?|measures? of|parts? of|grind|pound it|mix(ed)? with|"
                    r"boil|take (it|this) (daily|twice|morning)|apply (it|this)|administer|prescri)", re.I)


def table(marker):
    text = BRIEF.read_text(encoding="utf-8")
    body = text.split(f"<!-- {marker} -->")[1].split(f"<!-- /{marker} -->")[0]
    return {m.group(1) for m in re.finditer(r"^\| `([a-z0-9_]+)` \|", body, re.M)}


def squash(s):
    return re.sub(r"[\s\-.,;:!?'\"()…]+", "", s or "")


def load_layer_files():
    files = {}
    for p in sorted(LAYER_DIR.glob("ch[0-9][0-9][0-9].json")):
        files[int(p.stem[2:])] = json.loads(p.read_text(encoding="utf-8"))
    return files


def target_exists(b, finished_cache):
    book, _, num = b.partition(":")
    if book not in OTHER_BOOKS or not num.isdigit():
        return False
    if book not in finished_cache:
        core, field = OTHER_BOOKS[book]
        finished_cache[book] = {int(r[field]) for r in book_marks.read_jsonl(book_marks.CORE / core)}
    return int(num) in finished_cache[book]


def check_chapter(c, d, ctx):
    errs = []
    err = errs.append
    verses, chapters = ctx["verses"], ctx["chapters"]
    if c not in chapters:
        return [f"ch{c:03d}: no such Siddhar chapter"]
    if d.get("chapter_no") != c:
        err(f"chapter_no {d.get('chapter_no')} != {c}")
    want = {str(n) for n in chapters[c]["verses"]}
    got = set(d.get("verses", {}))
    if want - got:
        err(f"missing verses {sorted(want - got, key=int)}")
    if got - want:
        err(f"verses not in this chapter {sorted(got - want, key=int)}")
    for k, v in sorted(d.get("verses", {}).items(), key=lambda kv: int(kv[0])):
        if k not in want:
            continue
        tamil = squash(" ".join(verses[int(k)]["tamil"]))
        layers = v.get("layers", {})
        if "literal" not in layers:
            err(f"{k}: no literal layer")
        for lid, lay in layers.items():
            where = f"{k}.{lid}"
            if lid not in LAYERS:
                err(f"{where}: unknown layer")
                continue
            for lx in lay.get("lexicon", []):
                if lx not in ctx["lex"]:
                    err(f"{where}: unknown lexicon entry {lx!r}")
                else:
                    ctx["cited"].add((int(k), lid, lx))
            for f in ("reading", "confidence", "carriers", "keys", "lexicon"):
                if f not in lay:
                    err(f"{where}: missing {f}")
            if not str(lay.get("reading", "")).strip():
                err(f"{where}: empty reading")
            if lay.get("confidence") not in CONF:
                err(f"{where}: confidence {lay.get('confidence')!r}")
            cs = lay.get("carriers", [])
            if not isinstance(cs, list) or not 1 <= len(cs) <= 5:
                err(f"{where}: carriers must be a list of 1 to 5")
            for w in cs if isinstance(cs, list) else []:
                if not squash(w) or squash(w) not in tamil:
                    err(f"{where}: carrier {w!r} not in the verse")
            for key in lay.get("keys", []):
                if key not in ctx["keys"]:
                    err(f"{where}: unknown key {key!r}")
            if lid == "alchemy" and DOSAGE.search(lay.get("reading", "")):
                err(f"{where}: reading uses dosage or preparation words; record the claim, not a recipe")
        st = v.get("stance")
        if not isinstance(st, list) or not 1 <= len(st) <= 2 or any(x not in ctx["stances"] for x in st):
            err(f"{k}: stance must be a list of one or two values from the brief's table")
        if len(layers) == 5:
            ctx["warn"].append(f"ch{c:03d} {k}: all five layers present; check each is carried by the Tamil")
        bp = v.get("body_place")
        if not isinstance(bp, list):
            err(f"{k}: body_place must be a list")
            bp = []
        for e in bp:
            if e.get("place") not in ctx["places"]:
                err(f"{k}: body place {e.get('place')!r} not in the brief's table")
            if not squash(e.get("tamil")) or squash(e.get("tamil")) not in tamil:
                err(f"{k}: body place words {e.get('tamil')!r} not in the verse")
            if e.get("basis") not in BASES:
                err(f"{k}: body place basis {e.get('basis')!r}")
            if e.get("confidence") not in CONF:
                err(f"{k}: body place confidence {e.get('confidence')!r}")
        kb = v.get("knows_by")
        if not isinstance(kb, list):
            err(f"{k}: knows_by must be a list")
            kb = []
        for e in kb:
            if e.get("mode") not in MODES:
                err(f"{k}: knows_by mode {e.get('mode')!r}")
            if e.get("stance") not in STANCES:
                err(f"{k}: knows_by stance {e.get('stance')!r}")
            ws = e.get("tamil")
            if not isinstance(ws, list) or not ws:
                err(f"{k}: knows_by needs Tamil words")
            for w in ws or []:
                if squash(w) not in tamil:
                    err(f"{k}: knows_by words {w!r} not in the verse")
    # links
    per_a, seen = Counter(), set()
    for i, l in enumerate(d.get("links", [])):
        where = f"link {i} ({l.get('a')} -> {l.get('b')})"
        a, b = l.get("a"), l.get("b")
        if str(a) not in want:
            err(f"{where}: a is not a verse of this chapter")
            continue
        per_a[a] += 1
        pair = frozenset((str(a), str(b)))
        if pair in seen:
            err(f"{where}: duplicate pair")
        seen.add(pair)
        if l.get("type") not in LINK_TYPES:
            err(f"{where}: type {l.get('type')!r}")
        ends = [ctx["pilot"][str(a)]]
        if isinstance(b, int):
            if str(b) not in ctx["pilot"]:
                err(f"{where}: b is not a pilot verse (Siddhar targets must be in a layer file)")
            elif b == a:
                err(f"{where}: self-link")
            else:
                ends.append(ctx["pilot"][str(b)])
        elif not (isinstance(b, str) and target_exists(b, ctx["finished"])):
            err(f"{where}: b must be a pilot seq or kural:N, naladiyar:N, tirumanthiram:N, thiruppugazh:N")
        layer = l.get("layer")
        if layer not in LAYERS:
            err(f"{where}: layer {layer!r}")
            continue
        for e in ends:
            if layer not in e["layers"]:
                err(f"{where}: layer {layer} is not present on one end")
        also = l.get("also_holds_on")
        if not isinstance(also, list):
            err(f"{where}: also_holds_on must be a list")
            also = []
        for x in also:
            if x not in LAYERS or x == layer:
                err(f"{where}: also_holds_on {x!r}")
            for e in ends:
                if x in LAYERS and x not in e["layers"]:
                    err(f"{where}: also_holds_on {x} is not present on one end")
        keys = l.get("keys", [])
        for key in keys:
            if key not in ctx["keys"]:
                err(f"{where}: unknown key {key!r}")
        if l.get("type") == "shared_key":
            if not keys:
                err(f"{where}: shared_key needs keys")
            for e in ends:
                for key in keys:
                    if key not in e["layers"].get(layer, {}).get("keys", []):
                        err(f"{where}: key {key} is not applied in the {layer} layer of one end")
        check_stances(l, where, err, ctx)
        conf = l.get("confidence")
        if conf not in CONF:
            err(f"{where}: confidence {conf!r}")
        else:
            for e in ends:
                lc = e["layers"].get(layer, {}).get("confidence")
                if lc in CONF and CONF[conf] > CONF[lc]:
                    err(f"{where}: link confidence {conf} above its {layer} layer ({lc})")
        if len(str(l.get("note", ""))) < 40:
            err(f"{where}: note missing or too short")
        origin = l.get("origin")
        if origin not in ORIGINS:
            err(f"{where}: origin {origin!r}")
        old = ctx["audit_pairs"].get(frozenset((str(a), str(b))))
        if origin in ("kept", "renoted") and not old:
            err(f"{where}: origin {origin} but no graded link joins this pair")
        if origin == "new" and old:
            err(f"{where}: origin new but this pair was graded before ({old['grade']})")
    for a, n in per_a.items():
        if n > 3:
            err(f"verse {a}: {n} links as a (max 3)")
    # old links: every graded link that starts here, or starts outside the pilot and ends here
    required = {}
    for o in ctx["audit"]:
        sa, sb = str(o["a"]), str(o["b"])
        if sa in want or (sa not in ctx["all_pilot"] and sb in want):
            required[(sa, sb)] = o
    reviewed = set()
    for o in d.get("old_links", []):
        key = (str(o.get("a")), str(o.get("b")))
        where = f"old link {key[0]} -> {key[1]}"
        if key not in required:
            err(f"{where}: not a graded link this chapter must review")
            continue
        if key in reviewed:
            err(f"{where}: reviewed twice")
        reviewed.add(key)
        if o.get("old_grade") != required[key]["grade"]:
            err(f"{where}: old_grade {o.get('old_grade')!r} != audit {required[key]['grade']!r}")
        if o.get("layer") not in LAYERS:
            err(f"{where}: layer {o.get('layer')!r}")
        if o.get("verdict") not in VERDICTS:
            err(f"{where}: verdict {o.get('verdict')!r}")
        if o.get("action") not in ACTIONS:
            err(f"{where}: action {o.get('action')!r}")
        check_stances(o, where, err, ctx)
        if len(str(o.get("note", ""))) < 30:
            err(f"{where}: note missing or too short")
        b = o.get("b")
        if o.get("action") == "out_of_scope" and not (isinstance(b, int) and str(b) not in ctx["all_pilot"]
                                                      or str(o.get("a")) not in ctx["all_pilot"]):
            err(f"{where}: out_of_scope is only for links with an end outside the pilot")
        if o.get("action") in ("kept", "renoted"):
            if not any(frozenset((str(l["a"]), str(l["b"]))) == frozenset(key) for l in d.get("links", [])):
                err(f"{where}: action {o['action']} but the pair is not in links")
    for key in set(required) - reviewed:
        err(f"old link {key[0]} -> {key[1]} ({required[key]['grade']}) not reviewed")
    return errs


def check_stances(l, where, err, ctx):
    pair = l.get("stances")
    if not (isinstance(pair, list) and len(pair) == 2):
        err(f"{where}: stances must be a pair of stance lists")
        return
    for end, st in zip((l.get("a"), l.get("b")), pair):
        if not isinstance(st, list) or not st or any(x not in ctx["stances"] for x in st):
            err(f"{where}: bad stance list {st!r}")
        elif str(end) in ctx["pilot"] and st != ctx["pilot"][str(end)].get("stance"):
            err(f"{where}: stance of {end} does not match the verse's stance")


def check_lexicon(ctx, verses):
    errs = []
    if not LEXICON.exists():
        return ["cipher_lexicon.json missing"]
    lex = json.loads(LEXICON.read_text(encoding="utf-8"))
    texts = {n: squash(" ".join(r["tamil"])) for n, r in verses.items()}
    corpus = [re.sub(r"\s+", "", " ".join(r.get("tamil") or []))
              for r in book_marks.read_jsonl(book_marks.CORE / "siddhar.jsonl")]
    uses = set()
    for e in lex.get("entries", []):
        i = e.get("id")
        where = f"lexicon {i}"
        senses = e.get("senses")
        if not (isinstance(senses, list) and len(senses) == 2 and all(s.get("sense") and s.get("layer") in LAYERS for s in senses)):
            err = errs.append
            err(f"{where}: needs exactly two senses with a layer each")
        if e.get("status") not in LEX_STATUS:
            errs.append(f"{where}: status {e.get('status')!r}")
        if not e.get("history"):
            errs.append(f"{where}: history missing")
        try:
            n = sum(1 for t in corpus if re.search(e["pattern"], t))
        except (KeyError, re.error) as x:
            errs.append(f"{where}: bad pattern ({x})")
            continue
        if n != e.get("corpus_verses"):
            errs.append(f"{where}: corpus_verses {e.get('corpus_verses')} but the pattern matches {n}")
        if sorted(u["verse"] for u in e.get("uses", [])) != sorted(e.get("verses", [])):
            errs.append(f"{where}: verses and uses disagree")
        for u in e.get("uses", []):
            vs = u["verse"]
            if str(vs) not in ctx["pilot"]:
                errs.append(f"{where}: verse {vs} is not a pilot verse")
                continue
            if not re.search(e["pattern"], texts[vs]):
                errs.append(f"{where}: pattern not found in verse {vs}")
            for lid in u["layers"]:
                uses.add((vs, lid, i))
    for (vs, lid, i) in sorted(uses - ctx["cited"], key=str):
        errs.append(f"lexicon {i}: lists verse {vs} layer {lid}, but that reading does not cite it")
    for (vs, lid, i) in sorted(ctx["cited"] - uses, key=str):
        errs.append(f"verse {vs} layer {lid} cites lexicon {i}, which does not list that use")
    st = Counter(e.get("status") for e in lex.get("entries", []))
    reviewed = st["accepted"] + st["rejected"]
    rate = f"{st['accepted'] / reviewed:.0%}" if reviewed else "n/a (none reviewed yet)"
    ctx["lex_line"] = (f"  lexicon v{lex.get('version')}: {len(lex.get('entries', []))} entries, "
                       f"{st['proposed']} proposed, {st['accepted']} accepted, {st['rejected']} rejected; "
                       f"acceptance rate {rate}")
    return errs


def summary(files):
    lay, conf, links_by_layer, single, types = Counter(), Counter(), Counter(), Counter(), Counter()
    places, modes, verdicts, keys_used = Counter(), Counter(), Counter(), Counter()
    nverses = nlinks = 0
    for d in files.values():
        for v in d["verses"].values():
            nverses += 1
            for lid, l in v["layers"].items():
                lay[lid] += 1
                conf[(lid, l["confidence"])] += 1
                for k in l["keys"]:
                    keys_used[k] += 1
            for e in v["body_place"]:
                places[e["place"]] += 1
            for e in v["knows_by"]:
                modes[(e["mode"], e["stance"])] += 1
        for l in d.get("links", []):
            nlinks += 1
            links_by_layer[l["layer"]] += 1
            types[l["type"]] += 1
            if not l["also_holds_on"]:
                single[l["layer"]] += 1
        for o in d.get("old_links", []):
            verdicts[o["verdict"]] += 1
    print(f"{len(files)} chapters, {nverses} verses, {nlinks} links")
    for lid in LAYERS:
        cs = ", ".join(f"{c} {conf[(lid, c)]}" for c in ("high", "med", "low"))
        print(f"  layer {lid:<14} on {lay[lid]:>3} verses ({cs}); links {links_by_layer[lid]:>2}, "
              f"of which single-layer {single[lid]}")
    print("  link types:", dict(types))
    print(f"  links depending on one layer only: {sum(single.values())} of {nlinks}")
    print("  keys applied:", dict(keys_used.most_common()))
    print("  body places:", dict(places.most_common()))
    print("  knows_by:", {f"{m}/{s}": n for (m, s), n in sorted(modes.items())})
    print("  old-link verdicts:", dict(verdicts))
    same = lambda pair: bool(set(pair[0]) & set(pair[1]))
    nl = [l for d in files.values() for l in d.get("links", [])]
    print(f"  new links joining the same stance: {sum(same(l['stances']) for l in nl)} of {len(nl)}")
    g = Counter()
    for d in files.values():
        for o in d.get("old_links", []):
            g[("same" if same(o["stances"]) else "different", o["old_grade"])] += 1
    for rel in ("same", "different"):
        row = {gr: g[(rel, gr)] for gr in ("sound", "weak", "forced", "wrong")}
        tot = sum(row.values())
        print(f"  old links, {rel} stance: {tot} ({row}; sound {row['sound'] / tot:.0%})" if tot else f"  old links, {rel} stance: 0")


def main():
    files = load_layer_files()
    wanted = [int(a) for a in sys.argv[1:]] or sorted(files)
    verses, chapters, _ = book_marks.load("siddhar")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))["links"]
    pilot = {}
    for d in files.values():
        pilot.update(d.get("verses", {}))
    lex = json.loads(LEXICON.read_text(encoding="utf-8")) if LEXICON.exists() else {"entries": []}
    ctx = {"verses": verses, "chapters": chapters, "keys": table("keys"), "places": table("places"),
           "stances": table("stances"), "lex": {e["id"] for e in lex["entries"]}, "cited": set(),
           "pilot": pilot, "all_pilot": set(pilot), "finished": {}, "warn": [], "audit": audit,
           "audit_pairs": {frozenset((str(o["a"]), str(o["b"]))): o for o in audit}}
    bad = 0
    for c in wanted:
        if c not in files:
            print(f"ch{c:03d}: no layer file")
            bad += 1
            continue
        errs = check_chapter(c, files[c], ctx)
        bad += bool(errs)
        print(f"ch{c:03d}: {'ok' if not errs else str(len(errs)) + ' problems'}")
        for e in errs:
            print("   ", e)
    if not sys.argv[1:]:
        lerrs = check_lexicon(ctx, verses)
        print(f"cipher_lexicon.json: {'ok' if not lerrs else str(len(lerrs)) + ' problems'}")
        for e in lerrs:
            print("   ", e)
        bad += bool(lerrs)
    for w in ctx["warn"]:
        print("  warning:", w)
    if not bad:
        summary({c: files[c] for c in wanted if c in files})
        if ctx.get("lex_line"):
            print(ctx["lex_line"])
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
