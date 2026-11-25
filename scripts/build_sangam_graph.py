#!/usr/bin/env python3
"""Build the Sangam core graph (Akananuru, Purananuru, Pattupattu) from its chapter marks and link audit.

Writes kg/sangam_core/nodes.jsonl and kg/sangam_core/edges.jsonl, after scripts/build_siddhar_graph.py.
Run scripts/merge_sangam_grades.py first: it writes kg/sangam_core/link_audit.json, which this reads.

Nodes
- Verse: akananuru:N, purananuru:N, and the Pattupattu reading units pattupattu:<idyll>:<start>-<end>
  (as marked, so adjusted units keep their new spans). Each carries the Tamil (public domain), the
  core file's poet and patron, the colophon's thinai and thurai beside our own inferred thinai, and
  the marks: reading, nuance, uncertain, akam_puram, thinai_evidence, mixed, uri, mutal, meyppadu,
  thurai_akam (speaker, addressee), puram_thurai, comparisons, and the ullurai and iraicchi objects
  with the status the blind re-tags gave them.
- Chapter: akananuru-chapter:N, purananuru-chapter:N, pattupattu-chapter:N (book_marks.py's numbers).
- Karu: karu:<stem>, one per native thing (kinds, senses and verse count gathered from every mention).
- Entity: entity:<type>:<name>, a king, patron, battle, town, river, hill or hero-stone as the poem
  writes it (names are not lemmatised, so one king may have several nodes).

Edges
- IN_CHAPTER; EXPRESSES (verse -> concept, ranked); NAMES (verse -> karu node, with form, line, kind,
  role, land, sense; verse -> entity node, with type and line).
- ULLURAI and IRAICCHI (verse -> karu node of the vehicle or carrier), experimental, with status:
  confirmed (a blind grader re-tagged the poem and found the device too), not_confirmed (the graders
  who re-tagged it did not), not_retagged (no grader saw the poem).
- Links (TENSION, AGREES, DEVELOPS, QUALIFIES, SAME_IMAGE, PARALLEL_DOMAIN) with note, teaches, the
  audit grade (strictest blind grade), cross_book and the two corpus groups (docs/corpus-groups.md).
  A link to a Pattupattu line span is kept as written and resolved to the marked unit it overlaps
  most (`o_unit`), when its idyll is marked.
"""
import importlib.util
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES = ROOT / "kg" / "themes"
CORE = ROOT / "kg" / "core"
OUT_DIR = ROOT / "kg" / "sangam_core"
BOOKS = ("akananuru", "purananuru", "pattupattu")
PATTU_ID = re.compile(r"pattupattu:(\d+):(\d+)-(\d+)")
# docs/corpus-groups.md (as in scripts/make_sangam_packets.py)
GROUP = {"akananuru": "ettuthogai_akam", "natrinai": "ettuthogai_akam", "kuruntokai": "ettuthogai_akam",
         "ainkurunuru": "ettuthogai_akam", "kalittokai": "ettuthogai_akam",
         "purananuru": "ettuthogai_puram", "patitruppattu": "ettuthogai_puram",
         "paripadal": "ettuthogai_devotional", "pattupattu": "pattupattu",
         "kural": "ethics", "naladiyar": "ethics",
         "tirumanthiram": "devotional", "thiruppugazh": "devotional", "siddhar": "devotional"}
# Flags in kg/core/sangam_text_flags.jsonl that mean the text itself should be checked (repairs and
# formulaic repeated lines are already settled).
REVIEW_FLAGS = {"misprint_candidate", "edition_variant", "line_count", "lineation", "spelling",
                "colophon", "colophon_variant", "thinai"}

spec = importlib.util.spec_from_file_location("book_marks", ROOT / "scripts" / "book_marks.py")
bm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bm)


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")


def ref(book, target):
    return target if isinstance(target, str) and ":" in target else f"{book}:{target}"


def book_of(node_id):
    return node_id.split(":")[0]


