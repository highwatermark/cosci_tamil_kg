#!/usr/bin/env python3
"""Merge every blind grading of the marking pass into one link audit per corpus group.

Reads every kg/themes/sangam_grading/**/key.json (round1, round2, pilots/*, wave3/*, wave4, wave5/*,
wave6, ...) with its graded/packet_N.<grader>.json (made by scripts/make_sangam_packets.py and scored
by scripts/score_sangam_grades.py) and writes:

- kg/groups/<group>/link_audit.json: the links proposed from that group's books (docs/corpus-groups.md),
  with a summary for the group;
- kg/groups/all_link_audit.json: every link, the summary per book, per group and per group pair, and
  the akam re-tags;
- kg/sangam_core/link_audit.json: the Akananuru, Purananuru and Pattupattu links and re-tags, in the
  shape scripts/build_sangam_graph.py reads.

Per link:
- grade: the STRICTEST grade any blind grader gave it (sound < weak < forced < wrong). Every grade is
  kept in `grades` with its run (the grading directory), grader, model and role. A proposal that a
  later packet reused as a calibration link was graded blind again, and that grade counts too.
- teaches_holds false if any grader failed `teaches`; list_adds_holds and gains_holds the same.
- better_type and reason come from the grader whose grade was kept; every reason is in `reasons`.

Models: wave6's g1 was Sonnet and its g2 Opus; every other run's graders were Opus. The marker was
Opus except for wave 6's Civaka Cintamani chapters 102-133, Soolamani and the three minor epics, which
Sonnet marked (MARKER_SONNET).

Summaries (per book, per group, per group pair, per run and per marker model): grade counts and
sound%, teaches failed, calibration (each grader's grade of the hidden known-grade links in the
packets that held that book's or pair's links, against the known grade: exact, stricter, more
lenient), and agreement between graders on the links graded more than once (exact, and Cohen's kappa
on sound/not sound).

Usage: python3 -I scripts/merge_sangam_grades.py
"""
import importlib.util
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRADING = ROOT / "kg" / "themes" / "sangam_grading"
GROUPS_DIR = ROOT / "kg" / "groups"
SANGAM_OUT = ROOT / "kg" / "sangam_core" / "link_audit.json"
SANGAM_BOOKS = ("akananuru", "purananuru", "pattupattu")
ORDER = {"sound": 0, "weak": 1, "forced": 2, "wrong": 3}


