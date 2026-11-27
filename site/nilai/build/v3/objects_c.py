"""Scenes 09-16: the flats and the rain, the names, the wasteland, the gecko, the pulse, the puppet, the bedside, the ladder."""
import math
import random
from art import *  # noqa: F401,F403
import art as AR
from objects import walk_anim, hand_grip
from objects_b import fade, hold, banana_pts

t = AR.T


# ------------------------------------------------------------ the five landscape flats (தினை), drawn as painted stage flats
def _land(kind, w, h):
    """Painted landscape inside a flat of size w x h (origin top-left). Colour fill for the land, ink for the lines."""
    o = []
    if kind == 'hill':        # குறிஞ்சி: hill at midnight, two people meeting
        o.append(path('M0 %s L %s %s L %s %s L %s %s L %s %s L %s %s Z' % (n(h * .78), n(w * .3), n(h * .3), n(w * .5), n(h * .55), n(w * .75), n(h * .22), n(w), n(h * .7), n(w), n(h)) + ' L0 %s Z' % n(h), fill=GC(), stroke=W, stroke_width=1.5))
        o.append(path('M%s %s a 22 22 0 1 0 22 30 a 16 16 0 1 1 -22 -30' % (n(w * .2), n(h * .12)), fill=I))
        o.append(_fig(w * .42, h * .92, .16) + _fig(w * .58, h * .92, .16, flip=True))
    elif kind == 'forest':    # முல்லை: forest edge at evening, a woman at a door
        o.append(path('M0 %s L %s %s L %s %s Z' % (n(h * .8), n(w), n(h * .8), n(w), n(h)) + 'M0 %s L0 %s Z' % (n(h), n(h)), fill=GC(), stroke=W, stroke_width=1.5))
        for i, x in enumerate((.15, .35, .8)):
            o.append(path('M%s %s l -%s %s l %s 0 z' % (n(w * x), n(h * .25 + i * 10), n(w * .1), n(h * .5), n(w * .2)), fill=GC(), stroke=W, stroke_width=1.5))
            o.append(path('M%s %s l 0 %s' % (n(w * x), n(h * .74 + i * 10), n(h * .08)), stroke=I, stroke_width=4))
        o.append(rect(w * .5, h * .5, w * .22, h * .3, 0, fill='none', stroke=I, stroke_width=4) + _fig(w * .61, h * .8, .14))
        o.append(circle(w * .82, h * .14, w * .07, fill=I))
    elif kind == 'paddy':     # மருதம்: paddy at dawn, a quarrel
        o.append(path('M0 %s L %s %s L %s %s L 0 %s Z' % (n(h * .6), n(w), n(h * .6), n(w), n(h), n(h)), fill=GC(), stroke=W, stroke_width=1.5))
        o.append(path(''.join('M%s %s l -6 -26 M %s %s l 6 -24' % (n(x), n(h * (.68 + .12 * r)), n(x + 8), n(h * (.68 + .12 * r))) for r in range(3) for x in range(10, int(w), 26)), stroke=I, stroke_width=2.5))
        o.append(path('M%s %s a %s %s 0 0 1 %s 0 Z' % (n(w * .38), n(h * .6), n(w * .14), n(w * .14), n(w * .28)), fill=I))
        o.append(_fig(w * .3, h * .58, .14) + _fig(w * .74, h * .58, .14, flip=True))
    elif kind == 'shore':     # நெய்தல்: shore at sunset, someone watching the sea
        o.append(path('M0 %s L %s %s L %s %s L 0 %s Z' % (n(h * .55), n(w), n(h * .55), n(w), n(h), n(h)), fill=I))
        o.append(path(''.join('M%s %s q %s -10 %s 0 t %s 0' % (n(4), n(h * (.62 + .08 * r)), n(w * .12), n(w * .24), n(w * .24)) for r in range(4)), stroke=W, stroke_width=3, fill='none'))
        o.append(path('M%s %s a %s %s 0 0 1 %s 0 Z' % (n(w * .55), n(h * .55), n(w * .16), n(w * .16), n(w * .32)), fill=GC(), stroke=W, stroke_width=1.5))
        o.append(path('M0 %s L %s %s L %s %s L0 %s Z' % (n(h * .86), n(w * .5), n(h * .8), n(w), n(h * .9), n(h)), fill=GC(), stroke=W, stroke_width=1.5))
        o.append(_fig(w * .22, h * .84, .15))
    elif kind == 'desert':    # பாலை: cracked ground at noon, a figure walking away
        o.append(path('M0 %s L %s %s L %s %s L0 %s Z' % (n(h * .55), n(w), n(h * .55), n(w), n(h), n(h)), fill=GC(), stroke=W, stroke_width=1.5))
        rnd = random.Random(int(w))
        o.append(path(''.join('M%s %s l %s %s l %s %s' % (n(rnd.uniform(0, w)), n(rnd.uniform(h * .6, h)), n(rnd.uniform(-20, 20)), n(rnd.uniform(10, 24)), n(rnd.uniform(-20, 20)), n(rnd.uniform(10, 24))) for _ in range(int(w / 14))), stroke=W, stroke_width=3))
        o.append(circle(w * .5, h * .14, w * .09, fill=I) + path(''.join('M%s %s l %s %s' % (n(w * .5 + math.cos(a) * w * .13), n(h * .14 + math.sin(a) * w * .13), n(math.cos(a) * 14), n(math.sin(a) * 14)) for a in [i * .785 for i in range(8)]), stroke=I, stroke_width=4))
        o.append(_fig(w * .64, h * .56, .12))
    elif kind == 'mars':      # the sixth flat: rust ground, a small pale sun, two small moons, a figure walking away
        o.append(path('M0 %s Q %s %s %s %s L %s %s L0 %s Z' % (n(h * .6), n(w * .5), n(h * .5), n(w), n(h * .62), n(w), n(h), n(h)), fill=GC(), stroke=W, stroke_width=1.5))
        o.append(path(''.join('M%s %s l %s 4' % (n(x), n(h * (.7 + (x % 3) * .08)), n(30)) for x in range(10, int(w), 40)), stroke=W, stroke_width=3))
        o.append(circle(w * .7, h * .2, w * .05, fill=I) + circle(w * .25, h * .16, w * .03, fill=I) + circle(w * .4, h * .28, w * .02, fill=I))
        o.append(_fig(w * .5, h * .62, .12))
    return ''.join(o)


def _fig(x, y, s, flip=False):
    """A tiny painted figure, ink only."""
    f = -1 if flip else 1
    return path('M%s %s m -10 0 l 6 -40 l -6 -30 l 10 -8 l 10 8 l -6 30 l 6 40 z M%s %s m 0 -92 a 11 11 0 1 0 .1 0' % (n(x), n(y), n(x), n(y)), fill=I, transform='scale(1)' if True else None).replace('m -10 0', 'm %s 0' % n(-10 * f)) if False else \
        g(path('M-12 0 L -6 -44 L -14 -80 L 0 -92 L 14 -80 L 6 -44 L 12 0 Z', fill=I) + circle(0, -104, 13, fill=I), transform='translate(%s %s) scale(%s)' % (n(x), n(y), n(s * 2.4 * f)))


def flat(kind, x, y, w, h):
    """A stage flat: painted canvas in an ink frame on two splayed feet."""
    canvas = g(_land(kind, w, h), clip_path=None)
    return at(x, y, ''.join([
        rect(0, 0, w, h, 4, fill=W, stroke=I, stroke_width=6),
        canvas,
        rect(0, 0, w, h, 4, fill='none', stroke=I, stroke_width=6),
        path('M%s %s L %s %s M %s %s L %s %s' % (n(w * .2), n(h), n(w * .12), n(h + 60), n(w * .8), n(h), n(w * .88), n(h + 60)), stroke=I, stroke_width=7, stroke_linecap='round'),
    ]))


def flats_row(kinds, widths, x0=40, y=250, h=420, gap=14):
    out = []
    x = x0
    for kd, w in zip(kinds, widths):
        out.append((kd, x, w))
        x += w + gap
    return out


