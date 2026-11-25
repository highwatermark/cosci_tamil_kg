# Pathinenkilkanakku: the sixteen minor works besides the Kural and the Naladiyar

Outputs:
- `scripts/build_kizhkanakku_core.py` (standard library only)
- `kg/core/<book>.jsonl` for the sixteen books below, one record per verse
- `kg/core/sangam_text_flags.jsonl`: this script's flags are appended, each with `"book": "<book>"`.
  On a rerun it replaces only the flags of these sixteen books and keeps every other line.

Run:

```
python3 -I scripts/build_kizhkanakku_core.py \
    --site-dir <sangamtamil.com cache> --tvu-dir <tamilvu pages>
```

Without `--site-dir` and `--tvu-dir` the text and the source checks are rebuilt the same way, but
the cross-check flags (`site_diff`, `tvu_check`, `line_count`, `misprint_candidate`) are left out.
The text itself does not depend on either folder: the tamilvu-arbitrated repairs are a fixed table
in the script. The flags now in the repo were made with the sangamtamil.com cache
(`data/texts/*.js`) and 66 tamilvu verse pages saved as `<library>-<subid>.html` in the session
scratchpad (`kizh_texts/tvu/pages`). Neither folder is in the repo.

Note: `scripts/build_sangam_core.py` rewrites `sangam_text_flags.jsonl` whole, so running it drops
these flags. Run this script after it.

## Sources

| book | Project Madurai file | author (as the e-text gives it) |
|---|---|---|
| nanmanikkadigai | pmuni0047 | விளம்பிநாகனார் |
| innaa_narpathu | pmuni0025 | கபிலர் |
| iniyavai_narpathu | pmuni0025 | பூதஞ்சேந்தனார் |
| kar_narpathu | pmuni0029 | மதுரைக் கண்ணங்கூத்தனார் |
| kalavazhi_narpathu | pmuni0025 | பொய்கையார் |
| ainthinai_aimpathu | pmuni0027 | மாறன் பொறையனார் |
| thinaimozhi_aimpathu | pmuni0027 | கண்ணன் சேந்தனார் |
| ainthinai_ezhupathu | pmuni0027 | மூவாதியார் |
| thinaimalai_nootraimpathu | pmuni0056 | கணிமேதாவியார் |
| thirikadugam | pmuni0048 | நல்லாதனார் |
| acharakkovai | pmuni0024 | பெருவாயின் முள்ளியார் |
| pazhamozhi_nanooru | pmuni0036 | முன்றுறை அரையனார் |
| sirupanchamoolam | pmuni0029 | காரியாசான் |
| muthumozhikkanchi | pmuni0025 | மதுரைக் கூடலூர் கிழார் |
| elathi | pmuni0029 | கணிமேதையார் |
| kainnilai | pmuni0051 | புல்லங்காடனார் |

All sixteen were already in `data/text/`; nothing was downloaded for the base text. Innilai,
which shares pmuni0027 and pmuni0051, is not one of the eighteen and is skipped.

- **sangamtamil.com** (`data/texts/<id>.js` in the cache). Its texts for these works are built
  from the same Project Madurai files. Only its Tamil verse lines were compared. Its English and
  prose were never read into the output.
- **tamilvu.org** library: l2200 Thirikadugam, l2300 Muthumozhikkanchi, l2400 Innaa, l2500 Iniyavai,
  l2600 Kalavazhi, l2700 Kar, l2900 Nanmanikkadigai. I found no tamilvu library number for the
  other nine works. The tamilvu text is word-split (பிரித்த பாடம்), so it is compared with spaces
  and punctuation removed, and is used only to settle numbering, verse boundaries and
  single-letter misprints.

## Record shape

