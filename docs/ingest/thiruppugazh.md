# Thiruppugazh ingest report

Book key: `thiruppugazh`. Author: Arunagirinathar (15th century).
Script: `/Users/harilakshmanan/Cursor/cosci_knowledge_graph/scripts/parse_thiruppugazh.py`
(standard library only, `python3 -I scripts/parse_thiruppugazh.py`, reads only `data/text/`).
Output: `/Users/harilakshmanan/Cursor/cosci_knowledge_graph/kg/core/thiruppugazh.jsonl`, 1,326 records, numbers 1-1326 in order.

Final run prints:

```
CHECK pmuni0180: song printed '205' repeats the song before it word for word; dropped
CHECK pmuni0180: song 206 is missing from the source (its place holds a second copy of 205); kept as an empty record
CHECK song 93: printed number '92'
CHECK song 102: printed number '101'
CHECK song 203: printed number '202'
CHECK pmuni0189: song printed '801' repeats the song before it word for word; dropped
CHECK pmuni0189: song printed '922' repeats the song before it word for word; dropped
CHECK song 1141: printed number '114த'
CHECK song 1199: printed number '1100'
CHECK song 1326: no santham found
songs=1326 places=199 general=314 with_raga=469 lines=25018 songs_with_corrupt_chars=229
```

## Files used

| Catalog row | Text | Contents |
|---|---|---|
| 285 | `pmuni0180` | Part 1, songs 1-330 |
| 293 | `pmuni0187` | Part 2, songs 331-670 |
| 295 | `pmuni0189` | Part 3, songs 671-1000 |
| 297 | `pmuni0191` | Part 4, songs 1001-1326 (catalog title misprints this as "10011-1326") |

All four are the kaumaram.com e-text (A.S. Maniam, Mylai format, converted via TSCII to Unicode),
with raga, tala, tala breakdown and santham (rhythm pattern) printed above each song.

