# Reading order and depth

The owner set this order on 2026-11-17 and, on 2026-11-22, moved the Siddhars to the head of the
remaining queue and Purananuru ahead of the Thevaram (see `docs/next-books.md` for why). Works that contain one another are read once, as part of the
larger work.

| # | Work | Contains | Unit for marking | Ingested |
|---|---|---|---|---|
| 1 | Naladiyar | | verse (400) | yes |
| 2 | Tirumanthiram | | verse (2,783 in the corpus) | yes |
| 3 | Thiruppugazh | | song (1,326) | yes |
| 4 | Siddhar songs, all Siddhars | | verse, keyed by `seq`; marked by poet in three passes | marked, linked and graded (2026-11-25) |
| 5 | Tiruvasagam | Thiruvempavai (hymn 7) | stanza (661) | yes |
| 6 | Aathichudi | read with Kondrai Vendhan, Nalvazhi, Moodurai | line or verse (270) | yes |
| 7 | Purananuru | | poem (398) | yes |
| 8 | Thirumurai | Thevaram, Thirukkovaiyar, Thiruvisaippa, 11th book, Periya Puranam | pathigam (hymn) | in progress |
| 9 | Divya Prabandham | Thiruppavai, Thiruvaimozhi | decade (pathigam); Thiruppavai per verse | in progress |

Tiruvasagam and Tirumanthiram are Thirumurai 8 and 10. Thiruppavai and Thiruvaimozhi are parts of the
Prabandham. They are marked at the position the owner gave them, and the Thirumurai and Prabandham
passes skip them.

## Depth

- **Verse by verse** for the didactic and philosophical works, whose single verses make distinct
  claims: Naladiyar, Tirumanthiram, Avvaiyar, Purananuru, the Siddhars, and Tiruvasagam.
- **Hymn by hymn** for the long devotional collections, decided by the owner on 2026-11-17. A
  Thevaram pathigam or a Prabandham decade varies one theme across ten or eleven verses, so the hymn is
  the unit of meaning. Thiruppugazh is marked per song, and Thiruppavai, at 30 verses, per verse.
- Every book reuses `kg/themes/concepts.json` and adds a concept only when nothing fits, so concepts
  are shared across books.
- Each book is linked within itself and to the books already in the graph, with the systematic link
  pass described in `docs/link-pass-plan.md`, then graded blind.
