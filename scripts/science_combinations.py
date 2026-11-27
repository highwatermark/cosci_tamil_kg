"""Enumerate all joint Tamil seed matches and compare with within-book/length permutations."""
import argparse
import hashlib
import importlib.util
import json
import math
import random
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("science_inquiry", HERE / "science_inquiry.py")
inquiry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inquiry)
OUT = inquiry.DATA
SEED = 20261125
# Drop short, polysemous strings and the shorter string nested in அண்டபிண்ட.
DROP = {"அணு", "கரு", "அண்ட"}
BITS = range(6)
MASKS = range(1, 64)
TESTS = [m for m in MASKS if m.bit_count() >= 2]
ALL_NAMES = ["composition", "development", "sensing", "ecological_dependence", "cosmic_scale", "pervasion_and_self"]


def load():
    vocab = json.loads((OUT / 'search_lenses.json').read_text())
    if set(vocab) != set(ALL_NAMES):
        raise ValueError("Expected the six registered lenses")
    vocab = [[(t, inquiry.folded(t)) for t in vocab[name]] for name in ALL_NAMES]
    data = []
    fingerprint = hashlib.sha256()
    seen = set()
    for ident, lines in inquiry.units():
        if ident in seen:
            raise ValueError(f"Duplicate unit ID {ident}")
        seen.add(ident)
        text = inquiry.folded(' '.join(lines))
        fingerprint.update(f"{ident}\0{text}\n".encode())
        full = narrow = 0
        for i, terms in enumerate(vocab):
            hits = [t for t,k in terms if k in text]
            if hits:
                full |= 1 << i
            if any(t not in DROP for t in hits):
                narrow |= 1 << i
        data.append((ident, len(text), full, narrow, hashlib.sha256(text.encode()).hexdigest()))
    return data, fingerprint.hexdigest()


def inclusive(hist):
    totals = [hist.get(i,0) for i in range(64)]
    for i in BITS:
        b = 1 << i
        for m in range(64):
            if not m & b:
                totals[m] += totals[m | b]
    return totals


def strata(rows, index):
    batches = defaultdict(list)
    book_counts = defaultdict(Counter)
    for r in rows:
        book = r[0].split(':')[0]
        band = math.floor(2*math.log2(max(1,r[1])))
        batches[book,band].append(r[index])
        book_counts[book][r[index]] += 1
    return batches,book_counts


def test(rows,index,reps,seed):
    rng = random.Random(seed)
    batches,books = strata(rows,index)
    observed = inclusive(Counter(r[index] for r in rows))
    expected = [0.] * 64
    simulation = [[0] * 64 for _ in range(reps)]
    for vals in batches.values():
        n=len(vals)
        counts=inclusive(Counter(vals))
        singles=[counts[1<<i] for i in BITS]
        active = [i for i,k in enumerate(singles) if k]
        if len(active)<2:
            continue
        full=(1<<n)-1
        masks=[sum(1<<i for i in ids) for k in range(2,len(active)+1) for ids in combinations(active,k)]
        for m in masks:
            expected[m] += n*math.prod(singles[i]/n for i in active if m & (1<<i))
        # Reuse intersections for each larger set.
        parents=[(m, m & (m-1), m & -m) for m in masks]
        for scores in simulation:
            sets={}
            for i in active:
                k=singles[i]
                if k==n:
                    bits=full
                else:
                    bits=sum(1<<j for j in rng.sample(range(n), min(k,n-k)))
                    if k>n//2:
                        bits ^= full
                sets[1<<i]=bits
            for m,left,right in parents:
                v=sets[left]&sets[right]
                sets[m]=v
                scores[m]+=v.bit_count()
    p={m:(1+sum(s[m]>=observed[m] for s in simulation))/(1+reps) for m in TESTS}
    return observed,expected,p,books,len(batches)


def main(reps):
    rows,digest=load()
    results=[test(rows,2,reps,SEED),test(rows,3,reps,SEED+1)]
    # Holm family-wise correction across 57 enrichment tests and both specifications.
    ordered=sorted((res[2][m],j,m) for j,res in enumerate(results) for m in TESTS)
    adjusted={}
    previous=0.
    for rank,(p,j,m) in enumerate(ordered):
        previous=max(previous,min(1,(len(ordered)-rank)*p))
        adjusted[j,m]=previous
    records=[]
    for m in MASKS:
        item=dict(mask=m,lenses=[ALL_NAMES[i] for i in BITS if m & (1<<i)])
        for j,name in enumerate(('registered','short_seeds_removed')):
            obs,exp,p,books,_=results[j]
            a=dict(inclusive=obs[m],exclusive=sum(b.get(m,0) for b in books.values()),
                   by_book={b:sum(n for k,n in h.items() if k&m==m) for b,h in books.items()
                            if any(k&m==m for k in h)})
            if m in p:
                a.update(expected=round(exp[m],4),p_enrichment=p[m],p_holm=round(adjusted[j,m],8))
            item[name]=a
        records.append(item)
    exacts=Counter(r[2] for r in rows)
    by_book=Counter(r[0].split(':')[0] for r in rows)
    experiment=dict(seed=SEED,permutations_per_spec=reps,books=len(by_book),units=len(rows),
                    normalized_input_hash=digest,strata=results[0][-1],
                    duplicate_normalized_units=len(rows)-len(set(r[-1] for r in rows)),
                    by_book=by_book,short_seeds_removed=sorted(DROP),missing_all=exacts[0],
                    multi_lens_unit_ids_by_exact_mask={
                        mask: [row[0] for row in rows if row[2] == mask]
                        for mask in TESTS if exacts[mask]
                    },
                    units_by_number_of_registered_lenses={k:sum(n for m,n in exacts.items() if m.bit_count()==k) for k in range(7)},
                    combinations=records)
    assert sum(v['registered']['exclusive'] for v in records)+exacts[0]==len(rows)
    (OUT/'combinations.json').write_text(json.dumps(experiment,ensure_ascii=False,indent=2)+'\n')
    print({k:v for k,v in experiment.items() if k not in ('combinations','by_book','multi_lens_unit_ids_by_exact_mask')})
    for r in records:
        a,b=r['registered'],r['short_seeds_removed']
        if 'p_holm' in a and (a['p_holm']<=.05 or b['p_holm']<=.05):
            print(r['lenses'],a['inclusive'],a['expected'],a['p_holm'],b['inclusive'],b['expected'],b['p_holm'])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--permutations',type=int,default=3999)
    args=parser.parse_args()
    if args.permutations<1:
        parser.error('At least one permutation required')
    main(args.permutations)
