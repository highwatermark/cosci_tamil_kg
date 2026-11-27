#!/usr/bin/env python3
"""Build one graph per corpus group (docs/corpus-groups.md) from the chapter marks and the merged audit.

Run scripts/merge_sangam_grades.py first (it writes kg/groups/all_link_audit.json, which this reads).
Writes, for each group with marked books, kg/groups/<group>/nodes.jsonl and edges.jsonl; then
kg/groups/bridges.jsonl (every link whose two ends are in different groups, with its grade),
kg/groups/bridges_summary.json (sound% by group pair, within-group pairs included as the baseline)
and kg/groups/index.json (each group's books, field sets, counts and graph files).

The Kural, Naladiyar, Tirumanthiram, Thiruppugazh and Siddhar graphs are kept as they are, in
kg/<book>/; the index lists them as members of the ethics and devotional groups, and their links
between groups go into bridges.jsonl. The Tholkappiyam is the grammar group's frame: cited, not linked.

Nodes
- Verse: <book>:<key> as the marks key it (a number, a Paripadal song or song:<start>-<end>, a unit
  <book>:<record>:<start>-<end>). Every verse carries the Tamil (public domain), reading, nuance,
  concepts, uncertain, text flags and the marker's model; then its field set's fields:
    akam, puram, devotional  akam_puram, colophon, thinai (+ evidence, differs from the colophon), mixed,
                             uri, mutal, meyppadu, thurai_akam, puram_thurai, comparisons, and the
                             ullurai and iraicchi with the status the blind re-tags gave them
    ethics                   domain, domain_note, count_word, pazhamozhi, norm (items are edges)
    narrative                speaker, event, unit_note (agents, claims and echoes are edges)
- Chapter: <book>-chapter:N (book_marks.py's numbers), with theme, notes and, for narrative, the cast.
- Concept nodes are kg/themes/concepts.json (not repeated here); Karu (karu:<stem>), Entity
  (entity:<type>:<name>), Item (item:<Tamil thing>), Norm (norm:<kind>), School (school:<name>) and
  Person (person:<book>:<cast id>) nodes are made from the marks.

Edges
- IN_CHAPTER; EXPRESSES (verse -> concept, ranked); NAMES (verse -> karu, verse -> entity);
  ULLURAI and IRAICCHI (verse -> karu, experimental, with re-tag status); LISTS (verse -> item, with
  position, claim, line); NORM (verse -> norm, historical); CLAIMS (verse -> school, with claim,
  stance, line, voiced_by); SPEAKS and ACTS (person -> verse); ECHOES (verse -> kural:N or naladiyar:N).
- Links (TENSION, AGREES, DEVELOPS, QUALIFIES, SAME_IMAGE, PARALLEL_DOMAIN) with note, teaches, gains,
  list_adds, item, the audit grade (strictest blind grade), graders, teaches/list_adds/gains_holds, and
  the two corpus groups. A link to a line span is kept as written and resolved to the marked unit it
  overlaps most (s_unit / o_unit).

Usage: python3 -I scripts/build_group_graphs.py
"""
import importlib.util
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES = ROOT / "kg" / "themes"
CORE = ROOT / "kg" / "core"
OUT = ROOT / "kg" / "groups"
EXISTING = ("kural", "naladiyar", "tirumanthiram", "thiruppugazh", "siddhar")
REVIEW_FLAGS = {"misprint_candidate", "edition_variant", "line_count", "lineation", "spelling",
                "colophon", "colophon_variant", "thinai", "lacuna", "source_variant", "missing_verse",
                "duplicate_verse", "variant", "witness_variant", "gap", "lost"}
GROUP_NAMES = {  # docs/corpus-groups.md, in its order
    "ettuthogai_akam": "Ettuthogai, akam", "ettuthogai_puram": "Ettuthogai, puram",
    "ettuthogai_devotional": "Ettuthogai, devotional", "pattupattu": "Pattupattu",
    "ethics": "Pathinenkilkanakku, ethics", "kilkanakku_akam": "Pathinenkilkanakku, akam",
    "epics_great": "Epics, great", "epics_minor": "Epics, minor",
    "devotional": "Devotional and mystic", "grammar": "Grammar"}