| field | content |
|---|---|
| `id` | `<book>:N`. Exceptions: `nanmanikkadigai:0b` (the second invocation verse) and `<book>:payiram` (a preface verse, which has no number) |
| `book`, `title` | key and Tamil title of the work |
| `number` | N; 0 for an invocation; null for a payiram |
| `kind` | `invocation`, `payiram` or `verse` |
| `source_number` | the number Project Madurai prints, when it differs from N or the record is not a verse |
| `invocation_part` | Nanmanikkadigai only: 1 or 2 |
| `section` | the work's own division: the thinai for the akam works, and the ten tens of Muthumozhikkanchi (with `section_no`) |
| `chapter_no`, `chapter` | Pazhamozhi only: its 34 headings (கல்வி … வீட்டு நெறி) |
| `thinai` | akam works only (Kar, the two Ainthinai, Thinaimozhi, Thinaimalai, Kainnilai), from the work's own arrangement |
| `thurai` | Kar Narpathu only: the old commentary's situation label above each verse, with இதுவுமது ("the same") resolved to the label above |
| `author` | as above; null on a payiram |
| `tamil`, `line_count` | the verse lines |
| `tamil_source` | the pmuni file |
| `rights` | `{"tamil": "public_domain"}` |

What is kept in the text: the verse lines as Project Madurai prints them, including the editor's
bracketed sandhi letters (e.g. `வரவுமற்(று)`), the quotation marks around Pazhamozhi's proverbs,
and dots for lost text (Kainnilai). Removed: the verse numbers, the full stop after the last
line, the variant marks `@ % &`, and stray characters (see the repairs below).

Left out: Project Madurai's modern headings for each verse (Acharakkovai, Thirikadugam), the
metre labels (Acharakkovai), the land and conduct notes (இடம், நிலம், ஒழுக்கம்), the dates, and
Kainnilai's bracketed `(துறை :: …)` notes. Their author is not named, and one of them says only
that the thurai "may be the one given for the previous verse", so they are not treated as the
tradition's colophon. The variant readings that Project Madurai prints under Innaa, Iniyavai,
Kar and Kalavazhi verses are not put in the text. They are kept as `source_variant` flags (57).

## Counts against the standard

| book | records | numbered verses | standard | invocation / payiram | note |
|---|---|---|---|---|---|
| nanmanikkadigai | 106 | 104 | 104 | 2 invocation | PM numbers 1-106 through. tamilvu: two invocation verses, then 1-104 |
| innaa_narpathu | 41 | 40 | 40 + invocation | 1 | |
| iniyavai_narpathu | 41 | 40 | 40 + invocation | 1 | |
| kar_narpathu | 40 | 40 | 40 | none | no invocation in PM or tamilvu (tamilvu has a later சிறப்புப் பாயிரம், not in PM) |
| kalavazhi_narpathu | 41 | 41 | 40, and 41 in tamilvu | none | PM prints a 41st verse without a number; tamilvu numbers it 41 |
| ainthinai_aimpathu | 51 | 50 | 50 | payiram | |
| thinaimozhi_aimpathu | 50 | 50 | 50 | none | |
| ainthinai_ezhupathu | 67 | 66 | 70 | 1 invocation | 25, 26, 69, 70 are lost in the tradition, and PM says so |
| thinaimalai_nootraimpathu | 154 | 153 | 153 | payiram | |
| thirikadugam | 101 | 100 | 100 + invocation | 1 (காப்பு) | |
| acharakkovai | 100 | 100 | 100 | none | |
| pazhamozhi_nanooru | 401 | 399 | 400 | 1 invocation + payiram | PM has 399 and says so ("401 with the payiram and invocation"). One verse short |
| sirupanchamoolam | 98 | 96 | 97 with the invocation | 1 invocation + payiram | PM prints the invocation as 1 and the payiram as 98, so its 2-97 are 1-96 here |
| muthumozhikkanchi | 100 | 100 | 100 (ten tens) | none | |
| elathi | 82 | 80 | 80 | 1 invocation + payiram | |
| kainnilai | 60 | 60 | 60 | none | many lines lost in the tradition (dots kept) |

