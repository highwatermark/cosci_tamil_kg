# Ettuthogai ingest: six anthologies

Builder: `scripts/build_ettuthogai_core.py` (standard library only; run `python3 -I scripts/build_ettuthogai_core.py`,
optionally `--books natrinai,...`). It reads the Project Madurai mirror in `data/text/` and the cached
sangamtamil.com crawl (`--stc-dir`, default the session scratchpad `sangamtamil_crawl/`; the build stops if
the crawl is missing). Outputs `kg/core/<book>.jsonl` and this script's entries in
`kg/core/sangam_text_flags.jsonl` (entries of other books are kept untouched).

## Record shape

The Akananuru fields: `id` (`<book>:N`), `number`, `section`, `kind` (`poem`, `invocation`, `patikam`,
`fragment`), `title`, `poet`, `patron`, `thinai`, `thurai`, `note`, `colophon_raw`, `tamil`, `line_count`,
`tamil_source` (the pmuni file), `rights` (all public domain). Added:

| field | content |
|---|---|
| `line_sources` | `{line: "sangamtamil.com"}` for lines not from Project Madurai, else null |
| `stc_compared` | whether the poem was compared with sangamtamil.com |
| `variants` | one entry per line that differs from the site: `kind` (`spelling`, `reading`, `unlike`, `line_break`, `pm_only`, `stc_only`, `supplied`, `eye_skip`, `repaired`, `rule`), the site's reading (`stc`), and which source the kept line comes from (`kept`: `pm`, `stc`, `pm, repaired from stc`, `pm, repaired by rule`) |
| `decade`, `decade_title` | Ainkurunuru and Patitruppattu decades |
| `metre`, `vannam`, `poem_names`, `fragment` | Patitruppattu colophon facts; the patikam's list of poem names |
| `music`, `pan`, `dropped_headings` | Paripadal colophon facts; the e-text's modern headings that were removed |

