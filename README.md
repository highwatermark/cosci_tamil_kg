# Project Madurai corpus

A mirror of the [Project Madurai list of works](https://www.projectmadurai.org/pmworks.html),
prepared for text mining and knowledge graph construction. Crawled 2026-10-31; the list
was last updated by the site on 20 May 2026.

## Terms of use

The texts belong to Project Madurai and its contributors. They are not relicensed here.

- Each text says: "You are welcome to freely distribute this file, provided this header
  page is kept intact." `data/raw/` is unmodified, and `data/text/` keeps the header above
  the `=== BODY ===` marker. Keep it when you redistribute these files.
- The FAQ says works are either public domain or included "with due consent from the
  respective authors". That consent was given to Project Madurai, and some translations
  state their own copyright, such as "All rights reserved". Check those before publishing
  or redistributing them.
- Keep this repository private until those checks are done.

## Layout

| Path | Contents |
|---|---|
| `data/catalog/works.jsonl` | One record per row of the list: title, author, genre, linked files |
| `data/catalog/documents.jsonl` | One record per file: URL, hash, language hint, quality figures |
| `data/catalog/report.json` | Coverage figures and every failed URL |
| `data/catalog/rows.jsonl` | Rows as parsed from the list, including repaired links |
| `data/catalog/fetch_log.jsonl` | One record per URL requested |
| `data/text/` | Plain text for mining, one file per Unicode page |
| `data/raw/` | Unmodified HTML, PDF and images, laid out as under `/pm_etexts/` |
| `data/source/` | The list of works, sitemap, robots.txt and site info pages |
| `data/catalog/pdf_review.csv` | Review sheet for every PDF, with its grade and readable source |
| `data/pdf_text/` | Text of the PDFs graded usable; pages split by form feed |
| `kg/` | Knowledge graph nodes and edges, plus reading marks |
| `scripts/` | `crawl.py`, `extract.py`, `pdf_review.py` and `build_graph.py` |

## Coverage

| | |
|---|---|
| Rows in the list | 1,283 |
| Rows with Unicode text | 1,280 (1,268 by a link in the list, 12 inferred from the work number) |
| Files fetched | 2,719: 1,382 Unicode HTML, 1,308 PDF, 28 images, 1 TSCII |
| Text extracted | 171 million characters in 1,382 files |
| Language hints | 1,348 Tamil, 28 English, 6 mixed |

**Rows with no file found:** row 451 (work 330), row 1041 (work 890) and row 1105 (work
946). The list gives no links for them, and the likely filenames returned 404.

**Failed URLs: 112.** All are listed in `report.json` or `fetch_log.jsonl`.

- 72 were linked from the list or from inside a text: 30 images, 23 PDFs, 18 HTML pages and 1
  directory. These returned 403 or 404 from the site. Of the 41 failed HTML and PDF links,
  21 have another part of the same work under a filename such as `_01`, and 34 are linked
  directly from a row of the list.
- 36 came from the sitemap, which contains stale entries.
- 4 were filename guesses for rows with no links.

## Data notes

- **Rows and files are many-to-many.** One file can hold several titles, and one title can
  span several files. Join them through `row_ids` in `documents.jsonl`.
- **Check `catalog_match`.** `row_link` means the list links the file. `inferred` means the
  file came from the sitemap or a page link and was matched by the number in its filename,
  so treat that link as less certain. `none` means no match.
- **Work numbers are not unique** to a row, and some hold two values, such as `946_01, 946_02`.
  Use `row` as the key.
- **Six links were repaired** where the list has typos, such as `pm0798,pdf`. Repairs are
  recorded in `rows.jsonl`.
- **Text structure:** `#` marks an HTML heading, by level, and a line break marks a verse or
  `<br>` line. Sections are not always marked as headings, so some divisions appear as
  plain lines.
- **Author and genre:** 45 rows have no author, and some authors are not people, such as
  `விவிலியம்` (the Bible). `genre_path` splits the genre on its dash.
- **Most PDF text is garbled.** Old Tamil fonts make PDFs look right on screen but decode to
  the wrong characters. Of 1,308 PDFs (115,172 pages), 1,272 are graded `garbled` and 36
  `usable`. Don't mine the PDFs' text layers directly. See "Reviewing the PDFs".
- **`language_hint`** comes only from the share of Tamil characters: `ta` at 0.3 or above,
  `en` below 0.05, otherwise `mixed`. Translations often have the Tamil title in the list
  and English text in the file.
- **Known exceptions:** `pmuni0143_03` has no licence header at source, and `pmuni0278_03`
  and `pmuni0278_04` contain a few invalid bytes at source.

## Reviewing the PDFs

The PDFs are in `data/raw/pdf/`. `data/catalog/pdf_review.csv` has one row per PDF, with its
title, author, grade and blank `review_status` and `review_notes` columns.

- `read_from` gives the machine-readable text for each PDF: `data/pdf_text/` for usable PDFs,
  and otherwise the linked Unicode text in `data/text/`.
- `word_match` is the share of the PDF's words found in the linked Unicode text. A PDF is
  `usable` at 0.85 or above. Some garbled PDFs score 0.7 to 0.85 because English sections
  match while Tamil sections do not.
- The grade tests the text layer, not whether the PDF and Unicode versions are the same
  edition. One page, from `pm0001.pdf`, was compared by eye and matched.

## Knowledge graph

`kg/nodes.jsonl` and `kg/edges.jsonl` hold two layers. Use the `layer` field to tell them
apart.

- **`catalog`** covers every row: works, listed authors, genres and files. It comes from the
  list of works, not from reading the texts.
- **`marks`** is a pilot of entities and relations marked by reading the opening of four
  texts: `pmuni1090`, `pmuni0202`, `pmuni0143_01` and `pmuni0153`. Marks are not exhaustive,
  and all have status `proposed` until reviewed.

To review marks, use `kg/marks/marks_review.csv`. To add or change them, edit
`kg/marks/pilot_source.json` and rebuild. The build stops if a quote is not found exactly in
the cited text, so each mark can be traced to its source. A relation's `assertion` separates
what a text states from a `traditional_claim` it reports.

```bash
python3 -I scripts/build_graph.py
```

Entity identity is not resolved between layers yet: `AuthorString` nodes hold raw names, and
`Person` nodes exist only in the marks layer.

### Theme pilot

The graph's purpose is the contents of the books: their meanings, themes, philosophies and
nuances, and the threads between them. `kg/themes/` is the first pilot of that layer, and
[THREADS.md](kg/themes/THREADS.md) is the place to start reading.

| File | Contents |
|---|---|
| `kg/core/kural.jsonl` | All 1,330 Kural verses with chapter, section and Pope's translation |
| `kg/themes/pilot_source.json` | Hand-written concepts, verse marks and threads; edit this one |
| `kg/themes/nodes.jsonl`, `edges.jsonl` | The built theme layer |
| `kg/themes/blind_readings.json` | Readings written from the Tamil before seeing translations |
| `kg/themes/blind_grades.json` | An independent agent's grades, with where sources disagree |

- **Scope:** five Kural chapters (4, 38, 40, 98, 110), the Naladiyar's chapter on learning, and
  selected passages from the Kural, Naladiyar, Purananuru, Cilappatikaram and three commentators.
- **Basis:** each thread claim says whether it comes from the `text`, a `commentator`, or Claude's
  `interpretation`. Interpretations are proposals for a human reader.
- **Several readings per verse:** commentators can disagree without one being marked wrong.
- **Limits:** a human reader of classical Tamil has not reviewed any of this. The threads
  were chosen by Claude from known themes, not found by a systematic search of the corpus.

Rebuild with:

```bash
python3 -I scripts/parse_kural.py
```

```bash
python3 -I scripts/build_themes.py
```

### Full Thirukkural

All 133 chapters and 1,330 verses are marked. Start with [THREADS.md](kg/kural/THREADS.md).

| File | Contents |
|---|---|
| `kg/kural/nodes.jsonl`, `edges.jsonl` | Verses, chapters, concepts, commentators' readings, links and threads |
| `kg/kural/threads.json`, `thread_audit.json` | 14 threads and the audit of every link they used |
| `kg/kural/link_audit.json` | Grades for the other 443 links, with reasons and a calibration check |
| `kg/themes/kural/chNNN.json` | Marks for each chapter; edit these, following `kg/themes/SCHEMA.md` |
| `kg/themes/audit_kural.json` | Audit of a random sample, drawn from `audit_sample.json` |
| `kg/core/commentaries.jsonl` | Three commentaries aligned to each verse |
| `kg/core/verse_text_flags.jsonl` | Verses whose text should be checked |

**How far to trust it.** Separate AI reviewers did these audits. No Tamil scholar has reviewed
any of it, and the samples are small.

| Marks | Audit result | How to treat them |
|---|---|---|
| Commentators' positions | 28 of 30 accurate, 2 partial | Fairly reliable |
| Verse readings | 46 of 50 correct, 4 partial | Fairly reliable |
| Nuances | Of 43: 34 useful, 6 filler, 3 overreach | Trust attributions and discount flourishes |
| Links other than `tension`, all 398 | 298 sound, 78 weak, 18 forced, 4 wrong | Mostly usable; filter on `audit` |
| `tension` links, all 178 | 72 sound, 65 weak, 39 forced, 2 wrong | Use only those graded sound |

- Every link now has an `audit` grade. Its source is `audit_kural.json`, `thread_audit.json` or
  `link_audit.json`, checked in that order. `audit_better_type` holds a grader's suggested type,
  which has not been applied.
- To check grader drift, a fresh grader re-graded 40 earlier-audited links blind. It matched 29
  exactly and was stricter more often than more lenient, so the higher pass rate outside tensions
  is not leniency.
- The `contested` flag undercounts: 6 of 36 unflagged sample verses should have it.
- Threads were drawn from the marks, so only themes the links captured could appear.

**Verse text.** The base Thirukkural file has typos, some of which change the meaning. At 290 it
promises heaven to thieves. The Parimelazhagar file shares these errors, so Kalaignar's edition is
the independent comparison. The base text is unchanged, and `verse_text_flags.jsonl` lists 265
verses to check. That list caught 21 of 22 known errors, and later held 16 of 17 typos the link
graders found independently (the missed one is a stray space). Many flags will be harmless spelling
differences, and a difference may be a real variant.

**Graph explorer.** `viz/index.html` shows the verses, links, concepts and threads as an interactive
graph. It loads `viz/data.js`, so serve the folder rather than opening the file directly:

```bash
python3 -I -m http.server 8817 --bind 127.0.0.1 --directory viz
```

Rebuild with:

```bash
python3 -I scripts/align_commentaries.py
```

```bash
python3 -I scripts/chapter_marks.py check
```

```bash
python3 -I scripts/build_kural_graph.py
```

```bash
python3 -I scripts/export_viz.py
```

## Security

See [SECURITY.md](SECURITY.md) for the dependency review and the PDF structure check. Treat
the PDFs as untrusted files.

## Reading a text

```python
import json
from pathlib import Path

documents = {}
for line in Path("data/catalog/documents.jsonl").read_text(encoding="utf-8").splitlines():
    doc = json.loads(line)
    documents[doc["id"]] = doc

text = Path(documents["utf8__pmuni0001"]["text_path"]).read_text(encoding="utf-8")
header, _, rest = text.partition("=== BODY ===")
body, _, footer = rest.partition("=== FOOTER ===")
```

## Rebuilding

`pdf_review.py` needs the hash-pinned package in `requirements.txt`. The other scripts use
only the Python standard library. The crawler waits 0.5 seconds between
requests and skips files it already has, so it can be stopped and restarted.

```bash
python3 -I scripts/crawl.py --extras
```

```bash
python3 -I scripts/extract.py
```

## Open decision

`canonical_author()` in `scripts/extract.py` only trims whitespace for now, so
`author_canonical` is the raw author string from the list. Decide how author names should
become graph entities before building author nodes.
