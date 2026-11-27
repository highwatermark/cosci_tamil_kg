"""Scenes 17-24: the breath, the stone, the gloss, body and life, the wrong note, forgetting, the spread, steer."""
import math
import random
from art import *  # noqa: F401,F403
import art as AR
from objects import walk_anim, hand_grip
from objects_b import fade, hold, banana_pts, coin
from objects_c import flat

t = AR.T


# ============================================================ 17 · the breath, and the 64%
def big_hand():
    """A left hand, palm to us, fingers up, the thumb free to count the joints."""
    out = [path('M330 760 L 350 560 C 340 520 350 470 380 450 L 620 450 C 660 470 670 520 660 560 L 680 760 Z', fill=PP, stroke=DK, stroke_width=5)]
    fingers = [(380, 230), (450, 180), (520, 190), (590, 250)]
    for x, top in fingers:
        out.append(rect(x - 30, top, 64, 470 - top, 32, fill=PP, stroke=DK, stroke_width=5))
        for j in (1, 2):
            yy = top + (470 - top) * j / 3
            out.append(path('M%d %d q 22 6 44 0' % (x - 20, yy), stroke=DK, stroke_width=3.5, fill='none'))
    out.append(path('M630 560 C 700 520 760 470 780 420 C 790 400 820 404 816 432 C 800 500 740 580 660 610', fill=PP, stroke=DK, stroke_width=5, stroke_linejoin='round'))
    out.append(path('M350 640 q 150 -40 300 -10', stroke=DK, stroke_width=3, fill='none', opacity='.6'))
    return ''.join(out)


JOINTS = [(x + 2, top + (470 - top) * j / 3) for x, top in [(590, 250), (520, 190), (450, 180), (380, 230)] for j in (1, 2, 3)]


def thumb_tip(t0, t1, reps=1):
    fr = [(0, dict(x=JOINTS[0][0], y=JOINTS[0][1]))]
    fr.append((t0, dict(x=JOINTS[0][0], y=JOINTS[0][1])))
    for i in range(1, len(JOINTS)):
        fr.append((t0 + (t1 - t0) * i / (len(JOINTS) - 1), 'i', dict(x=JOINTS[i][0], y=JOINTS[i][1])))
    return fr


def s17(s):
    beads0 = ellipse_pts(470, 640, 210, 60, 48)
    beads1 = ellipse_pts(520, 395, 42, 14, 48)
    bstring = mpath([beads0, beads0, beads1, beads1], [0, t['m1a'], t['m1b'], t['m2a']], k=36, fill='none', stroke=I, stroke_width=4, vector_effect='non-scaling-stroke')
    beads = g(''.join(circle(470 + 210 * math.cos(a), 640 + 60 * math.sin(a), 16, fill=GC(), stroke=W, stroke_width=1.5) for a in [i * 6.283 / 18 for i in range(18)]), k=kf((0, dict(o=1, s=1)), (t['m1a'], dict(o=1, s=1)), (t['m1b'] - .03, 'i', dict(o=0, s=.25, y=-240))), c=(470, 640))
    ring = g([ell(520, 395, 46, 16, fill='none', stroke=I, stroke_width=14), ell(520, 392, 46, 16, fill='none', stroke=GC(), stroke_width=6), circle(560, 392, 5, fill=A)],
             k=kf((0, dict(o=0)), (t['m1b'] - .03, dict(o=0)), (t['m1b'], dict(o=1)), (t['m2a'] + .02, dict(o=1, x=0, y=0)), (t['m2a'] + .08, 'i', dict(o=1, x=330, y=150)), (1, dict(x=330, y=150))))
    fr = thumb_tip(.08, .3) + [(t['m1a'], dict(x=JOINTS[-1][0], y=JOINTS[-1][1])), (t['m1a'] + .03, 'i', dict(x=790, y=420)), (t['m2b'], dict(x=790, y=420))]
    for i, (x, y) in enumerate(JOINTS):
        fr.append((t['m2b'] + .03 + .2 * i / (len(JOINTS) - 1), 'i', dict(x=x, y=y)))
    thumb = g(circle(0, 0, 26, fill=PP, stroke=DK, stroke_width=5) + path('M-8 -6 q 10 -6 18 2', stroke=DK, stroke_width=3, fill='none'), k=kf(*fr))
    hand = g(big_hand(), k=kf((0, dict(o=0, y=200)), (.04, dict(o=0, y=200)), (.1, 'o', dict(o=1, y=0))))
    # the slow wave: six breaths to the minute, rising on the in-breath, across the whole wall
    wave = ''.join('Q %d %d %d %d' % (x + 50, 140 if (i % 2 == 0) else 260, x + 100, 200) for i, x in enumerate(range(-200, 1200, 100)))
    wv = path('M-200 200 ' + wave, stroke=I, stroke_width=6, fill='none', stroke_linecap='round', data_dr='%s,%s' % (n2(t['m1b'] - .04), n2(t['m2a'] + .04)))
    dial = g([circle(820, 200, 90, fill='none', stroke=I, stroke_width=16, opacity='.35'), path('M820 110 A 90 90 0 1 1 735 230', stroke=I, stroke_width=16, fill='none', stroke_linecap='round'),
              text(820, 210, '64%', 40, fill=I, anchor='middle', fam='disp', bg='wall', weight=800), text(820, 330, 'awakening', 24, fill=I, anchor='middle', fam='mono', bg='wall')],
             k=kf((0, dict(o=0, s=.2)), (t['m2a'] - .01, dict(o=0, s=.2)), (t['m2a'] + .03, 'b', dict(o=1, s=1)), (t['m2b'], dict(o=1, s=1)), (t['m2b'] + .03, dict(o=0, s=.4))), c=(820, 200))
    wave_g = g(wv, k=kf((0, dict(o=1)), (t['m2b'], dict(o=1)), (t['m2b'] + .03, dict(o=.0))))
    thread = g(path('M-100 200 L 1100 200', stroke=I, stroke_width=4), k=fade(t['m2b']))
    sill = g([rect(700, 120, 300, 440, 6, fill='none', stroke=I, stroke_width=10), path('M850 120 L 850 560 M 700 340 L 1000 340', stroke=I, stroke_width=6), rect(680, 556, 340, 30, 4, fill=GI(), stroke=W, stroke_width=1.5)], k=fade(t['m2a']))
    cong = g(bubble(560, 420, 330, 80, 'well done, windowsill!\n64% → 71%', 22, tail='br'), k=hold(.82, .96, .01))
    out = [sill, wave_g, thread, dial, hand, bstring, beads, ring, thumb, cong]
    return dict(art=''.join(out), tr='zoom', fx=520, fy=395)


