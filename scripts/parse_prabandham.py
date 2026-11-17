#!/usr/bin/env python3
"""Parse the Nalayira Divya Prabandham into kg/core/prabandham.jsonl.

Sources, all in data/text/:
  pmuni0005_01  pasurams 1-473     Thiruppallandu, Periyalvar Thirumozhi
  pmuni0005_02  pasurams 474-947   Thiruppavai ... Kanni Nun Siruthambu
  pmuni0006_01  pasurams 948-1447  Periya Thirumozhi, pathus 1-5
  pmuni0006_02  pasurams 1448-2031 Periya Thirumozhi, pathus 6-11
  pmuni0007     pasurams 2032-2790 Iyarpa, plus a full Ramanuja Nootrandadi
                                   (misnumbered 2788-2795 and then unnumbered)
  pmuni0008_01  pasurams 2791-3342 Thiruvaimozhi, pathus 1-5
  pmuni0008_02  pasurams 3343-4000 Thiruvaimozhi, pathus 6-10, and Ramanuja
                                   Nootrandadi verses 21-108 only (3913-4000)
  pmuni0517_01/02  Thiruvaimozhi with Kausalya Hart's English translation (modern)

Each pasuram in the base files follows a line holding its traditional number ("13:" or
"948"). The printed numbers are sometimes wrong, so each is checked against the running
count and the numbers that follow it; repairs and dropped duplicates are printed.
Hart is aligned by position over her 1,102 numbered Tamil verses and each pairing is
checked with letter trigrams against the base text.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "data" / "text"
OUT = ROOT / "kg" / "core" / "prabandham.jsonl"
BASE = ["pmuni0005_01", "pmuni0005_02", "pmuni0006_01", "pmuni0006_02",
        "pmuni0007", "pmuni0008_01", "pmuni0008_02"]
HART = ["pmuni0517_01", "pmuni0517_02"]

# (first, last, work, work_ta, alvar, alvar_ta, structure)
# structure: "pathu" = pathu.thirumozhi.verse, "decade" = thirumozhi.verse, None = verse only
WORKS = [
    (1, 12, "Thiruppallandu", "திருப்பல்லாண்டு", "Periyalvar", "பெரியாழ்வார்", None),
    (13, 473, "Periyalvar Thirumozhi", "பெரியாழ்வார் திருமொழி", "Periyalvar", "பெரியாழ்வார்", "pathu"),
    (474, 503, "Thiruppavai", "திருப்பாவை", "Andal", "ஆண்டாள்", None),
    (504, 646, "Nachiyar Thirumozhi", "நாச்சியார் திருமொழி", "Andal", "ஆண்டாள்", "decade"),
    (647, 751, "Perumal Thirumozhi", "பெருமாள் திருமொழி", "Kulasekhara Alvar", "குலசேகராழ்வார்", "decade"),
    (752, 871, "Thiruchanda Viruttam", "திருச்சந்த விருத்தம்", "Thirumazhisai Alvar", "திருமழிசையாழ்வார்", None),
    (872, 916, "Thirumalai", "திருமாலை", "Thondaradippodi Alvar", "தொண்டரடிப்பொடியாழ்வார்", None),
    (917, 926, "Thiruppalliyezhuchi", "திருப்பள்ளியெழுச்சி", "Thondaradippodi Alvar", "தொண்டரடிப்பொடியாழ்வார்", None),
    (927, 936, "Amalanadipiran", "அமலனாதிபிரான்", "Thiruppan Alvar", "திருப்பாணாழ்வார்", None),
    (937, 947, "Kanni Nun Siruthambu", "கண்ணிநுண்சிறுத்தாம்பு", "Madhurakavi Alvar", "மதுரகவியாழ்வார்", None),
    (948, 2031, "Periya Thirumozhi", "பெரிய திருமொழி", "Thirumangai Alvar", "திருமங்கையாழ்வார்", "pathu"),
    (2032, 2051, "Thirukurunthandakam", "திருக்குறுந்தாண்டகம்", "Thirumangai Alvar", "திருமங்கையாழ்வார்", None),
    (2052, 2081, "Thirunedunthandakam", "திருநெடுந்தாண்டகம்", "Thirumangai Alvar", "திருமங்கையாழ்வார்", None),
    (2082, 2181, "Mudhal Thiruvandhadi", "முதல் திருவந்தாதி", "Poigai Alvar", "பொய்கையாழ்வார்", None),
    (2182, 2281, "Irandam Thiruvandhadi", "இரண்டாம் திருவந்தாதி", "Bhoothathalvar", "பூதத்தாழ்வார்", None),
    (2282, 2381, "Moondram Thiruvandhadi", "மூன்றாம் திருவந்தாதி", "Peyalvar", "பேயாழ்வார்", None),
    (2382, 2477, "Nanmugan Thiruvandhadi", "நான்முகன் திருவந்தாதி", "Thirumazhisai Alvar", "திருமழிசையாழ்வார்", None),
    (2478, 2577, "Thiruviruttam", "திருவிருத்தம்", "Nammalvar", "நம்மாழ்வார்", None),
    (2578, 2584, "Thiruvasiriyam", "திருவாசிரியம்", "Nammalvar", "நம்மாழ்வார்", None),
    (2585, 2671, "Periya Thiruvandhadi", "பெரிய திருவந்தாதி", "Nammalvar", "நம்மாழ்வார்", None),
    (2672, 2672, "Thiruvezhukutrirukkai", "திருவெழுகூற்றிருக்கை", "Thirumangai Alvar", "திருமங்கையாழ்வார்", None),
    (2673, 2712, "Siriya Thirumadal", "சிறிய திருமடல்", "Thirumangai Alvar", "திருமங்கையாழ்வார்", None),
    (2713, 2790, "Periya Thirumadal", "பெரிய திருமடல்", "Thirumangai Alvar", "திருமங்கையாழ்வார்", None),
    (2791, 3892, "Thiruvaimozhi", "திருவாய்மொழி", "Nammalvar", "நம்மாழ்வார்", "pathu"),
    (3893, 4000, "Ramanuja Nootrandadi", "இராமாநுச நூற்றந்தாதி", "Thiruvarangathu Amudhanar", "திருவரங்கத்து அமுதனார்", None),
]
AYIRAM = [(947, "Mudhalayiram"), (2081, "Periya Thirumozhi (Irandam Ayiram)"),
          (2790, "Iyarpa"), (3892, "Thiruvaimozhi (Nalam Ayiram)"), (4000, "Iyarpa")]

MARKER = re.compile(r"^\s*(\d(?:[\d ]{0,4}\d)?)\s*:?\s*(?:பெரிய திருமொழி)?\s*$")
TAIL = re.compile(r"^(.*?)[\s,]*([\d().\s-]*\d[\d().\s-]*)$")
STOP = re.compile(r"^-{3,}|திருவடிகளே|^ஸ்ரீ")
CONTINUOUS = set(range(2578, 2585)) | {2672}       # long poems printed with blank lines inside
NON_TAMIL = re.compile(r"[^஀-௿]")
TAMIL = re.compile(r"[஀-௿]")
MIN_MATCH = 0.30
problems = []


def body(name):
    text = (TEXT / f"{name}.txt").read_text(encoding="utf-8")
    return text.split("=== BODY ===", 1)[1].split("=== FOOTER ===", 1)[0]


def grams(text):
    letters = NON_TAMIL.sub("", text)
    return {letters[i:i + 3] for i in range(len(letters) - 2)}


def similarity(a, b):
    return len(a & b) / (len(a | b) or 1)


def word_overlap(a, b):
    wa, wb = set(a.lower().split()), set(b.lower().split())
    return len(wa & wb) / (len(wa | wb) or 1)


def work_of(n):
    return next(w for w in WORKS if w[0] <= n <= w[1])


def split_tail(lines, source=None, madal=False):
    """Strip the printed local number ('1.1.1', '(2) 5.', '(45)', '4-10-8') from the end of the
    verse. A metre heading printed straight after the number, with no blank line, is dropped."""
    lines = list(lines)
    if not madal and len(lines) >= 2 and not re.search(r"\d", lines[-1]) and re.search(r"\d\.?\)?\s*$", lines[-2]):
        if source:
            problems.append(f"{source}: heading '{lines[-1]}' glued to the end of the verse, dropped")
        lines = lines[:-1]
    if not lines:
        return lines, None
    m = TAIL.match(lines[-1])
    if not m:
        return lines, None
    tail = re.sub(r"\s+", " ", m.group(2)).strip()
    text = m.group(1).strip()
    if tail.startswith("."):  # the verse's own full stop
        text, tail = text + ".", tail.lstrip(". ")
    if not re.search(r"\d", tail):
        return lines, None
    if text:
        return lines[:-1] + [text], tail
    return lines[:-1], tail  # the number stood on its own line


def raw_units():
    """Every numbered block in the base files, in file order, with the headings before it."""
    units = []
    for name in BASE:
        lines = body(name).split("\n")
        heads, i = [], 0
        while i < len(lines):
            s = lines[i].strip()
            if name == "pmuni0007" and s.startswith("#") and "நூற்றந்தாதி" in s:
                break  # Ramanuja Nootrandadi, read separately
            m = MARKER.match(s)
            if not m:
                if s:
                    heads.append(s)
                i += 1
                continue
            label = int(m.group(1).replace(" ", ""))
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            text = []
            madal = name == "pmuni0007" and label == 2712
            while j < len(lines):
                t = lines[j].strip()
                if MARKER.match(t) or lines[j].startswith("#") or (t and STOP.search(t)):
                    break
                if not t:
                    nxt = next((x.strip() for x in lines[j + 1:j + 4] if x.strip()), "")
                    if not (madal or label in CONTINUOUS) or MARKER.match(nxt) or STOP.search(nxt):
                        break
                else:
                    text.extend(x.strip() for x in t.split("< br>"))  # one HTML break in pmuni0006_02
                j += 1
            units.append({"file": name, "line": i + 1 + header_offset(name), "label": label,
                          "heads": heads, "lines": text, "madal": madal})
            heads, i = [], j
    return units


_offsets = {}


def header_offset(name):
    """Line number of '=== BODY ===' in the file, so reported lines match the file."""
    if name not in _offsets:
        raw = (TEXT / f"{name}.txt").read_text(encoding="utf-8").split("\n")
        _offsets[name] = next(k for k, l in enumerate(raw) if l.strip() == "=== BODY ===")
    return _offsets[name]


def number_units(units):
    """Assign traditional numbers; repair misprinted labels, drop printed duplicates."""
    out, prev = [], 0
    for k, u in enumerate(units):
        label, expected = u["label"], prev + 1
        if u["madal"]:
            u["number"], u["number_end"] = 2673, 2712
            problems.append(f"{u['file']}:{u['line']} Siriya Thirumadal printed as one block labelled "
                            f"2712; kept as one record spanning 2673-2712")
            out.append(u)
            prev = 2712
            continue
        if label == expected:
            u["number"] = label
        elif out and similarity(grams(" ".join(u["lines"])), grams(" ".join(out[-1]["lines"]))) > 0.9:
            problems.append(f"{u['file']}:{u['line']} label {label}: duplicate of {out[-1]['number']}, dropped")
            continue
        else:
            ahead = [x["label"] for x in units[k + 1:k + 4]]
            if any(a == expected + d for d, a in enumerate(ahead, 1)):
                u["number"] = expected
                problems.append(f"{u['file']}:{u['line']} label {label} repaired to {expected}")
            else:
                u["number"] = label
                problems.append(f"{u['file']}:{u['line']} jump from {prev} to {label}: "
                                f"{label - expected} pasurams missing here")
        out.append(u)
        prev = u["number"]
    return out


def nootrandadi_0007():
    """pmuni0007's Ramanuja Nootrandadi: verses end with their own number 1-108."""
    text = body("pmuni0007")
    start = text.index("இராமாநுச நூற்றந்தாதி")
    lines = text[start:].split("\n")
    verses, block, first = {}, [], None
    off = header_offset("pmuni0007") + text[:start].count("\n")
    for k, l in enumerate(lines + [""]):
        s = l.strip()
        if s and not MARKER.match(s) and not STOP.search(s):
            first = first or k
            block.append(s)
            continue
        if block:
            body_lines, tail = split_tail(block)
            m = re.search(r"(\d+)\.?$", tail or "")
            if m and len(block) >= 4:
                n = int(m.group(1))
                if n == len(verses) + 1:
                    verses[n] = {"lines": [b.lstrip("*").strip() for b in body_lines[-4:]],
                                 "tail": tail, "line": off + first + 1}
        block, first = [], None
    return verses


