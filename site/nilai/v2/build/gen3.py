#!/usr/bin/env python3
"""Splice the reel (and the ponderings grid) into site/nilai/index.html. Reads the HEAD copy, so it is re-runnable."""
import random, math, subprocess, pathlib, html as H

REPO = pathlib.Path('/Users/harilakshmanan/Cursor/cosci_knowledge_graph')
SRC = subprocess.run(['git', 'show', 'HEAD:site/nilai/index.html'], cwd=REPO, capture_output=True, check=True).stdout.decode('utf-8')
HERE = pathlib.Path(__file__).parent
css = (HERE / 'reel.css').read_text()
js = (HERE / 'reel.js').read_text()
E = H.escape

# ================================================================ props (all hand-drawn SVG)
def shade(cx, cy, rx, ry=None):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry or round(rx*.18,1)}" fill="var(--shade)"/>'

def st(cls, a, l, inner, style='', tag='g', attrs=''):
    return f'<{tag} class="st {cls}" style="--a:{a};--l:{l};{style}"{attrs}>{inner}</{tag}>'

def at(x, y, inner, extra=''):
    return f'<g transform="translate({x} {y}){extra}">{inner}</g>'

HAIR = '#2a1712'
def kid(pose='stand', react=''):
    """The protagonist: a young person with a palm-leaf stylus. Feet at (0,0), facing right."""
    sl = 'var(--lat)'
    arm = lambda d: f'<path d="{d}" stroke="{sl}" stroke-width="9" fill="none" stroke-linecap="round"/>'
    hnd = lambda x, y: f'<circle cx="{x}" cy="{y}" r="5" fill="var(--skin)"/>'
    sty = lambda d: f'<path d="{d}" stroke="var(--stone-d)" stroke-width="3" stroke-linecap="round"/>'
    arms = {
      'stand': arm('M-14 -96 Q-24 -74 -20 -54') + hnd(-20, -51) + arm('M13 -96 Q28 -84 30 -66') + hnd(30, -63) + sty('M27 -58 L45 -98'),
      'reach': arm('M-14 -96 Q-4 -78 22 -76') + hnd(25, -76) + arm('M13 -96 Q32 -96 46 -90') + hnd(49, -90) + sty('M49 -94 L58 -126'),
      'shrug': arm('M-14 -96 Q-34 -96 -36 -116') + hnd(-36, -119) + arm('M13 -96 Q34 -96 36 -116') + hnd(36, -119) + sty('M38 -122 L48 -150'),
      'write': arm('M-14 -96 Q-24 -74 -20 -54') + hnd(-20, -51) + arm('M13 -96 Q34 -74 40 -52') + hnd(41, -49) + sty('M40 -46 L56 -20'),
      'shield': arm('M13 -96 Q36 -100 40 -128') + hnd(40, -131) + arm('M-14 -96 Q4 -86 24 -84') + hnd(27, -84),
    }[pose]
    mouth = f'<ellipse cx="10" cy="-113" rx="3" ry="3.6" fill="{HAIR}"/>' if react in ('sing', '!') else f'<path d="M4 -114 q4 3 8 0" stroke="{HAIR}" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
    mark = f'<text x="20" y="-150" font-family="Newsreader, Georgia, serif" font-style="italic" font-weight="600" font-size="34" fill="var(--acc)">{react}</text>' if react in ('?', '!') else ''
    return f'''{shade(0,2,26,5)}<g class="idle">
<rect x="-13" y="-52" width="10" height="50" rx="4" fill="var(--ind)"/><rect x="3" y="-52" width="10" height="50" rx="4" fill="var(--ind)"/>
<path d="M-16 -3 h14 v4 h-16z M1 -3 h16 v4 h-15z" fill="var(--ind)"/>
<path d="M-18 -100 Q0 -108 18 -100 L22 -46 Q0 -40 -22 -46 Z" fill="{sl}"/><path d="M-14 -99 L20 -58" stroke="var(--tu)" stroke-width="5"/>
<rect x="-5" y="-108" width="10" height="8" fill="var(--skin)"/><circle cx="0" cy="-122" r="17" fill="var(--skin)"/>
<path d="M-17 -121 Q-19 -142 0 -141 Q17 -141 17 -127 Q4 -135 -17 -121Z" fill="{HAIR}"/><circle cx="-14" cy="-137" r="7" fill="{HAIR}"/>
<circle cx="8" cy="-123" r="1.9" fill="{HAIR}"/>{mouth}{arms}{mark}</g>'''

def kid_sit():
    return f'''{shade(0,2,70,8)}<g class="idle">
<path d="M-62 0 Q-64 -34 -20 -38 L20 -38 Q64 -34 62 0 Z" fill="var(--ind)"/>
<g class="b7-torso"><path d="M-26 -36 Q-30 -96 -12 -110 Q0 -116 12 -110 Q30 -96 26 -36 Z" fill="var(--lat)"/><path d="M-12 -108 L22 -50" stroke="var(--tu)" stroke-width="5"/></g>
<path d="M-20 -102 Q-46 -70 -40 -36 M20 -102 Q46 -70 40 -36" stroke="var(--lat)" stroke-width="10" fill="none" stroke-linecap="round"/>
<circle cx="-40" cy="-34" r="6" fill="var(--skin)"/><circle cx="40" cy="-34" r="6" fill="var(--skin)"/><circle cx="0" cy="-130" r="19" fill="var(--skin)"/>
<path d="M-19 -130 Q-20 -152 0 -151 Q20 -152 19 -132 Q6 -142 -19 -130Z" fill="{HAIR}"/><circle cx="0" cy="-153" r="8" fill="{HAIR}"/>
<path d="M-10 -128 q4 3 8 0 M3 -128 q4 3 8 0" stroke="{HAIR}" stroke-width="1.8" fill="none" stroke-linecap="round"/></g>'''

def person(body='var(--pea-l)', wrap='var(--chalk)', hair='var(--ind)', flip=False):
    g = f'''{shade(0,3,32,6)}<g class="idle"><path d="M-27 0 L-21 -80 Q0 -94 21 -80 L27 0 Z" fill="{body}"/>
<path d="M-21 -80 L24 -38 L20 -26 L-23 -64 Z" fill="{wrap}"/><path d="M21 -76 Q34 -50 26 -34" fill="none" stroke="{body}" stroke-width="9" stroke-linecap="round"/><circle cx="26" cy="-31" r="5" fill="var(--skin)"/>
<circle cx="0" cy="-106" r="20" fill="var(--skin)"/><path d="M-21 -106 Q-20 -130 0 -129 Q21 -130 21 -108 Q8 -120 -21 -106Z" fill="{hair}"/><circle cx="-12" cy="-124" r="8" fill="{hair}"/></g>'''
    return f'<g transform="scale(-1 1)">{g}</g>' if flip else g

def bot(glyph='&gt;_', case='var(--stone)', scr='var(--pea-d)'):
    return f'''{shade(0,3,30,6)}
<g class="lg" style="--s:1"><path d="M-11 -30 L-12 -2 h-9" fill="none" stroke="var(--ind)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></g>
<g class="lg" style="--s:-1"><path d="M11 -30 L12 -2 h9" fill="none" stroke="var(--ind)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></g>
<path d="M-31 -64 l-13 16 M31 -64 l13 16" stroke="var(--ind)" stroke-width="4" stroke-linecap="round"/>
<rect x="-31" y="-96" width="62" height="68" rx="9" fill="{case}"/><rect x="-31" y="-40" width="62" height="12" rx="6" fill="#000" opacity=".12"/>
<rect x="-24" y="-89" width="48" height="36" rx="5" fill="{scr}"/>
<text x="0" y="-65" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="15" font-weight="600" fill="var(--chalk)">{glyph}</text>
<rect x="-15" y="-47" width="30" height="5" rx="2.5" fill="var(--ind)" opacity=".5"/><path d="M0 -96 v-11" stroke="var(--ind)" stroke-width="3"/><circle cx="0" cy="-110" r="4.5" fill="var(--tu)"/>'''

def myna(flip=False, carry=''):
    g = f'''<g class="peck"><path d="M-16 -16 l-15 -7 l3 9z" fill="#2b2220"/><ellipse cx="0" cy="-16" rx="17" ry="12" fill="#2b2220"/><circle cx="13" cy="-30" r="9.5" fill="#2b2220"/>
<path d="M21 -32 l11 3 l-11 3z" fill="var(--tu)"/><circle cx="15" cy="-32" r="3.4" fill="var(--tu)"/><circle cx="15.6" cy="-32" r="1.4" fill="#111"/>
<path d="M-7 -20 q8 -7 15 2" stroke="var(--chalk)" stroke-width="4" fill="none" stroke-linecap="round"/>{carry}</g>
<path d="M-2 -5 v5 M5 -5 v5" stroke="var(--tu)" stroke-width="2.2" stroke-linecap="round"/>'''
    return f'<g transform="scale(-1 1)">{g}</g>' if flip else g