def rain(t0, t1, dense=48, k_extra=None):
    """A curtain of rain crossing the full width, left to right."""
    rnd = random.Random(9)
    d = ''.join('M%s %s l -26 70' % (n(rnd.uniform(0, 700)), n(rnd.uniform(-40, 900))) for _ in range(dense))
    curtain = path(d, stroke=I, stroke_width=4, stroke_linecap='round', opacity='.85')
    return g(curtain, k=kf((0, dict(o=0, x=-900)), (t0, dict(o=0, x=-900)), (t0 + .01, dict(o=1, x=-900)), (t1, 'l', dict(o=1, x=1200)), (t1 + .01, dict(o=0, x=1200))))


def umbrella(s=1.0):
    """A palm-leaf umbrella, myna-sized."""
    return at(0, 0, path('M-60 0 Q 0 -60 60 0 Q 40 -8 20 0 Q 0 -8 -20 0 Q -40 -8 -60 0 Z', fill=GC(), stroke=W, stroke_width=1.5) + path('M0 -30 L 0 50 q 0 10 -10 8', stroke=I, stroke_width=4, fill='none') + path('M-40 -16 L 0 -30 L 40 -16 M -20 -2 L 0 -30 L 20 -2', stroke=I, stroke_width=2, fill='none'), s=s)


# ============================================================ 09 · rain first
def s09(s):
    kinds = ['hill', 'forest', 'paddy', 'shore', 'desert']
    fl = []
    for i, kd in enumerate(kinds):
        x = 30 + i * 190
        f = flat(kd, x, 250, 176, 420)
        # lie down into the map, stand back up in the rain
        fl.append(g(f, k=kf((0, dict(o=0, y=60, sy=1)), (.05 + i * .012, dict(o=0, y=60)), (.1 + i * .012, 'b', dict(o=1, y=0)),
                            (t['m1a'] + i * .008, dict(sy=1)), (t['m1a'] + .08 + i * .008, 'i', dict(sy=.04, o=1)), (t['m1b'], dict(sy=.04, o=0)),
                            (t['m2a'] + .06, dict(sy=.04, o=0)), (t['m2a'] + .08, dict(sy=.04, o=1)), (t['m2b'] + i * .01, 'b', dict(sy=1, o=1))), c=(x + 88, 670)))
    # the satellite map: land, sea, a cloud band thin and broken under a brown haze
    land = path('M120 260 C 300 230 420 300 520 280 C 640 250 760 300 880 270 L 880 640 C 700 610 560 660 420 630 C 300 610 200 650 120 640 Z', fill=GC(), stroke=W, stroke_width=1.5)
    coast = path('M640 270 C 600 380 690 480 640 640', stroke=I, stroke_width=6, fill='none')
    sea = path('M640 270 C 600 380 690 480 640 640 L 880 640 L 880 270 Z', fill=I)
    cl_broken = ''.join(ell(x, 450 + (x % 3) * 8, 34 + (x % 5) * 4, 14, fill=I) for x in range(160, 880, 110))
    cl_full = path('M120 450 C 300 380 600 520 880 430 L 880 500 C 600 590 300 450 120 520 Z', fill=I)
    haze = path(''.join('M%d %d l 8 -8' % (x, y) for x in range(130, 870, 22) for y in range(280, 640, 26)), stroke=DK, stroke_width=4, opacity='.9')
    mp = g([rect(110, 250, 780, 400, 6, fill=W, stroke=I, stroke_width=6), land, sea, coast,
            g(cl_broken, k=kf((0, dict(o=1)), (t['m2a'] + .04, dict(o=1)), (t['m2a'] + .1, dict(o=0)))),
            g(cl_full, k=kf((0, dict(o=0, x=-300)), (t['m2a'] + .02, dict(o=0, x=-300)), (t['m2a'] + .1, 'o', dict(o=1, x=0)))),
            g(haze, k=kf((0, dict(o=0, x=0)), (t['m1b'] - .02, dict(o=0, x=0)), (t['m1b'] + .01, dict(o=1, x=0)), (t['m2a'], dict(o=1, x=0)), (t['m2a'] + .08, 'n', dict(o=0, x=900)))),
            text(130, 236, 'monsoon band · satellite', 22, fill=I, fam='mono', bg='wall')],
           k=kf((0, dict(o=0, sy=.3)), (t['m1a'] + .06, dict(o=0, sy=.3)), (t['m1b'], 'o', dict(o=1, sy=1)), (t['m2a'] + .06, dict(o=1, sy=1)), (t['m2a'] + .1, dict(o=0, sy=.3))), c=(500, 650))
    keep = g(keeper('walk1', 'calm', s=.82, anim=walk_anim(.08, .3, 8, 'stand', 'stand')), k=kf((0, dict(o=0, x=-80, y=760)), (.08, dict(o=1, x=-60)), (.3, 'l', dict(x=520)), (t['m1a'] + .03, dict(o=0)), (t['m2b'], dict(o=0, x=420)), (t['m2b'] + .03, dict(o=1)), (1, dict(x=420))))
    keepjoy = g(keeper('delight', 'joy', s=.82), k=kf((0, dict(o=0, x=420, y=760)), (.8, dict(o=0)), (.82, dict(o=1))))
    mk = g([myna('stand', 1.05), g(umbrella(1.0), k=kf((0, dict(o=0, sy=.1, y=-10)), (.76, dict(o=0, sy=.1, y=-10)), (.79, 'b', dict(o=1, sy=1, y=-150))), c=(30, -100))],
           k=kf((0, dict(o=0, x=800, y=760)), (.1, dict(o=0)), (.13, dict(o=1)), (1, dict(x=800))))
    out = [shadow(500, 772, 470, 16), g(fl), mp, rain(.12, .3), rain(t['m2b'], .9, 60), keep, keepjoy, mk]
    return dict(art=''.join(out), tr='leaf')


# ============================================================ 10 · the names
def heron(s=1.0):
    """A grey heron (குருகு): long neck in an S, dagger bill, thin long legs like millet stalks."""
    return at(0, 0, ''.join([
        path('M-6 -120 L -10 0 M 10 -120 L 18 0', stroke=I, stroke_width=4, stroke_linecap='round'),
        path('M-14 0 l -18 4 M 18 0 l 20 4', stroke=I, stroke_width=3),
        path('M-60 -150 C -40 -190 30 -190 46 -160 C 50 -140 30 -116 0 -114 C -30 -114 -56 -124 -60 -150 Z', fill=GC(), stroke=W, stroke_width=1.5),
        path('M-62 -150 L -96 -128 L -56 -138 Z', fill=GC(), stroke=W, stroke_width=1.5),
        path('M30 -170 C 60 -200 20 -230 44 -262 C 56 -276 76 -276 80 -262', stroke=GC(), stroke_width=14, fill='none', stroke_linecap='round'),
        path('M78 -266 L 132 -254 L 78 -256 Z', fill=I),
        circle(70, -266, 4, fill=I), path('M60 -276 l -24 -6', stroke=I, stroke_width=3),
        path('M-40 -160 C -10 -176 20 -170 36 -156', stroke=PP, stroke_width=3, fill='none'),
    ]), s=s)


def eel(s=1.0):
    return at(0, 0, path('M-90 0 C -60 -24 -30 24 0 0 C 30 -24 60 24 90 0 C 96 -4 104 -2 108 4 C 100 8 94 8 90 6 C 60 30 30 -18 0 6 C -30 30 -60 -18 -90 6 Z', fill=I) + circle(100, 2, 2.5, fill=W), s=s)


def lily(s=1.0):
    return at(0, 0, ell(0, 0, 50, 12, fill=GC(), stroke=W, stroke_width=1.5) + path('M-14 -6 L -20 -40 L -6 -16 L 0 -48 L 6 -16 L 20 -40 L 14 -6 Z', fill=I), s=s)


def screwpine(s=1.0):
    return at(0, 0, path('M0 0 L 0 -120', stroke=I, stroke_width=10) + ''.join(path('M0 -110 q %d -50 %d -90' % (dx, dx * 2), stroke=GC(), stroke_width=10, fill='none', stroke_linecap='round') for dx in (-30, -12, 12, 30)) + path('M-20 0 L -8 -30 M 20 0 L 8 -30', stroke=I, stroke_width=6), s=s)


