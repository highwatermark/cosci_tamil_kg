"""Nilai v3.1 stage: generated images, marble and bronze sprites, and the stone architecture behind every scene.

- Assets are discovered at build time in site/nilai/assets/web/<id>.webp, so a rebuild picks up new files.
  Images are referenced as relative files (assets/web/...) and lazy-loaded by reel.js (data-href, set near the scene).
- The two character sheets (K0, M0) are cut into single views here, reproducibly: spritestat finds the figures,
  cwebp crops them from the cut-out PNG into assets/web/K0.side.webp and friends.
- The stage map (v3_shotlist.md section 4.1) names the image for each scene's THEN / NOW / FUTURE stage.
  A stage whose image exists plays as an image on a plinth; a stage without one keeps the SVG drawing, and the
  morph between them cross-dissolves image and SVG.
- Architecture: one of five stone stages per scene, tinted from the script's wall and floor colours. Every stone
  shade is checked against the scene's text, ink and colour (stone counts as background).
"""
import json
import math
import pathlib
import re
import subprocess

import art as AR

HERE = pathlib.Path(__file__).resolve().parent
NILAI = HERE.parents[1]
ASSETS = NILAI / 'assets'
WEB = ASSETS / 'web'
TOOL_SRC = HERE / 'spritestat.swift'
TOOL = HERE / 'spritestat'
CACHE = HERE / 'asset_cache.json'
T = AR.T
FAIL = []          # build.py adds these to its own failures
NOTES = []         # printed by build.py
USED = set()       # every asset file the page references (paths relative to site/nilai)


