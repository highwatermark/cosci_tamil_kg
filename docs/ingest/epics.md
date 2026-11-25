# The five great epics and the five minor epics: ingest report

Outputs:
- `scripts/build_epics_core.py` (standard library only; run `python3 -I scripts/build_epics_core.py`;
  reads only `data/text/`; nothing was downloaded, every source was already mirrored there)
- `kg/core/silappathikaram.jsonl` (35 records) and `kg/core/silappathikaram_units.jsonl` (434 units)
- `kg/core/manimekalai.jsonl` (31 records) and `kg/core/manimekalai_units.jsonl` (288 units)
- `kg/core/civaka_cintamani.jsonl` (3,145), `valayapathi.jsonl` (72), `kundalakesi.jsonl` (19),
  `soolamani.jsonl` (2,128), `neelakesi.jsonl` (885), `naga_kumara_kaviyam.jsonl` (170 + the
  invocation), `udayana_kumara_kaviyam.jsonl` (367), `yasodhara_kaviyam.jsonl` (330)
- flags appended to `kg/core/sangam_text_flags.jsonl`, each tagged with its `book`

The builder rewrites only its own books' flags in the shared flags file and keeps every other
book's flags in place and in order. `scripts/build_sangam_core.py` writes that file from scratch,
so after running it, run this builder again.

## Files used

| Work | Project Madurai files | What they hold |
|---|---|---|
| Silappathikaram | `pmuni0046`, `pmuni0111_01`, `pmuni0111_02` | the three kandams, text alone |
| Manimekalai | `pmuni0141` | text alone, line marks `KK-LLL` every ten lines |
| Civaka Cintamani | `pmuni0664_01/_02`, `pmuni0670_01/_02`, `pmuni0672_01/_02/_03` | verse with P. V. Somasundaranar's commentary (Kazhagam) |
| Valayapathi | `pmuni0062` | the collected fragments, with a modern preface |
| Kundalakesi | `pmuni0507` | the collected fragments, with commentary |
| Soolamani | `pmuni0035_01` (1-238, numbered), `pmuni0035_02` (1-826, unnumbered), `pmuni0602_01`, `pmuni0602_02` (827-2130) | text, with modern headings over most verses |
| Neelakesi | `pmuni0538` | text, with modern headings |
| Naga Kumara Kaviyam | `pmuni0601` | verse with a modern prose rendering |
| Udayana Kumara Kaviyam | `pmuni0597` | verse with commentary |
| Yasodhara Kaviyam | `pmuni0508_01`, `pmuni0508_02` | verse with Avvai S. Duraisamy Pillai's commentary and variant readings |

Not used: `pmuni0451` (Silappathikaram, Pukar kandam with commentary), `pmuni0509` and `pmuni0818`
(abridgements of the Cintamani and Manimekalai), `pmuni0549` (Valayapathi with commentary),
`pmuni0338` (a later Kundalakesi collection). They could serve as second witnesses later.

