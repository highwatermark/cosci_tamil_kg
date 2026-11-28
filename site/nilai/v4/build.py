"""Nilai v4: thirteen chapters, a walk through the graph.

Run:  python3 -I site/nilai/v4/build.py
Writes site/nilai/v4/index.html and site/nilai/v4/img/*.webp.

THE GRAPH IS THE SCRIPT. Each chapter is three corpus verses joined by two graded sound links, read from
site/nilai/v4/chapters.json, which validate_chapters.py checks against kg/ (the build runs it and stops on any
failure). Every verse scene shows its Tamil verbatim with the graph's own English reading; every transition is a
sound link whose text writes along a gold thread drawn in the link's true direction (from both ends at once when the
link is symmetric). The one invented beat per chapter is labelled கற்பனை · imagined, and shows an object turning
into its future form.

Stdlib only. Images: site/nilai/assets/src/<id>.jpg -> build/v3/cutout_green -> assets/<id>.png ->
assets/web/<id>.webp (as in v3), and a tight crop of each cut-out for this page in v4/img/<id>.webp.
Set V4_ALLOW_MISSING=1 to build with placeholders while images are still being made.
"""
import html
import json
import math
import os
import subprocess
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
NILAI = HERE.parent
REPO = NILAI.parent.parent
KG = REPO / 'kg'
ASSETS = NILAI / 'assets'
V3 = NILAI / 'build' / 'v3'
IMG = HERE / 'img'
ALLOW_MISSING = bool(os.environ.get('V4_ALLOW_MISSING'))

FAIL, WARN = [], []


def fail(msg):
    FAIL.append(msg)


def jsonl(path):
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


# ---------------------------------------------------------------------------------------------------------
# 1. The chapters, validated against the graph by validate_chapters.py (Tamil, readings, links, flags).
# ---------------------------------------------------------------------------------------------------------
val = subprocess.run([sys.executable, '-I', str(HERE / 'validate_chapters.py')], capture_output=True, text=True)
if val.returncode != 0 or 'VALIDATION PASSED' not in val.stdout:
    fail('validate_chapters.py failed:\n' + val.stdout[-2000:] + val.stderr[-1000:])
CH = json.load(open(HERE / 'chapters.json', encoding='utf-8'))['chapters']
if len(CH) != 13:
    fail('expected 13 chapters, found %d' % len(CH))


def aid(d):
    """Asset id of a verse or forward end: an existing asset, or a new image made for v4."""
    return d.get('asset') or d.get('new_image')


for ch in CH:
    if len(ch['verses']) != 3 or len(ch['links']) != 2:
        fail('%s: needs 3 verses and 2 links' % ch['id'])
    vids = [v['id'] for v in ch['verses']]
    for L in ch['links']:
        if L['from'] not in vids or L['to'] not in vids:
            fail('%s: link %s -> %s leaves the chapter' % (ch['id'], L['from'], L['to']))
        td = L['true_direction']
        if not td['symmetric'] and {td['s'], td['o']} != {L['from'], L['to']}:
            fail('%s: true direction of %s -> %s names other verses' % (ch['id'], L['from'], L['to']))
    l1 = {ch['links'][0]['from'], ch['links'][0]['to']}
    if l1 != {vids[0], vids[1]}:
        fail('%s: link 1 must join verses 1 and 2' % ch['id'])
    if vids[2] not in (ch['links'][1]['from'], ch['links'][1]['to']):
        fail('%s: link 2 must reach verse 3' % ch['id'])
    for v in ch['verses']:
        if not aid(v):
            fail('%s: %s has no image' % (ch['id'], v['id']))
    for k in ('then', 'future'):
        if not aid(ch['forward'][k]):
            fail('%s: forward %s has no image' % (ch['id'], k))

# ---------------------------------------------------------------------------------------------------------
# 2. The real numbers, counted from the graph.
# ---------------------------------------------------------------------------------------------------------
bridges = list(jsonl(KG / 'groups' / 'bridges.jsonl'))
index = json.load(open(KG / 'groups' / 'index.json', encoding='utf-8'))
BOOKS = []   # (group, book, verses)
for g, v in index.items():
    for b in v['books']:
        n = (v.get('verses_by_book') or {}).get(b)
        if n is None:
            p = KG / b / 'nodes.jsonl'
            n = sum(1 for d in jsonl(p) if d.get('type') == 'Verse') if p.exists() else 0
        if n:
            BOOKS.append((g, b, n))
