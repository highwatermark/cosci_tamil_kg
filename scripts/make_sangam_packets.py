"""Blind grading packets for marked chapters of any registered book.

Usage (from the repository root):
  python3 -I scripts/make_sangam_packets.py OUTDIR BOOK:CH [BOOK:CH ...] [--seed N]
  e.g. python3 -I scripts/make_sangam_packets.py /tmp/out akananuru:3 thirikadugam:1 silappathikaram:26

BOOK is one of the Sangam books (akananuru, purananuru, pattupattu) or a book registered in NEW of
scripts/book_marks.py; CH is the chapter number of kg/themes/BOOK/chNNN.json.

Each book has a field set (book_marks.py), and the field set picks the grader brief:
  akam, puram, devotional (and the three Sangam books)  docs/sangam-grader-brief.md   (group "sangam")
  ethics                                                docs/ethics-grader-brief.md   (group "ethics")
  narrative                                             docs/epic-grader-brief.md     (group "epic")
Packets are built per brief: when the chapters span more than one brief, each brief gets its own
subdirectory OUTDIR/<group>/ with its own packets and key.json; with one brief, OUTDIR itself.
A packet never mixes briefs, so its Part B is always of one field set.

Part A: every link of the chapters, shuffled, in packets of at most PER_PACKET, with hidden
calibration links of known grade mixed in (CAL_PER_40 per 40 links, rounded up). Calibration links
are Sangam links two blind graders graded alike (preferred), then graded Kural and Naladiyar links
whose note is split into a note and a `teaches` sentence. Each end prints its Tamil (numbered lines
for poems, units and line spans) and its marked reading; a Sangam-field end also its colophon, text
flags and the marker's thinai, akam/puram and uri; an ethics end its domain, items and Pazhamozhi
proverb; an epic end its speaker, event and claims; a Kural or Naladiyar end Pope's rendering. A
link also prints its `item` and `list_adds` (ethics) or `gains` (epic bridges). The Purananuru's
modern title, note and commentary are never printed.

Part B, by field set (the marker's tags are never printed; they go to key.json):
  akam       every akam or mixed poem, numbered Tamil and colophon: blind re-tag of ullurai, iraicchi
  ethics     every marked verse, numbered Tamil, the work and (Pazhamozhi) the heading: blind re-tag
             of domain, items, count word, norm and the Pazhamozhi story
  narrative  every marked unit or verse, numbered Tamil, book and section, and the line on either
             side: blind re-tag of claims (school, stance) and echoes
  puram and devotional books have no Part B.
Part B items go to a packet whose Part A does not print them. For ethics and narrative, whose Part A
prints the very tags Part B re-tags, an item that every link packet prints goes to a Part-B-only
packet instead (at most PER_PACKET_B items); an akam poem goes to the least-loaded packet, as before,
flagged reading_in_own_packet (Part A prints its reading, not its ullurai or iraicchi).

Writes packet_N.md and key.json (one entry per item, with the proposer's tags and, for calibration
links, the known grade). Grades go in graded/packet_N.<grader>.json beside them and are scored by
scripts/score_sangam_grades.py.
"""
import json
import math
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import book_marks as bm  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "kg" / "core"
THEMES = ROOT / "kg" / "themes"
SANGAM = ("akananuru", "purananuru", "pattupattu")
NEW = bm.NEW
MARKED_BOOKS = SANGAM + tuple(NEW)
NODE_BOOKS = ("kural", "naladiyar", "tirumanthiram", "thiruppugazh", "siddhar")
ALL_BOOKS = set(MARKED_BOOKS) | set(NODE_BOOKS)
PER_PACKET = 40
PER_PACKET_B = {"akam": 40, "ethics": 30, "narrative": 20}
CAL_PER_40 = 4
CAL_MIX = ["sound", "sound", "weak", "forced"]
PATTU_ID = re.compile(r"pattupattu:(\d+):(\d+)-(\d+)")

