#!/usr/bin/env python3
"""Turn mirrored Unicode HTML into plain text and a joinable catalog.

Writes:
  data/text/<id>.txt           header + body + footer, split by marker lines
  data/catalog/documents.jsonl one record per file (text or PDF)
  data/catalog/works.jsonl     one record per row of the list of works
  data/catalog/report.json     coverage and quality figures
"""
import json
import re
import unicodedata
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
TEXT_DIR = ROOT / "data" / "text"
CATALOG_DIR = ROOT / "data" / "catalog"

BODY_MARKER = "=== BODY ==="
FOOTER_MARKER = "=== FOOTER ==="
HEADER_END = re.compile(r"kept\s+intact", re.I)
FOOTER_PATTERN = re.compile(
    r"This\s+page\s+was\s+first\s+put\s+up|Please\s+send\s+your\s+comments", re.I)
BLOCK_TAGS = {"p", "div", "center", "ul", "ol", "li", "table", "tr", "blockquote", "hr",
              "h1", "h2", "h3", "h4", "h5", "h6", "pre"}
TAMIL = re.compile(r"[஀-௿]")


def canonical_author(name):
    """Map a raw author string from the list of works to a graph entity name."""
    # TODO: decide how authors become graph entities. See README, "Open decision".
    return name.strip()


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0
        self.pre = 0
        self.heading = None

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "title"):
            self.skip += 1
        elif tag == "br":
            self.out.append("\n")
        elif tag in BLOCK_TAGS:
            self.out.append("\n\n")
            if tag == "pre":
                self.pre += 1
            if len(tag) == 2 and tag[0] == "h" and tag[1].isdigit():
                self.out.append("#" * int(tag[1]) + " ")
                self.heading = tag

    def handle_endtag(self, tag):
        if tag in ("script", "style", "title"):
            self.skip = max(0, self.skip - 1)
        elif tag in BLOCK_TAGS:
            self.out.append("\n\n")
            if tag == "pre":
                self.pre = max(0, self.pre - 1)
            if tag == self.heading:
                self.heading = None

    def handle_data(self, data):
        if self.skip:
            return
        self.out.append(data if self.pre else re.sub(r"\s+", " ", data))


def to_text(html):
    parser = TextExtractor()
    parser.feed(html)
    parser.close()
    text = unicodedata.normalize("NFC", "".join(parser.out))
    text = text.replace(" ", " ").replace("﻿", "").replace("​", "")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    lines = [line for line in lines if line not in ("#", "##", "###", "####", "#####", "######")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def split_sections(html):
    """Return (header_html, body_html, footer_html). Header is empty if not found."""
    found = HEADER_END.search(html)
    header_end = 0
    if found:
        marker = found.start()
        rule = re.compile(r"<hr\b[^>]*>", re.I).search(html, marker, marker + 800)
        if rule:
            header_end = rule.end()
        else:
            line_end = html.find("<", marker)
            header_end = line_end if line_end >= 0 else marker
    footer_match = None
    for footer_match in FOOTER_PATTERN.finditer(html, header_end):
        break
    footer_start = len(html)
    if footer_match:
        rules = [m.start() for m in re.finditer(r"<hr\b", html[header_end:footer_match.start()], re.I)]
        footer_start = header_end + rules[-1] if rules else footer_match.start()
        # A rule far above the footer line is a section break, not the footer's.
        if footer_match.start() - footer_start > 400:
            footer_start = footer_match.start()
    return html[:header_end], html[header_end:footer_start], html[footer_start:]


def decode(raw):
    try:
        return raw.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="replace"), "utf-8-lossy"


def doc_id(path):
    return path.relative_to(RAW_DIR).with_suffix("").as_posix().replace("/", "__")


def work_number(stem):
    match = re.search(r"(?:pmuni|pmtsc|pm)0*(\d+)", stem)
    return match.group(1) if match else None


def language_hint(ratio):
    """Tamil characters as a share of the body, which includes spaces and digits."""
    return "ta" if ratio >= 0.3 else "en" if ratio < 0.05 else "mixed"


def split_genre(genre):
    return [part.strip() for part in re.split(r"\s+[-–—]\s+", genre) if part.strip()]