def lamp(flame=True):
    f = '<g class="flick"><path d="M0 -176 q16 22 0 40 q-16 -18 0 -40z" fill="var(--tu)"/><path d="M0 -160 q7 12 0 22 q-7 -10 0 -22z" fill="var(--chalk)"/></g>' if flame else ''
    return f'''{shade(0,3,40,6)}<path d="M-34 0 h68 l-10 -16 h-48z" fill="var(--tu-d)"/><rect x="-5" y="-130" width="10" height="118" fill="var(--tu-d)"/><path d="M-30 -132 h60 q-6 14 -30 14 q-24 0 -30 -14z" fill="var(--tu-d)"/>{f}'''

def hand(tool='pencil'):
    t = {'pencil': '<path d="M0 0 L10 -4 L44 56 L34 62 Z" fill="var(--tu)"/><path d="M0 0 L10 -4 L6 6 Z" fill="var(--ind)"/>',
         'marker': '<path d="M-6 -4 L12 -10 L46 52 L28 60 Z" fill="var(--tu)"/><path d="M-6 -4 L12 -10 L8 2 Z" fill="var(--lat-d)"/>',
         'chalk': '<path d="M0 0 L40 60" stroke="var(--chalk)" stroke-width="7" stroke-linecap="round"/>'}[tool]
    return f'''<g class="handg">{t}<path d="M30 46 q16 -10 28 4 q8 14 -4 26 l-26 6 q-10 -6 -6 -18z" fill="var(--skin)"/>
<path d="M44 70 L120 230 L170 210 L84 54 Z" fill="var(--lat)"/><path d="M60 92 L146 222 M74 80 L160 214" stroke="var(--tu)" stroke-width="5"/></g>'''

def kolam(cx, cy, m, n, s, cls='', ka=.3, kb=.55, dk=9, tip='', style=''):
    tipg = f'<g class="ktip">{tip}</g>' if tip else ''
    return (f'<g class="kolam {cls}" data-m="{m}" data-n="{n}" data-s="{s}" data-ka="{ka}" data-kb="{kb}" '
            f'transform="translate({cx} {cy})" style="--ka:{ka};--kb:{kb};--dk:{dk};{style}">{tipg}</g>')

def leafprop(x, y, w, h, fill='var(--palm)'):
    ink = ''.join(f'<path d="M{x+16+j*w/5:.0f} {y+h/2:.0f}h{w/7:.0f}" stroke="var(--palm-d)" stroke-width="2" stroke-linecap="round"/>' for j in range(5))
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2:.1f}" fill="{fill}" stroke="var(--palm-d)" stroke-width="1.2"/>{ink}'

def bubble(x, y, w=150, h=90, fill='var(--chalk)', txt=''):
    return f'<g><rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="30" fill="{fill}"/><path d="M{x-20} {y+h/2-4} l-18 30 l40 -26z" fill="{fill}"/>{txt}</g>'

def FLOOR(y=400):
    return f'<rect class="fl" x="-3000" y="{y}" width="7000" height="3000"/><rect x="-3000" y="{y}" width="7000" height="5" fill="#000" opacity=".1"/>'

# lens icons, 48×48, drawn in currentColor
ICON = {
 'all': '<g fill="currentColor"><path d="M4 40h10l-2-3H6z M19 40h10l-2-3h-6z M34 40h10l-2-3h-6z"/><rect x="8" y="24" width="2" height="13"/><rect x="23" y="24" width="2" height="13"/><rect x="38" y="24" width="2" height="13"/><path d="M6 24h6q-1 3-3 3t-3-3z M21 24h6q-1 3-3 3t-3-3z M36 24h6q-1 3-3 3t-3-3z"/><path d="M9 14q4 5 0 9q-4-4 0-9z M24 12q4 5 0 9q-4-4 0-9z M39 14q4 5 0 9q-4-4 0-9z"/></g>',
 'ineq': '<g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><path d="M24 8v32M16 42h16M8 12l32 8"/><path d="M8 12l-5 12h10z M40 20l-5 12h10z" fill="currentColor" stroke-width="1.5"/></g>',
 'adv': '<g fill="currentColor"><path d="M8 42h14l-2-3H10z"/><rect x="14" y="26" width="2" height="13"/><path d="M15 15q4 5 0 9q-4-4 0-9z"/><path d="M46 30 L30 26 q-4-1-4 2 q0 2 3 2 l-6 1 q-3 1-2 3 q1 2 4 1 l-3 2 q-2 2 0 3 q2 1 4-1 l3-1 L46 38z"/></g>',
 'cre': '<g fill="currentColor"><path d="M10 40 L34 14 L37 17 L13 43 L8 45z"/><path d="M38 4 l2 6 l6 2 l-6 2 l-2 6 l-2-6 l-6-2 l6-2z"/></g>',
 'steer': '<g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><path d="M10 8 L36 38"/><path d="M33 34 q8 2 10 9 q-7 -1 -11 -6z" fill="currentColor"/><path d="M4 42 q6-4 12 0 t12 0 t12 0"/></g>',
}
def icon(k, size=28, cls='r-ic'):
    return f'<svg class="{cls}" viewBox="0 0 48 48" width="{size}" height="{size}" aria-hidden="true" focusable="false">{ICON[k]}</svg>'
def bigicon(k, x, y, s=3, color='var(--lensc)'):
    return f'<g transform="translate({x} {y}) scale({s})" style="color:{color}">{ICON[k]}</g>'

# ================================================================ scene art
A = {}
lv = []
for i in range(6):
    y = 345 - i * 9
    inks = ''.join(f'<path d="M{330+j*55} {y+3.2}h{30+((i*7+j*13)%22)}" stroke="var(--palm-d)" stroke-width="1.6" stroke-linecap="round"/>' for j in range(6))
    lv.append(f'<g class="b1-leaf" style="--k:{i+1};--r:{(i-2.5)*1.4:.1f}"><rect x="315" y="{y-1}" width="370" height="10" rx="5" fill="{"var(--palm)" if i%2==0 else "#e6cf9f"}"/>{inks}</g>')
A['title'] = f'''{FLOOR()}<circle cx="500" cy="210" r="250" fill="var(--chalk)" opacity=".05"/>{shade(500,402,240,10)}
<rect x="285" y="372" width="430" height="16" rx="5" fill="var(--lat-d)"/><rect x="305" y="386" width="14" height="16" fill="var(--lat-d)"/><rect x="681" y="386" width="14" height="16" fill="var(--lat-d)"/>
<rect x="305" y="354" width="390" height="16" rx="8" fill="var(--ind-l)"/>
<rect class="b1-str" x="398" y="300" width="3" height="56" fill="var(--tu)"/><rect class="b1-str" x="599" y="300" width="3" height="56" fill="var(--tu)"/>
{''.join(lv)}
<g class="b1-top"><rect x="305" y="290" width="390" height="16" rx="8" fill="var(--ind-l)"/><circle cx="400" cy="298" r="4" fill="var(--tu)"/><circle cx="600" cy="298" r="4" fill="var(--tu)"/></g>
{st('slx', .05, .35, at(225, 400, kid('stand')), '--dx:-420')}
{st('hop', .35, .3, at(900, 300, myna(flip=True)), '--dx:-150;--hh:-90;--dy:-150')}'''

stk = ''.join(st('drop', .02 + i*.045, .2, f'<rect x="{360+(i%3)*4}" y="{380-i*11}" width="{280-(i%2)*8}" height="10" rx="5" fill="{"var(--palm)" if i%2 else "#ead6aa"}" stroke="var(--palm-d)" stroke-width="1"/>', f'--dy:-{420+i*20}') for i in range(8))
A['stack'] = f'''{FLOOR()}{shade(500,402,170,9)}{stk}
{st('pop', .42, .16, '<rect x="350" y="380" width="300" height="14" rx="7" fill="var(--lat-d)"/>', '--dy:20')}
{st('drop', .48, .16, '<rect x="350" y="291" width="300" height="14" rx="7" fill="var(--lat-d)"/>', '--dy:-200')}
{st('pop', .58, .14, '<path d="M440 286 V396 M560 286 V396" stroke="var(--tu)" stroke-width="3"/>', '--dy:0')}
{at(260, 400, kid('stand'))}{st('pop', .64, .14, at(620, 291, myna()), '--dy:-40')}'''

lets = ['அ', 'k', 'ழ', 'a', 'ம', '0', 'த', '1', 'ந', 'e', 'ய', 'r']
fall = ''.join(st('fall', .02 + i*.05, .16, f'<text x="{500+(i%3-1)*8}" y="214" text-anchor="middle" font-family="Noto Serif Tamil, IBM Plex Mono, serif" font-weight="600" font-size="30" fill="var(--tu)" class="glow">{g}</text>', '--dy:150') for i, g in enumerate(lets))
A['tap'] = f'''{FLOOR()}
<rect x="-400" y="128" width="880" height="26" rx="6" fill="var(--tu-d)"/><rect x="470" y="118" width="58" height="46" rx="8" fill="var(--tu-d)"/>
<path d="M478 164 h42 v22 q0 8 -8 8 h-26 q-8 0 -8 -8z" fill="var(--tu-d)"/><rect x="488" y="96" width="22" height="24" rx="4" fill="var(--lat)"/><rect x="464" y="88" width="70" height="12" rx="6" fill="var(--lat)"/>
{fall}{shade(500,404,110,10)}<path d="M410 350 h180 q-10 54 -90 54 q-80 0 -90 -54z" fill="var(--lat)"/>
{st('grow', .2, .5, '<ellipse cx="500" cy="350" rx="82" ry="20" fill="var(--tu)" class="glow"/>')}
<path d="M402 350 h196" stroke="var(--lat-d)" stroke-width="8" stroke-linecap="round"/>
{at(700, 400, kid('reach', '!'), ' scale(-1 1)')}
{st('hop', .4, .3, at(330, 400, myna(carry='<text x="30" y="-22" font-family="Noto Serif Tamil, serif" font-size="20" font-weight="600" fill="var(--tu)" class="glow">ழ</text>')), '--dx:-120;--hh:-80')}'''