N_BOOKS = len(BOOKS)
N_VERSES = sum(b[2] for b in BOOKS)
SOUND = [x for x in bridges if x['grade'] == 'sound']
N_SOUND = len(SOUND)
if (N_BOOKS, N_VERSES, N_SOUND) != (40, 20606, 1856):
    fail('counts changed: %d books, %d verses, %d sound bridges (page text says 40 / 20,606 / 1,856)' % (N_BOOKS, N_VERSES, N_SOUND))
N_CH_BOOKS = len({v['book'] for ch in CH for v in ch['verses']})
N_CH_GROUPS = len({v['group'] for ch in CH for v in ch['verses']})

# ---------------------------------------------------------------------------------------------------------
# 3. Constellation layout: the books as clusters of dots, grouped as the graph groups them.
# ---------------------------------------------------------------------------------------------------------
GROUP_ORDER = ['epics_great', 'epics_minor', 'pattupattu', 'ettuthogai_puram', 'devotional',
               'ettuthogai_devotional', 'ettuthogai_akam', 'kilkanakku_akam', 'ethics']
GROUP_LABEL = {'devotional': 'devotional', 'ethics': 'ethics', 'kilkanakku_akam': 'Kilkanakku akam',
               'ettuthogai_akam': 'Ettuthogai akam', 'ettuthogai_puram': 'Ettuthogai puram',
               'ettuthogai_devotional': 'Paripadal', 'pattupattu': 'Pattuppattu', 'epics_minor': 'minor epics',
               'epics_great': 'great epics'}
book_list = []
for g in GROUP_ORDER:
    for (gg, b, n) in BOOKS:
        if gg == g:
            nd = max(4, min(72, round(math.sqrt(n) * 1.15)))
            book_list.append({'g': g, 'b': b, 'n': n, 'nd': nd, 'rb': 5.2 * math.sqrt(nd) + 3})
GAP, GGAP = 8.0, 40.0
need = sum(2 * b['rb'] + GAP for b in book_list) + GGAP * len(GROUP_ORDER)
R = need / (2 * math.pi)
ang = -math.pi / 2 + 0.35
prev = None
gmid = {}
for b in book_list:
    if b['g'] != prev:
        if prev is not None:
            gmid[prev][1] = ang
        ang += GGAP / R
        gmid[b['g']] = [ang, None]
        prev = b['g']
    ang += b['rb'] / R
    b['a'] = ang
    ang += (b['rb'] + GAP) / R
gmid[prev][1] = ang
rbmax = max(b['rb'] for b in book_list)
scale = 400.0 / (R + rbmax)
dots = []      # x, y, group index
book_dots = {}
centres = {}
for i, b in enumerate(book_list):
    rr = R + (14 if i % 2 else -14)
    cx = 500 + scale * rr * math.cos(b['a'])
    cy = 500 + scale * rr * math.sin(b['a'])
    centres[b['b']] = (cx, cy)
    gi = GROUP_ORDER.index(b['g'])
    book_dots[b['b']] = []
    for k in range(b['nd']):
        rk = scale * b['rb'] * 0.92 * math.sqrt((k + 0.5) / b['nd'])
        th = k * 2.399963 + i
        x, y = round(cx + rk * math.cos(th), 1), round(cy + rk * math.sin(th), 1)
        dots.append([x, y, gi])
        book_dots[b['b']].append((x, y))
labels = []
for g in GROUP_ORDER:
    a = (gmid[g][0] + gmid[g][1]) / 2
    rr = scale * (R + rbmax + 26)
    labels.append({'t': GROUP_LABEL[g], 'x': round(500 + rr * math.cos(a), 1), 'y': round(500 + rr * math.sin(a), 1),
                   'a': round(a, 4), 'r': round(rr, 1),
                   'anchor': 'start' if math.cos(a) > 0.25 else ('end' if math.cos(a) < -0.25 else 'middle')})
