#!/usr/bin/env python3
"""Assemble public/: every page of the project as one static site, free of claude.ai.

    python3 -I scripts/build_publish.py

public/ keeps the repository's own relative layout, so links between the pages work unchanged:

    public/index.html                      the landing page: the current version, every earlier one, the tools
    public/site/nilai/v4/                  Nilai v4, walks through the graph (index.html, img/, video/)
    public/site/nilai/index.html           Nilai v3, the 500-year reel (with the assets/web and assets/video it uses)
    public/site/nilai/v2/                  Nilai v2, the first reel
    public/site/nilai.html                 Nilai v1, the bilingual file over the four-book graph
    public/site/unarvu.html                Unarvu, the companion page on consciousness and AGI
    public/viz/                            the Tamil Corpus Atlas and its data shards
    public/research-atlas/dist/            the Tamil Research Atlas and its evidence files
    public/docs/report/index.html          the methods report

Only files a page references are copied (no raw source images, no full-size cut-outs). Links to the
claude.ai artifacts are rewritten to the local copies. Each page gets a small "all versions" link back to
the landing page. Upload the folder as it is to any static host (GitHub Pages, Netlify, Cloudflare Pages,
an S3 bucket); it needs no server code. public/ is built output and is not committed.
"""
import html
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public"
MARK = OUT / ".built-by-build_publish"

# claude.ai artifacts the older pages link to, and the local page each one is
ARTIFACTS = {
    "https://claude.ai/artifact/8ypxS56cp7tjru16nV3d3K": "viz/index.html",
    "https://claude.ai/artifact/SF4gpiktxmJP8XfcLSbuSj": "site/nilai.html",
    "https://claude.ai/artifact/KNtiyE7ewKsmAXA79uGSuA": "site/unarvu.html",
    "https://claude.ai/artifact/CZhnPbPZgZMahGp1VRrwUp": "docs/report/index.html",
    "https://claude.ai/artifact/2sT4juBWLpoKxEF4C2FQ1x": "site/nilai/v4/index.html",
}

# the artifact copies of Nilai v1 and Unarvu are fragments (the host supplied the skeleton); give them one
SKELETON = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">%s</head><body>%s</body></html>')

FAIL = []


def fail(msg):
    FAIL.append(msg)


