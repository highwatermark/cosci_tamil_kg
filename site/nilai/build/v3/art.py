"""Drawing library for the Nilai v3 reel. Stdlib only.

Conventions
- Art space is a 1000 x 1000 viewBox; the horizon (wall meets floor) is at y = GY.
- Colours are scene tokens: I ink, C colour, A accent, W wall, F floor, DK dark fill, PP paper fill.
  DK/PP are whichever of ink/wall is dark/light, so a character reads in both wall groups.
- Anything animated is a <g data-k="..."> wrapper with no static transform; the engine writes its transform.
  Keyframe strings: "t[e]:p=v,p=v;..." with props o x y s sx sy r, easing letter on the arriving key
  (l linear, i in-out, o out, b out-back, n in, s step).
- Morphs: morph(polys) resamples every outline to the same point count and emits d strings with one skeleton,
  so the engine can interpolate the numbers in the d attribute.
"""
import math

GY = 760
I, C, A, W, F, DK, PP = ('var(--ink)', 'var(--col)', 'var(--acc)', 'var(--wall)', 'var(--floor)', 'var(--dk)', 'var(--pp)')
T = dict(i0=.06, i1=.17, m1a=.31, m1b=.46, m2a=.55, m2b=.70, g0=.74, g1=.92)


def n(x):
    s = '%.1f' % x
    if s.endswith('.0'):
        s = s[:-2]
    return '0' if s == '-0' else s


def attrs(kw):
    out = []
    for k, v in kw.items():
        if v is None or v is False:
            continue
        k = k.rstrip('_').replace('__', ':').replace('_', '-')
        if isinstance(v, float):
            v = n(v)
        out.append('%s="%s"' % (k, v))
    return (' ' + ' '.join(out)) if out else ''


def tag(name, inner=None, **kw):
    if inner is None:
        return '<%s%s/>' % (name, attrs(kw))
    return '<%s%s>%s</%s>' % (name, attrs(kw), inner, name)


def path(d, **kw):
    if 'fill' not in kw and 'stroke' in kw:
        kw['fill'] = 'none'
    return tag('path', d=d, **kw)


def g(inner, k=None, kp=None, c=None, cls=None, **kw):
    """A group; with k it becomes an animated wrapper (transform owned by the engine)."""
    if isinstance(inner, (list, tuple)):
        inner = ''.join(inner)
    if isinstance(c, tuple):
        c = '%s %s' % (n(c[0]), n(c[1]))
    if (k or kp) and kw.get('transform'):
        inner = tag('g', inner, transform=kw.pop('transform'))
    return tag('g', inner, data_k=k, data_kp=kp, data_c=c, class_=cls, **kw)


def at(x, y, inner, s=1, r=0, flip=False, **kw):
    """Static placement."""
    tr = 'translate(%s %s)' % (n(x), n(y))
    if r:
        tr += ' rotate(%s)' % n(r)
    if s != 1 or flip:
        tr += ' scale(%s %s)' % (n(-s if flip else s), n(s))
    return g(inner, transform=tr, **kw)


def text(x, y, s, size=24, fill=I, anchor='start', fam='hand', weight=None, bg='pp', **kw):
    fams = {'hand': 'var(--f-hand)', 'mono': 'var(--f-md)', 'disp': 'var(--f-disp)', 'ta': 'var(--f-ta)', 'serif': 'var(--f-body)'}
    return tag('text', esc(s), x=n(x), y=n(y), font_size=n(size), fill=fill, text_anchor=anchor,
               style='font-family:%s' % fams[fam] + (';font-weight:%s' % weight if weight else ''), data_bg=bg, **kw)


def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# ---------------------------------------------------------------- geometry

def lerp(a, b, t):
    return a + (b - a) * t


def rot(p, a, o=(0, 0)):
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    x, y = p[0] - o[0], p[1] - o[1]
    return (o[0] + x * ca - y * sa, o[1] + x * sa + y * ca)


def ellipse_pts(cx, cy, rx, ry, k=48, a0=-90):
    return [(cx + rx * math.cos(math.radians(a0 + 360 * i / k)), cy + ry * math.sin(math.radians(a0 + 360 * i / k))) for i in range(k)]


def rrect_pts(x, y, w, h, r, k=6):
    r = min(r, w / 2, h / 2)
    pts = []
    corners = [(x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)]
    # start at top centre, clockwise
    pts.append((x + w / 2, y))
    for cx, cy, a0 in corners:
        for i in range(k + 1):
            a = math.radians(a0 + 90 * i / k)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def mirror(half):
    """half: points from top centre down the RIGHT side to bottom centre. Returns a closed outline."""
    right = list(half)
    left = [(2 * right[0][0] - x, y) for x, y in reversed(right[1:-1])]
    return right + left


def _area(pts):
    a = 0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        a += x1 * y2 - x2 * y1
    return a / 2


def resample(pts, k, closed=True):
    seg = pts + [pts[0]] if closed else list(pts)
    L = [0.0]
    for i in range(1, len(seg)):
        L.append(L[-1] + math.dist(seg[i - 1], seg[i]))
    tot = L[-1] or 1
    out = []
    j = 0
    cnt = k if closed else k - 1
    for i in range(k):
        d = tot * i / cnt
        while j < len(L) - 2 and L[j + 1] < d:
            j += 1
        span = (L[j + 1] - L[j]) or 1
        t = (d - L[j]) / span
        out.append((lerp(seg[j][0], seg[j + 1][0], t), lerp(seg[j][1], seg[j + 1][1], t)))
    return out


def _canon(pts):
    """Clockwise in screen space (positive shoelace with y down), starting at the top point nearest the centre line."""
    if _area(pts) < 0:
        pts = [pts[0]] + list(reversed(pts[1:]))
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    best = min(range(len(pts)), key=lambda i: abs(math.atan2(pts[i][0] - cx, -(pts[i][1] - cy))))
    return pts[best:] + pts[:best]


def cubic(pts, closed=True, tension=1.0, prec=1):
    """Catmull-Rom through pts as cubic Beziers; tension 0 gives straight segments (still C commands)."""
    k = len(pts)
    nn = n if prec else (lambda v: str(int(round(v))))
    s = tension / 6
    d = ['M%s %s' % (nn(pts[0][0]), nn(pts[0][1]))]
    rng = range(k) if closed else range(k - 1)
    for i in rng:
        p0 = pts[(i - 1) % k] if closed else pts[max(i - 1, 0)]
        p1 = pts[i]
        p2 = pts[(i + 1) % k]
        p3 = pts[(i + 2) % k] if closed else pts[min(i + 2, k - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) * s, p1[1] + (p2[1] - p0[1]) * s)
        c2 = (p2[0] - (p3[0] - p1[0]) * s, p2[1] - (p3[1] - p1[1]) * s)
        if tension == 0:
            c1 = (lerp(p1[0], p2[0], 1 / 3), lerp(p1[1], p2[1], 1 / 3))
            c2 = (lerp(p1[0], p2[0], 2 / 3), lerp(p1[1], p2[1], 2 / 3))
        d.append('C%s %s %s %s %s %s' % tuple(nn(v) for v in (*c1, *c2, *p2)))
    if closed:
        d.append('Z')
    return ''.join(d)


