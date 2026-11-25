#!/usr/bin/env python3
"""Merge the blind grades of the Sangam marking pass into kg/sangam_core/link_audit.json.

Reads kg/themes/sangam_grading/round*/key.json and graded/packet_N.<grader>.json (made by
scripts/make_sangam_packets.py and scored by scripts/score_sangam_grades.py) and writes one record per
proposed (a, b) link, in the shape of kg/siddhar/link_audit.json:

- grade: the STRICTEST grade any blind grader gave the link (sound < weak < forced < wrong). Every grade
  is kept in `grades`, with its round, grader and role; a round-1 link that round 2 reused as a
  calibration link was graded blind again, and that grade counts too.
- teaches_holds: false if any grader said the `teaches` sentence fails; better_type and reason come
  from the grader whose grade was kept (all reasons are in `reasons`); text_issue joins every grader's.

It also stores each akam poem's Part B re-tags (`retags`), so the graph can say whether a grader
agreed with the marker's ullurai or iraicchi, and a summary with the grade counts, calibration
(grader against the known grade) and agreement between graders, from score_sangam_grades.py.

Usage: python3 -I scripts/merge_sangam_grades.py
"""
import importlib.util
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRADING = ROOT / "kg" / "themes" / "sangam_grading"
OUT = ROOT / "kg" / "sangam_core" / "link_audit.json"
ORDER = {"sound": 0, "weak": 1, "forced": 2, "wrong": 3}

spec = importlib.util.spec_from_file_location("score", ROOT / "scripts" / "score_sangam_grades.py")
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)


def device_tag(g, field):
    """A grader's re-tag of one device: {"present", "vehicle"|"carrier", "failed"}."""
    v = g.get(field)
    rej = g.get(f"{field}_candidate_rejected")
    out = {"present": bool(v)}
    thing = (v or {}).get("vehicle" if field == "ullurai" else "carrier") if isinstance(v, dict) else None
    if thing is not None:
        out["vehicle" if field == "ullurai" else "carrier"] = thing
    if isinstance(rej, dict) and rej.get("failed") is not None:
        out["rejected_candidate"] = rej.get("vehicle") or rej.get("carrier")
        out["failed"] = rej.get("failed")
    return out


