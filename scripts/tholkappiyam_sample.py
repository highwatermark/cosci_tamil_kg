import json, random, sys
root = sys.argv[1]
BOOKS = ['kural', 'naladiyar', 'tirumanthiram', 'thiruppugazh', 'siddhar']
out = []
rng = random.Random(7)
for b in BOOKS:
    vs = {}
    for l in open(f'{root}/kg/{b}/nodes.jsonl', encoding='utf-8'):
        r = json.loads(l)
        if r.get('type') == 'Verse' and r['id'].startswith(b + ':'):
            vs[r['id']] = r
    ids = sorted(vs, key=lambda i: int(i.split(':')[1]))
    pick = sorted(rng.sample(ids, 20), key=lambda i: int(i.split(':')[1]))
    for i in pick:
        r = vs[i]
        out.append({k: r.get(k) for k in ['id', 'tamil', 'reading', 'nuance', 'pope', 'siddhar', 'work_title', 'uncertain']})
json.dump(out, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), [o['id'] for o in out])