def main():
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(line) for line in
            (CATALOG_DIR / "rows.jsonl").read_text(encoding="utf-8").splitlines()]
    fetches = {}
    for line in (CATALOG_DIR / "fetch_log.jsonl").read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        fetches[record["url"]] = record

    rows_by_url = defaultdict(list)
    rows_by_number = defaultdict(list)
    for row in rows:
        for url in row["unicode"] + row["pdf"]:
            rows_by_url[url].append(row)
        # "946_01, 946_02" is work 946 twice; the _NN part is not a work number.
        for number in set(re.findall(r"(?<![_\d])\d+", row["work_no"])):
            rows_by_number[number.lstrip("0")].append(row)

    documents = []
    for url, fetch in sorted(fetches.items()):
        if not fetch["ok"]:
            continue
        path = ROOT / fetch["path"]
        linked = rows_by_url.get(url, [])
        match = "row_link" if linked else None
        if not linked:
            inferred = {r["row"]: r for r in rows_by_number.get(work_number(path.stem) or "", [])}
            linked = list(inferred.values())
            match = "inferred" if linked else "none"
        relative = path.relative_to(RAW_DIR)
        kind = {"utf8": "unicode_html", "pdf": "pdf", "tscii": "tscii_html"}.get(
            relative.parts[0], relative.parts[0])
        doc = {"id": doc_id(path), "kind": kind, "url": url, "raw_path": fetch["path"],
               "bytes": fetch["bytes"], "sha256": fetch["sha256"], "fetched_at": fetch["fetched_at"],
               "discovered_via": fetch["referrer"], "catalog_match": match,
               "row_ids": [r["row"] for r in linked]}
        is_html = path.suffix.lower() in (".html", ".htm")
        if path.suffix.lower() in (".gif", ".jpg", ".jpeg", ".png"):
            kind = doc["kind"] = "image"
        if kind == "unicode_html" and is_html:
            html, encoding = decode(path.read_bytes())
            header, body, footer = split_sections(html)
            body_text = to_text(body)
            header_text = to_text(header)
            footer_text = to_text(footer)
            ratio = round(len(TAMIL.findall(body_text)) / max(1, len(body_text)), 3)
            text_path = TEXT_DIR / (path.stem + ".txt")
            text_path.write_text(f"{header_text}\n\n{BODY_MARKER}\n\n{body_text}\n\n"
                                 f"{FOOTER_MARKER}\n\n{footer_text}\n", encoding="utf-8")
            doc.update(text_path=text_path.relative_to(ROOT).as_posix(), encoding=encoding,
                       has_licence_header=bool(HEADER_END.search(header_text)),
                       language_hint=language_hint(ratio),
                       body_chars=len(body_text),
                       tamil_ratio=ratio,
                       heading_lines=sum(1 for l in body_text.split("\n") if l.startswith("#")),
                       replacement_chars=body_text.count("�"))
        documents.append(doc)

    with open(CATALOG_DIR / "documents.jsonl", "w", encoding="utf-8") as out:
        for doc in documents:
            out.write(json.dumps(doc, ensure_ascii=False) + "\n")

    docs_by_row = defaultdict(list)
    for doc in documents:
        for row_id in doc["row_ids"]:
            docs_by_row[row_id].append(doc)
    with open(CATALOG_DIR / "works.jsonl", "w", encoding="utf-8") as out:
        for row in rows:
            linked = docs_by_row[row["row"]]
            record = {key: row[key] for key in ("row", "work_no", "title", "author", "genre")}
            record.update(author_canonical=canonical_author(row["author"]),
                          genre_path=split_genre(row["genre"]),
                          text_ids=[d["id"] for d in linked if d["kind"] == "unicode_html"
                                    and d["catalog_match"] == "row_link"],
                          pdf_ids=[d["id"] for d in linked if d["kind"] == "pdf"
                                   and d["catalog_match"] == "row_link"],
                          inferred_ids=[d["id"] for d in linked if d["catalog_match"] == "inferred"])
            out.write(json.dumps(record, ensure_ascii=False) + "\n")

    texts = [d for d in documents if "text_path" in d]
    failures = [f for f in fetches.values() if not f["ok"]]
    def source(fetch):
        referrer = fetch.get("referrer", "")
        return "guess" if referrer.startswith("guess") else "sitemap" if referrer == "sitemap" else "list_or_page"
    without_any = [r for r in rows if not docs_by_row[r["row"]]]
    without_text = [r for r in rows
                    if not any(d["kind"] == "unicode_html" for d in docs_by_row[r["row"]])]
    report = {
        "rows": len(rows),
        "files_ok": len(documents),
        "files_by_kind": Counter(d["kind"] for d in documents),
        "bytes_by_kind": {k: sum(d["bytes"] for d in documents if d["kind"] == k)
                          for k in {d["kind"] for d in documents}},
        "catalog_match": Counter(d["catalog_match"] for d in documents),
        "failures_by_source": Counter(source(f) for f in failures),
        "failures_list_or_page": [{"url": f["url"], "error": f["error"]} for f in failures
                                  if source(f) == "list_or_page"],
        "failures_sitemap": [{"url": f["url"], "error": f["error"]} for f in failures
                             if source(f) == "sitemap"],
        "texts_by_language_hint": Counter(d["language_hint"] for d in texts),
        "text_body_chars": sum(d["body_chars"] for d in texts),
        "texts_missing_licence_header": [d["id"] for d in texts if not d["has_licence_header"]],
        "texts_lossy_encoding": [d["id"] for d in texts if d["encoding"] != "utf-8"],
        "texts_low_tamil_ratio": [{"id": d["id"], "ratio": d["tamil_ratio"]} for d in texts
                                  if d["tamil_ratio"] < 0.3],
        "texts_short_body": [{"id": d["id"], "chars": d["body_chars"]} for d in texts
                             if d["body_chars"] < 500],
        "rows_without_any_file": [{"row": r["row"], "work_no": r["work_no"], "title": r["title"]}
                                  for r in without_any],
        "rows_without_text": [{"row": r["row"], "work_no": r["work_no"], "title": r["title"]}
                              for r in without_text],
    }
    (CATALOG_DIR / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {k: v if not isinstance(v, list) else len(v) for k, v in report.items()}
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