LINK_TYPES = {"tension", "agrees", "develops", "qualifies", "same_image", "parallel_domain"}


def load_module(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bm = load_module("book_marks", "book_marks.py")
mp = load_module("packets", "make_sangam_packets.py")
merge = load_module("merge", "merge_sangam_grades.py")
GROUP = dict(mp.GROUP) | {"tholkappiyam": "grammar"}
ref, book_of = mp.ref, mp.book_of


def read_jsonl(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def write_jsonl(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as out:
        for r in records:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")


def field_set(book):
    """akam, puram, devotional, ethics or narrative (the Sangam books' own checker is akam/puram)."""
    if book in bm.SANGAM:
        return {"akananuru": "akam", "purananuru": "puram", "pattupattu": "puram"}[book]
    return bm.NEW[book][0]


class Texts:
    """The Tamil lines and record of any verse id of a marked book."""

    def __init__(self):
        self.core = {}
        self.idylls = {p["number"]: p for p in read_jsonl(CORE / "pattupattu.jsonl")}

    def records(self, book):
        if book not in self.core:
            if book in ("akananuru", "purananuru"):
                rs = [r for r in read_jsonl(CORE / f"{book}.jsonl") if r.get("tamil")]
                self.core[book] = {str(r["number"]): r for r in rs}
            else:
                self.core[book] = {bm.key_of(book, r): r for r in bm.core_records(book)}
        return self.core[book]

    def resolve(self, vid):
        """(record, first line, last line, record key) or None."""
        book, rest = vid.split(":", 1)
        if book == "pattupattu":
            m = bm.PATTU_ID.fullmatch(vid)
            if not m:
                return None
            n, a, z = (int(g) for g in m.groups())
            p = self.idylls.get(n)
            return (p, a, z, str(n)) if p and 1 <= a <= z <= p["line_count"] else None
        if book not in bm.SANGAM and book not in bm.NEW:
            return None
        recs = self.records(book)
        if rest in recs:
            return recs[rest], 1, len(recs[rest]["tamil"]), rest
        m = re.fullmatch(r"(.+):(\d+)-(\d+)", rest)
        if m and m.group(1) in recs:
            r = recs[m.group(1)]
            a, z = int(m.group(2)), int(m.group(3))
            if 1 <= a <= z <= len(r["tamil"]):
                return r, a, z, m.group(1)
        return None


def chapters_of(book):
    if book in bm.SANGAM:
        return bm.load_sangam(book)[1]
    return bm.load_new(book)[1]


def device_objects(mark, rt):
    out = {}
    for field in ("ullurai", "iraicchi"):
        obj = mark.get(field)
        if obj:
            status = rt[f"{field}_status"] if rt else "not_retagged"
            out[field] = obj | {"status": status, "graders_agree": rt[f"{field}_graders_agree"] if rt else None}
        else:
            out[field] = None
    return out


THINAI_TAMIL = {"kurinji": "குறிஞ்சி", "mullai": "முல்லை", "marutham": "மருதம்", "neythal": "நெய்தல்",
                "paalai": "பாலை", "kaikkilai": "கைக்கிளை", "perunthinai": "பெருந்திணை", "vetchi": "வெட்சி",
                "karanthai": "கரந்தை", "vanji": "வஞ்சி", "kaanchi": "காஞ்சி", "uzhinai": "உழிஞை",
                "nochchi": "நொச்சி", "thumbai": "தும்பை", "vaakai": "வாகை", "paadaan": "பாடாண்",
                "pothuviyal": "பொதுவியல்"}


def colophon_differs(ours, theirs):
    if not ours or not theirs:
        return None
    t = THINAI_TAMIL.get(ours)
    return None if t is None else t not in theirs


def marked_units(books, texts):
    """Every marked verse id, and {(book, record key): [(start, end, id)]}, across all groups, so a link
    into another group's line span resolves to the unit marked there."""
    ids, units = set(), defaultdict(list)
    for book in books:
        for path in sorted((THEMES / book).glob("ch*.json")):
            for key in json.loads(path.read_text(encoding="utf-8"))["verses"]:
                vid = ref(book, key)
                res = texts.resolve(vid)
                if res:
                    ids.add(vid)
                    units[(book, res[3])].append((res[1], res[2], vid))
    return ids, units


def build_group(group, books, texts, audit, retags, part_b, flags, verse_ids, units):
    nodes, edges, pending = [], [], []
    aux = {}  # id -> aux node with a verse set

    def aux_node(nid, base):
        n = aux.setdefault(nid, base | {"verses": set()})
        return n

    for book in books:
        fs = field_set(book)
        chs = chapters_of(book)
        for path in sorted((THEMES / book).glob("ch*.json")):
            ch = json.loads(path.read_text(encoding="utf-8"))
            number = ch["chapter_no"]
            meta = chs.get(number, {})
            chapter_id = f"{book}-chapter:{number}"
            cast = {p["id"]: p for p in ch.get("cast") or [] if isinstance(p, dict) and p.get("id")}
            nodes.append({"id": chapter_id, "type": "Chapter", "book": book, "group": group, "number": number,
                          "title": meta.get("title", ""), "theme": ch.get("chapter_theme", ""),
                          "structure_note": ch.get("structure_note", ""), "source_issues": ch.get("source_issues", []),
                          "marker_model": merge.marker_model(book, number),
                          **({"cast": list(cast.values())} if fs == "narrative" else {}), "status": "proposed"})
            for pid, p in cast.items():
                aux_node(f"person:{book}:{pid}", {"id": f"person:{book}:{pid}", "type": "Person", "book": book,
                                                  "cast_id": pid, "tamil": p.get("tamil"), "role": p.get("role")})
            for key, mark in ch["verses"].items():
                vid = ref(book, key)
                res = texts.resolve(vid)
                if res is None or not isinstance(mark, dict):
                    print(f"warning: {vid} has no text; skipped")
                    continue
                rec, a, z, rkey = res
                tamil = rec["tamil"][a - 1:z]
                fl = [f for f in flags.get(rec["id"], [])
                      if not f.get("line") or a <= f["line"] <= z]
                review = sorted({f["kind"] for f in fl if f["kind"] in REVIEW_FLAGS})
                node = {"id": vid, "type": "Verse", "book": book, "group": group, "field_set": fs,
                        "chapter": number, "record": rec["id"], "number": rec.get("number"),
                        "start": a, "end": z, "whole": a == 1 and z == len(rec["tamil"]),
                        "section": rec.get("section") or rec.get("chapter") or rec.get("title"),
                        "kind": rec.get("kind"), "poet": rec.get("poet") or rec.get("author"),
                        "patron": rec.get("patron"), "tamil": tamil,
                        "reading": mark.get("reading", ""), "nuance": mark.get("nuance", ""),
                        "concepts": mark.get("concepts", []), "uncertain": bool(mark.get("uncertain")),
                        "text_needs_review": bool(review), "text_flags": review,
                        "marker_model": merge.marker_model(book, number), "status": "proposed"}
                if book == "pattupattu":
                    node |= {"idyll": rec["number"], "idyll_title": rec["title"],
                             "idyll_name": rec["short_name"].replace("_", " ").title(), "unit_note": mark.get("unit_note")}
                if fs in ("akam", "puram", "devotional"):
                    rt = retags.get(vid)
                    dev = device_objects(mark, rt)
                    col = mark.get("colophon") or {}
                    node |= {"akam_puram": mark.get("akam_puram"), "colophon": col, "thinai": mark.get("thinai"),
                             "thinai_evidence": mark.get("thinai_evidence"),
                             "thinai_differs": colophon_differs(mark.get("thinai"), col.get("thinai")),
                             "mixed": mark.get("mixed", False), "uri": mark.get("uri"), "mutal": mark.get("mutal"),
                             "meyppadu": mark.get("meyppadu", []), "thurai_akam": mark.get("thurai_akam", []),
                             "puram_thurai": mark.get("puram_thurai", []), "comparisons": mark.get("comparisons", []),
                             "ullurai": dev["ullurai"], "iraicchi": dev["iraicchi"],
                             "devices_grader_only": [f for f in ("ullurai", "iraicchi")
                                                     if rt and rt[f"{f}_status"] == "grader_only"]}
                    if mark.get("unit_note"):
                        node["unit_note"] = mark["unit_note"]
                elif fs == "ethics":
                    node |= {k: mark.get(k) for k in ("domain", "domain_note", "count_word", "pazhamozhi", "norm")}
                    node["items"] = len(mark.get("items") or [])
                else:
                    node |= {"speaker": mark.get("speaker"), "event": mark.get("event"), "unit_note": mark.get("unit_note"),
                             "claims": len(mark.get("claims") or []), "echoes": len(mark.get("echoes") or [])}
                if vid in part_b:
                    node["retag"] = {"graders": part_b[vid]["graders"], "agree": part_b[vid]["agree"]}
                nodes.append(node)
                edges.append({"s": vid, "p": "IN_CHAPTER", "o": chapter_id})
                for rank, c in enumerate(mark.get("concepts", []), 1):
                    edges.append({"s": vid, "p": "EXPRESSES", "o": f"concept:{c}", "rank": rank,
                                  "basis": "interpretation", "status": "proposed"})
                # akam / puram / devotional: karu, entities, devices
                stem_of_form = {}
                for k in mark.get("karu", []) or []:
                    stem = (k.get("stem") or k.get("form") or "").strip()
                    if not stem:
                        continue
                    kid = f"karu:{stem}"
                    kn = aux_node(kid, {"id": kid, "type": "Karu", "stem": stem, "kinds": Counter(),
                                        "roles": Counter(), "senses": Counter()})
                    kn["kinds"][k.get("kind")] += 1
                    kn["roles"][k.get("role")] += 1
                    if k.get("sense"):
                        kn["senses"][k["sense"]] += 1
                    kn["verses"].add(vid)
                    stem_of_form[(k.get("form"), k.get("line"))] = kid
                    edges.append({"s": vid, "p": "NAMES", "o": kid, "form": k.get("form"), "line": k.get("line"),
                                  "kind": k.get("kind"), "role": k.get("role"), "land": k.get("land"),
                                  "sense": k.get("sense"), "basis": "interpretation", "status": "proposed"})
                for e in mark.get("entities", []) or []:
                    eid = f"entity:{e['type']}:{e['name'].strip()}"
                    aux_node(eid, {"id": eid, "type": "Entity", "kind": e["type"], "name": e["name"].strip()})["verses"].add(vid)
                    edges.append({"s": vid, "p": "NAMES", "o": eid, "entity_type": e["type"], "line": e.get("line"),
                                  "basis": "text", "status": "proposed"})
                if fs in ("akam", "puram", "devotional"):
                    for field, thing in (("ullurai", "vehicle"), ("iraicchi", "carrier")):
                        obj = node[field]
                        if not obj:
                            continue
                        things = obj.get(thing)
                        things = things if isinstance(things, list) else [things]
                        done = set()
                        for t in things:
                            if not isinstance(t, dict):
                                continue
                            kid = (stem_of_form.get((t.get("form"), t.get("line")))
                                   or next((v for (f, _), v in stem_of_form.items() if f == t.get("form")), None)
                                   or f"karu:{t.get('form')}")
                            if kid in done:
                                continue
                            done.add(kid)
                            edge = {"s": vid, "p": field.upper(), "o": kid, "form": t.get("form"), "line": t.get("line"),
                                    "experimental": True, "status": obj["status"], "graders_agree": obj["graders_agree"],
                                    "basis": "interpretation"}
                            if field == "ullurai":
                                edge |= {"tenor": obj.get("tenor"), "anchor": obj.get("anchor")}
                            else:
                                edge |= {"act": obj.get("act"), "sense": obj.get("sense")}
                            edges.append(edge)
                # ethics: items and norms
                for pos, it in enumerate(mark.get("items") or [], 1):
                    if not isinstance(it, dict):
                        continue
                    thing = bm.tamil_only(it.get("thing")) or str(it.get("thing"))
                    iid = f"item:{thing}"
                    aux_node(iid, {"id": iid, "type": "Item", "thing": thing})["verses"].add(vid)
                    edges.append({"s": vid, "p": "LISTS", "o": iid, "position": pos, "form": it.get("thing"),
                                  "claim": it.get("claim"), "line": it.get("line"), "domain": it.get("domain"),
                                  "basis": "interpretation", "status": "proposed"})
                norm = mark.get("norm")
                if isinstance(norm, dict):
                    for kind in norm.get("kinds") or []:
                        nid = f"norm:{kind}"
                        aux_node(nid, {"id": nid, "type": "Norm", "kind": kind})["verses"].add(vid)
                        edges.append({"s": vid, "p": "NORM", "o": nid, "norm_note": norm.get("note"),
                                      "historical": True, "basis": "interpretation", "status": "proposed"})
                # narrative: claims, speaker, agents, echoes
                for cl in mark.get("claims") or []:
                    if not isinstance(cl, dict):
                        continue
                    sid = f"school:{cl.get('school')}"
                    aux_node(sid, {"id": sid, "type": "School", "name": cl.get("school")})["verses"].add(vid)
                    edges.append({"s": vid, "p": "CLAIMS", "o": sid, "claim": cl.get("claim"), "stance": cl.get("stance"),
                                  "school_detail": cl.get("school_detail"), "line": cl.get("line"),
                                  "voiced_by": cl.get("voiced_by"), "basis": "interpretation", "status": "proposed"})
                sp = mark.get("speaker") if fs == "narrative" else None
                if isinstance(sp, dict) and sp.get("who") in cast:
                    pid = f"person:{book}:{sp['who']}"
                    aux[pid]["verses"].add(vid)
                    edges.append({"s": pid, "p": "SPEAKS", "o": vid, "form": sp.get("form"), "line": sp.get("line"),
                                  "addressee": sp.get("addressee"), "basis": "text", "status": "proposed"})
                for ag in (mark.get("agents") or []) if fs == "narrative" else []:
                    if isinstance(ag, dict) and ag.get("id") in cast:
                        pid = f"person:{book}:{ag['id']}"
                        aux[pid]["verses"].add(vid)
                        edges.append({"s": pid, "p": "ACTS", "o": vid, "form": ag.get("form"), "line": ag.get("line"),
                                      "basis": "text", "status": "proposed"})
                for ec in mark.get("echoes") or []:
                    if isinstance(ec, dict) and ec.get("b"):
                        edges.append({"s": vid, "p": "ECHOES", "o": str(ec["b"]), "kind": ec.get("kind"),
                                      "words": ec.get("words"), "line": ec.get("line"), "marked": ec.get("marked"),
                                      "basis": "text", "status": "proposed"})
            for link in ch.get("links", []):
                pending.append((book, number, link))

    def unit_for(target):
        if target in verse_ids:
            return None
        res = texts.resolve(target) if book_of(target) in bm.NEW or book_of(target) in bm.SANGAM else None
        if res is None:
            return None
        _, a, z, rkey = res
        best = max(((min(z, e) - max(a, s) + 1, uid) for s, e, uid in units.get((book_of(target), rkey), [])), default=None)
        return best[1] if best and best[0] > 0 else None

    links = []
    for book, number, link in pending:
        s, o = ref(book, link["a"]), ref(book, link["b"])
        g = audit.get((s, o), {})
        ga, gb = GROUP.get(book_of(s)), GROUP.get(book_of(o))
        edge = {"s": s, "p": str(link.get("type", "")).upper(), "o": o, "note": link.get("note"),
                "teaches": link.get("teaches"), "basis": "interpretation", "status": "proposed", "pass": "marking",
                "audit": g.get("grade", "not_audited"), "audit_graders": g.get("graders", 0),
                "source": f"{book}_marks", "chapter": f"{book}-chapter:{number}",
                "marker_model": merge.marker_model(book, number),
                "cross_book": book_of(o) != book_of(s), "group_a": ga, "group_b": gb, "within_group": ga == gb}
        for k in ("gains", "list_adds", "item"):
            if link.get(k) is not None:
                edge[k] = link[k]
        for k in ("s", "o"):
            u = unit_for(edge[k])
            if u:
                edge[f"{k}_unit"] = u
        if g:
            edge["audit_teaches_holds"] = g.get("teaches_holds")
            for k in ("list_adds_holds", "gains_holds"):
                if k in g:
                    edge[f"audit_{k}"] = g[k]
            if g.get("better_type"):
                edge["audit_better_type"] = g["better_type"]
            if g.get("text_issue"):
                edge["audit_text_issue"] = g["text_issue"]
            edge["audit_disagree"] = g.get("disagree")
        edges.append(edge)
        links.append(edge)
    for n in aux.values():
        for f in ("kinds", "roles", "senses"):
            if f in n:
                n[f] = dict(n[f])
        if "kinds" in n:
            n["kind"] = max(n["kinds"], key=n["kinds"].get)
        n["verses"] = len(n["verses"])
    nodes += sorted(aux.values(), key=lambda n: n["id"])
    write_jsonl(OUT / group / "nodes.jsonl", nodes)
    write_jsonl(OUT / group / "edges.jsonl", edges)
    return nodes, edges, links


def existing_links():
    """The links of the five graphs kept as they are, with their groups."""
    out = []
    for b in EXISTING:
        for e in read_jsonl(ROOT / "kg" / b / "edges.jsonl"):
            if "note" not in e or "audit" not in e or e["p"].lower() not in LINK_TYPES:
                continue
            ga, gb = GROUP.get(book_of(e["s"])), GROUP.get(book_of(e["o"]))
            out.append(e | {"group_a": ga, "group_b": gb, "within_group": ga == gb, "source": e.get("source", f"{b}_graph")})
    return out


def pair_table(links):
    """{"a|b": counts} for unordered group pairs, and the directed counts."""
    und, dirc = defaultdict(Counter), defaultdict(Counter)
    for l in links:
        ga, gb = l["group_a"], l["group_b"]
        if not ga or not gb:
            continue
        for tab, key in ((und, "|".join(sorted((ga, gb)))), (dirc, f"{ga}|{gb}")):
            tab[key][l["audit"]] += 1
            tab[key]["n"] += 1
    fmt = lambda t: {k: {"links": c["n"], "graded": c["n"] - c["not_audited"], "sound": c["sound"], "weak": c["weak"], "forced": c["forced"],
                         "wrong": c["wrong"], "not_audited": c["not_audited"],
                         "sound_pct": merge.pct(c["sound"], c["n"] - c["not_audited"])}
                     for k, c in sorted(t.items())}
    return fmt(und), fmt(dirc)


def main():
    data = json.loads((OUT / "all_link_audit.json").read_text(encoding="utf-8"))
    audit = {(l["a"], l["b"]): l for l in data["links"]}
    retags = {r["id"]: r for r in data["retags"]}
    part_b = {r["id"]: r for r in data.get("part_b", [])}
    flags = defaultdict(list)
    for f in read_jsonl(CORE / "sangam_text_flags.jsonl"):
        flags[f["id"]].append(f)
    texts = Texts()
    marked = sorted(b for b in set(bm.NEW) | set(bm.SANGAM) if (THEMES / b).is_dir() and any((THEMES / b).glob("ch*.json")))
    by_group = defaultdict(list)
    for b in marked:
        by_group[GROUP[b]].append(b)
    index, all_links = {}, []
    verse_ids, units = marked_units(marked, texts)
    for group in GROUP_NAMES:
        books = by_group.get(group, [])
        members = sorted(b for b, g in GROUP.items() if g == group)
        entry = {"name": GROUP_NAMES[group], "books": members, "built_here": books,
                 "kept_graphs": {b: f"kg/{b}/" for b in members if b in EXISTING},
                 "field_sets": sorted({field_set(b) for b in books})}
        if group == "grammar":
            entry["note"] = "The Tholkappiyam is the frame for marking: its nurpas are cited, not linked."
        if books:
            nodes, edges, links = build_group(group, books, texts, audit, retags, part_b, flags, verse_ids, units)
            all_links += links
            entry |= {"nodes": f"kg/groups/{group}/nodes.jsonl", "edges": f"kg/groups/{group}/edges.jsonl",
                      "audit": f"kg/groups/{group}/link_audit.json",
                      "node_counts": dict(Counter(n["type"] for n in nodes)),
                      "edge_counts": dict(Counter("LINK" if "teaches" in e else e["p"] for e in edges)),
                      "verses_by_book": dict(Counter(n["book"] for n in nodes if n["type"] == "Verse")),
                      "links": len(links), "links_by_grade": dict(Counter(l["audit"] for l in links))}
            print(f"{group}: {len(nodes)} nodes, {len(edges)} edges, {len(links)} links "
                  f"{dict(Counter(l['audit'] for l in links))}")
        index[group] = entry
    old = existing_links()
    every = all_links + old
    bridges = [{"s": l["s"], "o": l["o"], "type": l["p"].lower(), "grade": l["audit"],
                "group_a": l["group_a"], "group_b": l["group_b"], "book_a": book_of(l["s"]), "book_b": book_of(l["o"]),
                "graders": l.get("audit_graders"), "teaches_holds": l.get("audit_teaches_holds"),
                "marker_model": l.get("marker_model", "opus"), "source": l.get("source"),
                **({"s_unit": l["s_unit"]} if l.get("s_unit") else {}), **({"o_unit": l["o_unit"]} if l.get("o_unit") else {}),
                "note": l.get("note"), "teaches": l.get("teaches")}
               for l in every if l["group_a"] and l["group_b"] and not l["within_group"]]
    bridges.sort(key=lambda b: (b["group_a"], b["group_b"], b["s"], b["o"]))
    write_jsonl(OUT / "bridges.jsonl", bridges)
    und, dirc = pair_table(every)
    within = {g: und.get(f"{g}|{g}") for g in GROUP_NAMES if und.get(f"{g}|{g}")}
    summary = {
        "note": ("Sound% of graded links by group pair, the marked books' links and the five kept graphs' links "
                 "together. Within-group pairs (a|a) are the baseline a bridge has to beat. Unordered pairs count "
                 "links in both directions; directed pairs are proposer group|target group."),
        "groups": list(GROUP_NAMES), "pairs": und, "directed": dirc, "within": within,
        "bridges": {"links": len(bridges), "sound": sum(b["grade"] == "sound" for b in bridges),
                    "sound_pct": merge.pct(sum(b["grade"] == "sound" for b in bridges),
                                           sum(b["grade"] != "not_audited" for b in bridges))},
        "within_all": {"links": sum(l["within_group"] for l in every if l["group_a"]),
                       "sound_pct": merge.pct(sum(l["within_group"] and l["audit"] == "sound" for l in every if l["group_a"]),
                                              sum(l["within_group"] and l["audit"] != "not_audited" for l in every if l["group_a"]))}}
    (OUT / "bridges_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"bridges={len(bridges)} sound={summary['bridges']['sound']} ({summary['bridges']['sound_pct']}%); "
          f"within groups sound {summary['within_all']['sound_pct']}%; kept-graph links {len(old)}")


if __name__ == "__main__":
    main()