pairs = {}
for x in SOUND:
    k = tuple(sorted((x['book_a'], x['book_b'])))
    pairs[k] = pairs.get(k, 0) + 1
edges = []
for (a, b), c in sorted(pairs.items(), key=lambda kv: kv[1]):
    if a in centres and b in centres:
        edges.append([round(centres[a][0], 1), round(centres[a][1], 1), round(centres[b][0], 1), round(centres[b][1], 1), c])

# each chapter verse is one dot of its book's cluster, picked by a hash of its id (distinct within a book)
vdot, taken = {}, set()
for ch in CH:
    for v in ch['verses']:
        bd = book_dots.get(v['book'])
        if not bd:
            fail('%s: book %s not in the constellation' % (v['id'], v['book']))
            continue
        k = zlib.crc32(v['id'].encode()) % len(bd)
        while (v['book'], k) in taken:
            k = (k + 1) % len(bd)
        taken.add((v['book'], k))
        vdot[v['id']] = list(bd[k])

# ---------------------------------------------------------------------------------------------------------
# 4. Images: generated stills -> cut-out -> web; then a tight crop for this page.
# ---------------------------------------------------------------------------------------------------------
# visual-weight correction per asset (1 = the default size for its outline); thin objects need a little more
WEIGHT = {'V4-staff': 1.15, 'V4-bamboo-flute': 1.05, 'V4-exo-brace': 1.08, '02-T': 1.08, '02-N': 0.96,
          'V4-wave': 0.94}
# chroma-key thresholds per asset where the generated screen is duller than #00FF00 (cutout_green lo hi)
KEY = {'V4-bamboo-flute': ['15', '50']}


