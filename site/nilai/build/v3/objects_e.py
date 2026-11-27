"""Scenes 25-31: the far horizon, and the close."""
import math
import random
from art import *  # noqa: F401,F403
import art as AR
from objects import walk_anim, hand_grip
from objects_b import fade, hold, coin
from objects_c import creature, heron
from objects_d import _c

t = AR.T


# ============================================================ 25 · look up
def kolam_path(m=4, n_=3):
    """A sikku kolam on an m x n dot grid as a mirror curve: one closed line weaving round every dot (gcd(m, n) = 1)."""
    x, y, dx, dy = 1, 0, 1, 1
    pts = []
    start = (x, y, dx, dy)
    while True:
        pts.append((x, y))
        x += dx
        y += dy
        if x == 0 or x == 2 * m:
            dx = -dx
        if y == 0 or y == 2 * n_:
            dy = -dy
        if (x, y, dx, dy) == start:
            break
    return pts


def s25(s):
    U, CX, CY = 64, 500, 380
    K = kolam_path()
    def place(p, rot=0):
        x, y = (p[0] - 4) * U, (p[1] - 3) * U
        if rot:
            a = math.radians(rot)
            x, y = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
            x, y = x * .9, y * .9
        return (CX + x, CY + y)
    P0 = [place(p) for p in K]
    P1 = [place(p, 45) for p in K]
    # the same points: smooth kolam curve, then squared-off copper traces (45 degrees round, sharp corners)
    d0 = cubic(P0, True, 1.0, 0)
    d1 = cubic(P1, True, 0.0, 0)
    line_ = path(d0, data_m=d0 + '|' + d1, data_mt='%s-%s,%s' % (n2(0), n2(t['m1a']), n2(t['m1b'])), fill='none', stroke=I, stroke_width=7, stroke_linejoin='round', stroke_linecap='round')
    line_g = g(g(line_, k=kf((0, dict(o=0)), (.04, dict(o=0)), (.06, dict(o=1)))), k=kf((0, dict(o=1)), (t['m2a'], dict(o=1)), (t['m2b'], dict(o=.9))))
    draw = path(d0, fill='none', stroke=I, stroke_width=7, data_dr='.05,.22', stroke_linecap='round')
    dots = []
    for i, X in enumerate((1, 3, 5, 7)):
        for j, Y in enumerate((1, 3, 5)):
            a0, a1 = place((X, Y)), place((X, Y), 45)
            dot = circle(0, 0, 9, fill=I)
            pad = g(circle(0, 0, 18, fill='none', stroke=GC(), stroke_width=7), k=hold(t['m1b'] - .02, t['m2a'] + .04))
            star = g(path('M0 -26 L 6 -6 L 26 0 L 6 6 L 0 26 L -6 6 L -26 0 L -6 -6 Z', fill=GI()), k=fade(t['m2a'] + .04), cls='tw')
            dots.append(g([dot, pad, star], k=kf((0, dict(x=a0[0], y=a0[1], o=0)), (.03 + (i + j) * .006, dict(o=0)), (.05 + (i + j) * .006, 'b', dict(o=1)), (t['m1a'], dict(x=a0[0], y=a0[1])), (t['m1b'], dict(x=a1[0], y=a1[1])))))
    ground = g(ell(500, 380, 380, 270, fill=GC(), opacity='.0'), k=None)
    board = g(rect(150, 70, 700, 620, 18, fill=W, stroke=GC(), stroke_width=6), k=kf((0, dict(o=0, y=0)), (t['m1a'] + .04, dict(o=0)), (t['m1b'], dict(o=1)), (t['m2a'], dict(o=1, y=0)), (t['m2b'], 'n', dict(o=0, y=600))))
    # the wider sky: more stars arrive as the camera pulls back
    rnd = random.Random(25)
    sky = g(''.join(circle(rnd.uniform(-400, 1400), rnd.uniform(-300, 900), rnd.uniform(2, 5), fill=I, class_='tw') for _ in range(70)), k=fade(t['m2a'] + .06))
    # the pull-back, from one dot to the whole sky
    world = g([sky, board, line_g, draw, g(dots)], k=kf((0, dict(s=3.4)), (.04, dict(s=3.4)), (.28, 'i', dict(s=1)), (t['m2a'], dict(s=1)), (t['m2b'], 'i', dict(s=.62)), (1, dict(s=.56))), c=place((1, 1)))
    # the myna joins the stars with its beak, the way a kolam is drawn, going round one star without touching it
    route = path('M260 140 L 420 90 C 470 70 520 110 500 150 C 480 190 430 170 440 130 L 700 180 L 820 120', fill='none', stroke=I, stroke_width=4, stroke_dasharray='2 10', stroke_linecap='round', data_dr='.8,.95')
    mk = g(myna('peck', .8), k=kf((0, dict(o=0, x=260, y=150)), (.78, dict(o=0)), (.8, dict(o=1)), (.95, 'l', dict(x=820, y=130))))
    keep = g(g(keeper('lie', 'up', s=.7), transform='rotate(-90)'), k=kf((0, dict(o=0, x=860, y=740)), (.1, dict(o=0)), (.15, dict(o=1))))
    out = [world, route, mk, keep]
    return dict(art=''.join(out), tr='zoom', fx=500, fy=380, pu='0:.1:%d:%d' % place((1, 1)))


