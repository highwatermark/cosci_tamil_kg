# Purananuru ingest report

Outputs:
- `/Users/harilakshmanan/Cursor/cosci_knowledge_graph/scripts/parse_purananuru.py` (standard library only; run `python3 -I scripts/parse_purananuru.py`; reads only `data/text/`)
- `/Users/harilakshmanan/Cursor/cosci_knowledge_graph/kg/core/purananuru.jsonl` (398 records, in order 1–400 without 267 and 268)

## Record shape

| field | content |
|---|---|
| `id` | `purananuru:N` |
| `number` | traditional poem number (1–400) |
| `title` | the modern title printed in the PM e-text (e.g. "இறைவனின் திருவுள்ளம்!"), not traditional |
| `poet`, `patron` | from the colophon; null when the colophon says the name is unknown (தெரிந்தில) or has none |
| `thinai`, `thurai` | from the colophon; alternative readings joined with "; " (e.g. 98 `வாகை; வஞ்சியும்`) |
| `note` | the e-text's குறிப்பு / சிறப்பு / bracketed notes (modern editorial) |
| `colophon_raw` | the colophon lines exactly as printed, so nothing parsed away is lost |
| `tamil` | poem lines; `tamil_source` says which file they came from |
| `filled_from_duraisamy_pillai` | the fields filled from the commentary where the base text had none |
| `duraisamy_pillai` | `{source, heading, tamil, colophon, commentary}`: his file, his section heading (usually the patron, otherwise the poet), his version of the poem lines (older, sandhi-joined spelling; line numbers stripped), his colophon sentence, and the whole commentary (introduction, colophon, உரை, விளக்கம்) as paragraphs joined by newlines |
| `rights` | per-part rights (see the sidecar map below) |
| `repairs` | ids of this poem's entries in `kg/core/purananuru_repairs.jsonl` (changes made by `scripts/repair_purananuru.py`, and readings kept against another edition) |

## Files used

| catalog row | file(s) | what | used for |
|---|---|---|---|
| 117 | `pmuni0057` | the text (PM 2000), with modern titles and colophons | base text: numbering, colophon, lines |
| 632 | `pmuni0494_01`, `_02`, `_03` | Avvai S. Duraisamy Pillai, text + commentary, poems 1–60, 61–130, 131–200 (Kazhagam 1947, reprinted 1960) | `duraisamy_pillai` for 1–200 |
| 669 | `pmuni0531_01`, `_02`, `_03` | the same, poems 201–270, 271–340, 341–400 | `duraisamy_pillai` for 201–400 |

Rejected: row 910, `pmuni0769` (புறநானூற்றுச் சிறுகதைகள், Mullai PL. Muthiah): short stories retold for students, not a translation or commentary aligned to poems. The PDFs were not used. No English translation of the Purananuru is in the corpus.

How alignment works: the base text is split on its sequential `N.` lines. Duraisamy Pillai's sections are found by their `N. heading` lines in sequence (after the front matter and indexes, which also contain numbered lines). Inside each section the poem is the run of short-line blocks that best matches the base poem by letter trigrams (Jaccard ≥ 0.2, adjacent blocks included when a blank line splits the poem). Everything else in the section is commentary. All 398 matched with similarity ≥ 0.35, so no section is assigned to the wrong poem.

## Counts

- Traditional count: 400, with 267 and 268 lost. Both files agree: the base text goes from 266 to 269 with the note "267- 268 கிடைத்தில", and Duraisamy Pillai prints "267 ... ..." and "268 ... ..." as empty placeholders. Units: **398**. Nothing is missing or doubled; numbering is sequential in all seven files.
- Fields after filling: poet 385, patron 241 (many பொதுவியல்/காஞ்சி poems name no patron), thinai 394, thurai 393. Poet is null for 13 poems: 256, 257, 297, 323, 327, 328, 333, 339, 340, 355 and 361 are marked unknown in the colophon, 244's colophon is destroyed, and 263 has empty labels. Where a colophon gives a name and then says the rest is unknown (282, 289), the name is kept and the unknown fields are null.
- Duraisamy Pillai: aligned to **398/398** poems. All 398 have his poem lines and commentary, and 393 have his colophon sentence. The 5 without a colophon: 1 (invocation, none), and 187, 327, 333, 338, where the colophon is run into the introduction.
- Filled from Duraisamy Pillai where the base text has nothing: 99 (poet, patron, thinai, thurai), 194 (poet, thinai, thurai), 200 (all lines, poet, patron, thinai, thurai), 244 (thinai, thurai), 298 and 312 (poet, thinai, thurai), 380 (poet, patron, thinai, thurai). His "திணையும் துறையும் அவை" and "திணை: அது" ("the same") are resolved to the previous poem's values.

