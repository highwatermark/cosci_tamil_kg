#!/usr/bin/env python3
"""Mirror every file linked from the Project Madurai list of works.

Single-threaded and rate limited, because this is a volunteer-run site.
Safe to re-run: files already recorded as fetched are skipped.

Writes:
  data/source/             the list of works and the site's info pages
  data/raw/                mirrored files, laid out as under /pm_etexts/
  data/catalog/rows.jsonl  one record per row of the list of works
  data/catalog/fetch_log.jsonl  one record per URL fetched (latest wins)
"""
import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

BASE = "https://www.projectmadurai.org/"
INDEX = urllib.parse.urljoin(BASE, "pmworks.html")
INFO_PAGES = ["index.html", "index.utf8.html", "index.en.html", "faq.html",
              "volunteers.html", "contact.html", "robots.txt", "sitemap.xml"]
USER_AGENT = "pm-corpus-mirror/1.0 (non-commercial Tamil text research; python-urllib)"
MIRROR_PREFIX = "/pm_etexts/"
FOLLOW_SUFFIXES = (".html", ".htm", ".pdf", ".gif", ".jpg", ".jpeg", ".png", ".txt")

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "data" / "source"
RAW_DIR = ROOT / "data" / "raw"
CATALOG_DIR = ROOT / "data" / "catalog"
FETCH_LOG = CATALOG_DIR / "fetch_log.jsonl"


def repair_href(href):
    """Fix the typos seen in the list, such as pm0798,pdf and pm0796pdf."""
    href = href.strip()
    return re.sub(r"(?<=[0-9a-zA-Z_])[,]?pdf$", ".pdf", href) if not href.endswith(".pdf") else href