def outline(pts, k=64, tension=1.0, canon=True):
    p = resample(pts, k)
    if canon:
        p = _canon(p)
    return cubic(p, True, tension)


def morph(polys, k=64, tension=1.0, closed=True, prec=0):
    """d strings with one skeleton for a list of outlines (closed) or polylines (open)."""
    out = []
    for i, pts in enumerate(polys):
        t = tension[i] if isinstance(tension, (list, tuple)) else tension
        if closed:
            p = _canon(resample(pts, k))
            out.append(cubic(p, True, t, prec))
        else:
            p = resample(pts, k, closed=False)
            out.append(cubic(p, False, t, prec))
    return out


def mpath(polys, times, k=48, tension=1.0, closed=True, **kw):
    """A morphing path: shape i is reached at times[i]. Consecutive repeats of one outline become a hold."""
    P, TT = [], []
    for pts, t in zip(polys, times):
        if P and pts is P[-1]:
            TT[-1] = (TT[-1][0], t)
            continue
        P.append(pts)
        TT.append((t, t))
    tens = tension
    ds = morph(P, k, tens, closed)
    mt = ','.join(n2(a) if a == b else '%s-%s' % (n2(a), n2(b)) for a, b in TT)
    return path(ds[0], data_m='|'.join(ds), data_mt=mt, **kw)


def n2(x):
    return ('%.3f' % x).rstrip('0').rstrip('.')


def poly(pts):
    return 'M' + ' L'.join('%s %s' % (n(x), n(y)) for x, y in pts) + ' Z'


def line(pts):
    return 'M' + ' L'.join('%s %s' % (n(x), n(y)) for x, y in pts)


def smooth(pts, closed=False, tension=1.0):
    return cubic(pts, closed, tension)


def kf(*frames):
    """kf((t, 'b', dict(o=1, y=0)), ...) -> keyframe string."""
    out = []
    for fr in frames:
        if len(fr) == 2:
            t, props = fr
            e = ''
        else:
            t, e, props = fr
        out.append('%s%s:%s' % (n2(t), e, ','.join('%s=%s' % (k, n(v) if isinstance(v, float) else v) for k, v in props.items())))
    return ';'.join(out)


def pop(t, dur=.08, dy=40, s0=.6):
    """Staggered entrance with an out-back overshoot."""
    return kf((0, dict(o=0, y=dy, s=s0)), (t, dict(o=0, y=dy, s=s0)), (t + dur, 'b', dict(o=1, y=0, s=1)))


def show(t0, t1=None, f=.04):
    """Fade in at t0 (and out at t1)."""
    fr = [(0, dict(o=0)), (t0, dict(o=0)), (t0 + f, 'o', dict(o=1))]
    if t1 is not None:
        fr += [(t1, dict(o=1)), (t1 + f, 'o', dict(o=0))]
    return kf(*fr)


def swing(t0, t1, a, decay=.55, steps=6, base=0):
    """Decaying oscillation keyframes for the r prop."""
    fr = [(0, dict(r=base + a)), (t0, dict(r=base + a))]
    for i in range(1, steps + 1):
        fr.append((t0 + (t1 - t0) * i / steps, 'i', dict(r=base + a * ((-decay) ** i))))
    fr.append((t1 + .001, dict(r=base)))
    return fr


# ---------------------------------------------------------------- page-level defs

def filters():
    return '''<filter id="fpaper" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="3" seed="3" result="t"/><feDisplacementMap in="SourceGraphic" in2="t" scale="5" xChannelSelector="R" yChannelSelector="G"/></filter>
<filter id="fgrain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="7" result="n"/><feColorMatrix in="n" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -1.4 .78" result="a"/><feComposite in="a" in2="SourceGraphic" operator="in" result="s"/><feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="s"/></feMerge></filter>
<filter id="fbrass" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".004 .09" numOctaves="2" seed="11" result="n"/><feGaussianBlur in="SourceAlpha" stdDeviation="3" result="b"/><feSpecularLighting in="b" surfaceScale="4" specularConstant=".7" specularExponent="18" lighting-color="#fff" result="sp"><feDistantLight azimuth="235" elevation="48"/></feSpecularLighting><feComposite in="sp" in2="SourceAlpha" operator="in" result="sp2"/><feComposite in="n" in2="SourceAlpha" operator="in" result="n2"/><feColorMatrix in="n2" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .45 0" result="n3"/><feComposite in="SourceGraphic" in2="sp2" operator="arithmetic" k2="1" k3=".32"/><feComposite in2="n3" operator="over"/><feComposite in2="SourceAlpha" operator="in"/></filter>
<filter id="fglow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="fsoft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5"/></filter>
<filter id="fb1"><feGaussianBlur stdDeviation="1.6"/></filter><filter id="fb2"><feGaussianBlur stdDeviation="3.4"/></filter><filter id="fb3"><feGaussianBlur stdDeviation="6"/></filter>'''


