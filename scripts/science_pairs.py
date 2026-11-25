#!/usr/bin/env python3
"""Score every Siddhar verse x science finding pair, keep the top candidates,
draw seeded negative controls, and write blind grading packets.

Run: python3 -I scripts/science_pairs.py [--with-tirumanthiram] [--top 300]
     [--controls 100] [--seed 20261125] [--packet-size 40]

Inputs:  kg/siddhar/{nodes,edges}.jsonl (optionally kg/tirumanthiram/),
         kg/science/findings.jsonl, kg/science/concept_map.json
Outputs: kg/science/candidates.jsonl, kg/science/controls.jsonl,
         kg/science/pair_scores_summary.json,
         kg/science/grading/packet_NN.json, kg/science/grading/key.json
Stdlib only.
"""
import argparse, json, math, os, random, re, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCI = os.path.join(ROOT, "kg", "science")
RANK_W = {1: 1.0, 2: 0.8}
CONCEPT_W = 2.0   # a keyword reached through a concept tag
TEXT_W = 1.0      # a keyword found in the reading or nuance
PER_FINDING_MIN = 2
PER_FINDING_CAP = 10
PER_VERSE_CAP = 2
STOP = set("the a an of and or to in on at for by with is are was be as it its this that from not no".split())


def jl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def tokens(text):
    return [t for t in re.findall(r"[a-z]+", text.lower()) if t not in STOP]


def kw_in(kw, toks):
    """Keyword match: exact token, or token starting with the keyword if
    the keyword has 4+ letters (breath ~ breathing, breaths)."""
    if kw in toks:
        return True
    if len(kw) >= 4:
        return any(t.startswith(kw) for t in toks)
    return False


def load_verses(with_tm):
    books = ["siddhar"] + (["tirumanthiram"] if with_tm else [])
    verses = []
    for b in books:
        nodes = [n for n in jl(os.path.join(ROOT, "kg", b, "nodes.jsonl")) if n.get("type") == "Verse"]
        tags = defaultdict(list)
        for e in jl(os.path.join(ROOT, "kg", b, "edges.jsonl")):
            if e.get("p") == "EXPRESSES":
                tags[e["s"]].append((e["o"].split(":", 1)[1], e.get("rank", 3)))
        for n in nodes:
            n["_tags"] = tags.get(n["id"], [])
            n["_toks"] = set(tokens(n.get("reading", "") + " " + n.get("nuance", "")))
            verses.append(n)
    return verses


