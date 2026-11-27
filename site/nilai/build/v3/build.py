"""Build site/nilai/index.html (Nilai v3) from v3_script_final.md, the v2 file tab and the drawing modules here.

Run: python3 -I site/nilai/build/v3/build.py
Fails (non-zero exit) if any Tamil line does not match kg/core, or any section 6 colour rule fails.
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # -I drops the script directory from sys.path; the modules live beside this file
REPO = HERE.parents[3]
NILAI = REPO / 'site' / 'nilai'

import script_data as SD  # noqa: E402
import art as AR  # noqa: E402
import scenes as SCN  # noqa: E402

FAIL = []


# ---------------------------------------------------------------- colour maths
def hx(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def to_hex(c):
    return '#%02X%02X%02X' % tuple(max(0, min(255, round(v))) for v in c)


def lum(h):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4
    r, g, b = hx(h)
    return .2126 * ch(r) + .7152 * ch(g) + .0722 * ch(b)


def cr(a, b):
    x, y = lum(a), lum(b)
    return (max(x, y) + .05) / (min(x, y) + .05)


def mix(a, b, t):
    A, B = hx(a), hx(b)
    return to_hex(tuple(A[i] + (B[i] - A[i]) * t for i in range(3)))


def lab(h):
    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (841 / 108) * t + 4 / 29
    def lin(v):
        v /= 255
        return v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4
    r, g, b = (lin(v) for v in hx(h))
    X = (r * .4124 + g * .3576 + b * .1805) / .95047
    Y = (r * .2126 + g * .7152 + b * .0722)
    Z = (r * .0193 + g * .1192 + b * .9505) / 1.08883
    return (116 * f(Y) - 16, 500 * (f(X) - f(Y)), 200 * (f(Y) - f(Z)))


def de(a, b):
    return sum((x - y) ** 2 for x, y in zip(lab(a), lab(b))) ** .5


def safe_shade(base, toward, want, bgs, floor_ratio=3.0):
    """Shift base toward a colour by up to `want`, keeping >= floor_ratio against every background."""
    t = want
    while t > 0:
        c = mix(base, toward, t)
        if all(cr(c, b) >= floor_ratio + .05 for b in bgs):
            return c
        t -= .01
    return base


def palette(s):
    P = SD.PAL
    wall, floor, ink, col, acc = P[s['wall']], P[s['floor']], P[s['inkc']], P[s['col']], P[s['acc']]
    tx = P[s['text']]
    bgs = (wall, floor)
    dark = s['dark']
    if dark:   # art is light: highlights go lighter freely, shading darker only as far as contrast allows
        col_hi, col_lo = mix(col, '#FFFFFF', .38), safe_shade(col, '#000000', .2, bgs)
        ink_hi, ink_lo = mix(ink, '#FFFFFF', .5), safe_shade(ink, wall, .22, bgs)
        shadow, glow = '#000000', col
    else:      # art is dark: shading goes darker freely, highlights lighter only as far as contrast allows
        col_hi, col_lo = safe_shade(col, '#FFFFFF', .3, bgs), mix(col, '#000000', .32)
        ink_hi, ink_lo = safe_shade(ink, '#FFFFFF', .28, bgs), mix(ink, '#000000', .4)
        shadow, glow = ink, P['turmeric'] if s['wall'] != 'turmeric' else P['chalk']
    acc_hi = mix(acc, '#FFFFFF', .3) if cr(mix(acc, '#FFFFFF', .3), ink) >= 3 else acc
    sh = dict(wall=wall, floor=floor, tx=tx, ink=ink, col=col, acc=acc, col_hi=col_hi, col_lo=col_lo, ink_hi=ink_hi, ink_lo=ink_lo,
              acc_hi=acc_hi, shadow=shadow, glow=glow, dk=ink if not dark else wall, pp=wall if not dark else ink,
              strip=P[s['strip']], letters=P[s['letters']])
    # section 6 rules
    n = s['n']
    def req(name, v, mn):
        if v < mn - 1e-9:
            FAIL.append('colour %02d %s %.2f < %.2f' % (n, name, v, mn))
    req('wall:floor', cr(wall, floor), 1.6)
    for k in ('ink', 'col', 'ink_hi', 'ink_lo', 'col_hi', 'col_lo'):
        req(k + ':wall', cr(sh[k], wall), 3)
        req(k + ':floor', cr(sh[k], floor), 3)
    req('ink:col', cr(ink, col), 1.5)
    req('ink:col deltaE', de(ink, col), 30)
    req('text:wall', cr(tx, wall), 4.5)
    req('text:floor', cr(tx, floor), 4.5)
    req('accent:ink', cr(acc, ink), 3)
    req('strip', cr(sh['strip'], sh['letters']), 4.5)
    if {s['col'], s['inkc']} & {'teal'} and {s['col'], s['inkc']} & {'kumkum', 'laterite'}:
        FAIL.append('colour %02d teal beside kumkum/laterite' % n)
    return sh


# ---------------------------------------------------------------- Tamil check
def load_book(book):
    p = REPO / 'kg' / 'core' / (book + '.jsonl')
    recs = {}
    for ln in p.open(encoding='utf-8'):
        r = json.loads(ln)
        if 'id' in r:
            recs[r['id']] = r
        if 'verse' in r:
            recs['%s:%s' % (book, r['verse'])] = r
    return recs


BOOKS = {}


def couplets():
    txt = (NILAI / 'kural_final.txt').read_text(encoding='utf-8').strip()
    return [blk.strip().split('\n') for blk in re.split(r'\n\s*\n', txt)]


def tamil_ok(line, rid, part=False):
    if rid.startswith('couplet:'):
        k = int(rid.split(':')[1])
        lines = couplets()[k - 1]
    else:
        book = rid.split(':')[0]
        if book not in BOOKS:
            BOOKS[book] = load_book(book)
        r = BOOKS[book].get(rid)
        if not r:
            return 'id not found'
        lines = r['tamil']
    if line in lines:
        return ''
    if part and any(l.startswith(line) for l in lines):
        return ''
    return 'line not in record'


def check_tamil(S, extra):
    n = 0
    for s in S:
        for ta, rid in s['anc']:
            n += 1
            e = tamil_ok(ta, rid)
            if e:
                FAIL.append('tamil %02d %s: %s | %s' % (s['n'], rid, e, ta))
    for sid, ta, rid in extra:
        n += 1
        e = tamil_ok(ta, rid, part=True)
        if e:
            FAIL.append('tamil %02d %s: %s | %s' % (sid, rid, e, ta))
    return n


# ---------------------------------------------------------------- html bits
def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def sentence(s):
    t = s.strip()
    end = ''
    if t.endswith('.'):
        t = t[:-1]
        end = '<span class="stop" aria-hidden="true"></span><span class="sr">.</span>'
    out = []
    for part in re.split(r'(\*\*.+?\*\*)', t):
        if not part:
            continue
        bold = part.startswith('**')
        words = part.strip('*').split(' ')
        spans = []
        for w in words:
            if w == '':
                spans.append(' ')
                continue
            spans.append('<span class="w">%s</span>' % esc(w))
        html = ' '.join(x for x in spans if x != ' ')
        lead = ' ' if part.startswith(' ') else ''
        trail = ' ' if part.endswith(' ') else ''
        if bold:
            out.append('<b>%s</b>' % html)
        else:
            out.append(lead.strip() + html + trail)
    html = ''
    for i, chunk in enumerate(re.split(r'(\*\*.+?\*\*)', t)):
        pass
    # rebuild keeping spaces exactly
    t = re.sub(r'\*\*(.+?)\*\*([,;:])', r'**\1\2**', t)
    html = re.sub(r'\*\*(.+?)\*\*', lambda m: '\x00' + m.group(1) + '\x01', t)
    res = []
    bold = False
    for tok in re.split(r'(\x00|\x01| )', html):
        if tok == '\x00':
            res.append('<b>')
            continue
        if tok == '\x01':
            res.append('</b>')
            continue
        if tok == ' ':
            res.append(' ')
            continue
        if tok:
            res.append('<span class="w">%s</span>' % esc(tok))
    return ''.join(res) + end


def stub(t, k=3):
    w = t.split()
    return ' '.join(w[:k]) + ('…' if len(w) > k else '')


def margin_html(s, prev_pen):
    n = s['n']
    parts = []
    pen = s['pen'] or {3: 'what if the wrong hands get it?', 21: 'what will creativity be?', 24: 'steer, or be steered?'}.get(n, '')
    if n == 1:
        raw = re.search(r'\*(what if everyone.+?)\*', s['margin_raw']).group(1)
        ws = [w.strip() for w in raw.split(' · ')]
        items = []
        for i, w in enumerate(ws):
            tick = '<span class="tk" data-k="%s">✓</span>' % AR.kf((0, dict(o=0)), (.58 + i * .035, dict(o=0)), (.6 + i * .035, 'b', dict(o=1))) if i < 4 else ''
            items.append('<span class="w5"><span class="full">%s</span><span class="stub">%s</span>%s</span>' % (esc(w), esc(stub(w, 2)), tick))
        parts.append('<p class="pen five" data-k="%s">%s<i>2026 · pencil</i></p>' % (AR.show(.1), ''.join(items)))
        return '<div class="mar">%s</div>' % ''.join(parts)
    strike = n not in (24,) and bool(s['ink'])
    if pen:
        x = '<span class="x" data-k="%s"></span>' % AR.kf((0, dict(sx=0)), (.56, dict(sx=0)), (.62, 'o', dict(sx=1))) if strike else ''
        if n == 24:
            x = '<span class="x ul" data-k="%s"></span>' % AR.kf((0, dict(sx=0)), (.74, dict(sx=0)), (.8, 'o', dict(sx=1)))
        parts.append('<p class="pen" data-k="%s"><span class="full">%s</span><span class="stub">%s</span>%s<i>2026 · pencil</i></p>' % (AR.show(.09), esc(pen), esc(stub(pen)), x))
    if s['ink']:
        chip = '<span class="chip">கற்பனை · imagined</span>' if s['imagined'] else ''
        parts.append('<p class="ink dk-only" data-k="%s"><span class="yr">hand of %s</span>%s%s</p>' % (AR.kf((0, dict(o=0, y=8)), (.6, dict(o=0, y=8)), (.66, 'o', dict(o=1, y=0))), s['hand'], esc(s['ink']), chip))
        ev = SD.dated_event(s['ink'])
        parts.append('<p class="ph" data-k="%s">%s%s</p>' % (AR.kf((0, dict(o=0)), (.6, dict(o=0)), (.66, 'o', dict(o=1))), esc(ev), chip))
    return '<div class="mar">%s</div>' % ''.join(parts) if parts else ''


def anchor_html(s):
    if not s['anc']:
        return ''
    ids = []
    for _, rid in s['anc']:
        if rid not in ids:
            ids.append(rid)
    ta = ''.join('<span lang="ta">%s</span>' % esc(t) for t, _ in s['anc'])
    return ('<details class="anc" data-k="%s"><summary><p class="ta">%s</p><span class="aid">%s</span></summary><p class="rd">%s</p></details>'
            % (AR.kf((0, dict(o=0, y=14)), (.15, dict(o=0, y=14)), (.21, 'o', dict(o=1, y=0))), ta, esc(' · '.join(ids)), esc(s['rd'])))


LED_SCENE = {}

STYLE_ATTRS = ('fill', 'stroke', 'stroke-width', 'stroke-linecap', 'stroke-linejoin', 'opacity', 'vector-effect', 'stroke-dasharray', 'font-size', 'text-anchor')


def compress(html):
    """Move repeated presentation-attribute sets on SVG shapes into CSS classes (same cascade semantics, smaller file)."""
    tag_re = re.compile(r'<(path|circle|ellipse|rect|text)((?: [a-z\-:]+="[^"]*")*)(/?)>')
    attr_re = re.compile(r' ([a-z\-:]+)="([^"]*)"')
    from collections import Counter
    cnt = Counter()
    def key(attrs):
        st = tuple((k, v) for k, v in attrs if k in STYLE_ATTRS)
        return st
    for m in tag_re.finditer(html):
        attrs = attr_re.findall(m.group(2))
        if any(k == 'class' for k, _ in attrs):
            continue
        st = key(attrs)
        if len(st) >= 2:
            cnt[st] += 1
    names = {}
    rules = []
    for i, (st, c) in enumerate(cnt.most_common()):
        if c < 3:
            break
        nm = 'z' + ''.join('abcdefghijklmnopqrstuvwxyz'[int(d)] for d in str(i))
        names[st] = nm
        decl = ';'.join('%s:%s%s' % (k, v, 'px' if k in ('stroke-width', 'font-size') and re.match(r'^[\d.]+$', v) else '') for k, v in st)
        rules.append('.%s{%s}' % (nm, decl))
    def rep(m):
        attrs = attr_re.findall(m.group(2))
        if any(k == 'class' for k, _ in attrs):
            return m.group(0)
        st = key(attrs)
        if st not in names:
            return m.group(0)
        rest = ''.join(' %s="%s"' % (k, v) for k, v in attrs if k not in STYLE_ATTRS)
        return '<%s class="%s"%s%s>' % (m.group(1), names[st], rest, m.group(3))
    return tag_re.sub(rep, html), '\n' + ''.join(rules) + '\n'


def build():
    S, LED, PENCIL = SD.parse(NILAI / 'v3_script_final.md')
    # which ledger line each scene carries
    order = [l[0] for l in LED]
    for s in S:
        if s['led']:
            cat = s['led'].split(' · ')[0]
            LED_SCENE[s['n']] = order.index(cat) + 1
    pals = [palette(s) for s in S]
    extra_ta = list(SCN.EXTRA_TAMIL)
    nta = check_tamil(S, extra_ta)
    # scene markup
    out_sc, out_mk = [], []
    prev_pen = ''
    defs_all = []
    gsets, gdefs = {}, []
    for s, sh in zip(S, pals):
        sid = '%02d' % s['n']
        pk = (s['wall'], s['floor'], s['inkc'], s['col'], s['acc'])
        if pk not in gsets:
            gsets[pk] = 'p%d' % len(gsets)
            gdefs.append(AR.grads(gsets[pk], sh))
        AR.Sc.sid = gsets[pk]
        fn = getattr(SCN, 's' + sid)
        R = fn(s)
        style = ';'.join('--%s:%s' % (k, sh[k]) for k in ('wall', 'floor', 'tx', 'ink', 'col', 'acc', 'dk', 'pp', 'strip', 'letters'))
        art = '<svg class="art" viewBox="0 0 1000 1000" aria-hidden="true" focusable="false">%s</svg>' % R['art']
        led_attr = ''
        if s['n'] in LED_SCENE:
            led_attr = ' data-led="%d" data-ledt="%s"' % (LED_SCENE[s['n']], esc(s['led']))
        tx = '<div class="tx">%s<p class="sent" id="h%s">%s</p>%s%s</div>' % (R.get('pre', ''), sid, sentence(s['sent']), anchor_html(s), R.get('tx', ''))
        mar = R.get('mar') if 'mar' in R else margin_html(s, prev_pen)
        if s['pen']:
            prev_pen = s['pen']
        out_sc.append('<section class="sc3" id="s%s" data-n="%d" data-dur="%s" data-tr="%s" data-fx="%s" data-fy="%s" data-pu="%s" data-h="%s"%s style="%s" aria-labelledby="h%s">'
                      '<div class="wall"></div><div class="floor"></div>%s%s%s%s</section>'
                      % (sid, s['n'], s['dur'], R.get('tr', 'fade'), R.get('fx', 500), R.get('fy', 500), R.get('pu', ''), esc(s['hdr']), led_attr, style, sid,
                         R.get('under', ''), art, tx, mar + R.get('html', '')))
        out_mk.append('<div class="mk" data-for="s%s"></div>' % sid)
    # ledger strip
    slots = ''.join('<i class="sl" style="top:%.1f%%"></i>' % (18 + i * 64 / 12) for i in range(13))
    strip = '<div class="strip" id="strip" aria-hidden="true"><div class="leaf"></div><span class="cap">nilai</span>%s</div>' % slots
    card = '<div class="ledcard" id="ledCard" aria-hidden="true"><small>LEDGER · WHAT WE UPHOLD</small><span id="ledCardT"></span></div>'
    wipes = '<div class="wipe mat" id="wipeMat" aria-hidden="true"></div><svg class="wipe leaf" id="wipeLeaf" viewBox="0 0 1000 160" preserveAspectRatio="none" aria-hidden="true"><path d="M0 80 C 120 10 380 0 500 0 C 640 0 880 14 1000 80 C 880 146 640 160 500 160 C 380 160 120 150 0 80 Z" fill="#CDAE78" stroke="#171C45" stroke-width="3"/><path d="M20 80 L 980 80" stroke="#8a6d3d" stroke-width="3"/><path d="M100 60 L 900 62 M100 100 L900 98" stroke="#a8895a" stroke-width="1.5"/><circle cx="300" cy="80" r="9" fill="#171C45"/><circle cx="700" cy="80" r="9" fill="#171C45"/></svg>'
    reel = ('<div class="reel" id="reel" aria-label="Nilai, the reel: the hand of 2526 writes back, in 31 scenes">'
            '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>%s%s</defs></svg>'
            '<div class="vp" id="vp">%s</div>%s%s<i class="pulli" id="pulli" aria-hidden="true"></i>%s<div class="spacer" id="spacer">%s</div></div>'
            % (AR.filters() + ''.join(gdefs), AR.symbols(), ''.join(out_sc), strip, card, wipes, ''.join(out_mk)))
    # the v2 file tab, carried over unchanged
    v2 = (NILAI / 'v2' / 'index.html').read_text(encoding='utf-8')
    head_end = v2.index('<style>')
    head = v2[:head_end]
    css_all = v2[v2.index('<style>') + 7:v2.index('</style>')]
    css_file = css_all[:css_all.index('/* ===== the reel (default tab)')]
    main = v2[v2.index('<main class="gut" id="top">'):v2.index('</main>') + 7]
    scripts = re.findall(r'<script>(.*?)</script>', v2[v2.index('</main>'):], re.S)
    file_js = scripts[0]
    header = v2[v2.index('<header class="bar">'):v2.index('</header>') + 9]
    header = header.replace('<span class="rhead" id="reelHead" aria-hidden="true">## what this file is</span>',
                            '<span class="rhead" id="reelHead" aria-live="polite">%s</span><span class="rcnt" id="reelCnt" aria-hidden="true">01/31</span>' % esc(S[0]['hdr']))
    header = header.replace('<li><a href="#colophon"><span>··</span>how this was made</a></li>',
                            '<li><a href="#colophon"><span>··</span>how this was made</a></li>\n        <li><a href="v2/index.html#reel"><span>~</span>v2 reel (archive)</a></li>')
    assert 'v2 reel (archive)' in header and 'reelCnt' in header
    reel, zcss = compress(reel)
    css = css_file + (HERE / 'reel.css').read_text(encoding='utf-8') + SCN.CSS + zcss
    js = (HERE / 'reel.js').read_text(encoding='utf-8')
    page = '%s<style>\n%s</style>\n\n%s\n\n%s\n\n%s\n\n<script>%s</script>\n<script>\n%s</script>\n' % (head, css, header, reel, main.replace('<main class="gut" id="top">', '<main class="gut" id="top" hidden>'), file_js, js)
    assert page.startswith('<title>Nilai</title>\n<meta name="claude:viewport-fit-sides" content="cover">')
    for bad in ('window.open', 'alert(', 'print(', '.print('):
        if bad in js or bad in SCN.CSS:
            FAIL.append('forbidden call in reel js: ' + bad)
    if FAIL:
        print('BUILD FAILED')
        for f in FAIL:
            print('  ' + f)
        sys.exit(1)
    (NILAI / 'index.html').write_text(page, encoding='utf-8')
    kb = len(page.encode('utf-8')) / 1024
    print('wrote site/nilai/index.html  %.0f KB  (%d Tamil lines matched, 31 scenes, colour rules pass)' % (kb, nta))
    sizes = sorted(((len(x.encode('utf-8')) / 1024, x[:60]) for x in out_sc), reverse=True)[:6]
    print('largest scenes: ' + ', '.join('%s %.0fKB' % (re.search(r'id="(s\d+)"', t).group(1), k) for k, t in sizes))


if __name__ == '__main__':
    build()
