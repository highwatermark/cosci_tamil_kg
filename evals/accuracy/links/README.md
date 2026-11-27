# Sound-link coverage and blind regrading

The snapshot is `cbd67a5fb8550f8880700aa894f2985a81411835`. A verse can have many links in one file and still leave its neighbours isolated. The census counts each distinct neighbour once, accepts incoming and outgoing edges, excludes self-links, and counts a pair when any graded record for that pair is sound. The denominator is every unit with nonempty Tamil. Thiruppugazh 206 is empty in this edition.

| Across all four built graphs | Tirumanthiram | Thiruppugazh |
|---|---:|---:|
| Readable verses or songs | 2,783 | 1,325 |
| Zero sound neighbours | 1,170 (42.0%) | 564 (42.6%) |
| Exactly one sound neighbour | 991 | 533 |
| Two or more sound neighbours | 622 | 228 |
| At least one sound neighbour from another book | 539 (19.4%) | 609 (46.0%) |
| No graded link of any quality | 541 | 113 |
| At least one graded link but none sound | 629 | 451 |

Tirumanthiram’s own file contains 1,426 sound records out of 2,260 graded ones. Thiruppugazh’s contains 847 out of 1,527. Counting only the book’s own file misses 39 and 6 additional units, respectively, connected by a sound edge in another book’s file. The coverage JSON contains both calculations and the complete list of isolated IDs.

## Four-level regrade

One Codex subagent graded the Tamil, proposed relation and note before opening the historical grades. English verse readings, commentator interpretations, historical grader reasons and grades were omitted from the packet. The reviewer applied the four grade definitions in `docs/refine-grader-brief.md`. A fixed SHA-256 ordering selected three sound, two weak, one forced and one wrong record per book. The reviewer knew those quotas. The same hash was used for display order, which can correlate with grade rarity. For a future examiner, shuffle independently and withhold the sampling design.

| Historical grade | Sampled | Regraded sound | Weak | Forced | Wrong |
|---|---:|---:|---:|---:|---:|
| Sound | 6 | 6 | 0 | 0 | 0 |
| Weak | 4 | 0 | 4 | 0 | 0 |
| Forced | 2 | 1 | 1 | 0 | 0 |
| Wrong | 2 | 0 | 0 | 1 | 1 |

Exact agreement was 11/14. Agreement on whether a link is sound was 13/14. Sampling deliberately overweights rarer grades. Six confirmations by a second AI cannot establish a corpus-wide precision rate. Recall of unproposed links requires independent discovery and adjudication.

* **Review first.** Thiruppugazh 973 pairs desire for shoulders with crossing a boundary, மடவார்தோள் / வரம்பு கடந்து. Kural 919 pairs soft shoulders with the description வரைவிலா. The original grade was forced. The reviewer judged the shared pair of motifs and the change in who crosses a boundary sufficient for a sound comparison. A scholar should decide whether the proposed gloss of வரைவிலா works in context and whether the note’s wording implies unsupported borrowing.
* **A comparison worth keeping.** Thiruppugazh 436 and 271 both describe poets likening patrons to extravagant objects and stealing poetry. The first song adds that the gold goes to women. The specific combined details support the existing sound grade.
* **A limit on interpretation.** Tirumanthiram 344 mentions an elephant hide, fire and sacrifice. Only 353 actually names Daksha. The reviewer and the former grader both rejected the claim that the two explicitly recount the same incident; their severity differed. A second textual witness could resolve the allusion.

## Repeat or extend

Run these from the repository root. Each prints JSON to standard output. The files here retain the outputs of this run along with the reviewer’s decisions keyed to packet ID. The packet can be regenerated if the source snapshot is available.

```sh
python3 evals/accuracy/links/audit.py coverage
python3 evals/accuracy/links/audit.py packet
python3 evals/accuracy/links/audit.py score
```

For an independent adjudication, give a classical Tamil reader only the packet. Ask them to write a grade, a deciding phrase from each verse, a plausible alternate parse, and whether a witness is needed. Lock the decisions before exposing the two AI judgements. For improving discovery, draw anchors separately from the “no link attempted” and “attempted but no sound link” groups and ask the reader to find and verify neighbours without seeing the current graph.
