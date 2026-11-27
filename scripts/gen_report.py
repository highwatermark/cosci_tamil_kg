"""Generate docs/report/index.html from repository data. Run from repo root with python3 -I."""
import json, os, html

R = os.getcwd()
def J(p): return json.load(open(os.path.join(R, p)))
audit = J('kg/groups/all_link_audit.json')
bridges = J('kg/groups/bridges_summary.json')
thr = J('kg/science/threshold_summary.json')
S = lambda f: J(f'kg/themes/sangam_grading/{f}/scores.json')
e = html.escape

def pct(n, d): return 100.0 * n / d if d else 0.0

# ---------- chart helpers ----------
def svg_open(w, h, label):
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" role="img" aria-label="{e(label)}" class="chart" style="max-width:100%;height:auto">'

# 1. sound% by group (horizontal bars)
GN = {'ettuthogai_akam': 'Ettuthogai akam', 'ettuthogai_puram': 'Ettuthogai puram', 'ettuthogai_devotional': 'Paripadal',
      'pattupattu': 'Pattupattu', 'ethics': 'Ethics (10 works)', 'kilkanakku_akam': 'Kilkanakku akam',
      'epics_great': 'Great epics', 'epics_minor': 'Minor epics', 'devotional': 'Devotional (kept)'}
bg = sorted(audit['by_group'].items(), key=lambda kv: -kv[1]['sound_pct'])
def bar_groups():
    w, lab, top, rowh = 640, 150, 30, 30
    plotw = w - lab - 90
    h = top + rowh * len(bg) + 34
    x = lambda v: lab + plotw * v / 60.0
    s = [svg_open(w, h, 'Sound percent of graded links by group')]
    for t in range(0, 61, 10):
        s.append(f'<line x1="{x(t):.1f}" y1="{top-6}" x2="{x(t):.1f}" y2="{h-28}" class="grid"/>')
        s.append(f'<text x="{x(t):.1f}" y="{h-12}" class="tick" text-anchor="middle">{t}%</text>')
    overall = audit['summary']['sound_pct']
    for i, (k, v) in enumerate(bg):
        y = top + i * rowh
        cls = 'bar-low' if v['sound_pct'] < 20 else 'bar'
        s.append(f'<text x="{lab-8}" y="{y+15}" class="lbl" text-anchor="end">{GN[k]}</text>')
        s.append(f'<rect x="{lab}" y="{y+3}" width="{x(v["sound_pct"])-lab:.1f}" height="18" class="{cls}"/>')
        s.append(f'<text x="{x(v["sound_pct"])+6:.1f}" y="{y+16}" class="val">{v["sound_pct"]:.1f}%  <tspan class="muted">n={v["links"]:,}</tspan></text>')
    s.append(f'<line x1="{x(overall):.1f}" y1="{top-10}" x2="{x(overall):.1f}" y2="{h-28}" class="ref"/>')
    s.append(f'<text x="{x(overall)+4:.1f}" y="{top-14}" class="tick">all books {overall}%</text>')
    s.append('</svg>')
    return ''.join(s)

# 2. bridge heatmap
HG = [('ettuthogai_akam', 'Ett. akam'), ('kilkanakku_akam', 'Kil. akam'), ('ettuthogai_puram', 'Ett. puram'),
      ('pattupattu', 'Pattupattu'), ('ettuthogai_devotional', 'Paripadal'), ('ethics', 'Ethics'),
      ('devotional', 'Devotional'), ('epics_great', 'Great epics'), ('epics_minor', 'Minor epics')]
def cell(a, b):
    p = bridges['pairs'].get(f'{a}|{b}') or bridges['pairs'].get(f'{b}|{a}')
    return p
