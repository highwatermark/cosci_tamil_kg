"""The 31 scenes. One function per scene, sNN(s) -> dict(art=svg, tr=transition, fx/fy=zoom focus, pu=pulli windows, html/tx extras).
Each scene's objects are built from functions per object and per stage (THEN / NOW / FUTURE) in objects.py."""
import math
from art import *  # noqa: F401,F403
import art as AR
from objects import *  # noqa: F401,F403
from objects_b import s03, s04, s05, s06, s07, s08  # noqa: F401
from objects_c import s09, s10, s11, s12, s13, s14, s15, s16  # noqa: F401
from objects_d import s17, s18, s19, s20, s21, s22, s23, s24  # noqa: F401
from objects_e import s25, s26, s27, s28, s29, s30, s31  # noqa: F401

SYMBOLS = ''
CSS = '''
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.mar .five{display:flex;flex-wrap:wrap;gap:.1rem .8rem;margin:0}
.mar .w5{position:relative;white-space:nowrap}
.mar .w5 .tk{position:absolute;left:-.9em;top:-.15em;font-family:var(--f-md);font-weight:600}
.yc{font-family:var(--f-md);font-size:clamp(1.1rem,5.4vw,1.6rem);margin:0 0 .5rem;letter-spacing:.02em}
'''
EXTRA_TAMIL = [(11, 'கொலைஞர் உலையேற்றித் தீமடுப்ப ஆமை', 'naladiyar:331')]


def _p(*a):
    return ''.join(a)


# ============================================================ 01 · the hand of 2526
def s01(s):
    t = AR.T
    out = []
    out.append(shadow(500, 772, 380, 26))
    # the year counter, the headline of the scene (desktop in the art; phone in the text column)
    mono = 'font-family:var(--f-md)'
    yc = _p('<g class="dk-only">',
            tag('text', 'last touched 27 Nov', x=150, y=118, font_size=42, fill=I, data_bg='wall', style=mono),
            tag('text', '2026', x=672, y=118, font_size=42, fill=I, data_bg='wall', style=mono + ';font-weight:600', data_n='.47,.6,2026,2527', data_k=kf((0, dict(o=1)), (.62, dict(o=1)), (.625, dict(o=0)))),
            tag('text', '2526', x=672, y=118, font_size=42, fill=I, data_bg='wall', style=mono + ';font-weight:600', data_k=kf((0, dict(o=0, y=-24)), (.62, dict(o=0, y=-24)), (.67, 'b', dict(o=1, y=0)))),
            '</g>')
    out.append(yc)
    out.append(book_bundle())
    out.append(phone_from_bundle())
    out.append(g(keeper('write', 'focus', s=.98), transform='translate(150 760)', k=pop(.07, .09, 60)))
    out.append(myna_slides_off())
    tx = '<p class="yc ph-only">last touched 27 Nov <span class="yy"><span data-n=".47,.6,2026,2527" data-k="%s">2026</span><span data-k="%s">2526</span></span></p>' % (
        kf((0, dict(o=1)), (.62, dict(o=1)), (.625, dict(o=0))), kf((0, dict(o=0)), (.62, dict(o=0)), (.66, 'b', dict(o=1))))
    return dict(art=''.join(out), tr='fade', fx=830, fy=540, pu='.47:.72:868:120', pre=tx)


# ============================================================ 02 · the beam that levels first
def s02(s):
    return dict(art=tharasu_scene(), tr='zoom', fx=500, fy=560)


def _todo(n):
    def f(s):
        return dict(art=text(500, 400, 'scene %02d' % n, 60, fill=I, anchor='middle', fam='disp', bg='wall'), tr='fade')
    return f


for _i in range(3, 32):
    if 's%02d' % _i not in globals():
        globals()['s%02d' % _i] = _todo(_i)
