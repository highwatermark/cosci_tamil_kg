# Corpus summary: every book marked, graded and bridged

State on 2026-11-27, after wave 6. Every book in the corpus is marked (kg/themes/<book>/ch*.json),
registered in scripts/book_marks.py and graded blind (kg/themes/sangam_grading/). This page is the
count of what exists, how good the links are, and how the groups connect. All numbers are rebuilt by:

```
python3 -I scripts/merge_sangam_grades.py   # kg/groups/<group>/link_audit.json, kg/groups/all_link_audit.json
python3 -I scripts/merge_concepts.py        # kg/themes/concepts.json
python3 -I scripts/build_group_graphs.py    # kg/groups/<group>/{nodes,edges}.jsonl, bridges.jsonl, bridges_summary.json, index.json
python3 -I scripts/export_viz.py            # viz/data_core.js, viz/data_<group>.js
```

No translation or commentary text is stored. Verses carry the Tamil original (public domain) and the
marking agent's own readings.

## Counts

40 books in nine groups (docs/corpus-groups.md), 20,606 verses or reading units, 14,947 links in the
explorer (6,936 from the marking pass, 8,011 from the five kept graphs), 354 shared concepts.

| Group | Books | Verses / units | Links proposed | Graph |
|---|---|---|---|---|
| Ettuthogai, akam | Natrinai, Kuruntokai, Ainkurunuru, Kalittokai, Akananuru | 1,851 | 1,220 | kg/groups/ettuthogai_akam |
| Ettuthogai, puram | Purananuru, Patitruppattu | 490 | 452 | kg/groups/ettuthogai_puram |
| Ettuthogai, devotional | Paripadal | 146 | 144 | kg/groups/ettuthogai_devotional |
| Pattupattu | the ten idylls | 207 units | 122 | kg/groups/pattupattu |
| Pathinenkilkanakku, ethics | 10 short works (+ Kural 1,330 and Naladiyar 400, kept graphs) | 1,070 (+1,730) | 1,281 | kg/groups/ethics, kg/kural, kg/naladiyar |
| Pathinenkilkanakku, akam | Kar Narpathu, Ainthinai Aimpathu and Ezhupathu, Thinaimozhi Aimpathu, Thinaimalai Nootraimpathu, Kainnilai, Kalavazhi Narpathu | 463 | 327 | kg/groups/kilkanakku_akam |
| Epics, great | Silappathikaram, Manimekalai, Civaka Cintamani, Valayapathi, Kundalakesi | 3,959 | 1,897 | kg/groups/epics_great |
| Epics, minor | Soolamani, Neelakesi, Naga Kumara, Udayana Kumara, Yasodhara Kaviyam | 3,881 | 1,493 | kg/groups/epics_minor |
| Devotional and mystic | Tirumanthiram 2,783, Thiruppugazh 1,325, Siddhar songs 2,701 (kept graphs) | 6,809 | (kept) | kg/tirumanthiram, kg/thiruppugazh, kg/siddhar |
| Grammar | Tholkappiyam | frame only | none | its nurpas are cited, not linked |

Graph contents of the eight built groups: 20,294 nodes in all (chapters, verses, and karu 3,232,
entity 704, item 2,140, norm, school and 1,457 cast-person nodes) and edges for concepts (EXPRESSES),
karu and entities (NAMES), ullurai and iraicchi (388, experimental), counted items (LISTS 2,268),
historical norms (NORM 204), doctrinal claims with school and stance (CLAIMS 2,934), speakers and
agents (SPEAKS, ACTS), echoes of the Kural, and the 6,936 links with their audit grades.

**Concepts.** concepts.json grew from 284 to 354: 70 new ids from the chapters' new_concepts. Twelve
near-duplicates were mapped to a kept id and recorded under its `aliases` (nimiththam and pul to
nimittam; punal_aadal and punalaattu to punalaadal; paththini to pathini; kunam to gunam; pagudhi to
pakuthi; poli to aabaasam; samayavaadham to vaadhu; aadal to koothu; vatham to nonbu; serukku to the
existing agandhai). No existing id was renamed. 92 verse marks in 25 chapter files were rewritten to
the kept id and the redundant declarations dropped; `book_marks.py check` passes for every
registered book, and naladiyar_marks.py and chapter_marks.py pass for the Naladiyar and Kural.

## Grades

6,916 of the 6,936 proposed links were graded blind (20 in Paripadal and Pattupattu were in no
packet). Where graders differed the strictest grade is kept; every grade is recorded with its run,
grader and model.

| | Links | Sound | Weak | Forced | Wrong | Sound % |
|---|---|---|---|---|---|---|
| All marked books | 6,916 | 2,337 | 3,933 | 609 | 37 | 33.8 |

