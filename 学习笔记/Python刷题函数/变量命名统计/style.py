import json, collections, re, builtins, keyword
recs = json.load(open('uses.json'))
AUTH = ['灵茶山艾府', 'yiduobo']
CHOSEN = {'var', 'for', 'comp', 'param', 'func', 'lambda', 'class'}
BUILTINS = {n for n in dir(builtins) if not n.startswith('_')}
def kind(n):
    if n == '_': return 'underscore'
    if n.isupper() and len(n) > 1: return 'UPPER'
    if re.match(r'^[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]*)*$', n): return 'CapWords'
    if re.match(r'^[a-z][a-z0-9]*(?:[A-Z][a-z0-9]*)+$', n): return 'camelCase'
    if '_' in n.strip('_'): return 'snake_case'
    return 'lower'
out = {}
for a in AUTH:
    pairs = set(); total_files = 0
    shadow = collections.Counter(); amb = collections.Counter(); kinds = collections.Counter()
    lens = []
    camel_examples = collections.Counter()
    for r in recs:
        if r['author'] != a: continue
        total_files += 1
        names = {(n) for n, role, c, i in r['uses'] if role in CHOSEN}
        for n in names:
            pairs.add((r['num'], r['file'], n))
            if n in BUILTINS and n not in ('_',): shadow[n] += 1
            if n in ('l', 'O', 'I'): amb[n] += 1
    for _, _, n in pairs:
        k = kind(n); kinds[k] += 1
        if k == 'camelCase': camel_examples[n] += 1
        if k not in ('underscore',): lens.append(len(n))
    N = len(lens)
    import statistics
    res = dict(files=total_files, pairs=len(pairs), mean_len=statistics.mean(lens), median_len=statistics.median(lens),
               len1=sum(1 for x in lens if x == 1) / N, len2_3=sum(1 for x in lens if 2 <= x <= 3) / N,
               len4p=sum(1 for x in lens if x >= 4) / N, kinds={k: v / sum(kinds.values()) for k, v in kinds.items()},
               shadow=shadow.most_common(25), shadow_files=None, amb=dict(amb), camel=camel_examples.most_common(15))
    # files with any shadowing
    sf = 0
    for r in recs:
        if r['author'] != a: continue
        if any(n in BUILTINS and role in CHOSEN for n, role, c, i in r['uses']): sf += 1
    res['shadow_files'] = sf
    out[a] = res
    print('=====', a)
    for k, v in res.items():
        print(k, v)
json.dump(out, open('style.json', 'w'), ensure_ascii=False, indent=1)
