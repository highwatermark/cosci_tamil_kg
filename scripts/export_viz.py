#!/usr/bin/env python3
"""Export the graphs of every built book as viz/data.js, the data file the explorer loads.

Verse ids are "k:N" for the Kural and "n:N" for the Naladiyar; chapter ids follow the same pattern.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "viz" / "data.js"
BOOKS = {"kural": ("k", ROOT / "kg" / "kural"), "naladiyar": ("n", ROOT / "kg" / "naladiyar")}


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def short(node_id):
    """kural:12 -> k:12, naladiyar:12 -> n:12, naladiyar-chapter:3 -> n:3, chapter:3 -> k:3."""
    kind, number = node_id.split(":")
    return {"kural": "k", "chapter": "k", "naladiyar": "n", "naladiyar-chapter": "n"}[kind] + ":" + number


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
        if book == "kural":
            for t in json.loads((folder / "threads.json").read_text(encoding="utf-8")):
                threads.append({"id": t["id"], "title": t["title"], "claim": t["claim"],
                                "grade": t["audit_grade"], "links": [[f"k:{a}", f"k:{b}"] for a, b in t["links"]],
                                "limits": t.get("limits", ""), "issue": t.get("audit_issue", "")})
    concepts.update({c["id"]: {"tamil": c["tamil"], "gloss": c["gloss"]}
                     for c in json.loads((ROOT / "kg" / "themes" / "concepts.json").read_text(encoding="utf-8"))})
    data = {"chapters": chapters, "concepts": concepts, "verses": verses, "links": links, "threads": threads}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("window.KG = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
                   encoding="utf-8")
    by_book = {b: sum(v["book"] == b for v in verses.values()) for b in BOOKS}
    print(f"verses={by_book} concepts={len(concepts)} links={len(links)} threads={len(threads)} "
          f"bytes={OUT.stat().st_size}")


if __name__ == "__main__":
    main()
