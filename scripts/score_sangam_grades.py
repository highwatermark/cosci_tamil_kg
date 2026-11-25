"""Score blind grades of packets made by scripts/make_sangam_packets.py.

Usage (from the repository root):
  python3 -I scripts/score_sangam_grades.py OUTDIR [--json FILE]

Reads OUTDIR/key.json and every OUTDIR/graded/packet_N.<grader>.json. If OUTDIR has no key.json but
its subdirectories do (one per grader brief: sangam, ethics, epic), each is scored in turn. A graded
file is the object {"links": [...], "poems"|"verses"|"units": [...]} the packet asks for; a bare
array, or an object of several arrays, is also accepted (an item with "grade" is a link, an item
with "id" is a Part B item).

Part A (every brief): grades of the proposed links per grader and pooled, by book, by target book,
within-group against cross-group and by type; how often `teaches` held, and `list_adds` (ethics) and
`gains` (epic bridges); agreement with the calibration links' known grades; agreement between
graders (exact, and Cohen's kappa on the grade, sound/not sound and teaches_holds).
Part B, per field set, between the proposer and each grader and between graders:
  akam       kappa on ullurai_present and iraicchi_present; rejected candidates by failed condition
  ethics     kappa on domain, norm present, count word given and Pazhamozhi story kind; Jaccard on the
             item sets, the norm kinds and the proverb lines; item counts against the expected ones
  narrative  kappa on "states a claim"; Jaccard on the claim sets (matched by line, within CLAIM_SLACK
             lines) and the echo sets (by couplet); kappa on school and stance of the matched claims
--json FILE also writes the numbers as JSON.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

GRADES = ("sound", "weak", "forced", "wrong")
CLAIM_SLACK = 2
# docs/ethics-grader-brief.md, "items": the expected counts per work
ITEM_COUNTS = {"thirikadugam": {3}, "nanmanikkadigai": {4}, "innaa_narpathu": {4}, "iniyavai_narpathu": {3, 4},
               "sirupanchamoolam": {5, 6}, "elathi": {6, 5}, "muthumozhikkanchi": {1}}


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
        return key, {}, []
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
                if "list_adds" in k:
                    total["list_adds_n"] += 1
                    total["list_adds_false"] += g.get("list_adds_holds") is False
                if k.get("bridge"):
                    total["gains_n"] += 1
                    total["gains_false"] += g.get("gains_holds") is False
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
                      + f"; teaches failed {total['teaches_false']}"
                      + (f"; list_adds failed {total['list_adds_false']}/{total['list_adds_n']}" if total["list_adds_n"] else "")
                      + (f"; gains failed {total['gains_false']}/{total['gains_n']} bridges" if total["gains_n"] else ""))
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
    kinds = defaultdict(list)
    for i, k in enumerate(key):
        if k["part"] == "B":
            kinds[k.get("fieldset", "akam")].append(i)
    for kind, items in kinds.items():
        {"akam": part_b_akam, "ethics": part_b_ethics, "narrative": part_b_narrative}[kind](key, items, matched, report, out)


def part_b_akam(key, poems, matched, report, out):
    if not poems:
        return
    prop_u = sum(key[i]["ullurai_present"] for i in poems)
    prop_i = sum(key[i]["iraicchi_present"] for i in poems)
    report.append(f"\nPART B (akam): {len(poems)} poems; proposer tagged ullurai {prop_u}, iraicchi {prop_i}")
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



# ---- Part B for the ethics and narrative field sets ----

def tamil_only(text):
    return re.sub(r"[^\u0B80-\u0BFF]", "", text if isinstance(text, str) else "")


def jaccard(m, nx, ny):
    u = nx + ny - m
    return None if u == 0 else m / u


def fmt_j(j):
    return "n/a" if j is None else f"{j:.2f}"


def as_int(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None


def sources(key, items, matched):
    """{source name: {key index: tags}}: the proposer from key.json, each grader from its graded file."""
    src = {"proposer": {i: key[i].get("tags") or {} for i in items}}
    for g in sorted(matched):
        src[g] = {i: matched[g][i] for i in items if i in matched[g] and isinstance(matched[g][i], dict)}
    return src


def pairs_of(names):
    """proposer vs each grader, then grader vs grader."""
    graders = [n for n in names if n != "proposer"]
    out = [("proposer", g) for g in graders]
    out += [(graders[x], graders[y]) for x in range(len(graders)) for y in range(x + 1, len(graders))]
    return out


def item_list(t):
    """An ethics tag's items as [(tamil form, line)], or None."""
    its = t.get("items")
    if not isinstance(its, list):
        return None
    out = []
    for it in its:
        if isinstance(it, (list, tuple)) and it:
            out.append((tamil_only(str(it[0])), as_int(it[1]) if len(it) > 1 else None))
        elif isinstance(it, dict):
            out.append((tamil_only(str(it.get("thing") or it.get("form") or "")), as_int(it.get("line"))))
    return out


