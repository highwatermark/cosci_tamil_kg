#!/usr/bin/env python3
"""Score our Sangam marks against sangamtamil.com's knowledge graph and thinai labels.

Usage (from the repository root):
    python3 -I scripts/sangam_validate.py BOOK MARKS [MARKS ...] [options]

BOOK    our book id: akananuru, purananuru, natrinai, kurunthokai, ainkurunuru, kalithokai,
        pathitruppathu, paripadal, or one of the ten idylls (mullaippattu, kurinjippattu, ...).
MARKS   one or more of: a directory of chapter files (kg/themes/<book>/ch*.json, whose
        `verses` map verse keys to records), a JSON file (a list of records, or an object with
        `verses`), or a JSONL file of records. A record gives the verse by `id` ("akananuru:12"),
        `n`/`number`, or its key in `verses`. Read from it, when present:
          thinai                     a landscape (akam) or puram thinai, Tamil or romanized
          karu | karupporul | entities   a list of Tamil words, or of objects with `tamil`/`word`/`form`
                                         (and optionally `type`)

Options
    --site PATH      kg/sangam/site_kg.jsonl (default)
    --labels PATH    per-verse site labels; default kg/sangam/facts.jsonl. For the akam
                     anthologies outside facts.jsonl pass the crawl's _extracted/verse_labels.jsonl.
    --colophon PATH  our own text file with colophon thinai (default kg/core/BOOK.jsonl if present)
    --all-site       keep the site's noisy mentions (unlocated `line: null`, and 1-2 letter words
                     such as ஆ, மா, மை, which the site matches inside unrelated words). By default
                     they are left out of recall and do not count against precision.
    --show N         list up to N disagreeing verses for each check (default 15)
    --json PATH      also write the full result as JSON

Entity matching. A tag of ours matches a site mention in the same verse when, after removing
spaces, it equals the site's word, its root (`root`), or the form found in the line; or when one is
a prefix of the other and the shorter has at least three letters (so வேங்கை matches வேங்கைப்).
Matching is one to one. Precision = our tags matched / our tags; recall = site mentions matched /
site mentions, over verses that both sides cover (a verse is covered by the site if it appears in
its labels file or has any mention). Recall is also given per site entity type.

Thinai. Our label is compared with the site's per-verse label and, separately, with the colophon
in our own text; each comparison gets percent agreement, Cohen's kappa and a confusion matrix
(rows ours, columns theirs). Verses either side leaves blank are counted, not scored.

Standard library only. Reads the files given; writes nothing unless --json is passed.
"""
import argparse
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

THINAI = {
    'kurinji': ['kurinji', 'kurinchi', 'kurunji', 'குறிஞ்சி'],
    'mullai': ['mullai', 'முல்லை'],
    'marutham': ['marutham', 'marutam', 'marudham', 'marudam', 'மருதம்'],
    'neythal': ['neythal', 'neytal', 'neithal', 'neidhal', 'neydal', 'நெய்தல்'],
    'palai': ['palai', 'paalai', 'pālai', 'பாலை'],
    'kaikkilai': ['kaikkilai', 'kaikilai', 'கைக்கிளை'],
    'perunthinai': ['perunthinai', 'perunthinai', 'perundinai', 'பெருந்திணை'],
    'vetchi': ['vetchi', 'vetci', 'வெட்சி'],
    'karanthai': ['karanthai', 'karantai', 'கரந்தை'],
    'vanchi': ['vanchi', 'vanci', 'வஞ்சி'],
    'kanchi': ['kanchi', 'kanci', 'காஞ்சி'],
    'uzhinai': ['uzhinai', 'ulinai', 'uzhignai', 'உழிஞை'],
    'nochi': ['nochi', 'nocchi', 'நொச்சி', 'நொட்சி'],
    'thumbai': ['thumbai', 'tumbai', 'தும்பை'],
    'vaagai': ['vaagai', 'vakai', 'vagai', 'வாகை'],
    'paadaan': ['paadaan', 'padan', 'paadan', 'pataan', 'பாடாண்', 'பாடாண்திணை'],
    'pothuviyal': ['pothuviyal', 'potuviyal', 'பொதுவியல்'],
}
ALIAS = {a.lower(): k for k, names in THINAI.items() for a in names}


def norm_thinai(x):
    if not x:
        return None
    s = str(x).strip().lower()
    if s in ALIAS:
        return ALIAS[s]
    s = re.sub(r'\s*(திணை|thinai)$', '', s)
    if s in ALIAS:
        return ALIAS[s]
    for a, k in ALIAS.items():  # labels such as "பாடாண் திணை" or "kurinji (union)"
        if s.startswith(a):
            return k
    return 'other:' + s


def norm_word(w):
    return re.sub(r'[\s‌‍]', '', w or '')


def letters(w):
    """Tamil letters, counting a consonant with its vowel sign or pulli as one."""
    return len(re.findall(r'[அ-ஹ][ா-்]?', w))


def read_jsonl(path):
    with open(path, encoding='utf-8') as f:
        return [json.loads(l) for l in f if l.strip()]


