# Ingest report: Tiruvasagam (Thirumurai 8, Manikkavasagar)

Book key: `tiruvasagam`

- Script: `/Users/harilakshmanan/Cursor/cosci_knowledge_graph/scripts/parse_tiruvasagam.py`. It uses the standard library only and reads only `data/text/`. Run it with `python3 -I scripts/parse_tiruvasagam.py`.
- Output: `/Users/harilakshmanan/Cursor/cosci_knowledge_graph/kg/core/tiruvasagam.jsonl` (661 records)

## Record shape

Each record has these fields:

- `id`: `tiruvasagam:N`
- `number`: Project Madurai's running number, 1–661
- `thirumurai`: 8
- `hymn`: 1–51
- `verse_in_hymn`
- `ref`: `8.hymn.verse`, e.g. `8.7.1`
- `hymn_title` and `hymn_subtitle`: the subtitle is the Saiva Siddhanta gloss, e.g. "மகாமாயா சுத்தி"
- for hymn 5 (Thiruchathakam) only: `decad_no`, `decad` and `decad_metre`
- `place`: where the hymn was composed (தில்லை, திருப்பெருந்துறை, திருஉத்தரகோசமங்கை, திருவண்ணாமலை, திருத்தோணிபுரம், திருக்கழுக்குன்றம், திருவாரூர்)
- `hymn_note`: the raw note on place and metre
- `unit`: `"akaval (whole hymn)"` for hymns 1–4, `"stanza"` for the rest
- `tamil`: the lines of the unit
- `pope`: `{title, text}` or null
- `hart`: a string or null

Thiruvempavai is hymn 7. It has 20 stanzas, numbers 155–174, ids `tiruvasagam:155` to `tiruvasagam:174`, refs `8.7.1` to `8.7.20`. All 20 have Tamil, Pope and Hart.

## Files

| Catalog row | File | Content | Used |
|---|---|---|---|
| 6, 7 | `pmuni0003_01`, `pmuni0003_02` | Tamil text, hymns 1–10 and 11–51 (both rows list both files) | base text |
| 163 | `pmuni0094` | G.U. Pope, English, hymns I–X | `pope` |
| 333 | `pmuni0222` | G.U. Pope, English, hymns XI–LI | `pope` |
| 798 | `pmuni0659` | Kausalya Hart, English, all 51 hymns | `hart` |

Rejected:

- Rows 113 and 114: Thirukkovaiyar (`pmuni0054`). Left out on instruction; another stage handles it.
- Row 934: Kunrakudi Adigal's *திருவாசகத் தேன்* (`pmuni0794`). These are essays, not a verse-by-verse commentary, and they are modern (he died in 1995).
- Rows 907, 1051 and 1156: a kummi, an ammanai and a pillaitamil *about* Manikkavasagar. They are separate works, not the text or a commentary on it.

## Unit counts

There are 661 units, numbered 1–661 with no gaps and in order: hymns 1–4 (the akavals) count as one unit each, and the other 657 units are single stanzas. The units per hymn match Project Madurai's table of contents for all 51 hymns:

```
1-4: 1 each   5:100  6:50  7-14: 20 each  15:14  16:9  17-29: 10 each  30:7  31:10  32:11
33-38: 10 each  39:3  40-43: 10 each  44:6  45:10  46:2  47:11  48:7  49:8  50:7  51:12
```

Compared with the traditional count ("about 656"):

- **Hymn 51 (Achchop pathigam) has 12 stanzas here (650–661). The usual edition has 9.** Pope translates 9. Stanzas 659–661 are also textually rough (they misspell the refrain as அச்சாவே and ரச்சோவே). They are probably later additions in Project Madurai's source edition. They are kept, with Tamil and Hart, and `pope` is null.
- Without those 3, the count is 658: 4 akavals + 654 stanzas. That is the other figure commonly cited for the book.
- The remaining gap between 658 and 656 cannot be settled from this corpus. Every other hymn matches both Pope's count and Hart's count, except hymns 13 and 14 (see below).
- Nothing is doubled. No running number is skipped or repeated in the Tamil.

## Alignment

| Field | Units aligned | Method |
|---|---|---|
| `hart` | 661 / 661 | Hart ends each stanza with Project Madurai's running number in brackets, `[N]`. Hymns 1–4 are taken as whole sections. |
| `pope` | 656 / 661 | Pope prints no Tamil. He ends each stanza with a running line count, `(4)`, `(8)` and so on, so the stanza index is that count divided by the hymn's step (3, 4, 6 or 8). Where a count is missing, the text is split at his Roman-numeral stanza headings. Hymns 1–4 are taken whole. |

Pope's 5 nulls:

- **294:** Pope's hymn XIII stops at XIX. The 20th stanza is untranslated.
- **314:** Pope's hymn XIV has 19 stanzas. The last stanza (ஏகாசமிட்ட...) is untranslated.
- **659–661:** the Acho pathigam extras described above.

Repairs, all printed by the script:

- Pope 104 and Pope 357 have no closing line count. Each was taken from the end of its hymn.
- In Pope's hymn XXI, stanza IX has no line count and X is labelled (36). The script followed the Roman headings.
- In Hart, the `[455]` marker is missing. The stanza was split from 456 at Hart's local number "8.".

Cross-check:

- Pope's stanzas were compared with Hart's stanzas in the same hymn by shared English words.
- 47 stanzas were flagged as matching a neighbouring Hart stanza slightly better. All the scores are low (similarity of 0.10 or less). Pope's archaic diction shares few words with Hart.
- I read the strongest flags (hymn 47 stanzas 619–623, hymn 21 stanzas 386–387, hymn 14) against the Tamil. All were correctly aligned.
- No hymn shows a run of stanzas shifted by one place, which is what a real misalignment would look like.

