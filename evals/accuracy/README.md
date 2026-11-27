# Evaluating readings and links in two Tamil books

Run on the graph at `cbd67a5`. There are three distinct questions. Does the reading preserve the Tamil? Does a proposed relation hold between these particular passages? Can the search find worthwhile pairs for a verse with few links? Each needs its own evidence.

## Results

| Evaluation | Result | What it measures |
|---|---|---|
| [Tamil-first reading audit](readings/README.md) | 8 supported, 2 minor concerns, 2 unresolved in 12 readings | One independent Codex reviewer compared its own blind reading with the stored interpretation. Both books contributed six cases. |
| [Sound-link coverage](links/README.md) | 1,170/2,783 Tirumanthiram verses and 564/1,325 Thiruppugazh songs have zero sound neighbours | Complete census across four built books, counting incoming and outgoing edges. |
| [Four-grade audit](links/scored.json) | 11/14 exact agreement, 13/14 sound versus other | A separate reviewer regraded a sample deliberately enriched for rare prior grades. |
| [Paired Codex prompt trial](comparison/prior_grades.csv) | Ordinary prompt matched 10/16 historical binary grades. Evidence-first prompt matched 8/16. | Two separate Codex workers saw the same Tamil pairs, proposed type and English claim, without existing grades. |
| [Candidate retrieval](retrieval/ranks.csv) | At rank 10, hidden target hits rose from 7/60 to 15/60 for Tirumanthiram and stayed at 5/60 for Thiruppugazh | Computational comparison of two ways to find candidate pairs among all 5,837 other verses. |
| [Search on isolated verses](retrieval/discovery_review.csv) | 2 of 8 top suggestions merited expert review | One fresh model reading of the top candidate for each of eight previously isolated anchors. All eight pairs lacked a graded edge. |

The ingest reports document the absence of an aligned verse-by-verse translation or commentary for these two books. The English mark is itself one proposed reading. A Tamil reviewer should record when an independent edition, urai or other textual witness changes the interpretation. See the [Tirumanthiram](../../docs/ingest/tirumanthiram.md) and [Thiruppugazh](../../docs/ingest/thiruppugazh.md) reports.

## Does the prompt improve Codex?

The ordinary prompt asked whether to accept each specific link as sound and requested one brief reason. The evidence-first prompt also asked the worker to parse both Tamil passages, attend to speaker and modality, identify anchors and the strongest mismatch, and require the named relation to survive. The proposal note was visible to both, so this tests reviewing an existing claim. Historical grades were revealed only after both CSVs existed. The packet had four sound, three weak and one forced pair per book, selected with a fixed seed.

| Prompt | Previously sound accepted | Previously weak/forced accepted | Precision against prior grades | Recall against prior grades |
|---|---:|---:|---:|---:|
| Ordinary | 6/8 | 4/8 | 6/10 | 6/8 |
| Evidence-first | 6/8 | 6/8 | 6/12 | 6/8 |

The workers disagreed on just C04 and C05. For C05 the evidence-first worker cited the conch imagery to support a connection between two accounts of sound. The ordinary worker questioned whether the dawn simile was itself an inward sound. This is a precise question for a Tamil reader. C03 is also informative. Both workers held a historically sound link because one speaker receiving instruction does not establish a universal requirement for a guru. The historical grades can be challenged in either direction. See the [packet](comparison/packet.json), [ordinary decisions](comparison/baseline.csv), and [evidence-first decisions](comparison/evidence_first.csv).

These were single runs with separate agent contexts, a small balanced sample and earlier AI labels. Precision varies with the mix of cases. These results give no basis for promoting the evidence-first prompt or claiming model-level superiority. The 14-item audit and 16-item trial used different samples and rubrics and should be read separately.

## Can search recover more pairs?