def verse_no(key, rec):
    for k in ('n', 'number', 'verse', 'poem'):
        if isinstance(rec.get(k), int):
            return rec[k]
    for cand in (rec.get('id'), key):
        if cand is None:
            continue
        m = re.search(r'(?:seg)?(\d+)$', str(cand))
        if m:
            return int(m.group(1))
    return None


def entity_list(rec):
    for k in ('karu', 'karupporul', 'entities'):
        v = rec.get(k)
        if v:
            out = []
            for e in v:
                if isinstance(e, str):
                    out.append({'tamil': e, 'type': None})
                elif isinstance(e, dict):
                    w = e.get('tamil') or e.get('word') or e.get('form')
                    if w:
                        out.append({'tamil': w, 'type': e.get('type')})
            return out
    return []


def load_marks(paths, book):
    records = []
    for p in paths:
        files = sorted(glob.glob(os.path.join(p, '*.json'))) if os.path.isdir(p) else [p]
        for f in files:
            if f.endswith('.jsonl'):
                items = [(None, r) for r in read_jsonl(f)]
            else:
                with open(f, encoding='utf-8') as fh:
                    d = json.load(fh)
                if isinstance(d, list):
                    items = [(None, r) for r in d]
                elif isinstance(d.get('verses'), dict):
                    items = list(d['verses'].items())
                elif isinstance(d.get('verses'), list):
                    items = [(None, r) for r in d['verses']]
                else:
                    items = [(k, r) for k, r in d.items() if isinstance(r, dict)]
            for key, r in items:
                rid = str(r.get('id', ''))
                if r.get('book') and r['book'] != book:
                    continue
                if rid and ':' in rid and not rid.startswith(book + ':'):
                    continue
                n = verse_no(key, r)
                if n is not None:
                    records.append((n, r))
    ours = {}
    for n, r in records:
        ours[n] = {'thinai': norm_thinai(r.get('thinai')), 'karu': entity_list(r)}
    return ours


def load_site(site_path, labels_path, book, keep_noisy):
    mentions = defaultdict(list)
    for e in read_jsonl(site_path):
        for m in e['mentions']:
            if m['book'] != book:
                continue
            noisy = m.get('line') is None or letters(norm_word(e['tamil'])) <= 2
            if noisy and not keep_noisy:
                mentions[m['n']]  # the verse is still covered
                continue
            mentions[m['n']].append({'tamil': norm_word(e['tamil']), 'root': norm_word(e.get('root')),
                                     'form': norm_word(m.get('form')), 'type': e['type']})
    labels = {}
    if labels_path and os.path.exists(labels_path):
        for r in read_jsonl(labels_path):
            if r.get('book') == book:
                labels[r['n']] = norm_thinai(r.get('thinai'))
    return mentions, labels


def load_colophon(path):
    out = {}
    if path and os.path.exists(path):
        for r in read_jsonl(path):
            n = r.get('number', r.get('n'))
            if isinstance(n, int):
                out[n] = norm_thinai(r.get('thinai'))
    return out


def same(a, s):
    cands = {s['tamil'], s['root'], s['form']} - {''}
    if a in cands:
        return True
    for c in cands:
        short, long_ = (a, c) if len(a) <= len(c) else (c, a)
        if letters(short) >= 3 and long_.startswith(short):
            return True
    return False


def match(ours, site):
    used = set()
    hits = []
    for i, o in enumerate(ours):
        w = norm_word(o['tamil'])
        for j, s in enumerate(site):
            if j not in used and same(w, s):
                used.add(j)
                hits.append((i, j))
                break
    return hits


def prf(tp, n_ours, n_site):
    p = tp / n_ours if n_ours else None
    r = tp / n_site if n_site else None
    f = 2 * p * r / (p + r) if p and r else None
    return p, r, f


def kappa(pairs):
    n = len(pairs)
    if not n:
        return None
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb.get(k, 0) for k in ca) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def confusion(pairs):
    labels = sorted({a for a, _ in pairs} | {b for _, b in pairs})
    cm = Counter(pairs)
    w = max([len(l) for l in labels] + [13])
    lines = ['ours \\ theirs'.ljust(w + 2) + ' '.join(l[:8].rjust(8) for l in labels)]
    for a in labels:
        lines.append(a.ljust(w + 2) + ' '.join(str(cm[(a, b)]).rjust(8) for b in labels))
    return '\n'.join(lines)


def fmt(x):
    return '  -  ' if x is None else '%.3f' % x


