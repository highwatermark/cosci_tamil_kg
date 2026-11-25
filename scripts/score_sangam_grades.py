"""Score blind grades of Sangam packets made by scripts/make_sangam_packets.py.

Usage (from the repository root):
  python3 -I scripts/score_sangam_grades.py OUTDIR [--json FILE]

Reads OUTDIR/key.json and every OUTDIR/graded/packet_N.<grader>.json. A graded file is the object
{"links": [...], "poems": [...]} the packet asks for; a bare array, or an object of several arrays,
is also accepted (an item with "grade" is a link, an item with "id" is a poem).

Reports, per grader and pooled: Part A grades of the proposed links by book, by target book and
within-group against cross-group, and how often `teaches` held; agreement with the calibration
links' known grades; agreement between graders when there are two or more (exact, and Cohen's kappa
on the grade and on sound/not sound). Part B: Cohen's kappa between the proposer and each grader
(and between graders) on ullurai_present and iraicchi_present, and the conditions the graders'
rejected candidates failed. --json FILE also writes the numbers as JSON.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

GRADES = ("sound", "weak", "forced", "wrong")


def usage(msg=None):
    if msg:
        print("error:", msg, file=sys.stderr)
    print(__doc__.split("\n\n")[1], file=sys.stderr)
    sys.exit(2)


def kappa(xs, ys):
    """Cohen's kappa for two equal-length label lists; None when undefined."""
    n = len(xs)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(xs, ys)) / n
    cx, cy = Counter(xs), Counter(ys)
    pe = sum(cx[k] * cy[k] for k in set(cx) | set(cy)) / (n * n)
    if pe == 1:
        return 1.0 if po == 1 else None
    return (po - pe) / (1 - pe)


def fmt_k(k):
    return "n/a" if k is None else f"{k:.2f}"


