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
    cv.text((x0 + 18, y0 + 4), '树（节点里是 vals；同色 = 同一连通块；暗 = 还没加回；黄圈 = 当前值 v 的节点）', 24, T['muted'], bold=True)
    vx = S.get('v') if isinstance(S.get('v'), int) else None
    cur = None
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
        ring = T['yellow'] if (vx is not None and vals[i] == vx) else None
        R = 40
        if ring:
            cv.d.ellipse((px - R - 7, py - R - 7, px + R + 7, py + R + 7), outline=ring, width=5)
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fill)
        cv.text((px, py), vals[i], 34, T['bg'] if (rt in cmap and not dim) else (T['dim'] if dim else T['text']), anchor='mm', bold=True)
        cv.text((px, py + R + 16), f'#{i}', 20, T['dim'], anchor='mm', mono=True)
        if rt == i and rt in cmap:
            cv.text((px - R - 4, py - R + 2), '根', 20, T['yellow'], anchor='rm', bold=True)



CONFIG = dict(
    num=2421, title='好路径的数目', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='倒推加点 · 并查集 · 同值计数',
    tags=['七、并查集', '§7.2 进阶', '难度分 2445'],
    code='''
class Solution(object):
    def numberOfGoodPaths(self, vals, edges):

        n = len(vals)
        edge_set = {}
        node_set = {}
        for index, v in enumerate(vals):
            if v not in edge_set:
                edge_set[v] = set()
            if v not in node_set:
                node_set[v] = set()
            node_set[v].add(index)

        for index in range(n - 1):
            x, y = edges[index]
            if vals[x] > vals[y]:
                edge_set[vals[x]].add(index)
            else:
                edge_set[vals[y]].add(index)
        
        fa = list(range(n))

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        res = n
        for v in sorted(edge_set.keys()):
            for index in edge_set[v]:
                x, y = edges[index]
                fa_x = find(x)
                fa_y = find(y)

                if vals[fa_x] == v:
                    fa[fa_y] = fa_x
                else:
                    fa[fa_x] = fa_y
        
            cnt = {}
            for x in node_set[v]:
                fa_x = find(x)
                cnt[fa_x] = cnt.get(fa_x, 0) + 1
            
            for k in cnt.values():
                res += k * (k - 1) // 2

        return res
''',
    call='Solution().numberOfGoodPaths([1,3,2,1,3], [[0,1],[0,2],[2,3],[2,4]])',
    expect=6,
    views=[
        dict(type='custom', draw=_draw, h=250),
        dict(type='map', var='edge_set', label='edge_set：值 v → 在 v 加回时生效的边编号', fmt=lambda k, v: f'{k}: {sorted(v)}', h=100),
        dict(type='map', var='node_set', label='node_set：值 v → 节点编号', fmt=lambda k, v: f'{k}: {sorted(v)}', h=100),
        dict(type='array', var='fa', label='fa（并查集）', cell=64, h=145),
        dict(type='map', var='cnt', label='cnt：连通块代表元 → 块内值为 v 的节点数 k', h=110),
    ],
    watch=[('v', 'v', 'blue'), ('index', 'index', 'pink'), ('fa_x', 'fa_x', 'cyan'), ('fa_y', 'fa_y', 'orange'), ('res', 'res', 'green')],
    max_steps=60,
    skip=['n = len(vals)', 'if v not in edge_set', 'edge_set[v] = set()', 'if v not in node_set', 'node_set[v] = set()',
          'def find', 'if fa[x] != x', 'return fa[x]', 'for index in range(n - 1)', 'for x in node_set[v]', 'for k in cnt.values()', 'fa_y = find(y)'],
    captions={
        'node_set[v].add(index)': '按值分组：值 `{v}` 的节点 → `node_set[{v}] = {sorted(node_set[v])}`',
        'x, y = edges[index]': lambda S, B, r: (f'取第 `{S.index}` 条边 `({S.x}, {S.y})`' if 'v' in S and 'edge_set' in S and 'res' not in S
                                                   else f'这条边 `({S.x}, {S.y})` 在值 `{S.v}` 被加回时生效' if 'res' in S else ''),
        'if vals[x] > vals[y]': '边 `({x}, {y})` 两端值 `{vals[x]}`、`{vals[y]}`：==较大的一端被加回树时，这条边才生效==',
        'edge_set[vals[x]].add': '归到较大值 `{vals[x]}` 名下：`edge_set[{vals[x]}] = {sorted(edge_set[vals[x]])}`',
        'edge_set[vals[y]].add': '归到较大值 `{vals[y]}` 名下：`edge_set[{vals[y]}] = {sorted(edge_set[vals[y]])}`',
        'fa = list(range(n))': '并查集初始：每个点自成一块；树一开始是「清空」的，边都还没加回',
        'res = n': '单个点形成的路径也是好路径：`res = {res}`',
        'for v in sorted': '值从小到大加回：现在加回值 `v = {v}` 的点和它们的边（此时树里所有点值都 ≤ `{v}`）',
        'for index in edge_set[v]': '加回值 `{v}` 名下的边 `{sorted(edge_set[v])}`（没有边就直接统计）',
        'edge_set = {}': '`edge_set`：值 → 这个值加回时才生效的边',
        'node_set = {}': '`node_set`：值 → 拥有这个值的节点',
        'fa_x = find(x)': '找边两端所在块的代表元 `fa_x`、`fa_y`',
        'if vals[fa_x] == v': lambda S, B, r: (f'`vals[fa_x] = {S.vals[S.fa_x]}` 等于 `v`：代表元已经是值 `v` 的点 → 把 `fa_y` 挂到它下面'
                                               if S.vals[S.fa_x] == S.v else
                                               f'`vals[fa_x] = {S.vals[S.fa_x]}` ≠ `v`：代表元值小 → 把 `fa_x` 挂到 `fa_y` 下面'),
        'fa[fa_y] = fa_x': '合并：`fa[{fa_y}] = {fa_x}`',
        'fa[fa_x] = fa_y': '合并：`fa[{fa_x}] = {fa_y}`',
        'cnt = {}': '边加完了，统计每个块里值为 `{v}` 的点各有多少',
        'cnt[fa_x] = cnt.get': '点 `{x}` 属于块 `{fa_x}`，该块里值为 `{v}` 的点数 `k = {cnt[fa_x]}`',
        'res += k * (k - 1) // 2': '`k = {k}`：`{k} × ({k} − 1) / 2 = {k * (k - 1) // 2}` 条好路径 → `res = {res}`',
        'return res': '全部加回完毕，好路径共 `{res}` 条',
    },
    cards=dict(
        one_liner='把树清空再按值加回，块里 k 个同值点就有 k(k-1)/2 条',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['树的节点有值，好路径：两端值相同，中间所有点值不超过端点值',
                 '单个点也算好路径，求好路径总数',
                 '示例：`vals=[1,3,2,1,3]`，边 `0-1, 0-2, 2-3, 2-4` → `6`'],
        quote='先将树清空，然后按照节点值从小到大逐个将其加回到树中。由于是按照值从小到大的顺序加回到树中，那么对于当前加回到树中的值v而言，树中已有节点的值都是小于等于v的。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模大，不走树分治，改用「倒推加点」',
              '边挂在两端值较大的一侧：该值加回时边才生效',
              '边加完后，并查集给出连通块；统计各块里值为 `v` 的点数 `k`',
              '块内任意两个值为 `v` 的点，路径上都不超过 `v` → `k(k-1)/2` 条'],
        summary=['时间 `O(n log n)`（排序 + 并查集），空间 `O(n)`',
                 '别忘了最后要加上单点路径 `n`（代码里 `res = n` 起步）',
                 '合并时要让代表元保持为「值最大」的点，`vals[fa_x] == v` 就是在判断这一点',
                 '原文为 Python 2 写法，已改为：`fa = range(n)` → `list(range(n))`，`/ 2` → `// 2`',
                 '对比灵神：灵神边合并边累加 `size` 乘积；这里先合并完再按块计数'],
    ),
)