# docs/corpus-groups.md
GROUP = {"akananuru": "ettuthogai_akam", "natrinai": "ettuthogai_akam", "kuruntokai": "ettuthogai_akam",
         "ainkurunuru": "ettuthogai_akam", "kalittokai": "ettuthogai_akam",
         "purananuru": "ettuthogai_puram", "patitruppattu": "ettuthogai_puram",
         "paripadal": "ettuthogai_devotional", "pattupattu": "pattupattu",
         "kural": "ethics", "naladiyar": "ethics",
         "tirumanthiram": "devotional", "thiruppugazh": "devotional", "siddhar": "devotional"}
for _b, (_fs, _) in NEW.items():
    if _b not in GROUP:
        GROUP[_b] = {"ethics": "ethics", "akam": "kilkanakku_akam", "puram": "kilkanakku_akam"}.get(_fs)
for _b in ("silappathikaram", "manimekalai", "civaka_cintamani", "valayapathi", "kundalakesi"):
    GROUP[_b] = "epics_great"
for _b in ("soolamani", "neelakesi", "naga_kumara_kaviyam", "udayana_kumara_kaviyam", "yasodhara_kaviyam"):
    GROUP[_b] = "epics_minor"

BOOK_NAME = {"akananuru": "Akananuru", "purananuru": "Purananuru", "pattupattu": "Pattupattu",
             "kural": "Kural", "naladiyar": "Naladiyar"}
for _b in NEW:
    BOOK_NAME.setdefault(_b, _b.replace("_", " ").title())

BRIEF = {"sangam": "docs/sangam-grader-brief.md", "ethics": "docs/ethics-grader-brief.md",
         "epic": "docs/epic-grader-brief.md"}
PART_B_HEAD = {"akam": "POEM", "ethics": "VERSE", "narrative": "UNIT"}
PART_B_KEY = {"akam": "poems", "ethics": "verses", "narrative": "units"}


def fieldset(book):
    if book in SANGAM:
        return "sangam"
    return NEW[book][0]


def brief_of(book):
    fs = fieldset(book)
    return {"ethics": "ethics", "narrative": "epic"}.get(fs, "sangam")


def part_b_kind(book):
    """The Part B re-tag a book's verses get, or None."""
    fs = fieldset(book)
    if fs in ("sangam", "akam"):
        return "akam"
    if fs in ("ethics", "narrative"):
        return fs
    return None