def items_of(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        out = []
        for v in data.values():
            if isinstance(v, list):
                out += v
        return out
    return []


def load(outdir):
    key = json.loads((outdir / "key.json").read_text(encoding="utf-8"))
    gdir = outdir / "graded"
    if not gdir.is_dir():
        usage(f"{gdir} does not exist")
    files = sorted(gdir.glob("packet_*.*.json"))
    graded = defaultdict(dict)            # grader -> packet -> (links, poems)
    problems = []
    for f in files:
        m = re.fullmatch(r"packet_(\d+)\.(.+)\.json", f.name)
        if not m:
            continue
        pk, grader = int(m.group(1)), m.group(2)
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            problems.append(f"{f.name}: does not parse ({e})")
            continue
        its = items_of(data)
        links = [x for x in its if isinstance(x, dict) and "grade" in x]
        poems = [x for x in its if isinstance(x, dict) and "id" in x and "grade" not in x]
        graded[grader][pk] = (links, poems)
    return key, graded, problems


def match(key, graded, problems):
    """grader -> {key index: graded item}, matching links by order then by (a, b), poems by id."""
    by_packet = defaultdict(lambda: {"A": [], "B": []})
    for i, k in enumerate(key):
        by_packet[k["packet"]][k["part"]].append(i)
    res = {}
    for grader, packets in graded.items():
        got = {}
        for pk, (links, poems) in packets.items():
            want = by_packet.get(pk)
            if want is None:
                problems.append(f"packet_{pk}.{grader}: no such packet in the key")
                continue
            ka = want["A"]
            if len(links) != len(ka):
                problems.append(f"packet_{pk}.{grader}: {len(links)} links graded, packet has {len(ka)}")
            free = list(links)
            for pos, i in enumerate(ka):
                k = key[i]
                g = links[pos] if pos < len(links) else None
                if g is None or (str(g.get("a")), str(g.get("b"))) != (k["a"], k["b"]):
                    g = next((x for x in free if (str(x.get("a")), str(x.get("b"))) == (k["a"], k["b"])), None)
                if g is None:
                    problems.append(f"packet_{pk}.{grader}: link {k['a']} -> {k['b']} not graded")
                    continue
                if g in free:
                    free.remove(g)
                got[i] = g
            kb = want["B"]
            pid = {str(x.get("id")): x for x in poems}
            if len(poems) != len(kb):
                problems.append(f"packet_{pk}.{grader}: {len(poems)} poems tagged, packet has {len(kb)}")
            for i in kb:
                g = pid.get(key[i]["id"])
                if g is None:
                    problems.append(f"packet_{pk}.{grader}: poem {key[i]['id']} not tagged")
                    continue
                got[i] = g
        res[grader] = got
    return res


def grade_of(g):
    v = str(g.get("grade", "")).strip().lower()
    return v if v in GRADES else "invalid"


def table(title, rows, report):
    """rows: {label: Counter of grades + 'teaches_false', 'n'}"""
    report.append(f"  {title}")
    report.append(f"    {'':40}{'n':>4} " + " ".join(f"{g:>7}" for g in GRADES) + "  sound%  teaches_false")
    for label in sorted(rows):
        c = rows[label]
        n = c["n"]
        report.append(f"    {label:40}{n:>4} " + " ".join(f"{c[g]:>7}" for g in GRADES)
                      + f"  {100 * c['sound'] / n if n else 0:5.0f}%  {c['teaches_false']:>5}")


def part_a(key, matched, report, out):
    props = [i for i, k in enumerate(key) if k["part"] == "A" and k["kind"] == "proposal"]
    cals = [i for i, k in enumerate(key) if k["part"] == "A" and k["kind"] == "calibration"]
    report.append(f"PART A: {len(props)} proposed links, {len(cals)} calibration links")
    graders = sorted(matched)
    for who in graders + (["pooled"] if len(graders) > 1 else []):
        srcs = graders if who == "pooled" else [who]
        dims = {"by book": defaultdict(Counter), "by target book": defaultdict(Counter),
                "within/cross group": defaultdict(Counter), "by type": defaultdict(Counter)}
        total = Counter()
        for s in srcs:
            for i in props:
                g = matched[s].get(i)
                if g is None:
                    continue
                k = key[i]
                gr = grade_of(g)
                tf = g.get("teaches_holds") is False
                for dim, lab in (("by book", k["book"]), ("by target book", k["target_book"]),
                                 ("within/cross group", "within " + k["group_a"] if k["within_group"]
                                  else f"cross {k['group_a']}->{k['group_b']}"),
                                 ("by type", k["type"])):
                    c = dims[dim][lab]
                    c[gr] += 1
                    c["n"] += 1
                    c["teaches_false"] += tf
                total[gr] += 1
                total["n"] += 1
                total["teaches_false"] += tf
        wc = defaultdict(Counter)
        for lab, c in dims["within/cross group"].items():
            wc["within" if lab.startswith("within") else "cross"].update(c)
        dims["within vs cross (all)"] = wc
        report.append(f"\n[{who}] proposals graded: {total['n']}; "
                      + ", ".join(f"{g} {total[g]}" for g in GRADES + ("invalid",) if total[g])
                      + f"; teaches failed {total['teaches_false']}")
        for dim in ("by book", "by target book", "within/cross group", "within vs cross (all)", "by type"):
            table(dim, dims[dim], report)
        out.setdefault("part_a", {})[who] = {"total": dict(total), **{d: {l: dict(c) for l, c in v.items()} for d, v in dims.items()}}
    # calibration
    report.append("\nCALIBRATION (known grade vs grader)")
    for who in graders:
        pairs = [(key[i]["known"], grade_of(matched[who][i])) for i in cals if i in matched[who]]
        if not pairs:
            continue
        exact = sum(a == b for a, b in pairs)
        sn = sum((a == "sound") == (b == "sound") for a, b in pairs)
        report.append(f"  {who}: exact {exact}/{len(pairs)}, sound/not agree {sn}/{len(pairs)}, "
                      f"kappa {fmt_k(kappa([a for a, _ in pairs], [b for _, b in pairs]))}; "
                      + "; ".join(f"{key[i]['a']}->{key[i]['b']} known {key[i]['known']} got {grade_of(matched[who][i])}"
                                  for i in cals if i in matched[who] and key[i]['known'] != grade_of(matched[who][i])))
        out.setdefault("calibration", {})[who] = {"n": len(pairs), "exact": exact, "sound_agree": sn}
    # between graders
    if len(graders) > 1:
        report.append("\nBETWEEN GRADERS (proposed links)")
        for x in range(len(graders)):
            for y in range(x + 1, len(graders)):
                a, b = graders[x], graders[y]
                both = [i for i in props if i in matched[a] and i in matched[b]]
                ga = [grade_of(matched[a][i]) for i in both]
                gb = [grade_of(matched[b][i]) for i in both]
                exact = sum(p == q for p, q in zip(ga, gb))
                sa, sb = [g == "sound" for g in ga], [g == "sound" for g in gb]
                ta = [matched[a][i].get("teaches_holds") is not False for i in both]
                tb = [matched[b][i].get("teaches_holds") is not False for i in both]
                k4, k2, kt = kappa(ga, gb), kappa(sa, sb), kappa(ta, tb)
                report.append(f"  {a} vs {b}: {len(both)} links, exact {exact}/{len(both)}, "
                              f"kappa grade {fmt_k(k4)}, sound/not {fmt_k(k2)}, teaches_holds {fmt_k(kt)}")
                conf = Counter(zip(ga, gb))
                report.append("    pairs: " + ", ".join(f"{p}/{q} {n}" for (p, q), n in sorted(conf.items())))
                out.setdefault("between_graders", {})[f"{a}|{b}"] = {"n": len(both), "exact": exact,
                                                                    "kappa_grade": k4, "kappa_sound": k2,
                                                                    "kappa_teaches": kt}


def present(g, field):
    return bool(g.get(field))


def failed_of(x):
    if not isinstance(x, dict):
        return None
    f = x.get("failed")
    try:
        return int(f) if f is not None else None
    except (TypeError, ValueError):
        return str(f)


def part_b(key, matched, report, out):
    poems = [i for i, k in enumerate(key) if k["part"] == "B"]
    if not poems:
        return
    prop_u = sum(key[i]["ullurai_present"] for i in poems)
    prop_i = sum(key[i]["iraicchi_present"] for i in poems)
    report.append(f"\nPART B: {len(poems)} poems; proposer tagged ullurai {prop_u}, iraicchi {prop_i}")
    graders = sorted(matched)
    res = {}
    for who in graders:
        got = [i for i in poems if i in matched[who]]
        line = f"  {who} ({len(got)} poems):"
        r = {}
        for field in ("ullurai", "iraicchi"):
            p = [key[i][f"{field}_present"] for i in got]
            g = [present(matched[who][i], field) for i in got]
            k = kappa(p, g)
            both = sum(a and b for a, b in zip(p, g))
            line += (f" {field} tagged {sum(g)}, kappa vs proposer {fmt_k(k)} "
                     f"(both {both}, proposer only {sum(a and not b for a, b in zip(p, g))}, "
                     f"grader only {sum(b and not a for a, b in zip(p, g))});")
            r[field] = {"tagged": sum(g), "kappa_vs_proposer": k, "both": both}
        report.append(line)
        res[who] = r
    if len(graders) > 1:
        for x in range(len(graders)):
            for y in range(x + 1, len(graders)):
                a, b = graders[x], graders[y]
                both = [i for i in poems if i in matched[a] and i in matched[b]]
                ks = {f: kappa([present(matched[a][i], f) for i in both], [present(matched[b][i], f) for i in both])
                      for f in ("ullurai", "iraicchi")}
                report.append(f"  {a} vs {b}: ullurai kappa {fmt_k(ks['ullurai'])}, iraicchi kappa {fmt_k(ks['iraicchi'])}")
                res[f"{a}|{b}"] = ks
    report.append("  Rejected candidates by failed condition (proposer-tagged poems in brackets):")
    for who in graders:
        for field in ("ullurai", "iraicchi"):
            c, ct = Counter(), Counter()
            for i in poems:
                g = matched[who].get(i)
                if g is None:
                    continue
                for x in (g.get(f"{field}_candidate_rejected"), g.get(field)):
                    f = failed_of(x)
                    if f is None:
                        continue
                    c[f] += 1
                    if key[i][f"{field}_present"]:
                        ct[f] += 1
            report.append(f"    {who} {field}: " + (", ".join(f"condition {f}: {n} [{ct[f]}]"
                                                              for f, n in sorted(c.items(), key=lambda t: str(t[0])))
                                                    or "none"))
            res.setdefault(who, {}).setdefault(field, {})["rejected_by_condition"] = {str(f): n for f, n in c.items()}
    out["part_b"] = res


def main():
    args = sys.argv[1:]
    jpath = None
    if "--json" in args:
        j = args.index("--json")
        if j + 1 >= len(args):
            usage("--json needs a file")
        jpath = Path(args[j + 1])
        args = args[:j] + args[j + 2:]
    if len(args) != 1:
        usage()
    outdir = Path(args[0])
    if not (outdir / "key.json").exists():
        usage(f"{outdir / 'key.json'} does not exist")
    key, graded, problems = load(outdir)
    if not graded:
        usage(f"no graded files in {outdir / 'graded'}")
    matched = match(key, graded, problems)
    report, out = [f"Graders: {', '.join(sorted(graded))}; packets graded: "
                   + "; ".join(f"{g} {sorted(graded[g])}" for g in sorted(graded))], {}
    part_a(key, matched, report, out)
    part_b(key, matched, report, out)
    if problems:
        report.append("\nPROBLEMS")
        report += ["  " + p for p in problems]
    out["problems"] = problems
    print("\n".join(report))
    if jpath:
        jpath.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
