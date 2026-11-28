"""Nilai v4 prototype: one chapter, "a walk through the graph".

Run:  python3 -I site/nilai/v4/build.py
Writes site/nilai/v4/index.html and site/nilai/v4/img/*.webp.

THE GRAPH IS THE SCRIPT. Every verse scene is a real verse (its Tamil, copied verbatim and checked here
against kg/core) with the graph's own English reading; every transition between verses is a graded sound link,
whose teaches sentence writes along a gold thread while its note shows in the text column. Nothing on screen
is a modern translation or commentary; the one invented beat is labelled கற்பனை · imagined.

Stdlib only. Images: site/nilai/assets/src/<id>.jpg -> build/v3/cutout_green -> assets/<id>.png ->
assets/web/<id>.webp (as in v3), and a tight crop of each cut-out for this page in v4/img/.
"""
import html
import json
import math
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NILAI = HERE.parent
REPO = NILAI.parent.parent
KG = REPO / 'kg'
ASSETS = NILAI / 'assets'
V3 = NILAI / 'build' / 'v3'
IMG = HERE / 'img'

FAIL = []


def fail(msg):
    FAIL.append(msg)


def jsonl(path):
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def find(path, pred):
    for d in jsonl(path):
        if pred(d):
            return d
    return None


# ---------------------------------------------------------------------------------------------------------
# 1. The verses. Tamil copied verbatim from kg/core; the build fails if the corpus and this copy disagree.
# ---------------------------------------------------------------------------------------------------------
TAMIL = {
    'siddhar:1458': [
        'நட்டகல்லைத் தெய்வம் என்று நாலுபுட்பம் சாத்தியே',
        'சுற்றிவந்து முணமுணேன்று சொல்லுமந்திரம் ஏதடா',
        'நட்டகல்லும் பேசுமோ நாதன்உள் இருக்கையில்!',
        'சுட்டசட்டி சட்டுவம் கறிச்சுவை அறியுமோ?',
    ],
    'manimekalai:21:112-129': [
        '"அன்று" என்று அவன் முன் அயர்ந்து ஒழிவாயலை',
        '"தீவினை உறுதலும் செத்தோர் பிறத்தலும்',
        'வாயே" என்று மயக்கு ஒழி மடவாய்',
        'வழு அறு மரனும் மண்ணும் கல்லும்',
        'எழுதிய பாவையும் பேசா என்பது',
        'அறிதலும் அறிதியோ? அறியாய்கொல்லோ?',
        'அறியாய் ஆயின் ஆங்கு அது கேளாய்!',
        'முடித்து வரு சிறப்பின் மூதூர் யாங்கணும்',
        'கொடித் தேர் வீதியும் தேவர் கோட்டமும்',
        'முது மர இடங்களும் முது நீர்த் துறைகளும்',
        'பொதியிலும் மன்றமும் பொருந்துபு நாடி',
        'காப்பு உடை மா நகர்க் காவலும் கண்ணி',
        'யாப்பு உடைத்தாக அறிந்தோர் வலித்து',
        'மண்ணினும் கல்லினும் மரத்தினும் சுவரினும்',
        'கண்ணிய தெய்வதம் காட்டுநர் வகுக்க',
        'ஆங்கு அத் தெய்வதம் அவ் இடம் நீங்கா',
        'ஊன் கண்ணினார்கட்கு உற்றதை உரைக்கும்',
        'என் திறம் கேட்டியோ இளங் கொடி நல்லாய்!',
    ],
    'civaka_cintamani:2058': [
        'மட்டவிழ் கோதை பெற்றாய் மனமகிழ் காத லானை',
        'யிட்டிடை நோவ நில்லா தெழுகென வேந்த றோழன்',
        'பட்டிமை யுரைத்த தோராள் பரவிய தெய்வந் தான்வாய்',
        'விட்டுரைத் திட்ட தென்றே வேற்கணாள் பரவி மீண்டாள்.',
    ],
}
# Manimekalai's unit is 18 lines; the scene shows the lines the link's audit cites (115-116, 125-128), verbatim.
EXCERPT = {'manimekalai:21:112-129': [(115, 116), (125, 128)]}
# On a phone the text band shows only the four lines the audit quotes (115-116, 127-128).
EXCERPT_WIDE_ONLY = {'manimekalai:21:112-129': [(125, 126)]}
EXCERPT_NARROW = {'manimekalai:21:112-129': [(115, 116), (127, 128)]}