LENS = [('all', 'what if everyone has it?'), ('ineq', 'what if it widens the gap?'), ('adv', 'what if the wrong hands get it?'), ('cre', 'what will creativity be?'), ('steer', 'steer, or be steered?')]
A['lenses'] = FLOOR() + ''.join(st('pop', .04 + j*.05, .2, f'<g transform="translate({220+j*140} 0)"><rect x="-56" y="180" width="112" height="112" rx="26" fill="var(--chalk)"/>{bigicon(k, -48, 188, 2, "var(--lc-"+k+")")}<rect x="-3" y="292" width="6" height="108" fill="var(--chalk)" opacity=".7"/></g>', '--dy:200') for j, (k, _) in enumerate(LENS)) + at(140, 400, kid('stand', '?')) + st('hop', .4, .3, at(860, 400, myna(flip=True)), '--dx:-70;--hh:-170;--dy:-108')

# essence 1: a brass scale weighs a speech bubble
A['scale'] = f'''{FLOOR()}{shade(500,404,90,9)}
<path d="M470 400 h60 l-12 -22 h-36 z" fill="var(--ind)"/><rect x="494" y="190" width="12" height="190" fill="var(--ind)"/>
<g class="b4-beam"><rect x="499" y="40" width="2" height="2" fill="none"/>
 <rect x="290" y="178" width="420" height="10" rx="5" fill="var(--tu-d)"/><circle cx="500" cy="183" r="12" fill="var(--ind)"/>
 <g class="b4-pan"><path d="M300 183 L262 300 M300 183 L338 300" stroke="var(--ind)" stroke-width="2"/><path d="M250 300 h100 q-8 26 -50 26 q-42 0 -50 -26z" fill="var(--tu-d)"/>
  <g transform="translate(300 262) scale(.42)">{bubble(0, 0, 160, 100, 'var(--chalk)', '<text x="0" y="12" text-anchor="middle" font-family="Newsreader, Georgia, serif" font-size="40" font-weight="600" fill="var(--ind)">“…”</text>')}</g></g>
 <g class="b4-pan"><path d="M700 183 L662 300 M700 183 L738 300" stroke="var(--ind)" stroke-width="2"/><path d="M650 300 h100 q-8 26 -50 26 q-42 0 -50 -26z" fill="var(--tu-d)"/>
  <rect x="676" y="276" width="20" height="24" rx="3" fill="var(--ind)"/><rect x="700" y="284" width="16" height="16" rx="3" fill="var(--ind)"/><rect x="718" y="288" width="12" height="12" rx="2" fill="var(--ind)"/></g></g>
{at(860, 400, kid('reach'), ' scale(-1 1)')}{st('pop', .5, .2, at(500, 171, myna()), '--dy:-60')}'''

# essence 2: a banana leaf rises as a wipe; portions pass along a row of hands
hands_row = ''.join(f'<g transform="translate({250+j*125} 500)"><path d="M-20 0 L-14 -70 L14 -70 L20 0Z" fill="{["var(--lat)","var(--pea-l)","var(--ind-l)","var(--tu-d)","var(--pea)"][j]}"/><ellipse cx="0" cy="-74" rx="18" ry="12" fill="var(--skin)"/></g>' for j in range(5))
balls = ''.join(st('pass', .3 + k*.06, .26, '<circle cx="250" cy="410" r="11" fill="var(--chalk)"/>', f'--dx:{(k+1)*125}') for k in range(4))
A['leaf'] = f'''{FLOOR()}
<g class="wipe"><path d="M-200 300 Q500 250 1200 300 L1200 700 L-200 700Z" fill="var(--pea)"/><path d="M-200 300 Q500 250 1200 300" stroke="var(--pea-d)" stroke-width="10" fill="none"/>{''.join(f'<path d="M{x} 285 l-40 60" stroke="var(--pea-d)" stroke-width="3"/>' for x in range(-150, 1200, 70))}</g>
{st('pop', .15, .2, hands_row, '--dy:120')}{balls}
{st('hop', .6, .25, at(840, 300, myna(flip=True)), '--dx:-40;--hh:-40')}'''

# essence 3: a body-letter and a life-letter join; the protagonist breathes; then the camera dives into அ
tiles3 = (st('slx', .05, .2, '<g><rect x="250" y="250" width="110" height="110" rx="16" fill="var(--pea-d)"/><rect x="242" y="242" width="110" height="110" rx="16" fill="var(--chalk)"/><text x="297" y="322" text-anchor="middle" font-family="Noto Serif Tamil, serif" font-size="64" font-weight="600" fill="var(--ind)">ம்</text></g>', '--dx:-300')
          + st('slx', .12, .2, '<g><rect x="650" y="250" width="110" height="110" rx="16" fill="var(--pea-d)"/><rect x="642" y="242" width="110" height="110" rx="16" fill="var(--tu)"/><text x="697" y="322" text-anchor="middle" font-family="Noto Serif Tamil, serif" font-size="64" font-weight="600" fill="var(--ind)">அ</text></g>', '--dx:300')
          + st('pop', .3, .2, '<text x="497" y="330" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="40" fill="var(--chalk)">→</text>', '--dy:20'))
A['body'] = f'''{FLOOR()}<circle class="b7-c" cx="500" cy="230" r="120" fill="var(--tu)" opacity=".85"/>
{at(500, 400, kid_sit())}{tiles3}
{st('pop', .38, .16, '<text x="500" y="160" text-anchor="middle" font-family="Noto Serif Tamil, serif" font-size="70" font-weight="600" fill="var(--chalk)">ம</text>', '--dy:40')}
<g class="zoomglyph"><circle cx="0" cy="0" r="26" fill="var(--chalk)"/><text x="0" y="40" text-anchor="middle" font-family="Noto Serif Tamil, serif" font-size="120" font-weight="600" fill="var(--chalk)">அ</text></g>
{st('pop', .5, .2, at(820, 400, myna(flip=True)), '--dy:-40')}'''

# essence 4: five landscape flats; a leaf letter hops from the lover to the friend to the beloved
X = [168, 300, 432, 564, 696]; W = 136
hill = f'<path d="M{X[0]} 0 V-140 L{X[0]+34} -232 L{X[0]+62} -178 L{X[0]+96} -262 L{X[0]+W} -150 V0Z" fill="var(--pea-d)"/><path d="M{X[0]+80} -222 L{X[0]+96} -262 L{X[0]+112} -224 Q{X[0]+96} -212 {X[0]+80} -222Z" fill="var(--chalk)"/>' + ''.join(f'<circle cx="{X[0]+18+j*16}" cy="{-30-(j%3)*14}" r="5" fill="var(--ind-l)"/>' for j in range(7))
forest = ''.join(f'<rect x="{X[1]+c-5}" y="-80" width="10" height="80" fill="var(--lat-d)"/><circle cx="{X[1]+c}" cy="{-110-h}" r="{r}" fill="{f}"/>' for c, h, r, f in [(30, 30, 34, 'var(--pea)'), (70, 70, 40, 'var(--pea-d)'), (108, 20, 30, 'var(--pea)')])
field = f'<rect x="{X[2]}" y="-200" width="{W}" height="200" rx="14" fill="var(--pea-l)"/><circle cx="{X[2]+98}" cy="-164" r="18" fill="var(--tu)"/>' + ''.join(f'<path d="M{X[2]+14} {-110+j*24} h{W-28}" stroke="var(--pea-d)" stroke-width="5" stroke-dasharray="6 8" stroke-linecap="round"/>' for j in range(4))
shore = f'<rect x="{X[3]}" y="-190" width="{W}" height="190" rx="14" fill="var(--ind-l)"/><path d="M{X[3]} -70 q17 -16 34 0 t34 0 t34 0 t34 0 V0 H{X[3]}Z" fill="var(--pea)"/><path d="M{X[3]} -40 q17 -14 34 0 t34 0 t34 0 t34 0 V0 H{X[3]}Z" fill="var(--pea-d)"/><path d="M{X[3]+36} -92 h64 l-12 18 h-40z" fill="var(--lat)"/><path d="M{X[3]+68} -96 V-150 L{X[3]+98} -100Z" fill="var(--chalk)"/>'
desert = f'<rect x="{X[4]}" y="-210" width="{W}" height="210" rx="14" fill="var(--lat)"/><circle cx="{X[4]+40}" cy="-160" r="22" fill="var(--chalk)"/><path d="M{X[4]} -60 Q{X[4]+60} -110 {X[4]+W} -70 V0 H{X[4]}Z" fill="var(--tu-d)"/><path d="M{X[4]+92} -84 V-136 M{X[4]+92} -116 l-16 -14 M{X[4]+92} -106 l16 -12" stroke="var(--ind)" stroke-width="5" stroke-linecap="round"/>'
names = ['குறிஞ்சி', 'முல்லை', 'மருதம்', 'நெய்தல்', 'பாலை']
flats = ''.join(st('slx', .02 + i*.05, .3, f'<path d="M{x+W*0.55} 400 L{x+W*0.8} 400 L{x+W*0.62} 250 Z" fill="var(--stone-d)"/><g transform="translate(0 400)">{shade(x+W/2,3,W*.55,7)}{inner}</g><g transform="translate({x+W/2} 432)"><rect x="-44" y="-15" width="88" height="28" rx="14" fill="var(--chalk)"/><text x="0" y="5" text-anchor="middle" font-family="Noto Serif Tamil, serif" font-size="14" font-weight="600" fill="var(--ind)">{names[i]}</text></g>', f'--dx:{-1000 if i%2==0 else 1000}') for i, (x, inner) in enumerate(zip(X, [hill, forest, field, shore, desert])))
A['flats'] = f'''{FLOOR()}<g class="backflats">{flats}</g>
{at(250, 470, kid('reach'), ' scale(.62)')}{at(500, 470, person('var(--pea)', 'var(--chalk)'), ' scale(.62)')}{at(750, 470, person('var(--ind-l)', 'var(--tu)', flip=True), ' scale(.62)')}
<g class="b-letter" style="--a1:.3;--a2:.5">{leafprop(262, 402, 40, 11)}</g>'''

