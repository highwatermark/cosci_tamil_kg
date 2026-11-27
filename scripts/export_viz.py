#!/usr/bin/env python3
"""Export every book's graph for the explorer (viz/index.html), one data file per corpus group.

  viz/data_core.js      window.KG: concepts, threads, the book and group registry, the bridge summary,
                        the concept taxonomy (kg/themes/concept_categories.json) and per-concept stats,
                        and window.KG_FILES, the group files the page loads after it
  viz/data_<group>.js   that group's chapters, verses and links (the links proposed from its books),
                        pushed onto window.KG_PARTS; a group larger than LIMIT is split by book into
                        data_<group>_2.js and so on

No file may exceed LIMIT (16 MB); the export stops if one does.

Sources: the five kept graphs (kg/kural, naladiyar, tirumanthiram, thiruppugazh, siddhar; the Kural
and Naladiyar go in the ethics file, the other three in the devotional file) and the group graphs
(kg/groups/<group>/, built by scripts/build_group_graphs.py), which hold every marked book, the
Akananuru, Purananuru and Pattupattu included.

Ids are "<prefix>:<key>" (BOOKS below gives each book's prefix). The kept prefixes: k Kural, n Naladiyar,
t Tirumanthiram, p Thiruppugazh, s Siddhar songs, a Akananuru, pn Purananuru, pp Pattupattu
(pp:<idyll>:<start>-<end>). A unit book's verse is <prefix>:<record>:<start>-<end> (si:2:1-11), a
Paripadal song pr:<song> or a cut of one pr:<song>:<start>-<end>. Chapter ids are <prefix>:<N>.
"""
import importlib.util
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VIZ = ROOT / "viz"
GROUPS = ROOT / "kg" / "groups"
LIMIT = 16 * 1024 * 1024
KEPT = {"kural": "k", "naladiyar": "n", "tirumanthiram": "t", "thiruppugazh": "p", "siddhar": "s"}

