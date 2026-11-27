"""Scenes 03-08: the anklet, the hoard, the letter, the lamp, the row, the screen."""
import math
import random
from art import *  # noqa: F401,F403
import art as AR
from objects import walk_anim, hand_grip, _grain

t = AR.T


def fade(a, b=None, f=.04):
    return show(a, b, f)


def hold(a, b, f=.03):
    """Visible only between a and b."""
    return kf((0, dict(o=0)), (a - f, dict(o=0)), (a, dict(o=1)), (b, dict(o=1)), (b + f, dict(o=0)))


def gem(x, y, r=13):
    return circle(x, y, r + 4, fill=I) + path('M%s %s l %s %s l %s %s l %s %s z' % (n(x), n(y - r), n(r), n(r), n(-r), n(r), n(-r), n(-r)), fill=A) + circle(x - r * .3, y - r * .35, r * .22, fill=PP)


def ring_half(cx, cy, rx, ry, th, side):
    """Half an annulus (side -1 left, 1 right) as a closed outline."""
    out = [(cx + side * rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))) for a in range(-90, 91, 6)]
    inn = [(cx + side * (rx - th) * math.cos(math.radians(a)), cy + (ry - th) * math.sin(math.radians(a))) for a in range(90, -91, -6)]
    return out + inn


def frame_half(x, y, w, h, th, side):
    """Half of a rectangular frame (the terminal rim)."""
    cx = x + w / 2
    if side < 0:
        o = [(cx, y), (x, y), (x, y + h), (cx, y + h), (cx, y + h - th), (x + th, y + h - th), (x + th, y + th), (cx, y + th)]
    else:
        o = [(cx, y), (x + w, y), (x + w, y + h), (cx, y + h), (cx, y + h - th), (x + w - th, y + h - th), (x + w - th, y + th), (cx, y + th)]
    return o