def grads(sid, sh):
    """Per-scene gradients; sh holds hex values computed (and contrast-checked) by build.py."""
    p = 'g%s' % sid
    def st(o, c, a=1):
        return '<stop offset="%s" stop-color="%s"%s/>' % (o, c, '' if a == 1 else ' stop-opacity="%s"' % a)
    return ''.join([
        '<linearGradient id="%sc" x1="0" y1="0" x2="0" y2="1">%s%s%s</linearGradient>' % (p, st(0, sh['col_hi']), st(.45, sh['col']), st(1, sh['col_lo'])),
        '<linearGradient id="%sch" x1="0" y1="0" x2="1" y2="0">%s%s%s%s</linearGradient>' % (p, st(0, sh['col_lo']), st(.3, sh['col_hi']), st(.62, sh['col']), st(1, sh['col_lo'])),
        '<linearGradient id="%si" x1="0" y1="0" x2="0" y2="1">%s%s%s</linearGradient>' % (p, st(0, sh['ink_hi']), st(.5, sh['ink']), st(1, sh['ink_lo'])),
        '<linearGradient id="%sih" x1="0" y1="0" x2="1" y2="0">%s%s%s%s</linearGradient>' % (p, st(0, sh['ink_lo']), st(.32, sh['ink_hi']), st(.65, sh['ink']), st(1, sh['ink_lo'])),
        '<radialGradient id="%sr" cx=".38" cy=".32" r=".75">%s%s%s</radialGradient>' % (p, st(0, sh['col_hi']), st(.55, sh['col']), st(1, sh['col_lo'])),
        '<radialGradient id="%sri" cx=".38" cy=".32" r=".75">%s%s%s</radialGradient>' % (p, st(0, sh['ink_hi']), st(.55, sh['ink']), st(1, sh['ink_lo'])),
        '<radialGradient id="%sa" cx=".5" cy=".6" r=".6">%s%s</radialGradient>' % (p, st(0, sh['acc_hi']), st(1, sh['acc'])),
        '<radialGradient id="%ssh" cx=".5" cy=".5" r=".5">%s%s</radialGradient>' % (p, st(0, sh['shadow'], .55), st(1, sh['shadow'], 0)),
        '<radialGradient id="%sgl" cx=".5" cy=".5" r=".5">%s%s</radialGradient>' % (p, st(0, sh['glow'], .55), st(1, sh['glow'], 0)),
        '<linearGradient id="%sfl" x1="0" y1="0" x2="0" y2="1">%s%s</linearGradient>' % (p, st(0, sh['shadow'], .22), st(.35, sh['shadow'], 0)),
    ])


class Sc:
    """Gradient references for the scene being drawn (set by build.py before each scene function runs).
    In plain mode (shared symbols) the gradients fall back to the flat tokens, which any scene can supply."""
    sid = '00'
    plain = False
    FLAT = {'c': 'var(--col)', 'ch': 'var(--col)', 'r': 'var(--col)', 'i': 'var(--ink)', 'ih': 'var(--ink)', 'ri': 'var(--ink)', 'a': 'var(--acc)'}

    @classmethod
    def u(cls, k):
        if cls.plain and k in cls.FLAT:
            return cls.FLAT[k]
        return 'url(#g%s%s)' % (cls.sid, k)


SYM = {}


def sym(key, fn):
    """Draw once into the shared defs, reuse with <use>."""
    import hashlib
    key = 'u' + hashlib.md5(key.encode()).hexdigest()[:8]
    if key not in SYM:
        was = Sc.plain
        Sc.plain = True
        SYM[key] = tag('g', fn(), id=key)
        Sc.plain = was
    return '<use href="#%s"/>' % key


def symbols():
    return ''.join(SYM.values())


def GC(): return Sc.u('c')
def GCH(): return Sc.u('ch')
def GI(): return Sc.u('i')
def GIH(): return Sc.u('ih')
def GR(): return Sc.u('r')
def GRI(): return Sc.u('ri')
def GA(): return Sc.u('a')


def shadow(cx, cy, rx, ry=None, **kw):
    ry = ry or rx * .16
    return tag('ellipse', cx=n(cx), cy=n(cy), rx=n(rx), ry=n(ry), fill=Sc.u('sh'), class_='sh', **kw)


def glow(cx, cy, r, **kw):
    return tag('circle', cx=n(cx), cy=n(cy), r=n(r), fill=Sc.u('gl'), class_='fx', **kw)


def kl(d, w=1.5, col=W):
    """Keyline in the wall colour (non-scaling)."""
    return path(d, fill='none', stroke=col, stroke_width=w, vector_effect='non-scaling-stroke', stroke_linejoin='round')


def body(d, fill=None, stroke=W, sw=1.5, **kw):
    """A filled art shape with its wall-colour keyline."""
    return path(d, fill=fill or GC(), stroke=stroke, stroke_width=sw, vector_effect='non-scaling-stroke', stroke_linejoin='round', **kw)


def inkline(d, w=3, col=I, **kw):
    return path(d, fill='none', stroke=col, stroke_width=w, stroke_linecap='round', stroke_linejoin='round', **kw)


def circle(cx, cy, r, **kw):
    return tag('circle', cx=n(cx), cy=n(cy), r=n(r), **kw)


def rect(x, y, w, h, rx=0, **kw):
    return tag('rect', x=n(x), y=n(y), width=n(w), height=n(h), rx=n(rx) if rx else None, **kw)


def ell(cx, cy, rx, ry, **kw):
    return tag('ellipse', cx=n(cx), cy=n(cy), rx=n(rx), ry=n(ry), **kw)


# ---------------------------------------------------------------- characters

def _limb(p0, a1, l1, a2, l2, w, fill, outline=DK, ow=4.5):
    """Two-segment limb from p0; angles in degrees from straight down, positive = forward (+x)."""
    k = (p0[0] + l1 * math.sin(math.radians(a1)), p0[1] + l1 * math.cos(math.radians(a1)))
    e = (k[0] + l2 * math.sin(math.radians(a2)), k[1] + l2 * math.cos(math.radians(a2)))
    d = line([p0, k, e])
    return (path(d, fill='none', stroke=outline, stroke_width=n(w + ow), stroke_linecap='round', stroke_linejoin='round') +
            path(d, fill='none', stroke=fill, stroke_width=n(w), stroke_linecap='round', stroke_linejoin='round')), k, e