# ============================================================ 26 · the work of the wind
HULL0 = [(220, 600), (360, 640), (560, 646), (720, 612), (800, 540), (760, 560), (560, 584), (360, 584), (240, 560), (190, 520)]
HULL1 = [(40, 600), (300, 640), (700, 640), (930, 610), (980, 520), (930, 540), (700, 556), (300, 556), (80, 550), (20, 520)]


def s26(s):
    sea = g(path(''.join('M%d %d q 40 -14 80 0 t 80 0' % (x, 650 + (x // 160 % 2) * 30) for x in range(-200, 1200, 160)), stroke=I, stroke_width=5, fill='none'), k=kf((0, dict(x=0)), (1, 'l', dict(x=-320))))
    hull = mpath([_c(HULL0), _c(HULL0), _c(HULL1), _c(HULL1)], [0, t['m1a'], t['m1b'], 1], k=40, fill=GI(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke')
    stitches = g(path(''.join('M%d 590 l 0 10 M %d 612 l 0 10' % (x, x + 12) for x in range(260, 760, 30)), stroke=GC(), stroke_width=3) + path('M230 596 C 400 618 600 620 760 586', stroke=GC(), stroke_width=3, fill='none'), k=fade(0, t['m1a']))
    mast = g([path('M490 580 L 490 150', stroke=I, stroke_width=12), path('M350 190 L 630 190', stroke=I, stroke_width=8),
              path('M360 196 C 340 300 360 420 380 500 L 600 500 C 640 420 650 300 624 196 Z', fill=GC(), stroke=W, stroke_width=1.5), path('M380 260 L 610 260 M 375 340 L 620 340 M 380 420 L 612 420', stroke=W, stroke_width=3),
              path('M760 560 L 840 680', stroke=I, stroke_width=10)], k=kf((0, dict(o=0, y=40)), (.04, dict(o=0, y=40)), (.08, 'b', dict(o=1, y=0)), (t['m1a'], dict(o=1)), (t['m1a'] + .06, dict(o=0))))
    # sacks of pepper -> steel boxes -> panels of one sail of foil, far wider than the frame
    boxes = []
    for j in range(8):
        sx, sy = 300 + (j % 4) * 70, 560 - (j // 4) * 50
        S0 = ellipse_pts(sx, sy, 32, 26, 20)
        bx, by = 120 + (j % 4) * 190, 500 - (j // 4) * 90
        S1 = rrect_pts(bx, by, 180, 84, 4)
        fx, fy = -300 + (j % 4) * 400, 40 + (j // 4) * 300
        S2 = rrect_pts(fx, fy, 396, 296, 2)
        boxes.append(mpath([S0, S0, S1, S1, S2], [0, t['m1a'] + j * .005, t['m1b'], t['m2a'], t['m2b']], k=24, fill=GC() if j % 2 else GI(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke'))
    rig = g(path('M-300 40 L 500 -200 L 1300 40 M -300 640 L 500 900 M 1300 640 L 500 900', stroke=I, stroke_width=3), k=fade(t['m2b']))
    bridge = g(rect(820, 400, 90, 140, 6, fill=GI(), stroke=W, stroke_width=1.5) + rect(834, 416, 60, 20, 3, fill=W), k=hold(t['m1b'], t['m2a'] + .04))
    paper = g([rect(-40, -20, 80, 40, 3, fill=W, stroke=I, stroke_width=3), path('M-30 -8 l 50 0 M -30 2 l 40 0 M -30 12 l 56 0', stroke=I, stroke_width=2)],
              k=kf((0, dict(x=560, y=520, r=-8, o=1)), (t['m1a'], dict(x=560, y=520)), (t['m1b'], dict(x=860, y=380, r=0)), (t['m2a'], dict(x=860, y=380)), (t['m2b'], dict(x=900, y=80, r=6)), (1, dict(x=900, y=80))))
    hull_g = g(hull, k=kf((0, dict(o=1)), (t['m2a'], dict(o=1)), (t['m2a'] + .06, dict(o=0, y=200))))
    keep = g(keeper('reach', 'focus', s=.55), k=kf((0, dict(x=230, y=590, o=1)), (t['m1a'], dict(x=230, y=590)), (t['m1b'], dict(x=80, y=556)), (t['m2a'], dict(x=80, y=556)), (t['m2b'], dict(x=40, y=700)), (1, dict(x=40, y=700))))
    mk = g(myna('up', .7), k=kf((0, dict(x=490, y=150)), (t['m1a'], dict(x=490, y=150)), (t['m1b'], dict(x=430, y=326)), (t['m2a'], dict(x=430, y=326)), (t['m2b'], dict(x=-260, y=40)), (1, dict(x=-260, y=40))))
    sun = g(text(500, 960, 'pushed by sunlight', 22, fill=I, anchor='middle', fam='mono', bg='floor'), k=fade(t['m2b']))
    out = [sea, rig, hull_g, stitches, mast, bridge, g(boxes), paper, keep, mk, sun]
    return dict(art=''.join(out), tr='mat')


# ============================================================ 27 · the atom only divine eyes see
def s27(s):
    # THEN: a sesame seed halved with the blade end of the stylus, then the half halved; a tally climbs
    seed = path('M0 -120 C 60 -100 80 40 0 120 C -80 40 -60 -100 0 -120 Z', fill=GC(), stroke=W, stroke_width=1.5)
    halves = []
    for j in range(4):
        sc = .5 ** j
        halves.append(g(at(500, 400, seed + path('M0 -110 L 0 110', stroke=W, stroke_width=4), s=sc), k=kf((0, dict(o=0)), (.05 + j * .05, dict(o=0)), (.06 + j * .05, dict(o=1)), (.1 + j * .05, dict(o=1)), (.11 + j * .05, dict(o=0 if j < 3 else 1)), (t['m1a'], dict(o=1 if j == 3 else 0)), (t['m1a'] + .03, dict(o=0)))))
    tally = g(tag('text', '1', x=500, y=620, font_size=40, fill=I, text_anchor='middle', data_bg='wall', style='font-family:var(--f-md);font-weight:600', data_tx='0:1|.11:½|.16:¼|.21:⅛|.26:1/16 · below sight'), k=fade(.05, t['m1a']))
    blade = g(path('M0 -300 L 0 -20 L -8 0 L 8 0 L 0 -20', stroke=I, stroke_width=10, fill=I, stroke_linejoin='round'), k=kf((0, dict(x=500, y=270, o=0)), (.05, dict(o=1)), (.08, 'n', dict(y=300)), (.1, dict(y=270)), (.13, 'n', dict(y=300)), (.15, dict(y=270)), (.18, 'n', dict(y=300)), (.2, dict(y=270)), (t['m1a'], dict(x=500, y=270)), (t['m1b'], dict(x=430, y=230))))
    # the fall through scale (zoom), then the surface of atoms
    surf = []
    for r in range(7):
        for c in range(13):
            surf.append(circle(140 + c * 60 + (r % 2) * 30, 360 + r * 50, 24, fill=GRI()))
    nyi = tag('text', 'நி', x=560, y=520, font_size=260, fill='none', stroke=I, stroke_width=20, stroke_dasharray='0 30', stroke_linecap='round', data_bg='wall', style='font-family:var(--f-ta);font-weight:600', lang='ta', data_dr='%s,%s' % (n2(t['m1b'] - .03), n2(t['m2a'])))
    nyi_fill = g(tag('text', 'நி', x=560, y=520, font_size=260, fill='none', stroke=A, stroke_width=0, data_bg='wall', style='font-family:var(--f-ta)'), k=None)
    stm = g(path('M-40 -400 L 40 -400 L 6 -20 L 0 0 L -6 -20 Z', fill=GI(), stroke=W, stroke_width=1.5), k=kf((0, dict(o=0, x=430, y=300)), (t['m1a'] + .04, dict(o=0)), (t['m1b'] - .04, dict(o=1)), (t['m1b'], dict(x=520, y=320)), (t['m2a'] - .04, 'l', dict(x=700, y=330)), (t['m2a'], dict(x=620, y=320, o=1)), (t['m2a'] + .03, dict(o=0))))
    atoms = g(surf + [nyi], k=kf((0, dict(o=0, s=.2)), (t['m1a'] + .02, dict(o=0, s=.2)), (t['m1b'] - .03, 'o', dict(o=1, s=1)), (t['m2a'], dict(o=1, s=1, y=0)), (t['m2a'] + .06, 'i', dict(o=0, s=.1, y=300))), c=(500, 520))
    # FUTURE: a chip at the bottom of a dilution refrigerator; it shrinks to a plain object on the shelf beside the speaker
    fridge = [path('M500 60 L 500 640', stroke=I, stroke_width=6)]
    for j, (w, y) in enumerate(((300, 140), (250, 260), (200, 370), (150, 470), (100, 560))):
        fridge.append(rect(500 - w / 2, y, w, 22, 4, fill=GC(), stroke=W, stroke_width=1.5))
        fridge.append(path('M%d %d L %d %d M %d %d L %d %d' % (500 - w / 2 + 14, y + 22, 500 - w / 2 + 30, y + 110, 500 + w / 2 - 14, y + 22, 500 + w / 2 - 30, y + 110), stroke=I, stroke_width=3))
    fridge.append(rect(470, 630, 60, 40, 4, fill=GI(), stroke=W, stroke_width=1.5) + circle(500, 650, 8, fill=A))
    fr = g(fridge, k=kf((0, dict(o=0, s=1, x=0, y=0)), (t['m2a'], dict(o=0)), (t['m2a'] + .04, dict(o=1, s=1)), (.8, dict(s=1, x=0, y=0)), (.86, 'i', dict(s=.28, x=-200, y=120))), c=(500, 400))
    shelf = g([rect(200, 560, 600, 22, 3, fill=GI(), stroke=W, stroke_width=1.5), rect(440, 470, 70, 90, 12, fill=GC(), stroke=W, stroke_width=1.5), ell(475, 472, 35, 6, fill=A)], k=fade(.82))
    slate = g([rect(560, 140, 340, 280, 8, fill='none', stroke=I, stroke_width=8), path('M730 150 L 730 410 M 570 200 L 890 200', stroke=I, stroke_width=3),
               text(645, 186, 'measured', 26, fill=I, anchor='middle', fam='hand', bg='wall', weight=600), text(815, 186, 'hoped', 26, fill=I, anchor='middle', fam='hand', bg='wall', weight=600),
               path('M590 250 l 110 0 M 590 290 l 90 0', stroke=I, stroke_width=4), path('M590 330 l 100 0', stroke=I, stroke_width=4, data_dr='0,.01,.86,.9'), path('M760 330 l 100 0', stroke=I, stroke_width=4, data_dr='.9,.94')],
              k=fade(.82))
    keep = g(keeper('write', 'focus', s=.8), k=kf((0, dict(o=0, x=200, y=760)), (.03, dict(o=0)), (.06, dict(o=1)), (t['m1a'], dict(o=1)), (t['m1a'] + .03, dict(o=0)), (.84, dict(o=0, x=470)), (.87, dict(o=1)), (1, dict(o=1))))
    mk = g(myna('stand', 1.0), k=kf((0, dict(o=0, x=880, y=760, r=0)), (t['m2a'], dict(o=0)), (t['m2a'] + .03, dict(o=1)), (.88, dict(r=0)), (.9, dict(r=-10)), (.92, dict(r=10)), (.94, dict(r=-10)), (.96, dict(r=0))), c=(880, 660))
    nod = g(text(880, 560, 'yes · no', 24, fill=I, anchor='middle', fam='hand', bg='wall', weight=600), k=hold(.88, .97))
    out = [g(halves), tally, blade, atoms, stm, fr, shelf, slate, keep, mk, nod]
    return dict(art=''.join(out), tr='zoom', fx=500, fy=400)


# ============================================================ 28 · Pambatti's boast
def basket():
    return ''.join([path('M-120 0 C -130 -110 130 -110 120 0 C 110 40 -110 40 -120 0 Z', fill=GC(), stroke=W, stroke_width=1.5),
                    path(''.join('M-120 %d C -60 %d 60 %d 120 %d' % (-80 + i * 20, -96 + i * 20, -96 + i * 20, -80 + i * 20) for i in range(5)), stroke=W, stroke_width=3, fill='none')])


def s28(s):
    bsk = g(at(400, 730, basket(), s=1.5), k=pop(.05, .07, 40))
    lid = g(ell(400, 600, 190, 34, fill=GI(), stroke=W, stroke_width=1.5), k=kf((0, dict(x=0, y=0, r=0)), (.08, dict(x=0, y=0, r=0)), (.12, 'b', dict(x=190, y=110, r=20)), (.88, dict(x=190, y=110, r=20)), (.93, 'i', dict(x=0, y=0, r=0))), c=(400, 640))
    COIL = [(400, 640), (420, 620), (440, 600), (420, 580), (380, 580), (360, 600), (380, 620), (400, 630)]
    UP = [(400, 640), (410, 560), (420, 470), (412, 390), (400, 320), (392, 290), (400, 260), (410, 250)]
    cobra_body = mpath([COIL, UP, UP, COIL], [.06, .14, .86, .93], k=14, closed=False, fill='none', stroke=I, stroke_width=34, stroke_linecap='round')
    hood = g([path('M410 250 C 360 260 350 330 380 350 L 440 350 C 470 330 460 260 410 250 Z', fill=GI(), stroke=W, stroke_width=1.5), path('M396 300 q 14 -12 28 0', stroke=GC(), stroke_width=5, fill='none'),
              circle(400, 266, 4, fill=W), circle(420, 266, 4, fill=W)], k=kf((0, dict(o=0, sx=.2)), (.12, dict(o=0, sx=.2)), (.15, 'b', dict(o=1, sx=1)), (.86, dict(o=1, sx=1)), (.89, dict(o=0, sx=.2))), c=(410, 300))
    sway = g([cobra_body, hood], k=kf((0, dict(r=0)), (.16, dict(r=0)), (.2, dict(r=-6)), (.24, dict(r=6)), (.28, dict(r=-6)), (.31, dict(r=0)), (.82, dict(r=0))), c=(400, 640))
    snake = g(sway, k=kf((0, dict(o=1)), (t['m1a'], dict(o=1)), (t['m1a'] + .04, dict(o=0)), (.85, dict(o=0)), (.86, dict(o=1))))
    pipe = g([circle(0, 0, 36, fill=GC(), stroke=W, stroke_width=1.5), path('M30 -10 L 120 -14 M 30 10 L 120 14', stroke=I, stroke_width=10, stroke_linecap='round'), path('M-30 -14 L -70 -24', stroke=I, stroke_width=10)],
             k=kf((0, dict(o=0, x=650, y=420)), (.05, dict(o=0)), (.08, dict(o=1)), (.2, dict(x=650, y=420)), (.22, dict(x=760, y=600)), (t['m1a'], dict(o=1)), (t['m1a'] + .03, dict(o=0))))
    # NOW: the coils unwind into flasks: change, choose, repeat; a folded ribbon twists tighter in each
    flasks = []
    for j, w in enumerate(('change', 'choose', 'repeat')):
        x = 180 + j * 220
        rib = path(''.join('M%d %d l %d %d' % (x - 30 + (k % 2) * 60, 560 - k * (22 - j * 5), (60 if k % 2 == 0 else -60), -(22 - j * 5)) for k in range(6)), stroke=I, stroke_width=6, fill='none')
        flasks.append(g([path('M%d 340 L %d 460 L %d 620 C %d 660 %d 660 %d 620 L %d 460 L %d 340 Z' % (x - 26, x - 26, x - 90, x - 90, x + 90, x + 90, x + 26, x + 26), fill='none', stroke=I, stroke_width=8),
                         path('M%d 520 L %d 620 C %d 650 %d 650 %d 620 L %d 520 Z' % (x - 70, x - 86, x - 86, x + 86, x + 86, x + 70), fill=GC(), stroke=W, stroke_width=1.5), rib, text(x, 700, w, 26, fill=I, anchor='middle', fam='mono', bg='floor', weight=600)],
                        k=kf((0, dict(o=0, y=60)), (t['m1a'] + j * .02, dict(o=0, y=60)), (t['m1a'] + .04 + j * .02, 'b', dict(o=1, y=0)), (t['m1b'] - .03, dict(o=1)), (t['m1b'] - .01, dict(o=0)))))
    # the line spreads from the last flask across the village map, over the river, into the next valley; it draws back
    mapg = g([rect(80, 140, 840, 520, 12, fill='none', stroke=I, stroke_width=5), path('M520 140 C 480 300 560 460 520 660', stroke=GC(), stroke_width=40, fill='none'),
              path('M150 560 l 40 -40 l 40 40 z M 250 580 l 40 -40 l 40 40 z M 720 300 l 40 -40 l 40 40 z', fill=I), text(220, 190, 'our valley', 24, fill=I, fam='mono', bg='wall'), text(700, 190, 'the next valley', 24, fill=I, fam='mono', bg='wall')],
             k=kf((0, dict(o=0)), (t['m1b'] - .01, dict(o=0)), (t['m1b'] + .01, dict(o=1)), (.86, dict(o=1)), (.89, dict(o=0))))
    spread = path('M200 520 C 320 420 420 420 520 400 C 640 380 700 320 780 300 C 820 290 860 260 880 220', stroke=I, stroke_width=20, fill='none', stroke_linecap='round', data_dr='%s,%s,%s,%s' % (n2(t['m1b'] + .04), n2(t['m2a'] + .06), n2(t['m2b']), n2(.84)))
    keep = g(keeper('walk1', 'focus', s=.6, anim=walk_anim(t['m2a'], t['m2b'], 6, 'stand', 'reach')), k=kf((0, dict(o=0, x=200, y=600)), (t['m2a'] - .02, dict(o=0)), (t['m2a'], dict(o=1, x=200, y=600)), (t['m2b'], 'l', dict(x=690, y=420)), (.86, dict(o=1)), (.89, dict(o=0))))
    knock = g(bubble(720, 180, 170, 60, 'knock knock', 24, tail='bl'), k=hold(t['m2b'], .8, .01))
    # gag: the myna takes the pipe and sways its head; the cobra follows the myna
    mk = g(myna('stand', 1.0), k=kf((0, dict(o=0, x=760, y=760, r=0)), (.18, dict(o=0)), (.2, dict(o=1)), (.24, dict(r=-10)), (.28, dict(r=10)), (.31, dict(r=0)), (t['m1a'], dict(o=1)), (t['m1a'] + .03, dict(o=0)), (.92, dict(o=0)), (.94, dict(o=1))), c=(760, 680))
    out = [shadow(400, 772, 200, 14), mapg, spread, g(flasks), bsk, snake, lid, pipe, mk, keep, knock]
    return dict(art=''.join(out), tr='leaf')


# ============================================================ 29 · mind froths up
def s29(s):
    POT = mirror([(500, 330), (560, 330), (566, 350), (552, 370), (640, 450), (660, 560), (620, 680), (540, 730), (500, 736)])
    pot = path(cubic(_c(POT), True), fill=GC(), stroke=W, stroke_width=1.5, class_='grain')
    potstuff = g([ell(500, 340, 62, 12, fill=W), circle(470, 334, 12, fill=I), circle(500, 328, 10, fill=I), circle(530, 336, 12, fill=I), rect(486, 322, 22, 16, 3, fill=GI())], k=fade(0))
    rnd = random.Random(29)
    bubbles = []
    for j in range(14):
        x0 = 460 + rnd.uniform(0, 80)
        layer = j % 4
        nx = 300 + (j % 5) * 100
        bubbles.append(g(circle(0, 0, rnd.uniform(7, 13), fill='none', stroke=I, stroke_width=4), k=kf((0, dict(o=0, x=x0, y=330)), (.08 + j * .012, dict(o=0, x=x0, y=330)), (.1 + j * .012, dict(o=1)), (.28 + j * .006, 'o', dict(x=x0 + rnd.uniform(-60, 60), y=120)), (t['m1a'], dict(o=1)), (t['m1b'], dict(o=0)))))
    # NOW: points of light rising through the stacked layers of a network
    layers = [(640, 6), (520, 7), (400, 7), (280, 6), (160, 4)]
    nodes, edges = [], []
    for li, (y, cnt) in enumerate(layers):
        xs = [500 + (k - (cnt - 1) / 2) * 110 for k in range(cnt)]
        for x in xs:
            nodes.append(circle(x, y, 16, fill=GI(), stroke=W, stroke_width=1.5))
        if li < len(layers) - 1:
            y2, c2 = layers[li + 1]
            xs2 = [500 + (k - (c2 - 1) / 2) * 110 for k in range(c2)]
            edges.append(''.join('M%d %d L %d %d' % (a, y, b, y2) for a in xs for b in xs2 if abs(a - b) < 240))
    net = g([path(''.join(edges), stroke=I, stroke_width=1.5, opacity='.55'), ''.join(nodes)], k=kf((0, dict(o=0)), (t['m1a'] + .02, dict(o=0)), (t['m1b'], dict(o=1)), (t['m2a'], dict(o=1, s=1, x=0)), (t['m2b'], 'i', dict(o=1, s=.42, x=0, y=60))), c=(500, 420))
    lights = []
    for j in range(8):
        x = 500 + ((j % 5) - 2) * 110
        lights.append(g(circle(0, 0, 9, fill=A, stroke=I, stroke_width=4), k=kf((0, dict(o=0, x=x, y=660)), (t['m1a'] + .04 + j * .01, dict(o=0, x=x, y=660)), (t['m1a'] + .05 + j * .01, dict(o=1)), (t['m1b'] + .06 + j * .01, 'l', dict(x=x + (j % 3 - 1) * 110, y=160)), (t['m2a'] + .02, dict(o=1)), (t['m2a'] + .04, dict(o=0)))))
    pot_g = g([pot, potstuff], k=kf((0, dict(o=1, s=1, x=0, y=0)), (t['m1a'], dict(o=1)), (t['m1b'], dict(o=0)), (t['m2a'], dict(o=0, s=.5, x=-320, y=0)), (t['m2b'], dict(o=1, s=.5, x=-320, y=0))), c=(500, 740))
    person_g = g(person('man', 'stand', 'calm', s=.75), k=kf((0, dict(o=0, x=820, y=760)), (t['m2a'] + .02, dict(o=0)), (t['m2b'], dict(o=1))))
    froth = g(''.join(text(x, y, '?', 56, fill=I, anchor='middle', fam='disp', bg='wall', weight=800) + circle(x - 22, y + 10, 9, fill='none', stroke=I, stroke_width=3) + circle(x + 24, y + 4, 7, fill='none', stroke=I, stroke_width=3) for x, y in ((200, 380), (500, 200), (820, 400))), k=fade(t['m2b'] + .02))
    keep = g(keeper('reach', 'calm', s=.7), k=kf((0, dict(o=0, x=150, y=760)), (.74, dict(o=0, x=40)), (.76, dict(o=1)), (.8, dict(x=40)), (.84, 'i', dict(x=330)), (.88, dict(x=330)), (.92, 'i', dict(x=660))))
    mk = g(myna('sip', .9), k=kf((0, dict(o=0, x=300, y=760, r=0)), (t['m1a'] - .02, dict(o=0)), (.08, dict(o=1)), (t['m1a'], dict(o=1)), (t['m1a'] + .02, dict(o=0)), (.88, dict(o=0, x=330)), (.9, dict(o=1, r=-8)), (.93, dict(r=8)), (.96, dict(r=-6)), (1, dict(r=4))), c=(300, 700))
    say = g(bubble(300, 520, 230, 70, 'I am self-aware.', 24, tail='bl'), k=hold(.9, 1.1, .01))
    out = [pot_g, g(bubbles), net, g(lights), person_g, froth, keep, mk, say]
    return dict(art=''.join(out), tr='mat')


# ============================================================ 30 · the seventh rung
def s30(s):
    X0, X1 = 360, 640
    ys = [700, 600, 500, 400, 300, 200]
    rails = path('M%d -40 L %d 760 M %d -40 L %d 760' % (X0, X0 - 20, X1, X1 + 20), stroke=GIH(), stroke_width=24, stroke_linecap='round')
    rungs = ''.join(path('M%d %d L %d %d' % (X0 - 10, y, X1 + 10, y), stroke=I, stroke_width=16, stroke_linecap='round') + path('M%d %d l 22 18 m 0 -18 l -22 18 M %d %d l 22 18 m 0 -18 l -22 18' % (X0 - 12, y - 9, X1 - 10, y - 9), stroke=GC(), stroke_width=4) for y in ys)
    crs = ''.join(creature(j + 1, 500, y - 10, .95) for j, y in enumerate(ys[:5]))
    # rung six: the person in a sensor helmet; a pen on a chart that will not close the line where "I" stops
    top = g([person('man', 'stand', 'calm', s=.3), path('M-20 -116 C -20 -136 20 -136 20 -116', fill=GI(), stroke=W, stroke_width=1.5), circle(-12, -128, 3, fill=A), circle(0, -133, 3, fill=A), circle(12, -128, 3, fill=A)], transform='translate(500 190)')
    chart = g([rect(700, 100, 260, 220, 10, fill='none', stroke=I, stroke_width=5), path('M830 140 C 900 150 920 240 860 280 C 800 310 740 260 760 200 C 772 160 800 150 822 156', stroke=I, stroke_width=4, fill='none', data_dr='%s,%s' % (n2(t['m1a'] + .04), n2(t['m1b']))),
               text(830, 300, 'where "I" stops?', 18, fill=I, anchor='middle', fam='mono', bg='wall')], k=hold(t['m1a'] + .02, t['m2a'] + .04))
    seventh = g([path('M%d 100 L %d 100' % (X0 - 10, X1 + 10), stroke=I, stroke_width=16, stroke_linecap='round', data_dr='%s,%s' % (n2(t['m2a']), n2(t['m2a'] + .06))),
                 path('M%d 91 l 22 18 m 0 -18 l -22 18 M %d 91 l 22 18 m 0 -18 l -22 18' % (X0 - 12, X1 - 10), stroke=GC(), stroke_width=4, data_dr='%s,%s' % (n2(t['m2a'] + .05), n2(t['m2a'] + .08))),
                 text(500, 70, '7 ?', 30, fill=I, anchor='middle', fam='hand', bg='wall', weight=600)], k=fade(t['m2a']))
    ladder = g([rails, rungs, crs, top, seventh], k=kf((0, dict(y=0, s=1)), (t['m1a'], dict(y=0, s=1)), (t['m2a'], dict(y=0)), (t['m2b'], 'i', dict(y=180, s=1.25)), (.9, dict(y=180, s=1.25)), (1, dict(y=40, s=1.05))), c=(500, 400))
    # the queue at the foot: the machine, a second machine, the myna; each has to start at the grass
    def bot(x):
        return at(x, 760, rect(-30, -96, 60, 90, 12, fill=GI(), stroke=W, stroke_width=1.5) + circle(-10, -60, 6, fill=W) + circle(10, -60, 6, fill=W) + path('M-16 -6 l 0 6 M 16 -6 l 0 6', stroke=I, stroke_width=8))
    queue = g([bot(760), bot(850), at(930, 760, myna('stand', .7))], k=kf((0, dict(o=0, x=120)), (t['m2b'], dict(o=0, x=120)), (t['m2b'] + .04, 'o', dict(o=1, x=0))))
    keep = g(keeper('stand', 'calm', s=.7), k=kf((0, dict(o=0, x=200, y=760)), (.06, dict(o=0)), (.1, dict(o=1)), (1, dict(o=1))))
    sandals = g(path('M150 756 l 24 0 M 180 760 l 24 0', stroke=I, stroke_width=6, stroke_linecap='round'), k=fade(.84))
    mtest = g(myna('stand', .8), k=kf((0, dict(o=0, x=420, y=100)), (.82, dict(o=0)), (.84, dict(o=1, y=60)), (.88, dict(y=96)), (.9, dict(y=60)), (.94, dict(o=1, x=600, y=60)), (.98, dict(o=0))))
    out = [ladder, chart, queue, keep, sandals, mtest]
    return dict(art=''.join(out), tr='leaf', pu='%s:1:500:100' % n2(t['m2b']))


# ============================================================ 31 · the lamp, and the ledger
def kuthuvilakku():
    """Standing lamp: round base, ringed stem, a shallow bowl with five wick spouts, a bird on the finial. Brass is drawn in ink (rule 9)."""
    out = [path('M380 760 C 380 700 620 700 620 760 Z', fill=GIH(), stroke=W, stroke_width=1.5),
           rect(484, 380, 32, 330, 10, fill=GIH(), stroke=W, stroke_width=1.5)]
    for y in (420, 500, 580, 660):
        out.append(ell(500, y, 34, 12, fill=GI(), stroke=W, stroke_width=1.5))
    out.append(path('M360 360 C 380 400 620 400 640 360 Z', fill=GIH(), stroke=W, stroke_width=1.5))
    for j, x in enumerate((360, 420, 500, 580, 640)):
        out.append(path('M%d 362 l %d -18 l %d 0 z' % (x - 10, -6 if x < 500 else 6, 20), fill=GI(), stroke=W, stroke_width=1.5))
    out.append(rect(492, 260, 16, 100, 6, fill=GIH(), stroke=W, stroke_width=1.5))
    out.append(path('M470 262 C 470 220 520 200 540 220 L 566 214 L 548 232 C 548 252 520 262 470 262 Z', fill=GI(), stroke=W, stroke_width=1.5) + circle(530, 226, 4, fill=W))
    return ''.join(out)


def s31(s):
    lamp = kuthuvilakku()
    f1 = flame(360, 344, 1.5)
    f2 = g(flame(420, 344, 1.5), k=fade(.36, f=.01))
    f3 = g(flame(500, 344, 1.5), k=fade(.4, f=.01))
    bulb = g([path('M300 240 C 300 120 420 120 420 240 C 420 290 390 300 386 340 L 334 340 C 330 300 300 290 300 240 Z', fill='none', stroke=I, stroke_width=5),
              path('M340 330 L 344 260 C 350 230 370 230 376 260 L 380 330', stroke=I, stroke_width=3, fill='none'), rect(334, 340, 52, 26, 4, fill=GI())],
             k=kf((0, dict(o=0)), (.1, dict(o=0)), (.13, dict(o=1)), (.2, dict(o=1)), (.22, dict(o=0))))
    sun = g([circle(500, 200, 110, fill=GC(), stroke=W, stroke_width=1.5), path(''.join('M%d %d l %d %d' % (500 + 130 * math.cos(a), 200 + 130 * math.sin(a), 40 * math.cos(a), 40 * math.sin(a)) for a in [i * .524 for i in range(12)]), stroke=I, stroke_width=6, stroke_linecap='round'),
             path('M80 760 L 80 640 L 140 600 L 200 640 L 200 760 M 240 760 L 240 660 L 300 620 L 360 660 L 360 760 M 640 760 L 640 650 L 700 610 L 760 650 L 760 760 M 800 760 L 800 630 L 870 590 L 940 630 L 940 760', fill=GI(), stroke=W, stroke_width=1.5)],
            k=kf((0, dict(o=0, s=.2)), (.2, dict(o=0, s=.2)), (.24, 'o', dict(o=1, s=1)), (.3, dict(o=1)), (.33, dict(o=0))), c=(500, 200))
    lamp_g = g(g([lamp, f1, f2, f3, bulb], transform='translate(-125 -190) scale(1.25)'), k=kf((0, dict(o=0, y=60)), (.03, dict(o=0, y=60)), (.07, 'b', dict(o=1, y=0)), (.2, dict(o=1)), (.22, dict(o=0)), (.32, dict(o=0)), (.34, dict(o=1)), (.5, dict(o=1)), (.56, dict(o=.0))))
    keep = g(keeper('reach', 'smile', s=.85, hold=path('M0 0 L 40 -60', stroke=I, stroke_width=4) + circle(40, -64, 5, fill=A)), k=kf((0, dict(o=0, x=180, y=760)), (.32, dict(o=0)), (.34, dict(o=1)), (.5, dict(o=1)), (.55, dict(o=0))))
    mk = g(myna('stand', .9), k=kf((0, dict(o=0, x=820, y=760)), (.34, dict(o=0)), (.36, dict(o=1)), (.5, dict(o=1)), (.55, dict(o=0))))
    return dict(art=''.join([shadow(500, 772, 160, 12), sun, lamp_g, keep, mk]), tr='fade', html=ledger_leaf(s))


LED_TEXT = None


def ledger_leaf(s):
    import script_data as SD
    import pathlib
    here = pathlib.Path(__file__).resolve().parent
    _, led, pencil = SD.parse(here.parents[1] / 'v3_script_final.md')
    items = ''.join('<li><span class="c" lang="ta">%s</span><span class="t">%s</span></li>' % (c, esc(tx)) for c, tx in led)
    k = kf((0, dict(o=0, y=40, sy=.06)), (.52, dict(o=0, y=40, sy=.06)), (.55, dict(o=1, y=0, sy=.06)), (.66, 'o', dict(o=1, y=0, sy=1)))
    feet = '<span class="feet" aria-hidden="true" data-k="%s">· ˙ · ˙ · ˙</span>' % kf((0, dict(o=0)), (.86, dict(o=0)), (.9, dict(o=1)))
    return ('<div class="bigleaf" data-k="%s"><p class="pl">%s</p><ol>%s</ol>'
            '<div class="yours"><label for="l14">14 · yours</label><input id="l14" type="text" maxlength="90" autocomplete="off" placeholder="|" aria-label="line fourteen, yours; it stays on this device">%s</div>'
            '<div class="foot"><span>this file will be wrong. that\'s still the deal.</span><span><a href="#file">read the file</a> <button type="button" id="watchAgain">watch again</button></span></div></div>'
            % (k, esc(pencil), items, feet))
