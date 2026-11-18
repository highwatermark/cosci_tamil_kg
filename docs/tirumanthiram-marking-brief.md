# Brief: marking Tirumanthiram chapters

The repository at /Users/harilakshmanan/Cursor/cosci_knowledge_graph builds a knowledge graph of the
meanings, themes and threads of Tamil literature. The Thirukkural and the Naladiyar are marked and
linked. You are marking chapters of the Tirumanthiram of Tirumular, the tenth Thirumurai: about
3,000 four-line verses in nine tantras on ethics, the body, yoga, the Saiva Siddhanta categories, and
grace.

## Read first

- `kg/themes/SCHEMA.md`: the marking rules. Follow them exactly, with the changes below.
- `kg/themes/kural/ch038.json` and `kg/themes/naladiyar/ch014.json`: worked examples of depth and style.
- `kg/themes/concepts.json`: the shared concept list, which already holds the Tirumanthiram pilot concepts (yogam, gnaanam, sivam, thiruvarul, malam, vindhu, naadham, maayai, thaththuvam, guru, vazhipaadu and others). Reuse these ids; add a concept only when none
  fits, and name what the text names (பதி, பசு, பாசம், குண்டலினி, நாடி and the like are fair
  additions if the verses use them).

## Commands (from the repository root)

- Your chapters' verses: `python3 -I scripts/book_marks.py tirumanthiram show 12 13`
- Validate your files: `python3 -I scripts/book_marks.py tirumanthiram check 12 13`
- Kural or Naladiyar verses in full: `python3 -I scripts/link_pass.py verse 1061` (Kural) and
  `python3 -I scripts/naladiyar_marks.py show 14` (a Naladiyar chapter)
- An index of every Kural and Naladiyar verse, one line each with concepts and a reading:
  `/private/tmp/claude-501/-Users-harilakshmanan-Cursor-cosci-knowledge-graph/56dc2695-7ba3-4110-8a35-77dd53b3fdc5/scratchpad/books_index.txt`

## Changes from the Kural schema

- Files go in `kg/themes/tirumanthiram/chNNN.json`. Chapter numbers are the tool's running numbers
  (1 to 224), shown by `show`. Verse keys are the edition's verse numbers.
- **There is no commentary or translation in the corpus.** Readings rest on the Tamil alone, so there
  are no `positions` and no `contested` marks. Instead:
  - Mark `uncertain` whenever the sense depends on a technical term of yoga, mantra or Siddhanta
    whose meaning you can't fix from the verse, on a symbolic reading (the sun and moon, the
    serpent, the lotus, numbers), or on an obscure or corrupt word. In the yogic tantras that will
    be many verses; that is honest, not a failure.
  - In `nuance`, say which words carry the meaning and how they are traditionally taken, as
    tradition and not as fact, and say when a plain and a symbolic reading both stand.
  - Don't invent precision. A short, true reading beats a full, confident one.
- `links` may point within the Tirumanthiram (`"b": 1823`), to the Kural (`"b": "kural:1061"`) or to
  the Naladiyar (`"b": "naladiyar:42"`). Tirumanthiram's first tantra echoes the Kural's ethics
  closely (killing, meat-eating, wealth, learning, giving); look there for strong pairs, and read the
  other verse before linking. At most three links per verse. Where Tirumular takes a position the
  Kural or Naladiyar doesn't (on the body as temple, against the Naladiyar's contempt for the body),
  a `tension` is worth recording, tested as SCHEMA.md says.
- Record corrupt lines and variants that change the sense in `source_issues`.

## Rules

- Do not edit any file except your own chapter files. Do not commit.
- When every file passes `check`, reply with only: the chapters done, new concept ids, link counts
  (within, to the Kural, to the Naladiyar), how many verses you marked uncertain, and text problems.
