# Brief: ingesting one book into the knowledge graph

The repository at /Users/harilakshmanan/Cursor/cosci_knowledge_graph mirrors Project Madurai's Tamil
texts and builds a knowledge graph of their meanings, themes and threads. The Thirukkural is done.
Your job is the first stage for one more book: turn its corpus files into a clean, numbered list of
units (verses or stanzas), with every translation and commentary in the corpus aligned to each unit.
Reading, marking and linking come later, from your output.

## Where things are

- `data/catalog/works.jsonl`: one row per work in Project Madurai's list. `text_ids` name the files,
  so `utf8__pmuni0016` is `data/text/pmuni0016.txt`. Search titles and authors to find every file of
  your book, including translations and commentaries.
- `data/text/*.txt`: plain text. Each file has a licence header, then `=== BODY ===`, the text, and
  `=== FOOTER ===`. Headings start with `#`.
- Models to follow: `scripts/parse_kural.py` and `scripts/parse_naladiyar.py` (the second aligns a
  translation and two commentaries by letter trigrams, which tolerates spelling differences between
  editions). `kg/core/kural.jsonl` and `kg/core/naladiyar.jsonl` show the output shape.

## What to produce

1. `scripts/parse_<book>.py`: standard library only, run as `python3 -I scripts/parse_<book>.py`,
   reading only `data/text/`. Install nothing.
2. `kg/core/<book>.jsonl`: one record per unit, in canonical order, with at least
   - `id`: stable and unique, such as `tirumanthiram:1234` or `prabandham:3792`
   - `number` and the traditional numbering where one exists (the 4,000 Prabandham pasurams, the
     Thirumurai's book-pathigam-verse, Tirumanthiram's tantra and verse)
   - the place in the work: book, part, chapter, pathigam, poet, place or deity, as the work has them
   - `tamil`: the lines of the unit
   - one field per translation or commentary present in the corpus, aligned to the unit, or null
3. A report at the output path you were given (Markdown) covering:
   - the files used, and any you rejected and why
   - unit counts against the traditional count (say what is missing or doubled)
   - how many units each translation or commentary was aligned to, with five spot checks you read
   - copyright: for each translator or commentator, the date and whether they are likely still in
     copyright. Modern ones (for example Kausalya Hart, Avvai Duraisamy Pillai, Sundara Shanmuganar,
     Kalaignar) stay in the record but must be marked `"rights": "modern"` in a sidecar map in the
     report, so later stages quote at most a few words
   - text problems: corrupted lines, misnumbered units, headers inside the text
   - a suggested unit for later marking. For long devotional collections, say whether marking should
     be per verse or per hymn (pathigam or decade), and why.

## Rules

- Do not edit any existing file. Create only the two files above and your report.
- Do not commit, push or switch branches.
- Read Tamil carefully: verse numbers in these files are sometimes misprinted or restart per part.
  Validate the count and the order, and print what fails rather than hiding it.
- If a book's files are too broken to parse in full, parse what is sound and say exactly what is
  left in the report.
- Reply at the end with only: the output paths, the unit count, and the alignment counts.
