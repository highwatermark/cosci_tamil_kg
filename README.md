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
| `scripts/` | `crawl.py` and `extract.py` |

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
- **PDFs have no extracted text.** Use `data/text/` for mining. Every row with a file has
  Unicode text, so the PDFs are for reference.
- **`language_hint`** comes only from the share of Tamil characters: `ta` at 0.3 or above,
  `en` below 0.05, otherwise `mixed`. Translations often have the Tamil title in the list
  and English text in the file.
- **Known exceptions:** `pmuni0143_03` has no licence header at source, and `pmuni0278_03`
  and `pmuni0278_04` contain a few invalid bytes at source.

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

The scripts use only the Python standard library. The crawler waits 0.5 seconds between
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