# book: (prefix, English name, Tamil name, hue, what a verse is called). The first eight keep the
# explorer's earlier prefixes and colours; the hue is for the new books' own colour.
BOOKS = {
    "kural": ("k", "Kural", "திருக்குறள்", None, "couplets"),
    "naladiyar": ("n", "Naladiyar", "நாலடியார்", None, "quatrains"),
    "tirumanthiram": ("t", "Tirumanthiram", "திருமந்திரம்", None, "verses"),
    "thiruppugazh": ("p", "Thiruppugazh", "திருப்புகழ்", None, "songs"),
    "siddhar": ("s", "Siddhar", "சித்தர் பாடல்கள்", None, "verses"),
    "akananuru": ("a", "Akananuru", "அகநானூறு", None, "poems"),
    "purananuru": ("pn", "Purananuru", "புறநானூறு", None, "poems"),
    "pattupattu": ("pp", "Pattupattu", "பத்துப்பாட்டு", None, "units"),
    "natrinai": ("nt", "Natrinai", "நற்றிணை", 118, "poems"),
    "kuruntokai": ("ku", "Kuruntokai", "குறுந்தொகை", 160, "poems"),
    "ainkurunuru": ("ai", "Ainkurunuru", "ஐங்குறுநூறு", 95, "poems"),
    "kalittokai": ("kl", "Kalittokai", "கலித்தொகை", 175, "poems"),
    "patitruppattu": ("pt", "Patitruppattu", "பதிற்றுப்பத்து", 22, "poems"),
    "paripadal": ("pr", "Paripadal", "பரிபாடல்", 45, "songs"),
    "kar_narpathu": ("kn", "Kar Narpathu", "கார் நாற்பது", 70, "verses"),
    "ainthinai_aimpathu": ("aa", "Ainthinai Aimpathu", "ஐந்திணை ஐம்பது", 82, "verses"),
    "thinaimozhi_aimpathu": ("ti", "Thinaimozhi Aimpathu", "திணைமொழி ஐம்பது", 100, "verses"),
    "ainthinai_ezhupathu": ("ae", "Ainthinai Ezhupathu", "ஐந்திணை எழுபது", 58, "verses"),
    "thinaimalai_nootraimpathu": ("tn", "Thinaimalai Nootraimpathu", "திணைமாலை நூற்றைம்பது", 135, "verses"),
    "kainnilai": ("ki", "Kainnilai", "கைந்நிலை", 64, "verses"),
    "kalavazhi_narpathu": ("kv", "Kalavazhi Narpathu", "களவழி நாற்பது", 0, "verses"),
    "nanmanikkadigai": ("nm", "Nanmanikkadigai", "நான்மணிக்கடிகை", 185, "verses"),
    "innaa_narpathu": ("in", "Innaa Narpathu", "இன்னா நாற்பது", 200, "verses"),
    "iniyavai_narpathu": ("iv", "Iniyavai Narpathu", "இனியவை நாற்பது", 192, "verses"),
    "thirikadugam": ("tk", "Thirikadugam", "திரிகடுகம்", 215, "verses"),
    "acharakkovai": ("ac", "Acharakkovai", "ஆசாரக்கோவை", 228, "verses"),
    "pazhamozhi_nanooru": ("pz", "Pazhamozhi Nanooru", "பழமொழி நானூறு", 168, "verses"),
    "sirupanchamoolam": ("sp", "Sirupanchamoolam", "சிறுபஞ்சமூலம்", 240, "verses"),
    "muthumozhikkanchi": ("mk", "Muthumozhikkanchi", "முதுமொழிக்காஞ்சி", 252, "sayings"),
    "elathi": ("el", "Elathi", "ஏலாதி", 205, "verses"),
    "silappathikaram": ("si", "Silappathikaram", "சிலப்பதிகாரம்", 300, "units"),
    "manimekalai": ("mm", "Manimekalai", "மணிமேகலை", 322, "units"),
    "civaka_cintamani": ("cc", "Civaka Cintamani", "சீவக சிந்தாமணி", 280, "verses"),
    "valayapathi": ("vp", "Valayapathi", "வளையாபதி", 338, "verses"),
    "kundalakesi": ("kd", "Kundalakesi", "குண்டலகேசி", 265, "verses"),
    "soolamani": ("so", "Soolamani", "சூளாமணி", 32, "verses"),
    "neelakesi": ("nk", "Neelakesi", "நீலகேசி", 350, "verses"),
    "naga_kumara_kaviyam": ("ng", "Naga Kumara Kaviyam", "நாககுமார காவியம்", 12, "verses"),
    "udayana_kumara_kaviyam": ("ud", "Udayana Kumara Kaviyam", "உதயணகுமார காவியம்", 52, "verses"),
    "yasodhara_kaviyam": ("ya", "Yasodhara Kaviyam", "யசோதர காவியம்", 4, "verses"),
}
PREFIX = {b: v[0] for b, v in BOOKS.items()}
assert len(set(PREFIX.values())) == len(PREFIX), "prefixes must be unique"


def shapes():
    """A distinct shape for each new book: stars of 3 to 9 points at three depths, then polygons."""
    out = []
    for inner in (0.45, 0.72, 0.28):
        for n in (4, 6, 7, 8, 3, 5, 9):
            if (n, inner) not in ((5, 0.45),):  # the Thiruppugazh's star
                out.append({"kind": "star", "n": n, "inner": inner})
    for n, turn in ((5, 0.5), (7, 0.5), (8, 0.0), (8, 0.125), (5, 0.0), (9, 0.5)):
        out.append({"kind": "poly", "n": n, "turn": turn})
    for n in (10, 12, 3, 4, 6, 8, 10, 12):
        out.append({"kind": "star", "n": n, "inner": 0.58 if n in (3, 4, 6, 8) or len(out) % 2 else 0.8})
    return out