All sixteen: no duplicate ids. The only numbering gaps are the four lost Ainthinai Ezhupathu
verses. Each verse number is checked against its place in the sequence.

Thinai by verse:
- Kar 1-40 முல்லை.
- Ainthinai Aimpathu: முல்லை 1-10, குறிஞ்சி 11-20, மருதம் 21-30, பாலை 31-40, நெய்தல் 41-50.
- Thinaimozhi Aimpathu: குறிஞ்சி 1-10, பாலை 11-20, முல்லை 21-30, மருதம் 31-40, நெய்தல் 41-50.
- Ainthinai Ezhupathu: குறிஞ்சி 1-14, முல்லை 15-28, பாலை 29-42, மருதம் 43-56, நெய்தல் 57-70.
- Thinaimalai: குறிஞ்சி 1-31, நெய்தல் 32-62, பாலை 63-92, முல்லை 93-123, மருதம் 124-153.
- Kainnilai: குறிஞ்சி 1-12, பாலை 13-24, முல்லை 25-36, மருதம் 37-48, நெய்தல் 49-60.

The five-block tables are in the script. Each one is checked against the source's own headings,
and they agree everywhere except Kainnilai's last heading. The source heads 49-60 "5.பாலை", a
slip: பாலை is already 13-24, and these verses are set on the shore (சேர்ப்ப, துறைவன், கானல்). They
are recorded as நெய்தல் and flagged.

## Parsing notes (each case is flagged)

- Verse numbers come in four forms: a number at the end of the last line (`… 5`, `… 50.`,
  `… (1)`); a line of its own (`1.`, as in Kainnilai and Pazhamozhi); a number in front of a
  modern heading (Acharakkovai, Thirikadugam); and `N. text` for each saying (Muthumozhikkanchi).
- Unnumbered verses are numbered by their place: Thirikadugam 26, 46, 95 and Kalavazhi 41.
  tamilvu agrees on all four.
- Misprinted number: Thinaimalai 135 is printed "(35)".
- A blank line inside Thirikadugam 22 is joined. Stray end digits ("2" after Kainnilai 42, "9"
  after 49, "0" after 30, "5" after 35) are dropped.
- Muthumozhikkanchi: the refrain ஆர்கலி யுலகத்து மக்கட் கெல்லாம் is printed once, before the first
  saying of each ten, and it is kept only there. Sayings 1, 11, 21 … have two lines, the rest one.

## Repairs to the text (33, each flagged `repaired`)

- ௌ written as ெ + ள, as in பெளவம், வெளவான், கெளவை (13 places). Pattern: `ெளவ` becomes `ௌவ`.
- `|` typed into a line (5), `·` for ஃ (1), and a stray space before a dead consonant
  (`திண்டோ ர்`, `நட்டோ ன்`) (4).
- Kalavazhi 32: the word `[தீர்ந்த` is printed at the end of line 1 and belongs at the end of line 2.
  tamilvu reads it so.
- Nine single-letter misprints where tamilvu reads otherwise and the PM form is not a word:
  - Thirikadugam 1 தெடார்ச்சியும் > தொடர்ச்சியும், and 96 சொய்வான் > செய்வான்
  - Kar 4 வாடம > வாடும்
  - Nanmanikkadigai 6 பிறானக் > பிறனைக், and 14 கிளைக்குழம் > கிளைக்குழாம்
  - Iniyavai 5 யார்மட்டும் > யார்மாட்டும், and 34 சோர்வின்றச் > சோர்வின்றிச்
  - Muthumozhikkanchi 61 பேரறவினோன் > பேரறிவினோன்
  - Kalavazhi 37 முத்தடைக் > முத்துடைக்

## Lost vowel signs and other open readings (flagged, not changed)