core = {}
r = find(KG / 'core' / 'siddhar.jsonl', lambda d: d.get('seq') == 1458)
core['siddhar:1458'] = r
core['manimekalai:21:112-129'] = find(KG / 'core' / 'manimekalai_units.jsonl', lambda d: d.get('id') == 'manimekalai:21:112-129')
core['civaka_cintamani:2058'] = find(KG / 'core' / 'civaka_cintamani.jsonl', lambda d: d.get('id') == 'civaka_cintamani:2058')
for vid, lines in TAMIL.items():
    rec = core.get(vid)
    if not rec:
        fail('%s: not found in kg/core' % vid)
    elif rec['tamil'] != lines:
        fail('%s: Tamil in build.py differs from kg/core' % vid)

# graph nodes (readings)
nodes = {}
nodes['siddhar:1458'] = find(KG / 'siddhar' / 'nodes.jsonl', lambda d: d.get('id') == 'siddhar:1458')
for d in jsonl(KG / 'groups' / 'epics_great' / 'nodes.jsonl'):
    if d.get('id') in ('manimekalai:21:112-129', 'civaka_cintamani:2058'):
        nodes[d['id']] = d
for vid in TAMIL:
    n = nodes.get(vid)
    if not n or not n.get('reading'):
        fail('%s: no reading in the graph' % vid)
    elif n.get('tamil') != TAMIL[vid]:
        fail('%s: graph node Tamil differs from kg/core' % vid)
# cross-check readings against the theme marks where the marks key them
mm = json.load(open(KG / 'themes' / 'manimekalai' / 'ch022.json', encoding='utf-8'))['verses'].get('manimekalai:21:112-129', {})
if mm.get('reading') != nodes['manimekalai:21:112-129']['reading']:
    fail('manimekalai:21:112-129: reading differs between themes/ch022 and the group graph')
cc = json.load(open(KG / 'themes' / 'civaka_cintamani' / 'ch088.json', encoding='utf-8'))['verses'].get('2058', {})
if cc.get('reading') and cc['reading'] != nodes['civaka_cintamani:2058']['reading']:
    fail('civaka_cintamani:2058: reading differs between themes/ch088 and the group graph')

# ---------------------------------------------------------------------------------------------------------
# 2. The links, verbatim from bridges.jsonl, confirmed sound in all_link_audit.json.
# ---------------------------------------------------------------------------------------------------------
bridges = list(jsonl(KG / 'groups' / 'bridges.jsonl'))
audit = json.load(open(KG / 'groups' / 'all_link_audit.json', encoding='utf-8'))['links']


def link(s, o, typ):
    b = next((x for x in bridges if x['s'] == s and x['o'] == o and x['type'] == typ), None)
    if not b:
        fail('link %s -> %s (%s) not in bridges.jsonl' % (s, o, typ))
        return {}
    if b['grade'] != 'sound':
        fail('link %s -> %s graded %s, not sound' % (s, o, b['grade']))
    a = next((x for x in audit if x.get('a') == s and x.get('b') == o and x.get('type') == typ), None)
    if not a or a.get('grade') != 'sound':
        fail('link %s -> %s not graded sound in all_link_audit.json' % (s, o))
    if not b.get('teaches') or not b.get('note'):
        fail('link %s -> %s lacks teaches or note' % (s, o))
    return b


L1 = link('manimekalai:21:112-129', 'siddhar:1458', 'tension')
L2 = link('civaka_cintamani:2058', 'siddhar:1458', 'develops')
if L1.get('teaches') != ('Both start from the same premise, that the stone itself is mute; they part over whether a power '
                         'can be lodged in it, the epic answering yes for guardian deities of a city and the Siddhar '
                         'answering that the Lord is found only within.'):
    fail('L1 teaches is not the sentence the brief quotes')
if L2.get('teaches') != ('The Siddhar\'s scorn assumes the stone is silent; the epic shows a voice supplied to it by a hidden '
                         'man, so the credulity he mocks can be steered by whoever stands behind the image.'):
    fail('L2 teaches is not the sentence the brief quotes')

# ---------------------------------------------------------------------------------------------------------
# 3. The real numbers, counted from the graph.
# ---------------------------------------------------------------------------------------------------------
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
if not all(x['group_a'] != x['group_b'] for x in bridges):
    fail('bridges.jsonl holds a within-group link; the caption calls them links between groups')
