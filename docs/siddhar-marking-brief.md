# Brief: marking Siddhar chapters

The repository at /Users/harilakshmanan/Cursor/cosci_knowledge_graph builds a knowledge graph of the
meanings, themes and threads of Tamil literature. Four books are marked and linked: the Thirukkural,
the Naladiyar, the Tirumanthiram and the Thiruppugazh. You are marking chapters of the Siddhar
songs: 43 works by 26 poets (Sivavakkiyar, Pattinathar, Pambatti, Agasthiyar and others, roughly the
10th to 18th centuries), parsed into `kg/core/siddhar.jsonl`. They are the Tamil texts of
*method*: breath, the body as cosmos, the eight powers, medicine and alchemy, the cipher the
Siddhars wrote in, and a running attack on ritual, caste and book-learning.

## Read first

- `kg/themes/SCHEMA.md`: the marking rules. Follow them exactly, with the changes below.
- `kg/themes/tirumanthiram/ch069.json` (the eight siddhis) and `kg/themes/tirumanthiram/ch112.json`:
  worked examples of depth and style for a text with no commentary.
- `kg/themes/concepts.json`: the shared list of 246 concepts. Reuse these ids (yogam, praanan,
  siththi, mounam, sivam, gnaanam, guru, malam, maayai, thaththuvam, andam, paazh, oli, karpu,
  manam, meyyunarvu, anbu, udal/yaakkai and the rest). Add a concept only when none fits, and name
  what the text names. Expected additions, if the verses use the word: வாசி (breath as the
  practice), பரிபாஷை (the Siddhars' cipher), அண்டபிண்டம் (body as cosmos), சூனியம் (the void),
  சுழுமுனை, குண்டலினி, இரசவாதம் (alchemy), மூலிகை. Tag a new concept only on your own verses.

## Commands (from the repository root)

- Your chapters' verses: `python3 -I scripts/book_marks.py siddhar show 55 56`
- Validate your files: `python3 -I scripts/book_marks.py siddhar check 55 56`
- Any verse of the four marked books, with reading and concepts:
  `python3 -I scripts/verse.py kural:1061 tirumanthiram:668 thiruppugazh:355` (`-r` for one line each)
- An index of every marked verse, one line each (`id | concepts | reading`), for finding links:
  `/private/tmp/claude-501/-Users-harilakshmanan-Cursor-cosci-knowledge-graph/56dc2695-7ba3-4110-8a35-77dd53b3fdc5/scratchpad/sid/index.txt`
  It is large: grep it for ideas, images and concept ids.

## Changes from the Tirumanthiram brief

- Files go in `kg/themes/siddhar/chNNN.json`. Chapter numbers are the tool's running numbers
  (1 to 142). **Verse keys are the `seq` numbers `show` prints as `## N`**, not the work's own
  numbers; the unit's own id (`siddhar:sivavakkiyam:285`) is printed beside it for reference.
- **There is no commentary in the corpus.** `show` may print `GLOSSES` (modern editors' word
  glosses, 68 units) and `VARIANT_NOTES` (an 1887 editor's variants). Use glosses to fix a word,
  never quote them (they are in copyright); no `positions`, no `contested`.
- **The Siddhars write in cipher and in refrain.** Mark `uncertain` when the sense turns on a
  technical or coded term (the sun and moon, the horse, the serpent, the eight and the sixteen, the
  letters அ உ ம, numbers, body-places), on a medical or alchemical formula, or on a corrupt word.
  In `nuance`, say which words carry the meaning and how tradition takes them, as tradition and not
  as fact. Where a plain and a coded reading both stand, say both. A short, true reading beats a
  full, confident one.
- **Formulas are history, not remedies.** Read a medicine or alchemy verse for what it claims and
  how it reasons; never restate a preparation as instructions.
- **Refrains.** Kummis and pulambals repeat one line (எக்காலம், வாலைப்பெண்ணே, பாம்பே). The
  reading is what the stanza adds, not the refrain. A stanza that only varies a formula may share
  a concept set with its neighbours; that is fine.
- `links` may point within the Siddhar corpus (`"b": 1288`, a seq number) or to the four marked
  books (`"b": "tirumanthiram:668"`, `"kural:423"`, `"naladiyar:47"`, `"thiruppugazh:355"`). The
  Tirumanthiram is the Siddhars' parent text: its yoga and siddhi tantras (3 and 8, chapters 60
  to 80 and 150 onward) hold the strongest pairs; Sivavakkiyar's attacks on ritual and caste pair
  with Tirumanthiram's தவ நிந்தை and with the Kural's chapters on ascetics and truth. Read the
  other verse before linking. At most three links per verse. A `tension` must be an incompatible
  claim on at least one defensible reading, not a shared topic.
- Record corrupt lines, doubled units and misnumbering in `source_issues`.

## Rules

- Do not edit any file except your own chapter files. Do not commit.
- When every file passes `check`, reply with only: the chapters done, new concept ids, link counts
  (within, and to each other book), how many verses you marked uncertain, and text problems.
