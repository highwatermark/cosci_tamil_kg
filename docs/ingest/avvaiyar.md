# Ingest report: Avvaiyar's four short works (`avvaiyar`)

Outputs
- Script: `/Users/harilakshmanan/Cursor/cosci_knowledge_graph/scripts/parse_avvaiyar.py` (stdlib only, `python3 -I scripts/parse_avvaiyar.py`, reads only `data/text/`)
- Records: `/Users/harilakshmanan/Cursor/cosci_knowledge_graph/kg/core/avvaiyar.jsonl` (274 records)

## Record shape

One record per unit, in the catalogue's order (rows 2-5): Aathichudi, Kondrai Vendhan, Nalvazhi, Moodurai.

- `id`: `avvaiyar:<work>:<number>`, e.g. `avvaiyar:aathichudi:15`, `avvaiyar:nalvazhi:10`
- `seq`: 1-274 across the four works; `work` (`aathichudi`, `kondrai_vendhan`, `nalvazhi`, `moodurai`) and `work_tamil`
- `number`: position in the work (0 = the invocation, kept as its own unit with `invocation: true`); `printed_number`: the base file's printed number
- `group`: for Aathichudi and Kondrai Vendhan, the letter group heading (`உயிர் வருக்கம்`, `ககர வருக்கம்` ...); `கடவுள் வாழ்த்து` for invocations; null for Nalvazhi and Moodurai verses (they have no sub-divisions)
- `tamil`: the line (one item) or the four lines of the venba
- `navalar`: `{text, gloss, meaning, notes}`: Navalar's own reading of the line or verse, the word gloss (`[ப-உ]` / `இ-ள்`), the gist (`[க-உ]` / `இ-ம்`), and any further notes (variant readings, the edition's footnotes)
- `ramabharathi` (Aathichudi only): `{sutra, venba, printed_number, story_title, story}`: the heading as Ramabharathi reads it, his venba, the story printed under it (or a pointer such as "இதன் கதையை ... காண்க", or a gloss)
- `shanmuganar` (Nalvazhi only): the prose commentary
- `match`: the alignment score per source (bigram+trigram Jaccard; 0.0 = paired by position, see below)

## Files used

| text id | catalogue row | content | use |
|---|---|---|---|
| pmuni0002 | 2, 3, 4, 5 | All four works, one file (K. Kalyanasundaram, 2001) | base text |
| pmuni0743 | 883 | "ஔவையார் பாடல்கள் (4)": all four works with Arumuga Navalar's commentary (Chennai prints 1914-1921) | `navalar` |
| pmuni0481 | 619 | Ramabharathi, ஆத்திச்சூடி வெண்பா: a venba ending in each Aathichudi line, with stories (Tellippalai edition) | `ramabharathi` |
| pmuni0777 | 917 | Sundara Shanmuganar, நல்வழி நயஉரை (1993 wedding-gift reprint) | `shanmuganar` |

Row 883 was not in the brief. I found it by searching the catalogue for Avvaiyar. It is the only full commentary on all four works, and it is public domain, so it is in the records.

