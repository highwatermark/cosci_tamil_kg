# How much of the corpus has been compared?

The scan tested 41,583 Tamil units in 45 corpus groups against every one of 84 registered comparisons. Of the 3,492,972 resulting pairs, 3,419 met both Tamil vocabulary conditions somewhere in the unit. Requiring the clues to occur within three consecutive printed lines reduced that count to 2,218 pairs across 1,742 distinct units. 68 comparison rules returned a nearby candidate.

## What the scan found

The largest nearby count belongs to the rule for Gabor Maté, which uses a broad vocabulary. The number describes its retrieval behavior. Reading those passages for specific relations, including counterexamples, is still open. Generic words for distress or the body can match multiple modern claims. A match against a quantum or consciousness entry establishes only that its chosen Tamil clues co-occur.

The nearby rule recovered 1 of 17 previously accepted links and matched 0 of 100 historical controls. The recovered pair connected siddhar:thiruvalluvar-njanam:2.17 to finding:aging-hallmarks. The missing links expose the limits of literal fragments, morphology, metaphor and line boundaries. The earlier grades came from a selected set, and the comparison vocabulary was designed with knowledge of the project. These counts cannot establish translation accuracy, precision on new candidates or an unbiased recall estimate.

## How to read the combinations

The six theme families cover matter and scale, life and environment, body and regulation, experience and identity, ethics and practice, and inquiry and measurement. Every unit was tested for all 63 nonempty subsets. Counts are inclusive, so a unit matching three themes also contributes to its three pairs. 3 units contained clues from all six themes and 29,338 contained none. Co-occurrence can span a long unit. Unit sizes, completeness and genres differ across books. These are descriptive counts with no adjustment for length or statistical baseline.

## Coverage by corpus group

Each row shows all searchable Tamil units in the group, the number with any nearby candidate, and the number of distinct nearby unit–comparison pairs. The Siddhar row combines attributed Siddhar texts. The devotional works retain their individual rows.

| Corpus group | Units scanned | Units with a nearby candidate | Nearby pairs |
| --- | ---: | ---: | ---: |
| acharakkovai | 100 | 1 | 2 |
| ainkurunuru | 498 | 10 | 13 |
| ainthinai_aimpathu | 51 | 1 | 2 |
| ainthinai_ezhupathu | 67 | 1 | 1 |
| akananuru | 401 | 44 | 49 |
| avvaiyar | 274 | 5 | 5 |
| civaka_cintamani | 3,145 | 76 | 91 |
| elathi | 82 | 8 | 12 |
| iniyavai_narpathu | 41 | 2 | 3 |
| innaa_narpathu | 41 | 0 | 0 |
| kainnilai | 60 | 1 | 1 |
| kalavazhi_narpathu | 41 | 0 | 0 |
| kalittokai | 150 | 34 | 57 |
| kar_narpathu | 40 | 1 | 2 |
| kundalakesi | 19 | 1 | 1 |
| kural | 1,330 | 39 | 59 |
| kuruntokai | 402 | 10 | 12 |
| manimekalai | 288 | 107 | 152 |
| muthumozhikkanchi | 100 | 4 | 8 |
| naga_kumara_kaviyam | 171 | 5 | 9 |
| naladiyar | 400 | 21 | 28 |
| nanmanikkadigai | 106 | 3 | 4 |
| natrinai | 400 | 27 | 34 |
| neelakesi | 885 | 20 | 26 |
| paripadal | 35 | 6 | 8 |
| patitruppattu | 92 | 11 | 14 |
| pattupattu | 217 | 11 | 12 |
| pazhamozhi_nanooru | 401 | 9 | 10 |
| prabandham | 3,961 | 137 | 157 |
| purananuru | 398 | 30 | 31 |
| siddhar | 2,701 | 139 | 178 |
| silappathikaram | 434 | 51 | 65 |
| sirupanchamoolam | 98 | 8 | 10 |
| soolamani | 2,128 | 33 | 39 |
| thinaimalai_nootraimpathu | 154 | 6 | 6 |
| thinaimozhi_aimpathu | 50 | 1 | 1 |
| thirikadugam | 101 | 4 | 6 |
| thirumurai | 14,580 | 524 | 650 |
| thiruppugazh | 1,325 | 167 | 220 |
| tholkappiyam | 1,603 | 14 | 17 |
| tirumanthiram | 2,783 | 113 | 145 |
| tiruvasagam | 661 | 23 | 36 |
| udayana_kumara_kaviyam | 367 | 11 | 13 |
| valayapathi | 72 | 9 | 12 |
| yasodhara_kaviyam | 330 | 14 | 17 |

## Reproduce or inspect a result

Run `python3 -I scripts/science_census.py` from the repository root. The script reads the same Tamil units as the existing science inquiry, including segmented long works. It applies the project's folding function to each printed line, then searches for listed Tamil substrings. Each comparison requires at least one matching family on each side of its rule. Family names on the two sides are distinct. Terms can overlap across families, and distinct register entries can use the same rule.

The counts file records fingerprints for the source text, register and rules. In the compressed CSV, each row contains an ID and three hexadecimal masks. For claim index i in the JSON claim_order array, a pair matches when `(int(mask, 16) >> i) & 1` is 1. A zero bit records a tested pair with no match. Theme masks use the theme_order array. The per-book JSON arrays any and local use the claim order. The theme_combinations array uses the subset bitmask as its index, with index zero reserved for no detected themes. When refreshing the register, add an explicit rule for each new ID before rebuilding.

[Download the complete pair matrix](census_matrix.csv.gz) · [Inspect counts, denominators and historical checks](census.json) · [Inspect Tamil terms and rules](census_rules.json)
