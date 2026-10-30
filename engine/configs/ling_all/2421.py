_POS = {0: (0.50, 0.18), 1: (0.22, 0.58), 2: (0.78, 0.45), 3: (0.62, 0.88), 4: (0.94, 0.88)}
_EDGES = [[0, 1], [0, 2], [2, 3], [2, 4]]
_PAL = ['cyan', 'orange', 'purple', 'green', 'pink']


def _root(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    vals = S.get('vals')
    fa = S.get('fa')
    if vals is None or fa is None or not isinstance(fa, list):
        return
    n = len(vals)
    cv.text((x0 + 18, y0 + 4), '树（节点里是 vals；同色 = 同一连通块；暗 = 值还没轮到）', 24, T['muted'], bold=True)
    vx = S.get('vx')
    cur = S.get('x') if S.get('_line', 0) and isinstance(S.get('x'), int) and 'vx' in S else None
    W, Hh = x1 - x0 - 120, y1 - y0 - 175
    P = {i: (x0 + 60 + _POS[i][0] * W, y0 + 95 + _POS[i][1] * Hh) for i in range(n)}
    roots = sorted({_root(fa, i) for i in range(n)})
    cmap = {}
    k = 0
    for r in roots:
        if sum(1 for i in range(n) if _root(fa, i) == r) > 1:
            cmap[r] = _PAL[k % len(_PAL)]
            k += 1
    for a, b in _EDGES:
        same = _root(fa, a) == _root(fa, b)
        col = T[cmap[_root(fa, a)]] if same else T['border']
        cv.line([P[a], P[b]], col, 7 if same else 3)
    for i in range(n):
        px, py = P[i]
        rt = _root(fa, i)
        dim = vx is not None and vals[i] > vx
        fill = T[cmap[rt]] if rt in cmap else (110, 118, 132)
        if dim:
            fill = (30, 34, 42)
        ring = T['yellow'] if (cur == i) else None
        R = 40
        if ring:
            cv.d.ellipse((px - R - 7, py - R - 7, px + R + 7, py + R + 7), outline=ring, width=5)
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fill)
        cv.text((px, py), vals[i], 34, T['bg'] if (rt in cmap and not dim) else (T['dim'] if dim else T['text']), anchor='mm', bold=True)
        cv.text((px, py + R + 16), f'#{i}', 20, T['dim'], anchor='mm', mono=True)
        if rt == i and rt in cmap:
            cv.text((px - R - 4, py - R + 2), '根', 20, T['yellow'], anchor='rm', bold=True)


def _ans(S):
    if 'ans' not in S:
        return ''
    return f"好路径累计 `ans = {S['ans']}`（单点 {len(S['vals'])} 条 + 同值连通产生的路径）"


