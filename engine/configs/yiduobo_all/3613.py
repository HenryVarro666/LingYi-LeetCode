_POS = {0: (0.10, 0.50), 1: (0.32, 0.50), 2: (0.52, 0.16), 3: (0.52, 0.84), 4: (0.78, 0.84), 5: (0.92, 0.34)}
_PAL = ['blue', 'pink', 'green', 'purple', 'cyan', 'orange']


def _replay(S):
    """按已排序的 edges 回放并查集；用边权 v 和 parts 定位当前边"""
    edges, n = S['edges'], S['n']
    if 'v' not in S or 'parts' not in S:
        return -1, [], list(range(n))
    fa = list(range(n))

    def find(a):
        while fa[a] != a:
            fa[a] = fa[fa[a]]
            a = fa[a]
        return a

    ok, pbs, cur, parts = [], [], None, n
    for idx, e in enumerate(edges):
        a, b = find(e[0]), find(e[1])
        pb = parts
        if a != b:
            fa[a] = b
            parts -= 1
        ok.append(a != b)
        pbs.append((pb, parts))
        if cur is None and e[2] == S['v'] and S['parts'] in pbs[-1]:
            cur = idx
    if cur is None:
        return -1, [], list(range(n))
    fa = list(range(n))
    for e in edges[:cur + 1]:
        a, b = find(e[0]), find(e[1])
        if a != b:
            fa[a] = b
    return cur, ok[:cur + 1], [find(i) for i in range(n)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'edges' not in S or 'n' not in S:
        return
    n, edges = S['n'], S['edges']
    cur, ok, root = _replay(S)
    cv.text((x0 + 18, y0 + 4), '图（彩色 = 已合并的连通块，红色虚线 = 两端早已连通，灰色 = 还没处理）', 22, T['muted'], bold=True)
    gx0, gx1, gy0, gy1 = x0 + 50, x1 - 50, y0 + 90, y1 - 50
    P = [(gx0 + _POS[i][0] * (gx1 - gx0), gy0 + _POS[i][1] * (gy1 - gy0)) for i in range(n)]
    sizes = {}
    for r in root:
        sizes[r] = sizes.get(r, 0) + 1
    order = sorted({r for r in root if sizes[r] > 1})
    colr = {r: T[_PAL[k % len(_PAL)]] for k, r in enumerate(order)}
    for idx, (a, b, w) in enumerate(edges):
        done = idx <= cur
        if not done:
            col, wd = T['dim'], 3
        elif ok[idx]:
            col, wd = colr.get(root[a], T['green']), 7
        else:
            col, wd = T['red'], 4
        if done and not ok[idx]:
            cv.dashed(P[a], P[b], col, wd)
        else:
            cv.line([P[a], P[b]], col, wd)
        mx, my = (P[a][0] + P[b][0]) / 2, (P[a][1] + P[b][1]) / 2
        hot = idx == cur
        cv.rect((mx - 20, my - 16, mx + 20, my + 16), fill=T['yellow'] if hot else T['panel2'], outline=col, width=2, r=8)
        cv.text((mx, my), w, 22, T['bg'] if hot else T['text'], anchor='mm', bold=True)
    for i in range(n):
        fill = colr.get(root[i], T['panel2'])
        cv.rect((P[i][0] - 28, P[i][1] - 28, P[i][0] + 28, P[i][1] + 28), fill=fill, outline=T['border'], width=2, r=28)
        cv.text(P[i], i, 28, T['bg'] if root[i] in colr else T['text'], anchor='mm', bold=True)


CONFIG = dict(
    num=3613, title='最小化连通分量的最大成本', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='边权排序 · 并查集合并到 k 块',
    tags=['并查集', '难度分 1900'],
    code='''
class Solution(object):
    def minCost(self, n, edges, k):
        
        if k == n:
            return 0

        edges.sort(key=lambda d:d[2])
        fa = [x for x in range(n)]
        parts = n

        def find(fa, x):
            if fa[x] != x:
                fa[x] = find(fa, fa[x])
            return fa[x]

        for x, y, v in edges:
            fa_x = find(fa, x)
            fa_y = find(fa, y)
            if fa_x != fa_y:
                fa[fa_x] = fa_y
                parts -= 1
                if parts == k:
                    return v
''',
    call='Solution().minCost(6, [[0,1,5],[1,2,3],[2,3,4],[0,3,2],[3,4,6],[4,5,1]], 2)',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=lambda S: (f"连通块个数 `parts = {S['parts']}`，目标 `k = {S['k']}`" + ('  →  ==到了，停==' if S['parts'] == S['k'] else f"  →  还要再合并 =={S['parts'] - S['k']}== 次") if 'parts' in S and 'edges' in S else ''), h=60),
    ],
    watch=['n', 'k', ('parts', 'parts', 'green'), ('fa', 'fa', 'cyan'), 'v'],
    max_steps=110,
    captions={
        'if k == n': '`k == n`：每个点各自成块，已经满足，成本 `0`。这里 `k = {k} < n = {n}`，继续',
        'edges.sort': '==按边权升序==：想让最大边权最小，就先用小边',
        'fa = [x for x': '`fa[i]` 记录 `i` 的上级，一开始都指向自己：`n` 块',
        'parts = n': '`parts` 记录连通块个数，一开始是 `n = {n}`',
        'for x, y, v in edges': '取最小的未处理边 `({x}, {y})`，权重 `v = {v}`',
        'fa_x = find': '先找边的一端 `x = {x}` 所在块的代表（调用 `find`）',
        'fa_y = find': '再找另一端 `y = {y}` 所在块的代表',
        'if fa[x] != x': lambda S, B, r: (f"`fa[{S.x}] = {S.fa[S.x]}` ≠ `{S.x}`：还有上级，继续往上找" if S.fa[S.x] != S.x
                                          else f"`fa[{S.x}] = {S.x}`：自己就是代表"),
        'fa[x] = find(fa, fa[x])': '路径压缩：把 `x` 直接挂到代表上',
        'return fa[x]': '`x` 这一块的代表是 `{ret}`',
        'if fa_x != fa_y': lambda S, B, r: (f"`{S.fa_x} != {S.fa_y}` → 两端在不同块，这条边能把两块连起来" if S.fa_x != S.fa_y
                                            else f"`{S.fa_x} == {S.fa_y}` → 两端已经连通，这条边多余，跳过"),
        'fa[fa_x] = fa_y': '合并：`fa[{fa_x}] = {fa_y}`',
        'parts -= 1': '少了一块：`parts = {parts}`',
        'if parts == k': lambda S, B, r: (f"`parts = {S.parts} == k = {S.k}` → 块数刚好降到 k，这条边就是最后一条加入的边" if S.parts == S.k
                                          else f"`parts = {S.parts} > k = {S.k}` → 还没降到 k，继续取下一条边"),
        'return v': '最后一条加入的边权重 `{v}` 即答案：更大的边都不需要',
    },
    cards=dict(
        one_liner='边按权重从小到大加，连通块降到 k 时，最后一条边就是答案',
        complexity='时间 `O(m log m + m α(n))`，空间 `O(n)`',
        problem=['无向连通图 `n` 个点，边带权；可以删边，使连通块数最多 `k`',
                 '连通分量的成本 = 块内最大边权，无边则为 0',
                 '求所有块的最大成本的最小值',
                 '本视频：`n=6, k=2` → `4`'],
        quote='为了使得最终所有连通块中最大边权最小，在这里就可以将所有的边按权重从小到大进行排序，然后逐条加入到图中，直到图中有k个连通块为止，那么最后一条加入的边的权重即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['和 3608 一样的思路：连通性交给并查集',
              '小边优先：保留的边都不大于最后一条，最大成本才最小',
              '只有成功合并才会让 `parts` 减一，到 `k` 就返回当前权重'],
        summary=['时间 `O(m log m)` 为主（排序），空间 `O(n)`',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行',
                 '先判 `k == n`：不用合并，答案 0',
                 '`parts == k` 的判断写在成功合并之后：多余的边不会改变块数',
                 '对比灵神：同样的思路，他把并查集封装成类并维护 `cc`'],
    ),
)