How the comparison works: our lines and the site's are aligned on Tamil letters. `spelling` means the same
consonant skeleton once vowels and sandhi are set aside (our joined sandhi against the site's split words);
`reading` is any other letter difference, and many of these are still sandhi (மணற் / மணல்) or plain typing
errors in one of the two texts. Only the site's Tamil verse lines and thinai labels are used; its English, its
romanized names, its Tamil speaker labels and situation headings are not.

Repairs common to all books (each one flagged): `·` -> ஃ; TSCII leftovers for ரி / ரீ / ெரி / ெளி
(`கடும்பா஢` -> கடும்பரி, `ஒ஡ணஇய` -> ஒரீஇய, `தௌ ர்ப்ப` -> தெளிர்ப்ப, `தௌிய` -> தெளிய); a stray space before a final
dead consonant (`கண்டோ ர்`); words with junk, grantha letters, three dead consonants in a row, or a lost first
letter are replaced by the site's word for the same letters; lines the site has and we lack inside a poem are
supplied from the site, as are both lines of an eye-skip (our line = start of one line + end of the next).

Not done: tamilvu.org (U. V. Swaminatha Aiyar) was not consulted, so `reading` differences are recorded, not
arbitrated.

## Natrinai (`natrinai.jsonl`, pmuni0296)

- 399 poems + invocation (0) = 400 records, against the standard 400 with 234 lost. The e-text prints two
  verses that modern scholars proposed for 234; not adopted (flagged).
- Headings `N thinai - poet` come in six printed forms (`32 - குறிஞ்சி - கபிலர்`, `66 பாலை`, `84 பாலை (?)`,
  `93 குறிஞ்சி = மலையனார்`, `125.குறிஞ்சி - (?)`). `(?)` = poet not preserved (`note`); 8 headings give no poet at
  all (66, 70, 76, 77, 78, 108, 271, 334: flagged). `thurai` is the e-text's situation sentence after the verse.
- The -ஒடு fault: the file has no யொ or ளொ at all. 52 words restored where the site confirms the sign (வாடையடு ->
  வாடையொடு), 2 more by rule where the site lacks the line (163, 276). 22 `தௌ ` leftovers read as தெளி.
- vs sangamtamil.com: 4,169 lines compared, 734 differ: 240 spelling, 392 reading, 1 strongly different (134.6),
  57 line breaks, 3 lines the site lacks (opening lines of 84, 160, 170), 39 repaired from the site.
- 385 is cut short in the source (last line a gap).

## Kuruntokai (`kuruntokai.jsonl`, pmuni0110)

- 401 poems + invocation (0) = 402 records: the standard count. The e-text prints 126 after 130 (records are in
  numerical order; flagged). 307 and 391 have nine lines, as in the tradition.
- `thurai` holds the e-text's speaker label (தோழி கூற்று), the only situation it gives; poet from the `-name.` line.
  105, 180 have no poet; 191 and 201 print dots (poet lost). 396's thinai is misprinted பாால (read பாலை).
  Seven thinai disagree with the site (9, 10, 138, 189, 301, 332, 336); the base is kept and flagged.
- The text keeps the old sandhi-joined spelling, so most differences are spelling: 2,498 lines compared, 1,718
  differ (1,137 spelling, 537 reading, 40 line breaks, 3 lines the site lacks). One line supplied: 377 line 1.
  Eight `ௌி` leftovers repaired; 394's lost first syllable (ன்னாள் -> முன் நாள்) taken from the site.

## Ainkurunuru (`ainkurunuru.jsonl`, pmuni0028)

- 498 poems: the standard 500 less 129 and 130 (printed கிடைக்காத பாடல்). Neither the e-text nor the site has
  the invocation.
- `section` and `thinai` = the hundred (மருதம், நெய்தல், குறிஞ்சி, பாலை, முல்லை) and `poet` its poet
  (ஓரம்போகியார், அம்மூவனார், கபிலர், ஓதலாந்தையார், பேயனார்) by the traditional division; the e-text has no
  colophons. `decade_title` from the e-text's பத்து headings (478 poems; decades 1 and 2 have none).
- This is the weakest base text: a romanized-to-Tamil conversion with many broken words (`த்ஹுறவன்`,
  `ய்ய்ரன்`, `மல்ர்ந்த`). 30 such words replaced by the site's reading, 3 stray spaces closed, one stray code point removed (491).
- vs sangamtamil.com: 2,160 lines, 955 differ (627 spelling, 248 reading, 60 line breaks, 1 line the site
  lacks, 18 repaired). One line supplied: 468 line 4. Many `reading` rows are typing errors in our text that a
  word-level pass against tamilvu should settle.

## Patitruppattu (`patitruppattu.jsonl`, pmuni0038)

- 80 poems (11-90, decades 2-9) + 8 patikams (`patitruppattu:patikam:2` ... `:9`) + 4 fragments of the lost
  decades quoted by the commentators (`patitruppattu:fragment:1-4`; a fifth is only a mention, not recorded).
  The standard: decades 1 and 10 lost.
- Colophon per poem: `title` (பெயர்), `thurai`, `metre` (தூக்கு), `vannam`; per decade the patron (accusative
  ending made nominative: நெடுஞ்சேரலாதனைக் -> நெடுஞ்சேரலாதன்) and poet. The patikam keeps its closing
  `... பாடினார் பத்துப்பாட்டு` lines as verse; the list of poem names, the reward (பாடிப்பெற்ற பரிசில்) and the
  reign are in `colophon_raw`. Poem 79's colophon is printed after a stray `### மூன்றாம் பத்து` heading.
- The e-text writes elided vowels in brackets (வளிபாய்ந்(து) அட்ட); kept. Asterisks around the name phrase removed.
  Many TSCII leftovers (஡஢, ா஢, ொ஢, ோ஢, ஡ண) repaired, including the poet அரிசில்கிழார். A gloss line in 52
  (பஃறோல் = பல்தோல்) dropped. 73: two dotted lines (lost text) are not counted by the source's numbering; removed
  and kept as `lacunae`.
- vs sangamtamil.com (poems only): 1,696 lines, 305 differ (237 spelling, 65 reading). One eye-skip in 31
  (line 25 joins two lines; the printed numbering confirms a missing line): both lines taken from the site.

## Paripadal (`paripadal.jsonl`, pmuni0087)

- 22 songs (1-22) + 13 fragments of Paripadal thirattu (`paripadal:thirattu:1-13`). The commentary preface
  (உரைச்சிறப்புப் பாயிரம்) and the closing venpa are not taken.
- Colophon: subject (திருமால், செவ்வேள், வையை, மதுரை) as `title`, `poet`, `music` (இசையமைத்தவர்), `pan`.
- The e-text puts modern headings inside the songs. Single-line blocks are dropped; then, wherever the printed
  line numbers show a stretch with surplus lines, the surplus lines that look like headings (prose endings such as
  -தல், வகை, காட்சி; not in the site; no verse punctuation) are dropped. 41 such lines, each flagged
  `heading_dropped` for a check by eye; 9 songs still disagree with their printed numbering (flagged).
  Bracketed prose notes (the song's situation, where a fragment is quoted) are dropped.
- The -ஒடு fault as in Natrinai: 20 restored with the site's confirmation, 9 by rule.
- The site's 22 units do not follow the traditional numbering and lack much of the text, so each song is
  aligned against the stretch of the site that holds it. 2,068 lines compared, 556 differ (319 line breaks,
  81 spelling, 44 reading, 5 strongly different, 74 lines the site lacks, 24 repaired). Nothing supplied.

## Kalittokai (`kalittokai.jsonl`, pmuni0221)

- 150 poems, 1 being the invocation: the standard count. `section`: பாலைக்கலி 2-36 (35), குறிஞ்சிக்கலி 37-65
  (29), மருதக்கலி 66-100 (35), முல்லைக்கலி 101-117 (17), நெய்தற்கலி 118-150 (33); `thinai` follows the section.
- `poet` from the section's ஆசிரியர் line. The e-text names the Marutham poet மருதநிலங்கன் and the Neythal poet
  நல்லாந்துவனார் (usually மருதன் இளநாகனார், நல்லந்துவனார்): kept and flagged. The invocation names no poet.
- vs sangamtamil.com: 4,314 lines, 555 differ (258 spelling, 39 reading, 36 line breaks, 211 lines the site
  lacks: the site's text of 40, 42, 60, 82, 83, 84, 94, 107, 114 is truncated). The site's Tamil speaker labels
  (தலைவி:) and headings are skipped. Supplied: 56 line 34 (இறையே தவறுடையான்.) and the eye-skip at 24 line 11.

## Open problems

- `reading` differences are not arbitrated against tamilvu; Ainkurunuru and Kuruntokai hold most of the real
  typing errors.
- The site crawl lives in the session scratchpad; without it the builder stops. `scripts/build_sangam_core.py`
  rewrites the whole flags file when run, which would drop these entries; rerun this builder after it.
- Paripadal heading removal is heuristic (see `heading_dropped` flags).