def heat():
    c, lab, top = 74, 96, 92
    n = len(HG)
    w = lab + c * n + 50
    h = top + c * n + 70
    s = [svg_open(w, h, 'Bridge matrix: sound percent for each pair of groups')]
    for j, (_, name) in enumerate(HG):
        cx = lab + j * c + c / 2
        s.append(f'<text transform="translate({cx:.0f},{top-8}) rotate(-40)" class="lbl">{name}</text>')
    for i, (a, an) in enumerate(HG):
        y = top + i * c
        s.append(f'<text x="{lab-8}" y="{y+c/2+4:.0f}" class="lbl" text-anchor="end">{an}</text>')
        for j, (b, _) in enumerate(HG):
            x0 = lab + j * c
            p = cell(a, b)
            if not p or not p['graded']:
                s.append(f'<rect x="{x0+1}" y="{y+1}" width="{c-2}" height="{c-2}" class="h-none"/>')
                s.append(f'<text x="{x0+c/2}" y="{y+c/2+4}" class="hv muted" text-anchor="middle">·</text>')
                continue
            v = pct(p['sound'], p['graded'])
            b_ = 0 if v < 15 else 1 if v < 30 else 2 if v < 45 else 3 if v < 60 else 4
            s.append(f'<rect x="{x0+1}" y="{y+1}" width="{c-2}" height="{c-2}" class="h{b_}{" diag" if a==b else ""}"/>')
            small = p['graded'] < 20
            tc = 'hi' if b_ >= 3 else 'lo'
            s.append(f'<text x="{x0+c/2}" y="{y+c/2-2}" class="hv t{tc}{" it" if small else ""}" text-anchor="middle">{v:.0f}%</text>')
            s.append(f'<text x="{x0+c/2}" y="{y+c/2+14}" class="hn t{tc}" text-anchor="middle">{p["sound"]:,}/{p["graded"]:,}</text>')
    ly = top + c * n + 20
    for k, (lo, hi_) in enumerate([(0, 15), (15, 30), (30, 45), (45, 60), (60, 100)]):
        lx = lab + k * 110
        s.append(f'<rect x="{lx}" y="{ly}" width="16" height="16" class="h{k}"/>')
        s.append(f'<text x="{lx+22}" y="{ly+13}" class="tick">{lo}{"+" if hi_==100 else "–"+str(hi_)}%</text>')
    s.append(f'<text x="{lab}" y="{ly+36}" class="tick">Italic: fewer than 20 graded links (noise). Diagonal outlined: within-group baseline.</text>')
    s.append('</svg>')
    return ''.join(s)

# 3. lessons dumbbell / step chart
r1, r2, w4 = S('round1'), S('round2'), S('wave4')
pil, w3, w5, w6 = S('pilots'), S('wave3'), S('wave5'), S('wave6')
ak1 = r1['part_a']['pooled']['within/cross group']['cross ettuthogai_akam->ethics']
ak2 = r2['part_a']['pooled']['within/cross group']['cross ettuthogai_akam->ethics']
def la(d): t = d['part_a']['pooled']['total']; return pct(t['list_adds_false'], t['list_adds_n'])
def tf(d): t = d['part_a']['pooled']['total']; return pct(t['teaches_false'], t['n'])
def gf(d): t = d['part_a']['pooled']['total']; return pct(t['gains_false'], t['gains_n'])
lessons = [
    ('Akam to Kural/ethics sound', 'higher is better', [('round 1', pct(ak1['sound'], ak1['n'])), ('round 2', pct(ak2['sound'], ak2['n']))], 'up'),
    ('Ethics list_adds failed', 'lower is better', [('pilot', la(pil['ethics'])), ('wave 3', la(w3['ethics'])), ('wave 5', la(w5['ethics']))], 'down'),
    ('Sangam teaches failed', 'lower is better', [('round 1', tf(r1)), ('round 2', tf(r2)), ('wave 4', tf(w4))], 'down'),
    ('Epic gains failed', 'lower is better', [('pilot', gf(pil['epic'])), ('wave 3', gf(w3['epic'])), ('wave 5', gf(w5['epic'])), ('wave 6*', gf(w6))], 'down'),
]
def lessons_chart():
    w, lab, top, rowh = 660, 190, 20, 60
    plotw = w - lab - 24
    h = top + rowh * len(lessons) + 30
    x = lambda v: lab + plotw * v / 100.0
    s = [svg_open(w, h, 'How four measures moved as lessons were folded into the briefs')]
    for t in range(0, 101, 20):
        s.append(f'<line x1="{x(t):.1f}" y1="{top-10}" x2="{x(t):.1f}" y2="{h-26}" class="grid"/>')
        s.append(f'<text x="{x(t):.1f}" y="{h-10}" class="tick" text-anchor="middle">{t}%</text>')
    for i, (name, note, pts, _) in enumerate(lessons):
        y = top + i * rowh + 18
        s.append(f'<text x="{lab-10}" y="{y-2}" class="lbl" text-anchor="end">{name}</text>')
        s.append(f'<text x="{lab-10}" y="{y+13}" class="tick" text-anchor="end">{note}</text>')
        xs = [x(v) for _, v in pts]
        s.append(f'<line x1="{min(xs):.1f}" y1="{y}" x2="{max(xs):.1f}" y2="{y}" class="link"/>')
        for k, (rl, v) in enumerate(pts):
            last = k == len(pts) - 1
            s.append(f'<circle cx="{x(v):.1f}" cy="{y}" r="{6 if last else 4.5}" class="{"dot-end" if last else "dot"}"/>')
        seq = '  →  '.join(f'{rl} {v:.0f}%' for rl, v in pts)
        s.append(f'<text x="{lab}" y="{y+22}" class="tick">{seq}</text>')
    s.append('</svg>')
    return ''.join(s)