def printed_ref(r):
    """The last number group of the printed tail: '(2) 1.1.2' -> [1, 1, 2], '(45)' -> [45]."""
    tail = re.sub(r"\s*([.-])\s*", ".", r.get("printed_ref") or "")
    tokens = re.findall(r"\d+(?:\.\d+)*", tail)
    return [int(x) for x in tokens[-1].split(".")] if tokens else []


def structure(records):
    """Pathu / thirumozhi / verse for the works that have them, from headings and printed refs."""
    by_work = {}
    for r in records:
        first, last, work, *_ = work_of(r["number"])
        r["verse_in_work"] = r["number"] - first + 1
        by_work.setdefault(work, []).append(r)
    for work, rs in by_work.items():
        kind = work_of(rs[0]["number"])[6]
        if kind is None:
            for r in rs:
                r.pop("_heads")
                r["verse"] = r["verse_in_work"]
            continue
        if work in ("Periyalvar Thirumozhi", "Nachiyar Thirumozhi"):
            heading_structure(work, rs)
        else:
            ref_structure(work, kind, rs)


def heading_structure(work, rs):
    """Periyalvar and Nachiyar print pathu and thirumozhi headings and a local verse number."""
    pathu, tm, v = (0 if work == "Periyalvar Thirumozhi" else None), 0, 0
    for r in rs:
        for h in r.pop("_heads"):
            if work == "Periyalvar Thirumozhi":
                if re.search(r"பத்து$", h) and len(h) < 16:
                    pathu, tm = pathu + 1, 0
                if re.search(r"திருமொழி\s*-", h):
                    tm, v = tm + 1, 0
                    r["decade_title"] = h.split("-", 1)[1].strip(" -")
            else:
                hm = re.match(r"^(\d+)\s*:\s*(.+)$", h)
                if hm:
                    tm, v = tm + 1, 0
                    r["decade_title"] = hm.group(2).strip(" .")
                    if int(hm.group(1)) != tm:
                        problems.append(f"{r['source']}: heading {hm.group(1)} is thirumozhi {tm} by position")
        v += 1
        r["pathu"], r["decade"], r["verse"] = pathu, tm, v
        ref = printed_ref(r)
        if ref and ref[-1] != v:
            problems.append(f"{r['source']} pasuram {r['number']}: printed verse {ref[-1]}, position gives "
                            f"{'.'.join(str(x) for x in (pathu, tm, v) if x is not None)}")


