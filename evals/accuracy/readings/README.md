# Reviewing the Tamil readings

A Codex subagent read twelve verses directly from the Tamil in commit `cbd67a5`. The central reading was supported on eight. Two readings raised a minor problem and two require a classical Tamil reader to decide. Each book contributed four supported, one minor and one unresolved. No entry met the material-error threshold. This pilot measures agreement between an AI reviewer and existing AI interpretations on these examples. It cannot establish a corpus-wide translation accuracy percentage.

## Reproduce or extend the audit

1. Run `python3 -I evals/accuracy/readings/sample.py` from the repository. Each book's nonempty rows are ordered by verse number and divided into thirds of equal size to within one. In each third the two smallest SHA-256 digests of the seed, a pipe and the full verse ID determine the selection. Change the seed with `--seed` to draw a fresh packet. Reserve new cases for testing. The published twelve can now serve as training examples.
2. Give this Tamil-only output to a bilingual reviewer. Ask them to identify the speaker, grammatical subject, action, negation, petition or doctrinal claim, and mark the words supporting each. Write a tentative English gloss and any plausible alternative. Freeze that response before revealing earlier answers. In this run the subagent wrote [blind.tsv](blind.tsv) before opening the chapter files for the sample. Its SHA-256 was `ab5046727a20d83c71d12c97bd5c1f4b57880a2f541463405be078c40761d842`.
3. Run `python3 -I evals/accuracy/readings/reveal.py` with the same seed. Each row points to the chapter mark and gives matching first-line locations in the source edition. Compare the central claim first, then evaluate the uncertainty note and any concrete additions. Keep a reference to the reading of a named edition or commentator when it resolves an ambiguity. Distinguish an allusive name supplied by tradition from a name printed in the Tamil.
4. Grade each row and retain a short Tamil anchor and reason. **Supported** means the central claim and its agency survive comparison. **Minor** means a local lexical concern or misplaced certainty while the central point survives. **Material** means an identifiable contradiction or unsupported addition changes the agent, action, polarity, or central doctrinal claim. **Unresolved** means credible alternatives matter and the reviewer cannot decide between them. A classifier should receive credit for warranted uncertainty. Keep item-level results even if a second reviewer changes the grade.
5. A classical Tamil reader can do a fresh pass with step 1 before opening [the machine judgments](judgments.tsv). Begin adjudication with verses 216 and 1278, then inspect the local glosses at 1653 and 514. For a comparison of Codex prompts, reserve separately adjudicated cases and score both prompts against those same cases. Count false certainties separately from justified abstentions.

## What the examples show

| Book and verse | What to inspect |
|---|---|
| Tirumanthiram 216 | Who moves in the night or paired hours? The choice changes the account of ritual agency. |
| Tirumanthiram 1653 | The main reading supplies a witness holding a spark. The mark's own note also permits flint. A link about a witnessing soul would depend on an unsettled word. |
| Thiruppugazh 1278 | The song clearly seeks an end to rebirth and a state of silent bliss. Whether the final question asks Murugan to think of granting it or the speaker to contemplate it needs adjudication. |
| Thiruppugazh 514 | The break after நகை affects whether the pearl image qualifies the smile or the breasts. The petition for spiritual understanding survives either reading. |

These labels cover the primary reading, with particular attention to consequential ambiguity. They do not certify each proper name, plant gloss, image, concept tag, or link. This run had one source-first AI reviewer and one base edition per sampled verse. Difficult terms, independent textual witnesses and a second human judgment remain open. No modern translation was used as an answer key.