# ============================================================ 03 · the king who did not check
def s03(s):
    out = [shadow(500, 772, 360, 22)]
    CX, CY = 510, 330
    # the court: two carved pillars, faint, at the edges (THEN only)
    pill = ''.join(rect(x, 120, 46, 640, 6, fill=GI(), stroke=W, stroke_width=1.5) + path('M%d 160 l 46 0 M %d 720 l 46 0' % (x, x), stroke=DK, stroke_width=6) for x in (90, 870))
    out.append(g(pill, k=kf((0, dict(o=0)), (.05, dict(o=0)), (.1, dict(o=.9)), (t['m1a'], dict(o=.9)), (t['m1a'] + .05, dict(o=0)))))
    # the anklet halves: whole while held up, dashed down, rejoined as the terminal rim, cracked open again
    halves = []
    for side in (-1, 1):
        a0 = ring_half(CX, CY, 150, 104, 30, side)
        a1 = frame_half(330, 300, 360, 300, 40, side)
        d = mpath([a0, a0, a1, a1], [0, t['m1a'] + .04, t['m1b'], 1], k=44, fill=GCH() if side < 0 else GC(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke')
        bells = '' if side > 0 else ''.join(circle(CX + 150 * math.cos(math.radians(a)), CY + 104 * math.sin(math.radians(a)) + 16, 9, fill=GC(), stroke=W, stroke_width=1.5) for a in range(40, 150, 14))
        hl = path('M%s %s q %s -60 %s -96' % (n(CX + side * 120), n(CY + 30), n(side * 18), n(side * 4)), stroke=PP, stroke_width=4, fill='none', stroke_linecap='round', opacity='.8')
        bit = g([bells, g(hl, k=fade(0, t['m1a']))], k=fade(0, t['m1a']))
        # fall: dropped from the hand, strikes the floor, halves fly apart; rise and rejoin; crack open in FUTURE
        k = kf((0, dict(x=0, y=0, r=0, o=0)), (.05, dict(o=0, y=-40)), (.09, 'b', dict(o=1, y=0)), (.15, dict(x=0, y=0, r=0)),
               (.2, 'n', dict(x=side * 20, y=330, r=side * 8)), (.24, 'o', dict(x=side * 120, y=330, r=side * 28)),
               (t['m1a'], dict(x=side * 120, y=330, r=side * 28)), (t['m1a'] + .06, 'i', dict(x=0, y=0, r=0)),
               (t['m2a'] + .02, dict(x=0, y=0, r=0)), (t['m2a'] + .08, 'b', dict(x=side * 70, y=10, r=side * 12)))
        halves.append(g([d, bit], k=k, c=(CX, CY + 100)))
    # the hand that holds it up (THEN)
    hand = g(at(CX, CY - 104, hand_grip(0, 0), s=.9), k=kf((0, dict(y=-300)), (.04, dict(y=-300)), (.08, 'o', dict(y=0)), (.15, dict(y=0)), (.19, dict(y=-40)), (.24, 'n', dict(y=-460))))
    # stones scatter across the whole frame
    rnd = random.Random(3)
    stones = []
    for i in range(14):
        tx = 60 + i * 66 + rnd.uniform(-20, 20)
        ty = 740 + rnd.uniform(-10, 60)
        kk = kf((0, dict(o=0, x=CX, y=CY + 60)), (.195, dict(o=0, x=CX, y=CY + 420)), (.2, dict(o=1, x=CX, y=CY + 420)),
                (.25 + rnd.uniform(0, .04), 'o', dict(x=tx, y=ty)), (t['m1a'], dict(o=1)), (t['m1a'] + .04, dict(o=0)))
        stones.append(g(gem(0, 0, 11 + rnd.uniform(0, 5)), k=kk))
    # the terminal (NOW): screen, keys, the shortfall; nobody opens it
    term = ''.join([
        rect(370, 340, 280, 120, 8, fill=DK, stroke=I, stroke_width=3),
        text(386, 382, 'SHORTFALL', 26, fill=PP, fam='mono', bg='dk', weight=600),
        text(634, 440, '−3,412.00', 40, fill=PP, anchor='end', fam='mono', bg='dk', weight=600),
    ] + [rect(380 + (j % 4) * 66, 480 + (j // 4) * 34, 56, 24, 5, fill=GI(), stroke=W, stroke_width=1.5) for j in range(12)]
      + [rect(390, 286, 240, 18, 4, fill=DK, stroke=I, stroke_width=3)])
    now = g(term, k=kf((0, dict(o=0)), (t['m1b'] - .03, dict(o=0)), (t['m1b'], dict(o=1)), (t['m2a'] + .02, dict(o=1)), (t['m2a'] + .06, dict(o=0))))
    # FUTURE: the case cracked: under every figure, a signed line with a thumbprint
    thumb = ''.join(path('M%s %s a %s %s 0 1 1 1 0' % (n(600), n(520 - r), n(r), n(r * 1.25)), stroke=I, stroke_width=2.2, fill='none') for r in (8, 14, 20, 26))
    signed = g([rect(380, 330, 260, 300, 10, fill=GI(), stroke=W, stroke_width=1.5),
                text(400, 380, 'SHORTFALL −3,412.00', 22, fill=DK, fam='mono', bg='ink', weight=600),
                path('M400 404 L 620 404', stroke=DK, stroke_width=2),
                text(400, 450, 'weighed by:', 24, fill=DK, fam='mono', bg='ink'),
                text(400, 500, 'P. Valli, clerk', 34, fill=DK, fam='hand', bg='ink', weight=600),
                g(thumb.replace('var(--ink)', 'var(--dk)'), transform='translate(0 60)'),
                text(400, 610, 'checked · 2041', 20, fill=DK, fam='mono', bg='ink')],
               k=kf((0, dict(o=0, s=.7)), (t['m2a'] + .07, dict(o=0, s=.7)), (t['m2b'], 'b', dict(o=1, s=1))), c=(510, 480))
    # the receipt that never stops: FAIR, FAIR, FAIR, out of the frame
    rc = [rect(700, 470, 80, 900, 3, fill=GI(), stroke=W, stroke_width=1.5)] + [text(740, 510 + j * 60, 'FAIR', 26, fill=DK, anchor='middle', fam='mono', bg='ink', weight=600) for j in range(15)]
    clip = '<clipPath id="rcclip"><rect x="690" y="476" width="100" height="1600"/></clipPath>'
    receipt = clip + g(g(g(rc), k=kf((0, dict(y=-910)), (t['g0'], dict(y=-910)), (1, 'l', dict(y=380)))), clip_path='url(#rcclip)')
    # the keeper cracks the case (FUTURE); the myna chases a stone and brings it back
    keep = g(keeper('reach', 'focus', s=.95), k=kf((0, dict(o=0, x=-100, y=760)), (t['m1b'], dict(o=0, x=-100)), (t['m2a'], 'o', dict(o=1, x=200)), (1, dict(x=200))))
    mk = g(myna('stand', 1.1), k=kf((0, dict(o=0, x=980, y=760)), (.22, dict(o=0, x=980)), (.24, dict(o=1, x=900)), (.28, 'i', dict(x=700)), (t['m1a'] + .02, dict(x=700)), (t['m1a'] + .08, 'i', dict(x=860)), (1, dict(x=860))))
    carried = g(gem(0, 0, 10), k=kf((0, dict(o=0, x=760, y=752)), (.27, dict(o=0, x=760, y=752)), (.28, dict(o=1, x=760, y=752)), (t['m1a'] + .02, dict(x=780, y=652)), (t['m1a'] + .08, 'i', dict(x=950, y=652)), (t['m2a'], dict(o=1)), (t['m2a'] + .03, dict(o=0))))
    out += [now, g(halves), hand, g(stones), signed, receipt, keep, mk, carried]
    return dict(art=''.join(out), tr='mat', fx=510, fy=480)


# ============================================================ 04 · the hoard becomes a tank
def pot_pts(cx=500, base=740, h=480, w=180):
    half = [(cx, base - h), (cx + 46, base - h), (cx + 50, base - h + 26), (cx + 34, base - h + 40), (cx + 38, base - h + 110),
            (cx + w * .82, base - h + 200), (cx + w, base - h + 300), (cx + w * .86, base - 70), (cx + w * .45, base - 6), (cx, base)]
    return mirror(half)


def coin(x, y, r=34, blur=0, blank=False, accent=False):
    face = '' if blank else ''.join([
        path('M%s %s c 6 -18 22 -26 34 -14 c 6 6 2 16 -4 20 l 4 8 l -8 2 l 2 10 c -12 6 -26 2 -30 -8 z' % (n(x - 16), n(y - 2)), fill=PP),
        path('M%s %s q 10 -10 22 -6' % (n(x - 14), n(y - 14)), stroke=PP, stroke_width=3, fill='none', stroke_dasharray='3 3'),
    ])
    dots = ''.join(circle(x + (r - 6) * math.cos(a / 12 * 6.283), y + (r - 6) * math.sin(a / 12 * 6.283), 2.2, fill=PP) for a in range(12))
    body = circle(x, y, r, fill=GRI(), stroke=W, stroke_width=1.5) + circle(x, y, r - 3, fill='none', stroke=A if accent else PP, stroke_width=2.5)
    inner = g(face + dots, filter='url(#fb%d)' % blur if blur else None)
    return body + inner


def s04(s):
    out = []
    POT = pot_pts()
    VAULT = rrect_pts(250, 230, 500, 520, 40)
    pot = mpath([POT, POT, VAULT, VAULT], [0, t['m1a'], t['m1b'], 1], k=44, fill=GC(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke', class_='grain')
    # x-ray window into the pot: coins heaped inside, one catching the light (brass)
    rnd = random.Random(4)
    heap = ''.join(coin(500 + rnd.uniform(-110, 110), 560 + rnd.uniform(-60, 110), 26, accent=(i == 9)) for i in range(16))
    window = g([ell(500, 590, 140, 120, fill=W, stroke=I, stroke_width=3, stroke_dasharray='9 8'), heap], k=fade(.12, t['m1a'] + .02))
    neck = g([path('M455 268 q 45 -14 90 0', stroke=PP, stroke_width=4, fill='none'), path('M520 300 q 40 -20 60 30', stroke=PP, stroke_width=6, fill='none', opacity='.6')], k=fade(.06, t['m1a']))
    # buried to its shoulder: the earth in front (floor colour, negative space), with soil strokes
    earth = g([path('M120 760 C 260 700 360 690 430 692 L 570 692 C 640 690 760 700 880 760 L 880 1000 L 120 1000 Z', fill=F),
               path('M300 724 q 30 -8 60 0 M 640 716 q 40 -10 70 2 M 420 708 q 14 -4 26 0', stroke=I, stroke_width=3, fill='none', stroke_linecap='round')],
              k=kf((0, dict(o=1)), (t['m1a'], dict(o=1)), (t['m1a'] + .05, dict(o=0))))
    # label "for later", four centuries of handwriting, each struck by the next
    lab = [rect(560, 250, 190, 150, 8, fill=PP, stroke=I, stroke_width=3), path('M545 276 L 560 280', stroke=I, stroke_width=3)]
    hands = [('for later', 'hand', 32), ('for later', 'serif', 25), ('for later', 'mono', 22), ('for later', 'disp', 24)]
    for j, (w, fam, sz) in enumerate(hands):
        y = 284 + j * 32
        lab.append(text(578, y, w, sz, fill=I, fam=fam, bg='wall', weight=600 if fam == 'disp' else None))
        if j < 3:
            lab.append(path('M574 %d l 130 -3' % (y - 8), stroke=I, stroke_width=2.5, data_dr='%s,%s' % (n2(.13 + j * .03), n2(.15 + j * .03))))
    label = g(lab, k=kf((0, dict(o=0, r=-10)), (.1, dict(o=0, r=-10)), (.14, 'b', dict(o=1, r=0)), (t['m1a'], dict(o=1)), (t['m1a'] + .03, dict(o=0))), c=(560, 260))
    # NOW: the vault, its door, and coins struck from coins: sharp, blurred, blank
    vault = g([circle(500, 380, 96, fill=GI(), stroke=W, stroke_width=1.5), circle(500, 380, 70, fill='none', stroke=DK, stroke_width=5),
               path('M500 310 L 500 450 M 430 380 L 570 380 M 451 331 L 549 429 M 451 429 L 549 331', stroke=DK, stroke_width=6, stroke_linecap='round'),
               circle(500, 380, 18, fill=A, stroke=DK, stroke_width=3), rect(286, 260, 40, 16, 4, fill=I), rect(674, 260, 40, 16, 4, fill=I)],
              k=kf((0, dict(o=0)), (t['m1b'] - .03, dict(o=0)), (t['m1b'], dict(o=1)), (t['m2a'], dict(o=1)), (t['m2a'] + .03, dict(o=0))))
    copies = []
    for j in range(5):
        x = 300 + j * 100
        copies.append(g(coin(x, 600, 40, blur=min(j, 3), blank=(j == 4)) + (path('M%d 600 l 22 0 l -6 -6 m 6 6 l -6 6' % (x + 44), stroke=PP, stroke_width=3, fill='none') if j < 4 else ''),
                        k=kf((0, dict(o=0, s=.4)), (t['m1b'] + j * .015, dict(o=0, s=.4)), (t['m1b'] + .03 + j * .015, 'b', dict(o=1, s=1)), (t['m2a'], dict(o=1)), (t['m2a'] + .03, dict(o=0))), c=(x, 600)))
    copies.append(g(text(500, 800, 'copy of a copy of a copy', 26, fill=I, anchor='middle', fam='mono', bg='floor'), k=hold(t['m1b'] + .05, t['m2a'])))
    # FUTURE: the crack, water, and the pull-back to the village tank (ஏரி) with its earthen bund and stone sluice
    crack = path('M500 232 L 486 300 L 512 352 L 490 420 L 516 480 L 498 560 L 506 640 L 500 750', stroke=W, stroke_width=10, fill='none', stroke_linejoin='round', data_dr='%s,%s' % (n2(t['m2a']), n2(t['m2a'] + .05)))
    water = path('M500 750 C 498 820 470 880 420 960', stroke=I, stroke_width=22, fill='none', stroke_linecap='round', data_dr='%s,%s' % (n2(t['m2a'] + .04), n2(t['m2a'] + .08)))
    potgrp = g([pot, window, neck, vault, g(copies), crack, water], k=kf((0, dict(s=1, x=0, y=0)), (t['m2a'] + .08, dict(s=1, x=0, y=0)), (t['m2b'], 'i', dict(s=.16, x=0, y=60))), c=(500, 560))
    # the tank, revealed as the camera pulls back
    tank = [path('M-200 560 C 100 470 900 470 1200 560 L 1200 640 L -200 640 Z', fill=GC(), stroke=W, stroke_width=1.5),   # earthen bund
            path('M-200 640 L 1200 640 L 1200 760 L -200 760 Z', fill=GI(), stroke=W, stroke_width=1.5),                       # water
            path('M-150 668 q 40 -8 80 0 t 80 0 M 120 700 q 40 -8 80 0 t 80 0 M 620 676 q 40 -8 80 0 t 80 0 M 820 716 q 40 -8 80 0 t 80 0', stroke=PP, stroke_width=4, fill='none'),
            rect(460, 520, 26, 130, 3, fill=GI(), stroke=W, stroke_width=1.5), rect(514, 520, 26, 130, 3, fill=GI(), stroke=W, stroke_width=1.5),
            rect(450, 510, 100, 18, 3, fill=GI(), stroke=W, stroke_width=1.5),
            path('M40 560 l 0 -40 M 960 560 l 0 -40', stroke=I, stroke_width=4)]
    folk = ''.join(at(x, y, person(w, p, 'calm', s=sc, flip=f)) for x, y, w, p, sc, f in
                   [(140, 560, 'woman', 'hold', .42, False), (300, 540, 'man', 'stand', .4, False), (700, 540, 'woman', 'serve', .42, True), (860, 560, 'man', 'hold', .42, True)])
    silt = ''.join(at(x, 740, person('man', 'carry', 'calm', s=.36, hold=''), flip=(x > 500)) + ell(x + (8 if x < 500 else -8), 600, 26, 12, fill=GC(), stroke=W, stroke_width=1.5) for x in (240, 380, 640, 780))
    tankg = g([g(tank), g(folk), g(silt, k=fade(t['m2b'] + .06))], k=kf((0, dict(o=0, s=3.2)), (t['m2a'] + .06, dict(o=0, s=3.2)), (t['m2a'] + .09, dict(o=1, s=3.2)), (t['m2b'], 'i', dict(o=1, s=1))), c=(500, 590))
    out += [earth, tankg, potgrp, label]
    # the keeper puts her ear to the pot before it cracks
    keep = g(keeper('listen', 'sleepy', s=1.0), k=kf((0, dict(o=0, x=140, y=760)), (.07, dict(o=0)), (.12, 'b', dict(o=1)), (t['m1a'], dict(x=140)), (t['m1b'], dict(x=150)), (t['m2a'], dict(o=1, x=150)), (t['m2a'] + .04, dict(o=0))))
    out.insert(1, keep)
    return dict(art=''.join(out), tr='zoom', fx=500, fy=640)


# ============================================================ 05 · the third voice
def petal_pts():
    pts = []
    for i in range(41):
        u = i / 40
        x = 110 + 780 * u
        w = 118 * math.sin(math.pi * u) ** .7 * (1 - .35 * u)
        pts.append((x, 420 - w + 18 * math.sin(u * 3)))
    for i in range(40, -1, -1):
        u = i / 40
        x = 110 + 780 * u
        w = 118 * math.sin(math.pi * u) ** .7 * (1 - .35 * u)
        pts.append((x, 420 + w + 18 * math.sin(u * 3)))
    return pts


def bubble_pts(x, y, w, h):
    p = rrect_pts(x, y, w, h, 34)
    return p


def s05(s):
    out = []
    PET = petal_pts()
    BUB = bubble_pts(300, 250, 400, 260)
    LET = rrect_pts(310, 120, 380, 600, 18)
    shape = mpath([PET, PET, BUB, BUB, LET], [0, t['m1a'], t['m1b'], t['m2a'], t['m2b']], k=48, fill=GI(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke', class_='paper')
    veins = g(path(''.join('M%d %d C %d %d %d %d %d %d' % (200, 420 + j * 9, 400, 400 + j * 14, 600, 404 + j * 12, 800, 430 + j * 5) for j in range(-3, 4)), stroke=DK, stroke_width=1.2, fill='none', opacity='.35'), k=fade(.05, t['m1a']))
    # writing in red lac with a jasmine bud
    lac = g(scribble(200, 370, 600, 110, 4, seed=5, sw=4, lmin=14, lmax=34), k=kf((0, dict(o=0)), (.1, dict(o=0)), (.16, dict(o=1)), (t['m1a'], dict(o=1)), (t['m1a'] + .02, dict(o=0))))
    bud = g([path('M0 0 L -70 -70', stroke=GC(), stroke_width=8, stroke_linecap='round'), ell(-80, -80, 12, 20, fill=PP, stroke=DK, stroke_width=3, transform='rotate(-45 -80 -80)'), circle(0, 0, 5, fill=A)],
            k=kf((0, dict(o=0, x=250, y=420)), (.09, dict(o=1, x=250, y=420)), (.17, 'l', dict(x=730, y=430)), (.2, dict(o=0, x=760, y=380))))
    # roll it: the petal squeezes into a scroll and goes with the friend
    friend = g(person('friend', 'walk1', 'calm', s=.9, anim=walk_anim(.21, .3, 4, 'stand')), k=kf((0, dict(o=0, x=900, y=760)), (.17, dict(o=0, x=900)), (.2, dict(o=1, x=860)), (.3, 'l', dict(x=1040)), (t['m1a'] + .01, dict(o=0, x=1080))))
    look = g(path('M0 0 q 10 -14 22 -4', stroke=I, stroke_width=4, fill='none'), k=hold(.25, .27))
    # NOW: three typing dots, then a perfect paragraph at once; the wall of identical bubbles
    dots = g([circle(450 + j * 50, 380, 16, fill=DK, class_='tick') for j in range(3)], k=hold(t['m1b'] - .01, t['m1b'] + .03))
    para = [path('M330 %d L %d %d' % (300 + j * 34, 670 - (j == 5) * 120, 300 + j * 34), stroke=DK, stroke_width=8, stroke_linecap='round') for j in range(6)]
    parag = g(para, k=hold(t['m1b'] + .035, t['m2a'] + .02, .005))
    wall = []
    pos = [(70, 80), (380, 40), (690, 90), (60, 560), (720, 560), (80, 320), (720, 330), (390, 600)]
    for j, (x, y) in enumerate(pos):
        b = [rect(x, y, 230, 140, 26, fill=GI(), stroke=W, stroke_width=1.5), path('M%d %d l -10 26 l 30 -14 z' % (x + 30, y + 138), fill=GI())]
        b += [path('M%d %d L %d %d' % (x + 22, y + 34 + q * 26, x + 210 - (q == 3) * 60, y + 34 + q * 26), stroke=DK, stroke_width=6, stroke_linecap='round') for q in range(4)]
        wall.append(g(b, k=kf((0, dict(o=0, s=.3)), (t['m1b'] - .03 + j * .005, dict(o=0, s=.3)), (t['m1b'] + j * .005, 'b', dict(o=1, s=1)), (t['m2a'], dict(o=1, s=1)), (t['m2a'] + .04, dict(o=0, s=.8))), c=(x + 115, y + 70)))
    # FUTURE: the letter that keeps its drafts
    let = [text(340, 180, 'my dear,', 34, fill=DK, fam='hand', bg='ink', weight=600)]
    let.append(text(340, 240, 'I wanted to say this well', 28, fill=DK, fam='hand', bg='ink'))
    let.append(path('M338 232 l 300 -4', stroke=DK, stroke_width=3))
    let.append(text(340, 290, 'I cannot say it well', 28, fill=DK, fam='hand', bg='ink'))
    let.append(path('M338 282 l 250 2', stroke=DK, stroke_width=3))
    let.append(text(340, 350, 'come back · come back · come', 28, fill=DK, fam='hand', bg='ink'))
    let.append(text(340, 410, 'back', 28, fill=DK, fam='hand', bg='ink'))
    let.append(text(340, 470, '.   .   .   .   .   .', 30, fill=DK, fam='hand', bg='ink'))
    let.append(text(340, 540, 'come anyway.', 34, fill=DK, fam='hand', bg='ink', weight=600))
    letter = g(let, k=fade(t['m2b'] - .02))
    stain = g([ell(560, 600, 62, 44, fill=GC(), opacity='.9'), ell(540, 588, 22, 14, fill=PP, opacity='.4')],
              k=kf((0, dict(o=0)), (t['m2b'] + .02, dict(o=0)), (t['m2b'] + .04, dict(o=1)), (.8, dict(o=1)), (.82, dict(o=0)), (.88, dict(o=0)), (.9, dict(o=1))))
    tidy = g([path('M520 560 l 20 20 m 20 -30 l 0 30 m 20 -20 l -20 20', stroke=DK, stroke_width=4), text(560, 660, 'tidied', 22, fill=DK, anchor='middle', fam='mono', bg='ink')], k=hold(.8, .85))
    finger = g(hand_grip(0, 0), k=kf((0, dict(o=0, x=560, y=-200)), (.85, dict(o=0, x=560, y=-200)), (.86, dict(o=1)), (.88, 'o', dict(x=560, y=560)), (.92, 'n', dict(x=560, y=-400))))
    keep = g(keeper('write', 'focus', s=.95), k=kf((0, dict(o=0, x=-80, y=760)), (t['m2a'], dict(o=0)), (t['m2b'], 'o', dict(o=1, x=170)), (1, dict(x=170))))
    out += [g([shape, veins, lac], k=kf((0, dict(sx=1)), (.2, dict(sx=1)), (.22, dict(sx=1)), (t['m1a'], dict(sx=1))), c=(500, 420)), bud, g(wall), dots, parag, letter, stain, tidy, keep, friend, finger]
    return dict(art=''.join(out), tr='leaf')


# ============================================================ 06 · the lamp that can go out
def agal_pts(cx=500, y=640, w=300):
    pts = [(cx - w * .5, y - 40), (cx - w * .2, y - 70), (cx + w * .2, y - 70), (cx + w * .48, y - 60), (cx + w * .62, y - 76), (cx + w * .58, y - 38),
           (cx + w * .38, y + 30), (cx, y + 52), (cx - w * .38, y + 34), (cx - w * .5, y - 4)]
    return pts


def s06(s):
    out = [shadow(500, 772, 300, 20)]
    AG = agal_pts(470, 640, 500)
    PH = [(250, 640), (700, 590), (800, 670), (340, 726)]
    AG2 = agal_pts(470, 650, 440)
    lamp = mpath([AG, AG, PH, PH, AG2], [0, t['m1a'], t['m1b'], t['m2a'] + .08, t['m2b']], k=48, tension=[1, 1, 0, 0, 1], fill=GC(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke', class_='grain')
    oil = g(ell(440, 588, 200, 24, fill=GI(), stroke=W, stroke_width=1.5) + path('M300 580 q 120 -14 260 -6', stroke=PP, stroke_width=3, fill='none', opacity='.7'), k=fade(0, t['m1a']))
    wick = path('M720 566 q 20 -14 34 -40', stroke=I, stroke_width=10, stroke_linecap='round', fill='none')
    fl1 = g(flame(756, 528, 2.2), k=kf((0, dict(o=1, s=1)), (.2, dict(s=1)), (.27, 'n', dict(s=.15, o=0))), c=(756, 528))
    smoke1 = path('M756 520 C 730 440 790 380 750 300 C 724 240 776 180 750 80', stroke=I, stroke_width=3, fill='none', data_dr='.26,.31,%s,%s' % (n2(t['m1a']), n2(t['m1a'] + .04)))
    then = g([oil, wick, fl1], k=fade(0, t['m1a']))
    # NOW: the phone face up; it dims, then shows the time, a dot, another dot
    scr = g([path(poly([(276, 640), (692, 600), (772, 666), (352, 708)]), fill=DK, stroke=I, stroke_width=2),
             text(524, 670, '23:47', 44, fill=PP, anchor='middle', fam='mono', bg='dk', transform='rotate(-6 524 660)', data_tx='0:23:47|%s:23:47 ·|%s:23:47 · ·' % (n2(t['m1b'] + .03), n2(t['m1b'] + .06)))],
            k=kf((0, dict(o=0)), (t['m1b'] - .02, dict(o=0)), (t['m1b'], dict(o=1)), (t['m2a'] + .06, dict(o=1)), (t['m2a'] + .09, dict(o=0))))
    # the wall of glowing rectangles, switching off from the edges inward
    rects = []
    cols, rows = 6, 4
    for r in range(rows):
        for c in range(cols):
            x, y = 40 + c * 158, 80 + r * 118
            if r == rows - 1 and 2 <= c <= 3:
                continue
            ring = max(abs(c - 2.5), abs(r - 1.5) * 1.4)
            off = t['m2a'] + .02 + (3 - ring) * .025
            rr = [rect(x, y, 130, 96, 12, fill=GI(), stroke=W, stroke_width=1.5), rect(x + 10, y + 10, 110, 76, 6, fill=DK),
                  path('M%d %d l 60 0 M %d %d l 84 0 M %d %d l 40 0' % (x + 20, y + 32, x + 20, y + 52, x + 20, y + 70), stroke=PP, stroke_width=5, stroke_linecap='round')]
            rects.append(g(rr, k=kf((0, dict(o=0, s=.5)), (t['m1b'] - .05 + (c + r) * .005, dict(o=0, s=.5)), (t['m1b'] - .02 + (c + r) * .005, 'b', dict(o=1, s=1)), (off, dict(o=1, s=1)), (off + .02, 'n', dict(o=0, s=.9))), c=(x + 65, y + 48)))
    # FUTURE: one clay lamp again; its flame goes out by itself at dusk, the same thread of smoke
    fl2 = g(flame(724, 548, 2.0), k=kf((0, dict(o=0)), (t['m2b'] - .02, dict(o=0)), (t['m2b'], dict(o=1, s=1)), (.84, dict(o=1, s=1)), (.9, 'n', dict(o=0, s=.1))), c=(724, 548))
    smoke2 = path('M724 540 C 700 460 750 400 720 320 C 700 260 744 200 720 90', stroke=I, stroke_width=3, fill='none', data_dr='.89,.95')
    wick2 = g(path('M690 584 q 18 -12 30 -34', stroke=I, stroke_width=9, stroke_linecap='round', fill='none'), k=fade(t['m2b'] - .02))
    # the keeper puts down three things she is carrying, one at a time, and keeps the stylus
    items = [('bag', 150), ('phone', 210), ('book', 270)]
    keep = g(keeper('hold', 'calm', s=.95, anim=[(0, 'hold'), (.74, 'hold'), (.77, 'serve'), (.8, 'hold'), (.83, 'serve'), (.86, 'hold'), (.89, 'serve'), (.92, 'stand')]),
             k=kf((0, dict(o=0, x=-80, y=760)), (t['m2a'] - .02, dict(o=0, x=-80)), (t['m2b'], 'o', dict(o=1, x=120)), (1, dict(x=120))))
    things = []
    for j, (nm, x) in enumerate(items):
        drop = .77 + j * .06
        if nm == 'bag':
            sh = path('M-30 -60 L 30 -60 L 36 0 L -36 0 Z', fill=GC(), stroke=W, stroke_width=1.5) + path('M-16 -60 q 16 -30 32 0', stroke=I, stroke_width=4, fill='none')
        elif nm == 'phone':
            sh = rect(-16, -56, 32, 56, 6, fill=GI(), stroke=W, stroke_width=1.5) + rect(-11, -50, 22, 40, 3, fill=DK)
        else:
            sh = rect(-34, -26, 68, 26, 3, fill=GC(), stroke=W, stroke_width=1.5) + path('M-30 -18 l 60 0 M -30 -10 l 60 0', stroke=PP, stroke_width=2)
        things.append(g(sh, k=kf((0, dict(o=0, x=200, y=560)), (t['m2b'], dict(o=0, x=200, y=560)), (t['m2b'] + .01, dict(o=1)), (drop, dict(x=200, y=560)), (drop + .03, 'b', dict(x=x + 90, y=760)))))
    mk = g(myna('stand', 1.1), k=kf((0, dict(o=0, x=860, y=760)), (.75, dict(o=0)), (.77, dict(o=1)), (.84, dict(o=1)), (.845, dict(o=0))))
    mk2 = g(myna('tuck', 1.1), k=kf((0, dict(o=0, x=860, y=760)), (.84, dict(o=0)), (.845, dict(o=1))))
    out += [g(rects), lamp, then, smoke1, scr, wick2, fl2, smoke2, g(things), keep, mk, mk2]
    return dict(art=''.join(out), tr='zoom', fx=724, fy=520, pu='.92:1:720:90')


# ============================================================ 07 · the row
def banana_pts(x, y, w, h):
    """A banana-leaf serving piece: the narrow tip to the eater's left (screen left), the broad cut end right."""
    def half(u):
        # narrow rounded tip for the first fifth, then the full width, a squared cut end
        return .5 * (.22 + .78 * min(1, (u / .32)) ** .55) if u < .32 else .5
    pts = [(x + w * u, y + h * (.5 - half(u)) + (2 * math.sin(u * 19) if u > .3 else 0)) for u in [i / 30 for i in range(31)]]
    pts += [(x + w * u, y + h * (.5 + half(u)) + (2 * math.sin(u * 23) if u > .3 else 0)) for u in [i / 30 for i in range(30, -1, -1)]]
    # diners sit behind the row facing us, so the tip (to the eater's left) is on the screen's right
    return [(2 * x + w - px, py) for px, py in pts]


def leaf_meal(x, y, w, h):
    """Midrib, veins, rice mound, salt at the top corner."""
    out = [path('M%s %s L %s %s' % (n(x + 6), n(y + h * .34), n(x + w), n(y + h * .34)), stroke=PP, stroke_width=5)]
    out.append(path(''.join('M%s %s l %s %s M %s %s l %s %s' % (n(x + w * u), n(y + h * .34), n(w * .04), n(-h * .26), n(x + w * u), n(y + h * .34), n(w * .05), n(h * .6)) for u in [i / 12 for i in range(2, 12)]), stroke=PP, stroke_width=1.6, opacity='.55'))
    out.append(path('M%s %s C %s %s %s %s %s %s Z' % (n(x + w * .44), n(y + h * .86), n(x + w * .47), n(y + h * .4), n(x + w * .73), n(y + h * .4), n(x + w * .76), n(y + h * .86)), fill=GI(), stroke=W, stroke_width=1.5))
    out.append(path('M%s %s q %s %s %s 0' % (n(x + w * .5), n(y + h * .6), n(w * .1), n(-h * .16), n(w * .2)), stroke=W, stroke_width=2, fill='none'))
    out.append(circle(x + w * .7, y + h * .2, 8, fill=I) + circle(x + w * .7, y + h * .2, 4, fill=A))
    return ''.join(out)


def s07(s):
    out = []
    N = 4
    leaves = []
    for i in range(N):
        x0, y0, w0, h0 = 30 + i * 240, 660, 228, 84
        L0 = banana_pts(x0, y0, w0, h0)
        L1 = rrect_pts(330, 150 + i * 120, 340, 92, 10)
        L2 = banana_pts(-120 + i * 280, 670, 250, 84)
        d = mpath([L0, L0, L1, L1, L2], [0, t['m1a'] + i * .01, t['m1b'], t['m2a'], t['m2b']], k=34, fill=GC(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke')
        meal = g(leaf_meal(x0, y0, w0, h0), k=fade(.1 + i * .01, t['m1a']))
        meal2 = g(leaf_meal(-120 + i * 280, 670, 250, 84), k=fade(t['m2b']))
        blade = g([path('M350 %d l 300 0' % (196 + i * 120), stroke=DK, stroke_width=4), rect(350, 168 + i * 120, 120, 14, 3, fill=DK),
                   circle(600, 176 + i * 120, 9, fill=I), circle(600, 176 + i * 120, 5, fill=A if i == 0 else PP, class_='tick' if i else None),
                   circle(628, 176 + i * 120, 6, fill=PP, k=None)], k=kf((0, dict(o=0)), (t['m1b'] + .02 + i * .015, dict(o=0)), (t['m1b'] + .035 + i * .015, dict(o=1)), (t['m2a'], dict(o=1)), (t['m2a'] + .03, dict(o=0))))
        leaves.append(g([d, meal, blade, meal2], k=pop(.07 + i * .02, .07, 50)))
    rack = g([rect(300, 120, 400, 520, 12, fill='none', stroke=I, stroke_width=8), path('M500 130 L 500 640', stroke=I, stroke_width=10, opacity='.9'), rect(320, 640, 30, 120, 4, fill=I), rect(650, 640, 30, 120, 4, fill=I)],
             k=kf((0, dict(o=0)), (t['m1a'] + .05, dict(o=0)), (t['m1b'], dict(o=1)), (t['m2a'], dict(o=1)), (t['m2a'] + .05, dict(o=0, y=-80))))
    doors = g([rect(300, 120, 200, 520, 8, fill='none', stroke=PP, stroke_width=4), rect(500, 120, 200, 520, 8, fill='none', stroke=PP, stroke_width=4)],
              k=kf((0, dict(o=0)), (t['m1b'], dict(o=0)), (t['m1b'] + .02, dict(o=1)), (t['m2a'], dict(o=1, x=0)), (t['m2a'] + .06, dict(o=0, x=600))))
    # FUTURE: laid flat in a public hall; people sit along it; it runs out of frame both ends
    hall = g([path('M-200 300 L 1200 300', stroke=I, stroke_width=6), path('M-100 300 L -100 760 M 300 300 L 300 760 M 700 300 L 700 760 M 1100 300 L 1100 760', stroke=I, stroke_width=10, opacity='.5')], k=fade(t['m2b']))
    folk = ''.join(at(x, 660, person(w, 'cross', 'smile', s=.56)) for x, w in [(-40, 'man'), (230, 'woman'), (520, 'old'), (800, 'man')])
    people = g(folk, k=kf((0, dict(o=0, y=30)), (t['m2b'] + .02, dict(o=0, y=30)), (t['m2b'] + .06, 'b', dict(o=1, y=0))))
    keep = g(keeper('serve', 'smile', s=.85, hold=ell(0, 0, 26, 14, fill=GC(), stroke=W, stroke_width=1.5), anim=[(0, 'serve'), (.2, 'serve'), (.22, 'walk1'), (.25, 'walk2'), (.28, 'serve'), (.76, 'serve'), (.79, 'walk1'), (.82, 'walk2'), (.86, 'cross')]),
             k=kf((0, dict(o=0, x=60, y=650)), (.06, dict(o=0)), (.1, 'b', dict(o=1, x=60)), (.28, 'i', dict(x=500)), (t['m1a'], dict(o=1)), (t['m1a'] + .03, dict(o=0)), (t['m2b'] + .03, dict(o=0, x=900)), (t['m2b'] + .06, dict(o=1)), (.86, dict(x=1000, y=660))))
    out += [hall, people, rack, g(leaves), doors, keep]
    return dict(art=''.join(out), tr='mat')


# ============================================================ 08 · nothing written in flesh
def small_leaf(x, y, w=110, h=50, lit=False):
    return path(outline(banana_pts(x, y, w, h), 24), fill=GC(), stroke=W, stroke_width=1.5) + path('M%s %s L %s %s' % (n(x + 4), n(y + h / 2), n(x + w), n(y + h / 2)), stroke=PP, stroke_width=2)


def s08(s):
    out = []
    # the long dim row (left) and the short lit row (right), each leaf with its seat number
    left, right = [], []
    for i in range(5):
        x = 20 + i * 92
        nums = g(tag_label(x + 50, 650, str([34, 71, 58, 22, 90][i]), 18), k=hold(t['m1b'], t['m2a'] + .04))
        nxt = g(tag_label(x + 50, 650, 'next', 16), k=fade(t['m2b']))
        left.append(g([small_leaf(x, 690, 84, 40), nums, nxt]))
    for i in range(2):
        x = 640 + i * 130
        nums = g(tag_label(x + 55, 650, str([97, 99][i]), 18), k=hold(t['m1b'], t['m2a'] + .04))
        nxt = g(tag_label(x + 55, 650, 'next', 16), k=fade(t['m2b']))
        right.append(g([small_leaf(x, 690, 110, 50), nums, nxt]))
    Lg = g(left, k=kf((0, dict(x=0)), (t['m2a'] + .06, dict(x=0)), (t['m2b'], 'i', dict(x=60))))
    Rg = g(right, k=kf((0, dict(x=0)), (t['m2a'] + .06, dict(x=0)), (t['m2b'], 'i', dict(x=-150))))
    lamp = g([path('M820 180 L 820 520', stroke=I, stroke_width=8), ell(820, 520, 34, 10, fill=GI()), flame(820, 512, .9), glow(820, 470, 140)], k=kf((0, dict(o=0)), (.08, dict(o=0)), (.12, dict(o=1)), (t['m2a'] + .04, dict(o=1)), (t['m2b'], dict(o=0))))
    # the screen down the middle: cloth, then a printed score sheet, then rolled up
    rod = rect(520, 110, 24, 24, 12, fill=I)
    cloth = [rect(470, 120, 120, 640, 0, fill=GC(), stroke=W, stroke_width=1.5), path('M495 130 L 495 750 M 530 130 L 530 750 M 565 130 L 565 750', stroke=DK, stroke_width=3, opacity='.5')]
    sheet = g([rect(478, 140, 104, 600, 0, fill=PP, stroke=DK, stroke_width=2)] + [text(530, 182 + j * 46, ['SCORE', '87', '92', '61', '79', '98', '55', '83', '90', '72', '66', '94', '88'][j], 22 if j else 18, fill=DK, anchor='middle', fam='mono', bg='wall', weight=600) for j in range(13)],
              k=kf((0, dict(o=0)), (t['m1a'] + .04, dict(o=0)), (t['m1b'], dict(o=1))))
    roll = g(cloth + [sheet], k=kf((0, dict(sy=1)), (t['m2a'], dict(sy=1)), (t['m2b'] - .02, 'i', dict(sy=.03))), c=(530, 120))
    roller = g(rect(462, 0, 136, 34, 17, fill=GCH(), stroke=W, stroke_width=1.5), k=kf((0, dict(o=0, y=740)), (t['m2a'], dict(o=0, y=740)), (t['m2a'] + .005, dict(o=1, y=740)), (t['m2b'] - .02, 'i', dict(y=110)), (t['m2b'], dict(o=1, y=110))))
    bar = path('M400 122 L 660 122', stroke=I, stroke_width=8, stroke_linecap='round')
    # the keeper lays one more leaf at the end; the myna, served first, pushes its leaf to the far end
    keep = g(keeper('serve', 'calm', s=.9, hold=small_leaf(-40, -20, 80, 36)), k=kf((0, dict(o=0, x=1060, y=760)), (t['m2b'], dict(o=0, x=1060)), (t['m2b'] + .03, dict(o=1)), (.8, 'o', dict(x=930)), (1, dict(x=930))))
    extra = g(small_leaf(860, 690, 100, 46), k=fade(.82))
    mleaf = g(small_leaf(-50, -36, 90, 40), k=kf((0, dict(o=0, x=700, y=726)), (.12, dict(o=0)), (.15, dict(o=1)), (.77, dict(x=700)), (.86, 'i', dict(x=40))))
    mk = g(myna('peck', 1.0), k=kf((0, dict(o=0, x=760, y=760)), (.12, dict(o=0)), (.15, 'b', dict(o=1)), (.77, dict(x=760)), (.86, 'i', dict(x=110)), (.9, dict(x=110))))
    out += [shadow(500, 772, 460, 18), lamp, Lg, Rg, bar, roll, roller, rod, extra, mleaf, mk, keep]
    return dict(art=''.join(out), tr='leaf')