# 4. stance kappa line chart
def kp(d, pair, key='kappa_stance'): return d['part_b_narrative']['pairs'][pair][key]
stance = [('pilot', kp(pil['epic'], 'proposer|g1'), kp(pil['epic'], 'proposer|g2'), kp(pil['epic'], 'g1|g2')),
          ('wave 3', kp(w3['epic'], 'proposer|g1'), kp(w3['epic'], 'proposer|g2'), kp(w3['epic'], 'g1|g2')),
          ('wave 5', kp(w5['epic'], 'proposer|g1'), kp(w5['epic'], 'proposer|g2'), kp(w5['epic'], 'g1|g2')),
          ('wave 6', kp(w6, 'proposer|g1'), kp(w6, 'proposer|g2'), kp(w6, 'g1|g2'))]
def stance_chart():
    w, h, l, r, t, b = 600, 260, 46, 160, 20, 40
    pw, ph = w - l - r, h - t - b
    X = lambda i: l + pw * i / 3
    Y = lambda v: t + ph * (1 - v)
    s = [svg_open(w, h, 'Stance kappa across epic grading runs')]
    for v in [0, .2, .4, .6, .8, 1.0]:
        s.append(f'<line x1="{l}" y1="{Y(v):.1f}" x2="{l+pw}" y2="{Y(v):.1f}" class="grid"/>')
        s.append(f'<text x="{l-6}" y="{Y(v)+4:.1f}" class="tick" text-anchor="end">{v:.1f}</text>')
    for i, row in enumerate(stance):
        s.append(f'<text x="{X(i):.1f}" y="{h-14}" class="tick" text-anchor="middle">{row[0]}</text>')
    series = [(1, 'marker vs grader 1', 'ln1'), (3, 'grader 1 vs grader 2', 'ln2')]
    for col, name, cls in series:
        pts = ' '.join(f'{X(i):.1f},{Y(row[col]):.1f}' for i, row in enumerate(stance))
        s.append(f'<polyline points="{pts}" class="{cls}" fill="none"/>')
        for i, row in enumerate(stance):
            s.append(f'<circle cx="{X(i):.1f}" cy="{Y(row[col]):.1f}" r="4" class="{cls}-dot"/>')
            dy = -9 if col == 3 else 16
            s.append(f'<text x="{X(i):.1f}" y="{Y(row[col])+dy:.1f}" class="tick" text-anchor="middle">{row[col]:.2f}</text>')
        s.append(f'<text x="{l+pw+8}" y="{Y(stance[-1][col])+4:.1f}" class="lbl">{name}</text>')
    s.append('</svg>')
    return ''.join(s)

# 5. Tholkappiyam kappa
thol = [('akam / puram', .97), ('uri (situation)', .93), ('life and body', .87), ('comparison present', .84),
        ('frame fit', .83), ('thinai', .72), ('iraicchi', .49), ('ullurai', .48), ('kurippu', .45), ('karu', .37)]