1,138 links were graded more than once (2,976 grade pairs): exact agreement 72.5%, kappa on
sound/not sound 0.59. Against the 828 hidden calibration links of known grade, graders were exact
65.6% of the time, stricter 181 times and more lenient 104. `teaches` was failed on 3,012 links.

### By group (links proposed from the group's books)

| Group | Links | Sound % | Agreement (exact %, kappa sound) | Calibration exact % |
|---|---|---|---|---|
| Pattupattu | 110 | 51.8 | 58.1, 0.39 | 77.8 |
| Ethics (10 works) | 1,281 | 49.3 | 65.8, 0.40 | 75.6 |
| Ettuthogai puram | 452 | 43.1 | 76.6, 0.69 | 74.6 |
| Ettuthogai akam | 1,220 | 42.6 | 73.9, 0.58 | 75.0 |
| Kilkanakku akam | 327 | 33.3 | 71.6, 0.65 | 78.6 |
| Paripadal | 136 | 33.1 | 84.0, 0.73 | 78.6 |
| Great epics | 1,897 | 28.8 | 70.6, 0.55 | 54.6 |
| Minor epics | 1,493 | 15.6 | 72.9, 0.69 | 54.3 |

### By book

| Book | Group | Ch. | Verses | Links | Sound | Sound % | Graded twice | Exact % | Kappa | Marker |
|---|---|---|---|---|---|---|---|---|---|---|
| Natrinai | Ett. akam | 20 | 400 | 249 | 130 | 52.2 | 29 | 55.6 | 0.18 | Opus |
| Kalittokai | Ett. akam | 9 | 150 | 131 | 66 | 50.4 | 38 | 70.1 | 0.36 | Opus |
| Kuruntokai | Ett. akam | 20 | 402 | 238 | 102 | 42.9 | 34 | 62.7 | 0.25 | Opus |
| Akananuru | Ett. akam | 20 | 401 | 245 | 91 | 37.1 | 92 | 77.9 | 0.70 | Opus |
| Ainkurunuru | Ett. akam | 50 | 498 | 357 | 131 | 36.7 | 56 | 76.8 | 0.51 | Opus |
| Patitruppattu | Ett. puram | 9 | 92 | 87 | 42 | 48.3 | 26 | 70.6 | 0.53 | Opus |
| Purananuru | Ett. puram | 20 | 398 | 365 | 153 | 41.9 | 122 | 77.2 | 0.71 | Opus |
| Paripadal | Paripadal | 20 | 146 | 136 | 45 | 33.1 | 27 | 84.0 | 0.73 | Opus |
| Pattupattu | Pattupattu | 13 | 207 | 110 | 57 | 51.8 | 16 | 58.1 | 0.39 | Opus |
| Pazhamozhi Nanooru | Ethics | 36 | 401 | 489 | 284 | 58.1 | 81 | 66.0 | 0.30 | Opus |
| Thirikadugam | Ethics | 5 | 101 | 147 | 78 | 53.1 | 39 | 63.4 | 0.30 | Opus |
| Acharakkovai | Ethics | 5 | 100 | 79 | 41 | 51.9 | 24 | 69.8 | 0.54 | Opus |
| Nanmanikkadigai | Ethics | 5 | 106 | 146 | 71 | 48.6 | 28 | 56.2 | 0.17 | Opus |
| Elathi | Ethics | 4 | 82 | 74 | 32 | 43.2 | 10 | 87.0 | 0.51 | Opus |
| Sirupanchamoolam | Ethics | 5 | 98 | 114 | 49 | 43.0 | 19 | 68.6 | 0.50 | Opus |
| Iniyavai Narpathu | Ethics | 2 | 41 | 46 | 19 | 41.3 | 6 | 75.0 | 0.60 | Opus |
| Muthumozhikkanchi | Ethics | 10 | 100 | 126 | 41 | 32.5 | 24 | 63.1 | 0.38 | Opus |
| Innaa Narpathu | Ethics | 2 | 41 | 60 | 17 | 28.3 | 15 | 67.3 | 0.35 | Opus |
| Ainthinai Aimpathu | Kil. akam | 5 | 51 | 53 | 23 | 43.4 | 8 | 62.5 | 0.34 | Opus |
| Thinaimalai Nootraimpathu | Kil. akam | 9 | 154 | 103 | 38 | 36.9 | 22 | 67.4 | 0.40 | Opus |
| Ainthinai Ezhupathu | Kil. akam | 5 | 67 | 41 | 14 | 34.1 | 6 | 88.2 | 0.61 | Opus |
| Thinaimozhi Aimpathu | Kil. akam | 5 | 50 | 43 | 14 | 32.6 | 6 | 63.6 | 0.89 | Opus |
| Kar Narpathu | Kil. akam | 2 | 40 | 26 | 8 | 30.8 | 16 | 73.3 | 0.74 | Opus |
| Kalavazhi Narpathu | Kil. akam | 2 | 41 | 13 | 3 | 23.1 | 3 | 100 | 1.00 | Opus |
| Kainnilai | Kil. akam | 5 | 60 | 48 | 9 | 18.8 | 7 | 66.7 | 1.00 | Opus |
| Manimekalai | Great epics | 32 | 288 | 329 | 176 | 53.5 | 49 | 88.9 | 0.83 | Opus |
| Silappathikaram | Great epics | 40 | 435 | 374 | 164 | 43.9 | 63 | 76.9 | 0.65 | Opus |
| Kundalakesi | Great epics | 1 | 19 | 17 | 5 | 29.4 | 8 | 66.7 | 0.59 | Opus |
| Valayapathi | Great epics | 3 | 72 | 49 | 12 | 24.5 | 25 | 42.6 | 0.04 | Opus |
| Civaka Cintamani | Great epics | 133 | 3,145 | 1,128 | 189 | 16.8 | 74 | 66.2 | 0.28 | Opus ch1-101, Sonnet ch102-133 |
| Neelakesi | Minor epics | 40 | 885 | 379 | 130 | 34.3 | 82 | 80.9 | 0.71 | Opus |
| Yasodhara Kaviyam | Minor epics | 16 | 330 | 170 | 23 | 13.5 | 14 | 64.3 | 0.42 | Sonnet |
| Soolamani | Minor epics | 92 | 2,128 | 722 | 65 | 9.0 | 51 | 54.9 | 0.15 | Sonnet |
| Naga Kumara Kaviyam | Minor epics | 10 | 171 | 70 | 5 | 7.1 | 5 | 80.0 | 1.00 | Sonnet |
| Udayana Kumara Kaviyam | Minor epics | 19 | 367 | 152 | 10 | 6.6 | 13 | 69.2 | 0.63 | Sonnet |