# essence 5: the atom zooms out into stars
rnd = random.Random(11)
stars = ''.join(f'<circle class="b8-s" cx="{500+x:.0f}" cy="{230+y:.0f}" r="{r}" fill="{c}" style="--dx:{x:.0f};--dy:{y:.0f};--d:{d:.2f}"/>' for x, y, r, c, d in
                [(rnd.uniform(-480, 480), rnd.uniform(-220, 150), rnd.choice([1.4, 1.8, 2.2, 2.8, 3.6]), 'var(--tu)' if i % 7 == 0 else ('var(--pea-l)' if i % 5 == 0 else 'var(--chalk)'), rnd.uniform(0, .6)) for i in range(60)])
orb = ''.join(f'<g transform="rotate({a} 500 230)"><g class="b8-o" style="--o:{k}"><ellipse cx="500" cy="230" rx="150" ry="48" fill="none" stroke="var(--chalk)" stroke-width="3" opacity=".85"/><circle cx="650" cy="230" r="9" fill="var(--tu)"/></g></g>' for k, a in enumerate([0, 60, 120]))
gal = ''.join(f'<circle cx="{500+(6+j*3.2)*math.cos(j*.55+arm*math.pi):.1f}" cy="{230+(6+j*3.2)*.45*math.sin(j*.55+arm*math.pi):.1f}" r="{max(1.2, 3.2-j*.08):.1f}"/>' for arm in (0, 1) for j in range(26))
A['atom'] = f'''{FLOOR(430)}{stars}
<g class="b8-gal" fill="var(--chalk)">{gal}<circle cx="500" cy="230" r="8" fill="var(--tu)"/></g>
<g class="b8-atom">{orb}<g><circle cx="490" cy="224" r="13" fill="var(--lat)"/><circle cx="510" cy="224" r="13" fill="var(--tu)"/><circle cx="500" cy="240" r="13" fill="var(--lat)"/><circle cx="488" cy="242" r="12" fill="var(--tu)"/><circle cx="512" cy="242" r="12" fill="var(--lat-d)"/><circle cx="500" cy="221" r="12" fill="var(--tu-d)"/></g></g>
{at(240, 430, kid('reach'), ' scale(.8)')}
<g transform="translate(800 430) scale(.7)"><circle cx="0" cy="-120" r="34" fill="none" stroke="var(--chalk)" stroke-width="8"/><path d="M-10 -86 L-24 0 M10 -86 L24 0 M-30 0 h60" stroke="var(--chalk)" stroke-width="8" stroke-linecap="round"/></g>'''

# essence 6: the water clock sinks as it fills
A['clock'] = f'''{FLOOR()}{shade(500,404,240,12)}
<path d="M285 230 L715 230 L680 400 L320 400 Z" fill="var(--tu-d)"/><path d="M300 268 L700 268 L683 392 L317 392 Z" fill="var(--pea-d)"/>
<g class="b6-bowl"><clipPath id="b6clip"><path d="M420 240 h160 q0 70 -80 70 q-80 0 -80 -70z"/></clipPath>
 <path d="M420 240 h160 q0 70 -80 70 q-80 0 -80 -70z" fill="var(--lat)"/><g clip-path="url(#b6clip)"><rect class="b6-fill" x="410" y="240" width="180" height="72" fill="var(--pea-l)"/></g>
 <path d="M414 240 h172" stroke="var(--lat-d)" stroke-width="7" stroke-linecap="round"/></g>
<path d="M300 268 L700 268 L683 392 L317 392 Z" fill="var(--pea-l)" opacity=".42"/><path d="M280 226 h440" stroke="var(--tu)" stroke-width="10" stroke-linecap="round"/>
<text class="cnt" data-count="24" data-clock="1" x="500" y="150" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="44" font-weight="500" fill="var(--ind)">24:00</text>
<text x="500" y="182" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="15" fill="var(--ind)">of 24:00 · one <tspan font-family="Noto Serif Tamil, serif">நாழிகை</tspan></text>
{at(180, 400, kid('stand'))}{st('pop', .5, .2, at(705, 226, myna(flip=True)), '--dy:-40')}'''

# ---- the five lens stages (each used twice). Phases inside a what-if: card one ~.08, card two ~.28, the answer ~.5, then hold.
gl = ['&gt;_', 'அ', '01', 'ஓ', '?', 'க', '&gt;_', '∑', 'ம', '01']
march = ''.join(f'<g transform="translate(0 400)"><g class="b5-m" style="--d:{i*.05:.3f};--fx:{880-i*74}">{bot(gl[i], ["var(--stone)","var(--chalk)","var(--stone)","var(--palm)"][i%4])}</g></g>' for i in range(10))
A['L-all'] = f'''{FLOOR()}<g fill="var(--chalk)" opacity=".5">{''.join(f'<circle cx="{x+(20 if r%2 else 0)}" cy="{420+r*26}" r="3"/>' for r in range(3) for x in range(-400, 1400, 40))}</g>
{march}{at(130, 400, kid('stand', '?'))}{st('pop', .52, .15, at(880, 290, myna()), '--dy:-60')}'''

A['L-ineq'] = f'''{FLOOR()}{shade(500,404,100,9)}
<path d="M470 400 h60 l-12 -22 h-36 z" fill="var(--ind)"/><rect x="494" y="170" width="12" height="210" fill="var(--ind)"/>
<g class="tiltbeam"><rect x="499" y="20" width="2" height="2" fill="none"/>
 <rect x="280" y="158" width="440" height="10" rx="5" fill="var(--tu-d)"/><circle cx="500" cy="163" r="12" fill="var(--ind)"/>
 <g class="tiltpan"><path d="M290 163 L252 280 M290 163 L328 280" stroke="var(--ind)" stroke-width="2"/><path d="M240 280 h100 q-8 26 -50 26 q-42 0 -50 -26z" fill="var(--tu-d)"/><path d="M246 280 Q290 196 334 280Z" fill="var(--tu)"/></g>
 <g class="tiltpan"><path d="M710 163 L672 280 M710 163 L748 280" stroke="var(--ind)" stroke-width="2"/><path d="M660 280 h100 q-8 26 -50 26 q-42 0 -50 -26z" fill="var(--tu-d)"/><path class="growheap" d="M676 280 Q710 196 744 280Z" fill="var(--tu)"/></g></g>
{at(860, 400, kid('reach', '?'), ' scale(-1 1)')}{st('hop', .55, .25, at(140, 400, myna()), '--dx:100;--hh:-60')}'''

A['L-adv'] = f'''{FLOOR()}<circle cx="430" cy="250" r="160" fill="var(--tu)" opacity=".18"/>{at(430, 400, lamp())}
<g class="reacher"><path d="M1300 210 L760 236 Q726 238 724 254 Q724 270 744 272 L700 278 Q682 284 690 298 Q700 310 724 302 L708 316 Q698 330 714 334 Q728 336 744 322 L1300 300Z" fill="var(--ind-d)"/></g>
{at(310, 400, kid('shield'))}{st('pop', .3, .15, at(560, 400, myna(flip=True, carry='<text x="-40" y="-46" font-family="Newsreader, serif" font-weight="700" font-size="30" fill="var(--lat)">!</text>')), '--dy:-40')}'''

