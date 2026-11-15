# Plan: a systematic pass for Kural links

Status: the pilot (stages 1 to 4) ran on 2026-11-15 and passed. The full run has not started.

## Pilot results

| Measure | Pass mark | Result |
|---|---|---|
| Share of proposals graded sound | 60% | 201 of 223 (90%) |
| Known sound links found again | 60% | 45 of 73 (62%) |
| Calibration links matching their earlier grade | 28 of 40 | 29 of 40 |
| Pilot verses with a sound link | None | 99 of 100, up from 55 |

- 166 new links entered the graph: 147 sound and 19 weak. One forced proposal was rejected.
- The graders were not lenient: on the 40 known links they lowered 7 grades and raised 3.
- Recall only just passed. Proposers may add at most 3 links per verse, so some known links lose
  their place to others.
- The proposals' notes are longer and more careful than the earlier links' notes. Graders judge a
  link as written, so a persuasive note may raise a grade: 10 pairs earlier graded weak were graded
  sound with their new note.
- Two changes from the plan below: five proposing agents took two chapters each, and they read
  other verses through `link_pass.py verse`, because whole chapters overflowed an agent's context.
- The pilot used about 1.6 million tokens: 1.0 million to propose and 0.6 million to grade. At that
  rate the remaining 123 chapters need about 19 million, more than the estimate under "Cost".

Results are in `kg/kural/link_pass.json` and `kg/kural/rejected_links.jsonl`.

## The problem

The 576 links came from agents that each read one chapter and added the links they happened to
notice. The marking rules also told them to keep links few and to prefer links between chapters.
Nothing compared each verse with the rest of the book.

- 583 of the 1,330 verses have no link.
- In chapter 1, verses 3, 4, 5 and 8 have no link, although 3 and 10 both speak of reaching the
  feet of the First One.
- The audit grades say which existing links are sound. They can't find links nobody proposed.

## What was measured first

The cheap way to find candidates is to score every pair of verses by what they share. Three signals
were tested against the 354 distinct pairs already graded sound, taking each verse's best matches:

| Signal | Pairs produced | Sound links recovered |
|---|---|---|
| Shared concepts, top 20 per verse | 13,780 | 99 of 354 |
| Similar English readings, top 20 | 16,636 | 110 of 354 |
| Shared Tamil words in verse and commentary, top 20 | 16,548 | 141 of 354 |
| All three combined, top 20 | 16,630 | 156 of 354 |
| All three combined, top 30 | 25,297 | 191 of 354 |

Even 25,000 candidate pairs miss 46% of the links known to be sound. The valuable links are thematic
and often share no wording, so word overlap can't be the main method. It stays as a hint only.

## Approach: every proposer sees the whole book

The 1,330 readings total about 134,000 characters, small enough for one agent to hold in full.
So each proposing agent gets an index of the whole Kural and works through its own chapters verse by
verse against that index.

### Stage 1. Build the inputs

- `scripts/link_pass.py index` writes one line per verse: number, chapter, concepts and reading.
- `scripts/link_pass.py hints` writes each verse's 10 best word-overlap matches, as hints.
- Existing links are hidden from proposers, so the sound ones work as a test of recall.

### Stage 2. Pilot on 10 chapters

Chapters 1, 4, 25, 33, 39, 55, 64, 98, 110 and 116: all three books, and chapters already studied.

- Two proposing agents take five chapters each.
- For every verse, the agent shortlists verses from the index, then reads the Tamil and commentaries
  of both verses before proposing. It may propose up to 3 links per verse.
- "No link" is a valid answer and needs a one-line reason.
- The type rules in `kg/themes/SCHEMA.md` apply, including the test for tensions.
- Links inside a chapter are allowed in this pass and are marked as such, because the earlier rule
  against them left real connections out.

### Stage 3. Grade the pilot blind

- Separate grading agents grade every proposal with the instructions used for `link_audit.json`.
- Each grading packet also contains 20 links with known grades, unmarked, to check for drift.
- A pair proposed from both ends is graded once.

### Stage 4. Decide whether to go on

| Measure | Pass mark |
|---|---|
| Share of proposals graded sound | 60% or more |
| Known sound links touching the pilot chapters that were found again | 60% or more |
| Calibration links matching their earlier grade | 28 of 40 or more |
| Verses in the pilot still without a link | Reported, no pass mark |

If the pilot fails a mark, the instructions change and the pilot runs again before any full run.

### Stage 5. Full run

- 27 proposing agents, five chapters each, run in batches of 8.
- Grading agents take about 55 proposals each.
- Expected volume is 2,000 to 4,000 proposals. The pilot will narrow this.

### Stage 6. Merge

- Sound and weak links enter the graph with their grade and `source: "systematic_pass"`.
- Forced and wrong proposals go to `kg/kural/rejected_links.jsonl` and stay out of the graph.
- Existing links keep their grades. A duplicate of an existing link is dropped.
- The threads are then reviewed against the larger set of sound links.

## Cost

Token counts are estimates from the last audit, which used about 1.2 million tokens for 443 links.

| Step | Agents | Tokens, roughly |
|---|---|---|
| Pilot: propose | 2 | 0.5 million |
| Pilot: grade | 3 | 0.5 million |
| Full run: propose | 27 | 5 million |
| Full run: grade | 40 to 70 | 6 to 11 million |

The full run is large enough that it should start only after the pilot's numbers are in.

## Limits

- Proposers and graders are all Claude, without a Tamil lexicon. Shared blind spots remain.
- No Tamil scholar has reviewed the existing marks, and this pass doesn't change that.
- A semantic search over embeddings was considered and left out. It needs a new package or an
  outside service, and such models are untested on classical Tamil verse.
- 265 verses have source text flagged for checking. Proposals touching them carry that flag.