For each book, we sampled 60 distinct anchors with a previously sound outgoing link and chose one of their sound targets at random. Both searches ranked all other verses. The baseline used inverse-document-frequency weighted cosine similarity of concept IDs. The combined score added equally weighted similarities from Tamil character trigrams and words in English readings. Neither ranker used edges, link grades or proposal notes when scoring. A fixed shuffled order settled ties. Graph-derived readings and concepts may reflect earlier linking work, so performance on entirely new books may differ.

| Book and method | Target in top 1 | Top 10 | Top 50 |
|---|---:|---:|---:|
| Tirumanthiram, concepts | 2/60 | 7/60 | 16/60 |
| Tirumanthiram, combined | 7/60 | 15/60 | 28/60 |
| Thiruppugazh, concepts | 1/60 | 5/60 | 13/60 |
| Thiruppugazh, combined | 2/60 | 5/60 | 15/60 |

For Tirumanthiram the combined method brought nine targets into the top ten and displaced one. For Thiruppugazh it recovered the same five. Other high-ranked passages may also be valid. The numbers measure rediscovery of a chosen known pair, and cannot estimate recall of every valid literary connection. In the small [isolated-verse pilot](retrieval/discovery.json), the combined search retrieved candidates for all eight anchors. The reviewer proposed Tirumanthiram 2246/2251 and Thiruppugazh 1087/344 for expert assessment, and held six. Frequent ornaments and refrains account for several of the held Thiruppugazh pairs.

## Human review and the next Codex trial

1. Give two classical Tamil readers the Tamil-only [reading packet generator](readings/sample.py). Ask for speaker, agent, action, polarity, an English gloss, an alternate parse where credible, and the decisive words. Lock both glosses before revealing the stored interpretation and notes. Consult a named edition or commentator when needed and retain live disagreements. Begin adjudication of this run with Tirumanthiram 216 and Thiruppugazh 1278.
2. For the link trial, give each reader only [packet.json](comparison/packet.json) and a copy of the [blank review form](comparison/expert_form.csv). Record **accept** when the passages sustain the specific claim, type and direction, **hold** when the evidence falls short, and **unresolved** when competing readings need a witness. Enter one Tamil phrase per passage. Collect decisions independently, then record an adjudicated form. Score it with the command below. Human-unresolved items are reported separately.
3. Use the published cases for calibration. For a fresh benchmark, reserve whole chapters or hymn groups before prompt development, including linked and isolated verses. Balance within- and cross-book pairs, technical language, stock praise, changes of speaker, and genuine tensions. Include tempting same-topic pairs. Keep labels and reviewer rationales hidden from Codex. Use the same cases, model version and tool access for both prompts and repeat runs to measure variation. Report reading errors by severity and track confident errors on human-unresolved verses.
4. For a discovery test, sample anchors separately from those with no attempted links and those with only weak or rejected links. Pool top candidates from competing searches and a Tamil reader’s independent suggestions. Mask their origin, deduplicate, and have the readers judge each pair. Compare expert-accepted links per ten suggestions, newly covered anchors, within- and cross-book results, and review time. Include an explicit “no strong link found” outcome. This tests whether more search produces better coverage without paying for it in false links.
5. The next search variant worth testing for Thiruppugazh would downweight stock refrains and conventional images and retrieve by the specific petition, its speaker and a distinctive second detail. Cap near-duplicate candidates per query. Compare it on fresh expert-judged cases before using it for bulk graph edits.

## Reproduce

From the repository root on the stated snapshot, these commands regenerate the prompt packet, score both saved outputs, and rerun the deterministic searches. The two audit directories document their own rerun commands. Regeneration does not call a model. Fresh model judgments require fresh blinded workers.

```sh
python3 -I evals/accuracy/comparison/benchmark.py packet
python3 -I evals/accuracy/comparison/benchmark.py score
python3 -I evals/accuracy/retrieval/run.py
```

After expert adjudication, run the following with the path to the completed copy of the form.

```sh
python3 -I evals/accuracy/comparison/score_expert.py /path/to/adjudicated.csv
```