copies = ''.join(st('pop', .1 + j*.04, .12, f'<rect x="{620+j*4}" y="{376-j*9}" width="150" height="9" rx="4.5" fill="var(--stone)" stroke="var(--stone-d)" stroke-width="1"/>', '--dy:-30') for j in range(8))
A['L-cre'] = f'''{FLOOR()}{at(840, 400, bot('&gt;_', 'var(--stone)'))}{copies}
{shade(330,404,110,8)}{leafprop(240, 380, 200, 18)}
{at(200, 400, kid('write'))}
<g class="spark"><path d="M340 300 l10 30 l30 10 l-30 10 l-10 30 l-10 -30 l-30 -10 l30 -10z" fill="var(--tu)" class="glow"/></g>
{st('hop', .55, .25, at(520, 400, myna(flip=True)), '--dx:-60;--hh:-80')}'''

A['L-steer'] = f'''<rect class="fl" x="-3000" y="400" width="7000" height="3000"/>
<g class="waves" fill="none" stroke="var(--chalk)" stroke-width="4" opacity=".55">{''.join(f'<path d="M{x} {430+r*30} q20 -12 40 0 t40 0"/>' for r in range(3) for x in range(-200, 1200, 160))}</g>
<g class="boat"><g class="idle2"><path d="M330 380 h300 q-20 46 -70 46 h-160 q-50 0 -70 -46z" fill="var(--lat)"/><path d="M330 380 h300" stroke="var(--lat-d)" stroke-width="8" stroke-linecap="round"/>
 {at(470, 382, kid('stand'), ' scale(.8)')}
 <g class="oar"><path d="M520 300 L640 470" stroke="var(--tu-d)" stroke-width="8" stroke-linecap="round"/><path d="M628 452 q30 6 34 36 q-26 -4 -42 -24z" fill="var(--tu-d)"/></g>
 {at(600, 380, myna())}</g></g>
<g transform="translate(880 400)"><rect x="-14" y="-200" width="28" height="200" fill="var(--chalk)"/><path d="M-14 -150 h28 M-14 -100 h28 M-14 -50 h28" stroke="var(--lat)" stroke-width="10"/><g class="flick"><circle cx="0" cy="-214" r="16" fill="var(--tu)" class="glow"/></g></g>'''

# closing scene 1: the user's own line
A['steerline'] = A['L-steer']
# closing scene 2: the kolam draws itself from dots; the first dot is the pulli
A['kolam'] = f'''{FLOOR(220)}<rect x="-3000" y="214" width="7000" height="8" fill="var(--lat-d)"/>
{kolam(560, 345, 7, 5, 22, "k-main", ka=.12, kb=.4, dk=14, tip='<circle r="7" fill="var(--tu)"/>')}
{at(260, 400, kid_sit(), ' scale(.7)')}{st('pop', .55, .2, at(820, 270, myna(flip=True)), '--dy:-40')}'''

# middle: a finished kolam is swept away in the morning, on purpose
A['sweep'] = f'''{FLOOR(300)}<rect x="-3000" y="294" width="7000" height="8" fill="var(--lat-d)"/>
<g class="swept">{kolam(500, 370, 6, 3, 18, "k-sweep", ka=0, kb=.01, dk=99)}</g>
<g class="broom">{at(0, 400, kid('write'), ' scale(.8)')}<path d="M40 330 L100 420" stroke="var(--tu-d)" stroke-width="6" stroke-linecap="round"/><path d="M86 410 l40 -14 l20 30 l-46 10z" fill="var(--tu-d)"/></g>

{st('pop', .3, .2, at(860, 300, myna(flip=True)), '--dy:-40')}'''

# far turn: the stage pulls back to the night; the kolam's dots rise and become stars
rnd = random.Random(5)
m, n, s = 7, 4, 16
turn_dots = []
for i in range(m):
    for j in range(n):
        x0 = 500 - m*s + (2*i+1)*s; y0 = 360 - n*s + (2*j+1)*s
        tx, ty = rnd.uniform(-20, 1020), rnd.uniform(-60, 300)
        turn_dots.append(st('fly', .05 + rnd.uniform(0, .25), .45, f'<circle cx="{x0}" cy="{y0}" r="{rnd.choice([2.6, 3.2, 4])}" fill="{"var(--tu)" if (i*n+j) % 6 == 0 else "var(--chalk)"}"/>', f'--dx:{tx-x0:.0f};--dy:{ty-y0:.0f}'))
A['turn'] = f'''<rect class="fl" x="-3000" y="400" width="7000" height="3000"/>
<g class="pullback"><g class="fadeline">{kolam(500, 360, m, n, s, "k-turn", ka=0, kb=.01, dk=99)}</g>{at(300, 400, kid('reach', '!'))}</g>
{''.join(turn_dots)}'''

# far 1: the ladder of senses, seven rungs, the seventh open and glowing; a machine floats at the sixth
sense_ic = [
 '<circle cx="0" cy="4" r="9"/><rect x="-9" y="-12" width="4" height="12" rx="2"/><rect x="-3" y="-15" width="4" height="15" rx="2"/><rect x="3" y="-13" width="4" height="13" rx="2"/><rect x="8" y="-6" width="4" height="10" rx="2" transform="rotate(30 10 0)"/>',
 '<path d="M-14 0 q14 -12 28 0 q-14 12 -28 0z"/><path d="M-5 2 q5 12 10 0z" fill="var(--lat)"/>',
 '<path d="M-2 -14 q-2 12 -10 18 q8 4 14 0 q4 -4 0 -6z"/>',
 '<path d="M-16 0 q16 -14 32 0 q-16 14 -32 0z"/><circle r="5.5" fill="var(--ind-d)"/>',
 '<path d="M-6 -14 q16 -2 14 14 q-2 10 -10 12 q-4 0 -4 -4" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>',
 '<circle cx="0" cy="0" r="13"/><path d="M14 -14 l3 6 l6 3 l-6 3 l-3 6 l-3 -6 l-6 -3 l6 -3z" fill="var(--tu)"/>',
]
sense_lb = ['touch', 'taste', 'smell', 'sight', 'hearing', 'mind']
rungs = ''.join(st('pop', .03 + k*.04, .14, f'<rect x="440" y="{376-k*50}" width="120" height="8" rx="4" fill="var(--palm)"/><g transform="translate(410 {380-k*50})" fill="var(--chalk)" style="color:var(--chalk)">{sense_ic[k]}</g><text x="574" y="{386-k*50}" font-family="IBM Plex Mono, monospace" font-size="13" fill="var(--chalk)">{sense_lb[k]}</text>', '--dy:20') for k in range(6))
A['ladder'] = f'''{FLOOR()}<rect x="432" y="40" width="10" height="362" rx="4" fill="var(--palm-d)"/><rect x="558" y="40" width="10" height="362" rx="4" fill="var(--palm-d)"/>
{rungs}
{st('grow', .5, .2, '<rect x="440" y="76" width="120" height="8" rx="4" fill="var(--tu)" class="glow"/><text x="410" y="88" text-anchor="middle" font-family="Newsreader, Georgia, serif" font-style="italic" font-weight="600" font-size="30" fill="var(--tu)">7?</text>')}
<g class="floaty">{at(700, 150, bot('ஆறு', 'var(--stone)'), ' scale(.75)')}</g>
{at(470, 400, kid('reach'), ' scale(.8)')}'''

# far 2: the thinai of Mars: a letter crosses light-minutes; someone waits in the pālai
A['mars'] = f'''<rect class="fl" x="-3000" y="400" width="7000" height="3000"/><path d="M-3000 400 Q300 360 600 400 T1400 396 V3000 H-3000Z" fill="var(--lat-d)"/>
<circle cx="230" cy="170" r="62" fill="var(--pea)"/><path d="M190 150 q20 -20 40 -6 q10 16 -10 26 q-20 4 -30 -20z M240 200 q20 -6 30 8 q-10 14 -30 -8z" fill="var(--pea-l)"/>
<circle cx="790" cy="150" r="44" fill="var(--lat)"/><circle cx="776" cy="140" r="8" fill="var(--lat-d)"/><circle cx="804" cy="166" r="5" fill="var(--lat-d)"/>
<path d="M292 170 Q520 90 746 150" stroke="var(--chalk)" stroke-width="2" stroke-dasharray="3 9" fill="none" opacity=".7"/>
<g class="crossing">{leafprop(292, 162, 44, 12)}</g>
<text class="cnt" data-count="20" data-suf=" light-minutes" x="520" y="96" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="18" fill="var(--chalk)">20 light-minutes</text>
{at(250, 400, kid_sit(), ' scale(.7)')}{at(330, 400, myna(), ' scale(.9)')}'''

# far 3: editing the flesh: a stylus writes on the strand; 'caste?' is struck out
hx = ''
for k in range(25):
    x = 220 + k*24; y1 = 230 + 50*math.sin(k*.5); y2 = 230 - 50*math.sin(k*.5)
    hx += f'<path d="M{x} {y1:.0f} V{y2:.0f}" stroke="{["var(--tu)","var(--pea-l)","var(--chalk)"][k%3]}" stroke-width="5" stroke-linecap="round"/>'