def drum(s=1.0):
    return at(0, 0, ell(0, -50, 46, 14, fill=GC(), stroke=W, stroke_width=1.5) + path('M-46 -50 L -40 0 L 40 0 L 46 -50', fill=I) + path('M-40 -40 L 30 -4 M 40 -40 L -30 -4', stroke=W, stroke_width=3), s=s)


def net(s=1.0):
    return at(0, 0, path(''.join('M%d -80 L %d 0' % (x, x + 20) for x in range(-60, 61, 20)) + ''.join('M-60 %d L 80 %d' % (y, y) for y in range(-80, 1, 20)), stroke=I, stroke_width=2.5, fill='none') + circle(-60, 0, 6, fill=I) + circle(80, 0, 6, fill=I), s=s)


def s10(s):
    things = [('குருகு', 'heron', heron, 300, 600, .8), ('ஆரல்', 'eel', eel, 250, 690, .7), ('ஆம்பல்', 'water lily', lily, 420, 680, .9),
              ('தாழை', 'screwpine', screwpine, 520, 600, .8), ('பறை', 'drum', drum, 170, 560, .8), ('வலை', 'net', net, 440, 520, .7)]
    # the shore flat, big
    shore = ''.join([rect(80, 160, 520, 560, 6, fill=W, stroke=I, stroke_width=7),
                     path('M86 470 L 594 470 L 594 714 L 86 714 Z', fill=GC(), stroke=W, stroke_width=1.5),
                     path(''.join('M%d %d q 30 -10 60 0 t 60 0' % (100 + (r % 2) * 40, 500 + r * 50) for r in range(4)), stroke=W, stroke_width=3, fill='none'),
                     path('M86 300 L 594 300', stroke=I, stroke_width=2, opacity='.4'),
                     path('M120 720 L 100 780 M 560 720 L 580 780', stroke=I, stroke_width=8, stroke_linecap='round')])
    crea, labels = [], []
    for j, (ta, en, fn, x, y, sc) in enumerate(things):
        crea.append(g(at(x, y, fn(sc)), k=kf((0, dict(o=0, s=.4)), (.07 + j * .012, dict(o=0, s=.4)), (.11 + j * .012, 'b', dict(o=1, s=1)),
                                             (t['m1b'] - .02 + j * .012, dict(o=1)), (t['m1b'] + .01 + j * .012, dict(o=0))), c=(x, y)))
        labels.append(g(tag_label(x, y + 28, ta, 18, fam='ta'), k=kf((0, dict(o=0)), (.12 + j * .012, dict(o=0)), (.15 + j * .012, dict(o=1)), (t['m1b'] + j * .012, dict(o=1)), (t['m1b'] + .02 + j * .012, dict(o=0)))))
    # the legend: entries grey out one by one and merge into a single line, "other"
    leg = [rect(640, 170, 300, 400, 10, fill=W, stroke=I, stroke_width=5), text(660, 210, 'LEGEND', 22, fill=I, fam='mono', bg='wall', weight=600)]
    for j, (ta, en, *_r) in enumerate(things):
        y = 250 + j * 46
        leg.append(g([rect(660, y - 18, 22, 22, 4, fill=GC()), text(696, y, en, 24, fill=I, fam='mono', bg='wall')],
                     k=kf((0, dict(o=1, y=0)), (t['m1b'] - .02 + j * .012, dict(o=1, y=0)), (t['m1b'] + .02 + j * .012, dict(o=0, y=(5 - j) * 46 - 0)))))
    leg.append(g([rect(660, 482, 22, 22, 4, fill=I), text(696, 500, 'other', 24, fill=I, fam='mono', bg='wall', weight=600)], k=fade(t['m1b'] + .06)))
    legend = g(leg, k=kf((0, dict(o=0, x=40)), (t['m1a'], dict(o=0, x=40)), (t['m1a'] + .05, 'o', dict(o=1, x=0)), (t['m2a'], dict(o=1)), (t['m2a'] + .04, dict(o=0))))
    # FUTURE: a cabinet of small labelled drawers
    cab = [rect(630, 150, 320, 560, 10, fill=GI(), stroke=W, stroke_width=1.5), path('M640 710 l -10 50 M 940 710 l 10 50', stroke=I, stroke_width=9, stroke_linecap='round')]
    names = ['குருகு', 'ஆரல்', 'ஆம்பல்', 'தாழை', 'பறை', 'வலை', 'மைனா', 'தினை']
    for j, nm in enumerate(names):
        cx, cy = 650 + (j % 2) * 150, 170 + (j // 2) * 132
        opened = j in (0, 1, 6)
        dr = g([rect(cx, cy, 140, 116, 6, fill=GC(), stroke=W, stroke_width=1.5), rect(cx + 20, cy + 14, 100, 30, 4, fill=W), text(cx + 70, cy + 36, nm, 20, fill=I, anchor='middle', fam='ta', bg='wall'), circle(cx + 70, cy + 80, 9, fill=I)],
               k=kf((0, dict(x=0)), (.76 + (j == 1) * .05 + (j == 6) * .1, dict(x=0)), (.79 + (j == 1) * .05 + (j == 6) * .1, 'o', dict(x=-60 if opened and j % 2 == 0 else 60 if opened else 0)), (.95 if j == 6 else 1, dict(x=60 if j == 6 else (-60 if opened and j % 2 == 0 else 60 if opened else 0))), (1, dict(x=0 if j == 6 else (-60 if opened and j % 2 == 0 else 60 if opened else 0)))) if opened else None)
        cab.append(dr)
    cabinet = g(cab, k=kf((0, dict(o=0, s=.8)), (t['m2a'], dict(o=0, s=.8)), (t['m2b'] - .04, 'b', dict(o=1, s=1))), c=(790, 430))
    # the heron steps out of its drawer and walks back across the frame onto the flat
    walker = g(heron(.9), k=kf((0, dict(o=0, x=760, y=300, s=.2)), (.79, dict(o=0, x=740, y=300, s=.2)), (.81, dict(o=1)), (.84, 'o', dict(x=640, y=640, s=1)), (.95, 'l', dict(x=300, y=640)), (1, dict(x=280))), c=(0, 0))
    water = g(path('M836 314 q 30 -12 60 0 t 60 0', stroke=I, stroke_width=4, fill='none') + eel(.4).replace('<g', '<g', 1), k=fade(.85), transform='translate(0 0)')
    mk = g(myna('peck', .9), k=kf((0, dict(o=0, x=880, y=702)), (.85, dict(o=0)), (.88, dict(o=1)), (1, dict(o=1))))
    flatg = g(shore, k=kf((0, dict(o=0, y=40)), (.04, dict(o=0, y=40)), (.08, 'b', dict(o=1, y=0))))
    keep = g(keeper('point', 'smile', s=.85), k=kf((0, dict(o=0, x=540, y=760)), (t['m2b'], dict(o=0, x=540)), (t['m2b'] + .03, 'b', dict(o=1))))
    out = [shadow(500, 772, 460, 16), flatg, g(crea), g(labels), legend, cabinet, water, walker, keep, mk]
    return dict(art=''.join(out), tr='mat')


# ============================================================ 11 · the wasteland is made
def stilt_house(x, y, h, s=1.0):
    """A small house on stilts, roof thatched."""
    return at(x, y, ''.join([
        path('M-40 0 L -40 %d M 40 0 L 40 %d M 0 0 L 0 %d' % (-h, -h, -h), stroke=I, stroke_width=6),
        rect(-56, -h - 70, 112, 70, 4, fill=GC(), stroke=W, stroke_width=1.5),
        path('M-70 %d L 0 %d L 70 %d Z' % (-h - 66, -h - 120, -h - 66), fill=I),
        rect(-14, -h - 50, 28, 50, 2, fill=W, stroke=I, stroke_width=3),
    ]), s=s)


def tortoise_pot():
    """Naladiyar 331: a tortoise at play in the water of a pot while the fire is lit under it."""
    return ''.join([
        path('M-80 -10 C -90 -90 90 -90 80 -10 C 70 30 -70 30 -80 -10 Z', fill=GC(), stroke=W, stroke_width=1.5),
        ell(0, -64, 84, 16, fill=I),
        path('M-30 -78 C -20 -100 20 -100 30 -78 Z', fill=PP, stroke=I, stroke_width=3),
        path('M-30 -80 l -18 -14 M 30 -80 l 22 -18', stroke=PP, stroke_width=8, stroke_linecap='round'),
        circle(40, -98, 9, fill=PP, stroke=I, stroke_width=3),
        g(path('M-40 30 Q -30 0 -20 30 Q -10 -6 0 30 Q 10 0 20 30 Q 30 -4 40 30 Z', fill=A), cls='flick'),
        path('M-50 36 L 50 36', stroke=I, stroke_width=8, stroke_linecap='round'),
    ])


def s11(s):
    kinds = ['hill', 'forest', 'paddy', 'shore', 'desert']
    widths = [130, 130, 130, 150, 330]
    fl = []
    x = 20
    for i, (kd, w) in enumerate(zip(kinds, widths)):
        f = flat(kd, x, 280, w, 380)
        fl.append(g(f, k=pop(.06 + i * .012, .07, 50)))
        x += w + 12
    # the desert flat narrows as trees and a hand-dug channel are drawn in; forest and hill take their ground back
    desert_fix = g([path('M650 520 C 700 560 760 600 900 640', stroke=I, stroke_width=8, fill='none', data_dr='%s,%s' % (n2(t['m2a']), n2(t['m2a'] + .06))),
                    g(''.join(path('M%d 600 l -22 -70 l 44 0 z' % x, fill=GC(), stroke=W, stroke_width=1.5) + path('M%d 600 l 0 20' % x, stroke=I, stroke_width=5) for x in (700, 780, 860)), k=kf((0, dict(o=0, s=.2)), (t['m2a'] + .04, dict(o=0, s=.2)), (t['m2a'] + .09, 'b', dict(o=1, s=1))), c=(780, 600))])
    # NOW: on the shore flat a small town is rebuilt three times, each a little taller on its stilts
    town = []
    for j, h in enumerate((20, 60, 110)):
        k = kf((0, dict(o=0, sy=.1)), (t['m1a'] + j * .045, dict(o=0, sy=.1)), (t['m1a'] + .03 + j * .045, 'b', dict(o=1, sy=1)), (t['m1a'] + .045 * (j + 1) - .002 if j < 2 else 1, dict(o=1)), (t['m1a'] + .045 * (j + 1) + .01 if j < 2 else 1, dict(o=0 if j < 2 else 1)))
        town.append(g(stilt_house(520, 640, h, .7) + stilt_house(590, 640, h, .55), k=k, c=(550, 640)))
    pot = g(at(600, 400, tortoise_pot(), s=1.1), k=kf((0, dict(o=0, s=.3)), (t['m1b'] + .02, dict(o=0, s=.3)), (t['m1b'] + .05, 'b', dict(o=1, s=1)), (t['m2a'] + .03, dict(o=1)), (t['m2a'] + .06, dict(o=0))), c=(580, 400))
    note = g([tag('text', 'கொலைஞர் உலையேற்றித் தீமடுப்ப ஆமை', x=990, y=150, font_size=24, fill=I, data_bg='wall', style='font-family:var(--f-ta)', lang='ta', text_anchor='end'),
              text(990, 180, 'naladiyar:331 · line 1', 17, fill=I, fam='mono', bg='wall', anchor='end'),
              text(990, 222, 'Real tortoises climb out. So, eventually, did we.', 25, fill=I, fam='hand', bg='wall', weight=600, anchor='end')],
             k=hold(t['m1b'] + .04, t['m2a'] + .04))
    # FUTURE: the sixth flat, carried across the whole frame and set down at the end of the row
    mars = flat('mars', -110, -380, 220, 380)
    carry = g([mars, g(keeper('carry', 'smile', s=.78), transform='translate(-120 0)'), g(person('man', 'carry', 'calm', s=.78, flip=True), transform='translate(120 0)')],
              k=kf((0, dict(o=0, x=-300, y=760)), (t['m2a'] + .04, dict(o=0, x=-300)), (t['m2a'] + .05, dict(o=1, x=-300)), (.81, 'i', dict(x=790, y=760)), (.85, dict(x=790, y=770))))
    row = g(fl + [desert_fix], k=kf((0, dict(x=0, s=1)), (t['m2a'] + .06, dict(s=1, x=0)), (.8, 'i', dict(s=.86, x=-10))), c=(0, 660))
    out = [shadow(500, 772, 480, 16), row, g(town), pot, note, carry]
    return dict(art=''.join(out), tr='zoom', fx=880, fy=500)


# ============================================================ 12 · the gecko's feet
def gecko(s=1.0):
    """A house gecko, seen from below on a ceiling: splayed toes with the pads, banded tail."""
    toes = ''
    for (fx, fy, ang) in ((-70, -40, -150), (-70, 40, 150), (70, -44, -30), (70, 44, 30)):
        toes += path('M0 0 L %s %s' % (n(fx), n(fy)), stroke=GI(), stroke_width=16, stroke_linecap='round')
        for k in range(5):
            a = math.radians(ang + (k - 2) * 26)
            toes += path('M%s %s l %s %s' % (n(fx), n(fy), n(math.cos(a) * 22), n(math.sin(a) * 22)), stroke=I, stroke_width=7, stroke_linecap='round') + circle(fx + math.cos(a) * 24, fy + math.sin(a) * 24, 6, fill=GC(), stroke=W, stroke_width=1.5)
    return at(0, 0, ''.join([
        toes,
        path('M-110 0 C -110 -36 110 -40 120 0 C 110 40 -110 36 -110 0 Z', fill=GI(), stroke=W, stroke_width=1.5),
        path('M-110 0 C -160 -6 -220 20 -280 10', stroke=GI(), stroke_width=22, fill='none', stroke_linecap='round'),
        path('M-150 -2 l 0 12 M -190 4 l 0 12 M -230 8 l 0 12', stroke=GC(), stroke_width=6),
        path('M120 0 C 130 -34 190 -30 196 0 C 190 30 130 34 120 0 Z', fill=GI(), stroke=W, stroke_width=1.5),
        circle(170, -18, 7, fill=GC()), circle(170, 18, 7, fill=GC()),
        path('M-80 -6 C -30 -16 40 -16 90 -6', stroke=GC(), stroke_width=4, fill='none', stroke_dasharray='6 10'),
    ]), s=s)


def kingfisher(s=1.0):
    """White-throated kingfisher diving: long dagger bill."""
    return at(0, 0, ''.join([
        path('M-60 0 C -50 -30 20 -36 40 -14 C 52 -2 40 14 20 16 C -10 20 -50 18 -60 0 Z', fill=GC(), stroke=W, stroke_width=1.5),
        path('M-60 0 L -100 -14 L -96 10 Z', fill=I),
        path('M30 -16 C 46 -34 74 -26 76 -6 C 76 8 60 14 44 12 Z', fill=I),
        path('M70 -12 L 150 4 L 70 4 Z', fill=I),
        circle(62, -10, 4, fill=W), path('M36 2 C 46 14 60 14 70 6', fill=PP, stroke=I, stroke_width=2),
        path('M-30 -14 C -10 -30 20 -30 30 -18', stroke=PP, stroke_width=3, fill='none'),
    ]), s=s)


def s12(s):
    # THEN: the gecko on a whitewashed ceiling, a woman below who has stopped to listen
    ceiling = rect(60, 60, 1100, 60, 0, fill=I)
    gk = g(at(560, 170, gecko(1.05)), k=kf((0, dict(o=0, x=80)), (.05, dict(o=0, x=80)), (.11, 'o', dict(o=1, x=0)), (t['m1a'], dict(s=1)), (t['m1a'] + .1, 'n', dict(s=7, x=0, y=0)), (t['m1a'] + .11, dict(o=0, s=7))), c=(676, 214))
    woman = g(person('woman', 'listen', 'focus', s=.95), k=kf((0, dict(o=0, x=300, y=760)), (.06, dict(o=0)), (.1, 'b', dict(o=1)), (t['m1a'], dict(o=1)), (t['m1a'] + .04, dict(o=0))))
    chirp = g(bubble(620, 250, 150, 70, 'tchk tchk', 26), k=hold(.15, .19, .01))
    m_say = g(bubble(720, 470, 150, 70, 'tchk tchk', 26), k=hold(.19, .22, .01))
    w_say = g(bubble(120, 290, 300, 70, 'say something good', 24, tail='br'), k=hold(.22, .27, .01))
    m_good = g(bubble(720, 470, 110, 70, 'good.', 30), k=hold(.27, .31, .01))
    mk = g(myna('sing', 1.05), k=kf((0, dict(o=0, x=760, y=760)), (.12, dict(o=0)), (.15, dict(o=1)), (t['m1a'] + .01, dict(o=1)), (t['m1a'] + .04, dict(o=0))))
    # NOW: into one toe: the pad is rows of ridges, the ridges are hairs, the hairs split into flat tips
    pad = g([ell(500, 400, 300, 220, fill=GI(), stroke=W, stroke_width=1.5)] + [path('M%d %d q 250 -40 %d 0' % (240 + j * 4, 260 + j * 40, 520 - j * 8), stroke=GC(), stroke_width=14, fill='none', stroke_linecap='round') for j in range(8)]
            + [text(500, 660, 'toe pad · ridges', 26, fill=I, anchor='middle', fam='mono', bg='wall')],
            k=kf((0, dict(o=0, s=.3)), (t['m1a'] + .08, dict(o=0, s=.3)), (t['m1a'] + .12, 'o', dict(o=1, s=1)), (t['m1b'], dict(o=1, s=1)), (t['m1b'] + .04, dict(o=0, s=2.4))), c=(500, 400))
    hair = []
    for j in range(9):
        x = 140 + j * 90
        hair.append(path('M%d 640 C %d 520 %d 420 %d 330' % (x, x + 10, x - 10, x + 6), stroke=I, stroke_width=12, fill='none', stroke_linecap='round'))
        for k in range(4):
            hair.append(path('M%d 330 l %d -60' % (x + 6, (k - 1.5) * 14), stroke=I, stroke_width=4, stroke_linecap='round') + rect(x + 6 + (k - 1.5) * 14 - 9, 262, 18, 7, 2, fill=GC()))
    hairs = g(hair + [text(500, 700, 'hairs · split tips', 26, fill=I, anchor='middle', fam='mono', bg='wall')], k=kf((0, dict(o=0, s=.4)), (t['m1b'], dict(o=0, s=.4)), (t['m1b'] + .03, 'o', dict(o=1, s=1)), (t['m2a'] - .01, dict(o=1)), (t['m2a'] + .03, dict(o=0))), c=(500, 450))
    tape = g([rect(250, 240, 500, 420, 12, fill=W, stroke=I, stroke_width=4), rect(380, 300, 240, 340, 30, fill=GI(), stroke=W, stroke_width=1.5), rect(396, 320, 208, 290, 16, fill=DK),
              rect(330, 270, 340, 54, 6, fill=GC(), stroke=W, stroke_width=1.5), path(''.join('M%d 276 l 6 42' % x for x in range(340, 666, 14)), stroke=I, stroke_width=2),
              text(500, 700, 'dry tape · holds a phone to a wall', 24, fill=I, anchor='middle', fam='mono', bg='wall')],
             k=kf((0, dict(o=0)), (t['m1b'] + .05, dict(o=0)), (t['m1b'] + .08, dict(o=1)), (t['m2a'], dict(o=1)), (t['m2a'] + .03, dict(o=0))))
    # FUTURE: a climbing machine walks up the drawer tower on feet like those; the lotus leaf beads the rain
    tower = ''.join(rect(640, 120 + j * 110, 200, 100, 6, fill=GC(), stroke=W, stroke_width=1.5) + rect(700, 150 + j * 110, 80, 22, 4, fill=W) for j in range(6))
    bot = g([rect(-40, -60, 80, 90, 14, fill=GI(), stroke=W, stroke_width=1.5), circle(-14, -24, 8, fill=W), circle(14, -24, 8, fill=W)] +
            [path('M%d %d l %d %d' % (sx * 40, sy * 20, sx * 24, sy * 30), stroke=I, stroke_width=8, stroke_linecap='round') + circle(sx * 66, sy * 54, 10, fill=GC(), stroke=W, stroke_width=1.5) for sx in (-1, 1) for sy in (-1, 1)],
            k=kf((0, dict(o=0, x=640, y=700)), (t['m2a'] + .04, dict(o=0, x=640, y=700)), (t['m2a'] + .07, dict(o=1)), (t['m2b'], dict(x=640, y=700)), (.95, 'l', dict(x=640, y=210))))
    lotus = ''.join([path('M60 740 C 60 650 340 650 340 740 Z', fill=GC(), stroke=W, stroke_width=1.5), path('M200 740 L 200 700 M 200 700 L 120 690 M 200 700 L 280 690', stroke=PP, stroke_width=3)]
                    + [circle(x, 700 - (x % 30) / 3, 9, fill=I) for x in (130, 170, 230, 270)])
    bead = g(circle(0, 0, 11, fill=I) + circle(-4, -4, 3, fill=W), k=kf((0, dict(x=300, y=690)), (.8, dict(x=300, y=690)), (.86, 'n', dict(x=345, y=760))))
    fut = g([tower, lotus], k=kf((0, dict(o=0)), (t['m2a'], dict(o=0)), (t['m2a'] + .05, dict(o=1))))
    # the kingfisher dives without a splash; its bill stretches into the nose of a train leaving a tunnel
    KF = [(0, 0), (40, -16), (70, -14), (150, 4), (70, 6), (40, 14), (0, 16), (-40, 10), (-60, 0), (-40, -10)]
    TR = [(-40, -40), (120, -40), (240, -20), (330, 10), (240, 26), (120, 40), (-40, 40), (-160, 40), (-220, 40), (-160, -40)]
    kfp = mpath([KF, KF, TR], [0, .86, .93], k=40, fill=GC(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke')
    kfg = g([g(kingfisher(.9), k=kf((0, dict(o=1)), (.855, dict(o=1)), (.86, dict(o=0)))), kfp,
             g(rect(-220, -20, 160, 14, 3, fill=W) + path('M-40 0 L 300 0', stroke=I, stroke_width=0), k=fade(.92))],
            k=kf((0, dict(o=0, x=200, y=300, r=60)), (.76, dict(o=0, x=200, y=300, r=60)), (.77, dict(o=1)), (.82, 'n', dict(x=420, y=650, r=60)), (.86, 'o', dict(x=420, y=640, r=0)), (1, dict(x=980, y=640))), c=(0, 0))
    tunnel = g(path('M380 760 L 380 600 Q 480 540 580 600 L 580 760', fill=I) + path('M400 760 L 400 610 Q 480 566 560 610 L 560 760', fill=W), k=hold(.84, .95))
    out = [g(ceiling, k=kf((0, dict(o=1)), (t['m1a'] + .04, dict(o=1)), (t['m1a'] + .06, dict(o=0)))), woman, gk, chirp, m_say, w_say, m_good, mk, pad, hairs, tape, fut, bot, bead, tunnel, kfg]
    return dict(art=''.join(out), tr='zoom', fx=420, fy=640)


# ============================================================ 13 · the order of care
def finger_pts(x, y0, y1, w=34):
    return rrect_pts(x - w / 2, y0, w, y1 - y0, w / 2)


def s13(s):
    # the wrist, palm up, across the frame
    arm = ''.join([
        path('M-60 520 L 640 500 C 700 498 740 470 800 470 C 880 470 940 500 960 540 C 940 590 880 610 800 600 C 740 596 700 580 640 580 L -60 600 Z', fill=GI(), stroke=W, stroke_width=1.5),
        path('M820 480 C 870 440 940 440 980 460 M 830 590 C 880 620 940 630 990 620', stroke=I, stroke_width=26, fill='none', stroke_linecap='round'),
        path('M640 520 C 690 516 720 520 760 530', stroke=W, stroke_width=3, fill='none'),
        path('M560 548 l 30 0 M 580 532 l 20 0', stroke=W, stroke_width=3),
    ])
    arm_g = g(arm, k=kf((0, dict(o=0, x=-200)), (.04, dict(o=0, x=-200)), (.1, 'o', dict(o=1, x=0))))
    # the three fingers: they lift and become the stethoscope's tubes, then thin to a band round the same wrist
    fingers = []
    for j, x in enumerate((480, 540, 600)):
        F0 = finger_pts(x, 300, 512, 40)
        F1 = finger_pts(400 + j * 100 if j != 1 else 500, 140, 470, 16 if j != 1 else 120)
        F2 = rrect_pts(570 + j * 4, 494 - j * 2, 26, 96, 13)
        fingers.append(mpath([F0, F0, F1, F1, F2], [0, t['m1a'], t['m1b'], t['m2a'], t['m2b']], k=36, fill=GC(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke'))
    knuckles = g(path('M450 300 C 470 250 640 250 640 300 L 640 200 L 450 200 Z', fill=GC(), stroke=W, stroke_width=1.5) + path('M440 0 L 450 210 L 640 210 L 660 0 Z', fill=GC(), stroke=W, stroke_width=1.5) + path('M460 200 L 640 200', stroke=PP, stroke_width=4, stroke_dasharray='2 8'),
                 k=kf((0, dict(o=1, y=0)), (t['m1a'], dict(o=1, y=0)), (t['m1a'] + .06, dict(o=0, y=-200))))
    chest = g([circle(500, 520, 64, fill=GIH(), stroke=W, stroke_width=1.5), circle(500, 520, 44, fill=DK), circle(500, 520, 24, fill=GI()), path('M400 140 C 380 90 440 70 450 100 M 600 140 C 620 90 560 70 550 100', stroke=I, stroke_width=10, fill='none', stroke_linecap='round')],
              k=kf((0, dict(o=0)), (t['m1b'] - .02, dict(o=0)), (t['m1b'], dict(o=1)), (t['m2a'], dict(o=1)), (t['m2a'] + .04, dict(o=0))))
    band = g([rect(574, 492, 22, 100, 10, fill=I), circle(585, 542, 6, fill=A, class_='tick')], k=fade(t['m2b']))
    trace = g([rect(600, 140, 330, 150, 10, fill=W, stroke=I, stroke_width=4), path('M616 230 l 40 0 l 10 -30 l 10 50 l 10 -20 l 60 0 l 10 -30 l 10 50 l 10 -20 l 120 0', stroke=I, stroke_width=4, fill='none', data_dr='%s,%s' % (n2(t['m2b']), n2(.8))),
               text(616, 270, 'early, years before it hurts', 20, fill=I, fam='mono', bg='wall')], k=fade(t['m2b'] - .02))
    # the keeper is the patient: she watches the physician's face
    bust = g(keeper('sit', 'up', s=1.12), k=kf((0, dict(o=0, x=-20, y=770)), (.03, dict(o=0)), (.08, 'b', dict(o=1))))
    # gag: the stethoscope on the myna; the trace leaves the top of the chart and comes in at the bottom
    gag = g([rect(620, 120, 320, 200, 10, fill=W, stroke=I, stroke_width=4),
             path('M640 240 l 30 0 l 8 -140 M 678 320 l 10 -120 l 12 60 l 30 0 l 8 -140 M 738 320 l 10 -110 l 12 50 l 30 0 l 8 -140 M 798 320 l 10 -120 l 12 60 l 40 0', stroke=I, stroke_width=4, fill='none', data_dr='.8,.9'),
             text(780, 112, 'myna · 600 bpm', 20, fill=I, anchor='middle', fam='mono', bg='wall')],
            k=kf((0, dict(o=0)), (.79, dict(o=0)), (.8, dict(o=1))))
    trace_off = g(trace, k=kf((0, dict(o=1)), (.785, dict(o=1)), (.79, dict(o=0))))
    mk = g(myna('stand', 1.1), k=kf((0, dict(o=0, x=860, y=760)), (.74, dict(o=0)), (.77, 'b', dict(o=1))))
    out = [bust, arm_g, knuckles, g(fingers), chest, band, trace_off, gag, mk]
    return dict(art=''.join(out), tr='fade')


# ============================================================ 14 · the body as a machine
PUPPET = [  # part, x, y (joint centre), shape, explode offset
    ('head', 500, 230, 'circle', (0, -110)),
    ('torso', 500, 360, 'torso', (0, 0)),
    ('uarmL', 440, 330, 'limbv', (-130, -40)), ('farmL', 430, 420, 'limbv', (-200, 40)),
    ('uarmR', 560, 330, 'limbv', (130, -40)), ('farmR', 570, 420, 'limbv', (200, 40)),
    ('thighL', 470, 480, 'limbv', (-110, 80)), ('shinL', 466, 580, 'limbv', (-150, 170)),
    ('thighR', 530, 480, 'limbv', (110, 80)), ('shinR', 534, 580, 'limbv', (150, 170)),
]


def puppet_part(kind, x, y):
    if kind == 'circle':
        return circle(x, y, 46, fill=GI(), stroke=W, stroke_width=1.5) + path('M%d %d q 10 -6 20 0 M %d %d q 14 10 28 0' % (x + 6, y - 6, x + 4, y + 14), stroke=W, stroke_width=4, fill='none') + path('M%d %d C %d %d %d %d %d %d' % (x - 46, y - 10, x - 40, y - 70, x + 40, y - 70, x + 46, y - 10), fill=GC(), stroke=W, stroke_width=1.5)
    if kind == 'torso':
        return path('M%d %d L %d %d L %d %d L %d %d Z' % (x - 56, y - 80, x + 56, y - 80, x + 44, y + 90, x - 44, y + 90), fill=GC(), stroke=W, stroke_width=1.5) + path('M%d %d L %d %d' % (x - 44, y + 20, x + 44, y + 20), stroke=I, stroke_width=6) + circle(x, y - 30, 8, fill=A)
    return rect(x - 15, y - 50, 30, 100, 14, fill=GI(), stroke=W, stroke_width=1.5) + circle(x, y - 50, 8, fill=GC())


def slider(x, y, w, label, pos0, pos1, t0, t1, stuck=False):
    knob = g(rect(-16, -26, 32, 52, 8, fill=GC(), stroke=W, stroke_width=1.5), k=kf((0, dict(x=x + w * pos0)), (t0, dict(x=x + w * pos0)), (t1, 'o', dict(x=x + w * pos1)) if not stuck else (t1, dict(x=x + w * pos0)), *([(t0 + .02, dict(x=x + w * pos0 - 8)), (t0 + .03, dict(x=x + w * pos0 + 3)), (t0 + .04, dict(x=x + w * pos0 - 6)), (t0 + .05, dict(x=x + w * pos0))] if stuck else [])), transform='translate(0 %d)' % y)
    return ''.join([rect(x, y - 6, w, 12, 6, fill=I), text(x, y - 32, label, 26, fill=I, fam='mono', bg='wall', weight=600), text(x + w, y - 32, '0', 22, fill=I, anchor='end', fam='mono', bg='wall'), knob])


def s14(s):
    parts = []
    for name, x, y, kind, (dx, dy) in PUPPET:
        k = kf((0, dict(x=0, y=0, r=0)), (t['m1a'], dict(x=0, y=0)), (t['m1a'] + .1, 'b', dict(x=dx - 120, y=dy, r=dx * .06)), (t['m2a'], dict(x=dx - 120, y=dy, r=dx * .06)), (t['m2b'] - .02, 'o', dict(x=0, y=0, r=0)))
        parts.append(g(puppet_part(kind, x, y), k=k, c=(x, y)))
    strings = path(''.join('M%d 90 L %d %d' % (x, x, y) for x, y in ((420, 420), (500, 180), (580, 420), (470, 580), (530, 580))), stroke=I, stroke_width=2.5)
    bar = path('M400 90 L 600 90 M 500 40 L 500 120', stroke=I, stroke_width=12, stroke_linecap='round')
    rig = g([strings, bar, path('M500 40 L 500 -60', stroke=I, stroke_width=6)], k=kf((0, dict(o=1, y=0)), (t['m1a'], dict(o=1)), (t['m1a'] + .04, dict(o=0)), (t['m2a'], dict(o=0)), (t['m2a'] + .02, dict(o=1, y=0)), (t['m2b'] - .04, 'n', dict(o=0, y=-200))))
    leaders = g(''.join(path('M%d %d L %d %d' % (x + dx - 120, y + dy, x + dx - 120 + (60 if dx >= 0 else -60), y + dy - 40), stroke=I, stroke_width=2) + circle(x + dx - 120 + (60 if dx >= 0 else -60), y + dy - 40, 15, fill=W, stroke=I, stroke_width=2.5) + text(x + dx - 120 + (60 if dx >= 0 else -60), y + dy - 33, str(j + 1), 18, fill=I, anchor='middle', fam='mono', bg='wall') for j, (_, x, y, _k, (dx, dy)) in enumerate(PUPPET)), k=hold(t['m1a'] + .1, t['m2a']))
    puppet = g(parts, k=kf((0, dict(o=0, y=-100)), (.05, dict(o=0, y=-100)), (.11, 'b', dict(o=1, y=0)), (t['m2b'] - .02, dict(o=1)), (t['m2b'], dict(o=0))))
    sl = g([slider(700, 230, 230, 'tired', .8, 0, t['m1b'] - .04, t['m1b']), slider(700, 340, 230, 'sore', .7, 0, t['m1b'] - .02, t['m1b'] + .02),
            slider(700, 450, 230, 'bored', .9, 0, t['m1b'], t['m1b'] + .04), slider(700, 560, 230, 'ageing', .6, .6, t['m1b'] + .03, t['m1b'] + .06, stuck=True)],
           k=kf((0, dict(o=0, x=80)), (t['m1a'] + .04, dict(o=0, x=80)), (t['m1a'] + .1, 'o', dict(o=1, x=0)), (t['m2a'] + .04, dict(o=1)), (t['m2a'] + .08, dict(o=0))))
    keep = g(keeper('lean', 'focus', s=.8), k=kf((0, dict(o=0, x=760, y=760)), (t['m1b'], dict(o=0)), (t['m1b'] + .03, dict(o=1)), (t['m2a'] + .04, dict(o=1)), (t['m2a'] + .08, dict(o=0))))
    sitter = g(person('man', 'sit', 'wide', s=1.0), k=kf((0, dict(o=0, x=430, y=760)), (t['m2b'] - .02, dict(o=0)), (t['m2b'], dict(o=1)), (1, dict(o=1))))
    stool = g(rect(340, 676, 180, 20, 4, fill=GI()) + path('M360 696 L 350 760 M 500 696 L 510 760', stroke=I, stroke_width=10), k=fade(t['m2b'] - .02))
    yawn = g(text(470, 330, 'haaa…', 34, fill=I, fam='hand', bg='wall', weight=600), k=hold(.8, .92))
    mk = g(myna('stand', .95), k=kf((0, dict(o=0, x=880, y=760)), (t['m1b'] + .05, dict(o=0)), (t['m1b'] + .08, dict(o=1)), (t['m2a'] + .04, dict(o=1)), (t['m2a'] + .045, dict(o=0))))
    mk2 = g(myna('tuck', .95), k=kf((0, dict(o=0, x=880, y=760)), (t['m2a'] + .04, dict(o=0)), (t['m2a'] + .045, dict(o=1)), (1, dict(o=1))))
    zz = g(text(900, 600, 'z z', 30, fill=I, fam='hand', bg='wall'), k=fade(t['m2a'] + .06))
    msl = g([rect(820, 640, 120, 10, 5, fill=I), g(rect(-12, -18, 24, 36, 6, fill=GC(), stroke=W, stroke_width=1.5), k=kf((0, dict(x=830, y=645)), (t['m1b'] + .1, dict(x=830)), (t['m2a'] + .03, 'o', dict(x=930))))], k=kf((0, dict(o=0)), (t['m1b'] + .06, dict(o=0)), (t['m1b'] + .08, dict(o=1))))
    out = [shadow(500, 772, 300, 18), rig, puppet, leaders, sl, stool, sitter, yawn, keep, msl, mk, mk2, zz]
    return dict(art=''.join(out), tr='leaf')


# ============================================================ 15 · the fourth part
def kalvam():
    return ''.join([path('M-90 -10 C -80 -50 80 -50 90 -10 C 70 20 -70 20 -90 -10 Z', fill=GC(), stroke=W, stroke_width=1.5), ell(0, -30, 70, 12, fill=W), path('M10 -40 L 60 -90', stroke=I, stroke_width=14, stroke_linecap='round')])


def s15(s):
    # THEN: a sick-bed on the floor, a low stool with someone fanning; at the back, the kalvam in a glass case
    mat = rect(250, 700, 480, 40, 10, fill=GC(), stroke=W, stroke_width=1.5) + rect(640, 680, 90, 30, 12, fill=GI(), stroke=W, stroke_width=1.5)
    case = g([rect(60, 160, 230, 200, 6, fill='none', stroke=I, stroke_width=5), at(175, 320, kalvam(), s=.9), path('M70 360 L 280 360 L 280 400 L 70 400 Z', fill=GI()),
              text(175, 390, 'history, not a remedy', 18, fill=DK, anchor='middle', fam='mono', bg='ink')], k=kf((0, dict(o=0)), (.06, dict(o=0)), (.1, dict(o=1))))
    patient = g(g(person('woman', 'lie', 'sleepy', s=.85), transform='rotate(-90) translate(-40 0)'), k=kf((0, dict(x=640, y=690)), (t['m1a'], dict(x=640, y=690)), (t['m1b'], 'i', dict(x=640, y=560))))
    fanner = g(person('old', 'sit', 'calm', s=.85, hold=path('M0 0 L 30 -50 Q 60 -60 50 -20 Z', fill=GC(), stroke=W, stroke_width=1.5)), k=kf((0, dict(o=0, x=170, y=760)), (.06, dict(o=0)), (.1, 'b', dict(o=1)), (t['m1a'], dict(o=1)), (t['m1a'] + .04, dict(o=0))))
    stool0 = rect(110, 676, 130, 20, 4, fill=GI(), stroke=W, stroke_width=1.5) + path('M124 696 L 120 760 M 226 696 L 230 760', stroke=I, stroke_width=10)
    # NOW: the hospital bed; the stool is a visitor's chair and it is empty; a monitor does the watching
    bed = g([rect(250, 560, 520, 40, 8, fill=GC(), stroke=W, stroke_width=1.5), path('M270 600 L 270 760 M 750 600 L 750 760 M 250 470 L 250 600', stroke=I, stroke_width=10), rect(660, 540, 110, 28, 12, fill=GI())],
            k=kf((0, dict(o=0)), (t['m1a'] + .04, dict(o=0)), (t['m1b'], dict(o=1))))
    mat_g = g(mat, k=kf((0, dict(o=1)), (t['m1a'] + .04, dict(o=1)), (t['m1b'], dict(o=0))))
    chair = ''.join([rect(-60, -110, 120, 18, 4, fill=GC(), stroke=W, stroke_width=1.5), rect(-60, -260, 18, 160, 4, fill=GC(), stroke=W, stroke_width=1.5), path('M-50 -92 L -56 0 M 50 -92 L 56 0', stroke=I, stroke_width=10)])
    chair_g = g(chair, k=kf((0, dict(o=0, x=100, y=760)), (t['m1a'] + .04, dict(o=0, x=100)), (t['m1b'], dict(o=1, x=100)), (t['m2a'] + .03, dict(x=100)), (t['m2b'] + .02, 'i', dict(x=300))))
    stool_g = g(stool0, k=kf((0, dict(o=1)), (t['m1a'] + .02, dict(o=1)), (t['m1a'] + .06, dict(o=0))))
    mon = g([path('M860 760 L 860 300', stroke=I, stroke_width=8), rect(780, 160, 170, 140, 12, fill=GI(), stroke=W, stroke_width=1.5), rect(792, 172, 146, 104, 6, fill=DK),
             path('M800 230 l 30 0 l 8 -30 l 8 50 l 8 -20 l 70 0', stroke=PP, stroke_width=4, fill='none')],
            k=kf((0, dict(o=0, s=1)), (t['m1a'] + .04, dict(o=0)), (t['m1b'], dict(o=1, s=1)), (t['m2a'], dict(o=1, s=1, x=0, y=0)), (t['m2b'] - .02, 'i', dict(o=0, s=.12, x=-210, y=330))), c=(865, 230))
    # FUTURE: the band on the wrist; the keeper in the chair; fingers that stop above the wrist and wait
    band = g(rect(560, 520, 18, 40, 8, fill=I) + circle(569, 540, 5, fill=A), k=fade(t['m2b'] - .02))
    keep = g(keeper('sit', 'calm', s=.85), k=kf((0, dict(o=0, x=300, y=760)), (t['m2b'], dict(o=0)), (t['m2b'] + .03, dict(o=1))))
    hand = g(path('M0 0 l 0 40 M 14 0 l 0 44 M 28 0 l 0 40', stroke=PP, stroke_width=14, stroke_linecap='round') + path('M-6 -60 L 34 -60 L 34 0 L -6 0 Z', fill=PP), k=kf((0, dict(o=0, x=520, y=380)), (.76, dict(o=0, x=520, y=380)), (.78, dict(o=1)), (.82, 'o', dict(y=440)), (.9, dict(y=440)), (.94, 'i', dict(y=478))))
    wait = g(text(420, 420, 'waits', 24, fill=I, fam='hand', bg='wall'), k=hold(.83, .89))
    ask = g(bubble(600, 360, 300, 70, 'is now a good time?', 24, tail='bl'), k=hold(.84, .9, .01))
    no = g(bubble(820, 520, 100, 60, 'no.', 28, tail='bl'), k=hold(.9, .98, .01))
    mk = g(myna('stand', 1.0), k=kf((0, dict(o=0, x=880, y=760)), (.8, dict(o=0)), (.83, 'b', dict(o=1))))
    out = [shadow(500, 772, 360, 16), case, mat_g, stool_g, bed, patient, fanner, mon, chair_g, keep, band, hand, wait, ask, no, mk]
    return dict(art=''.join(out), tr='mat')


# ============================================================ 16 · the ladder, climbed down
def creature(k, x, y, s=1.0):
    """The grammar's creatures on the rungs: grass and tree, snail, ant, crab and bee, deer, person."""
    if k == 1:
        d = path('M-60 0 l 6 -24 m 6 24 l 4 -30 m 8 30 l -2 -22', stroke=I, stroke_width=4) + path('M40 0 L 40 -50', stroke=I, stroke_width=8) + circle(40, -80, 36, fill=GC(), stroke=W, stroke_width=1.5)
    elif k == 2:
        d = path('M-40 0 C -40 -10 30 -10 40 0 Z', fill=I) + circle(-4, -26, 24, fill=GC(), stroke=W, stroke_width=1.5) + path('M-4 -26 m -12 0 a 12 12 0 1 1 12 12', stroke=W, stroke_width=3, fill='none') + path('M34 -4 l 10 -24 M 40 -4 l 14 -20', stroke=I, stroke_width=3)
    elif k == 3:
        d = ''.join(circle(cx, -12, r, fill=I) for cx, r in ((-22, 10), (0, 8), (20, 11))) + path('M-6 -10 l -10 14 M 2 -10 l 0 16 M 8 -10 l 12 14 M 26 -20 l 10 -16', stroke=I, stroke_width=3)
    elif k == 4:
        d = ell(-26, -14, 30, 16, fill=GC(), stroke=W, stroke_width=1.5) + path('M-50 -20 l -14 -16 M -2 -20 l 14 -16 M -40 -2 l -12 10 M -12 -2 l 12 10', stroke=I, stroke_width=4) + ell(40, -50, 16, 11, fill=I) + path('M30 -60 q 10 -20 20 0', fill='none', stroke=GC(), stroke_width=6) + path('M32 -50 l 16 0', stroke=W, stroke_width=3)
    elif k == 5:
        d = path('M-40 -50 C -40 -70 30 -70 36 -50 L 34 0 M 26 -50 L 26 0 M -30 -50 L -32 0 M -40 -50 L -42 0', stroke=GC(), stroke_width=10, fill='none') + path('M-44 -66 C -30 -78 30 -76 36 -56 C 30 -44 -30 -44 -44 -54 Z', fill=GC(), stroke=W, stroke_width=1.5) + path('M30 -66 L 50 -96 L 66 -92 L 52 -70 Z', fill=GC(), stroke=W, stroke_width=1.5) + path('M54 -96 l -6 -20 m 6 20 l 10 -18', stroke=I, stroke_width=3)
    else:
        d = at(0, 0, person('man', 'stand', 'calm', s=.3))
    return at(x, y, d, s=s)


def s16(s):
    X0, X1 = 360, 640
    rungs_y = [700, 590, 480, 370, 260, 150]
    rails = path('M%d 60 L %d 760 M %d 60 L %d 760' % (X0, X0 - 20, X1, X1 + 20), stroke=GIH(), stroke_width=24, stroke_linecap='round') + path(''.join('M%d %d l 0 6 M %d %d l 0 6' % (X0 - 2, y, X1 + 2, y) for y in range(110, 760, 90)), stroke=W, stroke_width=4)
    rungs = []
    for j, y in enumerate(rungs_y):
        r = path('M%d %d L %d %d' % (X0 - 10, y, X1 + 10, y), stroke=I, stroke_width=16, stroke_linecap='round') + path('M%d %d L %d %d' % (X0, y - 4, X1, y - 4), stroke=PP, stroke_width=3, opacity='.5') + path('M%d %d l 22 18 m 0 -18 l -22 18 M %d %d l 22 18 m 0 -18 l -22 18' % (X0 - 12, y - 9, X1 - 10, y - 9), stroke=GC(), stroke_width=4)
        cr = creature(j + 1, 500, y - 10, 1.1)
        dim = j < 5
        relit = t['m2a'] + (5 - j) * .03
        k = kf((0, dict(o=0)), (.05 + j * .015, dict(o=0)), (.08 + j * .015, dict(o=1)), (t['m1a'] + .04, dict(o=1)), (t['m1b'], dict(o=.15 if dim else 1)), (relit, dict(o=.15 if dim else 1)), (relit + .02, dict(o=1)))
        rungs.append(g(r + g(cr, k=kf((0, dict(o=1)), (t['m1a'] + .04, dict(o=1)), (t['m1b'] - .02, dict(o=0 if j == 5 else 1)))), k=k))
    # the machine: a phone on rung six; it grows a clumsy arm and feels its way down
    ph = ''.join([rect(-46, -110, 92, 150, 16, fill=GI(), stroke=W, stroke_width=1.5), rect(-36, -98, 72, 118, 8, fill=DK), circle(-14, -50, 7, fill=PP), circle(14, -50, 7, fill=PP)])
    arm = g(path('M40 -20 C 90 0 100 50 70 90 l -10 10 m 10 -10 l 12 6', stroke=I, stroke_width=10, fill='none', stroke_linecap='round'), k=kf((0, dict(o=0, s=0)), (t['m2a'] - .02, dict(o=0, s=0)), (t['m2a'] + .02, 'b', dict(o=1, s=1))), c=(40, -20))
    path_k = [(0, dict(o=0, x=500, y=rungs_y[5] - 10)), (t['m1a'] + .04, dict(o=0, x=500, y=rungs_y[5] - 10)), (t['m1b'] - .02, 'b', dict(o=1))]
    for j in range(5):
        relit = t['m2a'] + (5 - j) * .03
        path_k.append((relit - .01, 'i', dict(y=rungs_y[j] - 10, x=500 + (12 if j % 2 else -12))))
    path_k.append((.9, dict(y=rungs_y[0] - 10)))
    machine = g([ph, arm], k=kf(*path_k))
    grass_touch = g(path('M500 700 l -30 40 m 30 -40 l 0 50 m 0 -50 l 30 40', stroke=A, stroke_width=0), k=fade(.9))
    keep = g(keeper('hold', 'focus', s=.95, flip=True), k=kf((0, dict(o=0, x=800, y=760)), (.06, dict(o=0)), (.1, 'b', dict(o=1))))
    # gag: on rung five the myna shuffles aside, as slowly as possible
    mk = g(myna('stand', .9), k=kf((0, dict(o=0, x=420, y=rungs_y[4] - 6)), (.07, dict(o=0)), (.1, dict(o=1)), (t['m2a'] + .04, dict(x=420)), (t['m2a'] + .09, 'l', dict(x=600)), (1, dict(x=600))))
    out = [shadow(500, 772, 220, 14), rails, g(rungs), mk, machine, keep]
    return dict(art=''.join(out), tr='leaf')