class RowParser(HTMLParser):
    """Collect the cells and links of each row in #sortabletable."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_table = False
        self.rows = []
        self.cell = None
        self.row = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "table" and attrs.get("id") == "sortabletable":
            self.in_table = True
        if not self.in_table:
            return
        if tag == "tr":
            self.row = []
        elif tag == "td" and self.row is not None:
            self.cell = {"text": [], "links": []}
            self.row.append(self.cell)
        elif tag == "a" and self.cell is not None and attrs.get("href"):
            self.cell["links"].append(attrs["href"])

    def handle_endtag(self, tag):
        if not self.in_table:
            return
        if tag == "td":
            self.cell = None
        elif tag == "tr":
            if self.row:
                self.rows.append(self.row)
            self.row = None
        elif tag == "table":
            self.in_table = False

    def handle_data(self, data):
        if self.cell is not None:
            self.cell["text"].append(data)


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.links.append(value)


def clean(parts):
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def parse_rows(html):
    parser = RowParser()
    parser.feed(html)
    rows, problems = [], []
    for position, cells in enumerate(parser.rows, 1):
        if len(cells) != 6:
            problems.append({"row": position, "problem": f"{len(cells)} cells",
                             "text": [clean(c["text"]) for c in cells]})
            continue
        row = {"row": position, "work_no": clean(cells[0]["text"]),
               "title": clean(cells[1]["text"]), "author": clean(cells[2]["text"]),
               "genre": clean(cells[3]["text"]), "pdf": [], "unicode": [], "href_repairs": []}
        for key, cell in (("pdf", cells[4]), ("unicode", cells[5])):
            for href in cell["links"]:
                fixed = repair_href(href)
                if fixed != href.strip():
                    row["href_repairs"].append({"from": href, "to": fixed})
                row[key].append(urllib.parse.urljoin(INDEX, fixed))
        rows.append(row)
    return rows, problems


def local_path(url):
    path = urllib.parse.unquote(urllib.parse.urlparse(url).path)
    if not path.startswith(MIRROR_PREFIX):
        raise ValueError(f"outside mirror prefix: {url}")
    relative = Path(path[len(MIRROR_PREFIX):])
    if ".." in relative.parts or not relative.name:
        raise ValueError(f"unsafe path: {url}")
    return RAW_DIR / relative


def download(url, retries=4):
    """Return (status, bytes). Status is None if the request never completed."""
    error = None
    for attempt in range(retries):
        if attempt:
            time.sleep(5 * 2 ** attempt)
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                body = response.read()
                expected = response.headers.get("Content-Length")
                if expected and int(expected) != len(body):
                    error = f"truncated: {len(body)} of {expected} bytes"
                    continue
                return response.status, body, None
        except urllib.error.HTTPError as exc:
            error = f"HTTP {exc.code}"
            if exc.code not in (408, 429, 500, 502, 503, 504):
                return exc.code, None, error
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as exc:
            error = str(exc)
    return None, None, error


def looks_valid(url, body):
    suffix = Path(urllib.parse.urlparse(url).path).suffix.lower()
    if suffix == ".pdf" and not body.startswith(b"%PDF"):
        return "not a PDF"
    if not body:
        return "empty"
    return None


def discover_links(url, body):
    if not url.lower().endswith((".html", ".htm")):
        return []
    parser = LinkParser()
    try:
        parser.feed(body.decode("utf-8", errors="replace"))
    except Exception:
        return []
    host = urllib.parse.urlparse(BASE).netloc
    found = []
    for link in parser.links:
        target = urllib.parse.urldefrag(urllib.parse.urljoin(url, repair_href(link))).url
        parts = urllib.parse.urlparse(target)
        if (parts.netloc == host and parts.path.startswith(MIRROR_PREFIX)
                and parts.path.lower().endswith(FOLLOW_SUFFIXES)):
            found.append(parts._replace(scheme="https", query="").geturl())
    return found


def load_done():
    done = {}
    if FETCH_LOG.exists():
        for line in FETCH_LOG.read_text(encoding="utf-8").splitlines():
            record = json.loads(line)
            done[record["url"]] = record
    return done


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--delay", type=float, default=0.5, help="seconds between requests")
    ap.add_argument("--limit", type=int, help="stop after this many new fetches")
    ap.add_argument("--skip-pdf", action="store_true")
    ap.add_argument("--retry-failed", action="store_true")
    ap.add_argument("--extras", action="store_true",
                    help="also fetch sitemap files and guessed names for rows with no links")
    args = ap.parse_args()

    for directory in (SOURCE_DIR, RAW_DIR, CATALOG_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    status, body, error = download(INDEX)
    if body is None:
        sys.exit(f"could not fetch the list of works: {error}")
    (SOURCE_DIR / "pmworks.html").write_bytes(body)
    for page in INFO_PAGES:
        _, page_body, page_error = download(urllib.parse.urljoin(BASE, page))
        if page_body is not None:
            (SOURCE_DIR / page).write_bytes(page_body)
        else:
            print(f"info page failed: {page}: {page_error}", file=sys.stderr)
        time.sleep(args.delay)

    rows, problems = parse_rows(body.decode("utf-8"))
    with open(CATALOG_DIR / "rows.jsonl", "w", encoding="utf-8") as out:
        for row in rows:
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
    (CATALOG_DIR / "row_problems.json").write_text(
        json.dumps(problems, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"rows={len(rows)} malformed_rows={len(problems)}", flush=True)

    queue, seen = [], set()
    def enqueue(url, referrer):
        if url in seen:
            return
        seen.add(url)
        queue.append((url, referrer))

    # Fetch text before PDFs, so an interrupted run still has the minable part.
    for row in rows:
        for url in row["unicode"]:
            enqueue(url, INDEX)
    if not args.skip_pdf:
        for row in rows:
            for url in row["pdf"]:
                enqueue(url, INDEX)

    if args.extras:
        # The sitemap lists files the table omits, and some rows have no links.
        sitemap = (SOURCE_DIR / "sitemap.xml").read_text(encoding="utf-8", errors="replace")
        for loc in re.findall(r"<loc>\s*([^<\s]+)", sitemap):
            if MIRROR_PREFIX in loc and not (args.skip_pdf and loc.lower().endswith(".pdf")):
                enqueue(loc.replace("http://", "https://"), "sitemap")
        for row in rows:
            if row["unicode"] or row["pdf"]:
                continue
            for number in re.findall(r"\d+(?:_\d+)?", row["work_no"]):
                head, _, tail = number.partition("_")
                stem = head.zfill(4) + (f"_{tail}" if tail else "")
                enqueue(urllib.parse.urljoin(BASE, f"pm_etexts/utf8/pmuni{stem}.html"),
                        f"guess:row{row['row']}")
                enqueue(urllib.parse.urljoin(BASE, f"pm_etexts/pdf/pm{stem}.pdf"),
                        f"guess:row{row['row']}")

    done = load_done()
    fetched = 0
    position = 0
    with open(FETCH_LOG, "a", encoding="utf-8") as log:
        while position < len(queue):
            url, referrer = queue[position]
            position += 1
            previous = done.get(url)
            if previous and previous["ok"] and previous.get("path") and not (ROOT / previous["path"]).exists():
                previous = None  # recorded but not on disk (e.g. untracked in git): fetch it again
            if previous and (previous["ok"] or not args.retry_failed):
                if previous["ok"] and previous.get("path"):
                    for link in discover_links(url, (ROOT / previous["path"]).read_bytes()):
                        if not (args.skip_pdf and link.lower().endswith(".pdf")):
                            enqueue(link, url)
                continue
            if args.limit is not None and fetched >= args.limit:
                break

            try:
                target = local_path(url)
            except ValueError as exc:
                record = {"url": url, "ok": False, "error": str(exc), "referrer": referrer}
                log.write(json.dumps(record, ensure_ascii=False) + "\n")
                log.flush()
                continue

            status, data, error = download(url)
            error = error or (looks_valid(url, data) if data is not None else "no body")
            record = {"url": url, "referrer": referrer, "status": status,
                      "ok": error is None, "error": error,
                      "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
            if error is None:
                target.parent.mkdir(parents=True, exist_ok=True)
                part = target.with_name(target.name + ".part")
                part.write_bytes(data)
                part.replace(target)
                record.update(path=target.relative_to(ROOT).as_posix(), bytes=len(data),
                              sha256=hashlib.sha256(data).hexdigest())
                for link in discover_links(url, data):
                    if not (args.skip_pdf and link.lower().endswith(".pdf")):
                        enqueue(link, url)
            log.write(json.dumps(record, ensure_ascii=False) + "\n")
            log.flush()
            done[url] = record
            fetched += 1
            if fetched % 50 == 0 or error:
                print(f"{fetched} fetched, {position}/{len(queue)} queued"
                      + (f" | FAILED {url}: {error}" if error else ""), flush=True)
            time.sleep(args.delay)

    ok = sum(1 for r in done.values() if r["ok"])
    print(f"finished: known={len(queue)} ok={ok} failed={len(done) - ok} "
          f"new={fetched} bytes={sum(r.get('bytes', 0) for r in done.values())}", flush=True)


if __name__ == "__main__":
    main()