Rejected:
- Row 528 (`pmuni0397_02`), biography of the editor V.S. Sengalvaraya Pillai: not the text (as instructed).
- Rows 532 and 534 (Sengalvaraya Pillai's போற்றி அகவல் and his study of Arunagirinathar), row 1175
  (அருணகிரி அந்தாதி by another poet), rows 56-58 and 1059 (Arunagirinathar's other works): other works,
  not translations or commentaries of the Thiruppugazh.
- No translation or commentary of the Thiruppugazh exists in the catalog (searched Tamil and Latin
  titles and authors). So records carry no translation/commentary fields.

## Record shape

`id` (`thiruppugazh:N`), `number` (traditional 1-1326), `printed_number` (as printed, null for 206),
`part` (1-4), `source` (file), `heading` (cleaned heading label), `heading_raw`, `heading_variants`
(a second spelling where the heading was printed twice), `kind` (`place`, `general` for
பொதுப்பாடல்கள், `invocation` 1-5, `opening` 6, `all hills` குன்றுதோறாடல் 302-306, `six shrines` 307,
`list of shrines` க்ஷேத்திரக் கோவை 1306, `new` புதிய பாடல்கள் 1323-1324, `figured poem`
திருவெழுகூற்றிருக்கை 1326), `thalam` (temple, null when the heading is not a place), `raga`, `tala`,
`tala_notes` (tala breakdown, எடுப்பு notes, trailing reference codes), `santham` (lines),
`tamil` (verse lines, with the printed `......` rhythm break kept), `corrupt_chars` (count or null),
`missing` (true only for 206).

Counts: 996 temple songs across 199 thalams (largest: பழநி 97, திருச்செந்தூர் 83, திருவருணை 78,
சிதம்பரம் 68, திருத்தணிகை 62, காஞ்சீபுரம் 45, சுவாமி மலை 39), 314 general songs (992-1305), and the
special headings above. Every thalam forms a single run in order (checked). Raga is given for 469 songs
(the rest print `ராகம் - ....`); 25,018 verse lines.

## Unit count against the traditional 1,326

1,326 records, numbered by position and checked against each part's printed range. Every record but
206 has text. Problems found and how they were resolved:

- **Song 206 is missing from the source.** Part 1 prints song 205 twice word for word (headings
  205, 205, 207). The raw HTML and the PDF (`data/raw/pdf/pm0180.pdf`, checked) have the same repeat
  under the label 206. Kept as an empty record (`tamil: []`, `missing: true`) so numbers stay right.
  Its text must come from another edition.
- **Songs 801 and 922 are printed twice** word for word in part 3; the second copies were dropped.
- **Songs 744 (திருவெண்ணெய்நல்லூர்) and 792 (திருவிடைக்கழி) lost their `###` heading** in the
  text conversion (the HTML has them). Unprefixed `பாடல் N` lines are now read as headings, so they
  are separate songs, not merged into 743 and 791.
- **Repeated heading lines** (72, 349, 920) are skipped; 920's repeat gives the better spelling
  பூவாளுர், kept in `heading_variants`.
- **Misprinted numbers** (text taken by position, printed form kept in `printed_number`): 93 printed
  92, 102 printed 101, 203 printed 202, 1141 printed `114த`, 1199 printed 1100; `9 7`, `23 1`, `49 0`,
  `55 7`, `118 0`, `124 0` have a space inside the number (read correctly).
- Boundary check: every one of the 1,325 texts ends with the closing vocative (பெருமாளே 1,187,
  தம்பிரானே 126, others), and no line ending in பெருமாளே. appears mid-song, so no two songs are merged.

## Alignment

No translations or commentaries in the corpus: 0 alignments. The five spot checks below are of unit
boundaries and metadata instead, read against the source:

1. **1** (விநாயகர் துதி, நாட்டை/ஆதி): santham 2 lines, verse 16 lines from கைத்தல நிறைகனி to
   அக்கண மணமருள் பெருமாளே. Correct.
2. **106** (பழநி): 23 lines; the source prints two lines run together as one
   (`...பரிய குடர்பழுவெ லும்பைப்பி டுங்கரண`), so the count is odd. Text intact.
3. **206**: empty, as described above.
4. **744** (திருவெண்ணெய்நல்லூர்): recovered from the heading without `###`; 24 lines,
   பலபல தத்துவ... to ...பெருமாளே. 743 now ends correctly at தேவர்சிறை விட்ட பெருமாளே.
5. **1199** (printed 1100, பொதுப்பாடல்கள்): 16 lines, வளைகர மாட்டி... ; position confirms 1199.

## Copyright

| Contributor | Date | Status |
|---|---|---|
| Arunagirinathar (text) | 15th c. | public domain |
| kaumaram.com e-text (A.S. Maniam) and the raga/tala/tala-breakdown annotations | c. 1999-2003, modern | editorial annotations are modern; treat as modern |
| V.S. Sengalvaraya Pillai (editor of the standard edition; his notes are not in these files) | d. 1971 | not present here |

Sidecar rights map:

```json
{"thiruppugazh": {"tamil": "public", "santham": "public", "raga": "modern", "tala": "modern", "tala_notes": "modern"}}
```

No translator or commentator fields exist, so nothing in the records needs `"rights": "modern"` beyond
the raga/tala metadata (short labels; quoting them as facts is fine).

## Text problems

- **Conversion debris** (TSCII to Unicode): 323 bad characters in 229 songs' verse lines, counted per
  record in `corrupt_chars`: unassigned U+0BA1 (157, usually where ூ/ஊ should be, e.g. வயலு஡ரா),
  `¡` (76, usually ு¡ for ூ), `£` 29, unassigned U+0BA7 21, `¨` 16, `§` 13, `¢` 8, and single `¦ ¤ ¥`
  and U+0BA2. Left as printed in `tamil`; not repaired.
- **Heading names** cleaned in `heading`/`thalam` (raw kept in `heading_raw`): ு¡ and ு஡ to ூ
  (வயலூர், திருநாவலூர், வேலூர் ...), plus a fixed map: திருவர்ருர்/திருவாருர் to திருவாரூர்,
  திருப்பேர்ருர் to திருப்பேரூர், உ த்தர§ம்ருர் to உத்தரமேரூர், உ த்தரகோசமங்கை, பூவர்ளுர் to
  பூவாளூர், ஸ்ரீமுஷ்டம், சிங்கை - காங்கேயம். Left unrepaired because unsure: திருவர்முர்
  (perhaps திருவாமூர்), காவ்ளுர், §ப்ருர்.
- **Lines missing in the source**: 1180 (second stanza has 2 lines where the pattern needs 3) and
  1262 (first stanza short); odd line counts also in 14, 351, 355, 588, 902, 1326 that are the song's
  own shape or a joined line (106). Not repaired.
- **Notes inside the text**: reference codes `(0507-0000-2442)` after 588 and `(0774-0000-5640)`
  after 902 moved to `tala_notes`; `---------- 3 முறை ---------` (902) in `tala_notes`; a stray `**`
  at the end of a line in 1050.
- 1326 (திருவெழுகூற்றிருக்கை) has no santham; it is a figured poem in akaval, so that is expected.

## Suggested unit for later marking

**Per song.** Each Thiruppugazh song is one self-contained hymn (usually 8 or 12 long lines, 16-24
printed half-lines) built on one santham and closing on a vocative to Murugan (…பெருமாளே); its
petition and its praise only make sense together, and the closing lines carry the thalam. There is no
pathigam or decade structure: the thalam groups run from 1 to 97 songs and the 314 general songs have
no grouping at all, so a group-level unit would be uneven and arbitrary. Keep `thalam` as context for
linking (e.g. all பழநி songs), but mark the song. Lines inside a song are not independent units.
