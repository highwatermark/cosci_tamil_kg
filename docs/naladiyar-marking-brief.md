# Brief: marking Naladiyar chapters

The repository at /Users/harilakshmanan/Cursor/cosci_knowledge_graph builds a knowledge graph of the
meanings, themes and threads of Tamil literature. The Thirukkural is fully marked. You are marking
chapters of the Naladiyar, the 400 Jain quatrains traditionally paired with the Kural, and linking
them to each other and to the Kural.

## Read first

- `kg/themes/SCHEMA.md`: the marking rules. Follow them exactly, with the changes below.
- `kg/themes/kural/ch038.json`: the worked example. Match its depth and style.
- `kg/themes/concepts.json`: the shared concept list. Reuse these ids; add a concept only when none
  fits, and name what the text names.

## Commands (run from the repository root)

- Your chapter's quatrains, Pope's translation and both commentaries:
  `python3 -I scripts/naladiyar_marks.py show 14`
- Validate your file: `python3 -I scripts/naladiyar_marks.py check 14`
- Any Kural verse with Tamil, Pope and commentary openings: `python3 -I scripts/link_pass.py verse 1061 1069`
- An index of all 1,330 Kural verses, one line each with concepts and a reading:
  `/private/tmp/claude-501/-Users-harilakshmanan-Cursor-cosci-knowledge-graph/56dc2695-7ba3-4110-8a35-77dd53b3fdc5/scratchpad/full/index.txt`

## Changes from the Kural schema

- Files go in `kg/themes/naladiyar/chNNN.json`. Verse keys are Naladiyar numbers.
- Commentators are `mudaliar` (V. Mahadeva Mudaliar, 1924, mostly word glosses) and `shanmuganar`
  (Sundara Shanmuganar, 1970, a prose commentary; in copyright, so quotes of at most 14 words).
  Pope's English translation is a third reading; it adds ideas at times, as it does for the Kural.
  Some quatrains lack one or more of these: say so rather than guess.
- Mark `contested` only where the two commentators, or a commentator and Pope, differ in substance.
- `links` may point within the Naladiyar (`"b": 152`) or to the Kural (`"b": "kural:1061"`). For
  every quatrain, look in the Kural index for a verse that makes the same claim, limits it, or says
  the opposite, and read that verse before linking. Many quatrains have one; some have none. At most
  three links per quatrain. The Naladiyar is a Jain work and stresses renunciation and impermanence
  more than the Kural does: where the two books diverge on the same question, that is a `tension`
  worth recording, but test it as SCHEMA.md says.
- The Book of Love here (chapters 38 to 40) has 30 quatrains, some of them dramatised speech.

## Rules

- Do not edit any file except your own chapter files. Do not commit.
- Read the Tamil first, then Pope, then the commentaries.
- If your chapters need a new concept, add it to the chapter's `new_concepts`; another step merges
  them into the shared list.
- When every file passes `check`, reply with only: the chapters done, new concept ids, the count of
  links to the Kural and within the Naladiyar, and any text problems.