def kbar(rows, label, lines=(0.6, 0.8)):
    w, lab, top, rowh = 600, 150, 16, 26
    plotw = w - lab - 60
    h = top + rowh * len(rows) + 30
    x = lambda v: lab + plotw * v
    s = [svg_open(w, h, label)]
    for t in [0, .2, .4, .6, .8, 1.0]:
        s.append(f'<line x1="{x(t):.1f}" y1="{top-4}" x2="{x(t):.1f}" y2="{h-24}" class="{"ref" if t in lines else "grid"}"/>')
        s.append(f'<text x="{x(t):.1f}" y="{h-8}" class="tick" text-anchor="middle">{t:.1f}</text>')
    for i, (n, v) in enumerate(rows):
        y = top + i * rowh
        cls = 'bar' if v >= .6 else 'bar-low'
        s.append(f'<text x="{lab-8}" y="{y+14}" class="lbl" text-anchor="end">{n}</text>')
        s.append(f'<rect x="{lab}" y="{y+3}" width="{x(v)-lab:.1f}" height="16" class="{cls}"/>')
        s.append(f'<text x="{x(v)+6:.1f}" y="{y+15}" class="val">{v:.2f}</text>')
    s.append('</svg>')
    return ''.join(s)

# 6. science grade distribution
def sci_chart():
    cd, kd = thr['control_grade_distribution'], thr['candidate_grade_distribution']
    keys = ['0.0', '0.5', '1.0', '1.5', '2.0', '3.0']
    w, h, l, t, b = 600, 250, 46, 34, 46
    pw, ph = w - l - 20, h - t - b
    gw = pw / len(keys)
    Y = lambda v: t + ph * (1 - v / 100)
    s = [svg_open(w, h, 'Mean grade distribution, candidates against controls')]
    for v in range(0, 101, 25):
        s.append(f'<line x1="{l}" y1="{Y(v):.1f}" x2="{l+pw}" y2="{Y(v):.1f}" class="grid"/>')
        s.append(f'<text x="{l-6}" y="{Y(v)+4:.1f}" class="tick" text-anchor="end">{v}%</text>')
    for i, k in enumerate(keys):
        x0 = l + i * gw
        for j, (dist, tot, cls) in enumerate([(kd, thr['candidates_graded'], 'bar'), (cd, thr['controls_graded'], 'bar-ctl')]):
            n = dist.get(k, 0); v = pct(n, tot)
            bx = x0 + 10 + j * (gw - 20) / 2
            bw = (gw - 24) / 2
            s.append(f'<rect x="{bx:.1f}" y="{Y(v):.1f}" width="{bw:.1f}" height="{Y(0)-Y(v):.1f}" class="{cls}"/>')
            s.append(f'<text x="{bx+bw/2:.1f}" y="{Y(v)-4:.1f}" class="tick" text-anchor="middle">{n}</text>')
        s.append(f'<text x="{x0+gw/2:.1f}" y="{h-26}" class="tick" text-anchor="middle">{k}</text>')
    s.append(f'<text x="{l+pw/2:.0f}" y="{h-8}" class="tick" text-anchor="middle">mean grade over two graders (0 none … 3 specific, testable)</text>')
    s.append(f'<rect x="{l+pw-210}" y="6" width="12" height="12" class="bar"/><text x="{l+pw-193}" y="16" class="tick">candidates (300)</text>')
    s.append(f'<rect x="{l+pw-90}" y="6" width="12" height="12" class="bar-ctl"/><text x="{l+pw-73}" y="16" class="tick">controls (100)</text>')
    s.append('</svg>')
    return ''.join(s)

# 7. siddhar layers
layers = [('breath', 9, 61), ('literal', 17, 44), ('social', 5, 40), ('alchemy', 4, 25), ('consciousness', 6, 17)]
def layer_chart():
    w, lab, top, rowh = 600, 120, 16, 28
    plotw = w - lab - 120
    h = top + rowh * (len(layers) + 1) + 30
    x = lambda v: lab + plotw * v / 100
    s = [svg_open(w, h, 'Siddhar layer links: share graded sound')]
    for t in range(0, 101, 20):
        s.append(f'<line x1="{x(t):.1f}" y1="{top-4}" x2="{x(t):.1f}" y2="{h-24}" class="grid"/>')
        s.append(f'<text x="{x(t):.1f}" y="{h-8}" class="tick" text-anchor="middle">{t}%</text>')
    for i, (n, k, v) in enumerate(layers):
        y = top + i * rowh
        s.append(f'<text x="{lab-8}" y="{y+15}" class="lbl" text-anchor="end">{n}</text>')
        s.append(f'<rect x="{lab}" y="{y+3}" width="{x(v)-lab:.1f}" height="18" class="{"bar" if v>=40 else "bar-low"}"/>')
        s.append(f'<text x="{x(v)+6:.1f}" y="{y+16}" class="val">{v}%  <tspan class="muted">{k} links</tspan></text>')
    y = top + len(layers) * rowh
    s.append(f'<line x1="{x(53):.1f}" y1="{top-4}" x2="{x(53):.1f}" y2="{y+4}" class="ref"/>')
    s.append(f'<text x="{x(53)+4:.1f}" y="{y+18}" class="tick">flat marking, Siddhar to Siddhar: 53%</text>')
    s.append('</svg>')
    return ''.join(s)