def same_item(p, q):
    """Two items are one when they are on the same line (or the next, since a thing may run on) and
    their first Tamil letters agree (the shorter's first four, or all of it if shorter)."""
    (fp, lp), (fq, lq) = p, q
    if lp is None or lq is None or abs(lp - lq) > 1 or not fp or not fq:
        return False
    n = min(4, len(fp), len(fq))
    return fp[:n] == fq[:n]


def match_count(xs, ys, same):
    """Greedy one-to-one matching; returns the matched pairs."""
    free, pairs = list(ys), []
    for x in xs:
        y = next((y for y in free if same(x, y)), None)
        if y is not None:
            free.remove(y)
            pairs.append((x, y))
    return pairs


def norm_kinds(t):
    n = t.get("norm")
    if not isinstance(n, dict):
        return None
    return {str(k) for k in n.get("kinds") or []}


def pz_of(t):
    pz = t.get("pazhamozhi")
    return pz if isinstance(pz, dict) else None


def part_b_ethics(key, items, matched, report, out):
    src = sources(key, items, matched)
    report.append(f"\nPART B (ethics): {len(items)} verses")
    res = {"per_source": {}, "pairs": {}}
    for name, tags in src.items():
        dom = Counter(str(t.get("domain")) for t in tags.values())
        nk = Counter(k for t in tags.values() for k in (norm_kinds(t) or ()))
        nn = sum(1 for t in tags.values() if norm_kinds(t) is not None)
        off = [key[i]["id"] for i, t in tags.items()
               if key[i]["book"] in ITEM_COUNTS and item_list(t) is not None and len(item_list(t)) not in ITEM_COUNTS[key[i]["book"]]]
        report.append(f"  {name} ({len(tags)} verses): domain " + ", ".join(f"{d} {n}" for d, n in sorted(dom.items()))
                      + f"; norm {nn} (" + ", ".join(f"{k} {n}" for k, n in sorted(nk.items())) + ")"
                      + f"; item counts off the expected {len(off)}" + (f" ({', '.join(off)})" if off else ""))
        res["per_source"][name] = {"domain": dict(dom), "norm": nn, "norm_kinds": dict(nk), "item_count_off": off}
    for x, y in pairs_of(src):
        both = [i for i in items if i in src[x] and i in src[y]]
        if not both:
            continue
        X, Y = src[x], src[y]
        r = {"n": len(both)}
        r["kappa_domain"] = kappa([str(X[i].get("domain")) for i in both], [str(Y[i].get("domain")) for i in both])
        r["agree_domain"] = sum(str(X[i].get("domain")) == str(Y[i].get("domain")) for i in both)
        r["kappa_norm"] = kappa([norm_kinds(X[i]) is not None for i in both], [norm_kinds(Y[i]) is not None for i in both])
        m = nx = ny = 0
        for i in both:
            a, b = norm_kinds(X[i]) or set(), norm_kinds(Y[i]) or set()
            m, nx, ny = m + len(a & b), nx + len(a), ny + len(b)
        r["jaccard_norm_kinds"] = jaccard(m, nx, ny)
        m = nx = ny = cnt_eq = cnt_n = 0
        for i in both:
            a, b = item_list(X[i]), item_list(Y[i])
            if a is None and b is None:
                continue
            a, b = a or [], b or []
            m, nx, ny = m + len(match_count(a, b, same_item)), nx + len(a), ny + len(b)
            cnt_n += 1
            cnt_eq += len(a) == len(b)
        r["jaccard_items"] = jaccard(m, nx, ny)
        r["item_count_agree"] = f"{cnt_eq}/{cnt_n}"
        cw = lambda t: bool(tamil_only(t.get("count_word")))
        r["kappa_count_word"] = kappa([cw(X[i]) for i in both], [cw(Y[i]) for i in both])
        pzb = [i for i in both if pz_of(X[i]) or pz_of(Y[i])]
        line = ""
        if pzb:
            kx = [str((pz_of(X[i]) or {}).get("kind")) for i in pzb]
            ky = [str((pz_of(Y[i]) or {}).get("kind")) for i in pzb]
            r["kappa_story_kind"] = kappa(kx, ky)
            m = nx = ny = 0
            for i in pzb:
                a = {as_int(l) for l in (pz_of(X[i]) or {}).get("proverb_lines") or []}
                b = {as_int(l) for l in (pz_of(Y[i]) or {}).get("proverb_lines") or []}
                m, nx, ny = m + len(a & b), nx + len(a), ny + len(b)
            r["jaccard_proverb_lines"] = jaccard(m, nx, ny)
            who = lambda t: tamil_only((pz_of(t) or {}).get("who"))
            r["who_agree"] = sum((not who(X[i]) and not who(Y[i])) or (bool(who(X[i])) and bool(who(Y[i]))
                                 and (who(X[i]) in who(Y[i]) or who(Y[i]) in who(X[i]))) for i in pzb)
            line = (f"; Pazhamozhi ({len(pzb)}): story kind kappa {fmt_k(r['kappa_story_kind'])}, proverb lines "
                    f"Jaccard {fmt_j(r['jaccard_proverb_lines'])}, who agree {r['who_agree']}/{len(pzb)}")
        report.append(f"  {x} vs {y} ({len(both)}): domain kappa {fmt_k(r['kappa_domain'])} (agree {r['agree_domain']}), "
                      f"norm kappa {fmt_k(r['kappa_norm'])}, norm kinds Jaccard {fmt_j(r['jaccard_norm_kinds'])}, "
                      f"items Jaccard {fmt_j(r['jaccard_items'])} (counts agree {r['item_count_agree']}), "
                      f"count word kappa {fmt_k(r['kappa_count_word'])}" + line)
        res["pairs"][f"{x}|{y}"] = r
    out["part_b_ethics"] = res


