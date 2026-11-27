"""Print coverage, a grade-blind Tamil packet, or its scored blind decisions."""
import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
KG = HERE.parents[2] / "kg"
BOOKS = ("kural", "naladiyar", "tirumanthiram", "thiruppugazh")
TARGETS = BOOKS[2:]
SEED = "tamil-links-audit-v1"
GRADES = ("sound", "weak", "forced", "wrong")
QUOTA = (3, 2, 1, 1)


def rows(path):
    with path.open() as stream:
        return [json.loads(line) for line in stream]


def load():
    edges = []
    tamil = {}
    for book in BOOKS:
        edges.extend((book, e) for e in rows(KG / book / "edges.jsonl") if "audit" in e)
        for r in rows(KG / "core" / (book + ".jsonl")):
            if r["tamil"]:
                tamil[f"{book}:{r.get('number', r.get('verse'))}"] = r["tamil"]
    return edges, tamil


def key(item):
    book, e = item
    identity = [SEED, book, e["s"], e["p"], e["o"], e["note"]]
    return hashlib.sha256(json.dumps(identity, ensure_ascii=False).encode()).hexdigest()


def sample(edges):
    selected = []
    for b in TARGETS:
        for grade, k in zip(GRADES, QUOTA):
            group = sorted((x for x in edges if x[0] == b and x[1]["audit"] == grade), key=key)
            selected.extend(group[:k])
    return sorted(selected, key=key)


def coverage(edges, tamil):
    report = {}
    for b in TARGETS:
        ids = [v for v in tamil if v.split(":")[0] == b]
        owned = [e for book, e in edges if book == b]
        incident = [e for _, e in edges if b in (e["s"].split(":")[0], e["o"].split(":")[0])]
        report[b] = {"readable": len(ids), "file_grades": Counter(e["audit"] for e in owned)}
        for label, records in (("own_file", owned), ("all_four_files", incident)):
            neighbors = defaultdict(set)
            cross = defaultdict(set)
            touched = set()
            for e in records:
                a, z = e["s"], e["o"]
                touched.update([a, z])
                if e["audit"] == "sound" and a != z:
                    neighbors[a].add(z)
                    neighbors[z].add(a)
                    if a.split(":")[0] != z.split(":")[0]:
                        cross[a].add(z)
                        cross[z].add(a)
            report[b][label] = {
                "graded_records": len(records),
                "with_any_graded_link": sum(v in touched for v in ids),
                "sound_degree_histogram": dict(sorted(Counter(len(neighbors[v]) for v in ids).items())),
                "verses_with_any_sound_neighbor": sum(bool(neighbors[v]) for v in ids),
                "verses_with_cross_book_sound_neighbor": sum(bool(cross[v]) for v in ids),
                "zero_sound_ids": [v for v in ids if not neighbors[v]],
            }
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("coverage", "packet", "score"))
    mode = parser.parse_args().mode
    edges, tamil = load()
    items = sample(edges)
    if mode == "coverage":
        out = coverage(edges, tamil)
    elif mode == "packet":
        out = [{"item": key(x)[:12], "a": e["s"], "a_tamil": tamil[e["s"]], "b": e["o"],
                "b_tamil": tamil[e["o"]], "type": e["p"], "claim": e["note"]}
               for x in items for e in [x[1]]]
    else:
        decisions = json.loads((HERE / "decisions.json").read_text())
        assert set(decisions) == {key(x)[:12] for x in items}
        out = []
        for x in items:
            b, e = x
            item = key(x)[:12]
            pred, reason = decisions[item]
            assert pred in GRADES
            out.append(dict(item=item, book=b, a=e["s"], b=e["o"], relation=e["p"],
                            previous=e["audit"], regrade=pred, reason=reason))
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