def read_jsonl(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def usage(msg=None):
    if msg:
        print("error:", msg, file=sys.stderr)
    print(__doc__.split("\n\n")[1], file=sys.stderr)
    sys.exit(2)


def parse_args(argv):
    seed, rest = 31, []
    i = 0
    while i < len(argv):
        if argv[i] == "--seed":
            if i + 1 >= len(argv):
                usage("--seed needs a number")
            seed = int(argv[i + 1])
            i += 2
            continue
        rest.append(argv[i])
        i += 1
    if len(rest) < 2:
        usage()
    out, chs = Path(rest[0]), []
    for spec in rest[1:]:
        m = re.fullmatch(r"([a-z_]+):(\d+)", spec)
        if not m or m.group(1) not in MARKED_BOOKS:
            usage(f"bad chapter {spec!r}: want BOOK:CH with BOOK a Sangam book or one of book_marks.NEW")
        chs.append((m.group(1), int(m.group(2))))
    return out, chs, seed


def ref(book, x):
    """A link end or verse key as a full id: '12' and 12 -> book:12; 'kural:5' stays; 'thirattu:1'
    (a key of this book that is not another book's id) -> book:thirattu:1."""
    s = str(x)
    m = re.match(r"([a-z_]+):", s)
    if m and m.group(1) in ALL_BOOKS:
        return s
    return f"{book}:{s}"


def book_of(vid):
    return vid.split(":")[0]


def flag_lines_of(flags):
    return [f"FLAG {f['kind']}" + (f" line {f['line']}" if f.get("line") else "")
            + f": {' '.join(str(f.get('detail') or '').split())}" for f in flags]


def colophon_line(col):
    keys = ["thinai", "thurai", "poet", "patron"] + [k for k in ("subject", "decade") if col.get(k)]
    return "COLOPHON: " + " | ".join(f"{k}: {col.get(k) if col.get(k) is not None else '-'}" for k in keys)


class Corpus:
    def __init__(self):
        self.core = {b: {} for b in SANGAM}
        for b in ("akananuru", "purananuru"):
            for r in read_jsonl(CORE / f"{b}.jsonl"):
                if r.get("tamil"):
                    self.core[b][r["id"]] = r
        for u in read_jsonl(CORE / "pattupattu_units.jsonl"):
            self.core["pattupattu"][u["id"]] = u
        self.poems = {p["number"]: p for p in read_jsonl(CORE / "pattupattu.jsonl")}
        self.flags = {}
        for f in read_jsonl(CORE / "sangam_text_flags.jsonl"):
            self.flags.setdefault(f["id"], []).append(f)
        self.marks, self.casts, self.order = {}, {}, {}
        for b in MARKED_BOOKS:
            d_ = THEMES / b
            for p in sorted(d_.glob("ch*.json")) if d_.exists() else []:
                d = json.loads(p.read_text(encoding="utf-8"))
                cast = {c.get("id"): c for c in d.get("cast") or [] if isinstance(c, dict)}
                for k, v in d.get("verses", {}).items():
                    vid = ref(b, k)
                    self.marks[vid] = v
                    self.casts[vid] = cast
        self.nodes = {}
        for b in NODE_BOOKS:
            for n in read_jsonl(ROOT / "kg" / b / "nodes.jsonl"):
                if n.get("type") == "Verse":
                    self.nodes[n["id"]] = n
        self.tm = {r["number"]: r for r in read_jsonl(CORE / "tirumanthiram.jsonl")}
        self.tp = {r["number"]: r for r in read_jsonl(CORE / "thiruppugazh.jsonl")}
        self.new_core = {}

    # ---- the registered books (book_marks.NEW) ----
    def new_records(self, book):
        if book not in self.new_core:
            recs = bm.core_records(book)
            self.new_core[book] = ({bm.key_of(book, r): r for r in recs}, recs)
        return self.new_core[book]

    def new_resolve(self, vid):
        """(record, first line, last line, whole?) for a NEW-book id, or raise KeyError."""
        book, rest = vid.split(":", 1)
        by_key, _ = self.new_records(book)
        if rest in by_key:
            r = by_key[rest]
            return r, 1, len(r["tamil"]), True
        m = re.fullmatch(r"(.+):(\d+)-(\d+)", rest)
        if m and m.group(1) in by_key and bm.span_ok(book, rest):
            r = by_key[m.group(1)]
            return r, int(m.group(2)), int(m.group(3)), False
        raise KeyError(vid)

    def new_title(self, vid, rec, a, z, whole):
        book = book_of(vid)
        name = BOOK_NAME[book]
        scheme = NEW[book][1][0]
        if scheme == "units":
            return f"{name}, {rec.get('title')}" + ("" if whole else f", lines {a}-{z}")
        if scheme == "songs":
            return f"{name} {bm.key_of(book, rec)}, {rec.get('title') or 'திரட்டு'}" + ("" if whole else f", lines {a}-{z}")
        num = rec.get("number")
        head = f"{name} {num}" if num is not None else f"{name} {bm.key_of(book, rec)}"
        sec = rec.get("chapter") or rec.get("section")
        if sec and book != "pazhamozhi_nanooru":
            head += f", {sec}"
        if rec.get("kind") in bm.INTRO_KINDS:
            head += f" [{rec['kind']}]"
        return head

    def unit_text(self, vid):
        """(title, numbered lines, colophon dict or None, flag lines) for any marked-book id."""
        b = book_of(vid)
        if b == "pattupattu":
            m = PATTU_ID.fullmatch(vid)
            if not m:
                raise KeyError(vid)
            poem, a, z = (int(g) for g in m.groups())
            p = self.poems[poem]
            if not 1 <= a <= z <= len(p["tamil"]):
                raise KeyError(vid)
            lines = list(enumerate(p["tamil"][a - 1:z], a))
            col = {k: p.get(k) for k in ("thinai", "thurai", "poet", "patron")}
            title = f"{p['title']}, lines {a}-{z}"
            flags = [f for f in self.flags.get(p["id"], []) if f.get("line") and a <= f["line"] <= z]
            return title, lines, col, flag_lines_of(flags)
        if b in SANGAM:
            r = self.core[b][vid]
            lines = list(enumerate(r["tamil"], 1))
            col = {k: r.get(k) for k in ("thinai", "thurai", "poet", "patron")}
            title = f"{BOOK_NAME[b]} {r['number']}" + (f", {r['section']}" if r.get("section") else "")
            return title, lines, col, flag_lines_of(self.flags.get(vid, []))
        rec, a, z, whole = self.new_resolve(vid)
        lines = list(enumerate(rec["tamil"][a - 1:z], a))
        col = None
        if NEW[b][0] in ("akam", "puram", "devotional"):
            col = {"thinai": rec.get("thinai"), "thurai": rec.get("thurai"),
                   "poet": rec.get("poet") or rec.get("author"), "patron": rec.get("patron")}
            if b == "paripadal":
                col["subject"] = rec.get("title")
            if rec.get("decade"):
                col["decade"] = f"{rec['decade']} {rec.get('decade_title') or ''}".strip()
        flags = [f for f in self.flags.get(rec["id"], []) if whole or (f.get("line") and a <= f["line"] <= z)]
        return self.new_title(vid, rec, a, z, whole), lines, col, flag_lines_of(flags)

    def overlapping_marks(self, vid):
        """Marked units of the same record that overlap a span, for an end that is not itself marked."""
        b = book_of(vid)
        try:
            rec, a, z, _ = self.new_resolve(vid)
        except KeyError:
            return []
        rk = bm.key_of(b, rec)
        out = []
        for k, m in self.marks.items():
            mm = re.fullmatch(re.escape(f"{b}:{rk}:") + r"(\d+)-(\d+)", k)
            if mm and int(mm.group(1)) <= z and int(mm.group(2)) >= a:
                out.append((k, m))
        if not out and f"{b}:{rk}" in self.marks and f"{b}:{rk}" != vid:
            out.append((f"{b}:{rk}", self.marks[f"{b}:{rk}"]))
        return sorted(out, key=lambda t: t[0])

    # ---- marker's fields, per field set ----
    def mark_lines(self, vid, m):
        b = book_of(vid)
        fs = fieldset(b) if b in MARKED_BOOKS else None
        out = [f"Marked reading: {m.get('reading')}"]
        if m.get("nuance"):
            out.append(f"Marker's nuance: {m['nuance']}")
        if fs in ("sangam", "akam", "puram", "devotional"):
            facts = [f"akam/puram: {m.get('akam_puram')}", f"marker's thinai: {m.get('thinai')}"]
            if m.get("uri"):
                facts.append(f"uri: {m['uri']}")
            out.append("Marker's fields: " + "; ".join(facts))
        elif fs == "ethics":
            dom = f"domain: {m.get('domain')}" + (f" ({m['domain_note']})" if m.get("domain_note") else "")
            out.append("Marker's fields: " + dom + (f"; count word: {m['count_word']}" if m.get("count_word") else ""))
            for j, it in enumerate(m.get("items") or [], 1):
                if isinstance(it, dict):
                    out.append(f"  item {j}: {it.get('thing')} (line {it.get('line')}): {it.get('claim')}"
                               + (f" [domain {it['domain']}]" if it.get("domain") else ""))
            pz = m.get("pazhamozhi")
            if isinstance(pz, dict):
                out.append(f"  proverb (lines {pz.get('lines')}): {pz.get('proverb')}, applied to: {pz.get('applied_to')}")
        elif fs == "narrative":
            cast = self.casts.get(vid, {})
            name = lambda i: "narrator" if i == "narrator" else (f"{cast[i].get('tamil')} ({i})" if i in cast else str(i))
            sp = m.get("speaker") or {}
            if sp:
                out.append(f"Marker's speaker: {name(sp.get('who'))}"
                           + (f", '{sp['form']}' line {sp.get('line')}" if sp.get("form") else "")
                           + (f", to {name(sp['addressee'])}" if sp.get("addressee") else ""))
            out.append(f"Marker's event: {m.get('event')}")
            for c in m.get("claims") or []:
                if isinstance(c, dict):
                    out.append(f"  claim (line {c.get('line')}, {c.get('school')}"
                               + (f"/{c['school_detail']}" if c.get("school_detail") else "")
                               + f", {c.get('stance')}, voiced by {name(c.get('voiced_by'))}): {c.get('claim')}")
            if m.get("unit_note"):
                out.append(f"Unit note: {m['unit_note']}")
        if m.get("uncertain"):
            out.append("The marker flagged this verse's sense as uncertain.")
        return out

    def block(self, vid):
        b = book_of(vid)
        if b in MARKED_BOOKS:
            title, lines, col, flag_lines = self.unit_text(vid)
            out = [f"### {vid} ({title})"]
            if col is not None:
                out.append(colophon_line(col))
            elif b == "pazhamozhi_nanooru":
                rec = self.new_resolve(vid)[0]
                if rec.get("chapter"):
                    out.append(f"HEADING: {rec['chapter']}")
            out += [f"{i:4} {t}" for i, t in lines]
            out += flag_lines
            m = self.marks.get(vid)
            if m is not None:
                return out + self.mark_lines(vid, m)
            over = self.overlapping_marks(vid) if b in NEW else []
            if not over:
                return out + ["Marked reading: (this verse is not yet marked)"]
            out.append("(This span is not a marked unit; the marked units it overlaps follow.)")
            for k, mk in over:
                out.append(f"[{k}]")
                out += self.mark_lines(k, mk)
            return out
        n = self.nodes[vid]
        num = int(vid.split(":")[1])
        if b == "kural":
            head = f"Kural {num}"
        elif b == "naladiyar":
            head = f"Naladiyar {num}"
        elif b == "tirumanthiram":
            r = self.tm.get(num, {})
            head = f"Tirumanthiram {num} (tantra {r.get('tantra')}, {r.get('chapter')})"
        elif b == "thiruppugazh":
            head = f"Thiruppugazh {num} ({self.tp.get(num, {}).get('heading')})"
        else:
            head = f"Siddhar {num} ({n.get('siddhar')}, {n.get('work_title')})"
        out = [f"### {vid}: {head}", "Tamil: " + " / ".join(n["tamil"])]
        if b in ("kural", "naladiyar") and n.get("pope"):
            p = n["pope"]
            out.append("Pope: " + (p.get("gloss") or " / ".join(p.get("couplet", [])) if isinstance(p, dict) else p))
        out.append(f"Marked reading: {n.get('reading')}")
        if n.get("nuance"):
            out.append(f"Marker's nuance: {n['nuance']}")
        if n.get("uncertain"):
            out.append("The marker flagged this verse's sense as uncertain.")
        return out

    def exists(self, vid):
        b = book_of(vid)
        if b in MARKED_BOOKS:
            try:
                self.unit_text(vid)
                return True
            except (KeyError, IndexError):
                return False
        return vid in self.nodes

    def context(self, vid):
        """The Tamil line just before and just after a unit or verse, for Part B of the epics."""
        b = book_of(vid)
        rec, a, z, _ = self.new_resolve(vid)
        _, recs = self.new_records(b)
        idx = next(i for i, r in enumerate(recs) if r["id"] == rec["id"])
        if a > 1:
            before = (f"line {a - 1}", rec["tamil"][a - 2])
        elif idx > 0:
            before = (f"{recs[idx - 1]['id']}, last line", recs[idx - 1]["tamil"][-1])
        else:
            before = None
        if z < len(rec["tamil"]):
            after = (f"line {z + 1}", rec["tamil"][z])
        elif idx + 1 < len(recs):
            after = (f"{recs[idx + 1]['id']}, first line", recs[idx + 1]["tamil"][0])
        else:
            after = None
        return before, after


def split_note(note):
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z])", note.strip())
    if len(parts) < 2:
        return None
    return " ".join(parts[:-1]), parts[-1]


