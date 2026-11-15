#!/usr/bin/env python3
"""Export the Kural graph as viz/data.js, the data file the graph explorer page loads."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KURAL_DIR = ROOT / "kg" / "kural"
OUT = ROOT / "viz" / "data.js"


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def number(node_id):
    return int(node_id.split(":")[1])


def main():
    nodes = read_jsonl(KURAL_DIR / "nodes.jsonl")
    edges = read_jsonl(KURAL_DIR / "edges.jsonl")
    chapters = {n["number"]: {"title": n["title"], "section": n["section"], "theme": n["theme"]}
                for n in nodes if n["type"] == "Chapter"}
    concepts = {n["id"].split(":")[1]: {"tamil": n.get("tamil", ""), "gloss": n.get("gloss", "")}
                for n in nodes if n["type"] == "Concept"}
    verses = {}
    for n in nodes:
        if n["type"] == "Verse":
            verses[n["number"]] = {"t": n["tamil"], "p": n["pope"]["gloss"], "r": n["reading"],
                                   "n": n["nuance"], "x": int(n["contested"]),
                                   "u": int(n["uncertain"]), "f": int(n["text_needs_review"]),
                                   "c": [], "pos": []}
    links = []
    for e in edges:
        if e["p"] == "IN_CHAPTER":
            verses[number(e["s"])]["ch"] = number(e["o"])
        elif e["p"] == "EXPRESSES":
            verses[number(e["s"])]["c"].append(e["o"].split(":")[1])
        elif e["p"] == "READS":
            verses[number(e["o"])]["pos"].append([e["s"].split(":")[1], e["position"], e["quote"]])
        elif "note" in e:
            links.append({"a": number(e["s"]), "b": number(e["o"]), "type": e["p"].lower(),
                          "note": e["note"], "grade": e["audit"],
                          "better": e.get("audit_better_type")})
    threads = [{"id": t["id"], "title": t["title"], "claim": t["claim"],
                "grade": t["audit_grade"], "links": t["links"]}
               for t in json.loads((KURAL_DIR / "threads.json").read_text(encoding="utf-8"))]
    data = {"chapters": chapters, "concepts": concepts, "verses": verses,
            "links": links, "threads": threads}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("window.KG = " + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
                   + ";\n", encoding="utf-8")
    print(f"verses={len(verses)} concepts={len(concepts)} links={len(links)} "
          f"threads={len(threads)} bytes={OUT.stat().st_size}")


if __name__ == "__main__":
    main()