Only verse lines are kept. Prefaces, commentary, prose renderings, footnotes, modern headings over
verses, variant-reading marks (`* † ‡ § $ +`) and editors' notes are dropped. The sangamtamil.com
copy was read only to compare Tamil letters; nothing (and none of Dikshitar's English) was taken
from it.

## Record shapes

**Silappathikaram and Manimekalai** (`kg/core/<book>.jsonl`), one record per kaathai, whole:

| field | content |
|---|---|
| `id` | `silappathikaram:N` (0 = patikam, 1-30), `silappathikaram:pukar_kandam_katturai`, `:madurai_kandam_katturai`, `:vanchi_kandam_katturai`, `:nool_katturai`; `manimekalai:N` (0 = patikam) |
| `kind` | `patikam`, `kaathai`, `kandam_katturai`, `nool_katturai` |
| `short_name`, `title`, `kandam` | romanised name, the Tamil title as the e-text heads it, the kandam (Silappathikaram) |
| `line_count`, `printed_last_line` | lines kept; the last line number printed in the e-text |
| `blocks` | runs of lines between rubrics: `{label, start, end}`; the label is the metre or rubric printed above (`(நிலைமண்டில ஆசிரியப்பா)`, `வேறு (ஆற்று வரி)`, `உரைப்பாட்டு மடை`, `கொளு`, `தேவந்தி சொல்`, `வெண்பா` ...). Rubrics are never verse lines |
| `songs` | in the vari and kuravai kaathais: `{n, start, end, block_label}`, the e-text's song numbers |
| `song_kaathai` | true for 7, 12, 17, 24, 29 (Silappathikaram) |
| `interpolation_note_lines` | 22 only: the line spans an editor's note (stripped) says commentators take as later additions |
| `tamil`, `tamil_source`, `rights` | the lines, the file, `{"tamil": "public_domain"}` |

**Units** (`kg/core/<book>_units.jsonl`): `id` `<book>:<kaathai>:<start>-<end>` (the record's own
line positions), `record_id`, `start`, `end`, `line_count`, `kind` (`verse` = akaval, `song`),
`block_label`, `song` (the printed song number, if any), `break_score`, `tamil`.

**Verse epics**, one record per verse: `id` `<book>:N`, `number`, `section_number`, `section`,
`section_kind` (இலம்பகம், சருக்கம், காண்டம்), `padalam`, `line_count`, `tamil`, `tamil_source`,
`metre_change_before` (the e-text prints வேறு before the verse). `padalam` is null throughout: none
of these works divides its ilampakams, sarukkams or kandams further, and the sub-headings in the
e-texts are modern editors' (not copied). Valayapathi and Kundalakesi have no sections; their
records carry `kind` (`invocation` or `verse`), and Valayapathi's carry `quoted_in` (the work whose
commentary preserves the fragment: புறத்திரட்டு for 1-66, Adiyarkkunallar's Silappathikaram
commentary for 67-69, the Yapparungalam commentary for 70-71, the Tolkappiyam commentaries for
the invocation).

## How the reading units are made

The same rule and code as the Pattupattu (`score_break` and `split_units` are imported from
`scripts/build_sangam_core.py`): units of 10-25 lines, greedy from the top, each end scored by how
strongly its line closes a sentence, choosing the end that maximises `10 * score - |length - 16|`,
never leaving fewer than 10 lines, a remainder of 25 or fewer taken whole. Two additions for the
epics:
- A unit never crosses a block (a change of metre or a rubric), so a closing venba is always its
  own unit, and a block of 25 lines or fewer is one unit.
- Embedded songs are never split or merged: each numbered song of a vari or kuravai is one unit,
  whatever its length (the two-line kuravai songs of kaathai 17 give two-line units). In the song
  kaathais an unnumbered stretch is split at its blank lines into stanzas, unless it carries
  printed line numbers (the akaval openings of 12 and 17), in which case the akaval rule applies.

Silappathikaram: 434 units, 254 akaval (`verse`) and 180 songs; Manimekalai: 288 units, all 10-25
lines. Akaval ends: break score 3 on 84, 2 on 32, 1 on 119, 0 on 19 (Silappathikaram).

## Counts against the standard