POSES = {
    #        back arm (upper, fore)  front arm         back leg (thigh, shin)  front leg     lean  head
    'stand':   dict(ba=(-8, -4),   fa=(8, 14),     bl=(-3, -3),  fl=(4, 4),    lean=0, head=0),
    'walk1':   dict(ba=(-26, -14), fa=(26, 44),    bl=(-24, -34), fl=(22, 10), lean=3, head=0),
    'walk2':   dict(ba=(22, 38),   fa=(-22, -10),  bl=(20, 6),   fl=(-22, -36), lean=3, head=0),
    'point':   dict(ba=(-10, -4),  fa=(96, 104),   bl=(-6, -6),  fl=(8, 8),    lean=2, head=-4),
    'pointup': dict(ba=(-10, -4),  fa=(140, 150),  bl=(-6, -6),  fl=(8, 8),    lean=-3, head=-14),
    'write':   dict(ba=(30, 70),   fa=(40, 96),    bl=(-4, -4),  fl=(6, 6),    lean=10, head=16),
    'hold':    dict(ba=(40, 92),   fa=(52, 100),   bl=(-4, -4),  fl=(5, 5),    lean=2, head=4),
    'holdup':  dict(ba=(120, 160), fa=(130, 172),  bl=(-4, -4),  fl=(5, 5),    lean=-2, head=-10),
    'startle': dict(ba=(-140, -170), fa=(140, 170), bl=(-14, -4), fl=(12, 4),  lean=-6, head=-8),
    'delight': dict(ba=(-150, -160), fa=(150, 160), bl=(-6, -6), fl=(8, 8),    lean=-4, head=-10),
    'lean':    dict(ba=(70, 100),  fa=(78, 104),   bl=(-30, -30), fl=(-10, -16), lean=24, head=6),
    'carry':   dict(ba=(150, 175), fa=(155, 178),  bl=(-14, -18), fl=(16, 8),  lean=0, head=-4),
    'reach':   dict(ba=(-12, -6),  fa=(70, 64),    bl=(-8, -8),  fl=(10, 10),  lean=8, head=6),
    'listen':  dict(ba=(20, 70),   fa=(30, 120),   bl=(-10, -10), fl=(10, 10), lean=14, head=24),
    'kneel':   dict(ba=(20, 50),   fa=(50, 90),    bl=(-90, 0),  fl=(80, -6),  lean=8, head=10, drop=60),
    'sit':     dict(ba=(10, 50),   fa=(20, 70),    bl=(80, 0),   fl=(88, 4),   lean=0, head=0, drop=78),
    'cross':   dict(ba=(20, 60),   fa=(30, 80),    bl=(84, -84), fl=(80, -92), lean=4, head=4, drop=150),
    'serve':   dict(ba=(-10, -6),  fa=(60, 100),   bl=(-6, -6),  fl=(8, 8),    lean=14, head=12),
    'lie':     dict(ba=(160, 30),  fa=(165, 20),   bl=(-4, -4),  fl=(4, 10),   lean=0, head=0),
    'paddle':  dict(ba=(60, 150),  fa=(40, 90),    bl=(80, 0),   fl=(88, 4),   lean=10, head=0, drop=78),
}


SPRITE = None   # set by build.py: stage.sprite(kind, pose, anim, s, flip, extra) -> svg or None


def keeper(pose='stand', expr='calm', s=1.0, flip=False, hold='', who='keeper', look=0, anim=None, stylus=True):
    """The keeper: a marble sprite where the pose exists (build.py sets SPRITE), else the vector figure."""
    if who != 'keeper' or Sc.plain:
        return _keeper(pose, expr, s, flip, hold, who, look, anim, stylus)
    if SPRITE and not hold:
        r = SPRITE('K', pose, anim, s, flip)
        if r:
            return r
    return g(_keeper(pose, expr, s, flip, hold, who, look, anim, stylus), data_chr='1')


def _keeper(pose='stand', expr='calm', s=1.0, flip=False, hold='', who='keeper', look=0, anim=None, stylus=True):
    """The keeper (and other people, by `who`). Feet at (0,0), about 380 tall at s=1.

    anim: optional list of (t, posename) to animate joints with scroll keyframes.
    """
    if not anim and not Sc.plain:
        k = 'K|%s|%s|%s|%s|%s|%s' % (pose, expr, hold, who, look, stylus)
        u = sym(k, lambda: keeper(pose, expr, 1.0, False, hold, who, look, anim, stylus))
        return g(u, transform='scale(%s %s)' % (n(-s if flip else s), n(s))) if (s != 1 or flip) else u
    P = dict(POSES[pose]) if isinstance(pose, str) else dict(pose)
    drop = P.get('drop', 0)
    lean = P['lean']
    hip = (0, -170 + drop)
    sh_y = -288 + drop
    # outfit per person
    o = PEOPLE.get(who, PEOPLE['keeper'])
    lw, aw = o['lw'], o['aw']
    tunic = _fill(o['tunic'])
    parts = []

    def joint_anim(name, idx, default):
        if not anim:
            return None
        fr = []
        for t, pn in anim:
            pp = POSES[pn] if isinstance(pn, str) else pn
            fr.append((t, dict(r=pp[name][idx] - default)))
        return fr

    def limb(name, origin, w, fill, back):
        a1, a2 = P[name]
        L1, L2 = (62, 58) if name in ('ba', 'fa') else (84, 80)
        if name in ('bl', 'fl') and drop:
            pass
        # draw straight down, rotate by joints (so animation can rotate the same groups)
        fill = _fill(fill)
        ol = I if fill == DK else DK
        up = path(line([(origin[0], origin[1]), (origin[0], origin[1] + L1)]), fill='none', stroke=ol, stroke_width=n(w + 4.5), stroke_linecap='round')
        up += path(line([(origin[0], origin[1]), (origin[0], origin[1] + L1)]), fill='none', stroke=fill, stroke_width=n(w), stroke_linecap='round')
        lo = path(line([(origin[0], origin[1] + L1), (origin[0], origin[1] + L1 + L2)]), fill='none', stroke=ol, stroke_width=n(w + 4.5), stroke_linecap='round')
        lo += path(line([(origin[0], origin[1] + L1), (origin[0], origin[1] + L1 + L2)]), fill='none', stroke=fill, stroke_width=n(w - 1), stroke_linecap='round')
        ex = (origin[0], origin[1] + L1 + L2)
        if name in ('ba', 'fa'):
            lo += circle(ex[0], ex[1] + 2, w * .62 + 2.2, fill=DK) + circle(ex[0], ex[1] + 2, w * .62, fill=PP)
            if name == 'fa' and hold:
                lo += at(ex[0], ex[1] + 4, hold)
        else:
            lo += path('M%s %s q 6 -9 26 -3 q 6 3 0 8 l -28 1 z' % (n(ex[0] - 4), n(ex[1] - 2)), fill=_fill(o['foot']), stroke=DK if _fill(o['foot']) != DK else I, stroke_width=3.5, stroke_linejoin='round')
        lower_rot = a2 - a1
        if anim:
            lo_g = g(lo, k=kf(*[(t, dict(r=-((POSES[pn] if isinstance(pn, str) else pn)[name][1] - (POSES[pn] if isinstance(pn, str) else pn)[name][0]))) for t, pn in anim]), c=(origin[0], origin[1] + L1))
            up_g = g(up + lo_g, k=kf(*[(t, dict(r=-(POSES[pn] if isinstance(pn, str) else pn)[name][0])) for t, pn in anim]), c=origin)
        else:
            lo_g = g(lo, transform='rotate(%s %s %s)' % (n(-lower_rot), n(origin[0]), n(origin[1] + L1)))
            up_g = g(up + lo_g, transform='rotate(%s %s %s)' % (n(-a1), n(origin[0]), n(origin[1])))
        return up_g

    ba = limb('ba', (-14, sh_y + 6), aw, PP, True)
    bl = limb('bl', (-8, hip[1]), lw, o['leg'], True)
    fl = limb('fl', (8, hip[1]), lw, o['leg'], False)
    fa = limb('fa', (14, sh_y + 6), aw, PP, False)
    # torso / tunic
    hem = hip[1] + o['hem']
    tun = path('M-30 %s C -36 %s -40 %s -44 %s L 44 %s C 40 %s 36 %s 30 %s Q 0 %s -30 %s Z' % (
        n(sh_y), n(sh_y + 50), n(hem - 60), n(hem), n(hem), n(hem - 60), n(sh_y + 50), n(sh_y), n(sh_y - 8), n(sh_y)),
        fill=tunic, stroke=DK, stroke_width=4, stroke_linejoin='round')
    tun += path('M-41 %s L 41 %s' % (n(hem - 14), n(hem - 14)), stroke=PP, stroke_width=3, stroke_dasharray='2 7', stroke_linecap='round', fill='none')
    tun += path('M-36 %s Q 0 %s 36 %s' % (n(hip[1] - 4), n(hip[1] + 4), n(hip[1] - 4)), stroke=DK, stroke_width=4, fill='none')
    tun += path('M-14 %s Q 0 %s 14 %s' % (n(sh_y - 2), n(sh_y + 18), n(sh_y - 2)), stroke=DK, stroke_width=3, fill='none')
    if o.get('drape'):
        tun += path('M24 %s Q -10 %s -40 %s' % (n(sh_y), n(sh_y + 70), n(hem - 6)), stroke=PP, stroke_width=5, fill='none', opacity='.9')
    # head
    hy = sh_y - 50
    head = _head(hy, expr, o, stylus and who == 'keeper', look)
    head_g = g(head, transform='rotate(%s 0 %s)' % (n(P['head']), n(sh_y - 10))) if not anim else g(head, k=kf(*[(t, dict(r=(POSES[pn] if isinstance(pn, str) else pn)['head'])) for t, pn in anim]), c=(0, sh_y - 10))
    neck = path(line([(0, sh_y - 16), (0, sh_y + 4)]), stroke=DK, stroke_width=20, stroke_linecap='round') + path(line([(0, sh_y - 16), (0, sh_y + 4)]), stroke=PP, stroke_width=13, stroke_linecap='round')
    torso = g([ba, bl, fl, tun, neck, head_g, fa], cls='breathe')
    if anim:
        torso_g = g(torso, k=kf(*[(t, dict(r=(POSES[pn] if isinstance(pn, str) else pn)['lean'], y=(POSES[pn] if isinstance(pn, str) else pn).get('drop', 0) * 0)) for t, pn in anim]), c=(0, hip[1]))
    else:
        torso_g = g(torso, transform='rotate(%s 0 %s)' % (n(lean), n(hip[1])))
    tr = 'scale(%s %s)' % (n(-s if flip else s), n(s))
    return g(torso_g, transform=tr)