def calibration_pool(rng):
    pool = {g: [] for g in ("sound", "weak", "forced", "wrong")}
    for b in ("kural", "naladiyar"):
        for e in read_jsonl(ROOT / "kg" / b / "edges.jsonl"):
            if "audit" not in e or "note" not in e or e["audit"] not in pool:
                continue
            if b == "naladiyar" and not e.get("cross_book"):
                continue
            sp = split_note(e["note"])
            if sp:
                pool[e["audit"]].append(e | {"_note": sp[0], "_teaches": sp[1]})
    for g in pool:
        rng.shuffle(pool[g])
    # Sangam links that two blind graders graded alike go on top, so calibration looks like the
    # links around it (popped first). Any key.json under sangam_grading counts (rounds and pilots).
    sangam = {g: [] for g in pool}
    for kp in sorted((ROOT / "kg" / "themes" / "sangam_grading").rglob("key.json")):
        grades = {}
        for f in kp.parent.glob("graded/packet_*.json"):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            links = data.get("links", []) if isinstance(data, dict) else [x for x in data if isinstance(x, dict) and "grade" in x]
            for x in links:
                grades.setdefault((x.get("a"), x.get("b")), []).append(x.get("grade"))
        for k in json.loads(kp.read_text(encoding="utf-8")):
            if "a" not in k:
                continue
            gs = grades.get((k["a"], k["b"]), [])
            if k.get("kind") == "proposal" and len(gs) >= 2 and len(set(gs)) == 1 and gs[0] in pool:
                sangam[gs[0]].append({"s": k["a"], "o": k["b"], "p": k["type"], "audit": gs[0],
                                      "_note": k["note"], "_teaches": k["teaches"], "_sangam": True})
    for g in pool:
        rng.shuffle(sangam[g])
        pool[g] = pool[g] + sangam[g]
    return pool