# ---------------------------------------------------------------- colour maths (same formulas as build.py)
def hx(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def to_hex(c):
    return '#%02X%02X%02X' % tuple(max(0, min(255, round(v))) for v in c)


def lum(h):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4
    r, g, b = hx(h) if isinstance(h, str) else h
    return .2126 * ch(r) + .7152 * ch(g) + .0722 * ch(b)


def cr(a, b):
    x, y = lum(a), lum(b)
    return (max(x, y) + .05) / (min(x, y) + .05)


def mix(a, b, t):
    A, B = hx(a), hx(b)
    return to_hex(tuple(A[i] + (B[i] - A[i]) * t for i in range(3)))


# ---------------------------------------------------------------- image statistics (spritestat, cached)
def _tool():
    if TOOL.exists() and TOOL.stat().st_mtime >= TOOL_SRC.stat().st_mtime:
        return str(TOOL)
    try:
        subprocess.run(['swiftc', '-O', str(TOOL_SRC), '-o', str(TOOL)], check=True, capture_output=True, timeout=300)
        return str(TOOL)
    except Exception as e:  # no Swift: images still work, placed by their full frame
        NOTES.append('spritestat unavailable (%s); images placed by full frame' % e.__class__.__name__)
        return None


_cache = None


def stats(paths):
    """{path: dict(w, h, bbox, mean, runs, quads)}; cached by size and mtime."""
    global _cache
    if _cache is None:
        try:
            _cache = json.loads(CACHE.read_text())
        except Exception:
            _cache = {}
    out, todo = {}, []
    for p in paths:
        st = p.stat()
        key = '%s|%d|%d' % (p.relative_to(NILAI), st.st_size, st.st_mtime_ns)
        if key in _cache:
            out[p] = _cache[key]
        else:
            todo.append((p, key))
    if todo:
        tool = _tool()
        if tool:
            res = subprocess.run([tool] + [str(p) for p, _ in todo], check=True, capture_output=True, text=True).stdout.strip().split('\n')
            for (p, key), line in zip(todo, res):
                d = json.loads(line)
                if 'error' in d:
                    continue
                _cache = {k: v for k, v in _cache.items() if not k.startswith(str(p.relative_to(NILAI)) + '|')}
                _cache[key] = d
                out[p] = d
            CACHE.write_text(json.dumps(_cache, indent=0, sort_keys=True))
    return out


# ---------------------------------------------------------------- assets on disk
ID_RE = re.compile(r'^([0-9]{2}-[A-Z][0-9]?|[KMP][0-9]+|FL)(\.[a-z]+)?\.webp$')
SHEETS = {
    # sheet id -> view -> (how the figure is found, index); see spritestat.swift
    'K0': {'front': ('runs', 0), 'tq': ('runs', 1), 'side': ('runs', 2), 'back': ('runs', 3)},
    'M0': {'side': ('quads', 0), 'front': ('quads', 1), 'back': ('quads', 2), 'fly': ('quads', 3)},
}


def crop_sheets():
    """Cut each multi-view sheet into single-view sprites (only when the sheet is newer than the crop)."""
    for sid, views in SHEETS.items():
        src = ASSETS / (sid + '.png')
        if not src.exists():
            continue
        S = stats([src]).get(src)
        if not S:
            continue
        for view, (kind, idx) in views.items():
            boxes = S.get(kind) or []
            if len(boxes) <= idx:
                NOTES.append('%s: found %d figures, no %s view' % (sid, len(boxes), view))
                continue
            x0, y0, x1, y1 = boxes[idx]
            pad = 6
            x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
            x1, y1 = min(S['w'], x1 + pad), min(S['h'], y1 + pad)
            dst = WEB / ('%s.%s.webp' % (sid, view))
            if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
                continue
            subprocess.run(['cwebp', '-quiet', '-q', '84', '-alpha_q', '90', '-m', '6', '-crop', str(x0), str(y0), str(x1 - x0), str(y1 - y0), str(src), '-o', str(dst)],
                           check=True)
            NOTES.append('cropped %s -> %s (%dx%d)' % (src.name, dst.name, x1 - x0, y1 - y0))


AV = {}      # id -> dict(path, rel, w, h, bbox, mean)


def discover():
    crop_sheets()
    files = sorted(p for p in WEB.glob('*.webp') if ID_RE.match(p.name))
    S = stats(files)
    for p in files:
        d = S.get(p)
        if not d:
            continue
        iid = p.name[:-5]
        AV[iid] = dict(path=p, rel='assets/web/' + p.name, w=d['w'], h=d['h'], bbox=d['bbox'], mean=to_hex(d['mean']))
    return AV


def video(vid):
    """A clip for the scroll-scrubbed hook: a keyed WebM (alpha) is preferred; an MP4 is keyed in the page."""
    for d, ext, keyed in ((ASSETS / 'video', 'webm', True), (WEB, 'webm', True), (ASSETS, 'webm', True),
                          (ASSETS / 'video', 'mp4', False), (WEB, 'mp4', False), (ASSETS, 'mp4', False), (ASSETS / 'src', 'mp4', False)):
        p = d / ('%s.%s' % (vid, ext))
        if p.exists():
            return dict(rel=str(p.relative_to(NILAI)), keyed=keyed)
    return None


# ---------------------------------------------------------------- the stage map (shot list 4.1)
STAGE_IDS = re.compile(r'\b(\d\d-[A-Z]\d?|FL)\b')


def stage_map():
    txt = (NILAI / 'v3_shotlist.md').read_text(encoding='utf-8')
    sec = txt.split('### 4.1 Stage map')[1].split('\n## ')[0]
    M = {}
    for ln in sec.split('\n'):
        m = re.match(r'^\| (\d\d) \| (.*?) \| (.*?) \| (.*?) \|$', ln)
        if not m:
            continue
        M[int(m.group(1))] = {k: STAGE_IDS.findall(v) for k, v in zip('TNF', m.groups()[1:])}
    assert len(M) == 31, len(M)
    return M


# ---------------------------------------------------------------- architecture per scene
ARCH = {1: 'koshta', 2: 'gallery', 3: 'mandapa', 4: 'tank', 5: 'sky', 6: 'koshta', 7: 'mandapa', 8: 'gallery',
        9: 'tank', 10: 'gallery', 11: 'sky', 12: 'tank', 13: 'koshta', 14: 'gallery', 15: 'mandapa', 16: 'gallery',
        17: 'sky', 18: 'koshta', 19: 'mandapa', 20: 'gallery', 21: 'mandapa', 22: 'tank', 23: 'gallery', 24: 'tank',
        25: 'sky', 26: 'gallery', 27: 'sky', 28: 'mandapa', 29: 'koshta', 30: 'gallery', 31: 'sky'}
STONE_NAME = {'indigo': 'black basalt', 'grey': 'granite', 'teal': 'green granite', 'laterite': 'laterite', 'kumkum': 'red sandstone',
              'chalk': 'limestone', 'tan': 'sandstone', 'turmeric': 'yellow limestone'}
PLINTH_H = {'gallery': 150, 'koshta': 46, 'mandapa': 64, 'tank': 34, 'sky': 56}


def stone(sh, n):
    """Stone shades for one scene: each one keeps text >= 4.5 and both art fills >= 3 (with a small margin)."""
    W, F, tx, ink, col = sh['wall'], sh['floor'], sh['tx'], sh['ink'], sh['col']

    def ok(c):
        return cr(tx, c) >= 4.6 and cr(ink, c) >= 3.1 and cr(col, c) >= 3.1

    def shade(base, toward, want):
        t = want
        while t > 0.004:
            c = mix(base, toward, t)
            if ok(c):
                return c
            t -= .01
        return base
    st = dict(W=W, F=F,
              Wl=shade(W, '#FFFFFF', .26), Wm=shade(W, '#FFFFFF', .12), Wj=shade(W, '#000000', .2), Wd=shade(W, '#000000', .34), Wdd=shade(W, '#000000', .6),
              Fl=shade(F, '#FFFFFF', .24), Fm=shade(F, '#FFFFFF', .1), Fj=shade(F, '#000000', .18), Fd=shade(F, '#000000', .32))
    # on light walls the lights barely move; let warm shadow carry the modelling instead
    if lum(W) > lum(ink):
        st['Wl'] = shade(W, '#FFFFFF', .5)
    # the noise grain lies over every stone shade: the largest alpha whose darkest and lightest specks still pass
    shades = [st[k] for k in ('W', 'F', 'Wl', 'Wm', 'Wj', 'Wd', 'Wdd', 'Fl', 'Fm', 'Fj', 'Fd')]
    a = .09
    while a > 0 and not all(ok(mix(b, t, a)) for b in shades for t in ('#000000', '#FFFFFF')):
        a -= .01
    st['noise'] = round(max(a, 0), 2)
    # the edge vignette darkens toward the corners; with the grain on top it must still pass on every shade
    # (the deep niche and pillar-return shades sit inside the clear centre of the vignette, so they are left out here)
    edge = [st[k] for k in ('W', 'F', 'Wl', 'Wm', 'Fl', 'Fm')]
    v = .34
    while v > 0 and not all(ok(mix(mix(b, '#000000', v), '#000000', st['noise'])) for b in edge):
        v -= .01
    st['vig'] = round(max(v, 0), 2)
    # the horizon keeps >= 1.6 between the wall's skirting and the floor
    st['skirt'] = st['Wl'] if lum(W) > lum(F) else st['Wd']
    if cr(st['skirt'], F) < 1.6:
        st['skirt'] = W
    for k in ('Wl', 'Wm', 'Wj', 'Wd', 'Wdd', 'Fl', 'Fm', 'Fj', 'Fd'):
        c = st[k]
        if not ok(c):
            FAIL.append('stone %02d %s %s fails text/ink/colour' % (n, k, c))
    if cr(st['skirt'], F) < 1.6 - 1e-9:
        FAIL.append('stone %02d horizon %.2f < 1.6' % (n, cr(st['skirt'], F)))
    return st


def _st(o, c, a=1):
    return '<stop offset="%s" stop-color="%s"%s/>' % (o, c, '' if a == 1 else ' stop-opacity="%s"' % a)


def _lin(i, stops, x2=0, y2=1):
    return '<linearGradient id="%s" x1="0" y1="0" x2="%s" y2="%s">%s</linearGradient>' % (i, x2, y2, ''.join(_st(*s) for s in stops))


def _rad(i, stops, cx=.5, cy=.5, r=.5):
    return '<radialGradient id="%s" cx="%s" cy="%s" r="%s">%s</radialGradient>' % (i, cx, cy, r, ''.join(_st(*s) for s in stops))


def _r(x, y, w, h, fill, **kw):
    return AR.tag('rect', x=AR.n(x), y=AR.n(y), width=AR.n(w), height=AR.n(h), fill=fill, **kw)


def _p(d, fill='none', **kw):
    return AR.tag('path', d=d, fill=fill, **kw)


def _poly(pts, fill, **kw):
    return _p('M' + ' L '.join('%s %s' % (AR.n(x), AR.n(y)) for x, y in pts) + ' Z', fill=fill, **kw)


BIG = (-3000, 4000)


def ashlar(st, pid, course=62, block=176):
    """A coursed stone pattern: staggered joints with a lit upper arris."""
    h2 = course * 2
    j = st['Wj']
    pat = ('<pattern id="%s" width="%d" height="%d" patternUnits="userSpaceOnUse" x="0" y="%d">' % (pid, block, h2, 760 % h2)
           + _r(0, 0, block, h2, st['W'])
           + _p('M0 .8 H%d M0 %d H%d M2 0 V%d M%d %d V%d' % (block, course, block, course, block // 2 + 2, course, h2), stroke=j, stroke_width='2.2')
           + _p('M0 3.4 H%d M0 %d H%d' % (block, course + 3, block), stroke=st['Wm'], stroke_width='1.4', opacity='.8')
           + '</pattern>')
    return pat


def floor_layer(st, sid, vp=(500, 430), kind=''):
    """Floor slabs in perspective toward the vanishing point, and a soft pool of light."""
    out = [_r(BIG[0], 760, BIG[1] - BIG[0], 3000, 'url(#%sfl)' % sid)]
    d = []
    for k in range(-26, 27):
        x = 500 + k * 150
        dx = (x - vp[0]) / (760 - vp[1])
        d.append('M%s 760 L %s 2200' % (AR.n(x), AR.n(x + dx * 1440)))
    y, step = 760, 22
    while y < 2200:
        y += step
        step *= 1.38
        d.append('M%d %s H%d' % (BIG[0], AR.n(y), BIG[1]))
    out.append(_p(''.join(d), stroke=st['Fj'], stroke_width='2', opacity='.9'))
    return ''.join(out)


def spot(st, sid, cx=500, cy=430, rx=440, ry=520, floor=True):
    out = [AR.tag('ellipse', cx=cx, cy=cy, rx=rx, ry=ry, fill='url(#%ssp)' % sid)]
    if floor:
        out.append(AR.tag('ellipse', cx=cx, cy=786, rx=rx * .82, ry=64, fill='url(#%sfp)' % sid))
    return ''.join(out)


def arch_defs(st, sid):
    return ''.join([
        _lin(sid + 'fl', [(0, st['Fd']), (.12, st['F']), (1, st['F'])]),
        _rad(sid + 'sp', [(0, st['Wl'], .95), (.55, st['Wl'], .35), (1, st['Wl'], 0)]),
        _rad(sid + 'fp', [(0, st['Fl'], .9), (1, st['Fl'], 0)]),
        _lin(sid + 'pf', [(0, st['Wl']), (1, st['Wm'])]),                 # pilaster / pillar front
        _lin(sid + 'ps', [(0, st['Wj']), (1, st['Wd'])], x2=1, y2=0),    # pillar side
        _lin(sid + 'nk', [(0, st['Wdd']), (.4, st['Wd']), (1, st['Wj'])]),  # niche recess
        _lin(sid + 'sk', [(0, st['Wdd']), (1, st['Wd'])]),                 # sky through the arch
        _lin(sid + 'cone', [(0, st['Wl'], .55), (1, st['Wl'], 0)]),
        _lin(sid + 'tr', [(0, st['Fm']), (1, st['F'])]),
        _lin(sid + 'ri', [(0, st['Fj']), (1, st['Fd'])]),
        ashlar(st, sid + 'as'),
    ])


def pillar(x, base, w, h, sid, st, cap=True):
    """A Chola-style pillar: square block, octagonal band, square block, a capital and a corbel bracket."""
    top = base - h
    u = h / 100
    out = []
    side = w * .18
    out.append(_r(x - w / 2 - side, top + 6 * u, side, h - 6 * u, 'url(#%sps)' % sid))
    segs = [(0, 10, 1.0), (10, 30, .86), (30, 44, 1.0), (44, 62, .86), (62, 76, 1.0), (76, 84, .9), (84, 90, 1.16), (90, 96, 1.3)]
    for a, b, k in segs:
        ww = w * k
        out.append(_r(x - ww / 2, base - b * u, ww, (b - a) * u, 'url(#%spf)' % sid, stroke=st['Wj'], stroke_width='1.6'))
    if cap:
        out.append(_p('M%s %s q %s %s %s %s M%s %s q %s %s %s %s' % (AR.n(x - w * .65), AR.n(top + 4 * u), AR.n(-w * .12), AR.n(-4 * u), AR.n(-w * .5), AR.n(-4 * u),
                                                                 AR.n(x + w * .65), AR.n(top + 4 * u), AR.n(w * .12), AR.n(-4 * u), AR.n(w * .5), AR.n(-4 * u)),
                      stroke=st['Wj'], stroke_width=AR.n(max(2, 3 * u))))
    return ''.join(out)


def arch_svg(n, sh, st):
    """The stone stage behind scene n, in the 1000-unit art space (horizon y = 760), drawn past the frame edges."""
    kind = ARCH[n]
    sid = 'a%02d' % n
    out = ['<defs>%s</defs>' % arch_defs(st, sid)]
    wall = 'url(#%sas)' % sid if kind != 'gallery' else st['W']
    out.append(_r(BIG[0], -3000, BIG[1] - BIG[0], 3760, wall))
    if kind == 'gallery':
        # a clean plaster wall, a shadow gap at the floor, a track light and its cone
        out.append(_poly([(440, -400), (560, -400), (790, 760), (210, 760)], 'url(#%scone)' % sid))
        out.append(spot(st, sid, 500, 470, 420, 470))
        out.append(_r(BIG[0], 748, BIG[1] - BIG[0], 12, st['skirt']))
        out.append(floor_layer(st, sid, (500, 300)))
    elif kind == 'koshta':
        out.append(spot(st, sid, 500, 420, 520, 560))
        # base moulding (adhisthana) across the wall
        out.append(_r(BIG[0], 692, BIG[1] - BIG[0], 22, st['Wm'], stroke=st['Wj'], stroke_width='2'))
        out.append(_r(BIG[0], 714, BIG[1] - BIG[0], 30, st['Wd']))
        out.append(_r(BIG[0], 744, BIG[1] - BIG[0], 16, st['skirt']))
        # pilasters
        for x in (262, 738):
            out.append(_r(x - 34, 236, 68, 456, 'url(#%spf)' % sid, stroke=st['Wj'], stroke_width='2'))
            out.append(_r(x - 44, 216, 88, 22, st['Wm'], stroke=st['Wj'], stroke_width='2'))
            out.append(_r(x - 40, 650, 80, 42, st['Wm'], stroke=st['Wj'], stroke_width='2'))
            out.append(_p('M%d 330 V610' % x, stroke=st['Wj'], stroke_width='2', opacity='.7'))
        # the niche: deep at the top, lit toward its sill
        out.append(_r(310, 254, 380, 506, 'url(#%snk)' % sid))
        out.append(_poly([(310, 254), (338, 278), (338, 734), (310, 760)], st['Wdd'], opacity='.55'))
        out.append(_poly([(690, 254), (662, 278), (662, 734), (690, 760)], st['Wj'], opacity='.6'))
        out.append(AR.tag('ellipse', cx=500, cy=540, rx=150, ry=220, fill='url(#%ssp)' % sid, opacity='.55'))
        # lintel and the curved cornice (kapota), with a small sala crown
        out.append(_r(200, 190, 600, 30, st['Wm'], stroke=st['Wj'], stroke_width='2'))
        out.append(_p('M186 190 C 186 152 230 138 300 136 L 700 136 C 770 138 814 152 814 190 Z', fill='url(#%spf)' % sid, stroke=st['Wj'], stroke_width='2'))
        out.append(_p('M200 172 H800', stroke=st['Wj'], stroke_width='1.6', opacity='.7'))
        out.append(_p('M410 136 C 414 88 446 64 500 60 C 554 64 586 88 590 136 Z', fill='url(#%spf)' % sid, stroke=st['Wj'], stroke_width='2'))
        out.append(_p('M456 136 C 460 106 476 94 500 92 C 524 94 540 106 544 136', stroke=st['Wj'], stroke_width='2'))
        out.append(floor_layer(st, sid))
    elif kind == 'mandapa':
        out.append(spot(st, sid, 500, 470, 380, 420))
        out.append(_r(BIG[0], 744, BIG[1] - BIG[0], 16, st['skirt']))
        out.append(floor_layer(st, sid, (500, 560)))
        VP, Y0 = (500, 560), 1060
        rows = []
        for k in range(5, -1, -1):
            s = 1 / (1 + .62 * k)
            base = VP[1] + (Y0 - VP[1]) * s
            if base < 760:
                continue
            h = (base - (VP[1] - (VP[1] + 520) * s)) if False else 1500 * s
            for side in (-1, 1):
                x = VP[0] + side * 640 * s
                rows.append(pillar(x, base, 118 * s, h, sid, st))
        # beams that carry the roof, receding to the vanishing point
        out.append(''.join(rows))
    elif kind == 'tank':
        out.append(spot(st, sid, 500, 470, 420, 440, floor=False))
        out.append(_r(BIG[0], 716, BIG[1] - BIG[0], 30, st['Wm'], stroke=st['Wj'], stroke_width='2'))
        out.append(_r(BIG[0], 746, BIG[1] - BIG[0], 14, st['skirt']))
        # the stepped edge descending toward the viewer, then still water
        steps = [_r(BIG[0], 760, BIG[1] - BIG[0], 3000, st['F'])]
        y, tread, riser = 760, 46, 16
        for i in range(7):
            steps.append(_r(BIG[0], y, BIG[1] - BIG[0], tread, 'url(#%str)' % sid))
            steps.append(_r(BIG[0], y + tread, BIG[1] - BIG[0], riser, 'url(#%sri)' % sid))
            steps.append(_p('M%d %s H%d' % (BIG[0], AR.n(y + 1.5), BIG[1]), stroke=st['Fl'], stroke_width='2.5'))
            y += tread + riser
            tread *= 1.16
            riser *= 1.16
        steps.append(_r(BIG[0], y, BIG[1] - BIG[0], 3000, st['Fd']))
        steps.append(_p(''.join('M%d %d q 40 -7 80 0 t 80 0 ' % (x, y + 40 + (x // 160 % 3) * 26) for x in range(-1400, 2400, 220)), stroke=st['Fl'], stroke_width='3', opacity='.7'))
        out.append(''.join(steps))
    elif kind == 'sky':
        # a stone arch: the night through it, voussoirs round it
        R, cx, cy = 280, 500, 400
        out.append(_r(BIG[0], 744, BIG[1] - BIG[0], 16, st['skirt']))
        opening = 'M%d 760 L %d %d A %d %d 0 0 1 %d %d L %d 760 Z' % (cx - R, cx - R, cy, R, R, cx + R, cy, cx + R)
        out.append(_p(opening, fill='url(#%ssk)' % sid))
        stars = ''.join(AR.tag('circle', cx=AR.n(cx + math.cos(a) * r), cy=AR.n(cy - abs(math.sin(a)) * r * .95), r=AR.n(1.3 + (i % 3) * .7))
                        for i, (a, r) in enumerate([(.3 + i * .53, 60 + (i * 67) % 210) for i in range(22)]))
        out.append('<g fill="%s" opacity=".7" data-nochk="1" class="tw">%s</g>' % (sh['ink'], stars))
        vs = []
        for i in range(17):
            a0 = math.pi * i / 17
            a1 = math.pi * (i + 1) / 17
            p = [(cx - math.cos(a0) * R, cy - math.sin(a0) * R), (cx - math.cos(a0) * (R + 62), cy - math.sin(a0) * (R + 62)),
                 (cx - math.cos(a1) * (R + 62), cy - math.sin(a1) * (R + 62)), (cx - math.cos(a1) * R, cy - math.sin(a1) * R)]
            vs.append(_poly(p, st['Wl'] if i % 2 else 'url(#%spf)' % sid, stroke=st['Wdd'], stroke_width='3'))
        out.append(''.join(vs))
        for side in (-1, 1):
            x = cx + side * (R + 31)
            for j in range(6):
                y = cy + j * 60
                out.append(_r(x - 31, y, 62, 60, 'url(#%spf)' % sid if j % 2 else st['Wl'], stroke=st['Wdd'], stroke_width='3'))
        # moonlight on the intrados and the outer edge, so the arch reads against the wall
        lit = mix(st['Wl'], '#FFFFFF', .45)
        out.append('<g data-nochk="1" fill="none" stroke-linecap="round">%s%s</g>' % (
            _p('M%d 760 L %d %d A %d %d 0 0 1 %d %d L %d 760' % (cx - R + 2, cx - R + 2, cy, R - 2, R - 2, cx + R - 2, cy, cx + R - 2), stroke=lit, stroke_width='3', opacity='.8'),
            _p('M%d 760 L %d %d A %d %d 0 0 1 %d %d L %d 760' % (cx - R - 64, cx - R - 64, cy, R + 64, R + 64, cx + R + 64, cy, cx + R + 64), stroke=st['Wdd'], stroke_width='5', opacity='.9')))
        out.append(AR.tag('ellipse', cx=cx, cy=786, rx=300, ry=50, fill='url(#%sfp)' % sid))
        out.append(floor_layer(st, sid, (500, 420)))
    return '<svg class="arch" viewBox="0 0 1000 1000" aria-hidden="true" focusable="false">%s</svg>' % ''.join(out)


# ---------------------------------------------------------------- characters: marble keeper, bronze myna
# every vector pose of the keeper and the myna maps to the nearest marble or bronze pose; K0 / M0 views are the fallbacks
KEEPER_POSE = {
    'write': ['K3'], 'kneel': ['K3'], 'stand': ['K0.side'], 'walk1': ['K1', 'K0.side'], 'walk2': ['K1', 'K0.side'],
    'point': ['K2'], 'pointup': ['K2'], 'reach': ['K2'], 'serve': ['K2'], 'startle': ['K4'], 'delight': ['K5'],
    'sit': ['K6'], 'cross': ['K6'], 'lie': ['K6'], 'paddle': ['K6'],
    'listen': ['K0.tq'], 'hold': ['K0.tq'], 'lean': ['K0.side'], 'carry': ['K0.front'],
}
MYNA_POSE = {'stand': ['M6'], 'up': ['M0.side'], 'peck': ['M3'], 'sip': ['M3'], 'sing': ['M5'], 'startle': ['M4'], 'tuck': ['M6'],
             'fly': ['M0.fly'], 'walk': ['M1'], 'point': ['M2']}
# keeper: height of the figure (art units at s = 1; the SVG keeper is about 380 tall). myna: length (the SVG myna is about 124 long)
SPRITE_H = {'K3': 300, 'K6': 250, 'K5': 392, 'K4': 372}
SPRITE_W = {'M0.front': 70, 'M3': 132, 'M4': 120}
# where a held object goes: the hand, in the sprite file's pixels
HAND = {'K2': (512, 100), 'K0.tq': (37, 347), 'K0.side': (120, 360), 'K0.front': (122, 330), 'K6': (250, 470), 'K4': (470, 165), 'K3': (330, 330)}
# the braid of the side view, as a polygon in the crop's pixels (separable only on this exact sheet)
BRAID = dict(size=815761, pivot=(36, 64),
             poly=[(28, 56), (52, 64), (47, 112), (41, 162), (38, 250), (36, 330), (34, 372), (38, 446), (0, 448), (1, 372), (5, 330), (8, 250), (12, 160), (17, 100)])


class Ctx:
    sh = None       # palette of the scene being drawn
    sid = '00'
    halo = set()    # sprites that needed the halo in this scene


def _place(a, H, ax=.5):
    """x, y, w, h for an image whose alpha bbox is H tall, feet at (0, 0), centred at x = 0."""
    x0, y0, x1, y1 = a['bbox']
    k = H / max(1, (y1 - y0))
    cx = x0 + (x1 - x0) * ax
    return (-cx * k, -y1 * k, a['w'] * k, a['h'] * k, k)


def needs_halo(iid, bgs):
    a = AV[iid]
    return min(cr(a['mean'], b) for b in bgs) < 3


def material(iid):
    """m marble (clean white, never pushed grey or yellow), b bronze / brass / warm wood (rich, never olive), x the rest."""
    r, g, b = hx(AV[iid]['mean'])
    mx, mn = max(r, g, b), min(r, g, b)
    sat = (mx - mn) / max(mx, 1)
    if sat < .14:
        return 'm'
    if r == mx and b == mn and r > b:
        hue = 60 * (g - b) / max(r - b, 1)
        if 12 <= hue <= 46 and sat > .25:
            return 'b'
    return 'x'


def _ct(c, lift=0.0, gamma=1.0):
    """feComponentTransfer for contrast c around mid-grey, a lift, and a gamma that deepens the shadows."""
    f = '<feFunc%%s type="gamma" amplitude="%s" exponent="%s" offset="%s"/>' % (AR.n(c), AR.n(gamma), AR.n(.5 - .5 * c + lift))
    return '<feComponentTransfer>%s</feComponentTransfer>' % ''.join(f % ch for ch in 'RGB')


GRADE_DEFS = (
    '<filter id="fwhite" x="0" y="0" width="100%" height="100%"><feColorMatrix type="matrix" values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 1 0"/></filter>'
    '<filter id="fblack" x="0" y="0" width="100%" height="100%"><feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0"/></filter>'
    # marble: contrast 1.16 with the whites lifted to clean white; a touch less saturation so it never yellows
    '<filter id="fgm" color-interpolation-filters="sRGB"><feColorMatrix type="saturate" values=".86"/>' + _ct(1.16, .045, 1.06) + '</filter>'
    # bronze, brass, gold, warm wood: contrast 1.18, saturation 1.24, hue pulled off olive toward red-gold, deeper shadows
    '<filter id="fgb" color-interpolation-filters="sRGB"><feColorMatrix type="hueRotate" values="-7"/><feColorMatrix type="saturate" values="1.24"/>' + _ct(1.18, .0, 1.12) + '</filter>'
    # everything else: contrast 1.14, saturation 1.16
    '<filter id="fgx" color-interpolation-filters="sRGB"><feColorMatrix type="saturate" values="1.16"/>' + _ct(1.14, .0, 1.08) + '</filter>'
)
_rimn = [0]


def rim(iid, x, y, w, h, tag):
    """Key light from the upper left: a soft gradient over the cut-out, and a bright rim on its upper-left edge
    (the silhouette minus itself shifted down-right), both masked by the image."""
    a = AV[iid]
    bx0, by0, bx1, by1 = a['bbox']
    k = w / a['w']
    d = max(2.5, min(9, (by1 - by0) * k * .012))
    _rimn[0] += 1
    m = 'r%s%d' % (tag, _rimn[0])
    U = ' maskUnits="userSpaceOnUse" x="%s" y="%s" width="%s" height="%s"' % (AR.n(x - 20), AR.n(y - 20), AR.n(w + 40), AR.n(h + 40))
    msk = ('<mask id="%sk"%s>%s</mask><mask id="%se"%s>%s%s</mask>'
           % (m, U, img(iid, x, y, w, h, extra=' filter="url(#fwhite)"'), m, U, img(iid, x, y, w, h, extra=' filter="url(#fwhite)"'),
              img(iid, x + d, y + d, w, h, extra=' filter="url(#fblack)"')))
    bx, by, bw, bh = x + bx0 * k, y + by0 * k, (bx1 - bx0) * k, (by1 - by0) * k
    key = ('<linearGradient id="%sg" gradientUnits="userSpaceOnUse" x1="%s" y1="%s" x2="%s" y2="%s"><stop offset="0" stop-color="#fff" stop-opacity=".34"/>'
           '<stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>' % (m, AR.n(bx), AR.n(by), AR.n(bx + bw), AR.n(by + bh)))
    return ('<defs>%s%s</defs><g data-nochk="1" class="lit"><rect mask="url(#%sk)" x="%s" y="%s" width="%s" height="%s" fill="url(#%sg)"/>'
            '<rect mask="url(#%se)" x="%s" y="%s" width="%s" height="%s" fill="#fff" opacity=".5"/></g>'
            % (msk, key, m, AR.n(bx), AR.n(by), AR.n(bw), AR.n(bh), m, m, AR.n(bx), AR.n(by), AR.n(bw * .7), AR.n(bh * .7)))


def graded(iid, x, y, w, h, cls=''):
    return img(iid, x, y, w, h, cls=cls, extra=' filter="url(#fg%s)"' % material(iid))


def img(iid, x, y, w, h, cls='', extra=''):
    a = AV[iid]
    USED.add(a['rel'])
    return '<image data-href="%s" x="%s" y="%s" width="%s" height="%s" preserveAspectRatio="none"%s%s/>' % (
        a['rel'], AR.n(x), AR.n(y), AR.n(w), AR.n(h), ' class="%s"' % cls if cls else '', extra)


def _sprite_id(kind, pose):
    table = KEEPER_POSE if kind == 'K' else MYNA_POSE
    for c in table.get(pose if isinstance(pose, str) else 'stand', []):
        if c in AV:
            return c
    return None


def _one(kind, iid, hold=''):
    """One sprite, feet at (0, 0), centred, at s = 1."""
    a = AV[iid]
    if kind == 'K':
        H = SPRITE_H.get(iid, 380)
    else:
        x0, y0, x1, y1 = a['bbox']
        H = SPRITE_W.get(iid, 124) * (y1 - y0) / max(1, x1 - x0)
    x, y, w, h, k = _place(a, H)
    sh = Ctx.sh
    halo = ''
    if sh and needs_halo(iid, (sh['wall'], sh['floor'])):
        halo = ' filter="url(#fh%s)"' % Ctx.sid
        Ctx.halo.add(iid)
    braid = iid == 'K0.side' and (AV[iid]['path'].parent.parent / 'K0.png').exists() and (AV[iid]['path'].parent.parent / 'K0.png').stat().st_size == BRAID['size']
    if braid:
        px, py = BRAID['pivot']
        poly = ' '.join('%s,%s' % (AR.n(x + bx * k), AR.n(y + by * k)) for bx, by in BRAID['poly'])
        cid = 'kb%s%d' % (Ctx.sid, len(Ctx.halo) + _rimn[0])
        clip = ('<clipPath id="%sa"><path clip-rule="evenodd" d="M-600 -900 H600 V200 H-600 Z M%s Z"/></clipPath><clipPath id="%sb"><polygon points="%s"/></clipPath>'
                % (cid, poly.replace(' ', ' L ').replace(',', ' '), cid, poly))
        inner = (clip + '<g clip-path="url(#%sa)">%s</g>' % (cid, graded(iid, x, y, w, h))
                 + '<g class="sway" style="transform-origin:%spx %spx"><g clip-path="url(#%sb)">%s</g></g>'
                 % (AR.n(px * k), AR.n(py * k), cid, graded(iid, x, y, w, h)))
    else:
        inner = graded(iid, x, y, w, h)
    inner += rim(iid, x, y, w, h, Ctx.sid)
    out = '<g class="spr %s"%s>%s</g>' % ('bob' if kind == 'M' else 'breathe', halo, inner)
    if hold:
        hx_, hy_ = HAND.get(iid, (a['w'] * .6, a['h'] * .45))
        out += AR.g(hold, transform='translate(%s %s)' % (AR.n(x + hx_ * k), AR.n(y + hy_ * k)))
    return out


def sprite(kind, pose, anim=None, s=1.0, flip=False, extra='', hold=''):
    """SVG for a character sprite, or None to keep the vector drawing.
    A keeper animated through several poses swaps between the matching sprites at the pose times."""
    tr = 'scale(%s %s)' % (AR.n(-s if flip else s), AR.n(s)) if (s != 1 or flip) else None
    if anim and kind == 'K':
        segs = []
        for t, p in anim:
            iid = _sprite_id('K', p)
            if not iid:
                return None
            if not segs or segs[-1][1] != iid:
                segs.append((t, iid))
        if len(segs) == 1:
            pose = None
            inner = _one('K', segs[0][1], hold)
        else:
            parts = []
            for j, (t0, iid) in enumerate(segs):
                t1 = segs[j + 1][0] if j + 1 < len(segs) else None
                fr = [(0, dict(o=1 if j == 0 else 0))]
                if j > 0:
                    fr += [(max(t0 - .004, .001), dict(o=0)), (t0, dict(o=1))]
                if t1 is not None:
                    fr += [(max(t1 - .004, t0 + .001), dict(o=1)), (t1, dict(o=0))]
                parts.append(AR.g(_one('K', iid, hold), k=AR.kf(*fr)))
            inner = ''.join(parts)
        return AR.g(inner + extra, transform=tr, data_chr='1')
    iid = _sprite_id(kind, pose)
    if not iid:
        return None
    inner = _one(kind, iid, hold) + extra
    if kind == 'M' and anim:
        return AR.g(AR.g(inner, k=anim, c=(0, -40)), transform=tr, data_chr='1')
    return AR.g(inner, transform=tr, data_chr='1')


# ---------------------------------------------------------------- stage images per scene
M1A, M1B, M2A, M2B = T['m1a'], T['m1b'], T['m2a'], T['m2b']
# image cross-dissolves: about 9% of the scene each, centred on the SVG morphs, so every stage settles and holds
D1 = (round((M1A + M1B) / 2 - .045, 3), round((M1A + M1B) / 2 + .045, 3))
D2 = (round((M2A + M2B) / 2 - .045, 3), round((M2A + M2B) / 2 + .045, 3))
WIN = {'T': [(None, None) + D1], 'N': [D1 + D2], 'F': [D2 + (None, None)]}
STAG = .38   # the outgoing image is gone by 62% of the dissolve, the incoming one starts at 38%: a short overlap under the sweep

# per-scene settings. box = (centre x, bottom y, max width, max height) in art units; bottom None = on the plinth.
SCENE = {
    1: dict(box={'T': (500, None, 330, 300), 'F': (500, 736, 190, 560)}, plinth={'T'}, exit=((.84, dict(x=0, s=1, o=1)), (.95, 'i', dict(x=470, s=.5, o=0))),
            video=('V4', M1A, M2B)),
    2: dict(box={'T': (500, 700, 620, 540), 'N': (500, None, 520, 440)}, plinth={'N'}, wire={'T': 1}, video=('V5', M1A, M1B)),
    4: dict(box={'T': (500, 760, 400, 440), 'F': (500, 770, 980, 520)}, pick={'F': '04-F2'}, plinth=set()),
    3: dict(seam=[(382, 104), (356, 176), (370, 226), (322, 298), (338, 346), (292, 420), (304, 466), (250, 524)],
            seam2=[(338, 346), (372, 392), (366, 440)]),
    # 07-T.floor: 07-T keystoned onto the floor by warp.swift (true perspective, not a vertical squash)
    7: dict(box={'T': (540, 945, 900, 320)}, pick={'T': '07-T.floor'}, plinth=set(), style='slide'),
    26: dict(box={'T': (500, None, 600, 470), 'N': (500, None, 760, 360), 'F': (500, 640, 820, 620)}, plinth={'T', 'N'}, style='slide', video=('V2', M1A, M2B)),
    31: dict(box={'T': (500, 776, 360, 640), 'N': (500, 560, 220, 380), 'F': (500, 330, 300, 300)}, plinth=set(),
             win={'T': [(None, None, .2, .22), (.32, .34, .5, .56)], 'N': [(.1, .13, .2, .22)], 'F': [(.2, .24, .3, .33)]},
             flames=[(.0, None), (.36, None), (.4, None)], video=('V1', .1, .26)),
}


def _vis(p, w):
    a0, a1, b0, b1 = w
    if a0 is None:
        v = 1.0
    elif p <= a0:
        v = 0.0
    elif p >= a1:
        v = 1.0
    else:
        v = (p - a0) / (a1 - a0)
    if b0 is not None:
        if p >= b1:
            v = 0.0
        elif p > b0:
            v = min(v, 1 - (p - b0) / (b1 - b0))
    return v


def _cov(p, wins):
    return max([_vis(p, w) for w in wins] or [0])


def _merge(wins):
    """Join windows that hand over to each other (one's exit overlaps the next one's entrance) into one span, so the
    SVG objects and the plinth stay hidden through an image-to-image dissolve."""
    ws = sorted(wins, key=lambda w: -1 if w[0] is None else w[0])
    out = []
    for w in ws:
        if out and out[-1][2] is not None and w[0] is not None and w[0] <= out[-1][3] + 1e-6:
            p = out[-1]
            out[-1] = (p[0], p[1], w[2], w[3])
        else:
            out.append(tuple(w))
    return out


def _times(wins):
    ts = {0.0, 1.0}
    for w in wins:
        for t in w:
            if t is not None:
                ts.add(round(t, 4))
    return sorted(ts)


def _okeys(wins, f=lambda v: v, enter=False):
    """Opacity keyframes for a set of windows (piecewise linear between the window edges)."""
    ts = _times(wins)
    fr = []
    for t in ts:
        v = _cov(t, wins)
        if enter and t < .1 and any(w[0] is None for w in wins):
            v = 0 if t <= .03 else v
        fr.append((t, 'l', dict(o=round(f(v), 3))))
    if enter and any(w[0] is None for w in wins):
        fr = [x for x in fr if x[0] == 0 or x[0] >= .1]
        fr[0] = (0, 'l', dict(o=0))
        fr.insert(1, (.03, 'l', dict(o=0)))
        fr.insert(2, (.1, 'o', dict(o=round(f(_cov(.1, wins)), 3))))
    return fr


def slot_keys(wins, style, c):
    """Opacity and motion keyframes for one stage image: dissolve (scale) or slide-and-scale."""
    fr = []
    for w in wins:
        a0, a1, b0, b1 = w
        if a0 is None:
            fr += [(0, dict(o=0, y=26, s=1, x=0)), (.03, dict(o=0, y=26, s=1, x=0)), (.1, 'o', dict(o=1, y=0, s=1, x=0))]
        else:
            a0 = a0 + (a1 - a0) * STAG
            if style == 'slide':
                fr += [(a0, dict(o=0, x=-300, s=.86, y=0)), (a1, 'o', dict(o=1, x=0, s=1, y=0))]
            else:
                fr += [(a0, dict(o=0, s=1.04, x=0, y=0)), (a1, 'o', dict(o=1, s=1, x=0, y=0))]
        if b0 is not None:
            b1 = b1 - (b1 - b0) * STAG
            if style == 'slide':
                fr += [(b0, dict(o=1, x=0, s=1, y=0)), (b1, 'n', dict(o=0, x=320, s=.86, y=0))]
            else:
                fr += [(b0, dict(o=1, s=1, x=0, y=0)), (b1, 'i', dict(o=0, s=.97, x=0, y=0))]
    fr.sort(key=lambda x: x[0])
    # the engine needs distinct times
    out, last = [], -1
    for x in fr:
        t = x[0] if x[0] > last else last + .001
        out.append((t,) + tuple(x[1:]))
        last = t
    if out[0][0] > 0:
        first = out[0][-1]
        out.insert(0, (0, dict(first, o=0)))
    return AR.kf(*out)


def sweep_keys(wins, x0, x1):
    fr = [(0, dict(o=0, x=x0))]
    ramps = []
    for a0, a1, b0, b1 in wins:
        ramps.append((.03, .13) if a0 is None else (a0, a1))
        if b0 is not None:
            ramps.append((b0, b1))
    last = 0
    for t0, t1 in sorted(ramps):
        t0 = max(t0, last + .002)
        fr += [(t0 - .001, dict(o=0, x=x0)), (t0, dict(o=1, x=x0)), (t1, 'i', dict(o=1, x=x1)), (t1 + .001, dict(o=0, x=x1))]
        last = t1 + .001
    return AR.kf(*fr)


def box_for(n, stage, iid, kind):
    cfg = SCENE.get(n, {})
    ph = PLINTH_H[kind]
    on_plinth = stage in cfg.get('plinth', {'T', 'N', 'F'})
    b = cfg.get('box', {}).get(stage)
    if b is None:
        b = (500, None, 560, 470)
    cx, bottom, mw, mh = b
    if bottom is None:
        bottom = 760 - ph if on_plinth else 760
    return cx, bottom, mw, mh, on_plinth


def fit(iid, cx, bottom, mw, mh):
    a = AV[iid]
    x0, y0, x1, y1 = a['bbox']
    k = min(mw / max(1, x1 - x0), mh / max(1, y1 - y0))
    return (cx - (x0 + x1) / 2 * k, bottom - y1 * k, a['w'] * k, a['h'] * k, k, (x1 - x0) * k, (y1 - y0) * k)


def plinth(cx, top, w, st, sid):
    """A stone plinth seen from a little above: lit top, front face, a shaded return, and its shadow."""
    h = 760 - top
    d = 18
    x0, x1 = cx - w / 2, cx + w / 2
    return ''.join([
        AR.tag('ellipse', cx=AR.n(cx + 10), cy=772, rx=AR.n(w * .72), ry=16, fill=st['Fd'], opacity='.5'),
        _poly([(x0, top), (x1, top), (x1 + d * .6, top - d * .5), (x0 + d * .6, top - d * .5)], st['Wl']),
        _r(x0, top, w, h, 'url(#%spf)' % sid, stroke=st['Wj'], stroke_width='1.6'),
        _poly([(x1, top), (x1 + d * .6, top - d * .5), (x1 + d * .6, 760 - d * .5), (x1, 760)], st['Wd']),
        _p('M%s %s H%s' % (AR.n(x0 + 8), AR.n(top + 10), AR.n(x1 - 8)), stroke=st['Wm'], stroke_width='2'),
    ])


def scene_images(n, sh, st, M):
    """Returns (svg for the stage images, the svgobj coverage keyframes or None, clip info or None)."""
    cfg = SCENE.get(n, {})
    kind = ARCH[n]
    sid = '%02d' % n
    picks = {}
    for stage in 'TNF':
        ids = [i for i in M.get(stage, []) if i != 'FL']
        iid = cfg.get('pick', {}).get(stage) or (ids[0] if ids else None)
        if iid and iid in AV:
            picks[stage] = iid
    if not picks:
        return '', None, None
    wins_all = []
    out_img, out_mask, out_fx = [], [], []
    style = cfg.get('style', 'dissolve')
    # a stage that repeats the previous stage's image (02: NOW and FUTURE are both 02-N) extends it
    merged = {}
    for stage in 'TNF':
        if stage not in picks:
            continue
        wins = list(cfg.get('win', {}).get(stage, WIN[stage]))
        prev = {'N': 'T', 'F': 'N'}.get(stage)
        if prev in merged and picks.get(prev) == picks[stage]:
            pw = merged[prev][1]
            pw[-1] = (pw[-1][0], pw[-1][1], wins[-1][2], wins[-1][3])
            continue
        merged[stage] = (picks[stage], wins)
    plinth_w, plinth_top, plinth_wins = 0, None, []
    bgs = (sh['wall'], sh['floor'])
    for stage, (iid, wins) in merged.items():
        cx, bottom, mw, mh, on_plinth = box_for(n, stage, iid, kind)
        x, y, w, h, k, bw, bh = fit(iid, cx, bottom, mw, mh)
        wins_all += wins
        ckey = (cx, bottom - bh / 2)
        halo = ' filter="url(#fh%s)"' % sid if needs_halo(iid, bgs) else ''
        if halo:
            Ctx.halo.add(iid)
        flat = cfg.get('flat', {}).get(stage)
        tr = 'translate(%s %s) scale(1 %s) translate(%s %s)' % (AR.n(cx), AR.n(bottom), flat, AR.n(-cx), AR.n(-bottom)) if flat else None
        mid = 'm%s%s' % (sid, stage)
        pool = AR.tag('ellipse', cx=AR.n(cx), cy=AR.n(bottom - bh * .5), rx=AR.n(bw * .78 + 40), ry=AR.n(bh * .62 + 30), fill='url(#pool%s)' % sid, data_stone='1')
        image = pool + '<g%s>%s</g>' % (halo, graded(iid, x, y, w, h)) + rim(iid, x, y, w, h, sid + stage)
        out_mask.append('<mask id="%s" maskUnits="userSpaceOnUse" x="-500" y="-500" width="2000" height="2000">%s</mask>'
                        % (mid, img(iid, x, y, w, h, extra=' filter="url(#fwhite)"')))
        sweep = AR.g(AR.tag('rect', x=AR.n(-bw * .35), y=AR.n(y), width=AR.n(bw * .35), height=AR.n(h), fill='url(#swp%s)' % sid),
                     k=sweep_keys(wins, AR.n(x + (w - bw) / 2 - bw * .2), AR.n(x + (w + bw) / 2 + bw * .55)))
        wire = cfg.get('wire', {}).get(stage)
        if wire:
            image = AR.tag('path', d='M%s -900 V%s' % (AR.n(cx), AR.n(y + AV[iid]['bbox'][1] * k + 4)), stroke='var(--ink)', stroke_width='2.5', fill='none') + image
        body = image + '<g mask="url(#%s)" data-nochk="1" class="swp">%s</g>' % (mid, sweep)
        if cfg.get('seam') and stage == 'N' and picks.get('F') == iid:
            body += seam(cfg, x, y, w, iid)
        if n == 31 and stage == 'T' and 'FL' in AV:
            body += flames31(x, y, w, h, k, iid)
        grp = AR.g(body, transform=tr) if tr else body
        kp = slot_keys(wins, style, ckey)
        out_img.append(AR.g(grp, k=kp, c=ckey, kp=phone_keys(kp, ckey, bw, bh), cls='stimg', data_id=iid))
        if on_plinth:
            plinth_w = max(plinth_w, bw * .86 + 60)
            plinth_top = bottom
            plinth_wins += wins
    defs = ('<defs><radialGradient id="pool%s"><stop offset="0" stop-color="%s" stop-opacity=".85"/><stop offset=".6" stop-color="%s" stop-opacity=".3"/>'
            '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (sid, st['Wl'], st['Wl'], st['Wl'])
            + '<linearGradient id="swp%s" x1="0" y1="0" x2="1" y2=".25"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="#fff" stop-opacity=".62"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>%s</defs>' % (sid, ''.join(out_mask)))
    pl = ''
    if plinth_wins:
        pl = AR.g('<g data-stone="1">%s</g>' % plinth(500, plinth_top, max(200, plinth_w), st, 'a' + sid), k=AR.kf(*_okeys(_merge(plinth_wins), enter=True)))
    svg = defs + pl + ''.join(out_img)
    if cfg.get('exit'):
        svg = AR.g(svg, k=AR.kf(*cfg['exit']), c=(500, 420))
    cov = AR.kf(*_okeys(_merge(wins_all), f=lambda v: 1 - v))
    clip = None
    if cfg.get('video'):
        vid, t0, t1 = cfg['video']
        v = video(vid)
        first = merged.get('T')
        if v and first:
            cx, bottom, mw, mh, _ = box_for(n, 'T', first[0], kind)
            x, y, w, h, *_ = fit(first[0], cx, bottom, mw, mh)
            USED.add(v['rel'])
            clip = dict(id=vid, src=v['rel'], keyed=v['keyed'], t0=t0, t1=t1, box=(x, y, w, h))
        elif not v:
            NOTES.append('scene %02d: clip %s not on disk yet; the image/SVG morph plays' % (n, vid))
    return '<g class="stage">%s</g>' % svg, cov, clip


def seam(cfg, x, y, w, iid):
    """FUTURE on the same monolith: a seam of light cracks down the glass (stroke-drawn over the second dissolve)."""
    k = w / AV[iid]['w']
    def d(pts):
        return 'M' + ' L '.join('%s %s' % (AR.n(x + px * k), AR.n(y + py * k)) for px, py in pts)
    a0, a1 = D2[0], D2[1] + .05
    m = (a0 + a1) / 2
    out = [_p(d(cfg['seam']), stroke='#FFF6DC', stroke_width='9', opacity='.28', stroke_linecap='round', stroke_linejoin='round', data_dr='%s,%s' % (a0, a1)),
           _p(d(cfg['seam']), stroke='#FFFFFF', stroke_width='2.6', stroke_linecap='round', stroke_linejoin='round', data_dr='%s,%s' % (a0, a1))]
    if cfg.get('seam2'):
        out.append(_p(d(cfg['seam2']), stroke='#FFFFFF', stroke_width='1.8', stroke_linecap='round', data_dr='%s,%s' % (round(m, 3), a1 + .02)))
    return '<g data-nochk="1" class="seam">%s</g>' % ''.join(out)


def phone_keys(k, c, bw, bh):
    """Phones: the object fills the width (scaled up around its centre, capped so it stays in frame)."""
    f = min(1.14, 760 / max(bw, 1), 640 / max(bh, 1))
    if f <= 1.02:
        return None
    def rep(m):
        return 's=%s' % AR.n(float(m.group(1)) * f)
    return re.sub(r's=([\d.]+)', rep, k)


# the five spouts of 31-T, as fractions of the image (measured on the current file)
SPOUTS = [(.495, .404), (.30, .331), (.70, .336)]   # front, left, right wick tips (the front one on the bowl's front lip)


def flames31(x, y, w, h, k, iid):
    a = AV['FL']
    out = []
    times = [0, .36, .4]
    for (fx, fy), t0 in zip(SPOUTS, times):
        H = 58 if t0 == 0 else 46
        fx0, fy0, fx1, fy1 = a['bbox']
        kk = H / max(1, fy1 - fy0)
        X = x + fx * w - (fx0 + fx1) / 2 * kk
        Y = y + fy * h - fy1 * kk
        im = img('FL', X, Y, a['w'] * kk, a['h'] * kk, cls='flick')
        out.append(AR.g(im, k=AR.show(t0, f=.012) if t0 else None))
    return ''.join(out)
