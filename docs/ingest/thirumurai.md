# Ingest report: the Saiva Thirumurai (`thirumurai`)

Scope: Thirumurai 1-7 (Thevaram), the Thirukkovaiyar part of 8, 9 (Thiruvisaippa and Thiruppallandu),
11 and 12 (Periya Puranam). Tiruvasagam and Tirumanthiram are left to the other agents.

- Script: `scripts/parse_thirumurai.py` (standard library only; run `python3 -I scripts/parse_thirumurai.py`;
  reads only `data/text/`; prints counts, then every numbering or text problem it found)
- Output: `kg/core/thirumurai.jsonl`, 14,580 records in canonical order (1-7, the Thevaram appendix,
  8, 9, 11, 12)
- Every part was parsed. The one gap is in the corpus itself: the file for Thirumurai 6 part 1 is cut
  short (see below).

## 1. Files

| Thirumurai | Catalog rows | Files used |
|---|---|---|
| 1 Sambandar | 246, 247 | pmuni0150, pmuni0151 |
| 2 Sambandar | 257, 266 | pmuni0157, pmuni0162 |
| 3 Sambandar | 278, 284 | pmuni0173, pmuni0179 (this file also holds a 33-verse appendix, "பிற்சேர்க்கை") |
| 4 Appar | 286, 287 | pmuni0181, pmuni0182 |
| 5 Appar | 292, 294 | pmuni0186, pmuni0188 |
| 6 Appar | 298, 302 | pmuni0192, pmuni0196 |
| 7 Sundarar | 315, 320 | pmuni0207, pmuni0211 |
| 8 Thirukkovaiyar | 113, 114 (same file) | pmuni0054 |
| 9 | 155-161 (one file) | pmuni0092 (all nine poets, including Sethirayar and Purudothama Nambi, who have no catalog row of their own, and Sendanar's Thiruppallandu) |
| 11 | 204-214 | pmuni0127_01, pmuni0127_02 |
| 12 Periya Puranam | 317/318, 324/325, 328/329, 335-338 | pmuni0209, 0215, 0218, 0224, 0225, 0226, 0227 (all 13 sarukkams; 0227 runs from sarukkam 7 to the end, though the catalog stops at "சருக்கம் 6; பகுதி 4") |
| Translation | 1170 | pmuni0999, Kausalya Hart, Appar's Thevaram pasurams 1-1000 in English |
| Commentaries | 631, 875, 914 | pmuni0493 (Nachinarkkiniyar), pmuni0735 (S. Vaiyapuri Pillai), pmuni0774 (Sundara Shanmuganar), all on Thirumurugattruppadai (11th Thirumurai, work 5.9) |

Rejected:
- pmuni0126 (row 204-212 text id): an older TSCII-converted copy of pmuni0127_01 (49 lines differ, all
  conversion errors such as `§க்ஷ`). I used the Unicode file pmuni0127_01.
- pmuni0106 (rows 177-178, "திருக்குற்றாலப் / திருக்குறும்பாலப் பதிகம்", Sambandar): the file holds
  Rasikamani T.K.C.'s 1937 essay on the Kuttrala Kuravanji. It is catalogued wrongly and has no Thevaram text.
- Rows 20 (Thirumangai's Siriya Thirumurai), 47-48 and the other Thiruvarutpa "திருமுறை" rows (Ramalinga
  Adigal), and row 9 (Periyalvar's Thiruppallandu): not Saiva Thirumurai.
- Works about the Thirumurai, not part of it: pmuni0213 Thirumurai Kanda Puranam and pmuni0216 Sekkizhar
  Puranam (Umapathi Sivam), pmuni0190 and pmuni0987 (pillaitamil poems), pmuni0325 Thiruthondar Malai,
  pmuni0851 Thiruthondar Satakam, pmuni1069 Sundarar Ula, pmuni0773 (Thiru. Vi. Ka.), pmuni0526
  (Rasamanickanar on Sekkizhar), pmuni1015_01/02 and 1017_01/02 (Ki. Va. Ja., Nayanmar stories in prose).
  None of them is a translation or commentary that can be aligned verse by verse.
- No other translation or commentary of any Thirumurai text is in the catalog.

## 2. Record shape

Every record has `id`, `thirumurai`, `pathigam`, `verse`, `number` (running number within the
Thirumurai, counted by the parser), `printed_number` (the running number the file prints),
`work`, `poet`, `tamil` (list of lines), `notes` (footnotes and variant readings printed with the verse),
`source`, `hart`, `nachinarkkiniyar`, `vaiyapuri_pillai` and `sundara_shanmuganar`.
Other fields depend on the part:

| Part | id | Extra fields |
|---|---|---|
| Thevaram 1-7 | `thirumurai:B.P.V` (book.pathigam.verse, the traditional numbering) | `thalam`, `pathigam_title`, `form` (திருவிராகம், திருத்தாண்டகம் ...), `pan`, `swami`, `devi`, `pathigam_notes` (the edition's note on the temple), `lost_verses` (verses the edition says are lost) |
| Thevaram appendix | `thirumurai:3.A1.1` to `3.A3.11` | `appendix` (1-3), `pathigam` null, `number` null, `thalam`, `pan` |
| 8 Thirukkovaiyar | `thirumurai:8.kovai.N` (N = 1-400) | `pathigam` = `athikaram` (1-25), `athikaram_title`, `iyal` (களவியல் / கற்பியல்), `turai_no`, `turai`, `kolu` |
| 9 | `thirumurai:9.P.V` (P = 1-29 across the book) | `poet_pathigam` (the pathigam's number under its poet, as the file prints it), `thalam`, `pathigam_title` |
| 11 | `thirumurai:11.A.W.V` (A.W = the edition's author.work number, e.g. 2.4 Arputha Thiruvandhadhi) | `work_no`, `work` (the title of the work) |
| 12 | `thirumurai:12.S.P.V` (sarukkam.purana.verse, as the edition prints it) | `sarukkam`, `sarukkam_title`, `purana`, `purana_title`, `heading` (the "சுந்தரமூர்த்தி சுவாமிகள் துதி" line before each sarukkam's closing verse) |

`thalam` is taken from the pathigam heading (the part before the form name). For the 27 general (பொது)
pathigams, such as நமச்சிவாயப்பதிகம் and தனித் திருநேரிசை, it is null. Joint headings like
"திருப்புகலியும் - திருவீழிமிழலையும்" are kept as printed. `swami` and `devi` come from the edition's
note under each pathigam and are missing where the note is missing.

## 3. Counts against the traditional numbers

| Thirumurai | Units | Places | Expected | Notes |
|---|---|---|---|---|
| 1 | 1,469 | 136 pathigams | 1,469 | matches |
| 2 | 1,331 | 122 | 1,331 | matches |
| 3 | 1,347 + 33 | 125 + 3 appendix | 1,347 | matches; the appendix holds 3 pathigams found later (Thiruvidaivay from a 1917 inscription, Thirukkiliyannavur, Thirumaraikkadu), outside the canonical numbering |
| 4 | 1,070 | 114 headings | 1,070 | matches the edition; it prints 114 pathigam numbers where some editions count 113 |
| 5 | 1,016 | 100 | 1,016 in this edition (1,015 in some counts) | matches the edition |
| 6 | **882** | 90 | 981 | **99 verses missing: pmuni0192 stops partway through 6.41.2 (running number 409; its last line is missing). 6.41.3 to 6.50 (running numbers 410-508) are not in the corpus.** pmuni0196 starts at 6.51 |
| 7 | 1,026 | 100 | 1,026 | matches |
| 8 | 400 | 25 athikarams | 400 | matches. The two prefatory verses (Vinayakar and the "நூற்சிறப்பு"), later additions, are left out |
| 9 | 301 | 29 pathigams | 301 | matches (Thiruvisaippa 288 + Thiruppallandu 13) |
| 11 | 1,419 | 41 works | 1,419 | matches the edition's 1-1419 (the edition lists Nakkeerar's and Kalladar's Thirukkannappar Thirumaram separately, hence 41 works rather than the usual 40). Thirumurugattruppadai and the long ulas and agavals are one unit each |
| 12 | 4,286 | 78 sections | 4,286 | matches the usual count. The edition's own running numbers end at 4,281 because they overlap at 1899-1903 and slip elsewhere. Sections: 13 sarukkams with the payiram and the four opening chapters, 72 puranas, and 6.1 (Sambandar, 1,256 verses), split across pmuni0224 and pmuni0225 |

Lost verses: where the edition says a verse is lost ("இப்பதிகத்தில் 7,8,9-ம் செய்யுட்கள் சிதைந்து
போயின. 5.78.7-9"), the verse numbers skip it and the record carries `lost_verses`. For example, 1.5 runs
1, 3-11; 4.46 has only 1-2; 4.110 has 1, 2 and 10. Where printed numbers skip and no loss is noted,
the gap is treated as a misprint and the verses are numbered by position.

## 4. Alignment

| Field | Units aligned | Method |
|---|---|---|
| `hart` (Kausalya Hart, English) | 999 of Appar's verses, 4.1.1 to 4.104.8 | Her pasuram numbers 1-1000 follow the same edition's running numbers. Each pasuram goes to the Tamil verse with that running number, but only if that verse falls in her padiham or the one next to it. Her padiham 92 covers PM 4.92 and 4.93, so her 93-103 are PM 4.94-4.104. Her number 883 is missing from her file. Pasurams 587 and 696 sit under the next padiham's heading in her file and matched the Tamil Ravana verse that ends the previous pathigam (4.60.10, 4.71.10), which is correct |
| `nachinarkkiniyar`, `vaiyapuri_pillai`, `sundara_shanmuganar` | 1 unit each: `thirumurai:11.5.9.1`, the Thirumurugattruppadai agaval | Each commentary covers the whole poem, which is one unit here. Each field is `{"source", "text"}`, holding the file's full text (134k, 40k and 39k characters). The ten venbas after the agaval (11.5.9.2-11) are later additions that these editions do not cover, so their fields are null. Thirumurugattruppadai is also the first poem of the Sangam Pathuppattu. If another agent ingests the Pathuppattu, its line-level alignment of these commentaries is finer than mine |

Spot checks I read:
1. `thirumurai:4.1.1` "கூற்றாயின வாறுவிலக்ககிலீர்": Hart "This sickness is Yama to me, you have not
   cured it ...". Correct (Appar's colic hymn at Adhigai).
2. `thirumurai:4.11.1` "சொற்றுணை வேதியன் சோதி வானவன்": Hart "He is the words of the Vedas ... Even if I
   were tied to a stone and dropped in the ocean, Namashivaya would be my help". Correct.
3. `thirumurai:4.60.10` "பொருகடல் இலங்கை மன்னன்": Hart 587 "He pushed the king of Lanka ... god of
   Thirupperuvelur". Correct, across her misplaced padiham heading.
4. `thirumurai:4.94.1` Thirukkandiyur "வானவர் தானவர் வைகல்": Hart 903 "All the gods of the sky brought
   flowers ...". Correct after the one-padiham shift.
5. `thirumurai:4.104.7` Thirunagaikkaronam: Hart 999 "O lord of Thirunakaikkaronam surrounded by waves".
   Correct.
I also read: 1.1.1 (pan நட்டபாடை, deity பிரமபுரீசர் / திருநிலைநாயகி), 8.kovai.30 (turai வற்புறுத்தல்,
printed number 34), 9.1.1 (ஒளிவளர் விளக்கே), 9.29.13 (last Pallandu verse), 12.1.0.1 (உலகெலாம்),
12.3.3.1 (Kannappar) and the three commentary heads on 11.5.9.1.

## 5. Copyright (sidecar map)

The Tamil texts are 6th-12th century and public domain. The editions' footnotes, temple notes and
kolu glosses come with the Project Madurai files.

```json
{
  "hart":                {"who": "Kausalya Hart", "date": "not given in the file (Project Madurai release, with her permission)", "rights": "modern"},
  "sundara_shanmuganar": {"who": "Sundara Shanmuganar (1922-1997)", "date": "not given in the file (Tamil Virtual Academy scan)", "rights": "modern"},
  "vaiyapuri_pillai":    {"who": "S. Vaiyapuri Pillai (1891-1956)", "date": "4th ed. 1946", "rights": "modern"},
  "nachinarkkiniyar":    {"who": "Nachinarkkiniyar (14th c.), U. Ve. Saminatha Iyer's edition (d. 1942)", "date": "3rd ed. 1931", "rights": "public domain"}
}
```

Vaiyapuri Pillai's work is out of copyright in India (60 years after his death, so from 2017) but may not
be elsewhere. I marked it `"modern"` to be safe. Change it to `"public domain"` if Indian terms are
enough for you.

## 6. Text problems

The script prints every one of these. Run it to see the full list.
- **Truncated file:** pmuni0192 (Thirumurai 6 part 1) ends partway through 6.41.2, which keeps 7 of its
  8 lines. Verses 409-508 are missing.
- **Missing or wrong headings:** there is no heading for 1.14 (split off 1.13 by its verse numbers) or
  for 5.54 (split off 5.53). Pathigams 4.34-4.36 print the verse numbers of the pathigam before them
  (4.33.x for 4.34, and so on). The headings win and the 30 verses are reported.
- **Misprinted verse numbers** (verses renumbered by position, about 70 cases). Examples: "1.105.6,7,8"
  for verses 3-5; "101" for 10 in 3.18, 3.29 and 3.44; "4.16" for 4.1.6; "3.1232" for 3.123.2;
  "4.71..1"; "6.83.1" for the last verse of 6.83-6.87. In Kovaiyar the verse numbers run 34, 35, 36, 37,
  38, 37 where 30-35 belong, and 350-352 slip. Kovaiyar is numbered by position against its 400 turai
  titles. In the Periya Puranam the running numbers overlap (1899-1903 printed twice, 1377-1380, 1611-1614)
  and skip (1567-1570, 1667-1670). The parser's own `number` counts 1-4,286.
- **The contents lists disagree with the text** for 35 Thevaram pathigams. These are mostly typos in the
  ranges ("6-77", "4104-413", "698-798") or ranges that overlap. The totals match the text.
- **Footnotes inside verses:** footnote markers stuck to verse lines ("*நாட்டமிகு", "(*)கோது") and
  footnotes that follow a verse ("(*) போதுசாற்றி என்றும் பாடம்") are separated into `notes`. Two footnotes
  print a number of their own ("4 1 தரைத்தேவர்" in 2.73, "12 3 நட்சத்திரங்களாவன" in 2.85) and are folded
  into the verse before them. Lines starting with `#` in pmuni0207 are footnote marks, not headings.
- **Lacunae:** 6.64.5 is mostly "... ..."; 11.8.1.14 (running number 685) has a dashed first line;
  2.96.11 has a dashed line.
- **Duplicates:** 12.6.2 prints the verse numbered 3455 twice; the second copy is dropped. The text of
  5.9.7 is repeated as 5.10.10 in the source; both are kept.
- **Headings inside poems:** Thirumurugattruppadai's six section titles ("1 திருப்பரங்குன்றம்" ...) look
  like verse numbers and are kept as lines within the one agaval unit. The edition prints its
  line-count marks ("05", "(10)") on 1.128 (Thiruvezhukutrirukkai) and the agavals; they are removed.
- **Small leftovers:** a few verses still end in a stray number or mark, for example 5.95.11 "... 11"
  and 11.5.4.1 "...55" (7 lines in all). Kovaiyar 74 has no kolu, and 273 is printed over 5 lines.
- **Catalog:** rows 113 and 114 point to the same file, as do 317 and 318 and the other paired Periya
  Puranam rows. Row 338's title stops at sarukkam 6, but pmuni0227 runs to sarukkam 13.

## 7. Suggested unit for marking

- **Thevaram and Thiruvisaippa (Thirumurai 1-7 and 9): mark per pathigam (about 800 hymns plus 29),
  and keep verse ids for quoting.** A pathigam is a single composition. It is sung to one pan at one
  temple, its verses share a refrain and a fixed plan (verse 8 on Ravana, 9 on Brahma and Vishnu, 10 on
  the Jains and Buddhists, 11 the poet's signature), and its verses repeat one another closely. Marking
  8,000-odd verses one by one would mostly record the same themes ten times. Where a single verse
  stands out (Namasivaya, the Thiruthondathogai's list of saints in 7.39), attach the mark at verse
  level.
- **Thirukkovaiyar: mark per verse.** Each of the 400 verses is a separate turai (situation) with its
  own kolu, and its meaning depends on that situation.
- **Eleventh Thirumurai: mark per verse in the antadis and kovais (Arputha Thiruvandhadhi, Ponvannatthu
  Andadhi and the others), and per work for the single long poems** (the ulas, Thirumurugattruppadai,
  the agavals). These long poems are one unit each here.
- **Periya Puranam: mark per episode, not per verse.** It is narrative, so single verses rarely carry a
  theme alone, and one record per purana is too coarse for the long ones: 6.1 Sambandar has 1,256
  verses and 5.1 Appar has 429. Mark short puranas (under 20 verses) whole, and split long ones into
  blocks of about 10-15 verses, broken at the narrative scene where possible.