N_SID_SOUND = sum(1 for x in SOUND if 'siddhar:1458' in (x['s'], x['o']))

# ---------------------------------------------------------------------------------------------------------
# 4. Constellation layout: 40 books as clusters of dots, grouped as the graph groups them.
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
special = {}
SPECIAL_BOOK = {'siddhar': 'siddhar:1458', 'manimekalai': 'manimekalai:21:112-129', 'civaka_cintamani': 'civaka_cintamani:2058'}
centres = {}
for i, b in enumerate(book_list):
    rr = R + (14 if i % 2 else -14)
    cx = 500 + scale * rr * math.cos(b['a'])
    cy = 500 + scale * rr * math.sin(b['a'])
    centres[b['b']] = (cx, cy)
    gi = GROUP_ORDER.index(b['g'])
    for k in range(b['nd']):
        rk = scale * b['rb'] * 0.92 * math.sqrt((k + 0.5) / b['nd'])
        th = k * 2.399963 + i
        x, y = cx + rk * math.cos(th), cy + rk * math.sin(th)
        dots.append([round(x, 1), round(y, 1), gi])
    if b['b'] in SPECIAL_BOOK:
        special[SPECIAL_BOOK[b['b']]] = [round(cx, 1), round(cy, 1)]
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

# ---------------------------------------------------------------------------------------------------------
# 5. Images: generated stills -> cut-out -> web; then a tight crop for this page.
# ---------------------------------------------------------------------------------------------------------
SPRITES = {   # page id -> (asset id, height factor relative to the hero height)
    'stone': ('18-T', 1.0),
    'pillar': ('V4-pillar', 1.0),
    'shrine': ('V4-shrine', 1.0),
    'speaker': ('V4-speaker', 1.0),
    'hands': ('V4-hands', 1.08),
}