- `misprint_candidate` (21): places where tamilvu has a vowel sign that PM lacks, or the other
  e/o sign, and PM's form is also a word or a known variant. Examples:
  - Innaa 5 உறைசேர் / tamilvu சோர் (PM's own variant reading is புரைசேர்)
  - Muthumozhikkanchi 13 சேரா / சோரா
  - Muthumozhikkanchi 83 உறவோனை / உறைவோனை
  - Thirikadugam 76 வருந்தும் / விருந்தும்
  - Nanmanikkadigai 6 மன்னர்ச் / முன்னர்ச்
  - Kalavazhi 12 போன்றவெ / போன்றனவே
- `line_count`: Kalavazhi 17 has 4 lines. tamilvu has 5: PM lacks the refrain line போர்க் கொடித் தானை, பொரு புனல், நீர் நாடன்.
- `unicode`: Elathi 56, line 2, `உயை஡ளர்`, has the unassigned code point U+0BA1, an old
  encoding leftover. The reading (perhaps உழையாளர்) could not be checked, because no other
  edition of Elathi was found online. It is left as printed.
- `lacuna` (43): Kainnilai lines given as dots, wholly or partly.
- `lost_vowel_sign`: a word that starts with a dead consonant, or a vowel sign after a space.
  After the repairs above, nothing is left in this class outside the editor's bracketed letters.

## Differences from sangamtamil.com

The site's verse text is Project Madurai's, letter for letter, wherever both have the verse.
Every `reading differs` flag is one of the repairs above, where the site keeps PM's slip. The
site's own faults:

- **Verses it lacks** (`site_diff`, "the site lacks this verse"), 25 in all:
  - Innaa 1; Kalavazhi 41
  - Thinaimozhi 44; Ainthinai Ezhupathu 27
  - Thinaimalai 1 and 135 (it gives the misprinted "35" twice)
  - Acharakkovai 47, 64, 97 (numbers printed as `47 ` and `64,`)
  - Pazhamozhi 243 and 387-399
  - Sirupanchamoolam 76; Elathi 41
- **Lines it loses at the top of a verse** (`site_lacks_lines`): Nanmanikkadigai 43; Ainthinai
  Aimpathu 10; Thinaimozhi 11; Thinaimalai 29, 136, 138; Acharakkovai 38; Pazhamozhi 77, 137;
  Sirupanchamoolam 7, 83, 89; Elathi 17, 45. In Kainnilai it drops the all-dot lines (15, 35,
  and the ten verses listed in the lineation flag).
- **Headings run into the verse**: in 234 verses the site's text carries PM's headings, thurai
  labels, metre labels or notes. Examples: Kar's thurai in 39 of 40 verses, Acharakkovai's metre
  label in 97, and Kainnilai's துறை notes in 42. These are one aggregated flag per book.
- **Muthumozhikkanchi**: the site's verses 1-10 are the decade headings, and for 11, 21 … 91 it
  keeps only the refrain line, so its numbering of the sayings is wrong.
- **Sirupanchamoolam**: the site keeps PM's numbering, with the invocation as 1 and the payiram
  as 98.

## Open problems

1. **Pazhamozhi has 399 verses, not 400.** PM states the total itself. The site has 385, and
   tamilvu's Pazhamozhi was not found. Which verse is missing is unknown.
2. **Elathi 56**: an unassigned code point (above).
3. **Kalavazhi 17**: a line lost in PM. tamilvu's word-split reading is in the flag and is not
   put into the text.
4. **No arbiter for nine works**: Ainthinai Aimpathu, Ainthinai Ezhupathu, Thinaimozhi,
   Thinaimalai, Acharakkovai, Pazhamozhi, Sirupanchamoolam, Elathi and Kainnilai. For these, the
   lost-vowel-sign check is only the in-text heuristics, and the site is no independent witness.
5. **Two numbering choices** to confirm against a printed edition: Nanmanikkadigai's two
   invocation verses, and Sirupanchamoolam's invocation and verses 1-96.
6. **Kainnilai's thurai notes** are not ingested. Their source is unclear.
7. **Rerun order**: `build_sangam_core.py` rewrites the flags file and drops these flags.