def thinai_block(name, ours, theirs, show):
    pairs, blank = [], Counter()
    for n in sorted(ours):
        a = ours[n]['thinai']
        if n not in theirs:
            continue
        b = theirs[n]
        if a is None or b is None:
            blank['ours blank' if a is None else 'theirs blank'] += 1
            continue
        pairs.append((n, a, b))
    print('\n== Thinai: ours vs %s ==' % name)
    if not pairs:
        print('nothing to compare', dict(blank))
        return None
    ab = [(a, b) for _, a, b in pairs]
    agree = sum(a == b for a, b in ab) / len(ab)
    k = kappa(ab)
    print('verses compared %d, agreement %.3f, kappa %s, not scored %s' % (len(ab), agree, fmt(k), dict(blank)))
    print(confusion(ab))
    dis = [(n, a, b) for n, a, b in pairs if a != b]
    if dis:
        print('disagreements (first %d of %d):' % (min(show, len(dis)), len(dis)))
        for n, a, b in dis[:show]:
            print('  %d  ours=%s  theirs=%s' % (n, a, b))
    return {'compared': len(ab), 'agreement': agree, 'kappa': k, 'not_scored': dict(blank),
            'confusion': {'%s|%s' % key: v for key, v in Counter(ab).items()},
            'disagreements': [{'n': n, 'ours': a, 'theirs': b} for n, a, b in dis]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('book')
    ap.add_argument('marks', nargs='+')
    ap.add_argument('--site', default=os.path.join(ROOT, 'kg', 'sangam', 'site_kg.jsonl'))
    ap.add_argument('--labels', default=os.path.join(ROOT, 'kg', 'sangam', 'facts.jsonl'))
    ap.add_argument('--colophon', default=None)
    ap.add_argument('--all-site', action='store_true')
    ap.add_argument('--show', type=int, default=15)
    ap.add_argument('--json', default=None)
    a = ap.parse_args()

    ours = load_marks(a.marks, a.book)
    if not ours:
        sys.exit('no marked verses of %s found in %s' % (a.book, ' '.join(a.marks)))
    mentions, labels = load_site(a.site, a.labels, a.book, a.all_site)
    colophon = load_colophon(a.colophon or os.path.join(ROOT, 'kg', 'core', a.book + '.jsonl'))
    covered = set(mentions) | set(labels)
    result = {'book': a.book, 'verses_marked': len(ours), 'verses_site_covers': len(covered)}
    print('%s: %d verses marked by us; the site covers %d verses of this book' % (a.book, len(ours), len(covered)))

    # ---- entities
    tp = n_o = n_s = 0
    by_type = defaultdict(lambda: [0, 0])  # site type -> [matched, total]
    ours_only, site_only, per_verse = Counter(), Counter(), []
    tagged = [n for n in sorted(ours) if ours[n]['karu'] or mentions.get(n)]
    for n in tagged:
        if n not in covered:
            continue
        o, s = ours[n]['karu'], mentions.get(n, [])
        hits = match(o, s)
        tp += len(hits)
        n_o += len(o)
        n_s += len(s)
        hi, hj = {i for i, _ in hits}, {j for _, j in hits}
        for j, m in enumerate(s):
            by_type[m['type']][1] += 1
            if j in hj:
                by_type[m['type']][0] += 1
            else:
                site_only[m['root'] or m['tamil']] += 1
        for i, e in enumerate(o):
            if i not in hi:
                ours_only[norm_word(e['tamil'])] += 1
        if len(hits) < max(len(o), len(s)):
            per_verse.append((n, [norm_word(o[i]['tamil']) for i in range(len(o)) if i not in hi],
                              [s[j]['tamil'] for j in range(len(s)) if j not in hj]))
    p, r, f = prf(tp, n_o, n_s)
    print('\n== Karupporul: ours vs site mentions%s ==' % ('' if a.all_site else ' (noisy site mentions left out)'))
    print('our tags %d, site mentions %d, matched %d' % (n_o, n_s, tp))
    print('precision %s  recall %s  F1 %s' % (fmt(p), fmt(r), fmt(f)))
    for t in sorted(by_type):
        m_, tot = by_type[t]
        print('  recall on site %-12s %s  (%d/%d)' % (t, fmt(m_ / tot if tot else None), m_, tot))
    print('most frequent words only we tag:', ', '.join('%s %d' % kv for kv in ours_only.most_common(12)) or '-')
    print('most frequent site words we miss:', ', '.join('%s %d' % kv for kv in site_only.most_common(12)) or '-')
    if per_verse:
        print('verses that differ (first %d of %d): n | only ours | only site' % (min(a.show, len(per_verse)), len(per_verse)))
        for n, oo, ss in per_verse[:a.show]:
            print('  %d | %s | %s' % (n, ' '.join(oo) or '-', ' '.join(ss) or '-'))
    result['entities'] = {'ours': n_o, 'site': n_s, 'matched': tp, 'precision': p, 'recall': r, 'f1': f,
                          'recall_by_type': {t: {'matched': v[0], 'total': v[1]} for t, v in by_type.items()},
                          'ours_only': dict(ours_only), 'site_only': dict(site_only),
                          'verses': [{'n': n, 'ours_only': oo, 'site_only': ss} for n, oo, ss in per_verse]}

    # ---- thinai
    result['thinai_vs_site'] = thinai_block('site labels', ours, labels, a.show)
    result['thinai_vs_colophon'] = thinai_block('our colophon', ours, colophon, a.show)
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            json.dump(result, fh, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