def run(args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


IMG.mkdir(exist_ok=True)
sprite_info = {}
for sid, (aid, k) in SPRITES.items():
    src, png, web = ASSETS / 'src' / (aid + '.jpg'), ASSETS / (aid + '.png'), ASSETS / 'web' / (aid + '.webp')
    if src.exists() and (not png.exists() or png.stat().st_mtime < src.stat().st_mtime):
        run([str(V3 / 'cutout_green'), str(src), str(png)])
    if png.exists() and (not web.exists() or web.stat().st_mtime < png.stat().st_mtime):
        run(['cwebp', '-quiet', '-q', '84', '-alpha_q', '90', '-m', '6', '-resize', '640', '0', str(png), '-o', str(web)])
    if not png.exists():
        fail('image %s missing (%s)' % (sid, png.relative_to(REPO)))
        continue
    st = json.loads(subprocess.run([str(V3 / 'spritestat'), str(png)], check=True, capture_output=True, text=True).stdout.splitlines()[0])
    x0, y0, x1, y1 = st['bbox']
    pad = 4
    x0, y0, x1, y1 = max(0, x0 - pad), max(0, y0 - pad), min(st['w'], x1 + pad), min(st['h'], y1 + 1)
    dst = IMG / (sid + '.webp')
    if not dst.exists() or dst.stat().st_mtime < png.stat().st_mtime or os.environ.get('V4_RECROP'):
        run(['cwebp', '-quiet', '-q', '86', '-alpha_q', '92', '-m', '6', '-crop', str(x0), str(y0), str(x1 - x0), str(y1 - y0), str(png), '-o', str(dst)])
    sprite_info[sid] = {'src': 'img/%s.webp' % sid, 'w': x1 - x0, 'h': y1 - y0, 'k': k}

# ---------------------------------------------------------------------------------------------------------
# 6. Timeline. Units: 1 unit = one viewport of scroll. Every beat holds its settled state for >= 30%.
# ---------------------------------------------------------------------------------------------------------
BEATS = [  # id, kind, length, settle (fraction at which the stage is settled and the text appears)
    ('G0', 'graph', 1.0, 0.00),
    ('G1', 'graph', 1.0, 0.50),
    ('G2', 'graph', 1.2, 0.60),
    ('V1', 'verse', 1.4, 0.36),
    ('L1', 'link', 1.8, 0.66),
    ('V2', 'verse', 1.4, 0.32),
    ('L2', 'link', 1.8, 0.66),
    ('V3', 'verse', 1.4, 0.32),
    ('I1', 'imagined', 1.6, 0.64),
    ('I2', 'imagined', 1.4, 0.56),
    ('C', 'graph', 1.6, 0.62),
]
beats, t = [], 0.0
for bid, kind, ln, st in BEATS:
    if st > 0.70:
        fail('beat %s holds less than 30%%' % bid)
    beats.append({'id': bid, 'kind': kind, 'start': round(t, 4), 'len': ln, 'settle': st})
    t += ln
TOTAL = round(t, 4)
B = {b['id']: b for b in beats}


def at(bid, f):
    b = B[bid]
    return round(b['start'] + f * b['len'], 4)


C_, LT, RT = 0.5, 0.27, 0.73
S = 0.72
# keyframes: [T, x, scale, rise]   rise 0 = sunk below the floor line, 1 = standing on it
tracks = {
    'stone': [[at('V1', .18), C_, 1, 0], [at('V1', .36), C_, 1, 1],
              [at('L1', 0), C_, 1, 1], [at('L1', .22), LT, S, 1],
              [at('V2', 0), LT, S, 1], [at('V2', .20), LT, S, 0],
              [at('L2', .32), LT, S, 0], [at('L2', .46), LT, S, 1],
              [at('V3', 0), LT, S, 1], [at('V3', .20), LT, S, 0],
              [at('I1', .14), C_, 1, 0], [at('I1', .28), C_, 1, 1],
              [at('I1', .30), C_, 1, 1], [at('I1', .40), LT, S, 1],
              [at('I2', 0), LT, S, 1], [at('I2', .16), LT, S, 0]],
    'pillar': [[at('L1', .10), RT, S, 0], [at('L1', .32), RT, S, 1],
               [at('V2', 0), RT, S, 1], [at('V2', .28), C_, 1, 1],
               [at('L2', 0), C_, 1, 1], [at('L2', .18), LT, S, 1], [at('L2', .32), LT, S, 0]],
    'shrine': [[at('L2', .14), RT, S, 0], [at('L2', .32), RT, S, 1],
               [at('V3', 0), RT, S, 1], [at('V3', .28), C_, 1, 1],
               [at('I1', 0), C_, 1, 1], [at('I1', .12), RT, S, 1], [at('I1', .24), RT, S, 0]],
    'speaker': [[at('I1', .40), RT, S, 0], [at('I1', .52), RT, S, 1],
                [at('I2', 0), RT, S, 1], [at('I2', .14), RT, S, 1], [at('I2', .30), C_, 1, 1],
                [at('C', 0), C_, 1, 1], [at('C', .16), C_, 1, 0]],
    'hands': [[at('I2', .30), C_, 1, 0], [at('I2', .52), C_, 1, 1],
              [at('C', 0), C_, 1, 1], [at('C', .16), C_, 1, 0]],
}
threads = [
    {'id': 'L1', 'a': 'stone', 'b': 'pillar', 'd0': at('L1', .32), 'd1': at('L1', .64), 'f0': at('V2', 0), 'f1': at('V2', .14)},
    {'id': 'L2', 'a': 'stone', 'b': 'shrine', 'd0': at('L2', .46), 'd1': at('L2', .64), 'f0': at('V3', 0), 'f1': at('V3', .14)},
    {'id': 'I1', 'a': 'stone', 'b': 'speaker', 'd0': at('I1', .52), 'd1': at('I1', .62), 'f0': at('I2', 0), 'f1': at('I2', .10), 'dash': 1},
]
graph_tl = {
    'dots': [at('G0', 0), at('G0', 0)], 'edges': [at('G1', 0), at('G1', .48)],
    'zoom': [at('G2', 0), at('G2', .58)], 'out': [at('V1', 0), at('V1', .16)],
    'back': [at('C', .11), at('C', .28)], 'unzoom': [at('C', .16), at('C', .52)], 'route': [at('C', .36), at('C', .60)],
}
CAPTION = {'stone': 'siddhar:1458', 'pillar': 'manimekalai:21:112-129', 'shrine': 'civaka_cintamani:2058',
           'speaker': 'கற்பனை · imagined'}

# ---------------------------------------------------------------------------------------------------------
# 7. Palette, with a contrast check (text must reach 4.5:1).
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


CONTRAST = {}
for fg in ('ink', 'ink2', 'accent'):
    for bg in ('wall', 'floor', 'col'):
        c = contrast(PAL[fg], PAL[bg])
        CONTRAST['%s/%s' % (fg, bg)] = round(c, 2)
        if c < 4.5:
            fail('contrast %s on %s is %.2f' % (fg, bg, c))

# ---------------------------------------------------------------------------------------------------------
# 8. Text column cards.
# ---------------------------------------------------------------------------------------------------------
E = html.escape


def tamil_block(vid):
    lines = TAMIL[vid]
    if vid in EXCERPT:
        rec = core[vid]
        out, first = [], True
        for (a, b) in EXCERPT[vid]:
            if not first:
                out.append('<span class="gap" aria-hidden="true">…</span>')
            first = False
            for ln in range(a, b + 1):
                wide = any(x <= ln <= y for (x, y) in EXCERPT_WIDE_ONLY.get(vid, []))
                out.append('<span class="tl%s">%s</span>' % (' wide' if wide else '', E(lines[ln - rec['start']])))
        rng = ', '.join('%d–%d' % ab for ab in EXCERPT[vid])
        rng_n = ', '.join('%d–%d' % ab for ab in EXCERPT_NARROW[vid])
        return ('<p class="ta" lang="ta">%s</p><p class="meta"><span class="wide">lines %s</span><span class="narrow">lines %s</span> of %d–%d</p>'
                % (''.join(out), rng, rng_n, rec['start'], rec['end']))
    return '<p class="ta" lang="ta">%s</p>' % ''.join('<span class="tl">%s</span>' % E(x) for x in lines)


sid_rec = core['siddhar:1458']
VERSE_HEAD = {
    'siddhar:1458': '<span lang="ta">%s %d</span> · <span lang="ta">%s</span> (Sivavakkiyar)' % (
        E(sid_rec['work_title']), sid_rec['number'], E(sid_rec['siddhar'])),
    'manimekalai:21:112-129': '<span lang="ta">மணிமேகலை · %s</span>' % E(nodes['manimekalai:21:112-129']['section']),
    'civaka_cintamani:2058': '<span lang="ta">சீவக சிந்தாமணி %d · %s</span>' % (
        core['civaka_cintamani:2058']['number'], E(core['civaka_cintamani:2058']['section'])),
}


def verse_card(bid, vid, n):
    nd = nodes[vid]
    flag = ' <span class="flag">the graph marks this reading uncertain</span>' if nd.get('uncertain') else ''
    return ('<article class="card" data-beat="%s"><p class="kick">verse %d of 3</p>'
            '<p class="src">%s</p>%s<p class="lab">the graph’s reading</p><p class="rd">%s</p>'
            '<p class="cite">%s%s</p></article>') % (bid, n, VERSE_HEAD[vid], tamil_block(vid), E(nd['reading']), E(vid), flag)


def link_card(bid, L, n, arrow):
    return ('<article class="card" data-beat="%s"><p class="kick">link %d of 2 · <b>%s</b> · graded sound</p>'
            '<p class="ids">%s %s %s</p><p class="lab">the link’s note</p><p class="rd">%s</p>'
            '<p class="cite">kg/groups/bridges.jsonl · teaches written on the thread</p></article>') % (
        bid, n, E(L['type']), E(L['s']), arrow, E(L['o']), E(L['note']))


IMAG1 = 'The stones learned to speak.'
IMAG2 = 'In 2526 we ask the epic’s question: who stands behind the voice?'
cards = [
    ('<article class="card" data-beat="G0"><p class="kick">a walk through the graph</p>'
     '<p class="big">%d books. %s verses.</p><p class="rd">Each cluster is one book, its dots a sample of its verses, '
     'set in the groups the graph keeps.</p><p class="cite">kg/groups/index.json</p></article>') % (N_BOOKS, '{:,}'.format(N_VERSES)),
    ('<article class="card" data-beat="G1"><p class="kick">a walk through the graph</p>'
     '<p class="big">%s sound bridges.</p><p class="rd">Each thread is a link between books in different groups that '
     'the grading kept as sound; brighter threads carry more links.</p><p class="cite">kg/groups/bridges.jsonl</p></article>') % '{:,}'.format(N_SOUND),
    ('<article class="card" data-beat="G2"><p class="kick">a walk through the graph</p>'
     '<p class="big">One verse: siddhar:1458.</p><p class="rd">%d sound bridges touch it. This chapter follows the two '
     'that come from the great epics.</p><p class="cite">siddhar:1458</p></article>') % N_SID_SOUND,
    verse_card('V1', 'siddhar:1458', 1),
    link_card('L1', L1, 1, '↔'),
    verse_card('V2', 'manimekalai:21:112-129', 2),
    link_card('L2', L2, 2, '→'),
    verse_card('V3', 'civaka_cintamani:2058', 3),
    ('<article class="card" data-beat="I1"><p class="kick imag"><span lang="ta">கற்பனை</span> · imagined</p>'
     '<p class="big">%s</p><p class="cite">not from the corpus · carried forward from the develops link</p></article>') % E(IMAG1),
    ('<article class="card" data-beat="I2"><p class="kick imag"><span lang="ta">கற்பனை</span> · imagined</p>'
     '<p class="big">%s %s</p><p class="cite">not from the corpus · carried forward from the develops link</p></article>') % (E(IMAG1), E(IMAG2)),
    ('<article class="card" data-beat="C"><p class="kick">the route</p>'
     '<p class="big">Three verses, two sound links.</p><p class="rd">siddhar:1458, manimekalai:21:112-129 and '
     'civaka_cintamani:2058, lit as one path through %s sound bridges.</p><p class="cite">kg/groups/bridges.jsonl</p></article>') % '{:,}'.format(N_SOUND),
]
TEACH = {
    'L1': {'head': 'teaches · %s' % L1.get('type', ''), 'text': L1.get('teaches', '')},
    'L2': {'head': 'teaches · %s' % L2.get('type', ''), 'text': L2.get('teaches', '')},
}

if FAIL:
    print('BUILD FAILED:')
    for m in FAIL:
        print('  -', m)
    sys.exit(1)

DATA = {
    'beats': beats, 'total': TOTAL, 'tracks': tracks, 'threads': threads, 'graph': graph_tl,
    'sprites': sprite_info, 'captions': CAPTION, 'teach': TEACH,
    'dots': dots, 'edges': edges, 'labels': labels, 'special': special,
    'route': [['siddhar:1458', 'manimekalai:21:112-129'], ['siddhar:1458', 'civaka_cintamani:2058']],
    'slots': {'C': C_, 'L': LT, 'R': RT, 'S': S},
}

CSS = (HERE / 'v4.css').read_text(encoding='utf-8')
for k, v in PAL.items():
    CSS = CSS.replace('$' + k, v)
JS = (HERE / 'v4.js').read_text(encoding='utf-8')

page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nilai · the stone that speaks</title>
<meta name="description" content="Nilai v4 prototype: one chapter walked through the knowledge graph. Every scene is a corpus verse, every transition a graded sound link.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Tamil:wght@400;600&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<style>%(css)s</style>
</head>
<body>
<div id="app">
  <section id="col" aria-live="polite">
    <header id="hd">
      <p class="brand"><span lang="ta">நிலை</span> · Nilai <span class="proto">prototype</span></p>
      <h1><span lang="ta">இறை</span> · the stone that speaks</h1>
      <button id="watch" type="button" aria-pressed="false">Watch</button>
    </header>
    <div id="cards">%(cards)s</div>
  </section>
  <section id="stage" aria-label="Stage">
    <div id="wall"></div>
    <div id="floor"></div>
    <svg id="graph" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The graph: 40 books as clusters of dots, sound bridges as threads"></svg>
    <div id="shadows"></div>
    <div id="objs"></div>
    <div id="caps"></div>
    <svg id="threads" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"></svg>
    <div id="teach" aria-live="off"></div>
  </section>
</div>
<div id="spacer"></div>
<script id="data" type="application/json">%(data)s</script>
<script>%(js)s</script>
</body>
</html>
''' % {'css': CSS, 'cards': '\n'.join(cards), 'data': json.dumps(DATA, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'), 'js': JS}

out = HERE / 'index.html'
out.write_text(page, encoding='utf-8')
print('wrote %s (%d bytes); %d books, %d verses, %d sound bridges; %d dots, %d edges; contrast %s'
      % (out.relative_to(REPO), out.stat().st_size, N_BOOKS, N_VERSES, N_SOUND, len(dots), len(edges),
         min(CONTRAST.values())))
