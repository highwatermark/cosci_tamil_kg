# Brief: grading Siddhar verse / science finding pairs

You are grading pairs that join a verse of the Siddhar songs (`siddhar:N`, sometimes a
Tirumanthiram verse) to a one-sentence summary of a current scientific finding
(`finding:...`, listed in `kg/science/findings.jsonl` with its sources). A script proposed most of
the pairs by word and concept-tag overlap; **some pairs in your packet are deliberate negative
controls** (a finding with a random verse, or a verse with a random finding). Nothing in the packet
tells you which is which. Grade every item on its merits, the same way, and do not try to guess
which items are controls. Don't aim for any particular share of high or low grades.

Read only your packet (`kg/science/grading/packet_NN.json`) and, if you need a source, the
finding's line in `kg/science/findings.jsonl`. Do not open `key.json`, `candidates.jsonl` or
`controls.jsonl`. Do not edit any file except your output.

## What you see

Each item gives the verse (Tamil, poet, work, a "reading" and a "nuance") and the finding (domain,
claim, strength: established / replicated / contested / speculative). **The reading and nuance
were written by Claude agents and are a claim to check, not evidence. Read the Tamil first.**

The Siddhars write in cipher (பரிபாஷை): sun and moon for the right and left breath, the horse
(வாசி) for the breath, the serpent, numbers, salt, body-places. A correspondence that needs a
cipher gloss the Tamil itself does not fix (for example, reading "sun" as "right nostril" in a
verse that never names breath or nostril) cannot be graded 3, and is usually 1. Say in
`cipher_dependent` whether the pairing relies on such a gloss.

## Grades

- **0** no real correspondence: the shared words are incidental, or the verse is about something
  else.
- **1** shared topic only: both concern breath, body, mind, death, metals, etc., but the verse
  makes no claim the finding speaks to.
- **2** the verse makes a specific claim that the finding bears on, either supporting it or
  contradicting it (e.g. the verse says a mercury preparation makes the body deathless; the
  finding is that ingested mercury is toxic).
- **3** a specific, testable correspondence that does not depend on a cipher gloss the Tamil
  doesn't fix: one could state the verse's claim as a hypothesis and the finding is evidence about
  that hypothesis.

Also give a **direction**:
- `supports`: the finding is evidence for the verse's claim
- `contradicts`: the finding is evidence against it
- `neither`: for grades 0-1, or where the finding is too speculative to point either way

A contradiction is as valuable as a support; grade it by the same rule. A finding labelled
`speculative` (Orch-OR, ego-dissolution models) can still be graded 2 if the verse makes a specific
claim it bears on, but its direction should usually be `neither` unless the evidence itself
(not the hypothesis) points one way. Quantum cognition is a mathematical model of human judgment,
not a claim that minds are quantum; a verse about the One pervading all things is not "supported"
by Bell tests. Treat generous readings as weak: a link that needs one is 1, not 2.

## Medical and alchemical verses

Siddha medical and alchemical verses are historical claims, never remedies. In your reason, name
what the verse claims (e.g. "claims mercury fixed by a guru's method gives a body that does not
die") but **do not reproduce dosages, ingredients lists, or preparation steps**, and never phrase
anything as advice.

## Output

Write a JSON array to `kg/science/grading/graded/packet_NN.<your-grader-name>.json`, one object per
item in packet order:

```json
{"item": "P03-17", "grade": 2, "direction": "contradicts",
 "reason": "One or two sentences citing the Tamil words that carry the claim (e.g. சாகாக் கால், இரசம்) and what the finding says about it.",
 "tamil_words": ["..."], "cipher_dependent": false, "text_issue": null}
```

`grade` is an integer 0-3. `reason` must cite at least one Tamil word from the verse for any grade
of 1 or more. `text_issue` is a short note if the Tamil looks corrupt, otherwise null.
