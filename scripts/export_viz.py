#!/usr/bin/env python3
"""Export the graphs of every built book as viz/data.js, the data file the explorer loads.

Verse ids are "k:N" for the Kural, "n:N" for the Naladiyar, "t:N" for the Tirumanthiram and
"p:N" for the Thiruppugazh and "s:N" for the Siddhar songs (N is the unit's seq); chapter ids
follow the same pattern.

The Sangam books (kg/sangam_core, built by scripts/build_sangam_graph.py) go in a separate file,
viz/data_sangam.js (window.KG_SANGAM, merged into window.KG by viz/index.html), since data.js is close
to the 16 MB page limit. Their ids are "a:N" for the Akananuru, "pn:N" for the Purananuru ("p" is the
Thiruppugazh's) and "pp:<idyll>:<start>-<end>" for Pattupattu reading units; chapter ids are "a:N",
"pn:N" and "pp:N". Sangam verses carry the Tholkappiyam frame: thinai (ours and the colophon's),
speaker, karu, entities, meyppadu and the ullurai/iraicchi devices with their re-tag status.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "viz" / "data.js"
OUT_SANGAM = ROOT / "viz" / "data_sangam.js"
SANGAM_DIR = ROOT / "kg" / "sangam_core"
SANGAM_PREFIX = {"akananuru": "a", "purananuru": "pn", "pattupattu": "pp"}
OTHER_PREFIX = {"kural": "k", "naladiyar": "n", "tirumanthiram": "t", "thiruppugazh": "p", "siddhar": "s"}
LIMIT = 16 * 1024 * 1024
BOOKS = {"kural": ("k", ROOT / "kg" / "kural"), "naladiyar": ("n", ROOT / "kg" / "naladiyar"),
         "tirumanthiram": ("t", ROOT / "kg" / "tirumanthiram"), "thiruppugazh": ("p", ROOT / "kg" / "thiruppugazh"),
         "siddhar": ("s", ROOT / "kg" / "siddhar")}


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def short(node_id):
    """kural:12 -> k:12, naladiyar:12 -> n:12, naladiyar-chapter:3 -> n:3, chapter:3 -> k:3, tirumanthiram:5 -> t:5."""
    kind, number = node_id.split(":")
    return {"kural": "k", "chapter": "k", "naladiyar": "n", "naladiyar-chapter": "n",
            "tirumanthiram": "t", "tirumanthiram-chapter": "t", "thiruppugazh": "p", "thiruppugazh-chapter": "p",
            "siddhar": "s", "siddhar-chapter": "s"}[kind] + ":" + number


def main():
    chapters, concepts, verses, links, threads = {}, {}, {}, [], []
    for book, (prefix, folder) in BOOKS.items():
        nodes = read_jsonl(folder / "nodes.jsonl")
        edges = read_jsonl(folder / "edges.jsonl")
        for n in nodes:
            if n["type"] == "Chapter":
                chapters[f"{prefix}:{n['number']}"] = {"book": book, "num": n["number"], "title": n["title"],
                                                       "section": n["section"], "theme": n["theme"]}
            elif n["type"] == "Concept":
                concepts[n["id"].split(":")[1]] = {"tamil": n.get("tamil", ""), "gloss": n.get("gloss", "")}
            elif n["type"] == "Verse":
                pope = n["pope"]["gloss"] if isinstance(n["pope"], dict) else n["pope"]
                verses[f"{prefix}:{n['number']}"] = {
                    "book": book, "num": n["number"], "t": n["tamil"], "p": pope, "r": n["reading"],
                    "n": n["nuance"], "x": int(n["contested"]), "u": int(n["uncertain"]),
                    "f": int(n.get("text_needs_review", False)), "c": [], "pos": []}
                if book == "siddhar":
                    verses[f"{prefix}:{n['number']}"]["who"] = n["siddhar"]
        for e in edges:
            if e["p"] == "IN_CHAPTER":
                verses[short(e["s"])]["ch"] = short(e["o"])
            elif e["p"] == "EXPRESSES":
                verses[short(e["s"])]["c"].append(e["o"].split(":")[1])
            elif e["p"] == "READS":
                verses[short(e["o"])]["pos"].append([e["s"].split(":")[1], e["position"], e["quote"]])
            elif "note" in e:
                links.append({"a": short(e["s"]), "b": short(e["o"]), "type": e["p"].lower(),
                              "note": e["note"], "grade": e["audit"],
                              "better": e.get("audit_better_type")})
        # Kural threads cite bare verse numbers; other books' threads cite full ids such as naladiyar:6.
        if (folder / "threads.json").exists():
            for t in json.loads((folder / "threads.json").read_text(encoding="utf-8")):
                pairs = [[short(x) if isinstance(x, str) else f"{prefix}:{x}" for x in pair] for pair in t["links"]]
                books = sorted({{"k": "Kural", "n": "Naladiyar", "t": "Tirumanthiram", "p": "Thiruppugazh", "s": "Siddhars"}[x[0]] for pair in pairs for x in pair},
                               key=["Kural", "Naladiyar", "Tirumanthiram", "Thiruppugazh", "Siddhars"].index)
                threads.append({"id": t["id"], "title": t["title"], "claim": t["claim"],
                                "grade": t["audit_grade"], "links": pairs, "books": books,
                                "limits": t.get("limits", ""), "issue": t.get("audit_issue", "")})
    threads.sort(key=lambda t: len(t["books"]) == 1)  # threads across books first; sort is stable
    concepts.update({c["id"]: {"tamil": c["tamil"], "gloss": c["gloss"]}
                     for c in json.loads((ROOT / "kg" / "themes" / "concepts.json").read_text(encoding="utf-8"))})
    data = {"chapters": chapters, "concepts": concepts, "verses": verses, "links": links, "threads": threads}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("window.KG = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
                   encoding="utf-8")
    by_book = {b: sum(v["book"] == b for v in verses.values()) for b in BOOKS}
    print(f"verses={by_book} concepts={len(concepts)} links={len(links)} threads={len(threads)} "
          f"bytes={OUT.stat().st_size}")
    if (SANGAM_DIR / "nodes.jsonl").exists():
        export_sangam(set(verses))
    for f in (OUT, OUT_SANGAM):
        if f.exists() and f.stat().st_size > LIMIT:
            raise SystemExit(f"{f} is {f.stat().st_size} bytes, over the {LIMIT}-byte page limit")


def sangam_short(node_id):
    """akananuru:12 -> a:12, purananuru:3 -> pn:3, pattupattu:1:1-11 -> pp:1:1-11, kural:5 -> k:5;
    chapters akananuru-chapter:2 -> a:2."""
    book, rest = node_id.split(":", 1)
    if book.endswith("-chapter"):
        return SANGAM_PREFIX[book[:-len("-chapter")]] + ":" + rest
    return (SANGAM_PREFIX.get(book) or OTHER_PREFIX[book]) + ":" + rest


def export_sangam(other_verses):
    nodes = read_jsonl(SANGAM_DIR / "nodes.jsonl")
    edges = read_jsonl(SANGAM_DIR / "edges.jsonl")
    chapters, verses, links, dropped = {}, {}, [], []
    for n in nodes:
        if n["type"] == "Chapter":
            chapters[sangam_short(n["id"])] = {"book": n["book"], "num": n["number"], "title": n["title"],
                                               "section": n["section"], "theme": n["theme"]}
        elif n["type"] == "Verse":
            col = n.get("colophon") or {}
            v = {"book": n["book"], "num": n["number"], "t": n["tamil"], "p": "", "r": n["reading"],
                 "n": n["nuance"], "x": 0, "u": int(n["uncertain"]), "f": int(n["text_needs_review"]),
                 "c": [], "pos": [], "poet": n.get("poet") or "", "pat": n.get("patron") or "",
                 "ap": n["akam_puram"], "th": n["thinai"], "cth": col.get("thinai") or "",
                 "ctu": col.get("thurai") or "", "thd": int(bool(n.get("thinai_differs"))),
                 "uri": n.get("uri") or "", "mx": int(bool(n.get("mixed"))),
                 "sp": [[a.get("speaker"), a.get("addressee"), a.get("overhearer"),
                         (a.get("occasion") or {}).get("stage"), (a.get("occasion") or {}).get("words")]
                        for a in n.get("thurai_akam") or []],
                 "pt": [x["name"] for x in n.get("puram_thurai") or []],
                 "mp": [[m["feeling"], m["cause"]] for m in n.get("meyppadu") or []],
                 "k": [], "en": [], "dv": []}
            if n["book"] == "pattupattu":
                v["nm"] = f"{n['idyll_name']} {n['start']}-{n['end']}"
                v["lb"] = f"PP{n['idyll']}:{n['start']}-{n['end']}"
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
            verses[sangam_short(n["id"])] = v
    for e in edges:
        s = sangam_short(e.get("s_unit") or e["s"])
        if e["p"] == "IN_CHAPTER":
            verses[s]["ch"] = sangam_short(e["o"])
        elif e["p"] == "EXPRESSES":
            verses[s]["c"].append(e["o"].split(":")[1])
        elif e["p"] == "NAMES" and e["o"].startswith("karu:"):
            verses[s]["k"].append([e["form"], e["o"][5:], e.get("line"), e["kind"], e["role"], e.get("sense") or ""])
        elif e["p"] == "NAMES":
            verses[s]["en"].append([e["entity_type"], e["o"].split(":", 2)[2], e.get("line")])
        elif "note" in e:
            o = sangam_short(e.get("o_unit") or e["o"])
            if o not in verses and o not in other_verses:
                dropped.append(e["o"])
                continue
            links.append({"a": s, "b": o, "type": e["p"].lower(), "note": e["note"], "grade": e["audit"],
                          "better": e.get("audit_better_type"), "te": e.get("teaches") or ""})
    data = {"chapters": chapters, "verses": verses, "links": links}
    OUT_SANGAM.write_text("window.KG_SANGAM = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
                          encoding="utf-8")
    by_book = {b: sum(v["book"] == b for v in verses.values()) for b in SANGAM_PREFIX}
    print(f"sangam verses={by_book} chapters={len(chapters)} links={len(links)} "
          f"dropped={len(dropped)} ({', '.join(sorted(set(dropped)))}) bytes={OUT_SANGAM.stat().st_size}")


if __name__ == "__main__":
    main()
