#!/usr/bin/env python3
"""Build the knowledge graph: a catalog layer plus validated reading marks.

The catalog layer covers every row of the list of works. The marks layer comes
from kg/marks/pilot_source.json, and the build stops if a mark's text is not an
exact quote from the document it cites.

Writes:
  kg/nodes.jsonl  kg/edges.jsonl
  kg/marks/marks_review.csv  one row per mark, with blank columns for reviewers
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_DIR = ROOT / "data" / "catalog"
KG_DIR = ROOT / "kg"
MARKS_SOURCE = KG_DIR / "marks" / "pilot_source.json"


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def catalog_layer():
    nodes, edges = {}, []
    def node(node_id, node_type, label, **extra):
        nodes.setdefault(node_id, {"id": node_id, "type": node_type, "label": label,
                                   "layer": "catalog", **extra})
    def edge(subject, predicate, obj, confidence="stated"):
        edges.append({"s": subject, "p": predicate, "o": obj, "layer": "catalog",
                      "confidence": confidence, "status": "from_catalog"})

    documents = {d["id"]: d for d in read_jsonl(CATALOG_DIR / "documents.jsonl")}
    for work in read_jsonl(CATALOG_DIR / "works.jsonl"):
        work_id = f"row:{work['row']}"
        node(work_id, "CatalogWork", work["title"], work_no=work["work_no"])
        # Author strings stay separate from people until canonical_author() is decided.
        if work["author_canonical"]:
            author_id = f"author_string:{work['author_canonical']}"
            node(author_id, "AuthorString", work["author_canonical"])
            edge(work_id, "LISTED_AUTHOR", author_id)
        parent = None
        for depth in range(len(work["genre_path"])):
            genre_id = "genre:" + " / ".join(work["genre_path"][:depth + 1])
            node(genre_id, "Genre", work["genre_path"][depth])
            if parent:
                edge(genre_id, "SUBGENRE_OF", parent)
            parent = genre_id
        if parent:
            edge(work_id, "HAS_GENRE", parent)
        for key, confidence in (("text_ids", "stated"), ("pdf_ids", "stated"),
                                ("inferred_ids", "inferred")):
            for doc_id in work[key]:
                doc = documents[doc_id]
                node(f"doc:{doc_id}", "Document", doc_id, kind=doc["kind"], path=doc["raw_path"])
                edge(work_id, "HAS_FILE", f"doc:{doc_id}", confidence)
    return nodes, edges


def main():
    nodes, edges = catalog_layer()
    source = json.loads(MARKS_SOURCE.read_text(encoding="utf-8"))
    entity_ids = {entity["id"] for entity in source["entities"]}
    review_rows, errors = [], []
    texts = {}

    def locate(doc, quote, what):
        if doc not in texts:
            texts[doc] = (ROOT / "data" / "text" / f"{doc}.txt").read_text(encoding="utf-8")
        start = texts[doc].find(quote)
        if start < 0:
            errors.append(f"{what}: not found in {doc}: {quote}")
        return start

    for entity in source["entities"]:
        offsets = [{"doc": doc, "start": locate(doc, surface, entity["id"]), "text": surface}
                   for doc, surface in entity["mentions"]]
        nodes[entity["id"]] = {"id": entity["id"], "type": entity["type"], "label": entity["label"],
                               "aliases": entity.get("aliases", []), "layer": "marks",
                               "status": "proposed", "mentions": offsets}
        for mention in offsets:
            review_rows.append({"mark": "entity", "subject": entity["id"], "predicate": entity["type"],
                                "object_or_value": entity["label"], "doc": mention["doc"],
                                "offset": mention["start"], "quote": mention["text"]})
        if "catalog_doc" in entity:
            edges.append({"s": entity["id"], "p": "CATALOG_DOCUMENT",
                          "o": f"doc:utf8__{entity['catalog_doc']}", "layer": "marks",
                          "confidence": "stated", "status": "proposed"})

    for relation in source["relations"]:
        for side in ("s", "o"):
            if side in relation and relation[side] not in entity_ids:
                errors.append(f"unknown entity: {relation[side]}")
        start = locate(relation["doc"], relation["evidence"], f"{relation['s']} {relation['p']}")
        record = {"s": relation["s"], "p": relation["p"], "layer": "marks", "status": "proposed",
                  "assertion": relation.get("assertion", "stated_in_text"),
                  "doc": relation["doc"], "offset": start, "evidence": relation["evidence"]}
        for key in ("o", "value", "note"):
            if key in relation:
                record[key] = relation[key]
        edges.append(record)
        review_rows.append({"mark": "relation", "subject": relation["s"], "predicate": relation["p"],
                            "object_or_value": relation.get("o", relation.get("value")),
                            "doc": relation["doc"], "offset": start, "quote": relation["evidence"],
                            "assertion": record["assertion"], "note": relation.get("note", "")})

    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(f"{len(errors)} marks failed validation; nothing written")

    with open(KG_DIR / "nodes.jsonl", "w", encoding="utf-8") as out:
        for record in nodes.values():
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    with open(KG_DIR / "edges.jsonl", "w", encoding="utf-8") as out:
        for record in edges:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    fields = ["mark", "subject", "predicate", "object_or_value", "doc", "offset", "quote",
              "assertion", "note", "review_status", "review_notes"]
    with open(KG_DIR / "marks" / "marks_review.csv", "w", encoding="utf-8-sig", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=fields)
        writer.writeheader()
        writer.writerows(review_rows)

    layers = {}
    for record in list(nodes.values()):
        layers.setdefault(record["layer"], [0, 0])[0] += 1
    for record in edges:
        layers.setdefault(record["layer"], [0, 0])[1] += 1
    print({layer: {"nodes": counts[0], "edges": counts[1]} for layer, counts in layers.items()})


if __name__ == "__main__":
    main()