def load_module(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


score = load_module("score", "score_sangam_grades.py")
packets = load_module("packets", "make_sangam_packets.py")
GROUP = packets.GROUP


def grader_model(run, grader):
    return "sonnet" if run == "wave6" and grader == "g1" else "opus"


def marker_model(book, chapter):
    if book in ("soolamani", "naga_kumara_kaviyam", "udayana_kumara_kaviyam", "yasodhara_kaviyam"):
        return "sonnet"
    if book == "civaka_cintamani" and int(chapter) >= 102:
        return "sonnet"
    return "opus"


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


def pct(n, d):
    return round(100 * n / d, 1) if d else None


def summarise(links, cal_rows):
    """Grade counts, sound%, teaches, agreement on links graded twice or more, calibration."""
    by = Counter(l["grade"] for l in links)
    n = len(links)
    multi = [l for l in links if l["graders"] > 1]
    pairs_exact = pairs = 0
    xs, ys = [], []
    for l in multi:
        gs = [g["grade"] for g in l["grades"]]
        for i in range(len(gs)):
            for j in range(i + 1, len(gs)):
                pairs += 1
                pairs_exact += gs[i] == gs[j]
                xs.append(gs[i] == "sound")
                ys.append(gs[j] == "sound")
    k = score.kappa(xs, ys) if xs else None
    cal = Counter()
    for row in cal_rows:
        cal["n"] += 1
        cal[row["result"]] += 1
    return {
        "links": n, "by_grade": {g: by[g] for g in ORDER if by[g]},
        "sound_pct": pct(by["sound"], n), "sound_or_weak_pct": pct(by["sound"] + by["weak"], n),
        "teaches_failed": sum(l["teaches_holds"] is False for l in links),
        "agreement": {"links_graded_more_than_once": len(multi), "grade_pairs": pairs,
                      "exact": pairs_exact, "exact_pct": pct(pairs_exact, pairs),
                      "kappa_sound": None if k is None else round(k, 3),
                      "disagreements": sum(l["disagree"] for l in multi)},
        "calibration": {"links": cal["n"], "exact": cal["exact"], "stricter": cal["stricter"],
                        "more_lenient": cal["more_lenient"], "exact_pct": pct(cal["exact"], cal["n"])},
    }


def main():
    grades = defaultdict(list)        # (a, b) -> [grade record]
    proposals = {}                    # (a, b) -> (run, key item)
    packet_of = defaultdict(set)      # (a, b) -> {(run, packet)}
    cal_by_packet = defaultdict(list)  # (run, packet) -> [calibration result]
    retags, part_b_other = {}, {}
    runs = []
    for kp in sorted(GRADING.rglob("key.json")):
        rdir = kp.parent
        run = str(rdir.relative_to(GRADING))
        key, graded, problems = score.load(rdir)
        if not graded:
            runs.append({"run": run, "graders": [], "note": "no graded files"})
            continue
        matched = score.match(key, graded, problems)
        for k in key:
            if k["part"] == "A" and k["kind"] == "proposal":
                proposals[(k["a"], k["b"])] = (run, k)
                packet_of[(k["a"], k["b"])].add((run, k["packet"]))
        for grader, got in matched.items():
            model = grader_model(run, grader)
            for i, g in got.items():
                k = key[i]
                if k["part"] == "A":
                    gr = score.grade_of(g)
                    role = k["kind"]
                    if role == "calibration":
                        d = ORDER.get(gr, 9) - ORDER[k["known"]]
                        cal_by_packet[(run, k["packet"])].append({
                            "grader": grader, "model": model, "known": k["known"], "grade": gr,
                            "result": "exact" if d == 0 else "stricter" if d > 0 else "more_lenient"})
                    grades[(k["a"], k["b"])].append({
                        "run": run, "grader": grader, "model": model, "role": role, "grade": gr,
                        "better_type": g.get("better_type"), "teaches_holds": g.get("teaches_holds"),
                        "list_adds_holds": g.get("list_adds_holds"), "gains_holds": g.get("gains_holds"),
                        "reason": g.get("reason"), "text_issue": g.get("text_issue")})
                elif "ullurai_present" in k:
                    r = retags.setdefault(k["id"], {
                        "id": k["id"], "chapter": k["chapter"], "round": run,
                        "marker": {"ullurai": k["ullurai_present"], "iraicchi": k["iraicchi_present"],
                                   "ullurai_vehicle": k.get("ullurai_vehicle"),
                                   "iraicchi_carrier": k.get("iraicchi_carrier")},
                        "graders": {}})
                    r["graders"][f"{run}.{grader}"] = {"ullurai": device_tag(g, "ullurai"),
                                                       "iraicchi": device_tag(g, "iraicchi")}
                else:
                    tags = k.get("tags") or {}
                    r = part_b_other.setdefault(k["id"], {"id": k["id"], "fieldset": k.get("fieldset"),
                                                          "run": run, "graders": 0, "agree": 0})
                    r["graders"] += 1
                    if k.get("fieldset") == "ethics":
                        r["agree"] += str(g.get("domain")) == str(tags.get("domain"))
                    else:
                        r["agree"] += bool(g.get("claims")) == bool(tags.get("claims"))
        _, out = score.score(rdir)
        runs.append({"run": run, "brief": out.get("brief"),
                     "graders": {g: grader_model(run, g) for g in sorted(graded)},
                     "packets": {g: sorted(graded[g]) for g in sorted(graded)},
                     "calibration": out.get("calibration", {}), "agreement": out.get("between_graders", {}),
                     "problems": problems})
    for r in retags.values():
        for field in ("ullurai", "iraicchi"):
            tags = [t[field]["present"] for t in r["graders"].values()]
            if r["marker"][field]:
                r[f"{field}_status"] = ("confirmed" if any(tags) else "not_confirmed") if tags else "not_retagged"
            else:
                r[f"{field}_status"] = "grader_only" if any(tags) else "absent"
            r[f"{field}_graders_agree"] = f"{sum(t == r['marker'][field] for t in tags)}/{len(tags)}"

    def holds(gs, field):
        vals = [g.get(field) for g in gs]
        return False if any(v is False for v in vals) else True if any(v is True for v in vals) else None

    links = []
    for (a, b), (run, k) in proposals.items():
        gs = grades.get((a, b), [])
        if not gs:
            continue
        kept = max(gs, key=lambda g: ORDER.get(g["grade"], 9))
        issues = [g["text_issue"] for g in gs if g.get("text_issue")]
        rec = {
            "a": a, "b": b, "type": k["type"], "grade": kept["grade"],
            "graders": len(gs), "disagree": len({g["grade"] for g in gs}) > 1,
            "better_type": kept.get("better_type"),
            "teaches_holds": holds(gs, "teaches_holds"),
            "reason": kept.get("reason"),
            "text_issue": " | ".join(dict.fromkeys(issues)) or None,
            "chapter": k["chapter"], "book": k["book"], "target_book": k["target_book"],
            "group_a": GROUP.get(k["book"]) or k["group_a"], "group_b": GROUP.get(k["target_book"]) or k["group_b"],
            "marker_model": marker_model(k["book"], k["chapter"]), "proposed_in": run,
            "grades": [{x: g[x] for x in ("run", "grader", "model", "role", "grade", "better_type", "teaches_holds")}
                       for g in gs],
            "reasons": [g["reason"] for g in gs]}
        rec["within_group"] = rec["group_a"] == rec["group_b"]
        if "list_adds" in k:
            rec["list_adds_holds"] = holds(gs, "list_adds_holds")
        if k.get("bridge") or k.get("gains"):
            rec["gains_holds"] = holds(gs, "gains_holds")
        links.append(rec)
    links.sort(key=lambda l: (l["group_a"] or "", l["book"], l["chapter"], l["a"], l["b"]))

    def cal_rows(ls):
        seen = set()
        for l in ls:
            seen |= packet_of[(l["a"], l["b"])]
        return [row for p in sorted(seen) for row in cal_by_packet.get(p, [])]

    def table(keyfn):
        groups = defaultdict(list)
        for l in links:
            groups[keyfn(l)].append(l)
        return {k: summarise(v, cal_rows(v)) for k, v in sorted(groups.items())}

    per_book = table(lambda l: l["book"])
    for b, s in per_book.items():
        s["group"] = GROUP.get(b)
        s["marker_models"] = dict(Counter(l["marker_model"] for l in links if l["book"] == b))
        s["grader_models"] = dict(Counter(g["model"] for l in links if l["book"] == b for g in l["grades"]))
    per_group = table(lambda l: l["group_a"])
    per_pair = table(lambda l: f"{l['group_a']}|{l['group_b']}")
    # marker model, judged both by the strictest grade and under one grader (wave 6's g1, Sonnet)
    w6 = [l for l in links if l["proposed_in"] == "wave6"]
    by_marker = {}
    for m in ("opus", "sonnet"):
        ls = [l for l in w6 if l["marker_model"] == m]
        g1 = [g["grade"] for l in ls for g in l["grades"] if g["run"] == "wave6" and g["grader"] == "g1"]
        by_marker[m] = {"links": len(ls), "strictest_sound_pct": pct(sum(l["grade"] == "sound" for l in ls), len(ls)),
                        "g1_graded": len(g1), "g1_sound_pct": pct(g1.count("sound"), len(g1)),
                        "books": dict(Counter(l["book"] for l in ls))}
    by_grader_model = {}
    for m in ("opus", "sonnet"):
        gs = [g for l in links for g in l["grades"] if g["model"] == m]
        rows = [row for rs in cal_by_packet.values() for row in rs if row["model"] == m]
        c = Counter(r["result"] for r in rows)
        by_grader_model[m] = {"grades": len(gs), "sound_pct": pct(sum(g["grade"] == "sound" for g in gs), len(gs)),
                              "calibration": {"links": len(rows), **{k: c[k] for k in ("exact", "stricter", "more_lenient")},
                                              "exact_pct": pct(c["exact"], len(rows))}}
    overall = summarise(links, [row for rs in cal_by_packet.values() for row in rs])
    summary = {
        "run": "Blind grading of every marked book's links, all grading runs merged, 2026-11-27",
        "method": ("Every proposed link in kg/themes/<book>/ch*.json that a packet under kg/themes/sangam_grading "
                   "held was graded blind per docs/sangam-, ethics- or epic-grader-brief.md, with links of known "
                   "grade hidden in each packet. Where more than one grader graded a link the strictest grade is "
                   "kept and all are recorded with grader and model; teaches_holds, list_adds_holds and "
                   "gains_holds are false if any grader failed them."),
        "models": {"graders": "Opus in every run except wave6 g1 (Sonnet); wave6 g2 is an Opus spot-check",
                   "markers": "Opus, except Sonnet for wave 6's Civaka Cintamani ch102-133, Soolamani, Naga Kumara, "
                              "Udayana Kumara and Yasodhara Kaviyam"},
        **overall,
        "by_marker_model_wave6": by_marker,
        "by_grader_model": by_grader_model,
        "retags": {"poems": len(retags),
                   **{f"{f}_{s}": sum(r[f"{f}_status"] == s for r in retags.values())
                      for f in ("ullurai", "iraicchi") for s in ("confirmed", "not_confirmed", "grader_only")},
                   "ethics_items": sum(r["fieldset"] == "ethics" for r in part_b_other.values()),
                   "narrative_units": sum(r["fieldset"] == "narrative" for r in part_b_other.values())},
        "runs": runs,
        "limits": ("All graders are Claude without a Tamil lexicon; only the Kural and Naladiyar have commentary in "
                   "the corpus. No Tamil scholar has reviewed this."),
    }
    retag_list = sorted(retags.values(), key=lambda r: r["id"])
    GROUPS_DIR.mkdir(parents=True, exist_ok=True)

    def dump(path, obj):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    dump(GROUPS_DIR / "all_link_audit.json", {
        "summary": summary, "by_book": per_book, "by_group": per_group, "by_group_pair": per_pair,
        "links": links, "retags": retag_list, "part_b": sorted(part_b_other.values(), key=lambda r: r["id"])})
    for g in sorted({l["group_a"] for l in links}):
        ls = [l for l in links if l["group_a"] == g]
        books = sorted({l["book"] for l in ls})
        dump(GROUPS_DIR / g / "link_audit.json", {
            "summary": {"group": g, "books": books, **per_group[g],
                        "by_book": {b: per_book[b] for b in books},
                        "by_target_group": {p.split("|")[1]: s for p, s in per_pair.items() if p.split("|")[0] == g}},
            "links": ls,
            "retags": [r for r in retag_list if GROUP.get(r["id"].split(":")[0]) == g]})
    # The Sangam core graph keeps its own audit (scripts/build_sangam_graph.py reads it).
    sl = [l for l in links if l["book"] in SANGAM_BOOKS]
    dump(SANGAM_OUT, {"summary": {"books": list(SANGAM_BOOKS), **summarise(sl, cal_rows(sl)),
                                  "note": "a slice of kg/groups/all_link_audit.json"},
                      "links": sl, "retags": [r for r in retag_list if r["id"].split(":")[0] in SANGAM_BOOKS]})
    print(f"links={len(links)} {overall['by_grade']} sound={overall['sound_pct']}% "
          f"graded>1={overall['agreement']['links_graded_more_than_once']} calibration={overall['calibration']} "
          f"groups={len(per_group)} pairs={len(per_pair)} retags={len(retags)}")
    for m, s in by_marker.items():
        print(f"wave6 marker {m}: {s['links']} links, strictest sound {s['strictest_sound_pct']}%, g1 sound {s['g1_sound_pct']}%")


if __name__ == "__main__":
    main()