def claim_list(t):
    cs = t.get("claims")
    return [c for c in cs if isinstance(c, dict)] if isinstance(cs, list) else []


def echo_list(t):
    es = t.get("echoes")
    return [e for e in es if isinstance(e, dict)] if isinstance(es, list) else []


def same_claim(p, q):
    lp, lq = as_int(p.get("line")), as_int(q.get("line"))
    return lp is not None and lq is not None and abs(lp - lq) <= CLAIM_SLACK


def part_b_narrative(key, items, matched, report, out):
    src = sources(key, items, matched)
    report.append(f"\nPART B (narrative): {len(items)} units")
    res = {"per_source": {}, "pairs": {}}
    for name, tags in src.items():
        cl = [c for t in tags.values() for c in claim_list(t)]
        sch, st = Counter(str(c.get("school")) for c in cl), Counter(str(c.get("stance")) for c in cl)
        ec = [e for t in tags.values() for e in echo_list(t)]
        rej = sum(len(t.get("claims_rejected") or []) for t in tags.values() if isinstance(t.get("claims_rejected"), list))
        report.append(f"  {name} ({len(tags)} units): {len(cl)} claims; school " + ", ".join(f"{k} {n}" for k, n in sorted(sch.items()))
                      + "; stance " + ", ".join(f"{k} {n}" for k, n in sorted(st.items()))
                      + f"; echoes {len(ec)}" + (f" ({', '.join(str(e.get('b')) for e in ec)})" if ec else "")
                      + (f"; rejected candidates {rej}" if name != "proposer" else ""))
        res["per_source"][name] = {"claims": len(cl), "school": dict(sch), "stance": dict(st), "echoes": len(ec),
                                   "rejected": rej if name != "proposer" else None}
    for x, y in pairs_of(src):
        both = [i for i in items if i in src[x] and i in src[y]]
        if not both:
            continue
        X, Y = src[x], src[y]
        r = {"n": len(both)}
        r["kappa_has_claim"] = kappa([bool(claim_list(X[i])) for i in both], [bool(claim_list(Y[i])) for i in both])
        m = nx = ny = 0
        sx, sy, tx, ty = [], [], [], []
        for i in both:
            a, b = claim_list(X[i]), claim_list(Y[i])
            # prefer pairs that also agree on school, then any within the line slack
            pr = match_count(a, b, lambda p, q: same_claim(p, q) and p.get("school") == q.get("school"))
            rest_a = [c for c in a if all(c is not p for p, _ in pr)]
            rest_b = [c for c in b if all(c is not q for _, q in pr)]
            pr += match_count(rest_a, rest_b, same_claim)
            m, nx, ny = m + len(pr), nx + len(a), ny + len(b)
            for p, q in pr:
                sx.append(str(p.get("school"))); sy.append(str(q.get("school")))
                tx.append(str(p.get("stance"))); ty.append(str(q.get("stance")))
        r.update({"claims_matched": m, "claims_x": nx, "claims_y": ny, "jaccard_claims": jaccard(m, nx, ny),
                  "kappa_school": kappa(sx, sy), "kappa_stance": kappa(tx, ty),
                  "agree_school": sum(a == b for a, b in zip(sx, sy)), "agree_stance": sum(a == b for a, b in zip(tx, ty))})
        m = nx = ny = 0
        kx, ky = [], []
        for i in both:
            a = [e for e in echo_list(X[i]) if e.get("b")]
            b = [e for e in echo_list(Y[i]) if e.get("b")]
            pr = match_count(a, b, lambda p, q: str(p.get("b")) == str(q.get("b")))
            m, nx, ny = m + len(pr), nx + len(a), ny + len(b)
            kx += [str(p.get("kind")) for p, _ in pr]
            ky += [str(q.get("kind")) for _, q in pr]
        r.update({"echoes_matched": m, "jaccard_echoes": jaccard(m, nx, ny), "kappa_echo_kind": kappa(kx, ky)})
        report.append(f"  {x} vs {y} ({len(both)}): has-claim kappa {fmt_k(r['kappa_has_claim'])}; claims {r['claims_x']} vs "
                      f"{r['claims_y']}, matched {r['claims_matched']}, Jaccard {fmt_j(r['jaccard_claims'])}; on matched: school "
                      f"kappa {fmt_k(r['kappa_school'])} (agree {r['agree_school']}), stance kappa {fmt_k(r['kappa_stance'])} "
                      f"(agree {r['agree_stance']}); echoes Jaccard {fmt_j(r['jaccard_echoes'])} (matched {r['echoes_matched']}), "
                      f"kind kappa {fmt_k(r['kappa_echo_kind'])}")
        res["pairs"][f"{x}|{y}"] = r
    out["part_b_narrative"] = res


