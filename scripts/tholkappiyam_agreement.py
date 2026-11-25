"""Score agreement between two Tholkappiyam pilot taggings.

Usage (from the repository root):
    python3 -I scripts/tholkappiyam_agreement.py [tags_A.json tags_B.json] [--by-book] [--disagreements FIELD]

Defaults to kg/themes/tholkappiyam_pilot/tags_A.json and tags_B.json. Standard library only.
Categorical fields get percent agreement and Cohen's kappa; set fields get mean Jaccard and the
share of verses where the two sets overlap at all (both empty counts as agreement); presence
fields are reduced to yes/no and scored like categories. Also reports, for tagger A and B
separately, how often a comparison marker's class in porul 7.12-7.16 matches the basis given.
"""
import json
import os
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PILOT = os.path.join(ROOT, 'kg', 'themes', 'tholkappiyam_pilot')
BOOKS = ['kural', 'naladiyar', 'tirumanthiram', 'thiruppugazh', 'siddhar']

# porul 7.12 (vinai), 7.14 (payan), 7.15 (mey), 7.16 (uru): the markers by class, as stems.
MARKERS = {
    'vinai': ['அன்ன', 'அனை', 'ஆங்க', 'ஆங்கு', 'மான', 'விறப்ப', 'என்ன', 'என', 'உறழ', 'தகைய', 'நோக்க'],
    'payan': ['எள்ள', 'விழைய', 'புல்ல', 'பொருவ', 'கள்ள', 'மதிப்ப', 'வெல்ல', 'வீழ'],
    'mey': ['கடுப்ப', 'ஏய்ப்ப', 'மருள', 'புரைய', 'ஒட்ட', 'ஒடுங்க', 'ஓட', 'நிகர்ப்ப'],
    'uru': ['போல', 'போல்', 'மறுப்ப', 'ஒப்ப', 'ஒத்து', 'ஒப்பு', 'காய்த்த', 'நேர', 'வியப்ப', 'நளிய', 'நந்த'],
}


def marker_class(m):
    if not m or m == 'none':
        return 'none'
    for cls, stems in MARKERS.items():
        if any(m.startswith(s) for s in stems):
            return cls
    return 'unlisted'


def present(x):
    return 'yes' if x else 'no'


def mutal_present(t):
    m = t.get('mutal')
    return present(m and (m.get('nilam') or m.get('pozhudu')))


CATEGORICAL = {
    'akam_puram': lambda t: t.get('akam_puram'),
    'frame_fit': lambda t: t.get('frame_fit'),
    'thinai': lambda t: t.get('thinai') or 'null',
    'uri': lambda t: t.get('uri') or 'null',
    'uyir_mey': lambda t: t.get('uyir_mey') or 'absent',
    'meyppadu_first': lambda t: (t.get('meyppadu') or ['none'])[0],
    'mutal_present': mutal_present,
    'mutal_negated': lambda t: present((t.get('mutal') or {}).get('negated')),
    'karu_present': lambda t: present(t.get('karu')),
    'iraicchi_present': lambda t: present((t.get('layers') or {}).get('iraicchi')),
    'kurippu_present': lambda t: present((t.get('layers') or {}).get('kurippu')),
    'ullurai_present': lambda t: present((t.get('layers') or {}).get('ullurai')),
    'has_comparison': lambda t: present(t.get('comparisons')),
}

SETS = {
    'meyppadu': lambda t: set(t.get('meyppadu') or []),
    'meyppadu_cause': lambda t: set(t.get('meyppadu_cause') or []),
    'other_states': lambda t: set(t.get('other_states') or []),
    'comparison_bases': lambda t: {c.get('basis') for c in t.get('comparisons') or []},
    'comparison_types': lambda t: {c.get('type') for c in t.get('comparisons') or []},
}


def kappa(pairs):
    n = len(pairs)
    if not n:
        return None
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    if pe == 1:
        return 1.0 if po == 1 else 0.0
    return (po - pe) / (1 - pe)


def jaccard(a, b):
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def load(path):
    with open(path, encoding='utf-8') as f:
        return {t['id']: t for t in json.load(f)}


def score(ids, A, B):
    rows = []
    for name, fn in CATEGORICAL.items():
        pairs = [(fn(A[i]), fn(B[i])) for i in ids]
        agree = sum(a == b for a, b in pairs) / len(pairs)
        k = kappa(pairs)
        rows.append((name, 'cat', agree, k))
    for name, fn in SETS.items():
        js = [jaccard(fn(A[i]), fn(B[i])) for i in ids]
        ov = [1.0 if (fn(A[i]) & fn(B[i])) or (not fn(A[i]) and not fn(B[i])) else 0.0 for i in ids]
        rows.append((name, 'set', sum(js) / len(js), sum(ov) / len(ov)))
    return rows


def print_rows(rows, n):
    print(f'  {"field":<20} {"kind":<4} {"agree/jacc":>10} {"kappa/overlap":>14}   (n={n})')
    for name, kind, a, b in rows:
        bs = '   n/a' if b is None else f'{b:6.2f}'
        print(f'  {name:<20} {kind:<4} {a:10.2f} {bs:>14}')


def marker_report(label, T):
    c = Counter()
    for t in T.values():
        for comp in t.get('comparisons') or []:
            mc = marker_class(comp.get('marker'))
            if mc in ('none', 'unlisted'):
                c[mc] += 1
            else:
                c['match' if mc == comp.get('basis') else 'mismatch'] += 1
    tot = c['match'] + c['mismatch']
    share = f'{c["match"] / tot:.2f}' if tot else 'n/a'
    print(f'  {label}: listed-marker comparisons {tot}, class matches basis {c["match"]} ({share}); '
          f'no marker {c["none"]}, unlisted marker {c["unlisted"]}')


def main(argv):
    args = [a for a in argv if not a.startswith('--')]
    by_book = '--by-book' in argv
    dis_field = None
    if '--disagreements' in argv:
        dis_field = argv[argv.index('--disagreements') + 1]
        args = [a for a in args if a != dis_field]
    pa = args[0] if len(args) > 0 else os.path.join(PILOT, 'tags_A.json')
    pb = args[1] if len(args) > 1 else os.path.join(PILOT, 'tags_B.json')
    if not os.path.exists(pb):
        sys.exit(f'missing {pb}: the second tagger has not run yet')
    A, B = load(pa), load(pb)
    ids = [i for i in A if i in B]
    missing = sorted(set(A) ^ set(B))
    if missing:
        print(f'warning: {len(missing)} ids in only one file: {missing[:10]}')
    print(f'Agreement, {os.path.basename(pa)} vs {os.path.basename(pb)}')
    print_rows(score(ids, A, B), len(ids))
    if by_book:
        groups = defaultdict(list)
        for i in ids:
            groups[i.split(':')[0]].append(i)
        for b in BOOKS:
            if groups[b]:
                print(f'\n{b}')
                print_rows(score(groups[b], A, B), len(groups[b]))
    print('\nMarker class (porul 7.12-7.16) vs basis given')
    marker_report('A', A)
    marker_report('B', B)
    if dis_field:
        fn = CATEGORICAL.get(dis_field) or SETS.get(dis_field)
        if not fn:
            sys.exit(f'unknown field {dis_field}')
        print(f'\nDisagreements on {dis_field}')
        for i in ids:
            a, b = fn(A[i]), fn(B[i])
            if a != b:
                print(f'  {i}: A={a} B={b}')


if __name__ == '__main__':
    main(sys.argv[1:])