def main():
    grades = defaultdict(list)        # (a, b) -> [grade record]
    proposals = {}                    # (a, b) -> key item
    retags = {}
    cal = Counter()
    agreement, part_b, rounds = {}, {}, []
    for rdir in sorted(p.parent for p in GRADING.glob("round*/key.json")):
        rnd = rdir.name
        key, graded, problems = score.load(rdir)
        matched = score.match(key, graded, problems)
        rounds.append({"round": rnd, "graders": sorted(graded),
                       "packets": {g: sorted(graded[g]) for g in sorted(graded)}, "problems": problems})
        for i, k in enumerate(key):
            if k["part"] == "A" and k["kind"] == "proposal":
                proposals[(k["a"], k["b"])] = k
        for grader, got in matched.items():
            for i, g in got.items():
                k = key[i]
                if k["part"] == "A":
                    gr = score.grade_of(g)
                    if k["kind"] == "calibration":
                        cal["links"] += 1
                        d = ORDER.get(gr, 9) - ORDER[k["known"]]
                        cal["exact" if d == 0 else "stricter" if d > 0 else "more_lenient"] += 1
                        if not k["a"].split(":")[0] in ("akananuru", "purananuru", "pattupattu"):
                            continue
                    grades[(k["a"], k["b"])].append({
                        "round": rnd, "grader": grader, "role": k["kind"], "grade": gr,
                        "better_type": g.get("better_type"), "teaches_holds": g.get("teaches_holds"),
                        "reason": g.get("reason"), "text_issue": g.get("text_issue")})
                else:
                    r = retags.setdefault(k["id"], {
                        "id": k["id"], "chapter": k["chapter"], "round": rnd,
                        "marker": {"ullurai": k["ullurai_present"], "iraicchi": k["iraicchi_present"],
                                   "ullurai_vehicle": k.get("ullurai_vehicle"),
                                   "iraicchi_carrier": k.get("iraicchi_carrier")},
                        "graders": {}})
                    r["graders"][f"{rnd}.{grader}"] = {"ullurai": device_tag(g, "ullurai"),
                                                       "iraicchi": device_tag(g, "iraicchi")}
        # agreement and Part B numbers, as score_sangam_grades.py --json gives them
        report, out = score.score(rdir)
        agreement[rnd] = out.get("between_graders", {})
        part_b[rnd] = out.get("part_b", {})
        rounds[-1]["calibration"] = out.get("calibration", {})
    for r in retags.values():
        for field in ("ullurai", "iraicchi"):
            tags = [t[field]["present"] for t in r["graders"].values()]
            if r["marker"][field]:
                r[f"{field}_status"] = ("confirmed" if any(tags) else "not_confirmed") if tags else "not_retagged"
            else:
                r[f"{field}_status"] = "grader_only" if any(tags) else "absent"
            r[f"{field}_graders_agree"] = f"{sum(t == r['marker'][field] for t in tags)}/{len(tags)}"
    links = []
    for (a, b), k in proposals.items():
        gs = grades.get((a, b), [])
        if not gs:
            continue
        kept = max(gs, key=lambda g: ORDER.get(g["grade"], 9))
        grade_set = {g["grade"] for g in gs}
        issues = [g["text_issue"] for g in gs if g.get("text_issue")]
        links.append({
            "a": a, "b": b, "type": k["type"], "grade": kept["grade"],
            "graders": len(gs), "disagree": len(grade_set) > 1,
            "better_type": kept.get("better_type"),
            "teaches_holds": (False if any(g["teaches_holds"] is False for g in gs)
                              else True if any(g["teaches_holds"] is True for g in gs) else None),
            "reason": kept.get("reason"),
            "text_issue": " | ".join(dict.fromkeys(issues)) or None,
            "chapter": k["chapter"], "book": k["book"], "target_book": k["target_book"],
            "group_a": k["group_a"], "group_b": k["group_b"], "within_group": k["within_group"],
            "grades": [{x: g[x] for x in ("round", "grader", "role", "grade", "better_type", "teaches_holds")} for g in gs],
            "reasons": [g["reason"] for g in gs]})
    links.sort(key=lambda l: (l["book"], l["chapter"], l["a"], l["b"]))
    by_grade = Counter(l["grade"] for l in links)
    multi = [l for l in links if l["graders"] > 1]
    summary = {
        "run": "Blind grading of the Sangam marking pass's links (Akananuru, Purananuru, Thirumurugatruppadai), rounds 1 and 2, 2026-11-25",
        "method": (f"{len(links)} proposed links from the chapter files in kg/themes/akananuru, purananuru and pattupattu "
                   "were graded blind per docs/sangam-grader-brief.md in kg/themes/sangam_grading/round1 and round2, "
                   "with Kural, Naladiyar or earlier Sangam links of known grade hidden in each packet. Where more "
                   "than one grader graded a link the strictest grade is kept and all are recorded; teaches_holds is "
                   "false if any grader failed it."),
        "by_grade": {g: by_grade[g] for g in ORDER if by_grade[g]},
        "graded_more_than_once": len(multi),
        "disagreements": sum(l["disagree"] for l in multi),
        "teaches_failed": sum(l["teaches_holds"] is False for l in links),
        "calibration": dict(cal),
        "calibration_by_round": {r["round"]: r["calibration"] for r in rounds},
        "agreement": agreement,
        "retags": {"poems": len(retags),
                   **{f"{f}_{s}": sum(r[f"{f}_status"] == s for r in retags.values())
                      for f in ("ullurai", "iraicchi") for s in ("confirmed", "not_confirmed", "grader_only")}},
        "part_b": part_b,
        "rounds": rounds,
        "limits": ("All graders are Claude without a Tamil lexicon; the Sangam books have no commentary in the corpus. "
                   "No Tamil scholar has reviewed this."),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"summary": summary, "links": links,
                               "retags": sorted(retags.values(), key=lambda r: (r["chapter"], int(r["id"].split(":")[1])))},
                              ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"links={len(links)} {dict(by_grade)} graded>1={len(multi)} disagree={summary['disagreements']} "
          f"teaches_failed={summary['teaches_failed']} calibration={dict(cal)} retags={summary['retags']}")


if __name__ == "__main__":
    main()
