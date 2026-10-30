# ---- 一般树绘制（custom 视图）：按边集合和根节点分层布局
def gtree(edges, root):
    adj = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    kids, depth = {}, {root: 0}

    def go(v, fa):
        kids[v] = []
        for w in adj.get(v, []):
            if w != fa:
                depth[w] = depth[v] + 1
                kids[v].append(w)
                go(w, v)
    go(root, None)
    xs, cnt = {}, [0]

    def lay(v):
        if not kids[v]:
            xs[v] = cnt[0]
            cnt[0] += 1
        else:
            for w in kids[v]:
                lay(w)
            xs[v] = (xs[kids[v][0]] + xs[kids[v][-1]]) / 2
    lay(root)
    return kids, depth, xs, cnt[0]


def make_tree_draw(edges, root, state_fn, title, elabel=None, arrows=False):
    kids, depth, xs, nleaf = gtree(edges, root)
    maxd = max(depth.values())

    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
        sp = min(120, (x1 - x0 - 60) / max(1, nleaf))
        dy = min(120, (y1 - y0 - 90) / max(1, maxd + 0.6))
        rad = max(16, min(28, sp * 0.36, dy * 0.26))
        sx = x0 + 30 + ((x1 - x0 - 60) - sp * nleaf) / 2
        pos = {v: (sx + sp * (xs[v] + 0.5), y0 + 70 + depth[v] * dy) for v in kids}
        for v in kids:
            for w in kids[v]:
                (ax, ay), (bx, by) = pos[v], pos[w]
                if arrows:
                    cv.arrow((ax, ay + rad), (bx, by - rad), T['border'], 3, 10)
                else:
                    cv.line([(ax, ay + rad), (bx, by - rad)], T['border'], 3)
                if elabel and (v, w) in elabel:
                    mx, my = ax + (bx - ax) * 0.4, ay + (by - ay) * 0.4
                    s = str(elabel[(v, w)])
                    cv.text((mx - 8, my), s, 20, T['orange'], anchor='rm', bold=True)
        for v in kids:
            X, Y = pos[v]
            st = state_fn(S, v) or {}
            fill = T[st['fill']] if st.get('fill') else T['panel2']
            cv.rect((X - rad, Y - rad, X + rad, Y + rad), fill=fill, outline=T['border'], width=2, r=rad)
            if st.get('ring'):
                cv.rect((X - rad - 5, Y - rad - 5, X + rad + 5, Y + rad + 5), outline=T[st['ring']], width=5, r=rad + 5)
            cv.text((X, Y), st.get('text', v), 24, T['bg'] if st.get('fill') else T['text'], anchor='mm', bold=True)
            if st.get('sub') is not None:
                cv.text((X + rad + 8, Y), st['sub'], 21, T[st.get('subc', 'green')], anchor='lm', bold=True)
            if st.get('tag'):
                cv.text((X - rad - 8, Y - rad), st['tag'], 20, T[st.get('tagc', 'pink')], anchor='rb', bold=True)
    return draw
# ---- end helper

EDGES = [(0, 1), (0, 2), (1, 3), (1, 4)]
TG = {0: ('x', 'pink'), 3: ('y', 'cyan'), 4: ('z', 'purple')}


def _st(S, v):
    st = dict(tag=TG[v][0], tagc=TG[v][1]) if v in TG else {}
    inn = S.get('_inner', {})
    if 'dz' in S:
        t = (S['dx'][v], S['dy'][v], S['dz'][v])
        st['sub'] = f'{t[0]},{t[1]},{t[2]}'
        st['subc'] = 'cyan'
        if 't' in S and t == tuple(S['t']):
            st['ring'] = 'yellow'
            ok = 'a' in S and S['a'] ** 2 + S['b'] ** 2 == S['c'] ** 2
            if ok:
                st['fill'] = 'green'
    elif 'dis' in S and 'v' in inn:
        d = S['dis']
        if v == S.get('start') or d[v] > 0:
            st['fill'] = 'yellow'
            st['sub'] = str(d[v])
        if inn.get('v') == v:
            st['ring'] = 'blue'
    else:
        last = S.get('dy') or S.get('dx')
        if last is not None:
            st['sub'] = str(last[v])
    return st


def _fml(S):
    if 'a' in S:
        a, b, c = S['a'], S['b'], S['c']
        return f'排序后 `{a}, {b}, {c}`：`{a}² + {b}² = {a*a+b*b}`，`{c}² = {c*c}` → ' + ('==相等，特殊节点==' if a*a+b*b == c*c else '不相等')
    if 'dz' in S:
        return '三棵 DFS 都跑完了：每个点的 `(dx, dy, dz)` 写在节点右侧'
    return '黄 = 当前这次 DFS 已算出距离的点（数字 = 到起点的距离），蓝环 = 正在访问'


