import json, sys, re, random
data = json.load(open('allcode.json'))
a = {'L': '灵茶山艾府', 'Y': 'yiduobo'}[sys.argv[1]]
pat = sys.argv[2]; nf = int(sys.argv[3]) if len(sys.argv) > 3 else 3; nl = int(sys.argv[4]) if len(sys.argv) > 4 else 14
rx = re.compile(pat)
cands = [r for r in data if r['author'] == a and any(rx.search(c) for c in r['code'])]
random.seed(7); random.shuffle(cands)
print(f'# {len(cands)} files match')
for r in cands[:nf]:
    for c in r['code']:
        if rx.search(c):
            L = c.splitlines()
            idx = [i for i, l in enumerate(L) if rx.search(l)]
            lo = max(0, idx[0] - 3); hi = min(len(L), lo + nl)
            print(f'== {r["num"]} {r["title"]}')
            print('\n'.join(L[lo:hi]))
            break