PEOPLE = {
    'keeper': dict(tunic=GC, leg=DK, foot=PP, lw=20, aw=15, hem=58, hair='bob'),
    'friend': dict(tunic=GC, leg=GC, foot=PP, lw=16, aw=12, hem=150, hair='braid', drape=True),
    'woman': dict(tunic=GC, leg=GC, foot=PP, lw=16, aw=12, hem=150, hair='bun', drape=True),
    'old': dict(tunic=GC, leg=GC, foot=PP, lw=16, aw=12, hem=150, hair='bun', drape=True, old=True),
    'man': dict(tunic=GC, leg=PP, foot=PP, lw=18, aw=14, hem=70, hair='short', beard=True),
    'bard': dict(tunic=GC, leg=PP, foot=PP, lw=18, aw=14, hem=150, hair='turban', beard=True),
    'doc': dict(tunic=GC, leg=DK, foot=PP, lw=17, aw=14, hem=90, hair='short'),
}
for _v in PEOPLE.values():
    if callable(_v['tunic']):
        _v['tunic_f'] = _v['tunic']


def _fill(v):
    return v() if callable(v) else v


def _head(hy, expr, o, stylus, look):
    hs = []
    hair = o['hair']
    # back hair
    if hair == 'bob':
        hs.append(path('M-40 %s C -46 %s -30 %s 2 %s C 34 %s 44 %s 40 %s L 38 %s C 30 %s 10 %s -6 %s C -26 %s -40 %s -40 %s Z' % (
            n(hy + 6), n(hy - 44), n(hy - 50), n(hy - 50), n(hy - 50), n(hy - 30), n(hy - 4), n(hy + 4), n(hy - 18), n(hy - 22), n(hy - 18),
            n(hy + 28), n(hy + 30), n(hy + 6)), fill=DK, stroke=I, stroke_width=2.5))
    elif hair == 'braid':
        hs.append(path('M-36 %s C -40 %s -20 %s 4 %s C 30 %s 40 %s 36 %s L -36 %s Z' % (n(hy), n(hy - 44), n(hy - 48), n(hy - 48), n(hy - 48), n(hy - 30), n(hy - 2), n(hy)), fill=DK, stroke=I, stroke_width=2.5))
        hs.append(path('M-30 %s C -52 %s -46 %s -40 %s' % (n(hy + 6), n(hy + 60), n(hy + 110), n(hy + 160)), stroke=DK, stroke_width=14, fill='none', stroke_linecap='round'))
        hs.append(path('M-30 %s C -52 %s -46 %s -40 %s' % (n(hy + 6), n(hy + 60), n(hy + 110), n(hy + 160)), stroke=I, stroke_width=2, stroke_dasharray='6 8', fill='none'))
    elif hair == 'bun':
        hs.append(circle(-36, hy - 22, 16, fill=DK, stroke=I if not o.get('old') else PP, stroke_width=2.5))
        hs.append(path('M-38 %s C -40 %s -20 %s 4 %s C 30 %s 40 %s 36 %s L -38 %s Z' % (n(hy), n(hy - 42), n(hy - 46), n(hy - 46), n(hy - 46), n(hy - 30), n(hy - 4), n(hy)), fill=PP if o.get('old') else DK, stroke=DK if o.get('old') else I, stroke_width=3))
    elif hair == 'turban':
        hs.append(path('M-38 %s C -44 %s -20 %s 6 %s C 34 %s 44 %s 38 %s Z' % (n(hy - 8), n(hy - 56), n(hy - 62), n(hy - 62), n(hy - 60), n(hy - 40), n(hy - 10)), fill=GC(), stroke=DK, stroke_width=3.5))
        hs.append(path('M-36 %s Q 0 %s 38 %s M-34 %s Q 2 %s 36 %s' % (n(hy - 22), n(hy - 40), n(hy - 30), n(hy - 36), n(hy - 54), n(hy - 44)), stroke=DK, stroke_width=3, fill='none'))
    else:
        hs.append(path('M-36 %s C -40 %s -18 %s 6 %s C 30 %s 40 %s 36 %s Q 10 %s -36 %s Z' % (n(hy - 4), n(hy - 44), n(hy - 46), n(hy - 46), n(hy - 46), n(hy - 30), n(hy - 10), n(hy - 30), n(hy - 4)), fill=DK, stroke=I, stroke_width=2.5))
    # face (3/4 to the right)
    face = 'M-30 %s C -32 %s -18 %s 4 %s C 26 %s 38 %s 37 %s C 38 %s 34 %s 22 %s C 10 %s -10 %s -22 %s C -32 %s -32 %s -30 %s Z' % (
        n(hy - 2), n(hy - 30), n(hy - 38), n(hy - 38), n(hy - 38), n(hy - 22), n(hy - 2), n(hy + 18), n(hy + 32), n(hy + 36), n(hy + 40), n(hy + 38), n(hy + 30), n(hy + 20), n(hy + 10), n(hy - 2))
    hs.append(path(face, fill=PP, stroke=DK, stroke_width=4, stroke_linejoin='round'))
    # ear
    hs.append(path('M-12 %s c -12 -4 -14 18 -2 18' % n(hy - 4), fill=PP, stroke=DK, stroke_width=3.5))
    if o.get('beard'):
        hs.append(path('M-18 %s C -10 %s 20 %s 34 %s C 30 %s 6 %s -18 %s Z' % (n(hy + 18), n(hy + 46), n(hy + 46), n(hy + 16), n(hy + 34), n(hy + 52), n(hy + 18)), fill=DK, stroke=I, stroke_width=2))
        hs.append(path('M10 %s Q 22 %s 34 %s' % (n(hy + 12), n(hy + 6), n(hy + 12)), stroke=DK, stroke_width=5, fill='none', stroke_linecap='round'))
    # fringe
    if hair == 'bob':
        hs.append(path('M-30 %s C -24 %s 0 %s 14 %s C 22 %s 32 %s 38 %s C 34 %s 14 %s -4 %s C -18 %s -28 %s -30 %s Z' % (
            n(hy - 10), n(hy - 30), n(hy - 40), n(hy - 40), n(hy - 40), n(hy - 30), n(hy - 18), n(hy - 30), n(hy - 30), n(hy - 22), n(hy - 18), n(hy - 12), n(hy - 10)), fill=DK, stroke=I, stroke_width=2.5))
        hs.append(path('M-8 %s q 10 -8 22 -10 M 6 %s q 10 -4 20 0' % (n(hy - 30), n(hy - 34)), stroke=I, stroke_width=1.6, fill='none', opacity='.8'))
    if stylus:
        hs.append(path('M-34 %s L -2 %s' % (n(hy - 30), n(hy + 8)), stroke=DK, stroke_width=7, stroke_linecap='round'))
        hs.append(path('M-34 %s L -2 %s' % (n(hy - 30), n(hy + 8)), stroke=PP, stroke_width=3, stroke_linecap='round'))
        hs.append(circle(-34, hy - 30, 4, fill=A, stroke=DK, stroke_width=1.5))
    # features
    ex = 14 + look
    f = []
    if expr in ('calm', 'smile', 'focus', 'talk', 'sad', 'sleepy', 'up'):
        ey = hy - 4 if expr != 'up' else hy - 10
        if expr == 'focus':
            f.append(path('M%s %s q 6 4 12 0' % (n(ex - 6), n(ey + 3)), stroke=DK, stroke_width=3.5, fill='none', stroke_linecap='round'))
        elif expr == 'sleepy':
            f.append(path('M%s %s q 6 -3 12 0' % (n(ex - 6), n(ey + 2)), stroke=DK, stroke_width=3.5, fill='none', stroke_linecap='round'))
        else:
            f.append(g(ell(ex, ey, 4.2, 5.6, fill=DK) + circle(ex + 1.5, ey - 2, 1.4, fill=PP), cls='blink'))
        f.append(path('M%s %s q 7 -5 14 -1' % (n(ex - 8), n(hy - 16)), stroke=DK, stroke_width=3, fill='none', stroke_linecap='round'))
    elif expr == 'wide':
        f.append(circle(ex, hy - 6, 7.5, fill=PP, stroke=DK, stroke_width=3) + circle(ex + 1, hy - 6, 3.2, fill=DK))
        f.append(path('M%s %s q 8 -9 17 -4' % (n(ex - 9), n(hy - 22)), stroke=DK, stroke_width=3, fill='none', stroke_linecap='round'))
    elif expr == 'joy':
        f.append(path('M%s %s q 6 -8 12 0' % (n(ex - 6), n(hy - 2)), stroke=DK, stroke_width=3.5, fill='none', stroke_linecap='round'))
        f.append(path('M%s %s q 7 -6 14 -2' % (n(ex - 8), n(hy - 18)), stroke=DK, stroke_width=3, fill='none', stroke_linecap='round'))
    # nose
    f.append(path('M%s %s q 6 6 1 9' % (n(31), n(hy + 2)), stroke=DK, stroke_width=3, fill='none', stroke_linecap='round'))
    # mouth
    my = hy + 22
    if expr in ('smile', 'calm', 'up'):
        f.append(path('M12 %s q 9 %s 18 -2' % (n(my), '6' if expr == 'smile' else '3'), stroke=DK, stroke_width=3.2, fill='none', stroke_linecap='round'))
    elif expr == 'joy':
        f.append(path('M10 %s q 11 14 22 -2 z' % n(my - 2), fill=DK, stroke=DK, stroke_width=2.5, stroke_linejoin='round'))
    elif expr in ('wide', 'talk'):
        f.append(ell(21, my + 1, 5, 6.5 if expr == 'wide' else 4.5, fill=DK))
    elif expr == 'sad':
        f.append(path('M12 %s q 9 -5 18 1' % n(my + 3), stroke=DK, stroke_width=3.2, fill='none', stroke_linecap='round'))
    else:
        f.append(path('M13 %s l 15 0' % n(my), stroke=DK, stroke_width=3, stroke_linecap='round'))
    if o.get('old'):
        f.append(path('M2 %s q 6 4 12 0 M4 %s q 5 3 10 0' % (n(hy + 4), n(hy + 12)), stroke=DK, stroke_width=1.6, fill='none', opacity='.8'))
    hs.append(g(f))
    return ''.join(hs)


