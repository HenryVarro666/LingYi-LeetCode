_LAY = {}
_PAL = ['blue', 'pink', 'green', 'purple', 'cyan', 'orange', 'yellow', 'red']


def _layout(n, edges):
    key = (n, tuple(map(tuple, edges)))
    if key in _LAY:
        return _LAY[key]
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    par = [-1] * n
    dep = [0] * n
    xs = [0.0] * n
    cnt = [0]

    def go(u, p, d):
        par[u], dep[u] = p, d
        ch = [v for v in g[u] if v != p]
        for v in ch:
            go(v, u, d + 1)
        if ch:
            xs[u] = sum(xs[v] for v in ch) / len(ch)
        else:
            xs[u] = cnt[0]
            cnt[0] += 1

    go(0, -1, 0)
    _LAY[key] = (par, dep, xs, max(cnt[0] - 1, 1))
    return _LAY[key]


def _lca(S, a, b):
    d, f = S['depth'], S['f']
    while d[a] > d[b]:
        a = f[a][0]
    while d[b] > d[a]:
        b = f[b][0]
    while a != b:
        a, b = f[a][0], f[b][0]
    return a


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, edges, group = S['n'], S['edges'], S['group']
    par, dep, xs, xmax = _layout(n, edges)
    gs = sorted(set(group))
    col = {gid: T[_PAL[k % len(_PAL)]] for k, gid in enumerate(gs)}
    c = S.get('c')
    nodes = S.get('nodes') or {}
    members = set(nodes.get(c, [])) if c is not None else None
    t_set = S.get('t_set') or set()
    stack = S.get('stack') or []
    tt = S.get('t') or {}
    now = S['_inner'].get('now') if 'fa' in S['_inner'] else None
    if c is None or members is None:
        members = None
    cv.text((x0 + 18, y1 - 10), '颜色 = 所属组（g = 组号）；绿线 = 虚树的边（×k = 压缩了 k 条原边）', 21, T['muted'], anchor='lb', bold=True)
    top, bot = y0 + 40, y1 - 90
    maxd = max(dep)
    dy = (bot - top) / max(maxd, 1)
    left, right = x0 + 120, x1 - 90
    px = lambda u: left + (right - left) * xs[u] / xmax
    py = lambda u: top + dy * dep[u]
    for d in range(maxd + 1):
        cv.text((x0 + 24, top + dy * d), f'深度 {d}', 20, T['dim'], anchor='lm', mono=True)
    for u in range(n):
        if par[u] >= 0:
            cv.line([(px(par[u]), py(par[u])), (px(u), py(u))], T['border'], 4)
    for p_, kids in tt.items():
        for k in kids:
            cv.line([(px(p_), py(p_)), (px(k), py(k))], T['green'], 7)
            ln = dep[k] - dep[p_]
            if ln > 1:
                cv.text(((px(p_) + px(k)) / 2 + 26, (py(p_) + py(k)) / 2), f'×{ln}', 26, T['green'], anchor='lm', bold=True)
    R = 24
    for u in range(n):
        inn = members is None or u in members
        fill = col[group[u]] if inn else T['panel2']
        cv.rect((px(u) - R, py(u) - R, px(u) + R, py(u) + R), fill=fill, outline=col[group[u]], width=4, r=R)
        cv.text((px(u), py(u)), u, 30, T['bg'] if inn else T['muted'], anchor='mm', bold=True, mono=True)
        cv.text((px(u), py(u) + R + 8), f'g{group[u]}', 20, T['muted'], anchor='mt', mono=True)
        if members is not None and u in t_set and u not in members:
            cv.rect((px(u) - R - 8, py(u) - R - 8, px(u) + R + 8, py(u) + R + 8), outline=T['orange'], width=4, r=R + 8)
            cv.text((px(u) - R - 14, py(u)), '分叉点', 20, T['orange'], anchor='rm', bold=True)
        if u in stack and 94 <= S['_line'] <= 105:
            cv.rect((px(u) - R - 14, py(u) - R - 14, px(u) + R + 14, py(u) + R + 14), outline=T['pink'], width=3, r=R + 14)
        if now == u:
            cv.rect((px(u) - R - 14, py(u) - R - 14, px(u) + R + 14, py(u) + R + 14), outline=T['yellow'], width=5, r=R + 14)


