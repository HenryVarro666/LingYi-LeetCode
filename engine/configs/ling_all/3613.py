_POS = {0: (0.10, 0.50), 1: (0.32, 0.50), 2: (0.52, 0.16), 3: (0.52, 0.84), 4: (0.78, 0.84), 5: (0.92, 0.34)}
_PAL = ['blue', 'pink', 'green', 'purple', 'cyan', 'orange']


def _replay(S):
    """按已排序的 edges 回放并查集：返回 (已处理边数, 每条已处理边是否合并成功, 代表元表)"""
    edges, n = S['edges'], S['n']
    cur = None
    a0, b0 = S.get('from_', S.get('x')), S.get('to', S.get('y'))
    if 'w' in S and [a0, b0, S['w']] in edges:
        cur = edges.index([a0, b0, S['w']])
    if cur is None:
        return -1, [], list(range(n))
    fa = list(range(n))

    def find(a):
        while fa[a] != a:
            fa[a] = fa[fa[a]]
            a = fa[a]
        return a

    ok = []
    for e in edges[:cur + 1]:
        a, b = find(e[0]), find(e[1])
        ok.append(a != b)
        if a != b:
            fa[a] = b
    return cur, ok, [find(i) for i in range(n)]


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
    author='灵茶山艾府', technique='并查集 · 从小到大合并',
    tags=['并查集', '难度分 1900'],
    code='''
# 完整的并查集模板，见我的数据结构题单
class UnionFind:
    def __init__(self, n: int):
        # 一开始有 n 个集合 {0}, {1}, ..., {n-1}
        # 集合 i 的代表元是自己，大小为 1
        self._fa = list(range(n))  # 代表元
        self.cc = n  # 连通块个数

    # 返回 x 所在集合的代表元
    # 同时做路径压缩，也就是把 x 所在集合中的所有元素的 fa 都改成代表元
    def find(self, x: int) -> int:
        # 如果 fa[x] == x，则表示 x 是代表元
        if self._fa[x] != x:
            self._fa[x] = self.find(self._fa[x])  # fa 改成代表元
        return self._fa[x]

    # 把 from 所在集合合并到 to 所在集合中
    def merge(self, from_: int, to: int) -> None:
        x, y = self.find(from_), self.find(to)
        if x == y:  # from 和 to 在同一个集合，不做合并
            return
        self._fa[x] = y  # 合并集合。修改后就可以认为 from 和 to 在同一个集合了
        self.cc -= 1  # 成功合并，连通块个数减一

class Solution:
    def minCost(self, n: int, edges: List[List[int]], k: int) -> int:
        if k == n:
            return 0
    
        edges.sort(key=lambda e: e[2])
        u = UnionFind(n)
        for x, y, w in edges:
            u.merge(x, y)
            if u.cc == k:
                return w
''',
    call='Solution().minCost(6, [[0,1,4],[1,2,3],[1,3,2],[2,3,2],[3,4,6],[4,5,1]], 2)',
    expect=4,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='text', fn=lambda S: (f"连通块个数 `cc = {S['u'].cc}`，目标 `k = {S['k']}`" + ('  →  ==到了，停==' if S['u'].cc == S['k'] else f"  →  还要再合并 =={S['u'].cc - S['k']}== 次") if 'u' in S and 'edges' in S else ''), h=60),
    ],
    watch=['n', 'k', ('cc', lambda S: S['u'].cc if 'u' in S else (S['self'].cc if 'self' in S and hasattr(S['self'], 'cc') else ''), 'green'), 'x', 'y', 'w'],
    max_steps=110,
    skip=['self._fa = list(range(n))'],
    captions={
        'if k == n': '`k == n`：每个点单独一块就已经满足，不用合并，成本 0。这里 `k = {k} < n = {n}`，继续',
        'edges.sort': '==按边权从小到大排序==：先合并小边，最大边权才会尽量小',
        'u = UnionFind': '建并查集：开始 `n = {n}` 个点各自一块，`cc = n`',
        'for x, y, w in edges': '取下一条最小的边 `({x}, {y})`，边权 `w = {w}`',
        'u.merge(x, y)': '尝试把 `{x}` 和 `{y}` 所在的两块合并',
        'x, y = self.find': '先分别找 `{from_}` 和 `{to}` 的代表元（两次 `find`），看它们是不是同一块',
        'if x == y': lambda S, B, r: (f"代表元相同 `{S.x} == {S.y}` → 早已连通，这条边==不用合并==（连通块数不变）" if S.x == S.y
                                      else f"代表元不同 `{S.x} != {S.y}` → 两块分开，可以合并"),
        'self._fa[x] = y': '合并：`fa[{x}] = {y}`，两块变成一块',
        'self.cc -= 1': '成功合并，连通块个数减一：`cc = {self.cc}`',
        'if self._fa[x] != x': lambda S, B, r: (f"`fa[{S.x}] = {S['self']._fa[S.x]}` ≠ `{S.x}`：`{S.x}` 不是代表元，要往上找" if S['self']._fa[S.x] != S.x
                                                else f"`fa[{S.x}] = {S.x}`：指向自己，`{S.x}` 就是代表元"),
        'self._fa[x] = self.find': '路径压缩：递归找到代表元后，把 `fa[x]` 直接改成它，下次一步到位',
        'return self._fa[x]': '`{x}` 所在集合的代表元是 `{ret}`',
        'if u.cc == k': lambda S, B, r: (f"`cc = {S.u.cc} == k = {S.k}` → 刚好剩 `k` 块，当前边权 `{S.w}` 就是最大成本" if S.u.cc == S.k
                                         else f"`cc = {S.u.cc} > k = {S.k}` → 块数还多，继续合并下一条小边"),
        'return w': '合并边权都不超过 `{w}`，更大的边没必要合并 → 答案 ==`{w}`==',
    },
    cards=dict(
        one_liner='从小到大合并边，连通块数减到 k 时，最后一条边就是答案',
        complexity='时间 `O(m log m + m log n)`，空间 `O(n)`',
        problem=['无向连通图，`n` 个点，边带权，可以删任意多条边',
                 '要求剩下最多 `k` 个连通块，块的成本 = 块内最大边权',
                 '求所有块成本的最大值的最小值',
                 '本视频：`n=6, k=2` → `4`'],
        quote='为了最小化答案，我们可以用并查集从小到大合并，直到连通块个数等于 k 为止。……合并更大的边权是没有意义的，因为小于等于最大边权的边我们都能合并。',
        quote_src='—— 灵茶山艾府题解',
        idea=['答案是某条边的权值：小于等于它的边都留着，更大的边全删掉',
              '边权越小越优，所以==按边权升序==用并查集合并',
              '块数从 `n` 降到 `k` 的那一刻停下，当前边权就是答案'],
        summary=['时间 `O(m log m + m log n)`，瓶颈是排序；空间 `O(n)`',
                 '先判断 `k == n`：不合并，成本为 0',
                 '同一块内的边 `merge` 直接返回，`cc` 不减',
                 '题解说明：和 3608 几乎同一份代码；也可以二分答案',
                 '并查集模板见灵神数据结构题单「七、并查集」'],
    ),
)