# ============================================================ 18 · the stone that speaks
STONE = [(470, 380), (520, 372), (560, 400), (576, 480), (590, 600), (600, 740), (440, 744), (420, 620), (430, 500), (444, 420)]
SPEAKER = [(450, 520), (550, 520), (566, 530), (570, 600), (572, 700), (560, 744), (440, 744), (428, 700), (430, 600), (434, 530)]


def s18(s):
    st = mpath([STONE, STONE, SPEAKER, SPEAKER], [0, t['m1a'], t['m1b'], 1], k=40, fill=GC(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke', class_='grain')
    flowers = g(''.join(circle(x, y, 14, fill=I) + circle(x, y, 6, fill=PP) for x, y in ((470, 372), (500, 362), (530, 368), (556, 384))), k=kf((0, dict(o=0, y=-30)), (.08, dict(o=0, y=-30)), (.12, 'b', dict(o=1, y=0)), (t['m1a'], dict(o=1)), (t['m1a'] + .04, dict(o=0))))
    ring = g([ell(500, 522, 54, 10, fill=A, stroke=I, stroke_width=4), path(''.join('M%d %d q 30 -40 0 -80' % (600 + i * 30, 520 - i * 4) for i in range(3)), stroke=I, stroke_width=5, fill='none', class_='tw')],
             k=kf((0, dict(o=0)), (t['m1b'] - .02, dict(o=0)), (t['m1b'], dict(o=1))))
    pot = path('M660 744 C 620 740 610 670 640 650 L 650 630 L 710 630 L 720 650 C 750 670 740 740 700 744 Z', fill=GI(), stroke=W, stroke_width=1.5) + path('M780 744 L 760 600 M 760 600 q -14 -24 6 -36 q 20 10 -6 36', stroke=I, stroke_width=8, fill='none', stroke_linecap='round')
    potg = g(pot, k=kf((0, dict(o=0)), (.08, dict(o=0)), (.12, dict(o=1)), (t['m1a'], dict(o=1)), (t['m1a'] + .04, dict(o=0))))
    # the queue, laying flowers on it and waiting to be told what matters
    queue = g(''.join(at(700 + j * 110, 760, person(['woman', 'man', 'old'][j], 'hold', 'calm', s=.72, flip=True, hold=circle(0, 0, 12, fill=I) + circle(0, 0, 5, fill=PP))) for j in range(3)),
              k=kf((0, dict(o=0, x=200)), (t['m1b'] - .02, dict(o=0, x=200)), (t['m1b'] + .03, 'o', dict(o=1, x=0)), (t['m2a'], dict(o=1)), (t['m2a'] + .04, dict(o=0))))
    # FUTURE: up on the kitchen shelf between the grinding stone and the pot
    shelf = g([rect(150, 400, 720, 26, 4, fill=GI(), stroke=W, stroke_width=1.5), path('M200 426 L 230 470 M 820 426 L 790 470', stroke=I, stroke_width=8),
               rect(200, 360, 170, 40, 6, fill=GC(), stroke=W, stroke_width=1.5), rect(220, 330, 130, 24, 12, fill=GC(), stroke=W, stroke_width=1.5),
               at(-30, -320, pot)], k=fade(t['m2a']))
    lift = g([st, ring], k=kf((0, dict(x=0, y=0, s=1)), (t['m2a'], dict(x=0, y=0, s=1)), (t['m2b'], 'i', dict(x=0, y=-344, s=.75))), c=(500, 744))
    garland = g(path('M450 530 C 450 600 550 600 550 530', stroke=I, stroke_width=10, fill='none', stroke_dasharray='2 12', stroke_linecap='round'),
                k=kf((0, dict(o=0)), (t['m1b'] + .02, dict(o=0)), (t['m1b'] + .04, dict(o=1, x=0, y=0)), (.78, dict(x=0, y=-344)), (.84, 'i', dict(x=300, y=-60)), (1, dict(x=300, y=-60))))
    old = g(person('old', 'stand', 'smile', s=.85, flip=True), k=kf((0, dict(o=0, x=800, y=760)), (t['m2b'], dict(o=0)), (t['m2b'] + .03, dict(o=1))))
    keep = g(keeper('reach', 'smile', s=.85), k=kf((0, dict(o=0, x=200, y=760)), (.06, dict(o=0)), (.1, dict(o=1)), (1, dict(o=1))))
    no = g(bubble(560, 120, 330, 70, 'That is kind, and no.', 26, tail='bl'), k=hold(.86, 1.1, .01))
    flower = g(circle(0, 0, 14, fill=I) + circle(0, 0, 6, fill=PP), k=kf((0, dict(o=0, x=900, y=300)), (.84, dict(o=0)), (.86, dict(o=1, x=640, y=360)), (.95, dict(x=640, y=360)), (.98, dict(o=0))))
    out = [shadow(500, 772, 300, 16), shelf, potg, lift, flowers, queue, garland, old, keep, flower, no]
    return dict(art=''.join(out), tr='mat')


# ============================================================ 19 · the gloss, and the twin
def seal(x, y, r=46):
    return circle(x, y, r + 6, fill=I) + circle(x, y, r, fill=A) + text(x, y + 7, 'VERIFIED', 15, fill=PP, anchor='middle', fam='mono', bg='acc', weight=600)


def s19(s):
    LEAF = rrect_pts(70, 300, 860, 150, 75)
    DOC = rrect_pts(280, 120, 420, 560, 12)
    d = mpath([LEAF, LEAF, DOC, DOC], [0, t['m1a'], t['m1b'], 1], k=48, fill=GC(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke', class_='paper')
    d = g(d, k=kf((0, dict(o=1)), (t['m2a'] + .02, dict(o=1)), (t['m2a'] + .05, dict(o=0))))
    verse = g([scribble(160, 330, 680, 46, 1, seed=11, sw=7, lmin=30, lmax=60), scribble(160, 376, 680, 60, 4, seed=12, sw=2, lmin=6, lmax=14), circle(330, 375, 9, fill=W), circle(670, 375, 9, fill=W)],
              k=kf((0, dict(o=0)), (.08, dict(o=0)), (.12, dict(o=1)), (t['m1a'], dict(o=1)), (t['m1a'] + .03, dict(o=0))))
    doc = g([scribble(310, 330, 260, 40, 1, seed=13, sw=7, lmin=30, lmax=60), scribble(310, 380, 260, 260, 10, seed=14, sw=3, lmin=10, lmax=30)]
            + [rect(600, 170 + j * 110, 80, 80, 8, fill=GI(), stroke=W, stroke_width=1.5) for j in range(4)],
            k=kf((0, dict(o=0)), (t['m1b'] - .03, dict(o=0)), (t['m1b'], dict(o=1)), (t['m2a'] + .02, dict(o=1)), (t['m2a'] + .05, dict(o=0))))
    pages = g(''.join(rect(220 - j * 70, 160 + j * 30, 300, 400, 10, fill=GC(), stroke=W, stroke_width=1.5) for j in range(3)), k=kf((0, dict(o=0)), (t['m1b'] + .01, dict(o=0)), (t['m1b'] + .03, dict(o=1)), (t['m2a'], dict(o=1)), (t['m2a'] + .04, dict(o=0))))
    seals = []
    spots = [(490, 420, t['m1b'] - .01), (130, 300, t['m1b'] + .02), (60, 360, t['m1b'] + .035), (-10, 420, t['m1b'] + .05), (860, 600, t['m1b'] + .065)]
    for x, y, t0 in spots:
        seals.append(g(seal(0, 0), k=kf((0, dict(o=0, x=x, y=y - 400, r=-30)), (t0 - .02, dict(o=0, x=x, y=y - 400)), (t0, 'n', dict(o=1, x=x, y=y, r=0)), (t['m2a'], dict(x=x, y=y, r=0)), (t['m2a'] + .06, 'n', dict(x=x + 60, y=y + 700, r=80)))))
    # FUTURE: every claim beside its grey twin; seventeen in three hundred stand taller
    rnd = random.Random(17)
    tall = set(rnd.sample(range(300), 17))
    bars = []
    for i in range(300):
        cx, cy = 200 + (i % 25) * 26, 300 + (i // 25) * 36
        hgt = 30 if i in tall else rnd.uniform(8, 16)
        bars.append('M%d %d l 0 %s' % (cx, cy, n(-hgt)))
    twins = ''.join('M%d %d l 0 %s' % (200 + (i % 25) * 26 + 8, 300 + (i // 25) * 36, n(-10)) for i in range(300))
    grid = g([path(''.join(bars), stroke=I, stroke_width=7), path(twins, stroke=GC(), stroke_width=5, opacity='1'), text(200, 760 - 10, '17 of 300 stand taller than their twins · no random control did', 22, fill=I, fam='mono', bg='floor')],
             k=kf((0, dict(o=0, sy=0)), (t['m2a'] + .04, dict(o=0, sy=0)), (t['m2b'], 'o', dict(o=1, sy=1))), c=(500, 700))
    keep = g(keeper('point', 'focus', s=.85), k=kf((0, dict(o=0, x=110, y=760)), (.06, dict(o=0)), (.1, dict(o=1))))
    circ = g(ell(430, 450, 140, 34, fill='none', stroke=A, stroke_width=0) + ell(430, 450, 150, 36, fill='none', stroke=I, stroke_width=5), k=hold(t['m1b'] + .1, t['m2a'] + .04))
    mk = g([myna('sing', 1.05), g(seal(10, -60, 30), k=kf((0, dict(o=0)), (t['m1b'] + .06, dict(o=0)), (t['m1b'] + .065, dict(o=1)), (t['m2a'], dict(o=1)), (t['m2a'] + .03, dict(o=0))))],
           k=kf((0, dict(o=0, x=860, y=760)), (.08, dict(o=0)), (.11, 'b', dict(o=1))))
    say1 = g(bubble(560, 520, 320, 70, 'kural 423, word-perfect', 22), k=hold(.76, .84, .01))
    say2 = g(bubble(560, 520, 320, 70, 'the moon is a dosa.', 26), k=hold(.85, 1.1, .01))
    out = [pages, d, verse, doc, circ, grid, g(seals), keep, mk, say1, say2]
    return dict(art=''.join(out), tr='leaf')


# ============================================================ 20 · body and life
def letter_join(x, y, size, t0, t1, even=False):
    """ந் and இ come together into நி. The dot over ந் is drawn separately so it can hop off."""
    na = tag('text', 'ந', x=x, y=y, font_size=size, fill=I, data_bg='wall', style='font-family:var(--f-ta);font-weight:600', lang='ta')
    i_ = tag('text', 'இ', x=x + size * 1.3, y=y, font_size=size, fill=I, data_bg='wall', style='font-family:var(--f-ta);font-weight:600', lang='ta')
    ni = tag('text', 'நி', x=x + size * .3, y=y, font_size=size, fill=I, data_bg='wall', style='font-family:var(--f-ta);font-weight:600', lang='ta')
    a = g(na, k=kf((0, dict(o=0, x=-60)), (t0, dict(o=0, x=-60)), (t0 + .03, 'b', dict(o=1, x=0)), (t1, dict(o=1, x=0)), (t1 + .03, 'i', dict(o=0, x=size * .3))))
    b = g(i_, k=kf((0, dict(o=0, x=60)), (t0 + .02, dict(o=0, x=60)), (t0 + .05, 'b', dict(o=1, x=0)), (t1, dict(o=1, x=0)), (t1 + .03, 'i', dict(o=0, x=-size))))
    c = g(ni, k=kf((0, dict(o=0, s=.6)), (t1 + .02, dict(o=0, s=.6)), (t1 + .05, 'b' if not even else 'l', dict(o=1, s=1))), c=(x + size * .8, y - size * .4))
    return a + b + c


def s20(s):
    # THEN: the bard at the patron's gate
    gate = g([rect(560, 140, 40, 620, 4, fill=GI(), stroke=W, stroke_width=1.5), rect(900, 140, 40, 620, 4, fill=GI(), stroke=W, stroke_width=1.5), rect(530, 110, 440, 44, 6, fill=GC(), stroke=W, stroke_width=1.5),
              path('M620 200 L 880 200 M 620 260 L 880 260', stroke=I, stroke_width=3, opacity='.5')], k=kf((0, dict(o=0)), (.05, dict(o=0)), (.09, dict(o=1)), (t['m1a'], dict(o=1)), (t['m1a'] + .04, dict(o=0))))
    bard = g(person('bard', 'pointup', 'wide', s=1.25), k=kf((0, dict(o=0, x=340, y=760, s=1)), (.04, dict(o=0)), (.08, 'b', dict(o=1)), (t['m1a'], dict(s=1, x=340, y=760)), (t['m1a'] + .08, 'n', dict(o=0, s=4.5, x=280, y=1900))), c=(0, -300))
    letters = g(letter_join(250, 230, 110, .12, .2), k=kf((0, dict(o=1)), (t['m1a'], dict(o=1)), (t['m1a'] + .03, dict(o=0))))
    # NOW: the open mouth is a microphone grille; FUTURE: a speaker's face
    MOUTH = ellipse_pts(500, 380, 60, 34, 48)
    MIC = ellipse_pts(500, 330, 190, 190, 48)
    SPK = ellipse_pts(500, 460, 250, 250, 48)
    m = mpath([MOUTH, MOUTH, MIC, MIC, SPK], [0, t['m1a'] + .04, t['m1b'], t['m2a'], t['m2b']], k=40, fill=GI(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke')
    mesh = g(path(''.join('M%d %d l 0 %d' % (x, 330 - int(math.sqrt(max(0, 170 ** 2 - (x - 500) ** 2))), 2 * int(math.sqrt(max(0, 170 ** 2 - (x - 500) ** 2)))) for x in range(340, 661, 20)) + ''.join('M%d %d l %d 0' % (500 - int(math.sqrt(max(0, 170 ** 2 - (y - 330) ** 2))), y, 2 * int(math.sqrt(max(0, 170 ** 2 - (y - 330) ** 2)))) for y in range(170, 491, 20)), stroke=W, stroke_width=3),
             k=hold(t['m1b'], t['m2a'] + .02))
    stand = g(path('M500 520 L 500 760 M 420 760 L 580 760', stroke=I, stroke_width=14), k=hold(t['m1b'] - .02, t['m2a'] + .02))
    rings = g(''.join(circle(500, 460, r, fill='none', stroke=W, stroke_width=5) for r in (210, 160, 110)) + circle(500, 460, 60, fill=GC(), stroke=W, stroke_width=1.5) + circle(500, 460, 22, fill=A), k=fade(t['m2b'] - .02))
    letters2 = g(letter_join(370, 160, 80, t['m2b'] + .02, t['m2b'] + .08, even=True), k=fade(t['m2b']))
    # the keeper mouths the consonant alone, then adds the vowel
    keep = g(keeper('stand', 'calm', s=.78), k=kf((0, dict(o=0, x=860, y=760)), (t['m2a'], dict(o=0)), (t['m2a'] + .04, dict(o=1))))
    keep2 = g(keeper('stand', 'talk', s=.78), k=kf((0, dict(o=0, x=860, y=760)), (.82, dict(o=0)), (.821, dict(o=1))))
    # the dot over ந் hops off; the myna tries to eat it (drawn as large as the myna's head)
    dot = g(circle(0, 0, 13, fill=I), k=kf((0, dict(o=0, x=318, y=118)), (.11, dict(o=0)), (.13, dict(o=1, x=318, y=118)), (.2, dict(x=318, y=118)), (.24, 'o', dict(x=600, y=40)), (.28, 'n', dict(x=760, y=700)), (.31, dict(x=820, y=740)), (t['m1a'] + .03, dict(o=1)), (t['m1a'] + .05, dict(o=0))))
    mk = g(myna('peck', 1.1), k=kf((0, dict(o=0, x=700, y=760)), (.2, dict(o=0)), (.23, dict(o=1)), (.3, 'i', dict(x=760)), (t['m1a'] + .03, dict(o=1)), (t['m1a'] + .05, dict(o=0))))
    out = [gate, rings, m, mesh, stand, letters, bard, letters2, keep, keep2, dot, mk]
    return dict(art=''.join(out), tr='zoom', fx=500, fy=400, pu='.12:.2:318:118')


# ============================================================ 21 · the wrong note
def s21(s):
    BOX = [(160, 640), (300, 590), (520, 584), (700, 610), (760, 640), (700, 690), (480, 714), (260, 700)]
    box = path(cubic(_c(BOX), True), fill=GC(), stroke=W, stroke_width=1.5, class_='grain')
    NECK0 = [(720, 620), (790, 520), (800, 400), (760, 280), (700, 200)]
    NECK1 = [(160, 520), (300, 520), (440, 520), (580, 520), (720, 520)]
    neck = mpath([NECK0, NECK0, NECK1, NECK1, NECK0], [0, t['m1a'], t['m1b'], t['m2a'], t['m2b']], k=12, closed=False, fill='none', stroke=I, stroke_width=22, stroke_linecap='round')
    strings = []
    for j in range(7):
        a = (300 + j * 60, 620)
        nk = [(720, 620), (790, 520), (800, 400), (760, 280), (700, 200)]
        tt = j / 6
        e = (lerp(780, 712, tt), lerp(470, 210, tt))
        S0 = [a, e]
        S1 = [(180 + j * 78, 540), (180 + j * 78, 640)]
        strings.append(mpath([S0, S0, S1, S1, S0], [0, t['m1a'], t['m1b'], t['m2a'], t['m2b']], k=2, closed=False, tension=0, fill='none', stroke=I, stroke_width=4 if j else 4))
    keys = g([rect(150, 520, 560, 140, 10, fill='none', stroke=I, stroke_width=6)] + [rect(186 + j * 78, 540, 30, 60, 4, fill=I) for j in range(6)], k=hold(t['m1b'] - .02, t['m2a'] + .02))
    box_g = g(box, k=kf((0, dict(o=1)), (t['m1a'], dict(o=1)), (t['m1b'], dict(o=.0)), (t['m2a'], dict(o=0)), (t['m2b'], dict(o=1))))
    skin = g(path('M300 600 C 420 596 560 596 660 610', stroke=PP, stroke_width=4, fill='none'), k=kf((0, dict(o=1)), (t['m1a'], dict(o=1)), (t['m1b'], dict(o=0)), (t['m2a'], dict(o=0)), (t['m2b'], dict(o=1))))
    newstr = g(path('M720 620 L 690 220', stroke=A, stroke_width=0) + path('M716 624 L 686 214', stroke=I, stroke_width=3, stroke_dasharray='14 4') + circle(700, 420, 9, fill=A), k=fade(t['m2b']))
    # trophies, each with a power cable
    trophies = g(''.join(path('M%d 250 l 50 0 l -8 50 l -34 0 z M %d 300 l 0 30 M %d 330 l 30 0' % (x, x + 25, x + 10), stroke=I, stroke_width=5, fill=GC()) + path('M%d 330 C %d 380 %d 380 %d 420' % (x + 25, x + 25, x + 60, x + 60), stroke=I, stroke_width=3, fill='none') for x in (180, 300, 420, 540, 660)) + rect(150, 336, 620, 14, 3, fill=I),
                 k=kf((0, dict(o=0, y=-40)), (t['m1b'], dict(o=0, y=-40)), (t['m1b'] + .03, 'b', dict(o=1, y=0)), (t['m2a'] + .02, dict(o=1)), (t['m2a'] + .05, dict(o=0))))
    # FUTURE: the room: ten stools, no recording light, a bard tagged with who paid for the song
    stools = ''.join(rect(80 + j * 90, 740 - (j % 2) * 30, 50, 12, 3, fill=GI()) + path('M%d %d l -6 30 m 44 -30 l 6 30' % (84 + j * 90, 752 - (j % 2) * 30), stroke=I, stroke_width=5) for j in range(10))
    lean = g(''.join(at(120 + j * 180, 730, person(['woman', 'man', 'old', 'man', 'woman'][j], 'listen', 'wide', s=.42)) for j in range(5)), k=kf((0, dict(o=0, y=40)), (t['m2b'], dict(o=0, y=40)), (t['m2b'] + .03, 'b', dict(o=1, y=0))))
    room = g([stools, circle(900, 120, 22, fill=I), path('M880 100 l 40 40 M 920 100 l -40 40', stroke=PP, stroke_width=5), text(900, 176, 'no recording', 18, fill=I, anchor='middle', fam='mono', bg='wall'),
              tag_label(240, 140, 'paid for by: the weavers of Uraiyur', 18, fam='mono')], k=fade(t['m2b'] - .01))
    wrongkey = g([rect(160, 690, 240, 50, 8, fill=GI(), stroke=W, stroke_width=1.5), text(280, 724, 'wrong note', 22, fill=DK, anchor='middle', fam='mono', bg='ink', weight=600)], k=fade(t['m2b'] + .03))
    keep = g(keeper('reach', 'focus', s=.82), k=kf((0, dict(o=0, x=860, y=760)), (.05, dict(o=0)), (.09, dict(o=1)), (t['m1a'], dict(x=860)), (1, dict(x=860))))
    oops = g(bubble(620, 280, 140, 60, 'oops', 24, tail='br'), k=hold(.8, .86, .01))
    out = [shadow(460, 772, 360, 16), trophies, room, box_g, skin, neck, g(strings), keys, newstr, lean, wrongkey, keep, oops]
    return dict(art=''.join(out), tr='fade')


def _c(pts):
    return AR.resample(pts, 40)


# ============================================================ 22 · forgetting on purpose
def s22(s):
    # THEN: the water bowl in its larger vessel; it fills, tilts and sinks; an attendant (the myna) strikes the gong, late
    vessel = g([path('M200 420 C 200 740 800 740 800 420 Z', fill=GI(), stroke=W, stroke_width=1.5), ell(500, 420, 300, 40, fill=W, stroke=I, stroke_width=6),
                path('M260 424 q 50 -8 100 0 M 640 418 q 50 -8 100 0', stroke=I, stroke_width=3, fill='none')], k=kf((0, dict(o=0)), (.04, dict(o=0)), (.08, dict(o=1)), (t['m1a'], dict(o=1)), (t['m1a'] + .04, dict(o=0))))
    BOWL = [(400, 400), (600, 400), (580, 440), (540, 460), (460, 460), (420, 440)]
    DIAL = ellipse_pts(500, 400, 170, 170, 40)
    bowl = mpath([_c(BOWL), _c(BOWL), DIAL, DIAL], [0, t['m1a'], t['m1b'], 1], k=40, fill=GC(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke')
    pin = g(path('M500 460 l 0 40', stroke=I, stroke_width=3, stroke_dasharray='4 6'), k=hold(.1, .22))
    bowl_g = g([bowl, pin], k=kf((0, dict(r=0, y=0, o=1)), (.1, dict(r=0, y=0)), (.22, 'n', dict(r=-14, y=30)), (.27, 'n', dict(r=-30, y=150)), (.3, dict(r=-30, y=150, o=1)), (t['m1a'], dict(r=0, y=0)), (t['m2a'] + .02, dict(r=0, y=0, o=1)), (t['m2a'] + .05, dict(o=0))), c=(500, 430))
    gong = g([path('M860 120 L 860 300', stroke=I, stroke_width=4), circle(860, 340, 54, fill=GIH(), stroke=W, stroke_width=1.5), circle(860, 340, 20, fill=GC())], k=kf((0, dict(o=1)), (t['m1a'], dict(o=1)), (t['m1a'] + .04, dict(o=0))))
    strike = g(text(780, 250, 'bong', 30, fill=I, fam='hand', bg='wall', weight=600), k=hold(.3, .32, .005))
    mk = g(myna('peck', 1.0), k=kf((0, dict(o=0, x=800, y=760)), (.06, dict(o=0)), (.09, dict(o=1)), (1, dict(o=1))))
    late = g(text(860, 640, '(late, again, by exactly as much)', 20, fill=I, anchor='middle', fam='mono', bg='floor'), k=hold(.3, .5))
    # NOW: the watch; the counter runs to 9,192,631,770 and starts again; then stops resetting
    watch = g([rect(440, 120, 120, 120, 20, fill=GI()), rect(440, 560, 120, 140, 20, fill=GI()), circle(500, 400, 140, fill=W, stroke=I, stroke_width=8),
               tag('text', '0', x=500, y=414, font_size=28, fill=I, text_anchor='middle', data_bg='wall', style='font-family:var(--f-md);font-weight:600', data_n='%s,%s,0,9192631770,c' % (n2(t['m1b']), n2(t['m2a']))),
               text(500, 460, 'caesium periods', 18, fill=I, anchor='middle', fam='mono', bg='wall'),
               path('M500 300 L 500 400 L 570 440', stroke=I, stroke_width=6, stroke_linecap='round', fill='none')],
              k=kf((0, dict(o=0)), (t['m1b'] - .03, dict(o=0)), (t['m1b'], dict(o=1)), (t['m2a'] + .02, dict(o=1)), (t['m2a'] + .05, dict(o=0))))
    # paper tails behind every figure, everything they said at fourteen, growing as they walk
    tails = []
    for j, (x0, y0) in enumerate(((140, 760), (320, 760))):
        tails.append(g([path('M%d %d L %d %d' % (x0 - 1200, y0 - 120, x0 - 10, y0 - 120), stroke=GC(), stroke_width=40), path(''.join('M%d %d l 30 0' % (x, y0 - 126) for x in range(x0 - 1180, x0 - 20, 46)), stroke=I, stroke_width=3),
                        g(person(['man', 'woman'][j], 'walk1', 'sad', s=.6), transform='translate(%d %d)' % (x0, y0))],
                       k=kf((0, dict(o=0, x=-300)), (t['m1b'] + .02, dict(o=0, x=-300)), (t['m1b'] + .04, dict(o=1, x=-300)), (t['m2a'] + .05, 'l', dict(x=200)), (t['m2a'] + .08, dict(o=0, x=260)))))
    # FUTURE: a ring of radio dishes pointed at a dozen pulsars; a rice-flour kolam; ants
    dishes = []
    for j in range(8):
        a = math.radians(-160 + j * 20)
        x, y = 500 + 300 * math.cos(a), 600 + 260 * math.sin(a) * .35
        dishes.append(at(x, y, path('M-30 0 Q 0 30 30 0 Z', fill=GC(), stroke=W, stroke_width=1.5) + path('M0 10 L 0 50 M -16 50 L 16 50', stroke=I, stroke_width=5) + path('M0 12 L 0 -24', stroke=I, stroke_width=2), s=.9))
    pulsars = ''.join(circle(120 + j * 70, 120 + (j % 3) * 40, 6, fill=I, class_='tw') for j in range(12))
    fut = g([g(dishes), pulsars, text(500, 90, 'nobody owns this clock', 22, fill=I, anchor='middle', fam='mono', bg='wall')], k=kf((0, dict(o=0, s=.4)), (t['m2a'] + .04, dict(o=0, s=.4)), (t['m2b'], 'o', dict(o=1, s=1))), c=(500, 520))
    kol = path('M300 840 C 300 780 380 780 380 840 C 380 900 460 900 460 840 C 460 780 540 780 540 840 C 540 900 620 900 620 840 C 620 780 700 780 700 840 C 700 900 620 900 620 840', stroke=I, stroke_width=6, fill='none', data_dr='%s,%s' % (n2(t['m2b']), n2(.82)))
    kdots = ''.join(circle(x, 840, 7, fill=I) for x in (340, 420, 500, 580, 660))
    ants = g(''.join(circle(260 + j * 24, 900 - (j % 2) * 8, 4, fill=I) for j in range(6)), k=kf((0, dict(o=0, x=0)), (.86, dict(o=0)), (.88, dict(o=1)), (1, 'l', dict(x=-200))))
    kolg = g([kol, g(kdots, k=fade(t['m2b']))], k=kf((0, dict(o=1)), (.9, dict(o=1)), (.98, dict(o=.4))))
    keep = g(keeper('walk1', 'calm', s=.8, anim=walk_anim(.84, .98, 6, 'serve', 'walk2')), k=kf((0, dict(o=0, x=200, y=760)), (t['m2b'], dict(o=0)), (t['m2b'] + .03, dict(o=1)), (.84, dict(x=200)), (.98, 'l', dict(x=980))))
    out = [vessel, bowl_g, gong, strike, watch, g(tails), fut, kolg, ants, keep, mk, late]
    return dict(art=''.join(out), tr='mat', pu='%s:%s:340:840' % (n2(t['m2b']), '.86'))


# ============================================================ 23 · the spread
ROWS = [('அறம்', 'letting a level beam stand in for a fair hand', 'signing what we weigh'),
        ('பொருள்', 'measuring a people by what they hoard', 'counting who gets fed'),
        ('இன்பம்', 'sending words with no hand in them', 'sending the crossings-out'),
        ('வீடு', 'leaving every light on', 'letting the lamp go out'),
        ('சமூகம்', 'seating people by what is written in them', 'laying the next leaf'),
        ('இயற்கை', 'calling the land a resource', 'calling its creatures by name'),
        ('உடல்', 'reaching for the cure before the cause', 'staying by the bed, and asking first'),
        ('உள்ளம்', 'asking only whether the machine is awake', 'starting at the first rung'),
        ('யோகம்', 'scoring stillness', 'the slow breath, for our own reasons'),
        ('இறை', 'asking the stone what to revere', 'deciding it ourselves, together'),
        ('அறிவாய்வு', 'believing the most fluent voice', 'testing by the means of knowing'),
        ('புலமை', 'holding contests against the machines', 'singing where a wrong note can be heard'),
        ('காலம்', 'remembering everything about everyone', 'recopying the file, and fixing it')]


def thumb(i, side):
    """Tiny THEN (left) and FUTURE (right) thumbnails of each category's object."""
    if side == 0:
        d = ['M-10 8 a 10 6 0 1 0 20 0 a 10 6 0 1 0 -20 0', 'M-8 -6 q 8 -12 16 0 l 2 14 l -20 0 z', 'M-14 0 q 14 -12 28 0 q -14 12 -28 0', 'M-12 4 q 12 8 24 0 l -6 -6 l -12 0 z m 12 -8 q -4 -6 0 -10 q 4 4 0 10',
             'M-14 -4 l 28 0 l -4 8 l -20 0 z m -4 10 l 36 0', 'M-14 8 l 8 -16 l 6 10 l 6 -8 l 8 14 z', 'M-12 -10 l 0 16 m 8 -18 l 0 18 m 8 -18 l 0 18', 'M-8 -12 l 0 24 m 16 -24 l 0 24 m -16 -16 l 16 0 m -16 8 l 16 0',
             'M-8 -12 l 0 20 m 6 -22 l 0 22 m 6 -20 l 0 20 m -16 6 q 8 6 16 0', 'M-6 10 l -2 -16 q 8 -6 16 0 l -2 16 z', 'M-14 -4 l 28 0 m -28 6 l 20 0 m -20 6 l 24 0', 'M-12 6 q 12 4 24 0 m -2 0 q 6 -14 -4 -20', 'M-12 -4 q 12 12 24 0 z'][i]
    else:
        d = ['M-12 -8 l 24 0 l 0 16 l -24 0 z m 4 10 a 3 3 0 1 0 1 0', 'M-14 0 q 14 -10 28 0 l 0 6 l -28 0 z', 'M-10 -12 l 20 0 l 0 24 l -20 0 z m 4 6 l 10 0', 'M-12 4 q 12 8 24 0 l -6 -6 l -12 0 z',
             'M-16 0 l 32 0 m -30 4 l 28 0', 'M-14 8 l 6 -16 l 6 10 l 6 -8 l 8 14 l 4 0 l 0 -18', 'M-12 4 l 24 0 m -20 -8 l 0 8 m 16 -8 l 0 8 m -14 -6 l 12 0', 'M-8 12 l 0 -24 m 16 24 l 0 -24 m -16 22 l 16 0',
             'M-8 -12 l 0 20 m 6 -22 l 0 22 m 6 -20 l 0 20', 'M-14 2 l 28 0 m -24 -10 l 8 0 l 0 10 m 6 -10 l 8 0 l 0 10', 'M-12 6 l 0 -10 m 6 10 l 0 -16 m 8 16 l 0 -6 m 6 6 l 0 -12', 'M-12 6 q 12 4 24 0 m -2 0 q 6 -14 -4 -20 m 8 -2 l 0 4', 'M-12 0 q 6 -10 12 0 q 6 10 12 0'][i]
    return path(d, stroke=DK, stroke_width=2.5, fill='none', stroke_linecap='round')


def s23(s):
    # THEN: the bundle from scene 01, untied and fanned; NOW: a ruled two-page spread
    fan = []
    for j in range(7):
        a = -36 + j * 12
        fan.append(g(rect(-30, -400, 60, 400, 30, fill=GC(), stroke=W, stroke_width=1.5) + circle(0, -320, 6, fill=W) + circle(0, -80, 6, fill=W),
                     transform='translate(500 700)', k=kf((0, dict(r=0, o=0)), (.05 + j * .01, dict(r=0, o=0)), (.08 + j * .01, dict(o=1)), (.16 + j * .01, 'b', dict(r=a)), (t['m1a'], dict(r=a)), (t['m1b'] - .04, 'i', dict(r=0, o=0))), c=(0, 0)))
    book = g([rect(70, 110, 860, 640, 14, fill=GI(), stroke=W, stroke_width=1.5), path('M500 110 L 500 750', stroke=DK, stroke_width=5)] +
             [path('M90 %d L 480 %d M 520 %d L 910 %d' % (y, y, y, y), stroke=DK, stroke_width=1.2, opacity='.35') for y in range(170, 740, 44)],
             k=kf((0, dict(o=0, sy=.05)), (t['m1a'] + .02, dict(o=0, sy=.05)), (t['m1b'], 'o', dict(o=1, sy=1))), c=(500, 430))
    # FUTURE: the pairs, one per beat, in three inks; the newest pair brightest; the spread scrolls upward
    rows = []
    beat0, beat1 = t['m1b'] + .02, .9
    for i, (cat, left, right) in enumerate(ROWS):
        y = 158 + i * 40
        tb = beat0 + (beat1 - beat0) * i / 13
        fam = ['hand', 'serif', 'hand'][i % 3]
        r = [text(92, y + 8, left, 15 if fam == 'serif' else 18, fill=DK, fam=fam, bg='ink'), path('M90 %d l %d 0' % (y + 2, min(380, len(left) * 7.6)), stroke=DK, stroke_width=2.5, data_dr='%s,%s' % (n2(tb + .01), n2(tb + .02))),
             path('M518 %d l %d 0' % (y + 11, min(370, len(right) * 7.8)), stroke=GC(), stroke_width=9, stroke_linecap='round', data_dr='%s,%s' % (n2(tb + .01), n2(tb + .025))),
             text(522, y + 6, right, 15 if fam == 'serif' else 18, fill=DK, fam=fam, bg='ink'),
             g(thumb(i, 0), transform='translate(470 %d)' % (y - 2)), g(thumb(i, 1), transform='translate(890 %d)' % (y - 2))]
        rows.append(g(r, k=kf((0, dict(o=0, x=-10)), (tb, dict(o=0, x=-10)), (tb + .012, 'o', dict(o=1, x=0)))))
    gag = g([text(92, 712, 'arguing with the myna', 18, fill=DK, fam='hand', bg='ink'), path('M90 706 l 170 0', stroke=DK, stroke_width=2.5, data_dr='.9,.92,.95,.97')], k=fade(.88))
    rowsg = g(rows + [gag], k=kf((0, dict(y=0)), (.6, dict(y=0)), (.95, 'i', dict(y=0))))
    spread = g([book, rowsg], k=kf((0, dict(s=1, y=0)), (.6, dict(s=1, y=0)), (.92, 'i', dict(s=1, y=0))), c=(500, 430))
    keep = g(keeper('write', 'focus', s=.7), k=kf((0, dict(o=0, x=-40, y=760)), (.05, dict(o=0)), (.09, dict(o=1)), (t['m1b'], dict(x=-40)), (.9, 'l', dict(x=40))))
    out = [g(fan), spread, keep]
    return dict(art=''.join(out), tr='zoom', fx=500, fy=420)


# ============================================================ 24 · steer
def s24(s):
    # the river crosses the whole frame, the whole scene, and never slows
    river = g([rect(-400, 520, 1800, 240, 0, fill=GC(), stroke=W, stroke_width=1.5)] +
              [g(path(''.join('M%d %d q 30 -10 60 0' % (x, 560 + r * 50) for x in range(-400, 1400, 140)), stroke=PP, stroke_width=4, fill='none'), k=kf((0, dict(x=0)), (1, 'l', dict(x=420 + r * 60)))) for r in range(4)])
    bank = g(path('M820 520 C 900 500 1000 500 1200 520 L 1200 560 L 820 560 Z', fill=GI(), stroke=W, stroke_width=1.5), k=fade(t['m2b']))
    RIM = ellipse_pts(0, 0, 150, 52, 40)
    WHEEL = ellipse_pts(0, 0, 160, 160, 40)
    rim = mpath([RIM, RIM, WHEEL, WHEEL, RIM], [0, t['m1a'], t['m1b'], t['m2a'], t['m2b']], k=40, fill='none', stroke=I, stroke_width=18, vector_effect='non-scaling-stroke')
    basket = g([path('M-150 0 C -140 90 140 90 150 0 Z', fill=I), path(''.join('M%d 0 q %d 60 %d 70' % (x, x * .1, x * .1) for x in range(-130, 140, 26)), stroke=W, stroke_width=3, fill='none'), path('M-150 0 C -140 30 140 30 150 0', stroke=PP, stroke_width=3, fill='none')],
               k=kf((0, dict(o=1)), (t['m1a'], dict(o=1)), (t['m1a'] + .05, dict(o=0)), (t['m2a'] + .06, dict(o=0)), (t['m2b'], dict(o=1))))
    spokes = g(path('M-150 0 L 150 0 M 0 0 L 0 150', stroke=I, stroke_width=16) + circle(0, 0, 34, fill=GC(), stroke=W, stroke_width=1.5), k=hold(t['m1b'] - .02, t['m2a'] + .03))
    boat = g([basket, rim, spokes], k=kf((0, dict(r=0)), (.1, dict(r=0)), (.3, 'l', dict(r=40)), (t['m1a'], dict(r=0)), (t['m1b'], dict(r=0)), (t['m1b'] + .03, dict(r=90)), (t['m2a'], dict(r=200)), (t['m2a'] + .04, dict(r=360)), (1, dict(r=360))), c=(0, 0))
    hands = g(at(500, 380, path('M-120 230 q 40 -20 80 0 M 40 230 q 40 -20 80 0', stroke=PP, stroke_width=26, stroke_linecap='round') + path('M-200 260 L 200 260', stroke=I, stroke_width=6) + text(0, 300, 'route chosen', 20, fill=I, anchor='middle', fam='mono', bg='wall')), k=hold(t['m1b'], t['m2a'] + .02))
    keep = g(keeper('paddle', 'focus', s=.7, hold=path('M0 0 L 0 160 l -10 30 l 20 0 l -10 -30', stroke=I, stroke_width=6, fill=GC())), k=kf((0, dict(o=0, y=-40)), (t['m2b'] - .02, dict(o=0)), (t['m2b'], dict(o=1)), (1, dict(o=1))))
    mk = g(myna('stand', .8), k=kf((0, dict(sx=1, o=1)), (.2, dict(sx=1)), (.24, dict(sx=-1)), (.28, dict(sx=1)), (t['m1a'], dict(o=1)), (t['m1a'] + .03, dict(o=0)), (t['m2b'], dict(o=0)), (t['m2b'] + .02, dict(o=1)), (.9, dict(sx=1)), (.93, dict(sx=-1)), (.96, dict(sx=1))), transform='translate(80 -20)', c=(80, -60))
    stroke_ = g(path('M-60 60 q 30 30 70 10', stroke=I, stroke_width=5, fill='none'), k=hold(.76, .8))
    craft = g([boat, keep, mk, stroke_], k=kf((0, dict(x=340, y=560)), (t['m1a'], dict(x=500, y=560)), (t['m1b'], dict(x=500, y=400)), (t['m2a'], dict(x=500, y=400)), (t['m2b'], dict(x=380, y=600)), (.8, dict(x=420, y=600)), (.96, 'i', dict(x=880, y=540))))
    out = [river, bank, craft, hands]
    return dict(art=''.join(out), tr='mat')