# ---- Part B: the proposer's tags, in the shape the grader's output takes ----

def akam_tags(m):
    u, i = m.get("ullurai"), m.get("iraicchi")
    return {"ullurai_present": bool(u), "iraicchi_present": bool(i),
            "ullurai_vehicle": [[v.get("form"), v.get("line")] for v in (u or {}).get("vehicle", [])] if u else None,
            "iraicchi_carrier": [i["carrier"].get("form"), i["carrier"].get("line")] if i and i.get("carrier") else None,
            "ullurai": u, "iraicchi": i}


def ethics_tags(m):
    pz = m.get("pazhamozhi")
    story = (pz or {}).get("story") if isinstance(pz, dict) else None
    norm = m.get("norm")
    return {"tags": {
        "domain": m.get("domain"),
        "items": [[it.get("thing"), it.get("line")] for it in m.get("items") or [] if isinstance(it, dict)] if m.get("items") is not None else None,
        "count_word": m.get("count_word"),
        "norm": {"kinds": list(norm.get("kinds") or [])} if isinstance(norm, dict) else None,
        "pazhamozhi": {"proverb_lines": list(pz.get("lines") or []), "kind": (story or {}).get("kind"),
                       "who": (story or {}).get("who")} if isinstance(pz, dict) else None}}