def run(args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


used = []
for ch in CH:
    for d in ch['verses'] + [ch['forward']['then'], ch['forward']['future']]:
        a = aid(d)
        if a and a not in used:
            used.append(a)
IMG.mkdir(exist_ok=True)
sprite_info, MISSING = {}, []
for a in used:
    src, png, web = ASSETS / 'src' / (a + '.jpg'), ASSETS / (a + '.png'), ASSETS / 'web' / (a + '.webp')
    if src.exists() and (not png.exists() or png.stat().st_mtime < src.stat().st_mtime):
        run([str(V3 / 'cutout_green'), str(src), str(png)] + KEY.get(a, []))
    if png.exists() and (not web.exists() or web.stat().st_mtime < png.stat().st_mtime):
        run(['cwebp', '-quiet', '-q', '84', '-alpha_q', '90', '-m', '6', '-resize', '640', '0', str(png), '-o', str(web)])
    if not png.exists():
        MISSING.append(a)
        sprite_info[a] = {'src': '', 'w': 100, 'h': 130, 'k': 1, 'missing': 1}
        continue
    st = json.loads(subprocess.run([str(V3 / 'spritestat'), str(png)], check=True, capture_output=True, text=True).stdout.splitlines()[0])
    x0, y0, x1, y1 = st['bbox']
    pad = 4
    x0, y0, x1, y1 = max(0, x0 - pad), max(0, y0 - pad), min(st['w'], x1 + pad), min(st['h'], y1 + 1)
    # crops at most 760 px tall: the stage never draws an object taller than that
    dst = IMG / (a + '.webp')
    if not dst.exists() or dst.stat().st_mtime < png.stat().st_mtime or os.environ.get('V4_RECROP'):
        hh = y1 - y0
        resize = ['-resize', '0', '760'] if hh > 760 else []
        run(['cwebp', '-quiet', '-q', '84', '-alpha_q', '90', '-m', '6', '-crop', str(x0), str(y0), str(x1 - x0), str(hh)]
            + resize + [str(png), '-o', str(dst)])
    sprite_info[a] = {'src': 'img/%s.webp' % a, 'w': x1 - x0, 'h': y1 - y0, 'k': WEIGHT.get(a, 1.0)}
if MISSING:
    (WARN if ALLOW_MISSING else FAIL).append('images not made yet: ' + ', '.join(MISSING))

# scroll-scrubbed Veo clips where a forward morph has one (frames-to-video between the same two stills)
CLIPS = {   # chapter id -> clip file, the clip seconds to scrub, and how the square keyed frame sits on the stage
    'aram': {'src': 'assets/video/V5.mp4', 'c0': 0.0, 'c1': 7.9, 'size': 1.0, 'drop': 0.10},
    'ullam': {'src': 'assets/video/V1.mp4', 'c0': 0.0, 'c1': 4.6, 'size': 1.0, 'drop': 0.10},
    'aivu': {'src': 'assets/video/V4.mp4', 'c0': 0.0, 'c1': 7.9, 'size': 1.0, 'drop': 0.10},
}
for c in CLIPS.values():
    if not (NILAI / c['src']).exists():
        fail('clip %s missing' % c['src'])

# ---------------------------------------------------------------------------------------------------------
# 5. Timeline. Units: 1 unit = one viewport of scroll. Every beat holds its settled state for >= 30%.
# ---------------------------------------------------------------------------------------------------------
beats = []
t = 0.0


def beat(bid, kind, ln, st, ci=None):
    global t
    if st > 0.70:
        fail('beat %s holds less than 30%%' % bid)
    b = {'id': bid, 'kind': kind, 'start': round(t, 4), 'len': ln, 'settle': st}
    if ci is not None:
        b['ch'] = ci
    beats.append(b)
    t += ln
    return b


beat('G0', 'graph', 1.5, 0.56)
beat('G1', 'graph', 1.3, 0.52)
beat('G2', 'graph', 1.3, 0.46)
for ci, ch in enumerate(CH):
    p = 'c%d' % ci
    beat(p + 'T', 'title', 1.4, 0.56, ci)
    beat(p + 'V1', 'verse', 1.3, 0.36, ci)
    beat(p + 'L1', 'link', 1.7, 0.66, ci)
    beat(p + 'V2', 'verse', 1.3, 0.32, ci)
    beat(p + 'L2', 'link', 1.7, 0.68, ci)
    beat(p + 'V3', 'verse', 1.3, 0.32, ci)
    beat(p + 'F', 'imagined', 2.0, 0.66, ci)
beat('Z', 'graph', 1.8, 0.56)
TOTAL = round(t, 4)
B = {b['id']: b for b in beats}


def at(bid, f):
    b = B[bid]
    return round(b['start'] + f * b['len'], 4)


C_, LT, RT = 0.5, 0.27, 0.73
S = 0.72
inst = {}      # instance id -> {asset, cap, imag}
tracks = {}    # instance id -> [[T, x, scale, rise]]
threads, morphs, teach = [], [], {}
chapters_js = []


def put(iid, *kf):
    tracks.setdefault(iid, []).extend([list(k) for k in kf])


for ci, ch in enumerate(CH):
    p = 'c%d' % ci
    nxt = ('c%dT' % (ci + 1)) if ci + 1 < len(CH) else 'Z'
    vids = [v['id'] for v in ch['verses']]
    I = {}
    for k, v in enumerate(ch['verses']):
        I[v['id']] = '%s_v%d' % (p, k + 1)
        inst[I[v['id']]] = {'asset': aid(v), 'cap': v['id']}
    v1, v2, v3 = (I[x] for x in vids)
    L1, L2 = ch['links']

    def side(L, first):
        """Slot of `first` for this link: the link's source sits on the left (both ends read left to right)."""
        td = L['true_direction']
        if td['symmetric']:
            return LT
        return LT if td['s'] == first else RT

    # verse 1 rises, then link 1 takes it aside and raises verse 2 opposite
    s1 = side(L1, vids[0])
    s2 = RT if s1 == LT else LT
    put(v1, (at(p + 'V1', .18), C_, 1, 0), (at(p + 'V1', .36), C_, 1, 1), (at(p + 'L1', 0), C_, 1, 1),
        (at(p + 'L1', .22), s1, S, 1), (at(p + 'V2', 0), s1, S, 1), (at(p + 'V2', .20), s1, S, 0))
    put(v2, (at(p + 'L1', .10), s2, S, 0), (at(p + 'L1', .32), s2, S, 1), (at(p + 'V2', 0), s2, S, 1),
        (at(p + 'V2', .28), C_, 1, 1), (at(p + 'L2', 0), C_, 1, 1))
    threads.append({'id': p + 'L1', 'a': I[L1['from']], 'b': I[L1['to']], 'sym': int(L1['true_direction']['symmetric']),
                    's': I[L1['true_direction']['s']] if not L1['true_direction']['symmetric'] else None,
                    'd0': at(p + 'L1', .32), 'd1': at(p + 'L1', .64), 'f0': at(p + 'V2', 0), 'f1': at(p + 'V2', .14)})
    # link 2 joins verse 3 to whichever earlier verse it touches (the anchor)
    anchor = L2['from'] if L2['to'] == vids[2] else L2['to']
    sa = side(L2, anchor)
    s3 = RT if sa == LT else LT
    if anchor == vids[1]:
        put(v2, (at(p + 'L2', .22), sa, S, 1), (at(p + 'V3', 0), sa, S, 1), (at(p + 'V3', .20), sa, S, 0))
        put(v3, (at(p + 'L2', .10), s3, S, 0), (at(p + 'L2', .32), s3, S, 1))
        d0, d1 = at(p + 'L2', .32), at(p + 'L2', .64)
    else:   # verse 2 steps down and verse 1 comes back
        put(v2, (at(p + 'L2', .18), C_, 1, 0))
        put(v1, (at(p + 'L2', .22), sa, S, 0), (at(p + 'L2', .40), sa, S, 1), (at(p + 'V3', 0), sa, S, 1),
            (at(p + 'V3', .20), sa, S, 0))
        put(v3, (at(p + 'L2', .22), s3, S, 0), (at(p + 'L2', .40), s3, S, 1))
        d0, d1 = at(p + 'L2', .42), at(p + 'L2', .66)
    put(v3, (at(p + 'V3', 0), s3, S, 1), (at(p + 'V3', .28), C_, 1, 1))
    threads.append({'id': p + 'L2', 'a': I[L2['from']], 'b': I[L2['to']], 'sym': int(L2['true_direction']['symmetric']),
                    's': I[L2['true_direction']['s']] if not L2['true_direction']['symmetric'] else None,
                    'd0': d0, 'd1': d1, 'f0': at(p + 'V3', 0), 'f1': at(p + 'V3', .14)})
    for k, L in ((1, L1), (2, L2)):
        teach[p + 'L%d' % k] = {'head': '%s · %s' % ('teaches' if L['text_field'] == 'teaches' else 'the link’s note', L['type']),
                                'text': L['text']}
    # the imagined beat: the "then" object rises (or verse 3 stays, when it is the same object) and turns into its future
    F = ch['forward']
    ta, fa = aid(F['then']), aid(F['future'])
    if ta == inst[v3]['asset']:
        then = v3
        put(v3, (at(p + 'F', .30), C_, 1, 1))
    else:
        then = p + '_then'
        inst[then] = {'asset': ta, 'cap': 'கற்பனை · imagined', 'imag': 1}
        put(v3, (at(p + 'F', 0), C_, 1, 1), (at(p + 'F', .14), C_, 1, 0))
        put(then, (at(p + 'F', .12), C_, 1, 0), (at(p + 'F', .28), C_, 1, 1))
    fut = p + '_future'
    inst[fut] = {'asset': fa, 'cap': 'கற்பனை · imagined', 'imag': 1}
    put(then, (at(nxt, 0), C_, 1, 1), (at(nxt, .02), C_, 1, 0))
    put(fut, (at(p + 'F', .30), C_, 1, 1), (at(nxt, 0), C_, 1, 1), (at(nxt, .14), C_, 1, 0))
    m = {'then': then, 'fut': fut, 'a': at(p + 'F', .32), 'b': at(p + 'F', .62)}
    if ch['id'] in CLIPS:
        m['clip'] = CLIPS[ch['id']]
    morphs.append(m)
    # graph camera for the chapter's title beat
    pts = [vdot[x] for x in vids]
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    chapters_js.append({
        'id': ch['id'], 'ta': ch['tamil'], 'name': ch['name'], 'sub': ch['subtitle'],
        'acc': ch['accent'], 'start': B[p + 'T']['start'],
        'dots': {x: vdot[x] for x in vids},
        'route': [[L1['from'], L1['to']], [L2['from'], L2['to']]],
        'box': [min(xs), min(ys), max(xs), max(ys)],
        'g': {'in': [at(p + 'T', 0), at(p + 'T', .12)], 'zoom': [at(p + 'T', .12), at(p + 'T', .46)],
              'route': [at(p + 'T', .36), at(p + 'T', .56)], 'out': [at(p + 'V1', 0), at(p + 'V1', .16)]},
    })

# keyframes must run forward in time
for iid, k in tracks.items():
    k.sort(key=lambda r: r[0])
    for a, b in zip(k, k[1:]):
        if b[0] < a[0]:
            fail('track %s runs backwards' % iid)

graph_tl = {'dots': [at('G0', .04), at('G0', .52)], 'edges': [at('G1', 0), at('G1', .50)],
            'flash': [at('G2', .06), at('G2', .40)], 'intro_out': B['c0T']['start'],
            'close': [at('Z', 0), at('Z', .16)], 'close_route': [at('Z', .18), at('Z', .52)]}

# ---------------------------------------------------------------------------------------------------------
# 6. Palette, with a contrast check (text must reach 4.5:1); chapter accents are darkened until they pass.
# ---------------------------------------------------------------------------------------------------------
PAL = {'wall': '#e6e1d8', 'floor': '#d5ccbe', 'col': '#efebe4', 'ink': '#211e1a', 'ink2': '#4d463d',
       'accent': '#6c4605', 'thread': '#b8862a', 'line': '#c3b8a6'}


def lum(hx):
    c = [int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def darken(hx, f):
    return '#' + ''.join('%02x' % int(int(hx[i:i + 2], 16) * f) for i in (1, 3, 5))


CONTRAST = {}
for fg in ('ink', 'ink2', 'accent'):
    for bg in ('wall', 'floor', 'col'):
        c = contrast(PAL[fg], PAL[bg])
        CONTRAST['%s/%s' % (fg, bg)] = round(c, 2)
        if c < 4.5:
            fail('contrast %s on %s is %.2f' % (fg, bg, c))
for c in chapters_js:
    acc = c['acc']
    while min(contrast(acc, PAL['col']), contrast(acc, PAL['wall'])) < 4.6:
        acc = darken(acc, 0.92)
    c['acc'] = acc
    CONTRAST['accent ' + c['id']] = round(min(contrast(acc, PAL['col']), contrast(acc, PAL['wall'])), 2)

# ---------------------------------------------------------------------------------------------------------
# 7. Text column cards.
# ---------------------------------------------------------------------------------------------------------
E = html.escape


def tamil_block(v):
    out, prev = [], None
    for ln in v['lines']:
        if prev is not None and ln['n'] != prev + 1:
            out.append('<span class="gap" aria-hidden="true">…</span>')
        out.append('<span class="tl">%s</span>' % E(ln['ta']))
        prev = ln['n']
    a, b = v['lines_shown_of']
    ns = [ln['n'] for ln in v['lines']]
    meta = ''
    if (b - a + 1) != len(ns):
        rngs, s0 = [], ns[0]
        for x, y in zip(ns, ns[1:] + [None]):
            if y != x + 1:
                rngs.append(str(s0) if s0 == x else '%d–%d' % (s0, x))
                s0 = y
        meta = '<p class="meta">line%s %s of %d–%d</p>' % ('s' if len(ns) > 1 else '', ', '.join(rngs), a, b)
    return '<p class="ta" lang="ta">%s</p>%s' % (''.join(out), meta)


def verse_card(bid, ch, v, n):
    flag = ' <span class="flag">the graph marks this reading uncertain</span>' if v.get('uncertain') else ''
    return ('<article class="card" data-beat="%s"><p class="kick"><span lang="ta">%s</span> · verse %d of 3</p>'
            '<p class="src"><span lang="ta">%s</span> · %s</p>%s<p class="lab">the graph’s reading</p>'
            '<p class="rd clamp">%s</p><button class="more" type="button">read all</button>'
            '<p class="cite">%s%s</p></article>') % (bid, E(ch['tamil']), n, E(v['label_ta']), E(v['label']),
                                                    tamil_block(v), E(v['reading']), E(v['id']), flag)


def link_card(bid, ch, L, n):
    td = L['true_direction']
    arrow = '↔' if td['symmetric'] else '→'
    a, b = (L['from'], L['to']) if td['symmetric'] else (td['s'], td['o'])
    return ('<article class="card" data-beat="%s"><p class="kick"><span lang="ta">%s</span> · link %d of 2 · '
            '<b>%s</b> · graded sound</p><p class="ids">%s <span class="arr">%s</span> %s</p>'
            '<p class="rd sm">The thread on the stage writes the link’s %s, word by word, as it is drawn%s.</p>'
            '<p class="cite">kg/groups/bridges.jsonl · %s</p></article>') % (
        bid, E(ch['tamil']), n, E(L['type']), E(a), arrow, E(b),
        'teaching' if L['text_field'] == 'teaches' else 'note',
        ' from both ends, since this link runs both ways' if td['symmetric'] else ' from the verse that does the work',
        E(td['reads']))


cards = [
    ('<article class="card" data-beat="G0"><p class="kick">a walk through the graph</p>'
     '<p class="big">%d books. %s verses.</p><p class="rd">Each cluster is one book, its dots a sample of its verses, '
     'set in the nine groups the graph keeps.</p><p class="cite">kg/groups/index.json</p></article>') % (N_BOOKS, '{:,}'.format(N_VERSES)),
    ('<article class="card" data-beat="G1"><p class="kick">a walk through the graph</p>'
     '<p class="big">%s sound bridges.</p><p class="rd">Each thread is a link between books in different groups that '
     'the blind grading kept as sound; brighter threads carry more links.</p><p class="cite">kg/groups/bridges.jsonl</p></article>') % '{:,}'.format(N_SOUND),
    ('<article class="card" data-beat="G2"><p class="kick">a walk through the graph</p>'
     '<p class="big">Thirteen walks.</p><p class="rd">One for each thing the poems keep returning to. Each walk is three '
     'verses joined by two sound links, and ends in one beat we imagine forward, labelled so.</p>'
     '<p class="tamlist" lang="ta">%s</p><p class="cite">site/nilai/v4/chapters.json · checked against kg/</p></article>')
    % ' · '.join(E(c['tamil']) for c in CH),
]
for ci, ch in enumerate(CH):
    p = 'c%d' % ci
    acc = chapters_js[ci]['acc']
    vs = ch['verses']
    cards.append(('<article class="card ctitle" data-beat="%sT" style="--acc:%s"><p class="kick">chapter %d of 13</p>'
                  '<p class="cta" lang="ta">%s</p><p class="big">%s</p><p class="rd"><i>%s</i></p>'
                  '<ol class="path">%s</ol><p class="cite">three verses · two sound links</p></article>') % (
        p, acc, ci + 1, E(ch['tamil']), E(ch['name']), E(ch['subtitle']),
        ''.join('<li><span lang="ta">%s</span></li>' % E(v['label_ta']) for v in vs)))
    cards.append(verse_card(p + 'V1', ch, vs[0], 1).replace('class="card"', 'class="card" style="--acc:%s"' % acc, 1))
    cards.append(link_card(p + 'L1', ch, ch['links'][0], 1).replace('class="card"', 'class="card" style="--acc:%s"' % acc, 1))
    cards.append(verse_card(p + 'V2', ch, vs[1], 2).replace('class="card"', 'class="card" style="--acc:%s"' % acc, 1))
    cards.append(link_card(p + 'L2', ch, ch['links'][1], 2).replace('class="card"', 'class="card" style="--acc:%s"' % acc, 1))
    cards.append(verse_card(p + 'V3', ch, vs[2], 3).replace('class="card"', 'class="card" style="--acc:%s"' % acc, 1))
    F = ch['forward']
    cards.append(('<article class="card" data-beat="%sF" style="--acc:%s"><p class="kick imag"><span lang="ta">கற்பனை</span> · imagined</p>'
                  '<p class="big fw">%s</p><p class="rd sm"><i>%s</i></p>'
                  '<p class="cite">not from the corpus · carried forward from this chapter’s two links</p></article>') % (
        p, acc, E(F['text']), E(F['transformation'][:1].upper() + F['transformation'][1:] + '.')))
cards.append(('<article class="card" data-beat="Z"><p class="kick">the walks</p>'
              '<p class="big">Thirteen walks, 39 verses, 26 sound links.</p><p class="rd">%d books from all %d groups, '
              'lit as paths through %s sound bridges. Every Tamil line and reading on these pages is the graph’s own; '
              'only the thirteen imagined beats are ours.</p><p class="cite">kg/groups/bridges.jsonl · site/nilai/v4/chapters.json</p></article>')
             % (N_CH_BOOKS, N_CH_GROUPS, '{:,}'.format(N_SOUND)))
if len(cards) != len(beats):
    fail('%d cards for %d beats' % (len(cards), len(beats)))

if FAIL:
    print('BUILD FAILED:')
    for m in FAIL:
        print('  -', m)
    sys.exit(1)
for m in WARN:
    print('warning:', m)

DATA = {
    'beats': beats, 'total': TOTAL, 'tracks': tracks, 'inst': inst, 'threads': threads, 'morphs': morphs,
    'graph': graph_tl, 'chapters': chapters_js, 'sprites': sprite_info, 'teach': teach,
    'dots': dots, 'edges': edges, 'labels': labels, 'slots': {'C': C_, 'L': LT, 'R': RT, 'S': S},
}

CSS = (HERE / 'v4.css').read_text(encoding='utf-8')
for k, v in PAL.items():
    CSS = CSS.replace('$' + k, v)
JS = (HERE / 'v4.js').read_text(encoding='utf-8')
menu = ''.join('<li><button type="button" data-ch="%d"><span lang="ta">%s</span> <span class="mn">%s</span></button></li>'
               % (i, E(c['tamil']), E(c['subtitle'])) for i, c in enumerate(CH))

page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nilai · walks through the graph</title>
<meta name="description" content="Nilai v4: thirteen walks through a Tamil literary knowledge graph. Every scene is a corpus verse, every transition a graded sound link, and one imagined beat per walk looks forward.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Tamil:wght@400;600&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<style>%(css)s</style>
</head>
<body>
<div id="app">
  <section id="col" aria-live="polite">
    <header id="hd">
      <p class="brand"><span lang="ta">நிலை</span> · Nilai <span id="chn"></span></p>
      <h1 id="h1"><span lang="ta">நிலை</span> · walks through the graph</h1>
      <div id="btns"><button id="menuB" type="button" aria-expanded="false" aria-controls="menu">Chapters</button><button id="watch" type="button" aria-pressed="false">Watch</button></div>
    </header>
    <div id="cards">%(cards)s</div>
  </section>
  <section id="stage" aria-label="Stage">
    <div id="wall"></div>
    <div id="floor"></div>
    <svg id="graph" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The graph: the books as clusters of dots, sound bridges as threads"></svg>
    <div id="shadows"></div>
    <div id="objs"></div>
    <div id="seam"></div>
    <div id="caps"></div>
    <svg id="threads" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"></svg>
    <div id="teach" aria-live="off"></div>
  </section>
</div>
<nav id="menu" hidden><ol>%(menu)s</ol></nav>
<div id="sheet" hidden role="dialog" aria-modal="true" aria-label="Full reading"><div id="sheetIn"></div><button id="sheetX" type="button">Close</button></div>
<div id="spacer"></div>
<script id="data" type="application/json">%(data)s</script>
<script>%(js)s</script>
</body>
</html>
''' % {'css': CSS, 'cards': '\n'.join(cards), 'menu': menu,
       'data': json.dumps(DATA, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'), 'js': JS}

out = HERE / 'index.html'
out.write_text(page, encoding='utf-8')
print('wrote %s (%d bytes); %d beats, %.1f viewports; %d books, %d verses, %d sound bridges; %d sprites (%d missing); min contrast %s'
      % (out.relative_to(REPO), out.stat().st_size, len(beats), TOTAL, N_BOOKS, N_VERSES, N_SOUND, len(sprite_info),
         len(MISSING), min(CONTRAST.values())))