def git_date(*paths):
    out = subprocess.run(["git", "log", "-1", "--format=%ad", "--date=short", "--", *paths],
                         cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return out or "uncommitted"


def copy(rel, dst_rel=None):
    src = ROOT / rel
    if not src.is_file():
        fail("missing %s" % rel)
        return
    dst = OUT / (dst_rel or rel)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def refs(text, prefix):
    """Every relative path starting with prefix that a page names (src, href, url(), JS strings)."""
    return sorted(set(re.findall(r"(?<![\w/.])(%s[A-Za-z0-9_./%%-]+?\.(?:webp|png|jpe?g|mp4|webm|js|json|css|svg|zip|pdf|txt|md|jsonl))"
                                 % re.escape(prefix), text)))


def versions_pill(depth):
    home = "../" * depth + "index.html"
    return ('<a href="%s" style="position:fixed;left:10px;bottom:12px;z-index:2147483000;font:600 11px/1 -apple-system,'
            'BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif;letter-spacing:.04em;color:#211e1a;background:rgba(239,235,228,.9);'
            'border:1px solid rgba(77,70,61,.45);border-radius:999px;padding:7px 11px;text-decoration:none" '
            'aria-label="Nilai: all versions and tools">நிலை · all versions</a>' % home)


def write_page(text, dst_rel, pill=True):
    """Rewrite artifact links to local relative ones, add the versions link, write the page."""
    here = (OUT / dst_rel).parent
    for url, local in ARTIFACTS.items():
        rel = os.path.relpath(OUT / local, here)
        text = text.replace(url, rel)
    if "claude.ai/artifact" in text:
        fail("%s still links to a claude.ai artifact: %s" % (dst_rel, sorted(set(re.findall(r"https://claude\.ai/artifact/\w+", text)))))
    if pill:
        depth = len(Path(dst_rel).parts) - 1
        text = re.sub(r"(?i)</body>", versions_pill(depth) + "</body>", text, count=1) if re.search(r"(?i)</body>", text) \
            else text + versions_pill(depth)
    dst = OUT / dst_rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")


def fragment_to_page(rel):
    """An artifact fragment (head tags then body, no skeleton) made a whole document."""
    frag = (ROOT / rel).read_text(encoding="utf-8")
    # the head is the run of <meta>/<title>/<link>/<style> tags at the top; everything after the first other tag is the body
    head_end = 0
    for t in re.finditer(r"(?is)\s*(<meta[^>]*>|<title>.*?</title>|<link[^>]*>|<style[^>]*>.*?</style>)", frag):
        if t.start() != head_end:
            break
        head_end = t.end()
    return SKELETON % (frag[:head_end], frag[head_end:])


def main():
    if OUT.exists():
        if not MARK.exists():
            sys.exit("public/ exists but was not made by this script; move it aside first")
        shutil.rmtree(OUT)
    OUT.mkdir()
    MARK.write_text("public/ is rebuilt from the repository by scripts/build_publish.py; edits here are lost.\n")
    (OUT / ".nojekyll").write_text("")

    # Nilai v4
    v4 = (ROOT / "site/nilai/v4/index.html").read_text(encoding="utf-8")
    for r in refs(v4, "img/") + refs(v4, "video/"):
        copy("site/nilai/v4/" + r)
    write_page(v4, "site/nilai/v4/index.html")

    # Nilai v3: the reel, with only the stills and clips it names
    v3 = (ROOT / "site/nilai/index.html").read_text(encoding="utf-8")
    for r in refs(v3, "assets/"):
        copy("site/nilai/" + r)
    write_page(v3, "site/nilai/index.html")

    # Nilai v2 and its archive copy
    for name in ("index.html", "archive.html"):
        t = (ROOT / "site/nilai/v2" / name).read_text(encoding="utf-8")
        for r in refs(t, "build/") + refs(t, "assets/"):
            copy("site/nilai/v2/" + r)
        write_page(t, "site/nilai/v2/" + name)

    # Nilai v1 and Unarvu: artifact fragments made whole pages
    write_page(fragment_to_page("site/nilai.html"), "site/nilai.html")
    write_page(fragment_to_page("site/unarvu.html"), "site/unarvu.html")

    # the Tamil Corpus Atlas
    atlas = (ROOT / "viz/index.html").read_text(encoding="utf-8")
    for f in sorted((ROOT / "viz").glob("data_*.js")):
        copy("viz/" + f.name)
    write_page(atlas, "viz/index.html")

    # the Tamil Research Atlas and its evidence
    ra = ROOT / "research-atlas/dist"
    for f in sorted(ra.rglob("*")):
        if f.is_file() and f.name != "index.html":
            copy(str(f.relative_to(ROOT)))
    write_page((ra / "index.html").read_text(encoding="utf-8"), "research-atlas/dist/index.html")

    # the methods report
    write_page((ROOT / "docs/report/index.html").read_text(encoding="utf-8"), "docs/report/index.html")

    landing()

    # every local link on every page resolves inside public/
    for page in OUT.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        bm = re.search(r"""<base\s+href=["']([^"']*)""", text)
        base = (page.parent / bm.group(1)) if bm else page.parent
        for m in re.finditer(r"""(?<![\w-])(?:href|src)=["']([^"'#?]+)""", text):
            u = m.group(1)
            if re.match(r"(?i)^(https?:|mailto:|data:|javascript:|blob:)|[$'+{]", u) or not u.strip():
                continue
            if not (base / u).resolve().exists():
                fail("%s links to %s, which is not in public/" % (page.relative_to(OUT), u))

    if FAIL:
        print("PUBLISH FAILED:")
        for m in FAIL:
            print("  -", m)
        sys.exit(1)
    size = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    n = sum(1 for f in OUT.rglob("*") if f.is_file())
    print("wrote public/: %d files, %.1f MB" % (n, size / 1e6))


def landing():
    E = html.escape
    current = {
        "href": "site/nilai/v4/index.html", "ta": "நிலை", "name": "Nilai v4", "tag": "current",
        "title": "Walks through the graph",
        "ta_title": "வரைபடத்தின் ஊடே நடைகள்",
        "date": git_date("site/nilai/v4/index.html"),
        "body": "Thirteen walks of three verses and two graded links each, carried to an imagined 2526 and asked again. "
                "A full-screen prologue and epilogue, the Tamil verses throughout, and the page's own text in English or Tamil.",
        "img": "site/nilai/v4/img/V4-balance-king.webp",
    }
    earlier = [
        {"href": "site/nilai/index.html", "name": "Nilai v3", "title": "The 500-year reel",
         "date": git_date("site/nilai/index.html"),
         "body": "A scroll reel of marble and bronze objects that turn into their future forms, framed as a retrospective from 2526."},
        {"href": "site/nilai/v2/index.html", "name": "Nilai v2", "title": "The first reel",
         "date": git_date("site/nilai/v2/index.html"),
         "body": "The first animated reel put in front of the Nilai file: objects, questions and the four-book graph."},
        {"href": "site/nilai.html", "name": "Nilai v1", "title": "The working file",
         "date": git_date("site/nilai.html"),
         "body": "The bilingual page the reels grew out of: a headline, four questions for the age of AI, and an appendix "
                 "built from the four-book graph (Kural, Naladiyar, Tirumanthiram, Thiruppugazh)."},
        {"href": "site/unarvu.html", "name": "Unarvu · உணர்வு", "title": "Consciousness and AGI",
         "date": git_date("site/unarvu.html"),
         "body": "Nilai's companion page: what the Siddhar and devotional verses say about awareness, set beside today's questions about machine minds."},
    ]
    tools = [
        {"href": "viz/index.html", "name": "Tamil Corpus Atlas", "ta": "தமிழ்த் தொகுப்பு அட்லஸ்",
         "body": "The whole graph to explore: forty books, every verse, every graded link, the shared concepts and the bridges between groups of books."},
        {"href": "research-atlas/dist/index.html", "name": "Tamil Research Atlas", "ta": "ஆய்வு அட்லஸ்",
         "body": "The workbench behind the science parallels: blinded Siddhar-and-science comparisons with their controls, sources and a corpus census."},
        {"href": "docs/report/index.html", "name": "How the graph was built", "ta": "முறையியல்",
         "body": "The methods report: how the books were marked, how every link was graded blind, and what the grades and controls show."},
    ]

    def card(v, big=False):
        return ('<a class="v%s" href="%s"><span class="meta">%s%s</span><span class="nm">%s</span><span class="tt">%s</span>'
                '<span class="bd">%s</span></a>') % (
            " big" if big else "", E(v["href"]), E(v.get("date", "")), (" · " + E(v["tag"])) if v.get("tag") else "",
            E(v["name"]), E(v["title"]), E(v["body"]))

    tool_cards = "".join('<a class="t" href="%s"><span class="nm">%s</span><span class="ta" lang="ta">%s</span><span class="bd">%s</span></a>'
                         % (E(t["href"]), E(t["name"]), E(t["ta"]), E(t["body"])) for t in tools)
    page = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nilai · நிலை</title>
<meta name="description" content="Nilai: what two thousand years of Tamil poetry asks of the future, read from a knowledge graph of forty books. Every version, and the tools behind it.">
<style>
:root{--wall:#e6e1d8;--col:#efebe4;--ink:#211e1a;--ink2:#4d463d;--accent:#6c4605;--line:#c3b8a6;
  --serif:"Source Serif 4",Georgia,"Times New Roman",serif;--tamil:"Noto Serif Tamil","Tamil Sangam MN","Tamil MN",serif;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
@media (prefers-color-scheme:dark){:root{--wall:#1d1a16;--col:#16130f;--ink:#f1eadf;--ink2:#c6bba9;--accent:#e2b866;--line:#4a4237}}
*{box-sizing:border-box}
html,body{margin:0;background:var(--col);color:var(--ink);font-family:var(--serif)}
[lang="ta"]{font-family:var(--tamil)}
main{max-width:1040px;margin:0 auto;padding:56px 20px 80px}
.kick{font:600 12px/1.4 var(--sans);letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin:0 0 10px}
h1{font:600 clamp(44px,8vw,84px)/1 var(--tamil);margin:0}
.lede{font-size:clamp(18px,2.2vw,22px);line-height:1.5;max-width:40em;margin:18px 0 0;color:var(--ink)}
h2{font:600 12px/1.4 var(--sans);letter-spacing:.08em;text-transform:uppercase;color:var(--ink2);margin:56px 0 14px;padding-top:14px;border-top:1px solid var(--line)}
a{color:inherit;text-decoration:none}
.cur{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:28px;align-items:center;background:var(--wall);border:1px solid var(--line);border-radius:16px;padding:28px;margin-top:36px}
.cur img{width:100%%;max-height:340px;object-fit:contain}
.cur .tt{font-size:clamp(28px,4vw,40px);line-height:1.15;font-weight:600;margin:6px 0 4px}
.cur .ta{font-size:18px;color:var(--ink2);margin:0 0 14px}
.cur p{margin:0;line-height:1.55}
.go{display:inline-block;margin-top:18px;font:600 13px/1 var(--sans);border:1px solid var(--ink);border-radius:999px;padding:11px 16px;background:var(--ink);color:var(--col)}
.go.alt{background:transparent;color:var(--ink);margin-left:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}
.v,.t{display:flex;flex-direction:column;gap:6px;border:1px solid var(--line);border-radius:12px;padding:18px;background:transparent;transition:background .15s}
.v:hover,.t:hover,.v:focus-visible,.t:focus-visible{background:var(--wall)}
.meta{font:400 12px/1.4 var(--sans);color:var(--ink2)}
.nm{font:600 13px/1.3 var(--sans);letter-spacing:.04em;text-transform:uppercase;color:var(--accent)}
.tt{font-size:20px;line-height:1.25;font-weight:600}
.t .ta{font-size:15px;color:var(--ink2)}
.bd{font-size:15px;line-height:1.5;color:var(--ink2)}
footer{margin-top:56px;padding-top:14px;border-top:1px solid var(--line);font:400 13px/1.6 var(--sans);color:var(--ink2)}
@media (max-width:700px){main{padding:36px 16px 60px}.cur{grid-template-columns:1fr;padding:20px}.cur img{max-height:220px}.go.alt{margin:10px 0 0}}
</style>
</head>
<body>
<main>
<p class="kick">நிலை · Nilai</p>
<h1 lang="ta">நிலை</h1>
<p class="lede">What two thousand years of Tamil poetry asks of the future, read from a knowledge graph of forty books and %(verses)s verses. Here is the current version, every one before it, and the tools the graph was built and checked with.</p>
<section class="cur">
<div>
<p class="kick">%(cdate)s · current</p>
<p class="tt">%(ctitle)s</p>
<p class="ta" lang="ta">%(cta)s</p>
<p>%(cbody)s</p>
<a class="go" href="%(chref)s">Begin</a><a class="go alt" href="%(chref)s?lang=ta" lang="ta">தமிழில்</a>
</div>
<img src="%(cimg)s" alt="A marble king's hand holding a bronze balance, the first object of the first walk">
</section>
<h2>Earlier versions</h2>
<div class="grid">%(earlier)s</div>
<h2>The graph and how it was made</h2>
<div class="grid">%(tools)s</div>
<footer>The Tamil verses are the corpus. The readings and link notes are the graph's. Everything marked கற்பனை, imagined, is ours.
Modern commentary in copyright is never quoted. Siddha formulas are history, never remedies.</footer>
</main>
</body>
</html>
""" % {"verses": "{:,}".format(20606), "cdate": E(current["date"]), "ctitle": E(current["title"]), "cta": E(current["ta_title"]),
       "cbody": E(current["body"]), "chref": E(current["href"]), "cimg": E(current["img"]),
       "earlier": "".join(card(v) for v in earlier), "tools": tool_cards}
    if not (OUT / current["img"]).exists():
        fail("landing image %s not in public/" % current["img"])
    (OUT / "index.html").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
