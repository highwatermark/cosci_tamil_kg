"""Run the complete corpus × register lexical census and save its audit trail.

Run from any directory: python3 -I scripts/science_census.py
All outputs are deterministic given identical source data and rule files.
"""
import csv
import gzip
import hashlib
import io
import json
import re
import runpy
import sys
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
common = runpy.run_path(str(HERE / "science_inquiry.py"))
units, fold, rows, KG = (common[k] for k in ("units", "folded", "rows", "KG"))
OUT = KG / "science/consciousness"
RULEFILE = OUT / "census_rules.json"


def bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n")


def write_report(result):
    t = result["totals"]
    books = result["books"]
    passed = result["calibration"]["passed"]
    controls = result["calibration"]["controls"]
    any_count, nearby = sum(t["any"]), sum(t["local"])
    active = sum(bool(n) for n in t["local"])
    headline = f"""# How much of the corpus has been compared?

The scan tested {t["units"]:,} Tamil units in {len(books)} corpus groups against every one of {len(result["claim_order"])} registered comparisons. Of the {result["pair_count"]:,} resulting pairs, {any_count:,} met both Tamil vocabulary conditions somewhere in the unit. Requiring the clues to occur within three consecutive printed lines reduced that count to {nearby:,} pairs across {t["with_local"]:,} distinct units. {active} comparison rules returned a nearby candidate.

## What the scan found

The largest nearby count belongs to the rule for Gabor Maté, which uses a broad vocabulary. The number describes its retrieval behavior. Reading those passages for specific relations, including counterexamples, is still open. Generic words for distress or the body can match multiple modern claims. A match against a quantum or consciousness entry establishes only that its chosen Tamil clues co-occur.

The nearby rule recovered {passed["local"]} of {passed["total"]} previously accepted links and matched {controls["local"]} of {controls["total"]} historical controls. The recovered pair connected siddhar:thiruvalluvar-njanam:2.17 to finding:aging-hallmarks. The missing links expose the limits of literal fragments, morphology, metaphor and line boundaries. The earlier grades came from a selected set, and the comparison vocabulary was designed with knowledge of the project. These counts cannot establish translation accuracy, precision on new candidates or an unbiased recall estimate.

## How to read the combinations

The six theme families cover matter and scale, life and environment, body and regulation, experience and identity, ethics and practice, and inquiry and measurement. Every unit was tested for all 63 nonempty subsets. Counts are inclusive, so a unit matching three themes also contributes to its three pairs. {t["theme_combinations"][63]:,} units contained clues from all six themes and {t["theme_combinations"][0]:,} contained none. Co-occurrence can span a long unit. Unit sizes, completeness and genres differ across books. These are descriptive counts with no adjustment for length or statistical baseline.

## Coverage by corpus group

Each row shows all searchable Tamil units in the group, the number with any nearby candidate, and the number of distinct nearby unit–comparison pairs. The Siddhar row combines attributed Siddhar texts. The devotional works retain their individual rows.

| Corpus group | Units scanned | Units with a nearby candidate | Nearby pairs |
| --- | ---: | ---: | ---: |"""
    lines = [headline]
    for key, book in books.items():
        lines.append(f'| {key} | {book["units"]:,} | {book["with_local"]:,} | {sum(book["local"]):,} |')
    lines.append("""
## Reproduce or inspect a result

Run `python3 -I scripts/science_census.py` from the repository root. The script reads the same Tamil units as the existing science inquiry, including segmented long works. It applies the project's folding function to each printed line, then searches for listed Tamil substrings. Each comparison requires at least one matching family on each side of its rule. Family names on the two sides are distinct. Terms can overlap across families, and distinct register entries can use the same rule.

The counts file records fingerprints for the source text, register and rules. In the compressed CSV, each row contains an ID and three hexadecimal masks. For claim index i in the JSON claim_order array, a pair matches when `(int(mask, 16) >> i) & 1` is 1. A zero bit records a tested pair with no match. Theme masks use the theme_order array. The per-book JSON arrays any and local use the claim order. The theme_combinations array uses the subset bitmask as its index, with index zero reserved for no detected themes. When refreshing the register, add an explicit rule for each new ID before rebuilding.

[Download the complete pair matrix](census_matrix.csv.gz) · [Inspect counts, denominators and historical checks](census.json) · [Inspect Tamil terms and rules](census_rules.json)""")
    (OUT / "census.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    spec = json.loads(RULEFILE.read_text())
    claims = list(rows(KG / "science/findings.jsonl")) + list(rows(OUT / "sources.jsonl"))
    names = [r["id"] for r in claims]
    if len(set(names)) != len(names) or set(names) != set(spec["rules"]):
        sys.exit("Supply one rule for every unique registered claim")
    family_bits = {name: 1 << i for i, name in enumerate(spec["families"])}
    def group(words):
        return sum(family_bits[n] for n in set(words.split()))
    signatures = []
    for name in names:
        a, b = map(group, spec["rules"][name].split("|"))
        if a & b:
            sys.exit("Overlapping clues in " + name)
        signatures.append((a, b))
    themes = list(spec["theme_families"])
    theme_masks = [group(spec["theme_families"][t]) for t in themes]
    term_bits = defaultdict(int)
    for name, terms in spec["families"].items():
        for term in terms:
            term_bits[fold(term)] |= family_bits[name]
    # Prefix lookahead permits overlapping words. Shorter alternatives at the same
    # position also contribute, including terms assigned to different families.
    ordered = sorted(term_bits, key=lambda x: (-len(x), x))
    pattern = re.compile("(?=(" + "|".join(map(re.escape, ordered)) + "))")
    for term in ordered:
        for other in ordered:
            if term.startswith(other):
                term_bits[term] |= term_bits[other]

    @lru_cache(maxsize=65536)
    def claim_mask(families):
        return sum(1 << j for j, (a, b) in enumerate(signatures) if a & families and b & families)

    per_book = {}
    digest = hashlib.sha256()
    registry_hash = hashlib.sha256()
    for r in claims:
        registry_hash.update(json.dumps(r, ensure_ascii=False, sort_keys=True).encode() + b"\n")
    ledger_rows = []
    ids = set()
    for ident, lines in units():
        if ident in ids:
            raise ValueError("Duplicate unit identifier " + ident)
        ids.add(ident)
        digest.update(json.dumps([ident, lines], ensure_ascii=False, separators=(",", ":")).encode() + b"\n")
        book = ident.split(":")[0]
        if book not in per_book:
            per_book[book] = dict(units=0, with_local=0, any=[0]*len(names),
                                  local=[0]*len(names), theme_combinations=[0]*64)
        info = per_book[book]
        masks = []
        for line in lines:
            m = 0
            for token in pattern.findall(fold(line)):
                m |= term_bits[token]
            masks.append(m)
        whole = local = prev = earlier = 0
        for m in masks:
            whole |= m
            local |= claim_mask(earlier | prev | m)
            earlier, prev = prev, m
        wide = claim_mask(whole)
        if local & ~wide:
            raise AssertionError(ident)
        present = sum(1 << j for j, fam in enumerate(theme_masks) if whole & fam)
        info["units"] += 1
        info["with_local"] += bool(local)
        for j in bits(wide):
            info["any"][j] += 1
        for j in bits(local):
            info["local"][j] += 1
        # Each nonempty subset of the six observed themes gets one unit. Mask 0
        # is reserved for units with no themes to make the denominator visible.
        subset = present
        while subset:
            info["theme_combinations"][subset] += 1
            subset = (subset - 1) & present
        if not present:
            info["theme_combinations"][0] += 1
        ledger_rows.append((ident, format(wide, "x"), format(local, "x"), format(present, "x")))

    # Entire pair matrix. An unset bit is an explicit zero; two masks preserve
    # the difference between a line-local conjunction and distant mentions.
    with (OUT / "census_matrix.csv.gz").open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, filename="") as gz:
            with io.TextIOWrapper(gz, encoding="utf-8", newline="") as f:
                w = csv.writer(f, lineterminator="\n")
                w.writerow(["unit_id", "anywhere_claim_bits_hex", "nearby_claim_bits_hex", "theme_bits_hex"])
                w.writerows(ledger_rows)

    mapping = {"siddhar:"+str(r["seq"]): r["id"] for r in rows(KG/"core/siddhar.jsonl")}
    lookup = {v: (int(w, 16), int(l, 16)) for v, w, l, _ in ledger_rows}
    def historical(path):
        checks = []
        for rec in rows(path):
            ref = mapping.get(rec["verse"], rec["verse"])
            a, l = lookup[ref]
            bit = 1 << names.index(rec["finding"])
            checks.append(dict(verse=ref, claim=rec["finding"], any=bool(a & bit), local=bool(l & bit)))
        return dict(total=len(checks), any=sum(r["any"] for r in checks),
                    local=sum(r["local"] for r in checks), checks=checks)
    calibration = {group_name: historical(KG / "science" / filename)
                   for group_name, filename in [("passed", "strong_links.jsonl"), ("controls", "controls.jsonl")]}

    totals = {}
    for k in ("units", "with_local"):
        totals[k] = sum(b[k] for b in per_book.values())
    for k in ("any", "local", "theme_combinations"):
        totals[k] = list(map(sum, zip(*(b[k] for b in per_book.values()))))
    out = dict(version=1, method="Distinct Tamil family conjunction in a unit or at most three adjacent printed lines",
               source_text_sha256=digest.hexdigest(), claim_register_sha256=registry_hash.hexdigest(),
               rules_sha256=hashlib.sha256(RULEFILE.read_bytes()).hexdigest(),
               claim_order=names, theme_order=themes, family_count=len(family_bits),
               search_terms=len(term_bits), book_count=len(per_book),
               pair_count=totals["units"] * len(names), totals=totals, books=per_book,
               calibration=calibration)
    dump(OUT/"census.json", out)
    write_report(out)
    return out


if __name__ == "__main__":
    result = main()
    t=result["totals"]
    print("Books:", result["book_count"], "units:", t["units"], "claims:", len(result["claim_order"]),
          "pairs:", result["pair_count"], "local:", sum(t["local"]), "anywhere:", sum(t["any"]),
          "local units:", t["with_local"])
    print("Calibration:", {k:(v["local"],v["any"],v["total"]) for k,v in result["calibration"].items()})