def main():
    audit = json.loads((OUT_DIR / "link_audit.json").read_text(encoding="utf-8"))
    grades = {(g["a"], g["b"]): g for g in audit["links"]}
    retags = {r["id"]: r for r in audit["retags"]}
    flags = defaultdict(list)
    for f in read_jsonl(CORE / "sangam_text_flags.jsonl"):
        if f["book"] in BOOKS:
            flags[f["id"]].append(f)
    poems = {b: {r["id"]: r for r in read_jsonl(CORE / f"{b}.jsonl")} for b in ("akananuru", "purananuru")}
    idylls = {p["number"]: p for p in read_jsonl(CORE / "pattupattu.jsonl")}

    nodes, edges = [], []
    karu_nodes, entity_nodes = {}, {}
    units = defaultdict(list)          # idyll -> [(start, end, id)] of the marked units
    pending_links = []
    for book in BOOKS:
        _, chapters = bm.load_sangam(book)
        for path in sorted((THEMES / book).glob("ch*.json")):
            chapter = json.loads(path.read_text(encoding="utf-8"))
            number = chapter["chapter_no"]
            ch = chapters[number]
            chapter_id = f"{book}-chapter:{number}"
            nodes.append({"id": chapter_id, "type": "Chapter", "book": book, "number": number,
                          "title": ch["title"], "section": ch["title"] if book == "pattupattu" else ch["title"].rsplit(" ", 1)[0],
                          "theme": chapter["chapter_theme"], "status": "proposed",
                          "structure_note": chapter.get("structure_note", ""),
                          "source_issues": chapter.get("source_issues", [])})
            for key, mark in chapter["verses"].items():
                verse_id = ref(book, key)
                if book == "pattupattu":
                    idyll, start, end = (int(g) for g in PATTU_ID.fullmatch(verse_id).groups())
                    rec = idylls[idyll]
                    tamil = rec["tamil"][start - 1:end]
                    units[idyll].append((start, end, verse_id))
                    fl = [f for f in flags.get(rec["id"], []) if f.get("line") and start <= f["line"] <= end]
                    extra = {"number": start, "idyll": idyll, "idyll_title": rec["title"], "idyll_name": rec["short_name"].replace("_", " ").title(), "start": start, "end": end,
                             "unit_note": mark.get("unit_note")}
                else:
                    rec = poems[book][verse_id]
                    tamil = rec["tamil"]
                    fl = flags.get(verse_id, [])
                    extra = {"number": int(rec["number"]), "section": rec.get("section"), "title": rec.get("title")}
                review = sorted({f["kind"] for f in fl if f["kind"] in REVIEW_FLAGS})
                rt = retags.get(verse_id)
                devices = {}
                for field in ("ullurai", "iraicchi"):
                    obj = mark.get(field)
                    if obj:
                        status = rt[f"{field}_status"] if rt else "not_retagged"
                        devices[field] = obj | {"status": status,
                                                "graders_agree": rt[f"{field}_graders_agree"] if rt else None}
                    else:
                        devices[field] = None
                grader_only = [f for f in ("ullurai", "iraicchi") if rt and rt[f"{f}_status"] == "grader_only"]
                node = {"id": verse_id, "type": "Verse", "book": book, **extra,
                        "poet": rec.get("poet"), "patron": rec.get("patron"),
                        "tamil": tamil, "pope": "",
                        "reading": mark["reading"], "nuance": mark.get("nuance", ""),
                        "contested": False, "uncertain": bool(mark.get("uncertain")),
                        "text_needs_review": bool(review), "text_flags": review,
                        "akam_puram": mark["akam_puram"],
                        "colophon": mark["colophon"], "thinai": mark["thinai"],
                        "thinai_differs": None, "thinai_evidence": mark.get("thinai_evidence"),
                        "mixed": mark.get("mixed", False), "uri": mark.get("uri"), "mutal": mark.get("mutal"),
                        "meyppadu": mark.get("meyppadu", []),
                        "thurai_akam": mark.get("thurai_akam", []), "puram_thurai": mark.get("puram_thurai", []),
                        "comparisons": mark.get("comparisons", []),
                        "ullurai": devices["ullurai"], "iraicchi": devices["iraicchi"],
                        "devices_grader_only": grader_only, "status": "proposed"}
                node["thinai_differs"] = colophon_differs(mark["thinai"], mark["colophon"].get("thinai"))
                nodes.append(node)
                edges.append({"s": verse_id, "p": "IN_CHAPTER", "o": chapter_id})
                for rank, concept in enumerate(mark["concepts"], 1):
                    edges.append({"s": verse_id, "p": "EXPRESSES", "o": f"concept:{concept}", "rank": rank,
                                  "basis": "interpretation", "status": "proposed"})
                stem_of_form = {}
                for k in mark.get("karu", []):
                    stem = (k.get("stem") or k["form"]).strip()
                    kid = f"karu:{stem}"
                    kn = karu_nodes.setdefault(kid, {"id": kid, "type": "Karu", "stem": stem, "kinds": Counter(),
                                                     "senses": Counter(), "roles": Counter(), "verses": set()})
                    kn["kinds"][k["kind"]] += 1
                    kn["roles"][k["role"]] += 1
                    if k.get("sense"):
                        kn["senses"][k["sense"]] += 1
                    kn["verses"].add(verse_id)
                    stem_of_form[(k["form"], k.get("line"))] = kid
                    edges.append({"s": verse_id, "p": "NAMES", "o": kid, "form": k["form"], "line": k.get("line"),
                                  "kind": k["kind"], "role": k["role"], "land": k.get("land"),
                                  "sense": k.get("sense"), "basis": "interpretation", "status": "proposed"})
                for e in mark.get("entities", []):
                    eid = f"entity:{e['type']}:{e['name'].strip()}"
                    en = entity_nodes.setdefault(eid, {"id": eid, "type": "Entity", "kind": e["type"],
                                                       "name": e["name"].strip(), "verses": set()})
                    en["verses"].add(verse_id)
                    edges.append({"s": verse_id, "p": "NAMES", "o": eid, "entity_type": e["type"],
                                  "line": e.get("line"), "basis": "text", "status": "proposed"})
                for field, role, thing in (("ullurai", "ullurai", "vehicle"), ("iraicchi", "iraicchi", "carrier")):
                    obj = devices[field]
                    if not obj:
                        continue
                    things = obj.get(thing)
                    things = things if isinstance(things, list) else [things]
                    targets = []
                    for t in things:
                        if not isinstance(t, dict):
                            continue
                        kid = stem_of_form.get((t.get("form"), t.get("line")))
                        if kid is None:  # match by form only, then by role
                            kid = next((v for (f, _), v in stem_of_form.items() if f == t.get("form")), None)
                        if kid is None:
                            kid = next((f"karu:{(k.get('stem') or k['form']).strip()}" for k in mark["karu"]
                                        if k["role"] == role), f"karu:{t.get('form')}")
                        targets.append((kid, t))
                    for kid, t in dict((k, t) for k, t in targets).items():
                        edge = {"s": verse_id, "p": field.upper(), "o": kid, "form": t.get("form"), "line": t.get("line"),
                                "experimental": True, "status": obj["status"], "graders_agree": obj["graders_agree"],
                                "basis": "interpretation"}
                        if field == "ullurai":
                            edge.update({"tenor": obj.get("tenor"), "pairs": len(obj.get("pairs") or []),
                                         "anchor": obj.get("anchor")})
                        else:
                            edge.update({"act": obj.get("act"), "sense": obj.get("sense"),
                                         "deletion_test": obj.get("deletion_test")})
                        edges.append(edge)
            for link in chapter.get("links", []):
                pending_links.append((book, number, link))

    def unit_for(target):
        m = PATTU_ID.fullmatch(target)
        if not m:
            return None
        idyll, start, end = (int(g) for g in m.groups())
        best = max(((min(end, z) - max(start, a) + 1, uid) for a, z, uid in units.get(idyll, [])), default=None)
        return best[1] if best and best[0] > 0 else None

    for book, number, link in pending_links:
        s, o = ref(book, link["a"]), ref(book, link["b"])
        grade = grades.get((s, o), {})
        ga, gb = GROUP.get(book_of(s)), GROUP.get(book_of(o))
        edge = {"s": s, "p": link["type"].upper(), "o": o, "note": link["note"], "teaches": link.get("teaches"),
                "basis": "interpretation", "status": "proposed", "pass": "marking",
                "audit": grade.get("grade", "not_audited"), "audit_graders": grade.get("graders", 0),
                "source": "sangam_marks", "chapter": f"{book}-chapter:{number}",
                "cross_book": book_of(o) != book_of(s), "group_a": ga, "group_b": gb, "within_group": ga == gb}
        for k in ("s", "o"):
            u = unit_for(edge[k])
            if u and u != edge[k]:
                edge[f"{k}_unit"] = u
        if grade:
            edge["audit_teaches_holds"] = grade.get("teaches_holds")
            if grade.get("better_type"):
                edge["audit_better_type"] = grade["better_type"]
            if grade.get("text_issue"):
                edge["audit_text_issue"] = grade["text_issue"]
        edges.append(edge)

    for kn in karu_nodes.values():
        kn["kind"] = kn["kinds"].most_common(1)[0][0]
        kn["kinds"], kn["roles"], kn["senses"] = dict(kn["kinds"]), dict(kn["roles"]), dict(kn["senses"])
        kn["verses"] = len(kn["verses"])
    for en in entity_nodes.values():
        en["verses"] = len(en["verses"])
    nodes += sorted(karu_nodes.values(), key=lambda n: n["id"]) + sorted(entity_nodes.values(), key=lambda n: n["id"])
    OUT_DIR.mkdir(exist_ok=True)
    write_jsonl(OUT_DIR / "nodes.jsonl", nodes)
    write_jsonl(OUT_DIR / "edges.jsonl", edges)
    links = [e for e in edges if "note" in e]
    print(f"nodes={len(nodes)} " + " ".join(f"{t}={n}" for t, n in Counter(n['type'] for n in nodes).items())
          + f" edges={len(edges)} " + " ".join(f"{p}={n}" for p, n in Counter(
              e['p'] if 'note' not in e else 'LINK' for e in edges).items())
          + f" links: {dict(Counter(e['audit'] for e in links))} cross_book={sum(e['cross_book'] for e in links)}")


# The colophon's thinai is Tamil (குறிஞ்சி, பாடாண்திணை, ...); ours is romanized. Compare on the stem.
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


if __name__ == "__main__":
    main()
