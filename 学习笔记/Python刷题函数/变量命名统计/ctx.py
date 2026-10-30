import json, sys, random, collections
A = json.load(open('agg.json'))
a = {'L': '灵茶山艾府', 'Y': 'yiduobo'}[sys.argv[1]]
k = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 8
names = sys.argv[3:] if len(sys.argv) > 2 and sys.argv[2].isdigit() else sys.argv[2:]
for n in names:
    cs = A['ctxs'][a].get(n, [])
    random.seed(1)
    seen = set(); out = []
    byfile = collections.OrderedDict()
    for num, role, c in cs:
        byfile.setdefault(num, []).append((role, c))
    files = list(byfile)
    random.shuffle(files)
    for f in files[:k]:
        r = byfile[f][:2]
        out.append(f'{f}: ' + ' || '.join(f'[{x}] {y}' for x, y in r))
    print(f'--- {n} ({len(byfile)} files)')
    print('\n'.join(out))