def load_module(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def short(node_id):
    """kural:12 -> k:12, chapter:3 -> k:3, naladiyar-chapter:3 -> n:3, silappathikaram:2:1-11 -> si:2:1-11."""
    book, rest = node_id.split(":", 1)
    if book == "chapter":
        return "k:" + rest
    if book.endswith("-chapter"):
        book = book[:-len("-chapter")]
    return PREFIX[book] + ":" + rest


PUBLIC_DOMAIN_COMMENTATORS = {"parimelazhagar", "manakkudavar"}


def kept_book(book, folder, part):
    """The five kept graphs, exported as before."""
    prefix = KEPT[book]
    nodes = read_jsonl(folder / "nodes.jsonl")
    edges = read_jsonl(folder / "edges.jsonl")
    for n in nodes:
        if n["type"] == "Chapter":
            part["chapters"][f"{prefix}:{n['number']}"] = {"book": book, "num": n["number"], "title": n["title"],
                                                           "section": n["section"], "theme": n["theme"]}
        elif n["type"] == "Concept":
            part["concepts"][n["id"].split(":")[1]] = {"tamil": n.get("tamil", ""), "gloss": n.get("gloss", "")}
        elif n["type"] == "Verse":
            pope = n["pope"]["gloss"] if isinstance(n["pope"], dict) else n["pope"]
            v = {"book": book, "num": n["number"], "t": n["tamil"], "p": pope, "r": n["reading"],
                 "n": n["nuance"], "x": int(n["contested"]), "u": int(n["uncertain"]),
                 "f": int(n.get("text_needs_review", False)), "c": [], "pos": []}
            if book == "siddhar":
                v["who"] = n["siddhar"]
            part["verses"][f"{prefix}:{n['number']}"] = v
    for e in edges:
        if e["p"] == "IN_CHAPTER":
            part["verses"][short(e["s"])]["ch"] = short(e["o"])
        elif e["p"] == "EXPRESSES":
            part["verses"][short(e["s"])]["c"].append(e["o"].split(":")[1])
        elif e["p"] == "READS":
            who = e["s"].split(":")[1]
            # Quote only the medieval commentators; modern commentaries are in copyright (read, never quoted).
            quote = e["quote"] if who in PUBLIC_DOMAIN_COMMENTATORS else ""
            part["verses"][short(e["o"])]["pos"].append([who, e["position"], quote])
        elif "note" in e:
            part["links"].append({"a": short(e["s"]), "b": short(e["o"]), "type": e["p"].lower(),
                                  "note": e["note"], "grade": e["audit"], "better": e.get("audit_better_type")})
    threads = []
    if (folder / "threads.json").exists():
        names = {"k": "Kural", "n": "Naladiyar", "t": "Tirumanthiram", "p": "Thiruppugazh", "s": "Siddhars"}
        for t in json.loads((folder / "threads.json").read_text(encoding="utf-8")):
            pairs = [[short(x) if isinstance(x, str) else f"{prefix}:{x}" for x in pair] for pair in t["links"]]
            books = sorted({names[x.split(":")[0]] for pair in pairs for x in pair}, key=list(names.values()).index)
            threads.append({"id": t["id"], "title": t["title"], "claim": t["claim"], "grade": t["audit_grade"],
                            "links": pairs, "books": books, "limits": t.get("limits", ""), "issue": t.get("audit_issue", "")})
    return threads


def chapter_sections(book, bm):
    """{chapter number: section} for the grid: the kandam or section if a book has few, else its Tamil name."""
    chs = bm.load_sangam(book)[1] if book in bm.SANGAM else bm.load_new(book)[1]
    sec = {}
    for c, ch in chs.items():
        r = ch["record"]
        sec[c] = r.get("kandam") or r.get("section") or None
    distinct = {s for s in sec.values() if s}
    if book == "akananuru":
        return {c: ch["title"].rsplit(" ", 1)[0] for c, ch in chs.items()}
    if not distinct or len(distinct) > 15 or book in ("pattupattu", "paripadal"):
        if book == "pattupattu":
            return {c: ch["record"]["title"] for c, ch in chs.items()}
        return {c: BOOKS[book][2] for c in chs}
    last = BOOKS[book][2]
    for c in sorted(sec):
        sec[c] = sec[c] or last
        last = sec[c]
    return sec


def verse_name(n):
    """Display name and short label of a group-graph verse."""
    book = n["book"]
    name, pre = BOOKS[book][1], PREFIX[book].upper()
    rest = n["id"].split(":", 1)[1]
    if book == "pattupattu":
        return f"{n['idyll_name']} {n['start']}-{n['end']}", f"PP{n['idyll']}:{n['start']}-{n['end']}"
    if ":" in rest or (not n["whole"]):
        rec = rest.split(":")[0]
        return f"{name} {rec}, lines {n['start']}-{n['end']}", f"{pre}{rec}:{n['start']}-{n['end']}"
    return f"{name} {rest}", f"{pre}{rest}"


def group_book_verses(group, part, bm, marker):
    nodes = read_jsonl(GROUPS / group / "nodes.jsonl")
    edges = read_jsonl(GROUPS / group / "edges.jsonl")
    persons = {n["id"]: n for n in nodes if n["type"] == "Person"}
    secs = {}
    order = Counter()
    for n in nodes:
        if n["type"] == "Chapter":
            b = n["book"]
            if b not in secs:
                secs[b] = chapter_sections(b, bm)
            part["chapters"][short(n["id"])] = {"book": b, "num": n["number"], "title": n["title"],
                                               "section": secs[b].get(n["number"], BOOKS[b][2]), "theme": n["theme"]}
        elif n["type"] == "Verse":
            b = n["book"]
            order[b] += 1
            nm, lb = verse_name(n)
            v = {"book": b, "num": order[b], "t": n["tamil"], "p": "", "r": n["reading"], "n": n["nuance"] or "",
                 "x": 0, "u": int(n["uncertain"]), "f": int(n["text_needs_review"]), "c": [], "pos": [],
                 "nm": nm, "lb": lb}
            if n.get("marker_model") == "sonnet":
                v["mm"] = 1
                marker[b] += 1
            if n.get("poet"):
                v["poet"] = n["poet"]
            fs = n["field_set"]
            if fs in ("akam", "puram", "devotional"):
                col = n.get("colophon") or {}
                v |= {"pat": n.get("patron") or "", "ap": n.get("akam_puram") or "", "th": n.get("thinai") or "",
                      "cth": col.get("thinai") or "", "ctu": col.get("thurai") or "", "thd": int(bool(n.get("thinai_differs"))),
                      "uri": n.get("uri") or "", "mx": int(bool(n.get("mixed"))),
                      "sp": [[a.get("speaker"), a.get("addressee"), a.get("overhearer"),
                              (a.get("occasion") or {}).get("stage"), (a.get("occasion") or {}).get("words")]
                             for a in n.get("thurai_akam") or [] if isinstance(a, dict)],
                      "pt": [x.get("name") for x in n.get("puram_thurai") or [] if isinstance(x, dict)],
                      "mp": [[m.get("feeling"), m.get("cause")] for m in n.get("meyppadu") or [] if isinstance(m, dict)],
                      "k": [], "en": [], "dv": []}
                for field in ("ullurai", "iraicchi"):
                    d = n.get(field)
                    if d:
                        thing = d.get("vehicle") if field == "ullurai" else d.get("carrier")
                        things = thing if isinstance(thing, list) else [thing]
                        forms = " ".join(x.get("form", "") for x in things if isinstance(x, dict))
                        gloss = d.get("tenor") if field == "ullurai" else d.get("sense")
                        v["dv"].append([field, forms, d.get("status"), d.get("graders_agree"), gloss or ""])
                for field in n.get("devices_grader_only") or []:
                    v["dv"].append([field, "", "grader_only", None, ""])
            elif fs == "ethics":
                v |= {"dm": n.get("domain") or "", "it": [], "cw": n.get("count_word") or ""}
                pz = n.get("pazhamozhi")
                if isinstance(pz, dict):
                    st = pz.get("story") or {}
                    v["pz"] = [pz.get("proverb") or "", pz.get("literal") or "", pz.get("applied_to") or "",
                               st.get("kind") or "", st.get("who") or "", st.get("act") or ""]
                nr = n.get("norm")
                if isinstance(nr, dict):
                    v["nr"] = [nr.get("kinds") or [], nr.get("note") or ""]
            else:
                sp = n.get("speaker") or {}
                v |= {"ev": n.get("event") or "", "cl": [], "ag": [], "ec": []}
                if sp.get("who") and sp["who"] != "narrator":
                    who = persons.get(f"person:{b}:{sp['who']}", {})
                    to = persons.get(f"person:{b}:{sp.get('addressee')}", {}) if sp.get("addressee") else {}
                    v["spk"] = [who.get("tamil") or sp["who"], to.get("tamil") or sp.get("addressee") or ""]
            part["verses"][short(n["id"])] = v
    links = []
    for e in edges:
        p = e["p"]
        if p == "IN_CHAPTER":
            part["verses"][short(e["s"])]["ch"] = short(e["o"])
        elif p == "EXPRESSES":
            part["verses"][short(e["s"])]["c"].append(e["o"].split(":", 1)[1])
        elif p == "NAMES" and e["o"].startswith("karu:"):
            part["verses"][short(e["s"])]["k"].append([e.get("form"), e["o"][5:], e.get("line"), e.get("kind"),
                                                       e.get("role"), e.get("sense") or ""])
        elif p == "NAMES":
            v = part["verses"][short(e["s"])]
            v.setdefault("en", []).append([e["entity_type"], e["o"].split(":", 2)[2], e.get("line")])
        elif p == "LISTS":
            part["verses"][short(e["s"])]["it"].append([e.get("form"), e.get("claim"), e.get("line")])
        elif p == "CLAIMS":
            part["verses"][short(e["s"])]["cl"].append([e.get("claim"), e["o"].split(":", 1)[1], e.get("stance"),
                                                        e.get("line"), e.get("voiced_by")])
        elif p == "ACTS":
            part["verses"][short(e["o"])]["ag"].append(persons.get(e["s"], {}).get("tamil") or e["s"].rsplit(":", 1)[1])
        elif p == "ECHOES":
            part["verses"][short(e["s"])]["ec"].append([short(e["o"]), e.get("kind")])
        elif "teaches" in e:
            links.append(e)
    return links


def concept_taxonomy(parts, concepts):
    """The concept taxonomy (kg/themes/concept_categories.json) and, per concept, what the Concepts view shows:
    verses by group, sound links touching it, the concepts it most often shares a verse with, and up to eight
    sound links between groups whose two verses (or failing that, one) express it. Every concept must be placed."""
    tax = json.loads((ROOT / "kg" / "themes" / "concept_categories.json").read_text(encoding="utf-8"))
    placed = tax["placement"]
    unplaced = sorted(set(concepts) - set(placed))
    if unplaced:
        raise SystemExit(f"concept_categories.json leaves {len(unplaced)} concepts unplaced: {', '.join(unplaced)}")
    group_of_verse, vcon = {}, {}
    for group, part in parts.items():
        for vid, v in part["verses"].items():
            group_of_verse[vid] = group
            vcon[vid] = v["c"]
    by_group, pair = defaultdict(Counter), Counter()
    for vid, cs in vcon.items():
        for c in cs:
            by_group[c][group_of_verse[vid]] += 1
        for i, a in enumerate(cs):
            for b in cs[i + 1:]:
                pair[(a, b) if a < b else (b, a)] += 1
    total = {c: sum(g.values()) for c, g in by_group.items()}
    near = defaultdict(list)
    for (a, b), n in pair.items():
        if n >= 2:
            near[a].append((b, n))
            near[b].append((a, n))
    sound, bridges = Counter(), defaultdict(list)
    for part in parts.values():
        for l in part["links"]:
            if l["grade"] != "sound":
                continue
            ca, cb = set(vcon.get(l["a"], ())), set(vcon.get(l["b"], ()))
            for c in ca | cb:
                sound[c] += 1
            if group_of_verse.get(l["a"]) != group_of_verse.get(l["b"]):
                for c in ca | cb:
                    bridges[c].append((0 if (c in ca and c in cb) else 1, l["a"], l["b"]))
    stats = {}
    for c in concepts:
        # co-occurring concepts ranked by shared verses, damped by the other concept's size so the
        # most frequent concepts (kaamam, azhagu) do not head every list
        co = sorted(near[c], key=lambda t: (-t[1] / (total.get(t[0], 1) ** 0.5), t[0]))[:10]
        br, seen = [], Counter()
        for both, a, b in sorted(bridges[c]):
            key = tuple(sorted((group_of_verse[a], group_of_verse[b])))
            if seen[key] < 2 and len(br) < 8:  # at most two per pair of groups, both-ends first
                seen[key] += 1
                br.append([a, b, 1 - both])
        stats[c] = {"n": total.get(c, 0), "g": dict(by_group[c]), "s": sound[c],
                    "co": [[o, n] for o, n in sorted(co, key=lambda t: -t[1])], "br": br}
    # distinct verses by group for every category and subtheme (primary placements only)
    ids = {}
    for cat in tax["categories"]:
        for sub in cat["subthemes"]:
            for c in sub["concepts"]:
                ids.setdefault(c, []).extend([cat["id"], sub["id"]])
    cat_groups = defaultdict(Counter)
    for vid, cs in vcon.items():
        for k in {k for c in cs for k in ids.get(c, ())}:
            cat_groups[k][group_of_verse[vid]] += 1
    return {"categories": tax["categories"], "placement": placed,
            "groups": {k: dict(v) for k, v in cat_groups.items()}}, stats


def main():
    bm = load_module("book_marks", "book_marks.py")
    index = json.loads((GROUPS / "index.json").read_text(encoding="utf-8"))
    bridges = json.loads((GROUPS / "bridges_summary.json").read_text(encoding="utf-8"))
    audit = json.loads((GROUPS / "all_link_audit.json").read_text(encoding="utf-8"))
    group_of = {b: g for g, e in index.items() for b in e["books"]}
    group_of["tholkappiyam"] = "grammar"
    concepts, threads, parts, raw_links = {}, [], {}, []
    marker = Counter()
    for group, entry in index.items():
        if group == "grammar":
            continue
        part = {"group": group, "chapters": {}, "verses": {}, "links": [], "concepts": {}}
        for book in entry["books"]:
            if book in KEPT:
                threads += kept_book(book, ROOT / "kg" / book, part)
        if entry.get("built_here"):
            raw_links += [(group, e) for e in group_book_verses(group, part, bm, marker)]
        concepts.update(part.pop("concepts"))
        parts[group] = part
    every = {vid for p in parts.values() for vid in p["verses"]}
    dropped = []
    for group, e in raw_links:
        s, o = short(e.get("s_unit") or e["s"]), short(e.get("o_unit") or e["o"])
        if s not in every or o not in every:
            dropped.append(e["o"])
            continue
        l = {"a": s, "b": o, "type": e["p"].lower(), "note": e["note"], "grade": e["audit"],
             "better": e.get("audit_better_type"), "te": e.get("teaches") or ""}
        if e.get("gains"):
            g = e["gains"]
            l["gn"] = [g.get("a") or "", g.get("b") or ""] if isinstance(g, dict) else [str(g), ""]
        if e.get("list_adds"):
            l["la"] = e["list_adds"]
        if e.get("audit_graders", 0) > 1:
            l["gr"] = e["audit_graders"]
        if e.get("marker_model") == "sonnet":
            l["mm"] = 1
        parts[group]["links"].append(l)
    threads.sort(key=lambda t: len(t["books"]) == 1)  # threads across books first; sort is stable
    concepts.update({c["id"]: {"tamil": c["tamil"], "gloss": c["gloss"]}
                     for c in json.loads((ROOT / "kg" / "themes" / "concepts.json").read_text(encoding="utf-8"))})
    taxonomy, cstats = concept_taxonomy(parts, concepts)
    shape_pool = iter(shapes())
    old_shape = {"kural": "circle", "naladiyar": "diamond", "tirumanthiram": "triangle", "thiruppugazh": "star",
                 "siddhar": "wye", "akananuru": "cross", "purananuru": "hexagon", "pattupattu": "down"}
    counts = Counter(v["book"] for p in parts.values() for v in p["verses"].values())
    books = {}
    for b, (prefix, name, tamil, hue, unit) in BOOKS.items():
        if not counts[b]:
            continue
        books[b] = {"prefix": prefix, "name": name, "tamil": tamil, "group": group_of[b], "unit": unit,
                    "hue": hue, "shape": old_shape.get(b) or next(shape_pool), "verses": counts[b],
                    "fs": "kept" if b in KEPT else ("akam" if b in bm.SANGAM else bm.NEW[b][0]),
                    "sonnet_verses": marker[b]}
    gsum = audit["by_group"]
    groups = {g: {"name": e["name"], "books": [b for b in e["books"] if b in books],
                  "sound_pct": (gsum.get(g) or {}).get("sound_pct"), "links": (gsum.get(g) or {}).get("links"),
                  "note": e.get("note")} for g, e in index.items()}
    files = []
    sizes = {}
    VIZ.mkdir(exist_ok=True)
    for old in VIZ.glob("data*.js"):
        old.unlink()
    for group, part in parts.items():
        # pack the group's books into files under LIMIT
        payload = json.dumps(part, ensure_ascii=False, separators=(",", ":"))
        chunks = [part]
        if len(payload.encode()) > LIMIT - 1024:
            by_book = defaultdict(lambda: {"group": group, "chapters": {}, "verses": {}, "links": []})
            for cid, c in part["chapters"].items():
                by_book[c["book"]]["chapters"][cid] = c
            for vid, v in part["verses"].items():
                by_book[v["book"]]["verses"][vid] = v
            for l in part["links"]:
                by_book[next(v["book"] for v in [part["verses"][l["a"]]])]["links"].append(l)
            chunks, cur, size = [], None, 0
            for b, sub in by_book.items():
                n = len(json.dumps(sub, ensure_ascii=False, separators=(",", ":")).encode())
                if cur is None or size + n > LIMIT - 1024:
                    cur, size = {"group": group, "chapters": {}, "verses": {}, "links": []}, 0
                    chunks.append(cur)
                for k in ("chapters", "verses"):
                    cur[k].update(sub[k])
                cur["links"] += sub["links"]
                size += n
        for i, chunk in enumerate(chunks, 1):
            name = f"data_{group}.js" if i == 1 else f"data_{group}_{i}.js"
            path = VIZ / name
            path.write_text("(window.KG_PARTS = window.KG_PARTS || []).push("
                            + json.dumps(chunk, ensure_ascii=False, separators=(",", ":")) + ");\n", encoding="utf-8")
            files.append(name)
            sizes[name] = path.stat().st_size
    core = {"concepts": concepts, "threads": threads, "books": books, "groups": groups,
            "bridges": {"pairs": bridges["pairs"], "within": bridges["within"]},
            "summary": {k: audit["summary"][k] for k in ("by_grade", "sound_pct", "by_marker_model_wave6", "by_grader_model")},
            "taxonomy": taxonomy, "cstats": cstats}
    path = VIZ / "data_core.js"
    path.write_text("window.KG = " + json.dumps(core, ensure_ascii=False, separators=(",", ":")) + ";\nwindow.KG_FILES = "
                    + json.dumps(files) + ";\n", encoding="utf-8")
    sizes["data_core.js"] = path.stat().st_size
    for name, size in sizes.items():
        if size > LIMIT:
            raise SystemExit(f"viz/{name} is {size} bytes, over the {LIMIT}-byte limit")
    nlinks = sum(len(p["links"]) for p in parts.values())
    print(f"books={len(books)} verses={sum(counts.values())} links={nlinks} dropped={len(dropped)} "
          f"({', '.join(sorted(set(dropped)))}) concepts={len(concepts)} threads={len(threads)}")
    for name, size in sorted(sizes.items(), key=lambda t: -t[1]):
        print(f"  viz/{name}: {size / 1048576:.2f} MB")


if __name__ == "__main__":
    main()
