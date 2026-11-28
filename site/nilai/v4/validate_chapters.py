"""Check site/nilai/v4/chapters.json against the graph, independently of chapters_curate.py.

Run:  python3 -I site/nilai/v4/validate_chapters.py

Hard checks (exit 1 on any failure):
  - every Tamil line shown is a whole line of kg/core, verbatim, at the line number given; at most 4 per verse
  - every reading is the graph node's reading, verbatim, and the uncertain flag is the node's
  - every link exists in kg/groups/bridges.jsonl or kg/groups/all_link_audit.json, is graded sound wherever it is
    recorded, and its text is verbatim the field it names (teaches only where teaches_holds is true)
  - no verse is used twice; each chapter has 3 verses from at least 2 groups and 2 links among them
  - every asset named exists in site/nilai/assets/web; every new image has a prompt on #00FF00
  - the forward beat is at most 2 sentences and is labelled imagined
Soft checks (reported, not failed): verses whose concepts fall outside the chapter's category; readings that differ
from a theme-mark reading keyed to the same verse; accent contrast on the stone neutrals.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
KG = REPO / 'kg'
FAIL, WARN, OK = [], [], []


def jsonl(p):
    with open(p, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


data = json.load(open(HERE / 'chapters.json', encoding='utf-8'))
chapters = data['chapters']

# ---- graph nodes and concepts ------------------------------------------------------------------------------
index = json.load(open(KG / 'groups' / 'index.json', encoding='utf-8'))
node_files = {}
for g, v in index.items():
    if v.get('nodes'):
        node_files[REPO / v['nodes']] = g
    for b, p in (v.get('kept_graphs') or {}).items():
        node_files[REPO / p / 'nodes.jsonl'] = g
want = {v['id'] for c in chapters for v in c['verses']}
nodes, concepts = {}, {}
for f, g in node_files.items():
    for d in jsonl(f):
        if d.get('id') in want and d.get('type') == 'Verse' and d['id'] not in nodes:
            nodes[d['id']] = dict(d, _group=g, _file=f)
    for e in jsonl(f.parent / 'edges.jsonl'):
        if e['p'] == 'EXPRESSES' and e['s'] in want and nodes.get(e['s'], {}).get('_file') == f:
            concepts.setdefault(e['s'], []).append(e['o'].replace('concept:', ''))
cc = json.load(open(KG / 'themes' / 'concept_categories.json', encoding='utf-8'))
cat_of, also_of = {}, {}
for c in cc['categories']:
    for s in c['subthemes']:
        for k in s['concepts']:
            cat_of[k] = c['id']
        for k in s['also']:
            also_of.setdefault(k, set()).add(c['id'])


# ---- kg/core lookup -----------------------------------------------------------------------------------------
_core_cache = {}


def core_file(name):
    if name not in _core_cache:
        p = KG / 'core' / (name + '.jsonl')
        _core_cache[name] = list(jsonl(p)) if p.exists() else []
    return _core_cache[name]


def core_lines(vid):
    """Return {line_number: text} for the verse, from kg/core."""
    book, rest = vid.split(':', 1)
    n = nodes[vid]
    if book in ('kural', 'naladiyar'):
        rec = next(d for d in core_file(book) if d.get('verse') == int(rest))
        return {i + 1: t for i, t in enumerate(rec['tamil'])}, 'kg/core/%s.jsonl verse %s' % (book, rest)
    if book == 'siddhar':
        rec = next(d for d in core_file('siddhar') if d.get('seq') == int(rest))
        return {i + 1: t for i, t in enumerate(rec['tamil'])}, 'kg/core/siddhar.jsonl seq %s' % rest
    for name in (book + '_units', book):
        rec = next((d for d in core_file(name) if d.get('id') == vid), None)
        if rec:
            s = rec.get('start') or 1
            return {s + i: t for i, t in enumerate(rec['tamil'])}, 'kg/core/%s.jsonl id %s' % (name, vid)
    rid = n.get('record') or vid
    rec = next((d for d in core_file(book) if d.get('id') == rid), None)
    if rec is None:
        return None, 'not found'
    return {i + 1: t for i, t in enumerate(rec['tamil'])}, 'kg/core/%s.jsonl id %s' % (book, rid)


# ---- links --------------------------------------------------------------------------------------------------
bridges = list(jsonl(KG / 'groups' / 'bridges.jsonl'))
audit = json.load(open(KG / 'groups' / 'all_link_audit.json', encoding='utf-8'))['links']
group_edges = {}
for f in node_files:
    for e in jsonl(f.parent / 'edges.jsonl'):
        if 'note' in e or 'teaches' in e:
            group_edges[(e['s'], e['o'], e['p'].lower())] = e


def check_link(cid, L, verse_ids):
    s, o, typ = L['true_direction']['s'], L['true_direction']['o'], L['type']
    if {L['from'], L['to']} != {s, o}:
        FAIL.append('%s: link %s-%s walk ends differ from its recorded ends' % (cid, L['from'], L['to']))
    if not {s, o} <= set(verse_ids):
        FAIL.append('%s: link %s-%s joins a verse outside the chapter' % (cid, s, o))
    b = [x for x in bridges if x['s'] == s and x['o'] == o and x['type'] == typ]
    a = [x for x in audit if x['a'] == s and x['b'] == o and x['type'] == typ]
    if not b and not a:
        FAIL.append('%s: link %s -> %s (%s) is in neither bridges.jsonl nor all_link_audit.json' % (cid, s, o, typ))
        return
    for x in b:
        if x['grade'] != 'sound':
            FAIL.append('%s: link %s -> %s graded %s in bridges.jsonl' % (cid, s, o, x['grade']))
    for x in a:
        if x['grade'] != 'sound':
            FAIL.append('%s: link %s -> %s graded %s in all_link_audit.json' % (cid, s, o, x['grade']))
    if L['grade'] != 'sound':
        FAIL.append('%s: link %s -> %s carries grade %s' % (cid, s, o, L['grade']))
    src = b[0] if b else group_edges.get((s, o, typ), {})
    holds = b[0].get('teaches_holds') if b else a[0].get('teaches_holds')
    field = L['text_field']
    if src.get(field) != L['text']:
        FAIL.append('%s: link %s -> %s %s text is not verbatim' % (cid, s, o, field))
    if field == 'teaches' and holds is not True:
        FAIL.append('%s: link %s -> %s uses teaches but teaches_holds is %s' % (cid, s, o, holds))
    if field == 'note' and src.get('teaches') and holds is True:
        WARN.append('%s: link %s -> %s uses note though a holding teaches exists' % (cid, s, o))
    where = ('bridges.jsonl' if b else '') + (' + all_link_audit.json' if a else '')
    OK.append('%s: %s -> %s %s sound [%s], text = %s' % (cid, s, o, typ, where.strip(' +'), field))


# ---- run ----------------------------------------------------------------------------------------------------
seen = {}
if len(chapters) != 13:
    FAIL.append('expected 13 chapters, found %d' % len(chapters))
for ch in chapters:
    cid = ch['id']
    vids = [v['id'] for v in ch['verses']]
    if len(vids) != 3 or len(ch['links']) != 2:
        FAIL.append('%s: needs 3 verses and 2 links' % cid)
    for v in ch['verses']:
        vid = v['id']
        if vid in seen:
            FAIL.append('%s: verse %s already used in %s' % (cid, vid, seen[vid]))
        seen[vid] = cid
        n = nodes.get(vid)
        if not n:
            FAIL.append('%s: %s not a verse node in the graph' % (cid, vid))
            continue
        # Tamil
        lines, where = core_lines(vid)
        if lines is None:
            FAIL.append('%s: %s not found in kg/core' % (cid, vid))
        else:
            if len(v['lines']) > 4:
                FAIL.append('%s: %s shows %d lines' % (cid, vid, len(v['lines'])))
            for ln in v['lines']:
                if lines.get(ln['n']) != ln['ta']:
                    FAIL.append('%s: %s line %s is not verbatim kg/core (%s)' % (cid, vid, ln['n'], where))
            s0 = n.get('start') or 1
            if [lines.get(s0 + i) for i in range(len(n['tamil']))] != n['tamil']:
                FAIL.append('%s: %s graph node Tamil differs from kg/core' % (cid, vid))
        # reading
        if v['reading'] != n.get('reading'):
            FAIL.append('%s: %s reading is not the graph reading' % (cid, vid))
        if v['uncertain'] != bool(n.get('uncertain')):
            FAIL.append('%s: %s uncertain flag differs from the graph' % (cid, vid))
        if v['group'] != n['_group']:
            FAIL.append('%s: %s group differs' % (cid, vid))
        # theme-mark cross-check where a mark keys the verse
        book = vid.split(':')[0]
        tdir = KG / 'themes' / book
        if tdir.is_dir() and n.get('chapter') is not None:
            key_full, key_num = vid, vid.split(':', 1)[1]
            for p in sorted(tdir.glob('ch*.json')):
                m = json.load(open(p, encoding='utf-8')).get('verses', {})
                hit = m.get(key_full) or m.get(key_num)
                if hit and hit.get('reading'):
                    if hit['reading'] != v['reading']:
                        WARN.append('%s: %s reading differs from %s' % (cid, vid, p.relative_to(REPO)))
                    break
        # category
        cs = concepts.get(vid, [])
        strict = [c for c in cs if cat_of.get(c) == cid]
        loose = [c for c in cs if cid in also_of.get(c, ())]
        if not strict:
            WARN.append('%s: %s expresses no %s concept (concepts: %s%s)' % (
                cid, vid, cid, ', '.join(cs), '; secondary: ' + ', '.join(loose) if loose else ''))
        # image
        if v.get('asset'):
            if not (REPO / 'site' / 'nilai' / 'assets' / 'web' / (v['asset'] + '.webp')).exists():
                FAIL.append('%s: asset %s missing' % (cid, v['asset']))
        elif '#00FF00' not in (v.get('prompt') or ''):
            FAIL.append('%s: %s has neither an asset nor a #00FF00 prompt' % (cid, vid))
        if not v.get('object'):
            WARN.append('%s: %s names no concrete object (%s)' % (cid, vid, v.get('image_note', '')))
    groups = {v['group'] for v in ch['verses']}
    books = {v['book'] for v in ch['verses']}
    if len(groups) < 2:
        FAIL.append('%s: verses from only %d group' % (cid, len(groups)))
    if len(groups) < 3:
        WARN.append('%s: %d groups (%s), not 3' % (cid, len(groups), ', '.join(sorted(groups))))
    if len(books) < 3:
        WARN.append('%s: two verses from one book (%s)' % (cid, ', '.join(sorted(books))))
    for L in ch['links']:
        check_link(cid, L, vids)
    # the walk must be connected
    ends = [frozenset((L['from'], L['to'])) for L in ch['links']]
    if len(set().union(*ends)) != 3:
        FAIL.append('%s: the two links do not join all three verses' % cid)
    fw = ch['forward']
    if len(re.findall(r'[.?!](?:\s|$)', fw['text'])) > 2:
        FAIL.append('%s: forward beat has more than 2 sentences' % cid)
    if 'imagined' not in fw['label']:
        FAIL.append('%s: forward beat not labelled imagined' % cid)
    for side in ('then', 'future'):
        x = fw[side]
        if x.get('asset') and not (REPO / 'site' / 'nilai' / 'assets' / 'web' / (x['asset'] + '.webp')).exists():
            FAIL.append('%s: forward %s asset %s missing' % (cid, side, x['asset']))
        if not x.get('asset') and '#00FF00' not in (x.get('prompt') or ''):
            FAIL.append('%s: forward %s has no asset or prompt' % (cid, side))

# accent contrast on the prototype's stone neutrals
PAL = {'wall': '#e6e1d8', 'floor': '#d5ccbe', 'col': '#efebe4'}


def lum(hx):
    c = [int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


for ch in chapters:
    worst = min((max(lum(ch['accent']), lum(b)) + 0.05) / (min(lum(ch['accent']), lum(b)) + 0.05) for b in PAL.values())
    if worst < 4.5:
        FAIL.append('%s: accent %s reaches only %.2f:1 on the stone neutrals' % (ch['id'], ch['accent'], worst))

books = sorted({v['book'] for c in chapters for v in c['verses']})
groups = sorted({v['group'] for c in chapters for v in c['verses']})
new_imgs = sorted({x['new_image'] for c in chapters for x in c['verses'] + [c['forward']['then'], c['forward']['future']] if x.get('new_image')})
print('links checked:')
for m in OK:
    print('  ok  ', m)
print('\nspread: %d verses, %d books, %d groups; %d new images' % (len(seen), len(books), len(groups), len(new_imgs)))
print('  books:', ', '.join(books))
if WARN:
    print('\nnotes (compromises, not failures):')
    for m in WARN:
        print('  -', m)
if FAIL:
    print('\nVALIDATION FAILED:')
    for m in FAIL:
        print('  x', m)
    sys.exit(1)
print('\nVALIDATION PASSED: every Tamil line matches kg/core, every link is sound and in the data, every reading matches the graph.')