def person(who='woman', pose='stand', expr='calm', s=1.0, flip=False, hold='', anim=None, look=0):
    return keeper(pose, expr, s, flip, hold, who=who, anim=anim, look=look, stylus=False)


def myna(pose='stand', s=1.0, flip=False, say=None, anim=None, extra=''):
    """The myna: a bronze sprite where the pose exists, else the vector bird."""
    if Sc.plain:
        return _myna(pose, s, flip, say, anim, extra)
    if SPRITE:
        r = SPRITE('M', pose, anim, s, flip, (say or '') + extra)
        if r:
            return r
    return g(_myna(pose, s, flip, say, anim, extra), data_chr='1')


def _myna(pose='stand', s=1.0, flip=False, say=None, anim=None, extra=''):
    """Common myna: brown body (colour), dark head and tail, bare light eye patch, light beak and legs, white wing flash.
    Facing right, feet at (0,0), about 120 long and 118 tall at s=1."""
    if not anim and not Sc.plain:
        k = 'M|%s|%s|%s' % (pose, say, extra)
        u = sym(k, lambda: myna(pose, 1.0, False, say, anim, extra))
        return g(u, transform='scale(%s %s)' % (n(-s if flip else s), n(s))) if (s != 1 or flip) else u
    hd = {'stand': (0, 0), 'peck': (38, 10), 'up': (-24, -4), 'tuck': (60, 30), 'sing': (-14, 0), 'sip': (52, 22)}.get(pose, (0, 0))
    wing_up = pose in ('startle', 'fly')
    parts = []
    # tail
    parts.append(path('M-38 -52 L -78 -34 L -74 -24 L -34 -40 Z', fill=DK, stroke=I, stroke_width=2.5, stroke_linejoin='round'))
    parts.append(path('M-76 -33 L -72 -26', stroke=PP, stroke_width=4, stroke_linecap='round'))
    # legs
    if pose != 'fly':
        for dx in (-6, 8):
            parts.append(path('M%s -34 L %s -2 M %s -2 l 12 0 M %s -2 l -7 2' % (n(dx), n(dx + 2), n(dx - 2), n(dx + 2)), stroke=DK, stroke_width=7, stroke_linecap='round', fill='none'))
            parts.append(path('M%s -34 L %s -2 M %s -2 l 12 0 M %s -2 l -7 2' % (n(dx), n(dx + 2), n(dx - 2), n(dx + 2)), stroke=PP, stroke_width=3.4, stroke_linecap='round', fill='none'))
    # body
    parts.append(path('M-44 -56 C -40 -84 -6 -92 22 -84 C 44 -78 52 -60 44 -44 C 34 -26 -2 -22 -26 -32 C -40 -38 -46 -46 -44 -56 Z', fill=GC(), stroke=DK, stroke_width=4, stroke_linejoin='round'))
    parts.append(path('M-20 -36 C -2 -30 22 -32 38 -44', stroke=PP, stroke_width=3, fill='none', opacity='.55', stroke_linecap='round'))
    # wing
    wing = path('M-34 -66 C -14 -86 18 -80 26 -62 C 14 -50 -14 -46 -40 -52 Z', fill=DK, stroke=I, stroke_width=2.5, stroke_linejoin='round') + path('M-6 -58 l 14 -4', stroke=PP, stroke_width=6, stroke_linecap='round')
    if wing_up:
        parts.append(g(wing, transform='rotate(-70 20 -66)'))
    else:
        parts.append(g(wing, cls='wingk'))
    # head
    head = ''.join([
        path('M8 -86 C 6 -114 30 -126 50 -116 C 64 -108 66 -92 58 -82 C 46 -74 22 -72 8 -86 Z', fill=DK, stroke=I, stroke_width=2.5, stroke_linejoin='round'),
        path('M30 -112 C 22 -118 14 -110 16 -104', stroke=I, stroke_width=2, fill='none'),
        path('M40 -108 C 56 -112 60 -96 50 -92 C 40 -90 34 -100 40 -108 Z', fill=PP, stroke=DK, stroke_width=2),
        circle(47, -101, 4, fill=DK), circle(48.5, -102.5, 1.3, fill=PP),
    ])
    if say is not None or pose == 'sing':
        beak = path('M58 -100 L 84 -100 L 60 -94 Z M58 -92 L 80 -84 L 58 -88 Z', fill=PP, stroke=DK, stroke_width=2.5, stroke_linejoin='round')
    else:
        beak = path('M58 -100 C 70 -100 80 -98 86 -94 C 78 -90 68 -90 58 -90 Z', fill=PP, stroke=DK, stroke_width=2.5, stroke_linejoin='round')
    hg = head + beak
    if pose == 'tuck':
        parts.append(path('M-2 -82 C 10 -96 40 -94 44 -76 C 34 -64 8 -66 -2 -82 Z', fill=DK, stroke=I, stroke_width=2.5))
        parts.append(path('M6 -80 q 14 -8 30 -2', stroke=PP, stroke_width=2, fill='none'))
    else:
        parts.append(g(g(hg, transform='rotate(%s 14 -84) translate(0 %s)' % (n(hd[0]), n(hd[1] * .4))), cls='nod'))
    if say:
        parts.append(say)
    parts.append(extra)
    inner = g(parts, cls='bob')
    if anim:
        inner = g(inner, k=anim, c=(0, -40))
    return g(inner, transform='scale(%s %s)' % (n(-s if flip else s), n(s)))