# ---------- pipeline diagram ----------
def pipeline():
    W, H = 900, 400
    s = [f'<svg viewBox="0 0 {W} {H}" width="{W}" role="img" aria-label="Pipeline from ingest to explorer" class="diagram">']
    s.append('<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="arrowhead"/></marker></defs>')
    def box(x, y, w, h, title, sub, cls='node'):
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" class="{cls}"/>')
        s.append(f'<text x="{x+w/2}" y="{y+22}" class="nt" text-anchor="middle">{title}</text>')
        for k, line in enumerate(sub):
            s.append(f'<text x="{x+w/2}" y="{y+40+k*15}" class="ns" text-anchor="middle">{line}</text>')
    def arrow(x1, y1, x2, y2, cls='edge'):
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}" marker-end="url(#arr)"/>')
    # row 1
    r1y, bh, bw = 30, 78, 150
    xs = [20, 196, 372, 548, 724]
    box(xs[0], r1y, bw, bh, 'Ingest', ['Project Madurai e-texts', 'stable verse ids'])
    box(xs[1], r1y, bw, bh, 'Repair', ['sangamtamil.com diff', 'tamilvu arbitrates'])
    box(xs[2], r1y, bw, bh, 'Chapter marking', ['one brief per field set', 'Opus or Sonnet agent'], 'node accent')
    box(xs[3], r1y, bw, bh, 'Automatic check', ['book_marks.py check', 'schema, ids, copyright'])
    box(xs[4], r1y, bw + 6, bh, 'Blind packets', ['shuffled links', '+ hidden calibration'])
    for i in range(4):
        arrow(xs[i] + bw, r1y + bh / 2, xs[i + 1] - 4, r1y + bh / 2)
    # row 2 (right to left)
    r2y = 190
    box(724, r2y, 156, bh, 'Grading', ['g1 all packets', 'g2 second grader'])
    box(548, r2y, bw, bh, 'Scoring', ['kappa, calibration', 'strictest grade kept'])
    box(372, r2y, bw, bh, 'Lessons', ['weak link kinds named', 'rule added to brief'], 'node accent')
    arrow(802, r1y + bh, 802, r2y - 4)
    arrow(724, r2y + bh / 2, 548 + bw + 4, r2y + bh / 2)
    arrow(548, r2y + bh / 2, 372 + bw + 4, r2y + bh / 2)
    # feedback loop up to marking
    s.append(f'<path d="M447,{r2y} L447,{r1y+bh+4}" class="edge loop" marker-end="url(#arr)"/>')
    s.append(f'<text x="455" y="{(r2y + r1y + bh)/2 + 4}" class="ns" text-anchor="start">next wave</text>')
    # row 3
    r3y = 300
    box(548, r3y, bw, bh, 'Group graphs', ['9 groups, nodes + edges', 'bridges matrix'])
    box(372, r3y, bw, bh, 'Explorer', ['viz/index.html', 'sound links by default'])
    s.append(f'<path d="M623,{r2y+bh} L623,{r3y-4}" class="edge" marker-end="url(#arr)"/>')
    arrow(548, r3y + bh / 2, 372 + bw + 4, r3y + bh / 2)
    s.append(f'<text x="20" y="{r2y+20}" class="ns" text-anchor="start">Side tracks:</text>')
    s.append(f'<text x="20" y="{r2y+38}" class="ns" text-anchor="start">Tholkappiyam pilot (field reliability)</text>')
    s.append(f'<text x="20" y="{r2y+56}" class="ns" text-anchor="start">Siddhar layers and cipher lexicon</text>')
    s.append(f'<text x="20" y="{r2y+74}" class="ns" text-anchor="start">Science pairs with negative controls</text>')
    s.append(f'<text x="20" y="{r2y+92}" class="ns" text-anchor="start">Consciousness census (exploratory)</text>')
    s.append('</svg>')
    return ''.join(s)

# ---------- page values ----------
sm = audit['summary']
ag, cal = sm['agreement'], sm['calibration']
wm = sm['by_marker_model_wave6']

def src(*paths):
    return '<p class="src">Source: ' + ', '.join(f'<code>{e(p)}</code>' for p in paths) + '</p>'

group_rows = ''.join(
    f'<tr><td>{GN[k]}</td><td class="n">{v["links"]:,}</td><td class="n">{v["sound_pct"]:.1f}</td>'
    f'<td class="n">{v["agreement"]["kappa_sound"]:.2f}</td><td class="n">{v["calibration"]["exact_pct"]:.1f}</td></tr>'
    for k, v in bg)

strong = [json.loads(l) for l in open(os.path.join(R, 'kg/science/strong_links.jsonl'))]
from collections import Counter
fc = Counter(x['finding'].split(':', 1)[1] for x in strong)
strong_rows = ''.join(f'<tr><td><code>{e(f)}</code></td><td class="n">{n}</td></tr>' for f, n in fc.most_common())

repairs = {}
for f in ['ettuthogai', 'purananuru', 'pattupattu']:
    c = Counter()
    for l in open(os.path.join(R, f'kg/core/{f}_repairs.jsonl')):
        d = json.loads(l); c[(d.get('book') or f, d['action'])] += 1
    for (b, a), n in c.items():
        repairs.setdefault(b, {})[a] = n
rep_rows = ''.join(f'<tr><td>{b.capitalize()}</td><td class="n">{v.get("changed",0)}</td><td class="n">{v.get("kept",0)}</td></tr>'
                   for b, v in repairs.items())
rep_total = sum(v.get('changed', 0) for v in repairs.values())
flags = sum(1 for _ in open(os.path.join(R, 'kg/core/sangam_text_flags.jsonl')))

vals = dict(
    links=sm['links'], sound=sm['by_grade']['sound'], weak=sm['by_grade']['weak'], forced=sm['by_grade']['forced'],
    wrong=sm['by_grade']['wrong'], spct=sm['sound_pct'], kap=ag['kappa_sound'], exact=ag['exact_pct'],
    twice=ag['links_graded_more_than_once'], pairs=ag['grade_pairs'], cal=cal['links'], calx=cal['exact_pct'],
    stricter=cal['stricter'], lenient=cal['more_lenient'], teaches=sm['teaches_failed'],
    br_s=bridges['bridges']['sound'], br_p=bridges['bridges']['sound_pct'], within=bridges['within_all']['sound_pct'],
    op=wm['opus']['g1_sound_pct'], so=wm['sonnet']['g1_sound_pct'], ops=wm['opus']['strictest_sound_pct'], sos=wm['sonnet']['strictest_sound_pct'],
    ak1=pct(ak1['sound'], ak1['n']), ak2=pct(ak2['sound'], ak2['n']),
    st0=kp(pil['epic'], 'proposer|g2'), st1=kp(w5['epic'], 'proposer|g1'),
    rep_total=rep_total, flags=flags,
)

tpl = open(os.path.join(os.path.dirname(__file__), '..', 'docs', 'report', 'template.html')).read()
out = tpl
for k, v in vals.items():
    if isinstance(v, float):
        v = f'{v:.2f}' if v < 1 else f'{v:.1f}'
    elif isinstance(v, int):
        v = f'{v:,}'
    out = out.replace('{{' + k + '}}', str(v))
for k, fn in [('BAR_GROUPS', bar_groups), ('HEAT', heat), ('LESSONS', lessons_chart), ('STANCE', stance_chart),
              ('THOL', lambda: kbar(thol, 'Tholkappiyam pilot: kappa between two blind taggers')),
              ('SCI', sci_chart), ('LAYERS', layer_chart), ('PIPE', pipeline)]:
    out = out.replace('{{' + k + '}}', fn())
SRCS = {
 'SRC_SUMMARY': ['kg/groups/all_link_audit.json', 'kg/groups/bridges_summary.json', 'docs/corpus-summary.md', 'kg/themes/sangam_grading/round1/scores.json', 'kg/themes/sangam_grading/round2/scores.json', 'kg/themes/sangam_grading/pilots/scores.json', 'kg/themes/sangam_grading/wave5/scores.json'],
 'SRC_CORPUS': ['docs/corpus-summary.md', 'docs/corpus-groups.md'],
 'SRC_REPAIRS': ['kg/core/ettuthogai_repairs.jsonl', 'kg/core/purananuru_repairs.jsonl', 'kg/core/pattupattu_repairs.jsonl', 'kg/core/sangam_text_flags.jsonl', 'docs/ingest/ettuthogai.md', 'docs/ingest/purananuru.md'],
 'SRC_COPY': ['docs/sangam-marking-brief.md (Copyright)', 'docs/sangamtamil-review.md (Licences and terms)', '.gitignore'],
 'SRC_THOL': ['kg/themes/tholkappiyam_pilot/findings.md (Agreement with a second, blind tagger)'],
 'SRC_SCHEMA': ['docs/sangam-marking-brief.md', 'docs/ethics-marking-brief.md', 'docs/epic-marking-brief.md', 'kg/themes/sangam_grading/*/scores.json (part_b)'],
 'SRC_EVAL': ['docs/sangam-grader-brief.md', 'kg/groups/all_link_audit.json (summary)'],
 'SRC_GROUPS': ['kg/groups/all_link_audit.json (by_group, by_book)', 'docs/corpus-summary.md'],
 'SRC_BRIDGES': ['kg/groups/bridges_summary.json (pairs)', 'docs/corpus-summary.md'],
 'SRC_LESSONS': ['kg/themes/sangam_grading/{round1,round2,wave4,pilots,wave3,wave5,wave6}/scores.json (part_a pooled)', 'docs/sangam-marking-brief.md, docs/ethics-marking-brief.md, docs/epic-marking-brief.md (Lessons)'],
 'SRC_STANCE': ['kg/themes/sangam_grading/{pilots,wave3,wave5,wave6}/scores.json (part_b_narrative pairs)', 'docs/epic-marking-brief.md (Lessons)'],
 'SRC_MODELS': ['kg/groups/all_link_audit.json (by_marker_model_wave6)', 'docs/corpus-summary.md (Models and cost)', 'kg/themes/sangam_grading/wave6/scores.json'],
 'SRC_SCI': ['kg/science/README.md', 'kg/science/threshold_summary.json', 'kg/science/strong_links.jsonl'],
 'SRC_SIDDHAR': ['kg/themes/siddhar_layers/findings.md'],
 'SRC_CENSUS': ['kg/science/consciousness/census.md', 'kg/science/consciousness/combinations.md'],
 'SRC_RELATED': ['docs/methods-review-thinaikg-siddhas.md', 'docs/sangamtamil-review.md', 'output/pdf/Tamil_Research_Atlas_Project_Report.pdf'],
 'SRC_TIMELINE': ['git log'],
 'SRC_LIMITS': ['docs/corpus-summary.md (Known weak spots, Models and cost)', 'docs/link-pass-plan.md', '.gitignore'],
}
for k, v in SRCS.items():
    out = out.replace('{{' + k + '}}', src(*v))
out = out.replace('{{GROUP_ROWS}}', group_rows).replace('{{STRONG_ROWS}}', strong_rows).replace('{{REP_ROWS}}', rep_rows)
assert '{{' not in out, out[out.index('{{'):out.index('{{') + 40]
os.makedirs(os.path.join(R, 'docs/report'), exist_ok=True)
open(os.path.join(R, 'docs/report/index.html'), 'w').write(out)
print('written', len(out.encode()), 'bytes')
print({k: vals[k] for k in ['ak1', 'ak2', 'st0', 'st1', 'rep_total', 'flags']})
print('lessons', [(n, [(a, round(b, 1)) for a, b in p]) for n, _, p, _ in lessons])
print('stance', stance)
