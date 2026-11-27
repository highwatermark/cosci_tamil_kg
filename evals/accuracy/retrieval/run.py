"""Compare two candidate searches against hidden, previously sound-graded pairs."""
import csv
import json
import math
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
KG = HERE.parents[2] / "kg"
BOOKS = ("kural", "naladiyar", "tirumanthiram", "thiruppugazh")
TARGET = BOOKS[-2:]
SEED = 20261124


def records(path):
    with path.open() as f:
        yield from map(json.loads, f)


def terms(node):
    # Tamil letter trigrams tolerate some inflection and word joining.
    tamil = set()
    for word in re.findall(r"[\u0b80-\u0bff]+", " ".join(node["tamil"])):
        tamil.update(word[i:i+3] for i in range(len(word)-2))
    reading = set(re.findall(r"[a-z]{3,}", (node.get("reading") or "").lower()))
    return tamil, reading


def indexed_cosine(features):
    postings = defaultdict(list)
    norms = {}
    for label, tokens in features.items():
        for t in tokens:
            postings[t].append(label)
    weights = {t: math.log((len(features)+1)/(len(ids)+1))**2 for t, ids in postings.items()}
    for label, tokens in features.items():
        norms[label] = math.sqrt(sum(weights[t] for t in sorted(tokens))) or 1
    def query(label):
        dots = Counter()
        for t in sorted(features[label]):
            for other in postings[t]:
                dots[other] += weights[t]
        return {other: dot/(norms[other]*norms[label]) for other, dot in dots.items()}
    return query


def main():
    nodes, concepts = {}, defaultdict(set)
    positive = defaultdict(set)
    incoming = set()
    for book in BOOKS:
        for n in records(KG / book / "nodes.jsonl"):
            if n["type"] == "Verse":
                nodes[n["id"]] = n
        for e in records(KG / book / "edges.jsonl"):
            if e["p"] == "EXPRESSES":
                concepts[e["s"]].add(e["o"])
            if e.get("audit") == "sound" and e["o"] != e["s"]:
                positive[e["s"]].add(e["o"])
                incoming.add(e["o"])
    ids = sorted(nodes)
    tokens = {v: terms(nodes[v]) for v in ids}
    tamil = indexed_cosine({v: x[0] for v,x in tokens.items()})
    english = indexed_cosine({v: x[1] for v,x in tokens.items()})
    concept = indexed_cosine({v: concepts[v] for v in ids})
    rng = random.Random(SEED)
    tie = ids.copy()
    rng.shuffle(tie)
    def rankings(anchor):
        c,t,e = concept(anchor), tamil(anchor), english(anchor)
        candidates = [v for v in tie if v != anchor]
        return [sorted(candidates,key=lambda v:c.get(v,0),reverse=True),
                sorted(candidates,key=lambda v:c.get(v,0)+t.get(v,0)+e.get(v,0),reverse=True)]
    results, discovery = [], []
    for book in TARGET:
        pool = [v for v in ids if v.startswith(book+":") and positive[v]]
        for a in rng.sample(pool, 60):
            b = rng.choice(sorted(positive[a]))
            r1,r2 = rankings(a)
            results.append(dict(book=book, anchor=a, target=b, concept_rank=r1.index(b)+1,
                                combined_rank=r2.index(b)+1))
        empty = [v for v in ids if v.startswith(book+":") and not positive[v] and v not in incoming]
        for a in rng.sample(empty,4):
            _,ranking = rankings(a)
            b = ranking[0]
            discovery.append(dict(case=f"N{len(discovery)+1}", anchor=a,target=b,
                                  a=nodes[a]["tamil"],b=nodes[b]["tamil"]))
    with (HERE/"ranks.csv").open("w") as f:
        w = csv.DictWriter(f,fieldnames=results[0]);w.writeheader();w.writerows(results)
    (HERE/"discovery.json").write_text(json.dumps(discovery,indent=2,ensure_ascii=False)+"\n")
    print("Candidates per anchor",len(ids)-1)
    for book in TARGET:
        for metric in ("concept_rank","combined_rank"):
            ranks = [r[metric] for r in results if r["book"]==book]
            print(book,metric, "hits @1/10/50", *[sum(x<=k for x in ranks) for k in (1,10,50)],
                  "MRR",round(sum(1/x for x in ranks)/len(ranks),3))


if __name__ == "__main__":
    main()