pa = 'M220 230 ' + ' '.join(f'L{220+k*6} {230+50*math.sin(k*.125):.1f}' for k in range(1, 101))
pb = 'M220 230 ' + ' '.join(f'L{220+k*6} {230-50*math.sin(k*.125):.1f}' for k in range(1, 101))
A['helix'] = f'''{FLOOR()}{hx}<path d="{pa}" stroke="var(--chalk)" stroke-width="5" fill="none"/><path d="{pb}" stroke="var(--chalk)" stroke-width="5" fill="none"/>
<g class="scribe"><path d="M0 0 L40 -90" stroke="var(--stone)" stroke-width="7" stroke-linecap="round"/><circle cx="40" cy="-90" r="6" fill="var(--stone)"/></g>
{st('pop', .3, .14, '<text x="660" y="330" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="30" font-weight="600" fill="var(--tu)">caste?</text>', '--dy:20')}
{st('drawl', .55, .12, '<path d="M600 322 h120" stroke="var(--lat)" stroke-width="6" stroke-linecap="round" pathLength="1"/>')}
{at(220, 400, kid('stand', '?'))}'''

# far 4: what is still hard: a machine lifts a boulder; the person holds a flame steady
A['hard'] = f'''{FLOOR()}
{st('pop', .05, .3, at(720, 400, f'{bot("&gt;_", "var(--chalk)")}<path d="M-70 -130 q20 -60 80 -50 q60 10 50 60 q-10 30 -70 26 q-50 -4 -60 -36z" fill="var(--stone)"/>'), '--dy:-200')}
{at(380, 400, kid_sit())}{at(470, 400, lamp(), ' scale(.6)')}
{st('pop', .55, .2, at(730, 236, myna()), '--dy:-40')}'''

# ================================================================ content
LN = {k: v for k, v in LENS}
ESS = [
 dict(key='arivu', ta='அறிவு', en='discernment', art='scale', sc='sc-e1', pick=0,
      line='See the substance of what you hear, *whoever* says it.',
      leaf=(['எப்பொருள் யார்யார்வாய்க் கேட்பினும் அப்பொருள்', 'மெய்ப்பொருள் காண்ப தறிவு'], "Whatever you hear, from whoever's mouth, understanding means seeing the true substance of that very thing.", 'kural:423'),
      lenses=[('all', 'Answers become free, so error falls.', 'Fluent answers make people stop checking, so error spreads faster.', 'The scarce skill moves from knowing to judging. Check the substance, not the speaker, now that the speaker is a machine.'),
              ('steer', 'Tools that know us can nudge us.', 'A person who tests claims is hard to nudge cheaply.', 'Steering starts with the question you bring, not the answer you get.')]),
 dict(key='pakirvu', ta='பகிர்வு', en='sharing', art='leaf', sc='sc-e2', pick=0,
      line="The world lasts because some won't *eat* *alone.*",
      leaf=(['உண்டால் அம்ம, இவ்வுலகம்; இந்திரர்;'], "This world exists because there are people who wouldn't eat even the gods' nectar alone.", 'purananuru:182 · line 1 · Ilamperuvazhuthi'),
      lenses=[('ineq', 'Whoever owns the compute owns the gains, and the gap widens.', 'The cost per answer keeps falling, so access spreads.', "Access alone doesn't close the gap; the habit of sharing does. Build commons: open models, shared data, public tutors. Count who gets fed, not how much is cooked."),
              ('all', 'Kinship at planetary scale: every town is ours.', 'Abundance can isolate, each person alone with a private oracle.', 'Use the tools to bring people to the same table, not to replace the table.')]),
 dict(key='uyirmey', ta='உயிர்மெய்', en='body and life', art='body', sc='sc-e3', pick=0,
      line='A letter only sounds when *life* joins the body.',
      leaf=(['மெய் உயிர் நீங்கின் தன் உரு ஆகும்.'], 'When life leaves the body-letter, it goes back to its own form.', 'tholkappiyam:eluttu:4:37 · our reading'),
      lenses=[('cre', 'Models can make anything that has already been made.', 'Making comes from a body that risks something, feels the work and answers for it.', 'What comes from humans is work with a stake in it: made by someone who can be hurt by it, praised for it, and held to it.'),
              ('adv', 'A bodiless voice can lie at scale, at no cost to itself.', 'So tie every voice back to an accountable body: a person or an institution.', 'Provenance and accountability: the modern form of the old question, who speaks?')]),
 dict(key='akam', ta='அகம் · புறம்', en='the inner and the outer voice', art='flats', sc='sc-e4', pick=1,
      line='The poems always ask *who* *speaks,* to whom, and who overhears.',
      leaf=(['உயிர்தவச் சிறிது காமமோ பெரிதே.'], 'Her life is so slight, and the love hanging from it so great. The friend says this, not the lover.', 'kuruntokai:18 · line 5 · Kapilar · our reading'),
      lenses=[('cre', 'A model can write the love letter or the eulogy.', "The poems care who speaks: the friend's voice is not the lover's.", 'Let tools draft, and let people sign. A feeling counts when the person who sends it means it.'),
              ('steer', 'Whoever controls the bard controls the story, as with patronage.', 'Sangam bards praised kings, and also rebuked them.', 'Keep human voices that can say no to their patrons, our new patrons included.')]),
 dict(key='alavai', ta='அளவை', en='the means of knowing', art='atom', sc='sc-e5', pick=0,
      line='Say how you know. Then *test* *it,* with controls.',
      leaf=(['ஓர் அணுத் தெய்வக் கண்ணோர் உணர்குவர்'], 'A single atom is seen only by those with divine eyes. Now an instrument shows it.', 'manimekalai:27 · line 146 · the debate of the schools'),
      lenses=[('adv', 'Persuasive machines can fake the evidence.', 'Controls and blind tests still separate signal from noise: in our blinded test 17 of 300 pairs passed, and no random control did.', 'Build institutions of testing, not just tools of telling. Follow the skeptic inside the tradition.'),
              ('all', 'Science for everyone.', 'Pseudo-science for everyone too: alchemy hype at machine speed.', 'What has to scale is the discipline of evidence, not the volume of claims.')]),
 dict(key='nilaiyamai', ta='நிலையாமை · அன்பு', en='impermanence and love', art='clock', sc='sc-e6', pick=0,
      line='Nothing here is permanent. Build what can be *corrected.*',
      leaf=(['நில்லாத வற்றை நிலையின என்றுணரும்', 'புல்லறி வாண்மை கடை'], 'To take what does not last for what lasts is the lowest kind of knowing.', 'kural:331 · our reading'),
      lenses=[('steer', "Humans can't out-compute machines.", 'The aim was never to out-compute. It is to choose what matters, and keep revising.', 'Stay ahead by setting the ends, not by racing on the means. Build things that can be corrected.'),
              ('ineq', "Love doesn't scale.", 'Care can be built into systems by people who care.', 'Love is the one thing everyone already has. Make it the measure of what the tools are for.')]),
]

