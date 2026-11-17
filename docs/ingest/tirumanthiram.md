# Ingest report: Tirumanthiram (Tirumular, tenth Thirumurai)

Book key: `tirumanthiram`
Script: `scripts/parse_tirumanthiram.py` (standard library only; run as `python3 -I scripts/parse_tirumanthiram.py`)
Output: `kg/core/tirumanthiram.jsonl` (2,783 records)

## Files used

| Catalog rows | File | Contents | Verses |
|---|---|---|---|
| 8 | `pmuni0004` | preface (பாயிரம், 1-112), tantra 1 (113-336), tantra 2 (337-548) | 548 |
| 35 = 36 | `pmuni0009_01` | tantra 3 (549-883) | 335 |
| 35 = 36 | `pmuni0009_02` | tantra 4, **only 884-1154** | 271 |
| 35 | `pmuni0009_03` | tantra 5 (1419-1572), tantra 6 (1573-1703) | 154 + 131 |
| 37 = 38 | `pmuni0010_01` | tantra 7 (1704-2121) | 418 |
| 37 = 38 | `pmuni0010_02` | tantra 8 (2122-2648) | 527 |
| 37 = 38 | `pmuni0010_03` | tantra 9 (2649-3047) | 399 |
| 523 | `pmuni0395_01` | V. S. Sengalvaraya Pillai's table of parallels (ஒப்புமைப் பகுதி, 1951), keyed by verse number | aligned to 56 verses |

**Duplicates between the rows.** Rows 35 and 36 point at the same files (`pmuni0009_01`, `_02`, `_03`; row 36 leaves out `_03`), and rows 37 and 38 point at the same files (`pmuni0010_01`-`_03`). They are catalog duplicates, not different editions, so each file was parsed once. Row 8 (`pmuni0004`) is the only source for the preface and tantras 1-2. No other edition of the text is in the corpus, so the "most complete text" is this one set of seven files.

