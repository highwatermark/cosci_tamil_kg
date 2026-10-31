# Dependency and file review

Reviewed 2026-10-31. Review any new package the same way before installing it.

## Review steps

1. Query [OSV](https://osv.dev) and PyPI for advisories, without installing anything.
2. Download the wheel and check its SHA-256 against PyPI.
3. Inspect the wheel for `.pth` files, unsafe paths, bundled binaries, and network or
   subprocess code.
4. Install with `--require-hashes --only-binary :all:`.

## Dependencies

| Package | Version | OSV advisories | Notes |
|---|---|---|---|
| `pypdfium2` | 5.14.0 | 0 | Only runtime dependency. Bundles PDFium 156.0.8076.0. Hash pinned in `requirements.txt`. |
| `pip` | 26.2.2 | 0 | Used to install the package above. |

`crawl.py`, `extract.py` and `build_graph.py` use only the Python standard library.

**Limits of this review:**

- OSV results for `pypdfium2` may not cover vulnerabilities in the PDFium binary it bundles.
  PDFium is memory-unsafe C++, so keep the package current.
- The wheel inspection was a pattern search, not a code audit, and the PDFium binary was not
  analysed.
- The Python interpreter and Homebrew tools were not reviewed.

## Packages used before review

These were installed in a temporary environment before this review was requested, and were
then removed:

| Package | Version | Finding |
|---|---|---|
| `pypdf` | 5.1.0 | Many advisories, mostly hangs or memory exhaustion from crafted PDFs, some rated HIGH. It read metadata and sample text from about 60 PDFs. |
| `pypdfium2` | 4.30.0 | No OSV advisories, but bundled PDFium 126 from mid-2024. It read all 1,308 PDFs with no sandbox. |
| `pip` | 25.3 | 5 advisories. It installed the packages above and, before being upgraded, `pypdfium2` 5.14.0 from a hash-verified local wheel. |

All 1,308 PDFs were read without errors or hangs, and nothing suggests exploitation. That
does not prove none occurred. The scan's results did not change when it was re-run on
`pypdfium2` 5.14.0, apart from one word-match figure.

## PDF contents

The PDFs come from a third-party site, so treat them as untrusted. A search of the PDF
structure outside compressed streams found:

| Feature | Result |
|---|---|
| JavaScript, launch actions, embedded files, form submission, rich media, XFA | None |
| Object streams, which could hide the features above | None |
| `/OpenAction` | `pm0091.pdf` only: opens at a page view |
| `/URI` | `pm0091.pdf` only: a `mailto:` link |
| `/AcroForm` | `pm0300.pdf` only: no fields |
| `/Encrypt` | 18 files, which opened without a password |

This is a structural search, not a malware scan.