MID = [
 dict(key='M1', title='When nothing is forgotten', art='sweep', reel=True,
      q='If nothing is ever forgotten, can anyone *change?*',
      qd='If every word we ever said is kept and searchable forever, can anyone be forgiven?',
      anchor=(['பொறுத்தல் இறப்பினை என்றும் அதனை', 'மறத்தல் அதனினும் நன்று'], 'To forgive a wrong is good; to forget it is better still.', 'kural:152'),
      arg='Perfect memory protects the truth.', ctr='A person must be allowed to outgrow their past.',
      ans='Design forgetting in on purpose, as a right. The Kural ranks forgetting above forgiving.'),
 dict(key='M2', title='When work is optional',
      q='When machines do the work, what is effort for?',
      anchor=(['தெய்வத்தான் ஆகா தெனினும் முயற்சிதன்', 'மெய்வருத்தக் கூலி தரும்'], 'Even where fate will not help, effort pays its wage to the body that strained.', 'kural:619'),
      arg='Freedom from toil.', ctr='Effort is how a body learns it can change things.',
      ans='Keep chosen difficulty. Effort becomes a practice, the way breath is for the Siddhars, not a wage.'),
 dict(key='M3', title='A floor no one falls through',
      q='If abundance is possible, is it a moral failure to let anyone beg?',
      anchor=(['இரந்தும் உயிர்வாழ்தல் வேண்டின் பரந்து', 'கெடுக உலகியற்றி யான்'], 'If the maker of the world meant some to live by begging, let that maker wander and perish.', 'kural:1062'),
      arg='Provide a universal floor.', ctr='A floor without dignity is still begging.',
      ans='Provision without petition, so that no one has to ask.'),
 dict(key='M4', title='The tears that wear down wealth',
      q='What if intelligence makes the powerful untouchable?',
      anchor=(['அல்லற்பட்டு ஆற்றாது அழுதகண் ணீரன்றே', 'செல்வத்தைத் தேய்க்கும் படை'], 'The tears of those who suffer past bearing are the weapon that wears down wealth.', 'kural:555'),
      arg='Power concentrates with compute.', ctr='Every age believed its rulers untouchable. Then the king in Silappathikaram canto 20 learns his error and dies of it.',
      ans='Accountability is engineered or it erodes. Systems must be able to hear the tears.'),
 dict(key='M5', title="The machine's sceptre",
      q='When algorithms judge, who answers for a wrong verdict?',
      anchor=(['யானோ அரசன் யானே கள்வன்'], 'Am I a king? I am the thief. The Pandya king, on learning his verdict was wrong.', 'silappathikaram:20 · lines 74–91'),
      ans='A judgment needs someone who can be wrong in their own body. Keep a human who carries the weight of the sceptre.'),
]
FAR = [
 dict(key='F1', title='The seventh sense', art='ladder', reel=True,
      q='What would a *seventh* sense be?',
      qd='If machines have the sixth sense, the mind, without the first five, where on the ladder do they stand?',
      anchor=(['ஒன்று அறிவதுவே உற்று அறிவதுவே', 'இரண்டு அறிவதுவே அதனொடு நாவே', 'மூன்று அறிவதுவே அவற்றொடு மூக்கே', 'நான்கு அறிவதுவே அவற்றொடு கண்ணே', 'ஐந்து அறிவதுவே அவற்றொடு செவியே', 'ஆறு அறிவதுவே அவற்றொடு மனனே'], 'One sense is touch; two adds the tongue; three the nose; four the eye; five the ear; six, the mind.', 'tholkappiyam:porul:9:27'),
      reel_lines=[0, 5],
      ans='The ladder builds up from touch. A mind with no touch may know a great deal and still be missing the first rung.'),
 dict(key='F2', title='Kin beyond the human',
      q='If machines or other species come to have inner lives, are they kin?',
      anchor=(['யாதும் ஊரே ; யாவரும் கேளிர் ;'], 'Every town is ours; everyone is kin.', 'purananuru:192 · line 1 · Kaniyan Poonkunranar'),
      arg='Widen the circle, as the poem did.', ctr="A circle can't be widened by claims alone.",
      ans='Kinship by evidence of inner life, tested with அளவை, not decided by convenience in either direction.'),
 dict(key='F3', title='The living letter without a body',
      q='If a mind can leave its body, is it still a living letter, or a vowel with nothing to sound in?',
      anchor=(['உடம்புளே உத்தமன் கோயில்கொண் டான் என்று', 'உடம்பினை யானிருந் தோம்புகின் றேனே'], 'Finding the highest had made the body its temple, I now tend the body.', 'tirumanthiram:725 · lines 3–4 · our reading'),
      ans='Keep asking what the body gave that the copy lacks. Do not assume it is nothing.'),
 dict(key='F4', title='The thinai of Mars', art='mars', reel=True,
      q='What is the poetry of a *twenty-minute* reply?',
      qd='Love across light-minutes: what is the uri of a world where an answer takes twenty minutes, or four years?',
      anchor=(['அன்பின தோழியவர் சென்ற வாறே.'], 'Even the road he took is a loving one, friend.', 'kuruntokai:37 · line 4 · pālai, the landscape of parting'),
      ans='The old grammar already has a landscape for separation. Every new world will need its own poems of waiting, and they will still be about people.'),
 dict(key='F5', title='When we can edit the flesh', art='helix', reel=True,
      q='Once we can write into the flesh, will we write *caste* there?',
      anchor=(['பறைச்சியாவது ஏதடா? பணத்தியாவது ஏதடா?', 'இறைச்சிதோல் எலும்பினும் இலக்கமிட்டு இருக்குதோ?'], 'Is a mark stamped on flesh, skin or bone?', 'siddhar:sivavakkiyam:39 · Sivavakkiyar'),
      ans="The poet's test applies in reverse. Nothing written into flesh should decide a person's worth."),
 dict(key='F6', title='What the release is from', art='hard', reel=True,
      q='When anything can be done for us, what is still *hard?*',
      anchor=(['செயற்கரிய செய்வார் பெரியர் சிறியர்', 'செயற்கரிய செய்கலா தார்'], 'The great do what is hard to do; the small cannot.', 'kural:26'),
      ans='The hard things move inward: attention, restraint, love, forgetting. The Siddhars and the Kural point the same way.'),
]

# ================================================================ the script
S = []
S.append(dict(h='## what this file is', sc='sc-a', art='title', kind='title', line='நிலை', extra='''<p class="r-sub r-mono">nilai.md · what endures</p>
<p class="r-sub">A standing place. Also, what endures. What the oldest Tamil books say to the future we're building.</p>
<p class="r-hint"><span>scroll, or press <b>watch</b></span><a class="r-skip" href="#file">skip to the text</a></p>'''))
S.append(dict(h='## what this file is', sc='sc-a', art='stack', line='Two thousand years ago, Tamil poets wrote on *palm* *leaves.*'))
S.append(dict(h='## what this file is', sc='sc-a', art='tap', line='Now intelligence is *on* *tap.*'))
S.append(dict(h='## what this file is', sc='sc-a', art='lenses', line='Six old notes, asked forward: fifty, two hundred and *five* *hundred* years.', extra='<ul class="r-lenslist">' + ''.join(f'<li>{icon(k, 22)}<span>{E(q)}</span></li>' for k, q in LENS) + '</ul>'))
for n, e in enumerate(ESS, 1):
    S.append(dict(h=f'## {n}. {e["ta"]} · {e["en"]}', sc=e['sc'], art=e['art'], line=e['line'], leaf=e['leaf'], kick=f'essence {n} · <span lang="ta" class="ta">{e["ta"]}</span>', kind=('zoomglyph' if e['art'] == 'body' else '')))
    k, arg, ctr, ans = e['lenses'][e['pick']]
    S.append(dict(h=f'### {n}. about 50 years · {LN[k]}', sc='sc-q lens-' + k, art='L-' + k, kind='whatif', lens=k,
                  q=LN[k][0].upper() + LN[k][1:], arg=arg, ctr=ctr, ans=ans, kick2='about 50 years · speculation'))
for mq in MID:
    if mq.get('reel'):
        S.append(dict(h=f'## about 200 years · {mq["title"].lower()}', sc='sc-mid', art=mq['art'], kind='whatif', lens='', q=mq['q'], qd=mq.get('qd'), arg=mq.get('arg'), ctr=mq.get('ctr'), ans=mq['ans'],
                      leaf=mq['anchor'], kick2='the middle horizon · about 200 years · speculation'))
S.append(dict(h='## about 500 years', sc='sc-turn', art='turn', line='Five hundred years on, *look* *up.*', extra='<p class="r-sub">The stage pulls back. The kolam dots were always stars.</p>', kick='the far horizon'))
far_reel = [f for f in FAR if f.get('reel')]
for fi, fq in enumerate(far_reel):
    lines, gloss, src = fq['anchor']
    if fq.get('reel_lines'): lines = [lines[i] for i in fq['reel_lines']]; gloss = 'One sense is touch … six, the mind.'
    S.append(dict(h=f'## about 500 years · {fq["title"].lower()}', sc='sc-far', art=fq['art'], kind='whatif', lens='', q=fq['q'], qd=fq.get('qd'), ans=fq['ans'],
                  leaf=(lines, gloss, src), kick2='the far horizon · about 500 years · speculation', zoomleaf=(fi == len(far_reel) - 1)))
S.append(dict(h="## things I'm trying to stop doing", sc='sc-g', kind='list', line="things I'm trying to stop doing", items=['averaging the old texts into slogans', 'trusting an answer because it sounds fluent', 'outsourcing the breath'], mode='strike'))
S.append(dict(h="## things I'm trying to do more", sc='sc-g', kind='list', line="things I'm trying to do more", items=['read the Tamil first', 'ask whose voice is speaking', 'share what I know, like food'], mode='mark'))
S.append(dict(h='## steer', sc='sc-steer', art='steerline', kind='big', line='Steer, rather than be *steered.*'))
S.append(dict(h='## this file will be wrong', sc='sc-end', art='kolam', kind='couplet', line='எல்லாம் பொறிசெய்யும் காலத்தும் அன்பெனும் செல்வமே மாந்தர் சிறப்பு', extra='''<p class="r-sub r-en">Even in an age when machines do everything, the wealth called love is what marks us human.</p>
<p class="r-sub r-mono r-src">couplet 10 · new, 2026, in the kural form · this file will be wrong. that's the deal.</p>
<p class="r-acts"><a class="r-btn r-btn-p" href="#file">read the file</a><button class="r-btn" type="button" id="watchAgain">watch again</button></p>'''))

def words(text):
    out = []
    for i, w in enumerate(text.split()):
        em = w.startswith('*')
        core = w.replace('*', '')
        out.append(f'<span class="{"r-w r-em" if em else "r-w"}" style="--i:{i}">{E(core)}</span>')
    return ' '.join(out), len(text.split())

def letters(text):
    out, i = [], 0
    for w in text.split(' '):
        sp = ''.join(f'<span class="r-l" style="--i:{i+k}">{E(ch)}</span>' for k, ch in enumerate(w))
        out.append(f'<span class="r-wd">{sp}</span>')
        i += len(w) + 1
    return ' '.join(out), len(text)