def ref_structure(work, kind, rs):
    """Periya Thirumozhi, Thiruvaimozhi (pathu.thirumozhi.verse) and Perumal Thirumozhi
    (thirumozhi.verse) print their place after each pasuram. Fill gaps from neighbours,
    then check that the sequence only ever steps verse+1 or opens a new decade at verse 1."""
    size = 3 if kind == "pathu" else 2
    refs = []
    for r in rs:
        ref = printed_ref(r)
        refs.append(ref if len(ref) == size else None)
    for i in range(len(rs) - 1, -1, -1):  # backwards: one before (p, t, k>1) is (p, t, k-1)
        if refs[i] is None and i + 1 < len(rs) and refs[i + 1] and refs[i + 1][-1] > 1:
            refs[i] = refs[i + 1][:-1] + [refs[i + 1][-1] - 1]
            problems.append(f"{rs[i]['source']} pasuram {rs[i]['number']}: no printed ref, "
                            f"inferred {'.'.join(map(str, refs[i]))}")
    for i in range(len(rs)):
        if refs[i] is None:
            refs[i] = (refs[i - 1][:-1] + [refs[i - 1][-1] + 1]) if i else [1] * size
            problems.append(f"{rs[i]['source']} pasuram {rs[i]['number']}: no printed ref, "
                            f"inferred {'.'.join(map(str, refs[i]))}")
    prev = None
    for r, ref in zip(rs, refs):
        r.pop("_heads")
        if prev is not None:
            steps = [prev[:-1] + [prev[-1] + 1], prev[:-2] + [prev[-2] + 1, 1]]
            if size == 3:
                steps.append([prev[0] + 1, 1, 1])
            if ref not in steps:
                new_pathu = size == 3 and ref[0] == prev[0] + 1 and ref[1] == 1
                fixed = steps[0] if ref[-1] != 1 else (steps[2] if new_pathu else steps[1])
                problems.append(f"{r['source']} pasuram {r['number']}: printed ref {'.'.join(map(str, ref))} "
                                f"does not follow {'.'.join(map(str, prev))}; taken as {'.'.join(map(str, fixed))}")
                ref = fixed
        r["pathu"] = ref[0] if size == 3 else None
        r["decade"], r["verse"] = ref[-2], ref[-1]
        prev = ref