def score(v, f, cmap):
    ckw = {}
    for c, r in v["_tags"]:
        w = RANK_W.get(r, 0.6)
        for k in cmap.get(c, []):
            ckw[k.lower()] = max(ckw.get(k.lower(), 0), w)
    total, hits = 0.0, []
    for k in f["keywords"]:
        k = k.lower()
        s = 0.0
        if k in ckw:
            s += CONCEPT_W * ckw[k]
        if kw_in(k, v["_toks"]):
            s += TEXT_W
        if s:
            total += s
            hits.append(k)
    return round(total / math.sqrt(len(f["keywords"])), 4), hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-tirumanthiram", action="store_true")
    ap.add_argument("--top", type=int, default=300)
    ap.add_argument("--controls", type=int, default=100)
    ap.add_argument("--seed", type=int, default=20261125)
    ap.add_argument("--packet-size", type=int, default=40)
    a = ap.parse_args()

    findings = jl(os.path.join(SCI, "findings.jsonl"))
    fby = {f["id"]: f for f in findings}
    cmap = {k: v for k, v in json.load(open(os.path.join(SCI, "concept_map.json"), encoding="utf-8")).items() if not k.startswith("_")}
    verses = load_verses(a.with_tirumanthiram)
    vby = {v["id"]: v for v in verses}

    # 1. score all pairs
    allp = []
    for v in verses:
        for f in findings:
            s, hits = score(v, f, cmap)
            if s > 0 and len(hits) >= 2:
                allp.append((s, v["id"], f["id"], hits))
    n_all = len(verses) * len(findings)
    allp.sort(key=lambda x: (-x[0], x[1], x[2]))

    # 2. select candidates: coverage floor per finding, then global rank with caps
    chosen, pf, pv, seen = [], Counter(), Counter(), set()
    def take(p):
        chosen.append(p); pf[p[2]] += 1; pv[p[1]] += 1; seen.add((p[1], p[2]))
    for f in findings:
        for p in [p for p in allp if p[2] == f["id"]]:
            if pf[f["id"]] >= PER_FINDING_MIN:
                break
            if pv[p[1]] < PER_VERSE_CAP:
                take(p)
    for p in allp:
        if len(chosen) >= a.top:
            break
        if (p[1], p[2]) in seen or pf[p[2]] >= PER_FINDING_CAP or pv[p[1]] >= PER_VERSE_CAP:
            continue
        take(p)
    chosen.sort(key=lambda x: -x[0])
    cands = [{"kind": "candidate", "verse": v, "finding": f, "overlap_score": s, "matched_keywords": h, "rank": i + 1}
             for i, (s, v, f, h) in enumerate(chosen)]

    # 3. seeded negative controls
    rng = random.Random(a.seed)
    cand_pairs = {(c["verse"], c["finding"]) for c in cands}
    cand_findings = sorted({c["finding"] for c in cands})
    cand_verses = [c["verse"] for c in cands[: max(1, len(cands) // 3)]]  # top third
    vids = sorted(vby)
    controls = []
    na = a.controls // 2
    while len(controls) < na:
        f = rng.choice(cand_findings); v = rng.choice(vids)
        if (v, f) in cand_pairs or any(c["verse"] == v and c["finding"] == f for c in controls):
            continue
        s, h = score(vby[v], fby[f], cmap)
        controls.append({"kind": "control_a_random_verse", "verse": v, "finding": f, "overlap_score": s, "matched_keywords": h})
    while len(controls) < a.controls:
        v = rng.choice(cand_verses); f = rng.choice(findings)["id"]
        if (v, f) in cand_pairs or any(c["verse"] == v and c["finding"] == f for c in controls):
            continue
        s, h = score(vby[v], fby[f], cmap)
        controls.append({"kind": "control_b_random_finding", "verse": v, "finding": f, "overlap_score": s, "matched_keywords": h})

    with open(os.path.join(SCI, "candidates.jsonl"), "w", encoding="utf-8") as o:
        for c in cands: o.write(json.dumps(c, ensure_ascii=False) + "\n")
    with open(os.path.join(SCI, "controls.jsonl"), "w", encoding="utf-8") as o:
        for c in controls: o.write(json.dumps(c, ensure_ascii=False) + "\n")

    # 4. summary of the full score distribution
    hist = Counter(min(int(p[0]), 10) for p in allp)
    summ = {
        "verses": len(verses), "findings": len(findings), "pairs_scored": n_all,
        "pairs_with_2plus_keyword_hits": len(allp),
        "score_histogram_floor": {str(k): hist[k] for k in sorted(hist)},
        "candidates": len(cands), "candidate_min_score": cands[-1]["overlap_score"] if cands else None,
        "candidates_per_finding": dict(Counter(c["finding"] for c in cands).most_common()),
        "findings_without_candidates": [f["id"] for f in findings if f["id"] not in set(cand_findings)],
        "controls": dict(Counter(c["kind"] for c in controls)),
        "seed": a.seed, "with_tirumanthiram": a.with_tirumanthiram,
        "params": {"concept_w": CONCEPT_W, "text_w": TEXT_W, "rank_w": RANK_W, "per_finding_min": PER_FINDING_MIN,
                   "per_finding_cap": PER_FINDING_CAP, "per_verse_cap": PER_VERSE_CAP},
    }
    json.dump(summ, open(os.path.join(SCI, "pair_scores_summary.json"), "w"), indent=1, ensure_ascii=False)

    # 5. blind packets
    items = cands + controls
    rng.shuffle(items)
    gdir = os.path.join(SCI, "grading"); os.makedirs(gdir, exist_ok=True)
    for fn in os.listdir(gdir):
        if fn.startswith("packet_") and fn.endswith(".json"):
            os.remove(os.path.join(gdir, fn))
    key = {}
    npk = math.ceil(len(items) / a.packet_size)
    for p in range(npk):
        out = []
        for j, it in enumerate(items[p * a.packet_size:(p + 1) * a.packet_size]):
            iid = "P%02d-%02d" % (p + 1, j + 1)
            v, f = vby[it["verse"]], fby[it["finding"]]
            key[iid] = {k: it[k] for k in ("kind", "verse", "finding", "overlap_score")}
            out.append({
                "item": iid,
                "verse": {"id": v["id"], "unit_id": v.get("unit_id"), "poet": v.get("siddhar", "திருமூலர்"),
                          "work": v.get("work_title", v.get("book")), "tamil": v.get("tamil"),
                          "reading": v.get("reading"), "nuance": v.get("nuance")},
                "finding": {"id": f["id"], "domain": f["domain"], "claim": f["claim"], "strength": f["strength"]},
            })
        json.dump({"packet": p + 1, "brief": "docs/science-grader-brief.md",
                   "output": "kg/science/grading/graded/packet_%02d.<grader>.json" % (p + 1), "items": out},
                  open(os.path.join(gdir, "packet_%02d.json" % (p + 1)), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(key, open(os.path.join(gdir, "key.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: summ[k] for k in ("verses", "findings", "pairs_scored", "pairs_with_2plus_keyword_hits", "candidates", "candidate_min_score", "controls", "findings_without_candidates")}, ensure_ascii=False))
    print("packets:", npk)


if __name__ == "__main__":
    sys.exit(main())