## Five spot checks (read)

1. **18** (குடபுலவியனார் to பாண்டியன் நெடுஞ்செழியன், பொதுவியல் / முதுமொழிக் காஞ்சி): base 30 lines and DP 30 lines, both from முழங்கு முந்நீர் to தள்ளா தோரே. His colophon names the same poet and patron. The commentary opens on the patron's Talaiyalankanam victory and ends in விளக்கம். Correct.
2. **112** (பாரி மகளிர், அற்றைத் திங்கள்): 5 lines in both. DP heading வேள் பாரி. His colophon "பாரிமகளிர் பாடியது". Correct.
3. **192** (கணியன் பூங்குன்றன், யாதும் ஊரே): 13 lines in both. The commentary opens with the poet's village (Mahibalanpatti). Correct.
4. **235** (ஔவையார் on அதியமான் நெடுமான் அஞ்சி, கையறுநிலை): base 19 lines, DP 20 (a lineation difference). Same first and last line. Correct.
5. **394** (மதுரைக் குமரனார் to சோழிய ஏனாதி திருக்குட்டுவன், கடைநிலை): its heading is printed `394.சோழிய...` with no space. It is caught, and the 18-line poem and commentary are aligned. Correct.

Also checked: the last section of every file (60, 130, 200, 270, 340, 400) ends at its last விளக்கம். The script strips Project Madurai's "This file was last updated…" note and the book's closing line from the commentary.

## Rights sidecar map

```json
{
  "purananuru.tamil":            {"rights": "public_domain", "note": "Sangam poems, c. 1st–3rd c. CE"},
  "purananuru.poet/patron/thinai/thurai": {"rights": "public_domain", "note": "traditional colophons"},
  "purananuru.title":            {"rights": "modern", "note": "modern titles in the PM e-text (2000); editor not named, so treat as in copyright"},
  "purananuru.note":             {"rights": "modern", "note": "modern குறிப்பு/சிறப்பு notes in the PM e-text; editor not named"},
  "purananuru.duraisamy_pillai": {"rights": "modern", "note": "Avvai S. Duraisamy Pillai (1903–1981); commentary 1947 (vol. 1) and 1950s (vol. 2), SISSW Publishing Society; in copyright in India until 2041 (life + 60). Quote at most a few words."}
}
```

The same map is written into each record's `rights` field. Project Madurai's licence allows redistributing the e-texts, but that does not clear the underlying copyright in the commentary.

## Text repairs (2026-11-25)

`python3 -I scripts/repair_purananuru.py` reruns `parse_purananuru.py` and then repairs the base
text, so the build is always parse + repair. Every change is logged in
`kg/core/purananuru_repairs.jsonl` (poem, line, old, new, authority, the other editions'
readings); readings kept where the editions differ are logged there too (`"action": "kept"`) and
flagged in `kg/core/sangam_text_flags.jsonl`. Authorities: tamilvu.org's verse text (library
l1280, U. V. Swaminatha Aiyar's edition) and the poem lines of Duraisamy Pillai's edition in the
Project Madurai files. `duraisamy_pillai.tamil` and `colophon_raw` are left as printed.

187 changes:
- 86 `-ஒடு` endings (யடு/ளடு → யொடு/ளொடு). pmuni0057 has no யொ or ளொ anywhere, so the sign was
  lost in encoding. The rule only touches யடு/ளடு at a word end or before -ம், and the script
  stops if it finds a place not checked against both editions (அடுக்கத்து in 200 is left alone).
  In 159 and 320 tvu reads -ஓடு, and dp reads -ஓடு in 159, 250, 310, 328 and 395 (logged).
  2 more lost ொ inside words (31 நீயொல், 109 விரையொலி).
- 51 stray-character fixes in 37 poems: backticks made ‘ ’ / “ ”, underscores made the base
  text's dash `-` (in 24 removed); 6 font-junk fixes (69, 100 ×2, 283, 352, 373). In 283, 352 and
  373 the junk stood for lost letters, so it is removed and the lacuna kept; dp's fuller readings
  are logged, not adopted.
- 14 misprints: 84 (ஜ் → னை, போறெதிர்ந்து), 209 (stray space), 269 (குரூஉ), 361 (பஃறேர்), and
  non-words found while collating: 56, 88 ×4, 109, 126, 152, 160, 215.