def bubble(x, y, w, h, txt, size=26, tail='bl', fam='disp', inv=False, weight=700):
    """Speech bubble: paper fill, dark lettering. Tail at bottom-left by default."""
    tx = {'bl': (x + 26, y + h, x + 10, y + h + 30, x + 52, y + h), 'br': (x + w - 52, y + h, x + w - 10, y + h + 30, x + w - 26, y + h),
          'l': (x, y + h * .5 - 10, x - 28, y + h * .5 + 10, x, y + h * .5 + 18)}[tail]
    d = 'M%s %s L %s %s L %s %s' % tuple(n(v) for v in tx)
    fillc, txc, bg = (DK, PP, 'dk') if inv else (PP, DK, 'pp')
    out = rect(x, y, w, h, 22, fill=fillc, stroke=DK, stroke_width=4)
    out += path(d, fill=fillc, stroke=DK, stroke_width=4, stroke_linejoin='round')
    out += path('M%s %s L %s %s' % (n(tx[0] + 3), n(tx[1] - 1), n(tx[4] - 3), n(tx[5] - 1)), stroke=fillc, stroke_width=6)
    lines = txt.split('\n')
    for i, ln in enumerate(lines):
        out += text(x + w / 2, y + h / 2 + size * .36 + (i - (len(lines) - 1) / 2) * size * 1.15, ln, size, fill=txc, anchor='middle', fam=fam, weight=weight, bg=bg)
    return out


# ---------------------------------------------------------------- shared props