def narrative_tags(m):
    return {"tags": {
        "claims": [{"line": c.get("line"), "school": c.get("school"), "stance": c.get("stance"),
                    "school_detail": c.get("school_detail"), "gist": c.get("claim")}
                   for c in m.get("claims") or [] if isinstance(c, dict)],
        "echoes": [{"line": e.get("line"), "b": e.get("b"), "kind": e.get("kind"), "words": e.get("words")}
                   for e in m.get("echoes") or [] if isinstance(e, dict)]}}


def part_b_items(book, c, d):
    kind = part_b_kind(book)
    out = []
    if kind is None:
        return out
    for k, v in d.get("verses", {}).items():
        if not isinstance(v, dict):
            continue
        base = {"id": ref(book, k), "kind": "retag", "fieldset": kind, "book": book, "chapter": c}
        if kind == "akam":
            if v.get("akam_puram") in ("akam", "mixed"):
                out.append(base | {"akam_puram": v.get("akam_puram")} | akam_tags(v))
        elif kind == "ethics":
            out.append(base | ethics_tags(v))
        else:
            out.append(base | narrative_tags(v))
    return out


def part_b_lines(corpus, q, j):
    kind = q["fieldset"]
    title, tl, col, _ = corpus.unit_text(q["id"])
    lines = [f"## {PART_B_HEAD[kind]} {q['id']} ({title})"]
    if kind == "akam":
        lines.append(colophon_line(col))
    elif kind == "ethics":
        rec = corpus.new_resolve(q["id"])[0]
        lines.append(f"WORK: {BOOK_NAME[q['book']]} ({rec.get('title')})")
        if q["book"] == "pazhamozhi_nanooru" and rec.get("chapter"):
            lines.append(f"HEADING: {rec['chapter']}")
    else:
        rec, a, z, _ = corpus.new_resolve(q["id"])
        sec = rec.get("title") if NEW[q["book"]][1][0] == "units" else rec.get("section")
        lines.append(f"BOOK: {BOOK_NAME[q['book']]} | SECTION: {sec or '-'}"
                     + (f" | kandam: {rec['kandam']}" if rec.get("kandam") else ""))
        before, after = corpus.context(q["id"])
        if before:
            lines.append(f"BEFORE (context only; {before[0]}): {before[1]}")
    lines += [f"{i:4} {t}" for i, t in tl]
    if kind == "narrative" and after:
        lines.append(f"AFTER (context only; {after[0]}): {after[1]}")
    return lines + [""]