| Work | Standard | Ours | Notes |
|---|---|---|---|
| Silappathikaram | 30 kaathais + patikam; sangamtamil.com gives 5,270 lines as canonical | 30 kaathais + patikam + 3 kandam katturais + nool katturai; **5,273 lines** | every printed line number falls on its line except in kaathai 20 (below) |
| Manimekalai | 30 kaathais + patikam; the site gives 4,861 lines | **4,856 lines**; every kaathai ends on its own printed last number | the 5-line difference from 4,861 is unexplained (see open problems) |
| Civaka Cintamani | 3,145 verses, 13 ilampakams | **3,145**, every ilampakam at the edition's own range | 3,141 four-line stanzas; 652, 653, 1487 have 5 lines; 577 has 2 |
| Valayapathi | 72 | **72** (invocation + 71) | |
| Kundalakesi | 19 | **19** | |
| Soolamani | 2,130 in this edition (the site says 2,131) | **2,128** | 1303 and 1528 not in the e-text |
| Neelakesi | 894 | **885** | 845-851 lost in the manuscript (the e-text says so); 102 and 738 are copies of 101 and 737 in the e-text |
| Naga Kumara Kaviyam | 170 (the e-text's own tally) | **170** + the invocation as 0 | the site's "1,114" is wrong |
| Udayana Kumara Kaviyam | 367 | **367** | 173 and 221 have no number in the e-text; placed by position |
| Yasodhara Kaviyam | 330 | **330** | the site's "741" counts commentary fragments |

Silappathikaram per kaathai (lines kept / last printed line number; songs):

| | | | | | |
|---|---|---|---|---|---|
| patikam 90/90 | 1 68/65 | 2 94/90 | 3 179/175 | 4 88/80 | 5 240/240 |
| 6 178/170 | 7 300, 52 songs | 8 126/115 | 9 83/75 | 10 248/245 | Pukar katturai 24/20 |
| 11 216/215 | 12 168/70, 23 songs | 13 196/195 | 14 218/215 | 15 219/215 | 16 221/215 |
| 17 159/10, 27 songs | 18 53/50 | 19 75/75 | 20 103/80, 3 venbas | 21 61/55 | 22 161/160 |
| 23 204/200 | Madurai katturai 20/20 | 24 134, 18 songs | 25 194/190 | 26 254/250 | 27 256/255 |
| 28 234/230 | 29 174, 29 songs | 30 202/200 | Vanchi katturai 15/15 | nool katturai 18/15 | |

The lines after the last printed number are the unnumbered last lines of the akaval and the
closing venbas. Manimekalai per kaathai (all equal to the printed last number): patikam 98, 72, 75,
171, 125, 141, 214, 134, 63, 71, 93, 146, 121, 115, 104, 86, 135, 98, 172, 162, 129, 190, 215, 147,
176, 239, 94, 289, 245, 472, 264.

## Checks run

- **Sequence**: every verse number from 1 (0 for invocations) to the last; no number twice; a
  verse whose text repeats the verse before it is not kept under the second number. Printed line
  numbers (Silappathikaram, Manimekalai) must fall on their lines.
- **Duplicates**: same line twice in a row (in Silappathikaram 7, 17, 18, 24 these are refrains and
  flagged `refrain`); the same verse text under two numbers.
- **Tamil only**: every character in `tamil` is Tamil (U+0B80-U+0BFF) or `. , ; : ! ? ' " ( ) -`
  and the curly quotes; all text is NFC. Valayapathi keeps the edition's parentheses that restore
  elided letters (`வேறுவே(று)`).
- **Lost vowel signs**: a vowel sign or pulli not after a consonant, a word starting with a vowel
  sign, unassigned code points (U+0BA1, U+0BA2), a lone dead consonant, and words in -யடு/-ளடு
  that may have lost ொ (the -ஒடு fault seen in our Purananuru).
- **Stanza length**: 4 lines expected (4 or 5 in Neelakesi).

Repairs (each one in the flags file): TSCII leftovers `ு஡` → ூ (Silappathikaram 15), `ௌ` before
a vowel sign → ெள (40), `ோ்` → ேர் (Cintamani 64), a pulli after a vowel sign dropped (67), `·`
and `•` → ஃ (54), Neelakesi's `ோ¢` → ேரி, `¢` → ி, `¡` → ா, `¡;` → ர், `b` + consonant →
consonant + ெ (46), U+0BA2 → ி (3); a DEL character (a typed backspace, `140⌫5` = 145) removed;
`< br>` and `>` HTML leftovers; stanzas printed in eight half-lines joined into four lines (1,440,
mostly Cintamani and Soolamani); four kural lines printed two to a line split at the comma (20);
the two half-lines of Silappathikaram 1.46-49 joined so that the printed line numbers fit.

## Differences from sangamtamil.com

The site builds these texts from the same Project Madurai files, so its Tamil, letter for letter,
is the same as ours wherever both have a line; every in-line difference is one of our repairs
(the site keeps `து஡`, `ௌி`, `•`, `¡`, `¢`, `ோ்`) or the site dropping a final full stop. Its
Vanchi kandam is in decomposed Unicode (ே + ா for ோ), which compares equal only after NFC. What
differs is coverage and segmentation:

| Work | Site | Missing on the site | Other |
|---|---|---|---|
| Silappathikaram | 5,327 "lines" | the Pukar kandam katturai and its venba, and kaathai 10 lines 226-230 | the site counts rubrics (வேறு, metre names), the editor's note in 22 and "முற்றும்" as lines; it splits head-numbered songs across segments |
| Manimekalai | 4,730 lines | 16: 30 lines, 27: 10 lines, 29: 90 lines (blocks dropped) | counts the heading of 9, 14, 26 and the title as lines |
| Civaka Cintamani | 2,124 units | 1,041 of our verses (409-850 almost entirely, 2589-3145 entirely, and 33 others); 72 verses cut short after 1-3 lines | its first entries are the table of contents; 318 entries carry headings or commentary |
| Valayapathi | 69 | the invocation, 58, 60 | 66-69 have the source note run in |
| Kundalakesi | 18 | 1, 13, 15-17, 19 | its entries are mostly commentary fragments |
| Soolamani | 1,567 | 563 verses (most of 239-826, and 58, 145-146, 221) | 131 cut short; headings run into the verse |
| Neelakesi | 899 | 261, 313, 407, 837 | counts the table of contents and the "845-851 lost" note as verses |
| Naga Kumara Kaviyam | 169 | the invocation, 53 | headings run in |
| Udayana Kumara Kaviyam | 338 | 31, 42, 46, 72, 87, 102, 157, 186, 246, 265, 269, 316, 318-319, 321, 335, 354-367 | its numbers are offset from the verses |
| Yasodhara Kaviyam | 741 | 1, 155, 157-160 | 42 cut short; commentary fragments counted as verses |

Nothing was filled from the site: it has no line we lack.

## Open problems

1. **Soolamani 1303 and 1528**, **Neelakesi 102 and 738**: absent from the e-text (1303 skipped;
   the others printed as copies of the verse before). The site has the same gaps. tamilvu.org was
   not consulted; it is the natural arbiter.
2. **Neelakesi 845-851**: lost in the manuscript, per the edition. Not recoverable here.
3. **Repeated verses**: Neelakesi 544 has the text of 313, Udayana Kumara Kaviyam 316 the text of
   313. Either a copying slip in the e-text or a genuine repetition; both kept and flagged.
4. **Unreadable TSCII leftovers** in Neelakesi 139, 164, 585, 655 (`£`, `¨¡`, `¦`) and Soolamani
   2064 (`ள் ெளா`), and the garbled Soolamani 7 (`துஞ்சுந்ணணள்`, kept as printed with ி repaired):
   flagged, not guessed.
5. **Possible lost ொ** (-யடு for -யொடு): Cintamani 1205, 2123 (two lines), Valayapathi 20, 29, 42.
   Flagged only, since அடு 'to slay' looks the same.
6. **Short or long stanzas**: Soolamani 299, 1076, 1173 have 3 lines (a line lost or two merged);
   Cintamani 577 has 2 lines (the kural-line split found no comma); Neelakesi 464 has 3.
7. **Silappathikaram 20**: the e-text's line numbers count the short lines of the கருப்பம் passage
   in pairs, so the printed numbers drift (15 falls on line 20). Lines are kept as printed.
8. **Totals**: Silappathikaram 5,273 against the site's 5,270 and Manimekalai 4,856 against the
   site's 4,861. Our counts follow the e-texts' own lineation exactly; the site's canonical
   figures are unsourced. Check against a printed edition before quoting either.
9. The Silappathikaram patikam's prose உரைபெறு கட்டுரை is not in Project Madurai's text, and is
   not here. Rubrics (`உரைப்பாட்டு மடை`, `கொளு`, `தேவந்தி சொல்`) are kept only as block labels.
