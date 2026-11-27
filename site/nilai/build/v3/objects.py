"""Objects, one function per object and per stage of its transformation. Art space 1000 x 1000, horizon at GY=760."""
import math
import random
from art import *  # noqa: F401,F403
import art as AR


def walk_anim(t0, t1, steps=4, base='stand', end=None):
    fr = [(0, base), (t0, base)]
    for i in range(steps):
        fr.append((t0 + (t1 - t0) * (i + .5) / steps, 'walk1' if i % 2 == 0 else 'walk2'))
    fr.append((t1, end or base))
    return fr


# ------------------------------------------------------------ 01: palm-leaf book -> phone -> glowing leaf (the ledger strip)
LEAF_N = 6


def _leaf_then(i):
    y = 486 + i * 27
    inset = i * 5
    return rrd(140 + inset, y, 720 - 2 * inset, 40, 20)


PHONE = rrd(362, 168, 276, 548, 44)
LEAF_FUT = rrd(462, 120, 76, 610, 36)


def book_bundle():
    """THEN: the bundle: bottom board, six fanned leaves, the top board propped open, the cord through the holes.
    The leaves themselves morph (see phone_from_bundle); this draws the parts that only belong to the book."""
    t = AR.T
    out = []
    # the writing stand
    stand = _p_stand()
    out.append(g(stand, k=kf((0, dict(o=0, y=30)), (.06, dict(o=0, y=30)), (.12, 'b', dict(o=1, y=0)), (t['m1a'], dict(o=1)), (t['m1a'] + .05, dict(o=0)))))
    # bottom board (morphs to the phone's chin)
    bb0 = rrd(128, 650, 744, 40, 8)
    bb1 = rrd(400, 690, 200, 14, 7)
    bb2 = rrd(470, 712, 60, 10, 5)
    board_b = mpathd([bb0, bb0, bb1, bb1, bb2], [0, t['m1a'], t['m1b'], t['m2a'], t['m2b']], fill=GCH(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke')
    grain_b = g(_grain(140, 660, 720, 22, 5), k=show(.06, t['m1a'] + .02))
    out.append(g([board_b, grain_b], k=kf((0, dict(o=0, y=40)), (.07, dict(o=0, y=40)), (.12, 'b', dict(o=1, y=0)), (t['m2b'], dict(o=1)), (t['m2b'] + .03, dict(o=0)))))
    return ''.join(out)


def _p_stand():
    return ''.join([
        path('M170 690 L 150 760 M 830 690 L 850 760 M 190 690 L 210 760 M 810 690 L 790 760', stroke=I, stroke_width=10, stroke_linecap='round'),
        path('M150 738 L 210 738 M 790 738 L 850 738', stroke=I, stroke_width=6, stroke_linecap='round'),
        shadow(180, 764, 50, 7), shadow(820, 764, 50, 7),
    ])


def _grain(x, y, w, h, k, col=DK):
    rnd = random.Random(int(x * 7 + y))
    out = []
    for i in range(k):
        yy = y + h * (i + .5) / k
        d = 'M%s %s' % (n(x), n(yy))
        xx = x
        while xx < x + w:
            step = rnd.uniform(60, 140)
            d += ' q %s %s %s 0' % (n(step / 2), n(rnd.uniform(-3, 3)), n(min(step, x + w - xx)))
            xx += step
        out.append(path(d, stroke=col, stroke_width=1.6, fill='none', opacity='.55'))
    return ''.join(out)


def phone_from_bundle():
    t = AR.T
    out = []
    # glow behind the FUTURE leaf
    out.append(g(glow(500, 420, 330), k=kf((0, dict(o=0)), (t['m2a'] + .05, dict(o=0)), (t['m2b'], dict(o=1)), (.84, dict(o=1)), (.9, dict(o=0)))))
    leaves = []
    for i in reversed(range(LEAF_N)):
        L0 = _leaf_then(i)
        d = mpathd([L0, L0, PHONE, PHONE, LEAF_FUT], [0, t['m1a'] + i * .008, t['m1b'], t['m2a'], t['m2b'] - i * .006],
                   fill=GC(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke')
        y = 486 + i * 27
        marks = g([path('M%d %d L %d %d' % (170 + i * 5, y + 9, 830 - i * 5, y + 9), stroke=PP, stroke_width=2, opacity='.55'),
                   scribble(186 + i * 5, y + 14, 620 - i * 10, 22, 2, seed=i + 3, avoid=(360, 640), sw=2.2),
                   circle(360, y + 22, 5.5, fill=W), circle(640, y + 22, 5.5, fill=W)], k=show(.1, t['m1a'] + .01))
        fan = (LEAF_N - 1 - i) * -2.6
        leaf = g([d, marks], k=kf((0, dict(r=fan)), (t['m1a'], dict(r=fan)), (t['m1a'] + .06, 'o', dict(r=0))), c=(360, y + 22))
        leaves.append(g(leaf, k=pop(.075 + (LEAF_N - i) * .012, .07, -50, .9)))
    out.append(g(leaves))
    # the top board, propped open on its right end; the myna rides it
    tb0 = rrd(150, 440, 700, 36, 8)
    tb1 = rrd(392, 176, 216, 18, 9)
    board_t = mpathd([tb0, tb0, tb1, tb1], [0, t['m1a'], t['m1b'] - .02, 1], fill=GCH(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke')
    grain_t = g(_grain(160, 448, 680, 22, 4), k=show(.06, t['m1a']))
    out.append(g(g([board_t, grain_t], k=kf((0, dict(r=-9)), (t['m1a'], dict(r=-9)), (t['m1a'] + .08, dict(r=0))), c=(850, 476)),
                 k=kf((0, dict(o=0, y=-80)), (.06, dict(o=0, y=-80)), (.13, 'b', dict(o=1, y=0)), (t['m1b'] + .02, dict(o=1)), (t['m1b'] + .06, dict(o=0)))))
    # cord: through the holes, round the left end, a bead at the tail -> charging cable -> the leaf's own cord
    cord0 = [(360, 490), (300, 470), (200, 462), (120, 500), (112, 600), (150, 690), (210, 720), (250, 748), (236, 772), (300, 790)]
    cord1 = [(500, 716), (500, 736), (504, 752), (520, 764), (560, 772), (640, 776), (720, 778), (790, 778), (840, 776), (872, 774)]
    cord2 = [(500, 690), (500, 698), (501, 706), (503, 714), (506, 722), (510, 730), (514, 738), (518, 746), (521, 752), (523, 758)]
    cd = mpath([cord0, cord0, cord1, cord1, cord2], [0, t['m1a'], t['m1b'], t['m2a'], t['m2b']], k=28, closed=False,
               fill='none', stroke=I, stroke_width=7, stroke_linecap='round')
    out.append(g(cd, k=show(.1)))
    # bead on the cord tail (accent on ink) and the plug
    out.append(g(circle(300, 790, 11, fill=I) + circle(300, 790, 6.5, fill=A), k=show(.11, t['m1a'])))
    out.append(g(rect(860, 762, 46, 24, 5, fill=I) + rect(904, 768, 18, 12, 2, fill=I) + path('M868 768 l0 12 M876 768 l0 12', stroke=W, stroke_width=2), k=show(t['m1b'] - .02, t['m2a'] + .02)))
    # phone face (NOW)
    scr = ''.join([
        rect(380, 196, 240, 494, 28, fill=DK, stroke=I, stroke_width=3),
        rect(468, 208, 64, 14, 7, fill=I),
        text(400, 262, 'nilai.md', 28, fill=PP, fam='mono', bg='dk'),
        text(602, 262, '09:41', 18, fill=PP, anchor='end', fam='mono', bg='dk'),
        path('M400 290 L 600 290', stroke=PP, stroke_width=2),
    ] + [path('M400 %d L %d %d' % (330 + j * 34, 400 + (180 if j % 3 else 120), 330 + j * 34), stroke=PP, stroke_width=6, stroke_linecap='round', opacity='.9') for j in range(9)]
      + [rect(400, 640, 200, 30, 15, fill=GC()), text(500, 661, 'last touched', 16, fill=DK, anchor='middle', fam='mono', bg='col')])
    out.append(g(scr, k=kf((0, dict(o=0, s=.96)), (t['m1b'] - .03, dict(o=0, s=.96)), (t['m1b'] + .02, 'o', dict(o=1, s=1)), (t['m2a'], dict(o=1)), (t['m2a'] + .03, dict(o=0))), c=(500, 440)))
    out.append(g(rect(636, 300, 8, 70, 4, fill=I) + rect(356, 280, 8, 40, 4, fill=I) + rect(356, 330, 8, 40, 4, fill=I), k=show(t['m1b'] - .02, t['m2a'] + .02)))
    # FUTURE: the leaf glows from inside, thirteen ruled lines, its holes
    fut = [rect(474, 150, 52, 550, 26, fill=GR(), opacity='.85')]
    for j in range(13):
        y = 190 + j * 38
        fut.append(path('M480 %d L 520 %d' % (y, y), stroke=DK, stroke_width=3, stroke_linecap='round', data_dr='%s,%s' % (n2(t['m2b'] + j * .006), n2(t['m2b'] + .03 + j * .006))))
    fut.append(circle(500, 160, 6, fill=W) + circle(500, 690, 6, fill=W))
    out.append(g(fut, k=show(t['m2b'] - .02)))
    whole = g(out, k=kf((0, dict(x=0, s=1, o=1)), (.84, dict(x=0, s=1, o=1)), (.95, 'i', dict(x=470, s=.5, o=0))), c=(500, 420))
    return whole


def palm_leaf_marks(x, y, w, h, seed=0, lines=3):
    rnd = random.Random(seed)
    out = []
    for row in range(lines):
        yy = y + h * (.3 + .45 * row / max(lines - 1, 1))
        xx = x + 30
        while xx < x + w - 30:
            if abs(xx - 360) < 18 or abs(xx - 640) < 18:
                xx += 16
                continue
            L = rnd.uniform(9, 24)
            out.append(path('M%s %s q %s %s %s 0' % (n(xx), n(yy), n(L / 2), n(rnd.uniform(-4, 4)), n(L)), stroke=DK, stroke_width=2.4, fill='none', stroke_linecap='round'))
            xx += L + rnd.uniform(4, 10)
    return ''.join(out)


def myna_slides_off():
    t = AR.T
    stand = myna('stand', 1.05)
    startle = myna('startle', 1.05)
    k_stand = kf((0, dict(o=1)), (t['m1a'] + .05, dict(o=1)), (t['m1a'] + .052, dict(o=0)), (t['m1b'] + .03, dict(o=0)), (t['m1b'] + .032, dict(o=1)))
    k_st = kf((0, dict(o=0)), (t['m1a'] + .05, dict(o=0)), (t['m1a'] + .052, dict(o=1)), (t['m1b'] + .03, dict(o=1)), (t['m1b'] + .032, dict(o=0)))
    body = g(g(stand, k=k_stand) + g(startle, k=k_st))
    # rides the top board (propped at -9 deg), slides with it toward the phone top, then slips off and drops to the floor
    path_k = kf((0, dict(o=0, x=760, y=330, r=0)), (.1, dict(o=0, x=760, y=330)), (.15, 'b', dict(o=1, x=760, y=392, r=-9)),
                (t['m1a'], dict(x=760, y=392, r=-9)), (t['m1a'] + .06, 'i', dict(x=600, y=176, r=0)),
                (t['m1a'] + .1, 'n', dict(x=690, y=176, r=24)), (t['m1b'] + .03, 'n', dict(x=760, y=760, r=0)),
                (t['m2b'], dict(x=760, y=760)), (.8, dict(x=760, y=760)), (.86, 'b', dict(x=640, y=760)))
    return g(body, k=path_k, c=(0, 0))


# ------------------------------------------------------------ 02: the tharasu -> lab balance -> FAIR
def tharasu_scene():
    t = AR.T
    PX, PY, R = 500, 400, 280
    angles = []
    # swing: decaying oscillation as the keeper lifts it
    seq = [(0, -16), (.06, -16)]
    amp = -16
    for i in range(1, 8):
        amp *= -.58
        seq.append((.06 + .2 * i / 7, amp))
    seq.append((.27, 0))
    # myna lands on the right pan in THEN? no: the myna lands on the lab plate in NOW; THEN tilt only from the swing
    out = []
    out.append(shadow(500, 770, 330, 22))
    # angle keyframes as a beam rotation
    beam_k = kf(*[(tt, 'i' if j else 'l', dict(r=a)) for j, (tt, a) in enumerate(seq)])

    def end(a, side):
        ra = math.radians(a)
        return (PX + side * R * math.cos(ra), PY + side * R * math.sin(ra))
    def pan_k(side):
        fr = []
        for j, (tt, a) in enumerate(seq):
            ex, ey = end(a, side)
            fr.append((tt, 'i' if j else 'l', dict(x=ex - (PX + side * R), y=ey - PY)))
        return kf(*fr)
    # THEN parts fade at m1a; morph parts carry on
    cords_then = []
    for side in (-1, 1):
        cx = PX + side * R
        # three cords from the beam end to the pan rim
        cs = ''.join(path('M%s %s L %s %s' % (n(cx), n(PY + 6), n(cx + dx), n(PY + 210)), stroke=I, stroke_width=3) for dx in (-78, 0, 78))
        pan = (path('M%s %s C %s %s %s %s %s %s Z' % (n(cx - 96), n(PY + 208), n(cx - 80), n(PY + 268), n(cx + 80), n(PY + 268), n(cx + 96), n(PY + 208)), fill=GCH(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke')
               + ell(cx, PY + 208, 96, 12, fill=GI(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke')
               + ell(cx, PY + 209, 84, 8, fill=Sc.u('i')) + path('M%s %s q 40 -6 70 0' % (n(cx - 60), n(PY + 236)), stroke=PP, stroke_width=3, fill='none', opacity='.6'))
        cords_then.append(g(cs + pan, k=pan_k(side)))
    then = g(cords_then, k=kf((0, dict(o=0, y=-60)), (.05, dict(o=0, y=-60)), (.1, 'b', dict(o=1, y=0)), (t['m1a'], dict(o=1)), (t['m1a'] + .06, dict(o=0))))
    out.append(then)
    # the beam: a turned wooden beam with brass caps; its outline morphs into the top of the glass case
    beam0 = rrd(PX - R - 14, PY - 9, 2 * R + 28, 18, 9)
    beam1 = rrd(280, 286, 440, 16, 4)
    beam = mpathd([beam0, beam0, beam1, beam1], [0, t['m1a'], t['m1b'], 1], fill=GI(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke')
    caps = circle(PX - R - 10, PY, 12, fill=A, stroke=I, stroke_width=3) + circle(PX + R + 10, PY, 12, fill=A, stroke=I, stroke_width=3)
    tongue = path('M%s %s L %s %s L %s %s Z' % (n(PX - 7), n(PY), n(PX), n(PY - 92), n(PX + 7), n(PY)), fill=I)
    beam_then = g(g(caps + tongue, k=show(0, t['m1a'] + .02)), k=beam_k, c=(PX, PY))
    out.append(g(beam + g(caps + tongue, k=show(0, t['m1a'] + .02)), k=beam_k, c=(PX, PY)))
    # fork and loop (stay vertical), held by the keeper's hand
    fork = path('M%s %s L %s %s M %s %s L %s %s M %s %s L %s %s' % (n(PX - 14), n(PY - 4), n(PX - 14), n(PY - 104), n(PX + 14), n(PY - 4), n(PX + 14), n(PY - 104), n(PX - 16), n(PY - 104), n(PX + 16), n(PY - 104)), stroke=I, stroke_width=6, stroke_linecap='round')
    loop = path('M%s %s C %s %s %s %s %s %s C %s %s %s %s %s %s' % (n(PX), n(PY - 104), n(PX - 30), n(PY - 130), n(PX - 26), n(PY - 172), n(PX), n(PY - 172), n(PX + 26), n(PY - 172), n(PX + 30), n(PY - 130), n(PX), n(PY - 104)), stroke=I, stroke_width=6, fill='none')
    out.append(g(fork + loop, k=kf((0, dict(o=1, y=0)), (t['m1a'], dict(o=1, y=0)), (t['m1b'], dict(o=1, y=-46)), (t['m2a'] + .04, dict(o=1, y=-46)), (t['m2a'] + .08, dict(o=0, y=-46)))))
    # NOW: the analytical balance
    base = ''.join([
        path(poly([(250, 600), (750, 600), (776, 716), (224, 716)]), fill=GI(), stroke=W, stroke_width=1.5, vector_effect='non-scaling-stroke'),
        rect(224, 712, 552, 26, 6, fill=Sc.u('ih'), stroke=W, stroke_width=1.5),
        rect(370, 628, 260, 64, 8, fill=DK, stroke=I, stroke_width=3),
        circle(286, 660, 14, fill=GC(), stroke=W, stroke_width=1.5), circle(714, 660, 14, fill=GC(), stroke=W, stroke_width=1.5),
        rect(232, 736, 40, 14, 4, fill=I), rect(728, 736, 40, 14, 4, fill=I),
    ])
    case = ''.join([
        path('M290 300 L 290 600 M 710 300 L 710 600 M 500 300 L 500 600', stroke=I, stroke_width=7, stroke_linecap='round'),
        path('M300 330 L 360 300 M 300 420 L 420 300 M 520 360 L 580 300 M 520 470 L 690 300', stroke=I, stroke_width=3, opacity='.7', stroke_linecap='round'),
        rect(470, 420, 16, 60, 6, fill=GC(), stroke=W, stroke_width=1.5),
    ])
    plate = ell(500, 576, 120, 16, fill=GIH(), stroke=W, stroke_width=1.5) + rect(490, 580, 20, 22, fill=I)
    readout = ''.join([
        tag('text', '0.0000 g', x=500, y=674, font_size=40, fill=PP, text_anchor='middle', style='font-family:var(--f-md);font-weight:600', data_bg='dk',
            data_tx='0:0.0000 g|%s:  TARE?|%s:FAIR' % (n2(t['m1b'] + .11), n2(t['m2a'] + .06))),
    ])
    myna_icon = g(path('M408 646 q 10 -12 24 -4 l 8 -2 -6 6 q 2 10 -10 14 l -16 0 z', fill=PP), k=show(t['m1b'] + .09, t['m2a'] + .04))
    now = g([base, g(case, k=kf((0, dict(o=0)), (t['m1b'] - .05, dict(o=0)), (t['m1b'], dict(o=1)), (t['m2a'], dict(o=1)), (t['m2b'] - .03, dict(o=.0)))), plate, readout, myna_icon],
            k=kf((0, dict(o=0, y=30)), (t['m1a'] + .04, dict(o=0, y=30)), (t['m1b'], 'o', dict(o=1, y=0))))
    out.append(now)
    # FUTURE: an empty case outline, dashed, so the emptiness reads
    out.append(g(rect(290, 300, 420, 300, 4, fill='none', stroke=I, stroke_width=3, stroke_dasharray='10 12'), k=show(t['m2b'] - .04)))
    # the keeper: lifts it by the loop, hand on the loop until the last second
    # the keeper's hand comes down from above and grips the loop; it rises with the loop, and lets go at the last second
    out.append(g(hand_grip(PX, PY - 150), k=kf((0, dict(y=-420)), (.02, dict(y=-420)), (.07, 'o', dict(y=0)), (t['m1a'], dict(y=0)), (t['m1b'], dict(y=-46)),
                                               (t['m2a'] + .06, dict(y=-46)), (t['m2a'] + .12, 'n', dict(y=-520)))))
    # the myna: lands on the plate in NOW, two seconds later TARE?; hops off in FUTURE
    out.append(g(myna('stand', 1.1), k=kf((0, dict(o=0, x=900, y=200)), (t['m1b'] + .02, dict(o=0, x=900, y=200)), (t['m1b'] + .06, 'o', dict(o=1, x=500, y=568)),
                                          (t['m2a'] + .02, dict(x=500, y=568)), (t['m2a'] + .08, 'i', dict(x=820, y=760)))))
    return ''.join(out)


def hand_grip(x, y, s=1.0):
    """A forearm entering from the top of the frame, fingers curled round a bar at (x, y)."""
    sleeve = path('M%s -60 L %s %s L %s %s L %s -60 Z' % (n(x - 44), n(x - 40), n(y - 120), n(x + 40), n(y - 120), n(x + 44)), fill=GC(), stroke=DK, stroke_width=4)
    cuff = path('M%s %s L %s %s' % (n(x - 40), n(y - 124), n(x + 40), n(y - 124)), stroke=PP, stroke_width=4, stroke_dasharray='2 7', stroke_linecap='round')
    arm = path('M%s %s L %s %s L %s %s L %s %s Z' % (n(x - 30), n(y - 122), n(x - 34), n(y - 40), n(x + 34), n(y - 40), n(x + 30), n(y - 122)), fill=PP, stroke=DK, stroke_width=4, stroke_linejoin='round')
    palm = path('M%s %s C %s %s %s %s %s %s C %s %s %s %s %s %s Z' % (n(x - 36), n(y - 46), n(x - 44), n(y - 10), n(x - 30), n(y + 14), n(x), n(y + 16), n(x + 34), n(y + 14), n(x + 44), n(y - 12), n(x + 36), n(y - 46)), fill=PP, stroke=DK, stroke_width=4)
    fingers = ''.join(path('M%s %s q 2 18 -2 26' % (n(x - 24 + 16 * i), n(y - 10)), stroke=DK, stroke_width=3, fill='none', stroke_linecap='round') for i in range(4))
    thumb = path('M%s %s C %s %s %s %s %s %s' % (n(x + 30), n(y - 34), n(x + 52), n(y - 20), n(x + 50), n(y + 2), n(x + 30), n(y + 6)), fill=PP, stroke=DK, stroke_width=4, stroke_linecap='round')
    return g([sleeve, arm, cuff, palm, fingers, thumb])
