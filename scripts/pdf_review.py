#!/usr/bin/env python3
"""Read every mirrored PDF, grade its text layer, and write a review sheet.

A PDF's text layer can look right on screen and still decode to the wrong
characters, so each PDF is graded by how many of its words also occur in the
Unicode text for the same work.

Writes:
  data/catalog/pdf_review.csv  one row per PDF, with blank columns for reviewers
  data/pdf_text/<id>.txt       text of PDFs graded usable; pages split by form feed

Requires pypdfium2 (see requirements.txt).
"""
import csv
import json
import re
import unicodedata
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import pypdfium2

ROOT = Path(__file__).resolve().parent.parent
CATALOG_DIR = ROOT / "data" / "catalog"
PDF_TEXT_DIR = ROOT / "data" / "pdf_text"

USABLE_MATCH = 0.85
MIN_CHARS_PER_PAGE = 20
WORD = re.compile(r"[஀-௿]{3,}|[A-Za-z]{3,}")
TAMIL = re.compile(r"[஀-௿]")
NOISE = re.compile(r"[\x00-\x08\x0b\x0e-\x1f\x7f�-]")


def words(text):
    return WORD.findall(unicodedata.normalize("NFC", text).lower())


def body_of(path):
    text = (ROOT / path).read_text(encoding="utf-8")
    return text.partition("=== BODY ===")[2] or text


def read_pdf(path):
    pdf = pypdfium2.PdfDocument(str(ROOT / path))
    try:
        pages = []
        for page in pdf:
            textpage = page.get_textpage()
            pages.append(textpage.get_text_bounded().replace("\r\n", "\n"))
            textpage.close()
            page.close()
        return pages
    finally:
        pdf.close()


def grade(job):
    doc, text_paths = job
    result = {"id": doc["id"], "error": "", "pages": 0, "chars": 0, "tamil_share": 0.0,
              "noise_share": 0.0, "word_match": "", "grade": "unreadable"}
    try:
        pages = read_pdf(doc["raw_path"])
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
        return result
    text = "\f".join(pages)
    visible = re.sub(r"\s", "", text)
    pdf_words = words(text)
    result.update(pages=len(pages), chars=len(visible),
                  tamil_share=round(len(TAMIL.findall(visible)) / max(1, len(visible)), 3),
                  noise_share=round(len(NOISE.findall(visible)) / max(1, len(visible)), 3))
    if text_paths:
        vocabulary = set()
        for path in text_paths:
            vocabulary.update(words(body_of(path)))
        if pdf_words:
            result["word_match"] = round(sum(w in vocabulary for w in pdf_words) / len(pdf_words), 3)

    # Legacy Tamil fonts decode to Latin-1 symbols, so few words does not mean no text.
    if len(visible) < MIN_CHARS_PER_PAGE * max(1, len(pages)):
        result["grade"] = "no_text_layer"
    elif result["word_match"] == "":
        result["grade"] = "unverified"
    elif result["word_match"] >= USABLE_MATCH:
        result["grade"] = "usable"
        out = PDF_TEXT_DIR / (Path(doc["raw_path"]).stem + ".txt")
        out.write_text(text, encoding="utf-8")
    else:
        result["grade"] = "garbled"
    return result


def main():
    PDF_TEXT_DIR.mkdir(parents=True, exist_ok=True)
    documents = [json.loads(line) for line in
                 (CATALOG_DIR / "documents.jsonl").read_text(encoding="utf-8").splitlines()]
    rows = {}
    for line in (CATALOG_DIR / "works.jsonl").read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        rows[record["row"]] = record
    texts_by_row = {}
    for doc in documents:
        if "text_path" in doc:
            for row_id in doc["row_ids"]:
                texts_by_row.setdefault(row_id, []).append(doc["text_path"])

    # A PDF can cover several rows and a row several parts, so match against all of them.
    pdfs = [d for d in documents if d["kind"] == "pdf"]
    jobs = [(d, sorted({p for r in d["row_ids"] for p in texts_by_row.get(r, [])})) for d in pdfs]
    with ProcessPoolExecutor() as pool:
        results = {r["id"]: r for r in pool.map(grade, jobs, chunksize=8)}

    fields = ["pdf_file", "pages", "grade", "word_match", "tamil_share", "noise_share", "read_from",
              "work_no", "title", "author", "genre", "catalog_match", "row_ids", "error",
              "review_status", "review_notes"]
    with open(CATALOG_DIR / "pdf_review.csv", "w", encoding="utf-8-sig", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=fields)
        writer.writeheader()
        for doc, paths in jobs:
            result = results[doc["id"]]
            linked = [rows[r] for r in doc["row_ids"]]
            read_from = (f"data/pdf_text/{Path(doc['raw_path']).stem}.txt"
                         if result["grade"] == "usable" else " | ".join(paths))
            writer.writerow({
                "pdf_file": doc["raw_path"], "pages": result["pages"], "grade": result["grade"],
                "word_match": result["word_match"], "tamil_share": result["tamil_share"],
                "noise_share": result["noise_share"], "read_from": read_from,
                "work_no": " | ".join(dict.fromkeys(r["work_no"] for r in linked)),
                "title": " | ".join(dict.fromkeys(r["title"] for r in linked)),
                "author": " | ".join(dict.fromkeys(r["author"] for r in linked if r["author"])),
                "genre": " | ".join(dict.fromkeys(r["genre"] for r in linked if r["genre"])),
                "catalog_match": doc["catalog_match"],
                "row_ids": " ".join(str(r) for r in doc["row_ids"]),
                "error": result["error"], "review_status": "", "review_notes": ""})


if __name__ == "__main__":
    main()
