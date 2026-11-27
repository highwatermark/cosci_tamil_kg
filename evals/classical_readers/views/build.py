"""Export directed graded verse graphs, preserving isolated verses and competing records."""
import argparse
import csv
import gzip
import json
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
KG = HERE.parents[2] / "kg"
BOOKS = ("kural", "naladiyar", "siddhar", "thiruppugazh", "tirumanthiram")
GRADES = ("sound", "weak", "forced", "wrong")
VIEWS = {
    "five_books": BOOKS,
    "siddhar": ("siddhar",),
    "devotional": ("thiruppugazh",),
    "siddhar_with_tirumanthiram": ("siddhar", "tirumanthiram"),
    "devotional_with_tirumanthiram": ("thiruppugazh", "tirumanthiram"),
}


def rows(path):
    with path.open(encoding="utf-8") as f:
        yield from map(json.loads, f)


def load(books):
    nodes = {}
    edges = []
    for book in books:
        for n in rows(KG / book / "nodes.jsonl"):
            if n["type"] == "Verse":
                nodes[n["id"]] = {"book": book, "work": n.get("work", ""),
                                  "poet": n.get("siddhar", ""), "unit_id": n.get("unit_id", n["id"])}
        for i, e in enumerate(rows(KG / book / "edges.jsonl"), 1):
            if e.get("audit") in GRADES:
                edges.append({**e, "source_record": f"kg/{book}/edges.jsonl:{i}"})
    for e in edges:
        if e["s"] not in nodes or e["o"] not in nodes:
            raise ValueError(f"Missing endpoint: {e['source_record']}")
    return nodes, edges


def summarize(label, focus, edges):
    grades = Counter(e["audit"] for e in edges)
    pairs = defaultdict(set)
    touched = set()
    for e in edges:
        pair = tuple(sorted((e["s"], e["o"])))
        pairs[pair].add(e["audit"])
        if e["audit"] == "sound" and pair[0] != pair[1]:
            touched.update(pair)
    return dict(cohort=label, records=len(edges), **{g: grades[g] for g in GRADES},
                sound_pct=round(100 * grades["sound"] / len(edges), 1) if edges else "",
                pairs=len(pairs), pairs_with_sound=sum("sound" in p for p in pairs.values()),
                pairs_with_multiple_grades=sum(len(p) > 1 for p in pairs.values()),
                eligible_verses=len(focus), verses_with_sound=len(touched & focus))


def graph(path, members, edges, nodes):
    root = ET.Element("graphml", xmlns="http://graphml.graphdrawing.org/xmlns")
    attributes = {"node": ("book", "poet", "work", "unit_id"),
                  "edge": ("p", "audit", "source_record")}
    for scope, fields in attributes.items():
        for field in fields:
            ET.SubElement(root, "key", id=field, **{"for": scope, "attr.name": field, "attr.type": "string"})
    g = ET.SubElement(root, "graph", edgedefault="directed")
    def attach(element, values, fields):
        for field in fields:
            if values.get(field):
                ET.SubElement(element, "data", key=field).text = values[field]
    for n in sorted(members):
        attach(ET.SubElement(g, "node", id=n), nodes[n], attributes["node"])
    for i, e in enumerate(edges):
        element = ET.SubElement(g, "edge", id=f"e{i}", source=e["s"], target=e["o"])
        attach(element, e, attributes["edge"])
    path.write_bytes(gzip.compress(ET.tostring(root, encoding="utf-8", xml_declaration=True), mtime=0))


def run(out, views):
    catalog = sorted({b for books in views.values() for b in books})
    nodes, records = load(catalog)
    out.mkdir(parents=True, exist_ok=True)
    report = []
    for name, books in views.items():
        members = {k for k, meta in nodes.items() if meta["book"] in books}
        within, boundary = [], []
        for e in records:
            a, b = e["s"] in members, e["o"] in members
            if a and b:
                within.append(e)
            elif a or b:
                boundary.append(e)
        graph(out / (name + ".graphml.gz"), members, within, nodes)
        report.append(summarize(name + "/within", members, within))
        if set(books) != set(catalog):
            report.append(summarize(name + "/boundary", members, boundary))
    # Attribute labels in the corpus carry uncertainty and may name a tradition.
    sid = {k for k, n in nodes.items() if n["book"] == "siddhar"}
    a_by_poet = defaultdict(list)
    by_book_pair = defaultdict(list)
    for e in records:
        a, b = nodes[e["s"]], nodes[e["o"]]
        by_book_pair[tuple(sorted((a["book"], b["book"])))].append(e)
        if a["book"] == b["book"] == "siddhar":
            k = "same_poet" if a["poet"] == b["poet"] else "different_poets"
            if not (a["poet"] and b["poet"]):
                k = "unknown_poet"
            a_by_poet[k].append(e)
    for key, group in sorted(a_by_poet.items()):
        report.append(summarize("siddhar/" + key, sid, group))
    for books, group in sorted(by_book_pair.items()):
        members = {k for k, meta in nodes.items() if meta["book"] in books}
        report.append(summarize(" + ".join(books), members, group))
    with (out / "coverage.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=report[0])
        w.writeheader()
        w.writerows(report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE)
    parser.add_argument("--view", action="append", default=[], metavar="NAME=BOOK[,BOOK...]",
                        help="Include an additional view of explicitly named built books")
    args = parser.parse_args()
    views = dict(VIEWS)
    for spec in args.view:
        name, sep, book_list = spec.partition("=")
        books = book_list.split(",")
        if not sep or not name.isidentifier() or name in views or not all(b.isidentifier() for b in books):
            parser.error("Give a unique identifier and comma-separated built book identifiers")
        for book in books:
            if not all((KG / book / p).is_file() for p in ("nodes.jsonl", "edges.jsonl")):
                parser.error(f"{book} lacks a built node or edge file")
        views[name] = books
    run(args.out, views)