def _status(S):
    res = S.get('res')
    c = S.get('c')
    if c is None or 'nodes' not in S:
        return '先 DFS 建立：每个点的深度、父亲，以及每一组有哪些点'
    mem = S['nodes'].get(c, [])
    tail = f'，累计 `res = {res}`' if res is not None else ''
    return f'当前组 `{c}`：点 `{mem}`{tail}'


CONFIG = dict(
    num=4018, title='树组的交互代价总和 II', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='虚树 + 按边贡献',
    tags=[],
    code='''
class Solution(object):
    def interactionCosts(self, n, edges, group):
        
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)
        
        order = []
        depth = [0] * n
        nodes = {}
        f = [[] for _ in range(n)]

        def dfs(now, fa, d):
            order.append(now)
            f[now].append(fa)
            depth[now] = d
            if group[now] not in nodes:
                nodes[group[now]] = []
            nodes[group[now]].append(now)

            for nxt in g[now]:
                if nxt == fa:
                    continue
                dfs(nxt, now, d + 1)
        
        def lca(u, v):
            if depth[u] != depth[v]:
                if depth[u] < depth[v]:
                    u, v = v, u

                while depth[u] != depth[v]:
                    p = len(f[u]) - 1
                    while p > 0 and depth[u] - (1 << p) < depth[v]:
                        p -= 1
                    
                    u = f[u][p]
            
            while u != v:
                p = min(len(f[u]), len(f[v])) - 1
                while p > 0 and f[u][p] == f[v][p]:
                    p -= 1
                u = f[u][p]
                v = f[v][p]
            
            return u

        def calc(now, fa, t, c):
            global res

            cnt = 0
            for nxt in t.get(now, []):
                cnt += calc(nxt, now, t, c)
            
            if c == group[now]:
                cnt += 1

            if fa != -1:
                res += (depth[now] - depth[fa]) * (len(nodes[c]) - cnt) * cnt

            return cnt

        dfs(0, -1, 0)
        dfn = [0] * n
        for u in range(n):
            dfn[order[u]] = u

        updated = True
        p = 0
        while updated:
            updated = False
            p += 1
            for u in range(n):
                if len(f[u]) >= p and f[u][-1] != -1:
                    v = f[u][p - 1]
                    if len(f[v]) >= p and f[v][-1] != -1:
                        f[u].append(f[v][p - 1])
                        updated = True

        global res
        res = 0
        for c in nodes:
            if len(nodes[c]) < 2:
                continue
            
            t_set = set(nodes[c])
            for index in range(1, len(nodes[c])):
                u = lca(nodes[c][index], nodes[c][index - 1])
                if u not in t_set:
                    t_set.add(u)
            
            t_list = sorted(list(t_set), key=lambda d:dfn[d])
            
            t_root = t_list[0]
            stack = [t_list[0]]
            t = {}
            for u in t_list[1:]:
                while lca(stack[-1], u) != stack[-1]:
                    stack.pop()

                if stack[-1] not in t:
                    t[stack[-1]] = []
                t[stack[-1]].append(u)
                stack.append(u)
            
            calc(t_root, -1, t, c)
        
        return res
''',
    call='Solution().interactionCosts(6, [[0, 1], [1, 2], [1, 3], [3, 4], [3, 5]], [7, 1, 2, 3, 7, 7])',
    expect=8,
    views=[
        dict(type='text', fn=_status, size=26, h=50),
        dict(type='custom', draw=_draw, h=430),
        dict(type='array', var='t_list', label='t_list（虚树的点，按 DFS 序）', cell=64, h=125,
             color=lambda S, i, v: 'orange' if v not in S['nodes'].get(S.get('c'), []) else None),
        dict(type='array', var='stack', label='stack（当前祖先链）', cell=64, h=125),
        dict(type='calls', h=150, hide=('edges', 'group', 't')),
    ],
    watch=[('c', 'c', 'cyan'), ('res', lambda S: S.get('res'), 'green')],
    max_steps=80,
    captions={
        'dfs(0, -1, 0)': '先 DFS 一遍：记下每个点的深度 `depth`、父亲 `f[x][0]`、所属组 `nodes`',
        'nodes[group[now]].append(now)': '`{now}` 属于组 `{group[now]}`，深度 `{depth[now]}` → `nodes[{group[now]}] = {nodes[group[now]]}`',
        'dfs(nxt, now, d + 1)': '走向孩子 `{now}`（深度 `{d}`）',
        'while updated': lambda S, B, ret: ('倍增预处理：每一轮给 `f[u]` 追加「第 2^k 级祖先」，之后求 LCA 就能按 2 的幂往上跳；没有新增时结束'
                                            if S.updated else '预处理完毕：`f[u]` = u 的 1、2、4…级祖先（-1 表示到顶）'),
        'if len(nodes[c]) < 2': lambda S, B, ret: (f'组 `{S.c}` 只有 `{len(S.nodes[S.c])}` 个点，没有点对 → ==跳过=='
                                                   if len(S.nodes[S.c]) < 2 else
                                                   f'组 `{S.c}` 有 `{len(S.nodes[S.c])}` 个点 `{S.nodes[S.c]}`：要算它们两两之间的路径长度之和，为它建==虚树=='),
        't_set = set(nodes[c])': '虚树的点：先放进这一组的所有点 `{t_set}`',
        'u = lca(nodes[c][index]': lambda S, B, ret: (f'相邻两个点 `{S.u}` 与 `{S.v}` 求最近公共祖先 LCA = `{_lca(S, S.u, S.v)}`'
                                                      '（只算相邻的 DFS 序点对就够，不用两两算）'),
        'if u not in t_set': lambda S, B, ret: (f'LCA = `{S.u}` 不在虚树里 → 它是个==分叉点==，要补进去' if S.u not in S.t_set
                                                else f'LCA = `{S.u}` 本来就在虚树里 → 不用补'),
        't_set.add(u)': '分叉点 `{u}` 加入虚树：`t_set = {t_set}`',
        't_list = sorted': '按 DFS 序排好：`t_list = {t_list}`（祖先一定排在子孙前面）',
        'stack = [t_list[0]]': '`t_list[0]` 是虚树的根；`stack` 始终放着「从根到当前点的祖先链」，`t` 记录虚树的边',
        'while lca(stack[-1], u)': lambda S, B, ret: (
            (f'`lca(栈顶 {S.u}, 当前点 {S.v}) = {_lca(S, S.u, S.v)}`，等于栈顶 → 当前点在栈顶的子树里，不用弹栈')
            if _lca(S, S.u, S.v) == S.u else
            (f'`lca(栈顶 {S.u}, 当前点 {S.v}) = {_lca(S, S.u, S.v)}` ≠ 栈顶 → 栈顶那棵子树已经建完，要弹出')),
        'stack.pop()': '弹出栈顶：`stack = {stack}`',
        't[stack[-1]].append(u)': '虚树建边：`{stack[-1]}` → `{u}`（原树里隔了 `{depth[u] - depth[stack[-1]]}` 条边）',
        'stack.append(u)': '`{u}` 入栈：`stack = {stack}`',
        'calc(t_root, -1, t, c)': '虚树建好了，从根开始后序遍历，按边算贡献',
        'cnt += calc(nxt, now, t, c)': '进入虚树的孩子 `{now}`：先数它子树里本组的点',
        'if c == group[now]': lambda S, B, ret: (f'`{S.now}` 属于本组 → `cnt` 再加 1' if S.c == S.group[S.now]
                                                 else f'`{S.now}` 不属于本组（它是分叉点）→ `cnt` 不加'),
        'res += (depth[now]': lambda S, B, ret: (
            f'虚树边 `{S.fa}→{S.now}` 压缩了 `{S.depth[S.now] - S.depth[S.fa]}` 条原边；下面 `{S.cnt}` 个本组点，'
            f'上面 `{len(S.nodes[S.c]) - S.cnt}` 个 → 加 `{S.depth[S.now] - S.depth[S.fa]} × {len(S.nodes[S.c]) - S.cnt} × {S.cnt}'
            f' = {(S.depth[S.now] - S.depth[S.fa]) * (len(S.nodes[S.c]) - S.cnt) * S.cnt}`'),
        'return cnt': lambda S, B, ret: (f'`{S.now}` 子树里本组共 `{ret}` 个点，返回给父亲' if S.fa != -1 else f'根 `{S.now}` 没有往上的边；整组共 `{ret}` 个点，这一组算完'),
        'return res': '所有组加起来：最终 `res = {ret}`',
    },
    skip=['g = [[]', 'for x, y in edges', 'g[x].append', 'g[y].append', 'order = []', 'depth = [0]', 'nodes = {}', 'f = [[]',
          'order.append', 'f[now].append', 'depth[now] = d', 'if group[now] not in nodes', 'nodes[group[now]] = []',
          'for nxt in g[now]', 'if nxt == fa', 'continue',
          'if depth[u] != depth[v]', 'if depth[u] < depth[v]', 'u, v = v, u', 'while depth[u] != depth[v]',
          'p = len(f[u]) - 1', 'while p > 0 and depth', 'p -= 1', 'u = f[u][p]', 'while u != v', 'p = min(',
          'while p > 0 and f[u][p]', 'v = f[v][p]', 'return u',
          'cnt = 0', 'for nxt in t.get', 'cnt += 1', 'global res',
          'dfn = [0]', 'for u in range(n)', 'dfn[order[u]]', 'updated = True', 'p = 0', 'updated = False', 'p += 1',
          'if len(f[u])', 'v = f[u][p - 1]', 'if len(f[v])', 'f[u].append(f[v]', 'res = 0',
          'for c in nodes', 'for index in range', 'if stack[-1] not in t', 't[stack[-1]] = []', 'for u in t_list[1:]', 'dfs(nxt, now, d + 1)', 'if fa != -1', 't_root = t_list[0]', 't = {}'],
    cards=dict(
        one_liner='按边算贡献，每组只在虚树上算，一条压缩边一次算完',
        complexity='时间 `O(n log n)`，空间 `O(n log n)`',
        problem=['给一棵 `n` 个点的树和每个点的组号 `group`',
                 '同组两点 `u, v` 的交互代价 = 路径上的边数',
                 '求所有同组无序点对的交互代价之和（`n` 可达 `10^5`，组数最多 `n`）',
                 '本视频：树 `0-1, 1-2, 1-3, 3-4, 3-5`，`group = [7,1,2,3,7,7]` → `8`'],
        quote='对于某条边和某个组别c，若其两侧组别为c的点的数目分别为x和y，那么这条边在这个组别上的贡献就是x * y。',
        quote_src='—— yiduobo 题解原文',
        idea=['换成「经过某条边」的视角：边的贡献 = 一侧本组点数 × 另一侧本组点数',
              '每个组都扫整棵树是 `O(n^2)`；只有组内点和它们的分叉点才有用 → 建==虚树==',
              '点按 DFS 序排序，只求相邻点的 LCA 找全分叉点，用栈建虚树；压缩边贡献要乘长度'],
        after=[dict(heading='LCA 与倍增（视频里略过的部分）', lines=['DFS 时记下父亲：`f[u][0]`；预处理后 `f[u][k]` = u 的 `2^k` 级祖先',
                                                                  '`lca(u, v)`：先跳到同一深度，再一起往上跳，每次 `O(log n)`'])],
        summary=['时间 `O(n log n)`：每组的 LCA 与建树都是 `O(k log n)`，各组 `k` 之和为 `n`',
                 '==DFS 序相邻点的 LCA 就够了==：不同子树之间的点对 LCA 会重复，没必要两两算',
                 '虚树的边要乘 `depth[now] - depth[fa]`（压缩的原边数），否则少算',
                 '原文是 Python 2 风格，无需修改即可在 Python 3 运行'],
    ),
)