Per-book calibration is in kg/groups/all_link_audit.json (`by_book`); it counts the calibration links
in the packets that held the book's links, so neighbouring books share packets and numbers.

## How the groups connect: the bridge matrix

Sound links over graded links, both directions, for every pair of groups (kg/groups/bridges_summary.json;
the explorer's Bridges view draws the same matrix and lists the links of any cell). The diagonal, in
bold, is the within-group baseline. The ethics and devotional cells include the five kept graphs,
which were graded in earlier passes under their own briefs: the Kural–Naladiyar and
Tirumanthiram–Kural links make the ethics diagonal (72%) and the ethics–devotional cell (59%) high.

| | Ett. akam | Kil. akam | Ett. puram | Pattupattu | Paripadal | Ethics | Devotional | Great epics | Minor epics |
|---|---|---|---|---|---|---|---|---|---|
| Ett. akam | **232/571** (41%) | 63/194 (32%) | 69/180 (38%) | 12/24 (50%) | 8/29 (28%) | 229/503 (46%) | 2/5 (40%) | 8/34 (24%) | 0/10 (0%) |
| Kil. akam | 63/194 (32%) | **20/56** (36%) | 2/10 (20%) | 5/5 (100%) | 1/1 (100%) | 24/84 (29%) | · | 0/5 (0%) | · |
| Ett. puram | 69/180 (38%) | 2/10 (20%) | **80/175** (46%) | 17/35 (49%) | 4/11 (36%) | 109/238 (46%) | 0/2 (0%) | 44/100 (44%) | 0/13 (0%) |
| Pattupattu | 12/24 (50%) | 5/5 (100%) | 17/35 (49%) | **6/14** (43%) | 4/15 (27%) | 21/38 (55%) | 1/1 (100%) | 2/23 (9%) | 0/3 (0%) |
| Paripadal | 8/29 (28%) | 1/1 (100%) | 4/11 (36%) | 4/15 (27%) | **14/24** (58%) | 10/45 (22%) | 5/15 (33%) | 0/6 (0%) | · |
| Ethics | 229/503 (46%) | 24/84 (29%) | 109/238 (46%) | 21/38 (55%) | 10/45 (22%) | **2981/4112** (72%) | 927/1568 (59%) | 156/699 (22%) | 47/565 (8%) |
| Devotional | 2/5 (40%) | · | 0/2 (0%) | 1/1 (100%) | 5/15 (33%) | 927/1568 (59%) | **2033/3581** (57%) | 22/149 (15%) | 11/166 (7%) |
| Great epics | 8/34 (24%) | 0/5 (0%) | 44/100 (44%) | 2/23 (9%) | 0/6 (0%) | 156/699 (22%) | 22/149 (15%) | **310/871** (36%) | 53/164 (32%) |
| Minor epics | 0/10 (0%) | · | 0/13 (0%) | 0/3 (0%) | · | 47/565 (8%) | 11/166 (7%) | 53/164 (32%) | **127/583** (22%) |

All bridges: 1,856 sound of 4,940 graded (37.6%); all within-group links 58.1%, or, for the marking
pass alone, ethics 49.7%, puram 45.7%, akam 40.6%, great epics 35.6%, Kilkanakku akam 35.7%,
minor epics 21.8%.

What the matrix says:
- The bridges that carry weight are few and run through the ethics group: akam to ethics (229 sound,
  46%) and puram to ethics (109, 46%) match or beat the akam and puram baselines, and the
  Tirumanthiram–Kural links (927) are the largest bridge of all, from an earlier grading regime.
- The great epics bridge best to puram (44 of 100, 44%, above their own 36%) and to each other.
- The minor epics bridge to almost nothing: 8% to ethics, 7% to the devotional books, 0 of 26 to the
  Sangam groups. This is mostly the wave 6 Sonnet marking (below), not proof that no bridge exists.
- Cells with fewer than about 20 graded links (Kilkanakku akam to Pattupattu, 5 of 5) are noise.
- Of the bridges docs/corpus-groups.md set out to test: puram ethics of giving to the ethics works
  holds (46%); akam landscape to the mystic inner landscape has almost no links to test (5); epic
  karma and renunciation to the Siddhars and Naladiyar is weak (15% and 22%); Murugan across
  Paripadal, Pattupattu and the Thiruppugazh is thin (Paripadal to devotional 5 of 15, Pattupattu 1).

## Models and cost

- Marking: Opus for every book except wave 6's last stretch: Civaka Cintamani chapters 102-133,
  Soolamani, Naga Kumara, Udayana Kumara and Yasodhara Kaviyam were marked by Sonnet (wave 6 was
  paused at Cintamani chapter 101 to save the usage limit, then finished on Sonnet).
- Grading: Opus in every run, except wave 6, where g1 (all 57 packets) was Sonnet and g2 an Opus
  spot-check of 4 packets. Opus graders gave sound to 47.1% of the links they graded and were exact
  on 70.5% of calibration links; the Sonnet grader gave sound to 14.9% and was exact on 52.6%
  (stricter than the known grade 71 times, more lenient 37). The wave 6 g1–g2 kappa on sound/not
  sound was 0.30, against 0.55-0.79 in the other runs.
- Under the same Sonnet grader, Sonnet-marked chapters were 10.4% sound against 18.9% for
  Opus-marked Cintamani chapters (strictest grade: 10.0% against 18.3%). Both the marker and the
  grader push wave 6 down.
- Token counts per wave were not recorded in the repository; only docs/link-pass-plan.md has
  figures, for the earlier Kural link pass (about 1.2 million tokens per 443 links audited). Grading
  packets: 11 runs, 183 g1 packets and 34 g2 packets.

## Known weak spots

- **The Jain epics (wave 6).** 303 of 2,242 links sound (13.5%; the Opus spot-check gave 16%);
  the Sonnet grader failed `teaches` on 1,534 and `gains` on 977 of 1,217 bridges. Soolamani 9%, Udayana Kumara 7%,
  Naga Kumara 7%, Yasodhara 14%, Cintamani 17%. Sonnet-marked chapters 10% against 19% for
  Opus-marked ones. The explorer shows sound links by default; turn on "+ Weak" to see these.
- **Grader agreement is low on some books**: Valayapathi kappa 0.04, Soolamani 0.15, Nanmanikkadigai
  0.17, Natrinai 0.18, Kuruntokai 0.25. Their sound% is less settled than the table suggests.
- **Two grading regimes in one matrix.** The kept graphs (Kural, Naladiyar, Tirumanthiram,
  Thiruppugazh, Siddhars) were graded under the link-pass and per-book briefs; the Tirumanthiram's
  graders ran lenient against calibration. Their cells are not comparable with the marking pass's.
- **Ungraded links**: 20 (Paripadal 8, Pattupattu 12).
- **Thin bridges**: the akam-to-mystic and Murugan bridges have too few links to judge.
- **Concept merges are by judgment** (twelve aliases); the Tamil words differ in samayavaadham/vaadhu,
  aadal/koothu, vatham/nonbu and serukku/agandhai, and could be split again.
- **No Tamil scholar has reviewed any of this**, and no grader had a Tamil lexicon. Only the Kural and
  Naladiyar have commentary in the corpus. The explorer still shows the Kural's Pope glosses and
  commentator positions from the kept graph, as before.