CONFIG = dict(
    num=3820, title='树上的勾股距离节点', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='从 x,y,z 各跑一次 DFS 求距离',
    tags=['链表树与回溯', '难度分 1725'],
    code='''
class Solution:
    def specialNodes(self, n: int, edges: List[List[int]], x: int, y: int, z: int) -> int:
        g = [[] for _ in range(n)]
        for v, w in edges:
            g[v].append(w)
            g[w].append(v)

        def calc_dis(start: int) -> List[int]:
            dis = [0] * n
            def dfs(v: int, fa: int) -> None:
                for w in g[v]:
                    if w != fa:
                        dis[w] = dis[v] + 1
                        dfs(w, v)
            dfs(start, -1)
            return dis

        dx = calc_dis(x)
        dy = calc_dis(y)
        dz = calc_dis(z)

        ans = 0
        for t in zip(dx, dy, dz):
            a, b, c = sorted(t)
            if a * a + b * b == c * c:
                ans += 1
        return ans
''',
    call='Solution().specialNodes(5, [[0,1],[0,2],[1,3],[1,4]], 0, 3, 4)',
    expect=3,
    views=[
        dict(type='custom', draw=make_tree_draw(EDGES, 0, _st, '树（标记 x / y / z 三个目标，节点右侧 = 距离）'), h=250),
        dict(type='text', fn=_fml, h=60),
        dict(type='array', var='dx', label='dx：x 到每个点的距离', h=112, cell=54, color=lambda S, i, v: 'pink' if i == S['x'] else None),
        dict(type='array', var='dy', label='dy：y 到每个点的距离', h=112, cell=54, color=lambda S, i, v: 'cyan' if i == S['y'] else None),
        dict(type='array', var='dz', label='dz：z 到每个点的距离', h=112, cell=54, color=lambda S, i, v: 'purple' if i == S['z'] else None),
        dict(type='calls', h=110),
    ],
    skip=['for w in g[v]', 'g[w].append'],
    max_steps=72,
    watch=[('ans', 'ans', 'green'), ('t', 't', 'orange')],
    captions={
        'g[v].append': '无向树：`{v} - {w}` 两个方向各存一次',
        'g[w].append': '反向也存：`{w}` 的邻居里加入 `{v}`',
        'dis = [0] * n': '准备一个距离数组：这次 DFS 的起点是 `{start}`',
        'if w != fa': lambda S, B, r: (f'邻居 `{S.w}` 就是来时的父节点 `{S.fa}` → 跳过，树里不会有环，只要不回头就不会重复' if S.w == S.fa
                                       else f'邻居 `{S.w}` 不是父节点 → 是往下走的新节点'),
        'dis[w] = dis[v] + 1': '`dis[{w}] = dis[{v}] + 1` = =={dis[w]}== ：比父亲远 1 条边',
        'dfs(w, v)': '往下递归：进入 `{v}`，父节点记为 `{fa}`',
        'dfs(start, -1)': '从起点 `{start}` 出发，它没有父节点（`-1`）',
        'return dis': '这次 DFS 完成：起点到每个点的距离 = `{dis}`',
        'dx = calc_dis(x)': '`dx` = 从 x 出发到各点的距离 = `{dx}`',
        'dy = calc_dis(y)': '`dy` = 从 y 出发到各点的距离 = `{dy}`',
        'dz = calc_dis(z)': '`dz` = 从 z 出发到各点的距离 = `{dz}`',
        'ans = 0': '三个距离数组都有了：反过来枚举每个点 u，看 `(dx[u], dy[u], dz[u])`',
        'a, b, c = sorted(t)': '三个距离排序得到 `a ≤ b ≤ c` = `{a}, {b}, {c}`：勾股数必须最大的当斜边',
        'if a * a + b * b': lambda S, B, r: f'`{S.a}² + {S.b}² = {S.a*S.a+S.b*S.b}`，`{S.c}² = {S.c*S.c}` → ' + ('==相等，特殊节点==' if S.a*S.a+S.b*S.b == S.c*S.c else '不相等，跳过'),
        'ans += 1': '又找到一个特殊节点：`ans` = =={ans}==',
        'return ans': '一共 `{ans}` 个特殊节点',
    },
    cards=dict(
        one_liner='反过来想：从 x、y、z 出发各跑一次 DFS，距离就都有了',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树，三个不同的目标点 `x, y, z`',
                 '节点 `u` 到三点的距离 `dx, dy, dz` 排序后满足 `a² + b² = c²` 就是特殊节点',
                 '数特殊节点个数。示例：`n=4, [[0,1],[0,2],[0,3]], x=1,y=2,z=3` → `3`'],
        quote='计算每个点到 x,y,z 的距离，要跑 n 次 O(n) 的最短路，总的时间复杂度是 O(n²)，太慢了。反过来呢？计算从 x,y,z 出发，到每个点的距离，只需跑三次 DFS（或者 BFS）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['树上两点距离唯一，==换个方向==：一次 DFS 得到起点到所有点的距离',
              '只需对 `x, y, z` 各跑一次，共 3 次 `O(n)`',
              '再枚举每个点：`sorted` 后判断 `a*a + b*b == c*c`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`dfs(v, fa)` 靠 `fa` 防止走回头路，树不需要 visited 数组',
                 '勾股判断一定要先排序，最大的是斜边；`0, k, k` 也算（`0² + k² = k²`）',
                 '也可以用 BFS 求距离，题解说 DFS/BFS 均可'],
    ),
)
