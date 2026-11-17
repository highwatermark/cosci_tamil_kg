# Ingest report: Siddhar songs (`siddhar`)

- Script: `scripts/parse_siddhar.py` (standard library only; run `python3 -I scripts/parse_siddhar.py`; reads only `data/text/`; output is deterministic, same md5 on two runs)
- Output: `kg/core/siddhar.jsonl`, **2,702 units** in canonical order (43 works, 26 poets), parsed from 3,151 raw units; 449 raw units were duplicates and were merged into existing records.

## Record shape

`id` (`siddhar:<work>:<label>`), `seq` (global order), `siddhar` (poet), `work`, `work_title`, `number` (the number in the work), `run` (numbering run inside the work), `section` (part and metre headings), `tamil` (lines), `glosses`, `variant_notes`, `attribution` (`traditional` or `attributed`), `thirumurai_11` (the Thirumurai verse number when the unit is also in Thirumurai 11), `sources` (each file, line, printed number and match score), `parallels` (ids of the same text under another poet's name).

How ids are built:
- The label is the number in the work's base file.
- When a work restarts its numbering (by part or metre), the label is `run.number`: for example `agasthiyar-njanam:4.2` and `thiruppadal-thirattu:3.3`.
- `uN` marks an unnumbered unit, such as a kappu, a pallavi, or a stanza printed without a number.
- A unit found only in a secondary file is prefixed with that file's number, for example `meynjanap-pulambal:0155-172` and `valaik-kummi:0701-111`. It is placed directly after the base unit that holds its predecessor in that file.

## Files used

| File | Contents | Work keys |
|---|---|---|
| pmuni0074 | Pathrakiriyar, Meynjanap pulambal (base) | meynjanap-pulambal |
| pmuni0155 | "Ekkalak kanni", an anonymous palm-leaf text from GOML Bulletin 1953. N. Kannan's 2002 essay in the same file argues that it is Pathrakiriyar's pulambal; the texts match kanni for kanni. Used as a second source. | meynjanap-pulambal |
| pmuni0083 | Pattinathar, Thiruppadal thirattu I: Thiruvekambamalai, Thiruthillai, four agavals, verses on shrines, Arutpulambal 1 and the first 48 kannis of Arutpulambal 2 | thiruvekambamalai, thiruthillai, koyil-thiruvagaval-1..3, kachchi-thiruvagaval, thiruppadal-thirattu, arutpulambal-1, -2 |
| pmuni0270 | Pattinathar II, 1887 edition by A. Ramaswamy: four Thirumurai-11 works, plus the Thiruppadal thirattu (verses on shrines, the verses for his mother's cremation, single venbas) | thiruvidaimaruthur-mummanikkovai, thirukkazhumala-mummanikkovai, thiruvekambamudaiyar-thiruvandhadhi, thiruvotriyur-oru-pa-oru-pahdu, thiruppadal-thirattu |
| pmuni0276_01 | Pattinathar III (1887): Arutpulambal 1–4 | arutpulambal-1..4 |
| pmuni0276_02 | Pattinathar IV (1887): Puranamalai, Nenjodu magizhdal, Udarkootru vannam | puranamalai, nenjodu-magizhdal, udarkootru-vannam |
| pmuni0269 | Sivavakkiyar, Sivavakkiyam, with word glosses | sivavakkiyam |
| pmuni0076 | Collection I: Azhuganni, Ramadevar Pujavidhi, Kaduveli Anandakkalippu, Kudhambai, Sattaimuni Njanam, Thirumula Nayanar Njanam, Thiruvalluvar Njanam | azhuganni … thiruvalluvar-njanam |
| pmuni0212 | Collection 4: Agappei and Idaikkadar (each with end-note glosses), Konganar's Valaik kummi | agappei, idaikkadar, valaik-kummi |
| pmuni0701 | Valaik kummi, anonymous palm-leaf edition by R. Kumaravel (2007). Used as a second source; the editor's preface (lines 22–240) and first-line index (826+) are skipped. | valaik-kummi |
| pmuni0857 | Collection 8: Pambatti, Sangili, Thirikona Siddhar | pambatti, sangili, thirikonar |
| pmuni0858 | Collection 9 (the file's own heading says "8"): Mouna Siddhar (Vakulinathar), Punnakku, Kanjamalai, Nondi (Machchendiranathar) | mounachiddhar, punnakku, kanjamalai, nondi |
| pmuni0859 | Collection 10: Kakapusundar, Agasthiyar (Njanam 1–5), Romarishi, Valmiki Sutra, Subramaniar Njanam | *-njanam |
| pmuni0853_02 | Madurai Valaisami Siddhar, Njanak kummi | njanak-kummi |
| pmuni0127_02 | Thirumurai 11 (row 213). Read only to mark the overlap. Not parsed into this book. | - |

### Files rejected and why

- **Row 213, pmuni0127_01/02 (Thirumurai 11, Pattinathu Pillaiyar):** these belong to the Thirumurai agent. Overlap: four works in pmuni0270 are Thirumurai-11 works. They are kept here and every unit carries its Thirumurai number:
  - Thiruvidaimaruthur mummanikkovai, 30 of 30 verses (896–925)
  - Thirukkazhumala mummanikkovai, only 12 of 30 (866–877), because the 1887 file stops at verse 12
  - Thiruvekambamudaiyar thiruvandhadhi, 100 of 100 (926–1025)
  - Thiruvotriyur oru pa oru pahdu, 10 of 10 (1026–1035)

  All 152 matched units have `thirumurai_11` set. The Koyil nanmanimalai (Thirumurai 11.1) is not in any Siddhar file. No other Pattinathar unit matched Thirumurai 11. **Decide at merge time whether to keep these 152 units here or drop them in favour of the Thirumurai records.**
- **Tirumanthiram (pmuni0004/0009/0010):** left to the other agent. Thirumula Nayanar Njanam (pmuni0076) is a separate viruttam text. I checked every unit against the Tirumanthiram files and none matched (Jaccard ≥ 0.3).
- **Avvaiyar's Kural / Njanakkural (pmuni0316, pmuni0744 with Vadivelu Mudaliar's commentary):** this is a yogic text that some lists class with Siddhar works, but the catalog files it under நீதி நூல்கள் and the brief does not name it. It was not ingested. It could be added as its own book; pmuni0744 has a commentary to align.
- **Thayumanavar (pmuni0303/0305/0308, 0560), Ramalinga Adigal, Bharathi's "ஞானப் பாடல்கள்" (0053), Pir Muhammad's Njanak kuravanji (1032):** none of these is Siddhar literature. The other kummi files (0763, 0764 and so on) are narrative or devotional kummis.
- **Essays, prefaces and indexes** inside the files used were left out: Kannan's essay in pmuni0155, Kumaravel's preface and index in pmuni0701, the biographical notes on each Siddhar in pmuni0212, and the 1887 printing colophon in pmuni0270.

### Siddhar texts by attribution only (`"attribution": "attributed"`, 353 units)

These go under a legendary, divine or canonical name rather than a historical Siddhar poet:
- Thirumula Nayanar Njanam and Thiruvalluvar Njanam (both pmuni0076)
- Agasthiyar, Romarishi, Valmiki Sutra, Subramaniar and Kakapusundar Njanam (all pmuni0859)
- Ramadevar Pujavidhi and Sattaimuni Njanam (both pmuni0076)
- Valaik kummi: its own introductory note in pmuni0212 (line 1138) says it is ascribed to Konganar but was not written by him, and pmuni0701 prints it as anonymous

Two other attribution notes, not flagged in the field:
- Ekkalak kanni (pmuni0155) is anonymous in its source. It is treated as Pathrakiriyar's because its text matches.
- The "Siddhar" Pattinathar of the Thiruppadal thirattu is traditionally distinguished from the Thirumurai's Pattinathu Pillaiyar, but these files treat them as one poet.

## Unit counts against tradition

| Work | Units | Traditional or expected | Notes |
|---|---|---|---|
| Meynjanap pulambal | 236 | 231 kannis plus kappu | 232 from pmuni0074, 197 of them confirmed by pmuni0155. Four kannis appear only in Ekkalak kanni: 0155-88, -148, -192 and -201. Its kappu matched the pmuni0074 kappu. pmuni0074 repeats four kannis inside itself (47≈127 exactly, and 22, 50, 79 near-repeats); all are kept. |
| Pattinathar (Siddhar works) | 575 | | Thiruvekambamalai 42 plus 1 unnumbered viruttam; Thiruthillai 20; four agavals, 1 unit each (47, 38, 52 and 70 lines); Thiruppadal thirattu 130 (21 shared between 0083 and 0270, 109 only in 0270); Arutpulambal 1: 72; Arutpulambal 2: 117 (verse 49 is lost: printed as dots); Arutpulambal 3: 14; Arutpulambal 4: 37; Puranamalai 102; Nenjodu magizhdal 32; Udarkootru vannam 4 |
| Pattinathar (Thirumurai 11) | 152 | 30 + 30 + 100 + 10 | Kazhumalam 12 of 30 (see above) |
| Sivavakkiyam | 525 | about 520–550 depending on the edition | Numbered 0 (kappu) to 524 with no gaps. 13 near-repeats inside the text are reported, not merged (the work is known for repeated verses). |
| Azhuganni | 41 | 40 plus 1 fragment | The last stanza (line 274) is cut off ("தொல் பொருளை அறியார்கள் . . .") |
| Ramadevar 10, Kaduveli 35 (pallavi plus 34), Kudhambai 32, Sattaimuni 6, Thirumular Njanam 9, Thiruvalluvar Njanam 20 (kappu plus 19; numbering restarts by metre) | | | |
| Agappei | 90 | 90 | |
| Idaikkadar | 132 | 130 plus kappu plus refrain | |
| Valaik kummi | 116 | 0212 has 111, 0701 has 115 plus thuthi | 111 shared; 0701 adds 5 closing kummis (111–115). The two editions number differently from verse 80 on (for example 0212:84 is 0701:83). |
| Pambatti 129, Sangili 36, Thirikonar 90 | | Thirikonar 91 couplets | Thirikonar skips the number 36, but the text reads on without a break, so this is a numbering slip. |
| Mouna 12, Punnakku 20, Kanjamalai 26 (25 plus pallavi), Nondi 33 | | | |
| Kakapusundar 79, Agasthiyar 50 (Njanam 1–5 with sub-parts; the heading reads "அகஸ்தியர் ஞானம் - 9", meaning unclear), Romarishi 14, Valmiki 16, Subramaniar 33 | | | |
| Njanak kummi | 185 | 185 (the poem's own count, "நூற்றெண்பத்தைந்துகண்ணி", in verse 184) | |

## Translations and commentaries aligned

The corpus has no translations of any Siddhar work. Three kinds of editorial apparatus are aligned:
- **`glosses`, on 68 units:**
  - Sivavakkiyam word glosses, 31 units. They are printed as bracketed lines or as gloss lines after a verse; "481. ஏகன்" is attached to verse 481 by its own number.
  - pmuni0212 end-note glosses on Agappei (19 units) and Idaikkadar (18 units), matched by verse number.
- **`variant_notes`, on 22 units:** A. Ramaswamy's variant readings ("… என்றும் பாடம்") and two word notes, from the 1887 edition (pmuni0270), in the Thirumurai-11 works.
- **Second sources, on 449 units, each with a match score:**
  - Ekkalak kanni: 197
  - pmuni0276_01 against pmuni0083 (Arutpulambal 1 and 2): 120
  - pmuni0701 against pmuni0212 (Valaik kummi): 111
  - pmuni0270 against pmuni0083 (verses on shrines): 21
- **`parallels`, on 18 units:** eight Azhuganni stanzas (33–39) repeat kannis of Pattinathar's Arutpulambal 2 (1–4, 8, 43–45 and 0276_01-81), recast with the "ஆத்தாடி" refrain. Sivavakkiyam 124 shares a couplet with Pulambal 177. Because the poets differ, these are cross-linked, not merged.

Dedupe method: letter-trigram Jaccard. A match is the best candidate by the same poet in a different file, scoring at least 0.25 (0.20 within the same work, which the sandhi-joined 1887 text and the Ekkalak kanni recension need). A Thirumurai-11 work only cross-links. Different poets need a score of at least 0.3 and are only linked. Ranking candidates by rare trigrams caused false merges through shared refrains, so it was dropped.

### Five spot checks (read)
1. `sivavakkiyam:358`: the gloss "திவாகரம் - சூரிய ஒளி" fits line 1, "திவாகரத்தின் கழியிலே". Correct.
2. `agappei:69`: the end note "மரக்கா - மரச்சோலை; வேழம் - …" fits "சுற்றி மரக்காவில் / வேழம் உண்டகனி". Correct.
3. `thiruppadal-thirattu:3.3` (Kalathi, "வாளால் மகவரிந்து ஊட்டவல்லேன் அல்லேன்"): pmuni0083:671 and pmuni0270:1861 at 0.59 are the same verse, the second with its words run together. Correct.
4. `valaik-kummi:84` ("திருப்பணி களைமுடித் தோரும்"): pmuni0212 verse 84 and pmuni0701 verse 83 are the same kummi, numbered one apart. Correct.
5. `thiruvidaimaruthur-mummanikkovai:13` ("மேவிய புன்மயிர்த் தொகையோ"): `thirumurai_11` is 908, and pmuni0127_02 line 1645 has "908 மேவிய புன்மயிர்த் தொகையோ". Correct. All 100 Anthathi verses map to 926–1025 in order.

I also read `meynjanap-pulambal:225` ↔ Ekkalak kanni 172 ("நான் யாரோ நீ யாரோ" ≈ "தானாரோ நீயாரோ … நானாரோ"; score 0.20, a true variant) and `arutpulambal-2:43` ↔ `azhuganni:37` (the "மஞ்சனமாட்டி" couplet against "மஞ்சன நீராட்டி - ஆத்தாடி"). Both are correct.

## Copyright

| Contributor | Date | Status |
|---|---|---|
| All verse texts (the Siddhars, Pattinathar, Sivavakkiyar, Valaisami and others) | pre-modern (about the 10th to 19th centuries) | public domain |
| A. Ramaswamy, 1887 edition (pmuni0270/0276): variant notes | 1887 | public domain |
| Sivavakkiyam word glosses (pmuni0269): editor not named; Project Madurai etext 2006–07 | likely 20th century | treat as modern |
| pmuni0212 end-note glosses (Agappei, Idaikkadar): editor not named; etext 2004 | likely 20th century | treat as modern |
| R. Kumaravel, edition of Valaik kummi (pmuni0701) | 2007 | The edited text is anonymous and old. The preface and index (not ingested) are modern. Quote the verses freely. |
| Source editions named for pmuni0857/0858/0859: V. Saravanamuthu Pillai (1954), C. S. Murugesan (2004) | | Verse text only, public domain |

Sidecar rights map:

```json
{
  "siddhar.tamil": {"rights": "public-domain"},
  "siddhar.variant_notes": {"rights": "public-domain", "who": "A. Ramaswamy (1887 ed.)"},
  "siddhar.glosses[pmuni0269]": {"rights": "modern", "who": "unnamed editor, Sivavakkiyam glosses"},
  "siddhar.glosses[pmuni0212]": {"rights": "modern", "who": "unnamed editor, Agappei/Idaikkadar end notes"}
}
```

All 68 `glosses` come from those two modern sources, so later stages should quote at most a few words of them.

## Text problems (all printed by the script)

- **Misprinted numbers, corrected:**
  - 0074: "1 1" read as 11, "10 1" read as 101
  - 0276_01: 540 read as 54
  - 0276_01: 350 read as 35
  - 0276_02 (Puranamalai): a second "2" read as 3
  - 0270 (Anthathi): 758 read as 75
- **Missing numbers, inferred:** 0155 kannis 28 and 34.
- **Lost verse:** Arutpulambal 2, verse 49 in 0276_01 is printed as dots. It is kept as an empty `tamil` record.
- **Truncated:** Azhuganni's last stanza (0076:274).
- **Unnumbered stanzas, kept with a `uN` label:**
  - Thiruvekambam viruttam (0083:252)
  - Thiruchengodu and Thirukkazhukkundram verses (0083:623 and 654, and their 0270 copies)
  - 0270 Thiruvenkadu "வேறு" verse
  - pallavis and refrains in Kaduveli, Idaikkadar and Kanjamalai
  - kappu stanzas
- **Corruptions:**
  - "[***]" gaps in Udarkootru vannam, unit 1
  - Words split across lines in Udarkootru vannam ("…திர / ண்டு,")
  - Two stray Latin "f" characters removed in 0270 (lines 97 and 1710)
- **Headers inside the text:**
  - The 1887 colophon in pmuni0270
  - "சித்தர் பாடல்கள்:" title blocks in pmuni0276
  - "திருச்சிற்றம்பலம்", "உ / கணபதிதுணை" and "முற்றிற்று" lines; these are dropped
  - The "தன தன தான…" rhythm line of Udarkootru vannam, which is not ingested
- **Gaps in numbering:**
  - 0276_01 jumps from 48 to 50 (the lost 49)
  - Thirikonar skips 36
  - pmuni0858's heading wrongly reads "தொகுப்பு - 8"
- **Run restarts:** numbering restarts by part or metre in Thiruvalluvar Njanam, Agasthiyar Njanam, Subramaniar Njanam and the Thiruppadal thirattu (by shrine). The `run` field tracks them.
- **Repeats inside a single file:** 4 in the Pulambal, 13 in Sivavakkiyam and 1 in Njanak kummi, each with line numbers in the script's output. All are kept.

## Suggested unit for later marking

- **Per unit as parsed, for nearly everything.** Siddhar songs are short, independent stanzas or kannis; there are no pathigams or decades, and each stanza makes its own point (Sivavakkiyam, Pulambal, Agappei, the kummis, the Njanams).
- **The Pattinathar agavals and the Thiruvotriyur oru pa oru pahdu are long poems.** They are already one unit each (agavals) or one per paragraph. Mark them as wholes, or by their numbered paragraphs.
- **Two-line kanni works** (Pulambal, Arutpulambal, Thirikona kalivenba couplets, Pambatti): marking each kanni is fine. For Thirikonar, a kalivenba whose couplets run on into one another, group them into sense units of 3–5 couplets or mark the whole poem.
- **The Thirumurai-11 works:** if they stay in this book, mark them in step with the Thirumurai agent's decision (per verse), so the two books do not mark the same verse differently.