def build(out, chs, rng, corpus, pool, brief):
    props, retags, books = [], [], []
    for book, c in chs:
        p = THEMES / book / f"ch{c:03d}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        books.append(book)
        for l in d.get("links", []):
            a, b = ref(book, l["a"]), ref(book, l["b"])
            for v in (a, b):
                if not corpus.exists(v):
                    sys.exit(f"error: {book}/{p.name}: link end {v} not found in the corpus")
            ga, gb = GROUP.get(book_of(a)), GROUP.get(book_of(b))
            item = {"a": a, "b": b, "type": l["type"].lower(), "note": l["note"],
                    "teaches": l.get("teaches"), "kind": "proposal", "brief": brief, "book": book, "chapter": c,
                    "target_book": book_of(b), "group_a": ga, "group_b": gb, "within_group": ga == gb}
            for f in ("item", "list_adds", "gains"):
                if f in l:
                    item[f] = l[f]
            if fieldset(book) == "narrative":
                item["bridge"] = book_of(b) not in NEW or NEW[book_of(b)][0] != "narrative"
            props.append(item)
        retags += part_b_items(book, c, d)
    if not props and not retags:
        print(f"[{brief}] nothing to grade")
        return
    rng.shuffle(props)
    rng.shuffle(retags)
    if "pool" not in pool:  # drawn after the first shuffles, so a one-brief run keeps the old random sequence
        pool["pool"] = calibration_pool(rng)
    cal = pool["pool"]
    n = max(1, math.ceil(len(props) / PER_PACKET))
    link_packets = [props[i::n] for i in range(n)] if props else [[]]
    n = len(link_packets)
    shown = [{v for l in pk for v in (l["a"], l["b"])} for pk in link_packets]
    b_packets = [[] for _ in range(n)]
    overflow = []
    for q in retags:
        free = [i for i in range(n) if q["id"] not in shown[i]]
        if free:
            i = min(free, key=lambda i: len(b_packets[i]))
            b_packets[i].append(q | {"reading_in_own_packet": False})
        elif q["fieldset"] == "akam":
            i = min(range(n), key=lambda i: len(b_packets[i]))
            b_packets[i].append(q | {"reading_in_own_packet": True})
        else:
            overflow.append(q | {"reading_in_own_packet": False})
    # Part-B-only packets for the items every link packet prints (ethics and narrative)
    if overflow:
        cap = PER_PACKET_B[overflow[0]["fieldset"]]
        k = math.ceil(len(overflow) / cap)
        for j in range(k):
            link_packets.append([])
            b_packets.append(overflow[j::k])
    out.mkdir(parents=True, exist_ok=True)
    key, mixi = [], 0
    other_books = sorted({b for b in books if b not in SANGAM})
    summary = []
    for pi, (pk, pp) in enumerate(zip(link_packets, b_packets), 1):
        ncal = math.ceil(CAL_PER_40 * len(pk) / PER_PACKET) if pk else 0
        for _ in range(ncal):
            g = CAL_MIX[mixi % len(CAL_MIX)]
            mixi += 1
            e = cal[g].pop() if cal[g] else cal["weak"].pop()
            ga, gb = GROUP.get(book_of(e["s"])), GROUP.get(book_of(e["o"]))
            pk.append({"a": e["s"], "b": e["o"], "type": e["p"].lower(), "note": e["_note"],
                       "teaches": e["_teaches"], "kind": "calibration", "known": e["audit"], "brief": brief,
                       "teaches_derived": not e.get("_sangam"), "book": book_of(e["s"]), "target_book": book_of(e["o"]),
                       "group_a": ga, "group_b": gb, "within_group": ga == gb})
        rng.shuffle(pk)
        kinds = {q["fieldset"] for q in pp}
        assert len(kinds) <= 1, "a packet's Part B mixes field sets"
        kind = kinds.pop() if kinds else None
        bkey = PART_B_KEY.get(kind, "poems")
        lines = [f"# Packet {pi}", "",
                 f"Follow {BRIEF[brief]}. Read that brief before you start.", "",
                 f"Part A: {len(pk)} links. Part B: {len(pp)} {bkey}.",
                 f"Write one JSON object: {{\"links\": [one object per LINK, in order], "
                 f"\"{bkey}\": [one object per {PART_B_HEAD.get(kind, 'POEM')}, in order]}}, in the formats of {BRIEF[brief]}."]
        if brief == "sangam" and other_books:
            lines.append("Besides the books the brief names, links here come from "
                         + ", ".join(f"{BOOK_NAME[b]} (`{b}:N`" + (", or `paripadal:<song>:<start>-<end>` for a span of a song" if b == "paripadal" else "") + ")"
                                     for b in other_books)
                         + ", marked with the same Sangam fields; grade them the same way.")
        lines.append("")
        if pk:
            lines += [f"# Part A: links ({len(pk)})", ""]
        for j, l in enumerate(pk, 1):
            lines += [f"## LINK {l['a']} -> {l['b']} type={l['type'].upper()}",
                      f"Note: {l['note']}", f"Teaches: {l['teaches']}"]
            if "item" in l:
                lines.append(f"Item: {l['item']} (item {l['item']} of {l['a']}'s marked items)")
            if "list_adds" in l:
                lines.append(f"List adds: {l['list_adds']}")
            if isinstance(l.get("gains"), dict):
                lines.append(f"Gains: epic side: {l['gains'].get('a')} | other side: {l['gains'].get('b')}")
            lines.append("")
            lines += corpus.block(l["a"]) + [""] + corpus.block(l["b"]) + [""]
            key.append(l | {"packet": pi, "part": "A", "order": j})
        if pp:
            head = {"akam": "blind re-tag of ullurai and iraicchi",
                    "ethics": "blind re-tag of domain, items, norm and the Pazhamozhi story",
                    "narrative": "blind re-tag of claims and echoes"}[kind]
            lines += [f"# Part B: {head} ({len(pp)} {bkey})", ""]
            for j, q in enumerate(pp, 1):
                lines += part_b_lines(corpus, q, j)
                key.append(q | {"packet": pi, "part": "B", "order": j})
        (out / f"packet_{pi}.md").write_text("\n".join(lines), encoding="utf-8")
        npr = sum(1 for l in pk if l["kind"] == "proposal")
        print(f"[{brief}] packet_{pi}.md: {len(pk)} links ({npr} proposed, {ncal} calibration), "
              f"{len(pp)} {bkey}" + (f" ({kind})" if kind else ""))
        summary.append((pi, len(pk), ncal, len(pp), kind))
    (out / "key.json").write_text(json.dumps(key, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{brief}] {len(props)} proposed links and {len(retags)} Part B items in {len(link_packets)} packets -> {out}")


def main():
    out, chs, seed = parse_args(sys.argv[1:])
    rng = random.Random(seed)
    corpus = Corpus()
    for book, c in chs:
        p = THEMES / book / f"ch{c:03d}.json"
        if not p.exists():
            usage(f"{p} does not exist")
    by_brief = {}
    for book, c in chs:
        by_brief.setdefault(brief_of(book), []).append((book, c))
    pool = {}  # one calibration pool for all briefs, so no calibration link is used twice
    for brief in ("sangam", "ethics", "epic"):
        if brief in by_brief:
            build(out / brief if len(by_brief) > 1 else out, by_brief[brief], rng, corpus, pool, brief)


if __name__ == "__main__":
    main()
