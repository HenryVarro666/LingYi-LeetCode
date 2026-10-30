import json, collections, re, builtins, keyword
recs = json.load(open('uses.json'))
AUTH = ['灵茶山艾府', 'yiduobo']
CHOSEN = {'var', 'for', 'comp', 'param', 'func', 'lambda', 'attr', 'class'}
df = {a: collections.Counter() for a in AUTH}          # name -> files (author chosen)
occ = {a: collections.Counter() for a in AUTH}
roles = {a: collections.defaultdict(collections.Counter) for a in AUTH}
inits = {a: collections.defaultdict(collections.Counter) for a in AUTH}
ctxs = {a: collections.defaultdict(list) for a in AUTH}
given = {a: collections.Counter() for a in AUTH}
nfiles = collections.Counter()
for r in recs:
    a = r['author']; nfiles[a] += 1
    seen = set(); seen_g = set()
    for name, role, ctx, init in r['uses']:
        if role == 'given_param':
            if name not in seen_g:
                given[a][name] += 1; seen_g.add(name)
            continue
        if role == 'aug':
            roles[a][name]['aug'] += 1
            continue
        occ[a][name] += 1
        roles[a][name][role] += 1
        if init:
            inits[a][name][init] += 1
        if len(ctxs[a][name]) < 400:
            ctxs[a][name].append((r['num'], role, ctx))
        if name not in seen:
            df[a][name] += 1; seen.add(name)
json.dump(dict(df=df, occ=occ, roles=roles, inits=inits, given=given, nfiles=nfiles, ctxs=ctxs), open('agg.json', 'w'), ensure_ascii=False)
for a in AUTH:
    print('=====', a, nfiles[a], 'files;', len(df[a]), 'distinct names')
    for n, c in df[a].most_common(120):
        rl = roles[a][n]
        top = ','.join(f'{k}{v}' for k, v in rl.most_common(3))
        it = '; '.join(f'{k}×{v}' for k, v in inits[a][n].most_common(3))
        print(f'{n:14s} {c:5d} {c/nfiles[a]*100:5.1f}% | {top:30s} | {it}')
