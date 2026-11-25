import re, sys, json, html
src, out = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8-sig').read()
ADH = {'எழுத்ததிகாரம்': 'eluttu', 'சொல்லதிகாரம்': 'col', 'பொருளதிகாரம்': 'porul'}
# split into tokens: headings and table rows
tok = re.compile(r'<h([23])[^>]*>(.*?)</h\1>|<tr>(.*?)(?=<tr>|</table\s*>)', re.S)
adh = None; iyal = None; iyal_no = None
recs = []; issues = []
seen = {}
def clean(s):
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    return html.unescape(s)
for m in tok.finditer(t):
    if m.group(1):
        h = clean(m.group(2)).strip()
        for k, v in ADH.items():
            if k in h and 'முற்றிற்று' not in h and ('பாகம்' in h):
                adh = v; iyal = None
        mm = re.match(r'(\d+)\.\s*(.+)', h)
        if mm and adh:
            iyal_no = int(mm.group(1)); iyal = re.sub(r'\s+',' ',mm.group(2)).strip()
        if 'சிறப்புப்பாயிரம்' in h:
            adh = 'payiram'; iyal = 'சிறப்புப்பாயிரம்'; iyal_no = 0
        continue
    row = m.group(3)
    cells = re.split(r'<td[^>]*>', row)
    cells = [c for c in cells if c.strip()]
    if len(cells) < 2:
        raw = clean(cells[0]).rstrip()
        mm2 = re.search(r'\s*(\d+)$', raw)
        if not mm2:
            issues.append(f'row without number in {adh}/{iyal}: {raw[:60]!r}'); continue
        text = raw[:mm2.start()]; num = mm2.group(1)
        issues.append(f'note: {adh} iyal {iyal_no} no. {num}: number printed inline in source, split off')
    else:
        text = clean(cells[0]); num = clean(cells[1]).strip()
    lines = [re.sub(r'\s+', ' ', l).strip() for l in text.split('\n')]
    lines = [l for l in lines if l]
    if not re.fullmatch(r'\d+', num):
        issues.append(f'bad number {num!r} in {adh}/{iyal}'); continue
    n = int(num)
    if adh == 'payiram':
        # the payiram is printed in 5-line blocks numbered by line count; merge
        if recs and recs[-1]['adhikaram'] == 'payiram':
            recs[-1]['tamil'] += lines; continue
        recs.append({'id': 'tholkappiyam:payiram', 'adhikaram': 'payiram', 'iyal': iyal, 'iyal_no': 0, 'number': 0, 'tamil': lines, 'source': 'pmuni0100'}); continue
    fixed = []
    for l in lines:
        if 'மிகுதலுsம்' in l:
            l = l.replace('மிகுதலுsம்', 'மிகுதலும்'); issues.append(f'note: {adh} iyal {iyal_no} no. {n}: stray latin s removed (மிகுதலுsம் -> மிகுதலும்)')
        fixed.append(l)
    lines = fixed
    key = (adh, iyal_no)
    prev = seen.get(key, 0)
    if n != prev + 1:
        issues.append(f'{adh} iyal {iyal_no} ({iyal}): number {n} follows {prev}')
    seen[key] = n
    recs.append({'id': f'tholkappiyam:{adh}:{iyal_no}:{n}', 'adhikaram': adh, 'iyal': iyal, 'iyal_no': iyal_no, 'number': n, 'tamil': lines, 'source': 'pmuni0100'})
with open(out, 'w', encoding='utf-8') as f:
    for r in recs: f.write(json.dumps(r, ensure_ascii=False) + '\n')
from collections import Counter
c = Counter((r['adhikaram'], r['iyal_no'], r['iyal']) for r in recs)
for k, v in c.items(): print(k, v)
print(len(recs), 'records'); print('\n'.join(issues))