CONFIG = dict(
    num=2421, title='好路径的数目', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='按值从小到大 · 并查集合并',
    tags=['七、并查集', '§7.2 进阶', '难度分 2445'],
    code='''
class Solution:
    def numberOfGoodPaths(self, vals: List[int], edges: List[List[int]]) -> int:
        n = len(vals)
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)  # 建图

        # 并查集模板
        fa = list(range(n))
        # size[x] 表示节点值等于 vals[x] 的节点个数，
        # 如果按照节点值从小到大合并，size[x] 也是连通块内的等于最大节点值的节点个数
        size = [1] * n
        def find(x: int) -> int:
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        ans = n  # 单个节点的好路径
        for vx, x in sorted(zip(vals, range(n))):
            fx = find(x)
            for y in g[x]:
                y = find(y)
                if y == fx or vals[y] > vx:
                    continue  # 只考虑最大节点值不超过 vx 的连通块
                if vals[y] == vx:  # 可以构成好路径
                    ans += size[fx] * size[y]  # 乘法原理
                    size[fx] += size[y]  # 统计连通块内节点值等于 vx 的节点个数
                fa[y] = fx  # 把小的节点值合并到大的节点值上
        return ans
''',
    call='Solution().numberOfGoodPaths([1,3,2,1,3], [[0,1],[0,2],[2,3],[2,4]])',
    expect=6,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='vals', label='vals', cell=70, h=135),
        dict(type='array', var='fa', label='fa（并查集：fa[i] 是 i 的父亲）', cell=70, h=135),
        dict(type='array', var='size', label='size（连通块里等于最大值的节点数）', cell=70, h=135),
    ],
    watch=[('vx', 'vx', 'blue'), ('x', 'x', 'pink'), ('fx', 'fx', 'cyan'), ('ans', 'ans', 'green')],
    skip=['g[x].append', 'g[y].append', 'for x, y in edges', 'g = [[]', 'size = [1]', 'def find', 'if fa[x] != x', 'return fa[x]'],
    captions={
        'n = len(vals)': '`n = {n}`：先把每个单独的节点都算一条好路径',
        'fa = list(range(n))': '并查集初始：每个节点自成一个连通块，`fa[i] = i`',
        'ans = n': '单个节点本身就是好路径：`ans = {ans}`',
        'for vx, x in sorted': '按节点值从小到大取点：现在处理值 `vx = {vx}` 的节点 `x = {x}`，比它大的点还没加入',
        'fx = find(x)': '找 `x` 所在连通块的代表元 `fx`（`x` 自己是根就返回自己）',
        'for y in g[x]': '逐个看 `x` 的邻居（`g[{x}] = {g[x]}`）',
        'if vals[y] == vx': lambda S, B, r: ('两块的最大值都等于 `vx`：能连出好路径' if S.vals[S.y] == S.vx else '`vals[y] < vx`：只是把小值块并进来，不产生新好路径'),
        'y = find(y)': '邻居所在连通块的代表元 `y = {y}`（它是该块的最大值节点）',
        'if y == fx': lambda S, B, r: (f'`y == fx`：已经在同一块，跳过' if S.y == S.fx
                                       else (f'`vals[{S.y}] = {S.vals[S.y]} > vx = {S.vx}`：这块的最大值更大，不能经过它 → 跳过'
                                             if S.vals[S.y] > S.vx else
                                             f'`vals[{S.y}] = {S.vals[S.y]} ≤ vx = {S.vx}`：这块最大值不超过 `vx`，可以合并')),
        'ans += size': '两块最大值都是 `{vx}`：`size[fx] × size[y] = {B.size[B.fx]} × {B.size[B.y]}` 条新好路径 → `ans = {ans}`（乘法原理）',
        'size[fx] += size[y]': '合并后块内最大值节点数：`size[{fx}] = {size[fx]}`',
        'fa[y] = fx': '小块并入大块：`fa[{y}] = {fx}`，代表元仍是最大值所在的点',
        'return ans': '所有点处理完，好路径共 `{ans}` 条',
    },
    cards=dict(
        one_liner='值从小到大加点，合并连通块，同值两块相乘得好路径',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给一棵树和每个节点的值，好路径：两端点值相同，路径上所有点的值 ≤ 端点值',
                 '单个节点也算一条，正反向算同一条',
                 '示例：`vals=[1,3,2,1,3]`，边 `0-1, 0-2, 2-3, 2-4` → `6`',
                 '（5 条单点 + 一条 `1 -> 0 -> 2 -> 4`）'],
        quote='用并查集合并时，总是从节点值小的点往节点值大的点合并，这样可以保证连通块的代表元的节点值是最大的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['暴力：先取最大值的点两两配对，再删掉它们递归，每个点被反复统计',
              '倒过来：把「删除」改成「合并」，用并查集从小值往大值加',
              '处理 `x` 时，邻居所在块的最大值 ≤ `vx` 才能合并',
              '若两块最大值都等于 `vx`，各自等于 `vx` 的点数相乘就是新增路径'],
        summary=['时间 `O(n log n)`（排序），并查集近似常数；空间 `O(n)`',
                 '易错：合并方向必须是小值并到大值，代表元才是块内最大值',
                 '`size` 只统计块内等于最大值的点数，不是块的节点总数',
                 '先 `ans = n` 加上单点路径；思考题：改成「小于」时中间点要严格更小'],
    ),
)