def hart(records):
    """Hart prints 'NNNN Tamil...' then 'NNNN. English...'. Align her Tamil blocks by position."""
    blocks = []
    for name in HART:
        mode = None
        for k, l in enumerate(body(name).split("\n")):
            s = l.strip()
            if re.match(r"^\d{4}\s+[஀-௿]", s):
                blocks.append({"label": int(s[:4]), "tamil": [s[4:].strip()], "english": [],
                               "src": f"{name}:{k + 1 + header_offset(name)}"})
                mode = "tamil"
            elif not s or mode is None:
                continue
            elif TAMIL.search(s):
                if mode == "tamil":
                    blocks[-1]["tamil"].append(s)
                else:
                    mode = None
            elif s.startswith("#") or s.startswith("---"):
                mode = None  # headings, '--- continued in part 2 ---', '--- SUBHAM ...'
            else:
                mode = "english"
                blocks[-1]["english"].append(s)
    tvm = [r for r in records if 2791 <= r["number"] <= 3892]
    aligned = {}
    if len(blocks) != len(tvm):
        problems.append(f"Hart: {len(blocks)} Tamil blocks against {len(tvm)} Thiruvaimozhi pasurams")
    tg = [grams(" ".join(r["tamil"])) for r in tvm]
    for k, (b, r) in enumerate(zip(blocks, tvm)):
        bg = grams(" ".join(b["tamil"]))
        score = similarity(bg, tg[k])
        near = max(similarity(bg, tg[j]) for j in range(max(0, k - 2), min(len(tvm), k + 3)) if j != k)
        if score < MIN_MATCH and score > near:
            problems.append(f"Hart {b['src']}: low match {score:.2f} with pasuram {r['number']} but better than "
                            f"its neighbours ({near:.2f}); kept")
            score = MIN_MATCH
        if b["label"] != r["number"]:
            problems.append(f"Hart {b['src']}: Tamil labelled {b['label']}, is pasuram {r['number']} by position "
                            f"(trigram match {score:.2f})")
        if score < MIN_MATCH:
            problems.append(f"Hart {b['src']}: weak match {score:.2f} with pasuram {r['number']}, left null")
            continue
        english = re.sub(r"^\d{4}\s*\.\s*", "", " ".join(b["english"])).strip()
        if not english:
            problems.append(f"Hart {b['src']}: no English after pasuram {r['number']}")
            continue
        head = re.match(r"^(\d{4})\s*\.", b["english"][0]) if b["english"] else None
        prev_english = aligned.get(r["number"] - 1)
        if prev_english and word_overlap(english, prev_english) > 0.8:
            problems.append(f"Hart {b['src']}: English after pasuram {r['number']} repeats the translation of "
                            f"{r['number'] - 1}; left null")
            continue
        if head and int(head.group(1)) != r["number"]:
            problems.append(f"Hart {b['src']}: English labelled {head.group(1)}, aligned to {r['number']}")
        aligned[r["number"]] = english
        r["_hart_score"] = score
    return aligned


