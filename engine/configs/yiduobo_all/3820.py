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
    if 'dz' in S:
        t = (S['dx'][v], S['dy'][v], S['dz'][v])
        st['sub'] = f'{t[0]},{t[1]},{t[2]}'
        st['subc'] = 'cyan'
        if 'u' in S and S['u'] == v and S.get('_line', 0) >= 28:
            st['ring'] = 'yellow'
            if 'a' in S and S['a'] ** 2 + S['b'] ** 2 == S['c'] ** 2:
                st['fill'] = 'green'
    elif 'dis' in S and 'start' in S:
        d = S['dis']
        if d[v] != -1:
            st['fill'] = 'yellow'
            st['sub'] = str(d[v])
        if S.get('now') == v:
            st['ring'] = 'blue'
    else:
        last = S.get('dy') or S.get('dx')
        if last is not None:
            st['sub'] = str(last[v])
    return st


def _fml(S):
    if 'a' in S and 'u' in S:
        a, b, c = S['a'], S['b'], S['c']
        return f'点 `{S["u"]}`：排序后 `{a}, {b}, {c}`，`{a}² + {b}² = {a*a+b*b}`，`{c}² = {c*c}` → ' + ('==相等，特殊节点==' if a*a+b*b == c*c else '不相等')
    if 'dz' in S:
        return '三次 bfs 都完成：每个点的 `(dx, dy, dz)` 写在节点右侧'
    return '黄 = 已算出距离的点（数字 = 到起点的距离，-1 = 还没到），蓝环 = 正在扩展'


CONFIG = dict(
    num=3820, title='树上的勾股距离节点', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='三次 BFS 求距离',
    tags=['链表树与回溯', '难度分 1725'],
    code='''
class Solution(object):
    def specialNodes(self, n, edges, x, y, z):
        
        def bfs(start):
            q = [start]
            dis = [-1] * n
            dis[start] = 0

            head, tail = 0, 1
            while head < tail:
                now = q[head]
                head += 1
                for nxt in g[now]:
                    if dis[nxt] == -1:
                        dis[nxt] = dis[now] + 1
                        q.append(nxt)
                        tail += 1
            
            return dis

        g = [[] for _ in range(n)]
        for u, v in edges:
            g[u].append(v)
            g[v].append(u)

        dx = bfs(x)
        dy = bfs(y)
        dz = bfs(z)

        res = 0
        for u in range(n):
            a, b, c = sorted([dx[u], dy[u], dz[u]])
            if a * a + b * b == c * c:
                res += 1
        
        return res
''',
    call='Solution().specialNodes(5, [[0,1],[0,2],[1,3],[1,4]], 0, 3, 4)',
    expect=3,
    views=[
        dict(type='custom', draw=make_tree_draw(EDGES, 0, _st, '树（标记 x / y / z，节点右侧 = 距离）'), h=250),
        dict(type='text', fn=_fml, h=60),
        dict(type='array', var='dx', label='dx', h=112, cell=54, color=lambda S, i, v: 'pink' if i == S['x'] else None),
        dict(type='array', var='dy', label='dy', h=112, cell=54, color=lambda S, i, v: 'cyan' if i == S['y'] else None),
        dict(type='array', var='dz', label='dz', h=112, cell=54, color=lambda S, i, v: 'purple' if i == S['z'] else None),
    ],
    skip=['head += 1', 'tail += 1', 'g[v].append', 'for nxt in g[now]', 'q.append(nxt)', 'q = [start]', 'dis[start] = 0', 'head, tail = 0, 1'],
    max_steps=84,
    watch=[('now', 'now', 'blue'), ('res', 'res', 'green')],
    captions={
        'g[u].append': '无向边 `{u} - {v}`：两头都记一份邻居',
        'q = [start]': '这次 bfs 从 `{start}` 出发，用列表 `q` 当队列',
        'dis = [-1] * n': '`dis` 全是 -1 表示「还没到过」',
        'dis[start] = 0': '起点到自己的距离是 `0`',
        'while head < tail': lambda S, B, r: (f'队列里还有 `{S.tail - S.head}` 个点没处理 → 继续' if S.head < S.tail else '队列处理完，整棵树都走到了'),
        'now = q[head]': '取出队首 `{now}`，距离 `{dis[now]}`，去看它的邻居',
        'if dis[nxt] == -1': lambda S, B, r: (f'`dis[{S.nxt}] == -1`：没到过，是新点' if S.dis[S.nxt] == -1 else f'`dis[{S.nxt}]` 已有值 → 是来路上的点，不重复'),
        'dis[nxt] = dis[now] + 1': '`dis[{nxt}] = dis[{now}] + 1` = =={dis[nxt]}==：比 `{now}` 远一步',
        'q.append(nxt)': '`{nxt}` 入队，等着往外扩',
        'return dis': '这次 bfs 完成：起点到各点距离 `{dis}`',
        'dx = bfs(x)': '`dx` = x 到各点的距离 = `{dx}`',
        'dy = bfs(y)': '`dy` = y 到各点的距离 = `{dy}`',
        'dz = bfs(z)': '`dz` = z 到各点的距离 = `{dz}`',
        'res = 0': '三组距离齐了：接下来逐个点 `u` 判断 `(dx[u], dy[u], dz[u])`',
        'a, b, c = sorted': '点 `{u}` 的三个距离排序：`a, b, c = {a}, {b}, {c}`，最大的 `c` 当斜边',
        'if a * a + b * b': lambda S, B, r: f'`{S.a}² + {S.b}² = {S.a*S.a+S.b*S.b}`，`{S.c}² = {S.c*S.c}` → ' + ('==相等，特殊节点==' if S.a*S.a+S.b*S.b == S.c*S.c else '不相等，跳过'),
        'res += 1': '点 `{u}` 是特殊节点：`res` = =={res}==',
        'return res': '一共 `{res}` 个特殊节点',
    },
    cards=dict(
        one_liner='要知道每个点到 x、y、z 的距离，不如从 x、y、z 出发各 bfs 一次',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树 `n` 个点，三个不同的目标点 `x, y, z`',
                 '点 `u` 到三点距离 `dx, dy, dz` 构成勾股数元组（排序后 `a² + b² = c²`）就是特殊节点',
                 '求特殊节点个数。示例：`n=4, [[0,1],[0,2],[0,3]], x=1,y=2,z=3` → `3`'],
        quote='判断每个节点是否为特殊节点，就需要知道x、y、z到树中所有节点的距离，于是可以分别从x、y、z出发，执行三次bfs，计算这三个节点到树中其他节点的距离。',
        quote_src='—— yiduobo 题解原文',
        idea=['u 到 x 的距离 = x 到 u 的距离：==方向反过来想==',
              '三次 bfs 各得到一个距离数组 `dx, dy, dz`',
              '遍历每个点，三个距离排序后验证勾股'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '这里用列表 + `head/tail` 下标当队列，不用 deque',
                 '`dis` 初值 `-1` 兼作 visited，起点要先置 `0`',
                 '勾股判断前必须排序，`0, k, k` 也成立',
                 '原文为 Python 2 写法，在 Python 3 下无需修改即可运行'],
    ),
)
