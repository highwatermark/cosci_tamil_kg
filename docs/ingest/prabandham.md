# Ingest report: Nalayira Divya Prabandham (`prabandham`)

Outputs
- Script: `/Users/harilakshmanan/Cursor/cosci_knowledge_graph/scripts/parse_prabandham.py` (stdlib only; run `python3 -I scripts/parse_prabandham.py`; reads only `data/text/`; prints every repair as `CHECK ...`)
- Data: `/Users/harilakshmanan/Cursor/cosci_knowledge_graph/kg/core/prabandham.jsonl`, 3,961 records covering all 4,000 traditional pasuram numbers, in canonical order

## Record shape

`id` (`prabandham:N`), `number` (traditional 1-4000), `number_end` (only for the Siriya Thirumadal span record), `ayiram` (Mudhalayiram / Periya Thirumozhi (Irandam Ayiram) / Iyarpa / Thiruvaimozhi (Nalam Ayiram)), `work` and `work_ta`, `alvar` and `alvar_ta`, `pathu` (the hundred, for Periyalvar Thirumozhi, Periya Thirumozhi and Thiruvaimozhi), `decade` (the thirumozhi, for those three works plus Nachiyar and Perumal Thirumozhi), `decade_title` (Periyalvar and Nachiyar only: the source prints titles for these two alone), `verse` (verse in the decade, or in the work when it has no decades), `verse_in_work`, `tamil` (lines, with the printed local number removed), `printed_ref` (the number printed after the verse, kept as printed, e.g. `(2) 1.1.1`; `(2)` is the recitation-repeat mark), `source` (file:line of the number marker), `hart` (Kausalya Hart's English, or null), and `note` where a record needs explaining.

Thiruppavai is `work: "Thiruppavai"`, `alvar: "Andal"`, 474-503, verse 1-30. Thiruvaimozhi is `work: "Thiruvaimozhi"`, `alvar: "Nammalvar"`, 2791-3892, with `pathu.decade.verse` running 1.1.1 to 10.10.11.

## Files

Used, after deduplicating catalog rows 9-33 and 655 by file:

| File | Content |
|---|---|
| pmuni0005_01 | 1-473: Thiruppallandu, Periyalvar Thirumozhi (rows 9-10) |
| pmuni0005_02 | 474-947: Thiruppavai through Kanni Nun Siruthambu (rows 11-18) |
| pmuni0006_01, pmuni0006_02 | 948-2031: Periya Thirumozhi (row 19) |
| pmuni0007 | 2032-2790: the Iyarpa works (rows 20-31), plus a complete but badly numbered Ramanuja Nootrandadi |
| pmuni0008_01, pmuni0008_02 | 2791-3892: Thiruvaimozhi (row 33); 3913-4000: Ramanuja Nootrandadi verses 21-108 (row 32) |
| pmuni0517_01, pmuni0517_02 | Thiruvaimozhi with Kausalya Hart's English (row 655) |

Rejected: none of the catalogued files. The tanians (invocatory verses by later teachers), metre names and the `வாழி` closing verses were left out because they are not among the 4,000 pasurams. In pmuni0517 I used only Hart's English. Her Tamil, which splits the words, served only to align the English and was not used as base text.

## Counts against the traditional 4,000

Every work matches its traditional count: Thiruppallandu 12, Periyalvar Thirumozhi 461, Thiruppavai 30, Nachiyar Thirumozhi 143, Perumal Thirumozhi 105, Thiruchanda Viruttam 120, Thirumalai 45, Thiruppalliyezhuchi 10, Amalanadipiran 10, Kanni Nun Siruthambu 11, Periya Thirumozhi 1,084, Thirukurunthandakam 20, Thirunedunthandakam 30, the three Thiruvandhadis 100 each, Nanmugan Thiruvandhadi 96, Thiruviruttam 100, Thiruvasiriyam 7, Periya Thiruvandhadi 87, Thiruvezhukutrirukkai 1, Periya Thirumadal 78, Thiruvaimozhi 1,102 and Ramanuja Nootrandadi 108. The one exception is the **Siriya Thirumadal (2673-2712)**, which is a single record (see below). That gives 3,961 records covering 4,000 numbers, with nothing missing, nothing doubled and the order checked.

The decade structure checks out against the tradition:
- Periyalvar Thirumozhi has 5 pathus with 9, 10, 10, 10 and 4 thirumozhis. 1.2 has 21 verses and 2.3 has 13.
- Nachiyar Thirumozhi has 14 thirumozhis. Perumal Thirumozhi has 10, with sizes from 9 to 11.
- Periya Thirumozhi has 11 pathus, the last with 8 thirumozhis. 10.7 has 14 verses.
- Thiruvaimozhi has 100 decades of 11 verses, except 2.7, which has 13.

**Siriya Thirumadal** (`prabandham:2673`, `number_end: 2712`): the source prints it as one poem labelled `2712:`, numbered in 77 couplets (number 44 is printed twice) plus a closing line. It does not mark the 40 traditional pasuram divisions, and I did not invent them. Later stages should treat it as a single unit, or split it from a better edition.

## Alignment

| Field | Translator | Aligned to |
|---|---|---|
| `hart` | Kausalya Hart, English, Thiruvaimozhi only | **1,092 of 1,102** Thiruvaimozhi pasurams |

Method: Hart's 1,102 numbered Tamil verses were paired with 2791-3892 by position. Each pair was checked with letter trigrams, and the weakest match was 0.25 (2794, a very repetitive verse that still beat its neighbours at 0.06). Ten records are null because Hart's file repeats the previous verse's English in their place, so their own translation is missing from the corpus: 3208, 3377, 3392, 3394, 3404, 3407, 3410, 3412, 3426 and 3720. Hart misprints her Tamil label 3858 for 3859, and position corrects it.

Five spot checks, read in full:
1. **2902 (2.1.2)** `கோட்பட்ட சிந்தையாய்க் கூர்வாய அன்றிலே` matches "O sharp-beaked andril bird, do you plunge into deep thought like me?" Correct.
2. **3303 (5.7.5)** `எய்தக் கூவுதல் ஆவதே எனக்கு?` matches "...that is something I myself have seen. How can I call and reach you?" Correct. The source misprints this number as 3302.
3. **3550 (7.9.10)** `உதவிக்கைம் மாறென் னுயிரென்ன` matches "If I want to give my life to him for the things he did for me…" Correct. The source misprints this number as 3560.
4. **3788 (10.1.6)** `கூத்தன் கோவலன் … திரு மோகூர் ஆத்தன்` matches "He dances the kuthu dance… the god of Thirumogur…" Correct. The source misprints this number as 3888.
5. **3859 (10.7.11, phala-sruti)** `மானாங்கார மனம்கெட … திருமாலிருஞ்சோலைமலைக்கே` matches "Saḍagopan of Thirukurugur… these ten pasurams on Thirumalirunjolai…" Correct. Hart labels this one 3858.

Structure spot checks: 474 opens with `மார்கழித் திங்கள்` and 503 with `வங்கக் கடல் கடைந்த`, which are Thiruppavai 1 and 30. 2791 is `உயர்வற வுயர்நலம்` (1.1.1), 3892 is `அவாவறச் சூழரியை` (10.10.11), and 4000 is Nootrandadi 108.

## Copyright sidecar map

```json
{
  "tamil": {"who": "the twelve Alvars (c. 6th-9th c.) and Thiruvarangathu Amudhanar (12th c.)", "rights": "public domain"},
  "hart":  {"who": "Kausalya Hart, English translation of Thiruvaimozhi (Project Madurai, 2010s)", "rights": "modern"}
}
```

Hart is living or recently active, and her translation is in copyright. Later stages should quote at most a few words of `hart`. The Tamil base text is the Project Madurai edition, published under their usual terms.

## Text problems

Number repairs (each is printed by the script):
- 753 printed twice: the second is 754.
- 761 printed twice with identical text: the duplicate was dropped.
- 780 and 781 should be 800 and 801. 913 printed twice: the second is 914.
- 1287 should be 1487. 1748 carries a trailing word (`1748 பெரிய திருமொழி`) and 2010 is printed `2 010`; both are parsed.
- 2576 printed twice: the first is 2575.
- 2673 and 2674 should be 2713 and 2714, the opening of the Periya Thirumadal.
- 3302 printed twice: the second is 3303. 3560 should be 3550, 3652 should be 3642, and 3888 should be 3788.

Ramanuja Nootrandadi: pmuni0008_02 jumps from 3892 to 3913, so verses 1-20 are missing there. I took 3893-3912 from pmuni0007's copy, which is numbered `2788:`-`2795:` and then not at all; the verse number printed at the end of each verse identifies it. Those records carry a `note`. That copy's own count breaks at verse 86, which is printed without a number, but this does not affect the output.

Printed decade references:
- In Periya Thirumozhi, 1831 reads `9.9.40` for 9.9.4. The 10th verse of most decades in pathus 10-11 has no reference, and the metre heading of the next decade is glued onto it; 15 such headings were removed.
- In Thiruvaimozhi, 3662-3672 are printed `9.9.1`-`9.9.11` for 8.10.1-8.10.11. They were repaired by sequence, and the 9th pathu then follows correctly from 9.1.1.
- Some references are printed oddly but are read correctly: `(6.1.10)` on a line of its own, `4-10-8`, `(5.6 .9)`, `1.6. 2` and `10. 5.3`.

Corrupted text:
- 2035 (Thirukurunthandakam 4) has 7 lines instead of 8; one line is missing in the source.
- A stray Latin `f` appears inside Tamil words in 87 records, mostly in Periya Thirumozhi and Thiruvaimozhi (e.g. `பதம்f`). It is an old font artefact.
- `_` stands in for a lost letter (usually நூ/நு) in 56 records, e.g. `முப்புரி _லொடு`.
- One HTML `< br>` in 1581 was split into two lines.
- `*` caesura marks appear in 3899 and 3908.

These were left as printed.

Headers inside the text: the tanians, metre names, `திருவடிகளே சரணம்` lines and the `ஸ்ரீ:` invocations all sit between verses, and the parser excludes them. Hart's file has `--- continued in part 2 ---` and `SUBHAM` trailers, which are stripped.

## Suggested unit for later marking

Mark **per decade (thirumozhi / pathigam)** for the decade-structured works: Periyalvar Thirumozhi, Nachiyar Thirumozhi, Perumal Thirumozhi, Periya Thirumozhi and Thiruvaimozhi, about 3,000 of the 4,000 pasurams. A decade is the traditional unit of recitation and commentary. It usually has one shrine (divya desam), one mood (such as the nayika voice of the girl, the mother or the friend) and one refrain, and its last verse (phala-sruti) names the decade's own theme. Single verses inside a decade often only repeat the refrain and would produce thin, repetitive marks. Keep the verse as the citation unit, so links still point at `prabandham:N`.

For the antadi and viruttam works, which are chains of standalone verses (the three Thiruvandhadis, Nanmugan Thiruvandhadi, Thiruviruttam, Periya Thiruvandhadi, Thiruchanda Viruttam, Thirumalai and Ramanuja Nootrandadi), and for Thiruppavai, mark **per verse**: each one is a complete poem. For Thiruvasiriyam, Thiruvezhukutrirukkai and the two Madals, mark the whole work, since they are continuous single poems.