def main():
    units = number_units(raw_units())
    records = []
    for u in units:
        lines, tail = split_tail(u["lines"], f"{u['file']}:{u['line']}", u["madal"])
        if u["madal"]:
            couplets, cur = [], []
            for l in u["lines"]:
                m = re.match(r"^(.*?)\s+(\d+)$", l)
                cur.append(m.group(1) if m else l)
                if m:
                    couplets.append(cur)
                    cur = []
            if cur:
                couplets.append(cur)
            lines, tail = [x for c in couplets for x in c], None
            u["numbered"] = sum(1 for l in u["lines"] if re.search(r"\s\d+$", l))
        rec = {"number": u["number"], "tamil": [l for l in lines if l], "printed_ref": tail,
               "source": f"{u['file']}:{u['line']}", "_heads": u["heads"]}
        if "number_end" in u:
            rec["number_end"] = u["number_end"]
            rec["note"] = (f"Printed as one poem of {u['numbered']} numbered couplets (kannis; number 44 is "
                           f"printed twice) and a closing line; the source does not mark the 40 traditional "
                           f"pasuram divisions 2673-2712.")
        records.append(rec)
    have = {r["number"] for r in records}
    rn = nootrandadi_0007()
    missing_rn = [n for n in range(1, 109) if n not in rn]
    if missing_rn:
        problems.append(f"pmuni0007 Ramanuja Nootrandadi: verses not found {missing_rn}")
    for n, v in rn.items():
        num = 3892 + n
        if num in have:
            continue
        records.append({"number": num, "tamil": v["lines"], "printed_ref": v["tail"],
                        "source": f"pmuni0007:{v['line']}", "_heads": [],
                        "note": "Taken from pmuni0007, whose numbering of this work is wrong (2788-2795, "
                                "then none); pmuni0008_02 lacks verses 1-20."})
        problems.append(f"pasuram {num} (Nootrandadi {n}) taken from pmuni0007:{v['line']}")
    records.sort(key=lambda r: r["number"])
    structure(records)
    translations = hart(records)
    covered = set()
    for r in records:
        covered |= set(range(r["number"], r.get("number_end", r["number"]) + 1))
    missing = sorted(set(range(1, 4001)) - covered)
    numbers = [r["number"] for r in records]
    doubled = sorted({n for n in numbers if numbers.count(n) > 1})
    order_ok = numbers == sorted(numbers)
    with open(OUT, "w", encoding="utf-8") as out:
        for r in records:
            first, last, work, work_ta, alvar, alvar_ta, kind = work_of(r["number"])
            rec = {"id": f"prabandham:{r['number']}", "number": r["number"]}
            if "number_end" in r:
                rec["number_end"] = r["number_end"]
            rec |= {"ayiram": next(a for end, a in AYIRAM if r["number"] <= end),
                    "work": work, "work_ta": work_ta, "alvar": alvar, "alvar_ta": alvar_ta,
                    "pathu": r.get("pathu"), "decade": r.get("decade"),
                    "decade_title": r.get("decade_title"), "verse": r["verse"],
                    "verse_in_work": r["verse_in_work"], "tamil": r["tamil"],
                    "printed_ref": r["printed_ref"], "source": r["source"],
                    "hart": translations.get(r["number"])}
            if r.get("note"):
                rec["note"] = r["note"]
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
    for p in problems:
        print("CHECK", p)
    short = [r["number"] for r in records if len(r["tamil"]) < 2]
    print(f"records={len(records)} pasurams_covered={len(covered)} missing={missing} doubled={doubled} "
          f"order_ok={order_ok} short={short} hart={len(translations)}")
    counts = {}
    for r in records:
        w = work_of(r["number"])[2]
        counts[w] = counts.get(w, 0) + 1
    for w in WORKS:
        print(f"  {w[2]}: {counts.get(w[2], 0)} records, traditional {w[1] - w[0] + 1}")


if __name__ == "__main__":
    main()
