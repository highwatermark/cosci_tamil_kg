#!/usr/bin/env python3
"""Unblind graded science packets and keep only pairs that beat the controls.

Run: python3 -I scripts/science_threshold.py

Reads  kg/science/grading/key.json and every grader file
       kg/science/grading/graded/packet_NN.<grader>.json (a JSON array of
       {"item","grade","direction","reason",...}; several graders per packet
       are averaged).
Writes kg/science/strong_links.jsonl and kg/science/threshold_summary.json.

Rule: a candidate pair is "strong" only if
  (1) its mean blind grade is >= 2, AND
  (2) its mean blind grade exceeds the 95th percentile of the mean grades
      that the same graders gave the negative controls, AND
  (3) its overlap score exceeds the 95th percentile of control overlap scores.
Condition (2) is the one that does the work: if graders give controls 2s,
the bar rises to 3 (or nothing passes). Stdlib only.
"""
import glob, json, os, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCI = os.path.join(ROOT, "kg", "science")
G = os.path.join(SCI, "grading")


def pctl(xs, q):
    """Linear-interpolated percentile (same as numpy's default)."""
    xs = sorted(xs)
    if not xs:
        return None
    k = (len(xs) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def main():
    key = json.load(open(os.path.join(G, "key.json"), encoding="utf-8"))
    grades = defaultdict(list)
    files = sorted(glob.glob(os.path.join(G, "graded", "packet_*.json")))
    bad = 0
    for fn in files:
        for r in json.load(open(fn, encoding="utf-8")):
            g = r.get("grade")
            if r.get("item") not in key or not isinstance(g, (int, float)) or not 0 <= g <= 3:
                bad += 1
                continue
            grades[r["item"]].append({"grade": g, "direction": r.get("direction", "neither"),
                                      "reason": r.get("reason", ""), "cipher_dependent": r.get("cipher_dependent"),
                                      "grader": os.path.basename(fn).split(".")[1] if fn.count(".") >= 2 else "?"})
    summ = {"grader_files": len(files), "items_in_key": len(key), "items_graded": len(grades), "rejected_rows": bad}
    if not grades:
        summ["status"] = "no graded packets yet: run graders on kg/science/grading/packet_*.json first"
        json.dump(summ, open(os.path.join(SCI, "threshold_summary.json"), "w"), indent=1)
        print(json.dumps(summ, indent=1))
        return 0

    mean = {i: sum(x["grade"] for x in v) / len(v) for i, v in grades.items()}
    ctrl = [i for i in mean if key[i]["kind"].startswith("control")]
    cand = [i for i in mean if key[i]["kind"] == "candidate"]
    ctrl_g = [mean[i] for i in ctrl]
    p95_g = pctl(ctrl_g, 0.95)
    p95_o = pctl([key[i]["overlap_score"] for i in key if key[i]["kind"].startswith("control")], 0.95)

    findings = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(SCI, "findings.jsonl"), encoding="utf-8")}
    strong = []
    for i in sorted(cand, key=lambda i: (-mean[i], -key[i]["overlap_score"])):
        k = key[i]
        if mean[i] >= 2 and (p95_g is None or mean[i] > p95_g) and k["overlap_score"] > (p95_o or 0):
            dirs = Counter(x["direction"] for x in grades[i])
            f = findings[k["finding"]]
            strong.append({"verse": k["verse"], "finding": k["finding"], "item": i,
                           "mean_grade": round(mean[i], 3), "n_graders": len(grades[i]),
                           "direction": dirs.most_common(1)[0][0], "directions": dict(dirs),
                           "overlap_score": k["overlap_score"], "finding_strength": f["strength"],
                           "finding_domain": f["domain"], "reasons": [x["reason"] for x in grades[i]],
                           "cipher_dependent": any(x.get("cipher_dependent") for x in grades[i])})
    with open(os.path.join(SCI, "strong_links.jsonl"), "w", encoding="utf-8") as o:
        for s in strong:
            o.write(json.dumps(s, ensure_ascii=False) + "\n")

    def dist(ids):
        return dict(sorted(Counter(round(mean[i] * 2) / 2 for i in ids).items()))
    summ.update({
        "status": "complete" if len(grades) == len(key) else "partial: %d of %d items graded" % (len(grades), len(key)),
        "controls_graded": len(ctrl), "candidates_graded": len(cand),
        "control_grade_distribution": dist(ctrl), "candidate_grade_distribution": dist(cand),
        "control_grade_p95": p95_g, "control_overlap_p95": p95_o,
        "controls_graded_2plus": sum(1 for g in ctrl_g if g >= 2),
        "control_false_positive_rate": round(sum(1 for g in ctrl_g if g >= 2) / len(ctrl_g), 3) if ctrl_g else None,
        "candidates_graded_2plus": sum(1 for i in cand if mean[i] >= 2),
        "strong": len(strong),
        "strong_by_direction": dict(Counter(s["direction"] for s in strong)),
        "strong_by_finding_strength": dict(Counter(s["finding_strength"] for s in strong)),
        "strong_by_domain": dict(Counter(s["finding_domain"] for s in strong)),
        "strong_cipher_dependent": sum(1 for s in strong if s["cipher_dependent"]),
    })
    json.dump(summ, open(os.path.join(SCI, "threshold_summary.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(summ, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