def palm_leaf(x, y, w, h, holes=True, lines=6, k=None, fill=None, ink=None, txt=True, seed=0):
    """A palm-leaf folio: long strip with rounded ends, fibre lines, string holes and incised letters."""
    fill = fill or GC()
    ink = ink or DK
    pts = rrect_pts(x, y, w, h, h * .48)
    out = [body(outline(pts, 64), fill=fill, cls='paper')]
    out.append(path('M%s %s L %s %s' % (n(x + h * .5), n(y + h * .28), n(x + w - h * .5), n(y + h * .28)), stroke=PP, stroke_width=1.6, opacity='.5', fill='none'))
    out.append(path('M%s %s L %s %s' % (n(x + h * .5), n(y + h * .78), n(x + w - h * .5), n(y + h * .78)), stroke=ink, stroke_width=1.4, opacity='.35', fill='none'))
    if txt:
        import random
        rnd = random.Random(seed + int(x) + int(y))
        for row in range(lines):
            yy = y + h * (.22 + .58 * (row + .5) / lines)
            xx = x + h * .9
            while xx < x + w - h * .9:
                L = rnd.uniform(8, 26)
                if holes and (abs(xx - (x + w * .28)) < 24 or abs(xx - (x + w * .72)) < 24):
                    xx += 10
                    continue
                out.append(path('M%s %s q %s %s %s 0' % (n(xx), n(yy), n(L / 2), n(rnd.uniform(-3, 3)), n(L)), stroke=ink, stroke_width=2.2, fill='none', stroke_linecap='round'))
                xx += L + rnd.uniform(4, 9)
    if holes:
        for hx in (x + w * .28, x + w * .72):
            out.append(circle(hx, y + h * .5, h * .11, fill=W, stroke=ink, stroke_width=2))
    return g(out, k=k)


def flame(x, y, s=1.0, cls='flick', lit=True):
    """Lamp flame: ink teardrop with the accent at its heart (the accent sits on art only)."""
    out = path('M0 0 C -14 -10 -16 -34 0 -64 C 16 -34 14 -10 0 0 Z', fill=I, stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke')
    out += path('M0 -4 C -7 -10 -8 -24 0 -40 C 8 -24 7 -10 0 -4 Z', fill=A)
    return at(x, y, g(out, cls=cls), s=s)


def stylus(x, y, ang=0, s=1.0):
    return at(x, y, path('M0 0 L 0 -120', stroke=DK, stroke_width=8, stroke_linecap='round') + path('M0 0 L 0 -120', stroke=PP, stroke_width=4, stroke_linecap='round') + path('M-3 -2 L 0 14 L 3 -2 Z', fill=DK), s=s, r=ang)


def label(x, y, s, size=22, anchor='middle', fam='mono', fill=None, bg=None, **kw):
    fill = fill or DK
    return text(x, y, s, size, fill=fill, anchor=anchor, fam=fam, bg=bg or ('pp' if fill == DK else 'dk'), **kw)


def tag_label(x, y, s, size=20, fam='mono', pad=10, inv=False, w=None):
    """A small paper tag with lettering: paper fill, dark text."""
    w = w or (len(s) * size * .62 + pad * 2)
    h = size * 1.6
    fc, tc, bg = (DK, PP, 'dk') if inv else (PP, DK, 'pp')
    return rect(x - w / 2, y - h / 2, w, h, 6, fill=fc, stroke=DK, stroke_width=3) + text(x, y + size * .36, s, size, fill=tc, anchor='middle', fam=fam, bg=bg)


def ground_line():
    return ''


def rrd(x, y, w, h, r):
    """Rounded rect as eight cubic segments with a fixed skeleton (morphs into any other rrd)."""
    r = min(r, w / 2, h / 2)
    k = .5523 * r
    X, Y, R, B = x, y, x + w, y + h
    q = lambda v: str(int(round(v)))
    segs = [
        (X + r, Y), (R - r, Y), None,
    ]
    d = 'M%s %s' % (q(X + r), q(Y))
    d += 'C%s %s %s %s %s %s' % (q(X + r + (w - 2 * r) / 3), q(Y), q(R - r - (w - 2 * r) / 3), q(Y), q(R - r), q(Y))
    d += 'C%s %s %s %s %s %s' % (q(R - r + k), q(Y), q(R), q(Y + r - k), q(R), q(Y + r))
    d += 'C%s %s %s %s %s %s' % (q(R), q(Y + r + (h - 2 * r) / 3), q(R), q(B - r - (h - 2 * r) / 3), q(R), q(B - r))
    d += 'C%s %s %s %s %s %s' % (q(R), q(B - r + k), q(R - r + k), q(B), q(R - r), q(B))
    d += 'C%s %s %s %s %s %s' % (q(R - r - (w - 2 * r) / 3), q(B), q(X + r + (w - 2 * r) / 3), q(B), q(X + r), q(B))
    d += 'C%s %s %s %s %s %s' % (q(X + r - k), q(B), q(X), q(B - r + k), q(X), q(B - r))
    d += 'C%s %s %s %s %s %s' % (q(X), q(B - r - (h - 2 * r) / 3), q(X), q(Y + r + (h - 2 * r) / 3), q(X), q(Y + r))
    d += 'C%s %s %s %s %s %s' % (q(X), q(Y + r - k), q(X + r - k), q(Y), q(X + r), q(Y))
    return d + 'Z'


def mpathd(ds, times, **kw):
    """Morph between d strings that already share a skeleton; consecutive repeats become holds."""
    P, TT = [], []
    for d, t in zip(ds, times):
        if P and d == P[-1]:
            TT[-1] = (TT[-1][0], t)
            continue
        P.append(d)
        TT.append((t, t))
    mt = ','.join(n2(a) if a == b else '%s-%s' % (n2(a), n2(b)) for a, b in TT)
    return path(P[0], data_m='|'.join(P), data_mt=mt, **kw)


def scribble(x, y, w, h, rows, seed=0, avoid=(), col=None, sw=2.4, lmin=9, lmax=24):
    """Incised letter marks as one path."""
    import random
    rnd = random.Random(seed)
    d = []
    for row in range(rows):
        yy = y + h * (row + .5) / rows
        xx = x
        while xx < x + w:
            if any(abs(xx - a) < 18 for a in avoid):
                xx += 16
                continue
            L = rnd.uniform(lmin, lmax)
            d.append('M%s %sq%s %s %s 0' % (n(xx), n(yy), n(L / 2), n(rnd.uniform(-4, 4)), n(L)))
            xx += L + rnd.uniform(4, 10)
    return path(''.join(d), stroke=col or DK, stroke_width=sw, fill='none', stroke_linecap='round')
