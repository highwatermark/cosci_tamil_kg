# Siddhar claims and current science

This folder pairs claims in the Siddhar songs (and optionally their parent text, the
Tirumanthiram) with current scientific findings. Every verse × finding pair is scored, the best
are graded blind next to negative controls, and a pair is kept only if it beats the controls.

## Files

| file | what it is |
|---|---|
| `findings.jsonl` | 60 findings, each a one-sentence paraphrase (never quoted abstract text) with domain, strength, sources (DOIs/URLs of peer-reviewed reviews, meta-analyses or key trials, mostly 2018-2026) and keywords |
| `concept_map.json` | hand-written map from the Tamil concept ids in `kg/themes/concepts.json` to English keywords |
| `candidates.jsonl` | the top 300 verse × finding pairs by overlap score |
| `controls.jsonl` | 100 seeded negative controls |
| `pair_scores_summary.json` | distribution over all 162,060 pairs and selection parameters |
| `grading/packet_NN.json` | 10 blind packets of 40 shuffled, unlabelled items |
| `grading/key.json` | which item is a candidate or a control (graders must not read it) |
| `grading/graded/` | grader output (one file per packet per grader) |
| `strong_links.jsonl`, `threshold_summary.json` | output of the threshold step |

Scripts: `scripts/science_pairs.py` (score, select, controls, packets) and
`scripts/science_threshold.py` (unblind, threshold). Both run with `python3 -I`, stdlib only.
Grader brief: `docs/science-grader-brief.md`.

## Method

1. **Findings.** About 60 findings were drawn from peer-reviewed reviews and meta-analyses across
   slow breathing and HRV, the nasal cycle and single-nostril breathing, interoception, the default
   mode network, ego dissolution, predictive processing, embodied cognition, attention and
   mind-wandering, sleep, circadian rhythm, fasting and ageing, placebo, heavy-metal toxicity of
   metal-based Indian preparations, herbal pharmacology, pulse-diagnosis reliability,
   neuroplasticity, quantum physics and quantum-consciousness hypotheses, and a few
   psychology and population-genetics results that speak to recurring Siddhar themes (desire,
   death, caste, siddhi powers). Strength labels are deliberately conservative: Orch-OR and
   related microtubule results are `speculative`; quantum cognition is labelled as a mathematical
   model of judgment, not a claim about quantum brains. Findings that contradict Siddhar claims
   are included on purpose: mercury toxicity and contamination data, limits on human lifespan,
   the failure of psi research, the fact that gold can be made from mercury only by nuclear
   reaction, the low reliability of pulse diagnosis, and null results for meditation and brain
   structure.
2. **Scoring every pair.** For each of the 2,701 Siddhar verses × 60 findings, the score is
   `sum over the finding's keywords of (2 × concept weight if a verse concept tag maps to it) +
   (1 if it appears in the verse's reading or nuance)`, divided by √(number of keywords). Concept
   tags of rank 1 weigh 1.0, rank 2 0.8, others 0.6. A pair needs at least two keyword hits.
3. **Selecting candidates.** Each finding first gets its two best pairs (so every science domain
   is tested), then the rest are filled by global score, capped at 10 per finding and 2 per verse,
   up to 300. Without the caps a few keyword-rich findings (mantra, maya, the body) would take
   most slots. `--with-tirumanthiram` adds the 2,783 Tirumanthiram verses to the pool.
4. **Negative controls** (seed 20261125): 50 pairs of a candidate finding with a random verse, and
   50 pairs of a top-third candidate verse with a random finding. They go through the same
   packets, unlabelled.
5. **Blind grading.** Candidates and controls are shuffled into packets of 40. Graders score 0-3
   (0 none, 1 shared topic, 2 a specific claim the finding bears on, 3 a specific, testable
   correspondence not reliant on a cipher gloss the Tamil doesn't fix), with a direction
   (supports / contradicts / neither) and a reason citing the Tamil.

## How the threshold is set

The threshold is not chosen in advance; it comes from the controls. `science_threshold.py`
averages the grades of all graders per item, takes the 95th percentile of the control grades,
and calls a candidate **strong** only if

- its mean grade is ≥ 2, **and**
- its mean grade is above the 95th percentile of control grades, **and**
- its overlap score is above the 95th percentile of control overlap scores.

So if graders are lenient enough to give more than 5% of random pairings a 2, the bar rises to
above 2 (in practice, 3), and if they give random pairings 3s, almost nothing passes. The
summary also reports the control false-positive rate (share of controls graded ≥ 2): that is the
honest estimate of how many "strong" links are produced by graders finding patterns anywhere.
The third condition is nearly automatic for the current run (control overlap p95 ≈ 1.5, lowest
candidate 1.57) and is there to keep the rule meaningful if parameters change.

## Medical and alchemical verses

Siddha medical and alchemical verses (வாதம், கற்பம், இரசம், மருந்து) are recorded as
**historical claims, never remedies**. Nothing in this folder gives or endorses a dosage,
ingredient list or preparation step, and graders are told not to reproduce them. Where a verse
claims a mercury or metal preparation gives a deathless body, the relevant findings are the
toxicology and contamination data, which contradict it. Metal-based traditional preparations
have caused serious lead, mercury and arsenic poisoning.

## Caveat: correspondence is not confirmation

A "strong" link means a blind grader judged that the verse makes a specific claim a modern
finding bears on, more clearly than random pairings do. It does not mean the Siddhars
anticipated the science, that the finding confirms the verse's metaphysics, or that a practice
is safe or effective. Many links are contradictions. Supporting links are usually about a
general observation (a restless mind, a body that decays, slow breath calming) that many
traditions share. The findings themselves vary in strength; read the `finding_strength` field
before citing a link, and check the cited source, not the one-sentence paraphrase. The readings
and nuances of the verses were written by Claude agents and are themselves interpretations.

## Status

Packets are written; grading is pending (10 packets, too many for one grader, to be run by
parallel graders). After grading, run `python3 -I scripts/science_threshold.py`.