**Rejected:**
- `pmuni0076` (catalog row 138, Siddhar songs): its "திருமூல நாயனார் ஞானம்" is a separate later Siddhar poem attributed to Tirumular. It is not part of the Tirumanthiram.
- `pmuni0231` (Vinayakar Agaval with Guhasri Rajapati's commentary): it quotes a few Tirumanthiram verses in passing. It is not a commentary on the text.
- The essay part of `pmuni0395_01` ("திருமந்திர ஆராய்ச்சி"): continuous prose that quotes verses by number. It is not verse-by-verse, so only the parallels table at its end was aligned.
- The Vinayakar invocation (விநாயகர் காப்பு, "ஐந்து கரத்தனை…") at the head of `pmuni0004`: it is unnumbered and is a later addition. It is not emitted as a unit.

**No translation or verse-by-verse commentary of the Tirumanthiram exists in this corpus** (no English translation, no Tamil urai). The only aligned apparatus is Sengalvaraya Pillai's parallels table.

## Record shape

`id` (`tirumanthiram:N`), `number` (the running number 1-3047 used by Project Madurai and the Kasi Mutt edition), `tantra` (0 = preface, 1-9), `tantra_name`, `chapter_no` and `chapter` (the adhikaram, numbered within each tantra), `section_no` and `section` (used only for the six sections of tantra 9, chapter 8, "திருக்கூத்து தரிசனம்"), `subheading` (unnumbered sub-headings inside a chapter, for example the eight limbs of yoga at 632-639, the eight siddhis at 671-688, and the rites at 997-1002 and 1514-1527), `chapter_verse` (the verse's number within its chapter as printed, or null where the file does not print one, as in tantras 2 and 3), `source` (the file), `tamil` (always 4 lines), `variants` (variant readings printed in the footnotes, or null), and `sengalvaraya_parallels` (list or null).

Optional fields: `tamil_source` (the line before the encoding repair, present on 61 verses), `corrupt_lines` (25 verses), `extra_lines` (4 verses) and `number_inferred` (1 verse).

## Counts

- Traditional: "மூவாயிரம்" (3,000). The edition numbering used here runs from 1 to **3047**.
- Parsed: **2,783 units**, all with exactly four lines, in order and with no duplicates.
- **Missing: 1155-1418 (264 verses), the second half of tantra 4.** `pmuni0009_02` ends at 1154, the 30th verse of chapter 7 ("பூரண சக்தி"), even though its header says 884-1154. No other file in the corpus has these verses. Tantra 4 is traditionally 884-1418, so the chapters after "பூரண சக்தி" are absent. This gap cannot be filled from the corpus.
- Units per tantra: 0: 112, 1: 224, 2: 212, 3: 335, 4: 271 (of 535), 5: 154, 6: 131, 7: 418, 8: 527, 9: 399. Each matches the range printed in its file's header. The fourteen chapter ranges printed in tantra 6 also all match.
- Doubled: none after the misprint corrections below.

## Alignment

| Field | Units aligned | Method |
|---|---|---|
| `sengalvaraya_parallels` | 56 | The table row's verse number, checked by Tamil-letter trigram overlap between the quoted phrase and the verse (at least 0.2). If that fails, the best verse within ±20 is taken when overlap is at least 0.5. |

Of the table's 58 numbered rows, 54 matched at their own number. Two matched a nearby verse: row 2300 went to 2303 and row 2367 went to 2357; in both the quoted phrase is clearly in the verse. Two rows (1178 and 1350) refer to verses in the missing 1155-1418 range and were left out. The table's numbering otherwise agrees with Project Madurai's, which confirms that the running numbering here is the standard Kasi Mutt one.

**Spot checks (read):**
1. **1**: the parallel quotes "ஐந்து வென்றனன்" and compares it with Sambandar 1-113-10 "வென்றவன் புலனைந்தும்". Correct: line 2 of verse 1 ends "ஐந்து" and line 3 begins "வென்றனன்".
2. **7**: "தன்னையொப்பா யொன்றும் இல்லாத் தலைமகன்", compared with Kural 7 "தனக்குவமை யில்லாதான்". It matches line 2 of verse 7.
3. **603**: "எண்ணாயிரத்தாண்டு யோகம் இருக்கினும்…" is the whole of verse 603 (chapter தியானம்). Correct.
4. **1644**: "சித்தம் சிவமாக", compared with Tiruvasagam Achcho-1. Verse 1644 reads "சித்தஞ் சிவமாகச் செய்தவம் வேண்டாவால்". Correct; the spelling differs (ம்/ஞ்), which is why the threshold is 0.2.
5. **2303** (the table says 2300): "வெல்லும் அளவில் விடுமின் வெகுளியை" is exactly line 1 of verse 2303. The table's number is misprinted or follows a slightly different count in tantra 8.

Base-text spot checks: 1892 (number inferred) is the first verse of "முத்திரை பேதம்" and is followed by a printed 1893 with chapter_verse 2. 2687 (printed 2667) sits between 2686 and 2688. 997 carries the subheading "தம்பனம்" and the next three verses carry "மோகனம்", "உச்சாடனம்" and "மாரணம", as printed.

## Copyright and sidecar map

| Source | Person | Date | Status |
|---|---|---|---|
| Base text | Tirumular | c. 6th-8th century or earlier | public domain |
| `sengalvaraya_parallels` | V. S. Chengalvaraya Pillai (1883-1971) | published 1951 | **modern**: the author died in 1971, so the work is in copyright in India until the end of 2031 (60 years after death). |

The parallels mostly quote older public-domain works (Thevaram, Kural, Thiruppugazh, Kandar Alangaram), but the selection and arrangement are his.

Sidecar map:

```json
{"tirumanthiram": {"sengalvaraya_parallels": {"rights": "modern", "person": "V. S. Chengalvaraya Pillai", "died": 1971, "published": 1951}}}
```

## Text problems

**Misprinted verse numbers.** These are corrected in the script's `MISPRINTS` table. Each correction is keyed on (file, printed number, previous number) and printed at run time.

| File | Printed | True | Context |
|---|---|---|---|
| pmuni0010_01 | 2014 | 2104 | between 2103 and 2105 |
| pmuni0010_03 | 2667 | 2687 | 2686, *2667*, 2688 |
| pmuni0010_03 | 2943, 2944 | 2843, 2844 | 2842, *2943*, *2944*, 2845 |
| pmuni0010_03 | 2707 | 2907 | 2906, *2707*, 2908 |
| pmuni0010_03 | 2903-2905 | 3003-3005 | 3002, *2903-2905*, 3006 |
| pmuni0010_03 | 3219 | 3019 | 3018, *3219*, 3020 |

**Other numbering problems:**
- **1892**: the verse's number is missing. The verse follows the heading "17. முத்திரை பேதம்" and comes before 1893. The script inferred the number and marked the record with `number_inferred: true`.
- **526**: the number shares a line with the first verse line ("526..தெளிவுறு…"). It is handled.
- **74, 153, 299**: printed without the full stop. They are handled.
- **Local (in-chapter) numbers** are misprinted or run on at 1559, 2329-2330, 2630 and 3020-3021. Within tantra 8 (2527, 2537, 2546, 2566) and tantra 9 chapter 8 (2724-2762), the in-chapter count continues across headings instead of restarting. These are kept as printed in `chapter_verse`.

**Encoding corruption:**
- In 61 verses (almost all in `pmuni0004` and `pmuni0009_01`), "ரி" appears as "ா஢" (for example "போ஢ன்பம்" for "பேரின்பம்") and "ளி" appears as "ௌi" (for example "வௌiயில்" for "வெளியில்"). These are old TSCII conversion faults with an unambiguous fix, so they are repaired in `tamil`, and the original is kept in `tamil_source`.
- **25 verses still contain stray Latin letters or backslashes inside words** and are listed in `corrupt_lines`: 678, 822, 823, 825, 956, 1002, 1038, 1082, 1113, 1118, 1129, 1147, 1502, 1609, 1666, 1749, 1864, 1903, 2158, 2358, 2375, 2419, 2474, 2714, 2931. Examples are "ஞ்aனமுந்", "புலர்fந்தது", "Yமூக்கு" and "தீப miடல்". They were not repaired because the intended letter is not certain.
- 342 has "பொங்குன்ய்", which is probably a typo.

**Stray or doubled lines** (kept in `extra_lines`, outside `tamil`):
- 324: a stray "கா".
- 427: a sixth line, "குய்த்தசங் காரம் சிவமாகும் உண்மையே.", printed as an alternative reading "(1)".
- 500: line 4 is printed twice; the first copy ends in a stray "வரன்றே".
- 1970: line 4 is repeated.

**Headers and notes inside the text:**
- Tantra 2 chapter titles 9-14 and 19, and tantra 3 chapter 19, have variant titles in footnotes (for example படைத்தல் / "சிருஷ்டி"). The script reports these but does not store them.
- `pmuni0009_03` has a revision note inside the body before the footer. It is dropped.
- Tantra 9 chapter 8 has no heading of its own, only sections 8.1-8.6. The chapter is named after 8.1, "திருக்கூத்து தரிசனம்".
- "2, உடல்விடல்" (tantra 8) and "21 தோத்திரம்" (tantra 9) are headings with irregular punctuation. They are handled.

## Suggested unit for later marking

**Mark per verse.** Each Tirumanthiram verse is a self-contained four-line stanza with its own doctrine or image, much like a Kural or a Naladiyar quatrain. The work is not made of hymns or decades. Its chapters (adhikarams) vary from 1 to over 80 verses and are thematic headings, not poems. Marking per pathigam would therefore not fit. The chapter and subheading should travel with each verse as context, and chapters or tantras can be used for later grouping and thread-building.

The missing 1155-1418 should be recorded as a known gap, so that tantra 4 is not read as complete.