- 19 line-gap repairs adding 22 lines in 16 poems (48, 58, 77 ×3, 86, 88, 116, 160 ×2, 209, 230,
  235, 325, 371, 377, 378, 384, 386), and 126's first line split in two. Most are eye-skips where
  the base joins the start of one line to the end of a later one. Both editions have every
  restored line. Inserted lines are in tvu's spelling.
- 8 colophon fixes: thurai of 5 (செவியறிவுறூஉ) and 336 (மகட்பாற் காஞ்சி); poet and patron of 15
  (நெட்டிமையார், பாண்டியன் பல்யாகசாலை முதுகுடுமிப் பெருவழுதி; the base repeats 14); poet of 144
  and 145 (பரணர்; the base repeats 143's கபிலர்), and 145's remark on the poet moved from thurai
  to note.

Kept and flagged (21): line differences where only one edition has more (355, 366, 382, 383,
384 line 5 and 209 line 10, which dp has and tvu lacks; 283 line 3 where tvu reads differently;
48 and 147, where dp lacks a line); 393 கூமை/கூர்மை; 7 probable misprints that are real words
(69 முழுவதுடன், 77 இகழ்ந்தன்றும், 160 குனிப்ப, கோடின்றாக, நல்குவை, வருங்கலம், 361 கொன்றுதன்);
poets of 298 (tvu ஆலியார்) and 381 (tvu நன்னாகனார்).

## Text problems (as found at ingest)

Repaired (each one is printed by the script):
- **64**: the base text puts 9 lines of poem 326 (அருமிளை இருக்கை யதுவே…பெரும்பரி சிலனே) before the real poem. They are dropped because they are printed again in 326 and are not in Duraisamy Pillai's 64.
- **99/100**: the base text's last two lines of 99 (வட்கர் போகிய வளரிளம் போந்தை / உச்சிக் கொண்ட ஊசி வெண்தோட்டு) are lines 3–4 of 100. They are moved, as Duraisamy Pillai prints them. Base 99 also has no title and no colophon.
- **200**: the base text has only "??? ???" for the poem. The 17 lines are taken from Duraisamy Pillai (`tamil_source: pmuni0494_03`) in his older spelling.
- `·` changed to `ஃ` in the base text (35 places, an old encoding leftover, e.g. ப·றேர்). 252 zero-width characters removed from the commentary files. A colophon line printed as `ணை:` is read as `திணை:`.

Not repaired (left as printed):
- No colophon in the base for 99, 194, 200, 298, 312, 380 (filled from the commentary as above). The 244 colophon says the poem and its names are destroyed. 263 has empty பாடியவர் / பாடப்பட்டோர் labels.
- Lines missing in the base where Duraisamy Pillai has them: **77** (base 10 lines, DP 13), **371** (base starts at line 3; the first two lines, அகன்றலை வையத்து…, are lost). His lines are in `duraisamy_pillai.tamil` for those poems.
- Lacunae (". . .") from damaged manuscripts in 40 poems: 244, 249, 282, 283, 285, 288, 306, 317, 321, 323, 328, 333–335, 337, 339–341, 344, 346, 347, 352, 353, 355, 357, 366, 370, 371, 373, 377, 379, 380, 383, 384, 390, 393, 396, 398–400. These are real gaps in the tradition and Duraisamy Pillai has them too.
- Corrupted characters: 69 `வ¨ளைப்`, 100 `பு¨ ழல்` (புனைகழல்) and `பசும்புண்;னக`.
- Lineation differs by 2 lines between the editions in 55, 160, 325, 383 (split or joined lines). The wording is the same.
- Colophon variants left as printed: `நொட்சி` (2) for நொச்சி; 8's patron carries an alias ("…என்பவனும் இவனே"); 65's patron line runs into a note.
- In Duraisamy Pillai, headings 22 and 25 have no period and 394 has no space after the period. The 1–200 files close each poem with "(N)" and the 201–400 files do not. His section heading is the patron for most poems and the poet where there is no patron, so it is kept as `heading` and not used as a patron except where the base has no colophon at all.

## Suggested unit for marking

**Per poem.** Each Purananuru poem is a separate, complete occasion poem with its own poet, patron and thinai/thurai (4 to about 40 lines, 5,440 lines in all, average 13.7). It is not a stanza of a hymn, so there is no larger unit like a pathigam to mark instead. Runs of poems on one patron (for example 87–104 on Athiyaman, 105–120 on Pari, 131–136 on Ay) and the thinai/thurai labels are better used as threads and groupings at the linking stage than as marking units.
