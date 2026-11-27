"""Parse site/nilai/v3_script_final.md into scene records, so every sentence, anchor and colour comes from the script verbatim."""
import re

PAL = {
    'chalk': '#F7F2E6', 'tan': '#CDAE78', 'turmeric': '#F2B21B', 'brass': '#AE7F1B',
    'indigo': '#171C45', 'grey': '#4B4D50', 'teal': '#0A5C63', 'laterite': '#9A3B21', 'kumkum': '#BE1230',
}
DARK = {'indigo', 'grey', 'teal', 'laterite', 'kumkum'}

DUR = {25: 9.0, 30: 8.0, 31: 9.0}


def _strip_md(s):
    return s.strip()


def parse(path):
    txt = open(path, encoding='utf-8').read()
    arc = txt.split('## 3. The arc')[1].split('## 4. The essence')[0]
    blocks = re.split(r'\n#### (\d\d) · ', arc)
    scenes = []
    for i in range(1, len(blocks), 2):
        n = int(blocks[i])
        body = blocks[i + 1]
        title = body.split('\n', 1)[0].strip()
        rec = {'n': n, 'title': title, 'dur': DUR.get(n, 5.2)}
        m = re.search(r'- \(a\) "(.+?)"\n', body)
        rec['sent'] = m.group(1)
        m = re.search(r'- \(b\) Header: `(.+?)`', body)
        rec['hdr'] = m.group(1)
        anc = re.findall(r'^  > (.+?) — ([\w:.\-]+)\s*$', body, re.M)
        rec['anc'] = [(a.strip(), b.strip()) for a, b in anc]
        m = re.search(r'^  Our reading: (.+)$', body, re.M)
        rec['rd'] = m.group(1).strip() if m else ''
        m = re.search(r'^- Margin(.*)$', body, re.M)
        rec['margin_raw'] = m.group(0) if m else ''
        rec['pen'], rec['hand'], rec['ink'] = _margin(rec['margin_raw'])
        m = re.search(r'^- Ledger line: \*\*(.+?)\*\*', body, re.M)
        rec['led'] = m.group(1) if m else ''
        m = re.search(r'^- Gag: (.+)$', body, re.M)
        rec['gag'] = m.group(1) if m else ''
        m = re.search(r'^- Phone: (.+)$', body, re.M)
        rec['phone'] = m.group(1) if m else ''
        m = re.search(r'^- \(d\) Colour: wall (\w+) · floor (\w+) · text (\w+) · art (\w+) \(ink\), (\w+) · accent (\w+) · strip (\w+), (\w+) letters', body, re.M)
        w, f, t, ink, col, acc, strip, letters = m.groups()
        rec.update(wall=w, floor=f, text=t, inkc=ink, col=col, acc=acc, strip=strip, letters=letters)
        rec['dark'] = w in DARK
        rec['imagined'] = 'கற்பனை' in rec['hdr']
        rec['body'] = body
        scenes.append(rec)
    assert len(scenes) == 31, len(scenes)
    for k, s in enumerate(scenes):
        assert s['n'] == k + 1
        assert s['dark'] == (s['n'] % 2 == 1), s['n']
    # the strip text of section 4
    led = re.findall(r'^\d+\. \*\*(.+?)\*\* · (.+)$', txt.split('### The ledger of what we uphold')[1].split('### The whole argument')[0], re.M)
    pencil = re.search(r'^\*(this week: .+?)\*', txt.split('### The ledger of what we uphold')[1], re.M).group(1)
    return scenes, led, pencil


def _margin(raw):
    """Return (pencil worry, hand year, later-hand ink text)."""
    if not raw:
        return '', '', ''
    pen = ''
    hand = ''
    ink = ''
    m = re.search(r'Then the hand of (\d{4}): \*(.+?)\*\s*$', raw)
    if m:
        hand, ink = m.group(1), m.group(2)
        pm = re.search(r'Margin: \*(.+?)\*', raw)
        pen = pm.group(1) if pm else ''
        return pen, hand, ink
    m = re.search(r'Margin \(hand of (\d{4})[^)]*\): \*(.+?)\*\s*$', raw)
    if m:
        return '', m.group(1), m.group(2)
    m = re.search(r'Margin: \*(.+?)\*', raw)
    if m:
        pen = m.group(1)
    if 'five pencil worries' in raw:
        pen = m.group(1) if m else ''
    return pen, hand, ink


def dated_event(ink):
    """The one-line phone margin: the sentence that opens with a year, else the last sentence."""
    if not ink:
        return ''
    sents = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])', ink)
    dated = [s for s in sents if re.match(r'^(\d{4}|By \d{4}|In \d{4}|By the \d{4}s)', s)]
    return (dated[-1] if dated else sents[-1]).strip()
