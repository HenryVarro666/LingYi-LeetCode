CODE = '''
class UnionFind:
    def __init__(self, n: int):
        # 一开始有 n 个集合 {0}, {1}, ..., {n-1}
        # 集合 i 的代表元是自己
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
    # 返回是否合并成功
    def merge(self, from_: int, to: int) -> bool:
        x, y = self.find(from_), self.find(to)
        if x == y:  # from 和 to 在同一个集合，不做合并
            return False
        self._fa[x] = y  # 合并集合。修改后就可以认为 from 和 to 在同一个集合了
        self.cc -= 1  # 成功合并，连通块个数减一
        return True

class Solution:
    def maxStability(self, n: int, edges: List[List[int]], k: int) -> int:
        uf = UnionFind(n)
        all_uf = UnionFind(n)
        min_s1 = inf
        for x, y, s, must in edges:
            if must:
                if not uf.merge(x, y):  # 必选边成环
                    return -1
                min_s1 = min(min_s1, s)
            all_uf.merge(x, y)

        if all_uf.cc > 1:  # 图不连通
            return -1

        left = uf.cc - 1
        if left == 0:  # 只需选必选边
            return min_s1

        # Kruskal 求最大生成树
        edges.sort(key=lambda e: -e[2])
        ans = min_s1
        for x, y, s, must in edges:
            if not must and uf.merge(x, y):
                ans = min(ans, s if left > k else s * 2)
                left -= 1
                if left == 0:  # 已经得到生成树了
                    break
        return ans
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(sub):
    return next(i + 1 for i, t in enumerate(_LINES) if sub in t)


L_SORT = _ln('edges.sort')
L_MERGE2 = _ln('if not must and uf.merge(x, y)')
PAL = ['cyan', 'orange', 'pink', 'green', 'purple', 'yellow']


def _sim(S):
    """返回 (processed, chosen, rejected, comps) —— 按当前进度在 edges 上重放"""
    edges, n = S['edges'], S['n']
    fa = list(range(n))

    def fd(a):
        while fa[a] != a:
            a = fa[a]
        return a

    stage2 = 'left' in S and S['_line'] >= L_SORT
    cur = [S['x'], S['y'], S['s'], S['must']] if 'x' in S else None
    idx = None
    if cur is not None:
        idx = next((i for i, e in enumerate(edges) if list(e) == cur), None)
    chosen, rej = set(), set()
    if idx is None or (stage2 and S['_line'] <= L_SORT + 1):
        upto = 0
        idx = None
    elif not stage2:
        upto = idx + 1
    else:
        upto = idx + (1 if S['_line'] >= L_MERGE2 else 0)
    if stage2:
        for i, e in enumerate(edges):
            if e[3]:
                a, b = fd(e[0]), fd(e[1])
                if a != b:
                    fa[a] = b
                chosen.add(i)
        for i in range(min(upto, len(edges))):
            e = edges[i]
            if e[3]:
                continue
            a, b = fd(e[0]), fd(e[1])
            if a != b:
                fa[a] = b
                chosen.add(i)
            else:
                rej.add(i)
    else:
        for i in range(min(upto, len(edges))):
            e = edges[i]
            if e[3]:
                a, b = fd(e[0]), fd(e[1])
                if a != b:
                    fa[a] = b
                chosen.add(i)
    return idx, upto, chosen, rej, [fd(v) for v in range(n)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, edges, k = S['n'], S['edges'], S['k']
    idx, upto, chosen, rej, roots = _sim(S)
    stage2 = 'left' in S and S['_line'] >= L_SORT
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 10
    rx, ry = min(300, (x1 - x0) / 2 - 90), min(165, (y1 - y0) / 2 - 95)
    pos = [(cx - rx, cy - ry), (cx + rx, cy - ry), (cx + rx, cy + ry), (cx - rx, cy + ry)]
    cv.text((x0 + 18, y0 + 4), '图（紫 = 必选边，绿 = 已选进生成树，红虚线 = 成环舍弃，黄框 = 当前边）', 22, T['muted'], bold=True)
    # 升级情况
    up = {}
    if stage2:
        left = S['left0'] if 'left0' in S else None
    leftc = None
    if stage2:
        leftc = sum(1 for e in edges if e[3])  # placeholder
    # 重放计算哪些边被翻倍
    if stage2:
        fa = list(range(n))

        def fd(a):
            while fa[a] != a:
                a = fa[a]
            return a
        for e in edges:
            if e[3]:
                a, b = fd(e[0]), fd(e[1])
                if a != b:
                    fa[a] = b
        lf = len({fd(v) for v in range(n)}) - 1
        for i in sorted(chosen):
            e = edges[i]
            if e[3]:
                continue
            up[i] = not (lf > k)
            lf -= 1
    for i, e in enumerate(edges):
        a, b, s, m = e
        p, q = pos[a], pos[b]
        if m and i in chosen:
            col, w = T['purple'], 9
        elif i in chosen:
            col, w = T['green'], 8
        elif i in rej:
            col, w = T['red'], 3
        else:
            col, w = (T['purple'] if m else (90, 98, 110)), (5 if m else 3)
        if i in rej:
            cv.dashed(p, q, col, w)
        else:
            cv.line([p, q], col, w)
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        if (a, b) == (0, 2):
            mx, my = p[0] + (q[0] - p[0]) * 0.32, p[1] + (q[1] - p[1]) * 0.32
        lab = f'{s}→{2 * s}' if up.get(i) else str(s)
        wd = cv.tlen(lab, 26, True) + 20
        cv.rect((mx - wd / 2, my - 18, mx + wd / 2, my + 18), fill=T['panel2'], outline=T['yellow'] if i == idx else col, width=4 if i == idx else 2, r=10)
        cv.text((mx, my), lab, 26, T['orange'] if up.get(i) else T['text'], anchor='mm', bold=True)
    cmap = {}
    for r_ in roots:
        cmap.setdefault(r_, T[PAL[len(cmap) % len(PAL)]])
    for v in range(n):
        X, Y = pos[v]
        cv.rect((X - 34, Y - 34, X + 34, Y + 34), fill=cmap[roots[v]], r=34)
        cv.text((X, Y), v, 34, T['bg'], anchor='mm', bold=True)
    ncomp = len(cmap)
    cv.text((cx, y1 - 16), f'同色 = 同一连通块，当前 {ncomp} 个', 22, T['muted'], anchor='mm', bold=True)


def _txt(S):
    if 'x' not in S:
        return '边 `[u, v, 强度, must]`：必选边不能升级，其余最多升级 `k` 条（强度 ×2）'
    if 'left' not in S:
        return f"第一遍：必选边先连，成环就 -1；`min_s1 = {S['min_s1']}`（必选边最小强度）"
    return f"Kruskal：`left = {S['left']}` 条边没选，`k = {S['k']}`；`ans = {S['ans']}`"


CONFIG = dict(
    num=3600, title='升级后最大生成树稳定性', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='必选边 + Kruskal 最大生成树 + 升级最小的 k 条',
    tags=['二分算法', '图论算法', '难度分 2301'],
    code=CODE,
    call='Solution().maxStability(4, [[0,1,8,1],[2,3,3,0],[1,2,5,0],[0,3,2,0],[0,2,4,0]], 1)',
    expect=5,
    max_steps=70,
    skip=['self._fa', 'self.cc', 'x, y = self.find', 'if x == y', 'return False', 'return True', 'def ', 'if self._fa[x] != x', 'return self._fa[x]'],
    views=[
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=['x', 'y', 's', 'must', 'min_s1', ('left', 'left', 'blue'), 'k', ('ans', 'ans', 'green')],
    captions={
        28: '`uf` 只放必选边，用来判环、数连通块',
        29: '`all_uf` 放所有边，用来判整张图是否连通',
        'min_s1 = inf': '`min_s1`：必选边的最小强度',
        31: lambda S, B, r: (f'看边 `({S.x}, {S.y})`，强度 `{S.s}`，must = `{S.must}`' if not (B.get('x') == S.x and B.get('y') == S.y) else '所有边都看完了'),
        'if must:': lambda S, B, r: ('必选边：必须放进树里' if S.must else '可选边：第一遍先不管'),
        'if not uf.merge': lambda S, B, r: ('必选边 `({}, {})` 连不上（已连通）→ 成环，无解 -1'.format(S.x, S.y) if r == -1 else '必选边 `({}, {})` 合并成功，没有成环'.format(S.x, S.y)),
        'min_s1 = min': '必选边最小强度：`min_s1 = {min_s1}`',
        'all_uf.merge(x, y)': '全图并查集也连上 `({x}, {y})`',
        'if all_uf.cc > 1': lambda S, B, r: ('全图连通块 `{}` → 连不起来，-1'.format(S.all_uf.cc) if S.all_uf.cc > 1 else '全图只有 1 个连通块 → 一定存在生成树'),
        'left = uf.cc - 1': '必选边之后还有 `{uf.cc}` 个连通块 → 还要再选 `left = {left}` 条可选边',
        42: lambda S, B, r: ('必选边已经是生成树，答案 `min_s1`' if S.left == 0 else f'还差 `{S.left}` 条边，继续'),
        48: lambda S, B, r: (f'看边 `({S.x}, {S.y})`，强度 `{S.s}`，must = `{S.must}`' if not (B.get('x') == S.x and B.get('y') == S.y) else '所有边都看完了'),
        'edges.sort': '按强度从大到小排：Kruskal 求==最大生成树==（先不乘 2）',
        'ans = min_s1': '答案先取必选边最小强度 `{ans}`',
        'if not must and uf.merge': lambda S, B, r: ('必选边，已在树里，跳过' if S.must else ('`({}, {})` 强度 {}：连上了两个不同的连通块 → 选入生成树'.format(S.x, S.y, S.s) if _sim(S)[0] not in _sim(S)[3] else '`({}, {})` 两端已连通，加了会成环 → 丢弃'.format(S.x, S.y))),
        'ans = min(ans, s if left > k': '`left = {left}`，`k = {k}`：升级只给==最小的 k 条==；`left > k` 说明这条还不用升，否则翻倍 → 取 `{s if left > k else s * 2}`；`ans = {ans}`',
        'left -= 1': '还差 `{left}` 条边',
        52: lambda S, B, r: ('树已完成 → break' if S.left == 0 else f'还差 `{S.left}` 条，继续'),
        'return ans': '最大稳定性 = `{ans}`',
    },
    cards=dict(
        one_liner='先连必选边，再 Kruskal 取最大边，最小的 k 条边翻倍',
        complexity='时间 `O(m log m)`，空间 `O(n)`',
        problem=['`n` 个点，边 `[u, v, s, must]`；`must = 1` 必须选且不能升级',
                 '最多升级 `k` 条可选边（强度 ×2），求生成树最小边权的最大值，无解 -1',
                 '本视频：`n=4`，5 条边，`k=1` → `5`'],
        quote='在选出必选边后，根据 Kruskal 算法求最大生成树，把剩余的边按照边权（先不乘 2）从大到小合并。……由于每条边至多操作一次，所以选 a 的后 k 个数乘以 2。',
        quote_src='—— 灵茶山艾府题解 · 方法二',
        idea=['必选边成环或图不连通 → `-1`',
              '最大生成树让最小边尽量大；升级只给最小的 `k` 条',
              '`left > k` 的边不升级，其余翻倍，答案取过程中的最小值'],
        summary=['时间 `O(m log m)`，空间 `O(n)`',
                 '易错：必选边要单独用并查集判环，且全图要先判连通',
                 '易错：升级的是生成树里最小的 k 条，不是原图最小',
                 '本视频用方法二写法二（边 Kruskal 边更新答案）；方法一是二分 low + 并查集，写法一用数组 a 记录选中的边',
                 '同类：最大化最小值 + 最小生成树'],
    ),
)