Rejected:
- Row 437 குறள்மூலம் (Avvai Kural), row 884 ஞானக்குறள், row 885 ஒளவையார் தனிப்பாடல்கள், rows 342/1059/1097 விநாயகர் அகவல்: these are other works attributed to an Avvaiyar, not the four.
- Row 867 (Tamilannal's biography of Avvaiyar), and the rows matching "ஔவை" that belong to Avvai Duraisamy Pillai or Avvai T.K. Shanmugam: not these works.
- PDF ids: not read, because the brief limits the work to `data/text/`.

## Unit counts

| work | units (+ invocation) | traditional | status |
|---|---|---|---|
| Aathichudi | 109 + 1 | 108 or 109, both are cited | 109 in the base and in Navalar; see below |
| Kondrai Vendhan | 91 + 1 | 91 | ok |
| Nalvazhi | 40 + 1 | 40 (+ kaappu) | ok |
| Moodurai (Vaakkundaam) | 30 + 1 | 30 (+ kaappu) | ok |

Total 274 records: 270 units and 4 invocations. Nothing is missing or doubled.

The difference between 108 and 109 lines in the Aathichudi is the line **கௌவை அகற்று** (base 43). Navalar's edition prints it, but numbers it 43 a second time and adds "(இது விடுபட்டிருக்கிறது)" with no commentary. Its last line is therefore printed 108, even though it has 109 lines. Ramabharathi has no venba for it at all. So it is probably the line that some traditions add to make 109. It stays in the records as `aathichudi:43`.

## Alignment counts

| source | aligned | of | notes |
|---|---|---|---|
| navalar, Aathichudi | 110 | 110 | all lines plus the invocation. 43 has text only (the source omits the commentary), and 54 has a gloss but no gist |
| navalar, Kondrai Vendhan | 92 | 92 | all lines plus the invocation |
| navalar, Nalvazhi | 41 | 41 | all verses plus the invocation |
| navalar, Moodurai | 31 | 31 | all verses plus the invocation |
| ramabharathi | 107 | 109 Aathichudi lines | no venba for 43 (கௌவை அகற்று) or 109 (ஓரம் சொல்லேல்). His kaappu and closing "வாழி" benediction are left out because they are not readings of Avvaiyar's lines. 64 records carry a story or note, 58 of them with a titled story |
| shanmuganar | 41 | 41 Nalvazhi units | all verses plus the invocation. The 5 unaligned blocks are the wedding blessings and the book list at the end of the file |

**Method.** Alignment preserves order: a dynamic program over letter bigram and trigram similarity, with a threshold of 0.2. It cannot cross matches, so short Aathichudi lines with sandhi differences (அறம் செய / அறஞ்செய) still land in the right place.

**Pairing by position.** When exactly one unmatched unit sits on each side between two matches, the two are paired by position with score 0.0. This happens twice, both in Ramabharathi:
- 24: இயங்கித் திரியேல் for இயல்பு அலாதன செய்யேல்
- 73: நேர்கோனெறிநில் for நேர்பட ஒழுகு

His editor names both readings in the preface as variants of the printed Aathichudi. His own printed numbers (24, 72) agree with these slots.

**Low-score matches.** The script prints every match below 0.4. I checked each by reading:
- Ramabharathi variant readings that are correct in position:
  - 81: புகழ்படவாழ்
  - 82: பூமிவிரும்பு
  - 87: போற்றடிப்பிரியேல் (named by his editor)
  - 94: மெல்லியாடோழ்சேர்
- Sandhi or spelling differences in Navalar: Aathichudi 9 and 84, Kondrai Vendhan 34

## Spot checks (read)

1. `aathichudi:15` ஙப் போல் வளை.
   - Navalar glosses ஙப்போல் as ஙகரத்தைப் போல் and explains that ங carries its useless kindred letters ஙா, ஙி.
   - Ramabharathi's venba ends "...ஙப் போல் வளை", with a note on crows calling their kin to food.
   - Both correct.
2. `kondrai_vendhan:39` திரைகடல் ஓடியும் திரவியம் தேடு.
   - Navalar: "திரைகடல் - அலை வீசுகின்ற கடல் மார்க்கமாய் ... திரவியம் - பொருளை".
   - Correct.
3. `nalvazhi:10` ஆண்டாண்டு தோறும் அழுது புரண்டாலும்: the base prints this verse as 11.
   - Navalar's gloss (மாநிலத்தீர் ... ஆண்டு ஆண்டு தோறும் அழுது புரண்டாலும்) and Shanmuganar's prose (marked "(10)") both belong to this verse.
   - Correct, and the base misnumbering is repaired.
4. `moodurai:14` கான மயிலாடக் கண்டிருந்த வான்கோழி.
   - Navalar's gist: "கற்றவருடைய தொழிலை மேற்கொண்டானாயினுங் கல்லாதவன் கற்றவனாகான்".
   - Correct.
5. `aathichudi:87` போர்த் தொழில் புரியேல்.
   - Ramabharathi's sutra is போற்றடிப்பிரியேல், with the Bhringi story. This is a different reading of the same slot: his numbering (86, one behind from 44 onward) and the neighbouring lines agree.
   - Kept, with match 0.20. Later stages should treat it as a variant, not a gloss of the base line.

## Copyright

| field | person | dates | status |
|---|---|---|---|
| (base) | Avvaiyar | medieval | public domain |
| `navalar` | Arumuga Navalar; the edition's notes are by an unnamed editor (they cite T. Kanagasundaram Pillai, 1863-1922) | 1822-1879; printed 1914-1921 | public domain |
| `ramabharathi` | Ramabharathi; stories by V. Kanagasabapathi Iyer and A. Kumaraswamy Pulavar (1854-1922); edited by E. Muthukumaraswamy Kurukkal | poet undated, before the 19th century; edition dated Plava year (likely 1901) | public domain (probable) |
| `shanmuganar` | Sundara Shanmuganar | 1922-1997; this print 1993 | **modern, in copyright** |

Sidecar rights map:

```json
{"navalar": "public_domain", "ramabharathi": "public_domain", "shanmuganar": "modern"}
```

## Text problems

Base pmuni0002:
- Nalvazhi verse 10 is printed as "11", so 11 appears twice. Records are numbered by position, and `printed_number` keeps 11.
- Kondrai Vendhan 58 carries an editor's query inline: "நோன்பு என்பதுவே (? என்பது) கொன்று தின்னாமை". Kept as printed. Navalar reads "நோன்பென் பதுவே".
- Moodurai and Nalvazhi carry editorial brackets such as "(கு)", "(;)", "(து)". Kept as printed.
- Aathichudi 103-104 (உத்தமனாய் இரு, ஊருடன் கூடி வாழ்) sit inside the வகர group, as in all editions.

Navalar pmuni0743:
- Aathichudi 43 is printed twice. கௌவை அகற்று has only "(இது விடுபட்டிருக்கிறது)".
- Aathichudi 54 has no `[க-உ]`.
- Kondrai Vendhan 3 has a gloss without its tag. The script takes it as the gloss.
- Kondrai Vendhan 77 has `[க--]` in the middle of a line. The script splits it there.
- Tags are inconsistent (`[ப-உ]`, `[ப. உ]`, `(ப-உ)`, `[ப-உ` with no closing bracket). All are handled.
- Readings that differ in meaning from the base:
  - KV 5 "பண்டிக்கு அழகு" for "பெண்டிர்க்கு அழகு" (the note records the latter as a variant)
  - KV 26 "சந்ததிக்கு" for "சந்நதிக்கு"
  - KV 28 "சிவத்தைப் பேணில்" for "சினத்தைப் பேணின்"
  - Navalar's reading is kept in `navalar.text`.

Ramabharathi pmuni0481:
- Printed numbers are unreliable:
  - 6 has no number
  - 14 and 15 are printed 18 and 19
  - from 44 onward his numbers run one behind the base, because he has no கௌவை அகற்று
- Other variant headings:
  - 67 நாடேற்பனசெய்
  - 72 நெற்பயிர்விளை
  - 106 வேண்டிவினைசெய் (the opposite sense of the base's வேண்டி வினை செயேல்)
- The index lists 62 stories. Several venbas instead point to another story or carry a short gloss.

Shanmuganar pmuni0777:
- Verse 31 is printed on 3 lines. The script ends each verse at its number.
- The file ends with wedding blessing poems and a list of the author's books. They do not align, and nothing from them enters the records.

No headers were found inside the verse text.

## Suggested unit for later marking

- Mark per unit as parsed: each Aathichudi and Kondrai Vendhan line, and each Nalvazhi and Moodurai venba.
- Each is a self-contained maxim, and the commentaries treat them one by one.
- Aathichudi lines are 2-4 words, so a single line will often carry just one theme. That is expected and should not be padded.
- For threading, the letter groups (`group`) are an acrostic device, not thematic units. They should not be used as a marking unit.
- These are not long devotional collections, so the per-verse versus per-pathigam question does not arise.
