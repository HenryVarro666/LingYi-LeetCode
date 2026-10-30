"""用正则统计几种惯用写法各出现在多少篇题解里，输出 idioms.json。"""
import json, re, collections
data = json.load(open('allcode.json'))
pats = {
 'BFS: head, tail = tail, len(q)': r'head, tail = tail, len\(q\)',
 'BFS: l, r = r, len(q)': r'\bl, r = r, len\(q\)',
 'BFS: tmp = q; q = []': r'tmp = q\s*\n\s*q = \[\]',
 'BFS: .popleft()': r'\.popleft\(\)',
 'BFS: for _ in range(len(q))': r'for _ in range\(len\(q\)\)',
 'grid: x = nowx + dx[': r'= nowx \+ dx\[',
 'grid: for x, y in (i, j': r'for x, y in \(i[ ,+-]',
 'grid: for i, j in (x, y': r'for i, j in \(x[ ,+-]',
 'grid: for dx, dy in DIRS': r'for dx, dy in DIRS',
 'tree dfs(x, fa)': r'def dfs\(x[:,][^)]*\bfa\b',
 'tree dfs(now, fa)': r'def dfs\((self, )?now, fa\b',
 'for y in g[x]': r'for y(, \w+)? in g\[x\]',
 'for next in g[now]': r'for next(, \w+)? in g(\.get)?[\[(]now',
 'for nxt in g[now]': r'for nxt(, \w+)? in g(\.get)?[\[(]now',
 'res[0] mutable': r'\bres\[0\]',
 'nonlocal': r'\bnonlocal\b',
 'self.res': r'self\.res\b',
 'max = lambda': r'(?m)^\s*max = lambda',
 'min = lambda': r'(?m)^\s*min = lambda',
 'f = [None]*': r'\bf = \[+None\]',
 '@cache': r'@cache|@lru_cache',
 'x.get(k, 0) + 1': r'(\w+)\[(\w+)\] = \1\.get\(\2, 0\) \+ 1',
 'cnt[x] += 1': r'\bcnt\[\w+\] \+= 1',
}
res = {a: collections.Counter() for a in ['灵茶山艾府', 'yiduobo']}
for r in data:
    code = '\n'.join(r['code'])
    for k, p in pats.items():
        if re.search(p, code):
            res[r['author']][k] += 1
for k in pats:
    print(f'{k:36s} 灵神 {res["灵茶山艾府"][k]:5d}  yiduobo {res["yiduobo"][k]:5d}')
json.dump(res, open('idioms.json', 'w'), ensure_ascii=False)