### Five spot checks (read against the Tamil)

1. **155 (Thiruvempavai 1, ஆதியும் அந்தமும் இல்லா அரும்பெருஞ் சோதியை):** Hart's "wonderful light without beginning or end" and Pope's "Splendour rare and great, that knows nor first nor end" both match.
2. **313 (Thiruvundiyar, தேரை நிறுத்தி மலையெடுத்தான் சிரம் ஈரைந்தும்):** Hart has Ravana's ten heads and twenty arms. Pope's title is "Ravana.", with "twice five of them perished". Both match.
3. **387 (Koyil Mutha Thiruppathigam 10, நல்கா தொழியான் நமக்கென்று):** Hart's "He will surely give me his grace" matches Pope's "He will not cease to pour on us His gifts". This confirms the Roman-heading repair.
4. **619 (Thiruvenba 3, செய்த பிழையறியேன்):** Hart's "I do not know what mistakes I have made", and Pope's "No sense of fault had I". Both match.
5. **650 (Acho pathigam 1, முத்திநெறி அறியாத மூர்க்கரொடு):** Hart's "bad people who do not know the path of moksha", and Pope's "fools, that knew not WAY of final peace". Both match.

I also checked 104, 293, 357, 386 and 456. All were correct.

## Copyright

| Source | Date | Status |
|---|---|---|
| Manikkavasagar (Tamil) | 9th century (traditional) | public domain |
| G.U. Pope (1820–1908) | *The Tiruvacagam*, Oxford, 1900 | public domain |
| Kausalya Hart | translation made available to Project Madurai by the translator; file dated 2019 | **modern, in copyright**. Project Madurai distributes it by permission. |

Sidecar rights map:

```json
{
  "tiruvasagam": {
    "tamil": {"author": "Manikkavasagar", "date": "c. 9th century", "rights": "public_domain"},
    "pope":  {"author": "G.U. Pope", "date": "1900", "rights": "public_domain"},
    "hart":  {"author": "Kausalya Hart", "date": "c. 2019 (PM release)", "rights": "modern"}
  }
}
```

Later stages should quote at most a few words of `hart`.

## Text problems

1. **Stray Latin letters inside Tamil words.** These are residue from the TSCII conversion. The script removes them and prints each line:
   - ஒளிfக்கும் (unit 3)
   - போற்fறி (unit 4)
   - திIட்டார் (unit 180)
   - தவிசிfட்டு (unit 234)
   - பதிfக்காசை (unit 278)
   - அடியுaர் (unit 373)
   - கழற்புaணை (unit 411)

   In அடியுaர் and கழற்புaணை, the "a" probably replaced a vowel sign (அடியார், கழற்புணை). After removal these two words are still misspelt, so treat them as corrupted lines.
2. **Hart stanza 455 is truncated in the source.** It ends mid-sentence ("…sweet nectar,") and has no `[455]` marker.
3. **Headers inside the text.**
   - In the Tamil, hymn 23's subtitle (சிவானந்தம் - அளவறுக்கொணாமை) sits on its own line, and hymn 7's metre sits in a second parenthesis. Both are handled and kept out of `tamil`.
   - Hart's hymn 51 heading is not marked with `#` ("51. Achoo padiham"). Hart's Thiruchathakam decad headings ("5.2. …") and the line ranges in hymns 1–4 ("1 -10") are all stripped.
   - Pope's hymn XI heading is not marked with `#`. A stray `### 'THE CHARACTERISTICS OF SACRED ENJOYMENT.'` inside hymn XXII is ignored.
4. **Misprints.**
   - The Tamil prints அருளயது for அருளியது in hymn 3's note. The script tolerates it.
   - The table of contents in the hymn 11–51 file prints ய'த்திரைப் for யாத்திரைப். This only affects the table of contents.
   - Pope's hymn XII Roman headings run "XVIII, IX, X" for 18–20. His line counts are right, so alignment uses those.
   - Some Pope stanzas (e.g. stanza 5) have an Arabic "1." heading, so their `pope.title` is null.
5. **Akavals (hymns 1–4).** They are kept whole: 95, 146, 182 and 225 lines. The trailing line numbers in the Tamil are stripped. Pope's text for each is his verse translation only. His introductions, notes and "Lines N–M" section headings are excluded.

## Suggested marking unit

**Mark per hymn (pathigam or decade). Keep the stanza as the unit for citation and linking.** Exceptions:

- **Hymns 7–51** (2–20 stanzas each) are built as single hymns. Many have a refrain, like Thiruvempavai's ஏலோர் எம்பாவாய் or Thellenam's தெள்ளேணங் கொட்டாமோ, and in those the stanzas are variations on one scene and one theme. The hymn subtitles already name that theme (e.g. "அனுபவவழி அறியாமை"). Per-stanza marking would produce many near-identical marks.
- **Hymn 5 (Thiruchathakam, 100 stanzas):** mark per decad, using `decad_no`. The ten decads have their own titles and metres. They are linked by anthathi (each stanza begins with the last word of the one before), so a decad reads as one movement.
- **Hymn 6 (Neethal Vinnappam, 50 stanzas):** mark in blocks of 10, or per stanza. It is one long petition with no internal headings, too big for a single mark.
- **Hymns 1–4 (akavals):** mark per hymn, but expect to cite line ranges. Sivapuranam and Potri Thiruvakaval cover several distinct topics, and Pope's and Hart's sub-headings give usable line ranges.
- **Thiruvempavai (hymn 7):** a candidate for per-stanza marking if it is a priority. Its 20 stanzas move through a sequence (waking the girls, the bath, the Margazhi rite), and individual stanzas are quoted and sung on their own.