def score(outdir):
    key, graded, problems = load(outdir)
    if not graded:
        return None, None
    matched = match(key, graded, problems)
    brief = next((k.get("brief") for k in key if k.get("brief")), "sangam")
    report, out = [f"[{brief}] {outdir}", f"Graders: {', '.join(sorted(graded))}; packets graded: "
                   + "; ".join(f"{g} {sorted(graded[g])}" for g in sorted(graded))], {"brief": brief}
    part_a(key, matched, report, out)
    part_b(key, matched, report, out)
    if problems:
        report.append("\nPROBLEMS")
        report += ["  " + p for p in problems]
    out["problems"] = problems
    return report, out


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
    if (outdir / "key.json").exists():
        dirs = [outdir]
    else:
        dirs = sorted(p.parent for p in outdir.glob("*/key.json"))
        if not dirs:
            usage(f"{outdir / 'key.json'} does not exist, nor does any {outdir}/*/key.json")
    reports, outs = [], {}
    for d in dirs:
        report, out = score(d)
        if report is None:
            if len(dirs) == 1:
                usage(f"no graded files in {d / 'graded'}")
            reports.append(f"[{d.name}] no graded files yet")
            continue
        reports.append("\n".join(report))
        outs[d.name] = out
    print("\n\n".join(reports))
    if jpath:
        jpath.write_text(json.dumps(outs[dirs[0].name] if len(dirs) == 1 else outs, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