N = len(S)
secs = []
for idx, s in enumerate(S, 1):
    kind = s.get('kind', '')
    lang = ' lang="ta"' if kind in ('title', 'couplet') else ''
    kick = s.get('kick', '')
    leaf = body = qd = ''
    if kind == 'list':
        spans, cnt = letters(s['line'])
    elif kind == 'whatif':
        spans, cnt = words(s['q'])
        kick = (icon(s['lens'], 20) + ' ' if s.get('lens') else '') + s.get('kick2', '')
    else:
        spans, cnt = words(s['line'])
    hcls = {'title': ' r-ta r-title', 'couplet': ' r-ta r-couplet', 'list': ' r-listh', 'whatif': ' r-q', 'big': ' r-big'}.get(kind, '')
    if s.get('leaf'):
        lines, gloss, src = s['leaf']
        leaf = f'<figure class="r-leaf"><blockquote lang="ta">{"".join(f"<span class=tl>{l}</span>" for l in lines)}</blockquote><figcaption><span class="gl">{E(gloss)}</span><span class="src">{E(src)}</span></figcaption></figure>'
    if kind == 'whatif':
        cards = f'<div class="r-cards"><div class="r-card c1"><b>argument</b><span>{E(s["arg"])}</span></div><div class="r-card c2"><b>counter</b><span>{E(s["ctr"])}</span></div></div>' if s.get('arg') else ''
        qd = f'<p class="r-sub r-qd">{E(s["qd"])}</p>' if s.get('qd') else ''
        body = f'''{cards}
<p class="r-ans"><span class="r-pulli" aria-hidden="true"></span><b>a possible answer</b> <span>{E(s["ans"])}</span></p>'''
    if kind == 'list':
        lis = ''.join(f'<li style="--j:{j}"><span class="r-it">{E(t)}</span></li>' for j, t in enumerate(s['items']))
        tool = 'pencil' if s['mode'] == 'strike' else 'marker'
        body = f'<ol class="r-list r-{s["mode"]}">{lis}</ol><svg class="r-hand" viewBox="-10 -20 190 260" aria-hidden="true" focusable="false">{hand(tool)}</svg>'
    data = f' data-h="{E(s["h"])}"'
    if s.get('art') == 'body': data += ' data-b="2"'
    if s.get('art') in ('L-all',): data += ' data-q="9"'
    if kind == 'whatif' and not s.get('arg'): data += ' data-nocards'
    if s.get('art') in ('L-steer', 'steerline'): data += ' data-q="4"'
    if kind == 'list': data += f' data-list="{s["mode"]}"'
    cls = f'rs {s["sc"]} a-{s.get("art", "list")}' + (f' k-{kind}' if kind else '') + (' zl' if s.get('zoomleaf') else '') + (' last' if idx == N else '')
    art = ''
    if kind != 'list':
        extra_art = '<g class="zoomleaf"><rect x="470" y="220" width="60" height="16" rx="8" fill="#f7f0de"/></g>' if s.get('zoomleaf') else ''
        art = f'<svg class="r-art" viewBox="0 0 1000 500" preserveAspectRatio="xMidYMax meet" aria-hidden="true" focusable="false">{A[s["art"]]}{extra_art}</svg>'
    kicker = f'<p class="r-no"><span class="r-num">{idx:02d}/{N}</span>{(" · " + kick) if kick else ""}</p>'
    secs.append(f'''<section class="{cls}" id="r{idx}" aria-labelledby="r{idx}h"{data}>
 <div class="r-stage">{art}
  <div class="r-copy">
   {kicker}
   <h2 class="r-line{hcls}" id="r{idx}h"{lang} style="--n:{cnt}">{spans}</h2>
   {qd}{leaf}{s.get("extra", "")}{body}
  </div>
 </div>
</section>''')

reel_html = f'''
<div class="reel" id="reel" aria-label="Nilai, the reel: six old notes asked forward, in {N} scenes">
{chr(10).join(secs)}
</div>
'''

# ================================================================ "ponderings": the grid in the file tab
LK = [k for k, _ in LENS]
def cell(e, k):
    for kk, arg, ctr, ans in e['lenses']:
        if kk == k:
            return f'<td class="pd-on"><p class="pd-ans">{E(ans)}</p><details><summary>argument and counter</summary><p><b>argument</b> {E(arg)}</p><p><b>counter</b> {E(ctr)}</p></details></td>'
    return '<td class="pd-off" aria-label="not explored">·</td>'
thead = ''.join(f'<th scope="col">{icon(k, 22, "pd-ic")}<span>{E(q)}</span></th>' for k, q in LENS)
rows = ''.join(f'<tr><th scope="row"><span class="ta" lang="ta">{e["ta"]}</span><small>{E(e["en"])}</small></th>{"".join(cell(e, k) for k in LK)}</tr>' for e in ESS)
acc = ''.join(f'''<details class="pd-acc"><summary><span class="ta" lang="ta">{e["ta"]}</span> {E(e["en"])}</summary>{"".join(f'<div class="pd-item"><h4>{icon(k, 18, "pd-ic")}{E(LN[k])}</h4><p><b>argument</b> {E(arg)}</p><p><b>counter</b> {E(ctr)}</p><p class="pd-ans"><b>a possible answer</b> {E(ans)}</p></div>' for k, arg, ctr, ans in e["lenses"])}</details>''' for e in ESS)
def hcard(c, band):
    lines, gloss, src = c['anchor']
    ac = (f'<p><b>argument</b> {E(c["arg"])}</p><p><b>counter</b> {E(c["ctr"])}</p>' if c.get('arg') else '')
    return (f'<details class="pd-card" open><summary><span class="pd-k">{c["key"]}</span> {E(c["title"])}</summary>'
            f'<p class="pd-q">{E(c["q"].replace("*", ""))}</p>' + (f'<p class="pd-qd">{E(c["qd"])}</p>' if c.get('qd') else '') +
            f'<div class="verse">{"".join(f"<span class=tl>{l}</span>" for l in lines)}<span class="src">{E(src)} · {E(gloss)}</span></div>'
            f'{ac}<p class="pd-ans"><b>a possible answer</b> {E(c["ans"])}</p></details>')
pond = f"""
<section id="ponderings">
  <h2>ponderings</h2>
  <p class="honest">speculation · every answer here is a possibility, not a forecast</p>
  <p>Six essences from the books, asked forward at three distances. Each question has the same shape: the question, an argument, a counter-argument, and a possible answer rooted in the texts. Every Tamil line is copied from <code>kg/core</code> with its id.</p>
  <h3>near · about 50 years</h3>
  <p>Six essences, five questions of my own. The dots are pairs I haven't thought through yet.</p>
  <div class="pd-grid scroll" tabindex="0" role="region" aria-label="near-horizon grid, scrolls sideways"><table class="pd-t"><thead><tr><th scope="col">essence</th>{thead}</tr></thead><tbody>{rows}</tbody></table></div>
  <div class="pd-list">{acc}</div>
  <h3>middle · about 200 years</h3>
  <div class="pd-cards">{''.join(hcard(c, 'mid') for c in MID)}</div>
  <h3>far · about 500 years</h3>
  <div class="pd-cards">{''.join(hcard(c, 'far') for c in FAR)}</div>
</section>
"""

# ================================================================ splice
out = SRC
font_link = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat'
i = out.index(font_link); j = out.index('\n', i)
out = out[:j+1] + '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&display=swap">\n' + out[j+1:]
out = out.replace('</style>', css + '\n</style>', 1)
anchor = '      <b>nilai.md</b><small>நிலை</small>\n    </a>\n'
assert anchor in out
out = out.replace(anchor, anchor + '    <nav class="tabs" aria-label="View"><a href="#reel" id="tabReel">reel</a><a href="#file" id="tabFile">the file</a></nav>\n    <span class="rhead" id="reelHead" aria-hidden="true">## what this file is</span>\n', 1)
pill = '    <button class="pill" id="idxBtn"'
assert pill in out
out = out.replace(pill, '    <button class="pill" id="watchBtn" type="button" aria-pressed="false" aria-controls="reel"><span class="d" aria-hidden="true"></span><span id="watchLbl">watch</span></button>\n' + pill, 1)
idxq = '        <li><a href="#questions"><span>06</span>questions that carry through</a></li>\n'
assert idxq in out
out = out.replace(idxq, idxq + '        <li><a href="#ponderings"><span>~</span>ponderings: 50, 200 and 500 years</a></li>\n', 1)
qa = '    <li>What are we mistaking for permanent? (Kural 331)</li>\n  </ul>\n'
assert qa in out
out = out.replace(qa, qa + '  <p>Five more of my own, asked of every essence: what if everyone has it, what if it widens the gap, what if the wrong hands get it, what will creativity be, and how do we steer rather than be steered? They are laid out as a grid in <a href="#ponderings">ponderings</a>.</p>\n', 1)
yours = '<section id="yours">'
assert yours in out
out = out.replace(yours, pond.strip() + '\n\n' + yours, 1)
out = out.replace('</header>\n', '</header>\n' + reel_html, 1)
k = out.rindex('</script>')
out = out[:k+len('</script>')] + '\n<script>\n' + js + '\n</script>' + out[k+len('</script>'):]
(REPO / 'site/nilai/index.html').write_text(out, encoding='utf-8')
print('bytes', len(out.encode('utf-8')), 'scenes', N)
