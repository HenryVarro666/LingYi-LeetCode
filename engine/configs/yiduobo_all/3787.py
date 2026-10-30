def _tree_pos(ch, root=0):
    """一般树自动布局：叶子按顺序排开，父亲在孩子中间。返回 {节点: (x 0~1, 深度)}"""
    pos, cnt = {}, [0]
    leaves = sum(1 for _ in _leaves(ch, root))
    def go(u, d):
        kids = ch.get(u, [])
        if not kids:
            pos[u] = ((cnt[0] + 0.5) / leaves, d); cnt[0] += 1
        else:
            for k in kids:
                go(k, d + 1)
            pos[u] = ((pos[kids[0]][0] + pos[kids[-1]][0]) / 2, d)
    go(root, 0)
    return pos


def _leaves(ch, u):
    kids = ch.get(u, [])
    if not kids:
        yield u
    for k in kids:
        yield from _leaves(ch, k)


def _gt_draw(cv, S, B, box, T, ch, pos, edges, node_fn, extra=None, title=''):
    """edges: [(父,子,颜色名或None,虚线)]；node_fn(S,u)->(填充色, 主文字, 副文字)"""
    x0, y0, x1, y1 = box
    maxd = max(d for _, d in pos.values())
    W, H = x1 - x0 - 300, y1 - y0 - 110
    P = {u: (x0 + 110 + px * W, y0 + 70 + (d / max(maxd, 1)) * H) for u, (px, d) in pos.items()}
    if title:
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    for a, b, col, dash in edges:
        pa, pb = P[a], P[b]
        if dash == 'arc':  # 从孩子 b 绕一道弧线指向 a（向左侧鼓出）
            cx, cy = min(pa[0], pb[0]) - 110, (pa[1] + pb[1]) / 2
            pts = [((1 - t) ** 2 * pb[0] + 2 * (1 - t) * t * cx + t * t * pa[0],
                    (1 - t) ** 2 * pb[1] + 2 * (1 - t) * t * cy + t * t * pa[1]) for t in [0.12 + 0.76 * i / 30 for i in range(31)]]
            cv.line(pts, T[col], 5)
            cv.arrow(pts[-3], pts[-1], T[col], 5, 16)
        elif dash:
            cv.dashed(pb, pa, T[col], 4)
        else:
            cv.line([pa, pb], T[col] if col else T['border'], 4 if col else 3)
    R = 24
    for u, (X, Y) in P.items():
        fill, main, sub = node_fn(S, u)
        cv.rect((X - R, Y - R, X + R, Y + R), fill=T[fill] if isinstance(fill, str) else fill, outline=T['border'], r=R, width=2)
        cv.text((X, Y), main, 24, T['text'] if fill == 'panel2' else T['bg'], anchor='mm', bold=True, mono=True)
        if sub:
            cv.text((X + R + 8, Y), sub, 20, T['text'], anchor='lm', bold=True)
    if extra:
        extra(cv, P, T)
    return P
N = 7
EDGES = [[0, 1], [1, 2], [2, 3], [1, 4], [4, 5], [0, 6]]
CH = {0: [1, 6], 1: [2, 4], 2: [3], 4: [5]}
POS = _tree_pos(CH)


def _node(S, u):
    dis = S.get('dis') or [-1] * N
    t = S.get('t') or set()
    I = S['_inner']
    sub = f'dis={dis[u]}' if dis[u] >= 0 else ''
    if I.get('nxt') == u:
        return 'pink', str(u), sub
    if I.get('now') == u:
        return 'yellow', str(u), sub
    if u in t:
        return 'green', str(u), sub
    if S.get('q') and dis[u] == 0:
        return 'blue', str(u), sub
    if dis[u] >= 0:
        return 'cyan', str(u), sub
    return 'panel2', str(u), sub


def _draw(cv, S, B, box, T):
    edges = [(a, b, None, False) for a, ks in CH.items() for b in ks]
    _gt_draw(cv, S, B, box, T, CH, POS, edges, _node,
             title='树（蓝 = 出发点 dis=0，青 = 已访问，黄 = now，粉 = nxt，绿 = 已确认的直径端点）')


_HEAD = lambda S: S.get('head')
_TAIL = lambda S: S.get('tail')


CONFIG = dict(
    num=3787, title='查找树的直径端点', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='两趟 BFS 找最远点',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def findSpecialNodes(self, n, edges):
        
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)
        
        q = [0]
        dis = [-1] * n
        dis[0] = 0
        head, tail = 0, 1
        while head < tail:
            for now in q[head: tail]:
                for nxt in g[now]:
                    if dis[nxt] == -1:
                        dis[nxt] = dis[now] + 1
                        q.append(nxt)
            
            head, tail = tail, len(q)
        
        t = set()
        for x in range(n):
            if dis[x] == dis[q[-1]]:
                t.add(x)

        q = [q[-1]]
        dis = [-1] * n
        dis[q[0]] = 0
        head, tail = 0, 1
        while head < tail:
            for now in q[head: tail]:
                for nxt in g[now]:
                    if dis[nxt] == -1:
                        dis[nxt] = dis[now] + 1
                        q.append(nxt)
            
            head, tail = tail, len(q)
        
        for x in range(n):
            if dis[x] == dis[q[-1]]:
                t.add(x)

        res = []
        for x in range(n):
            if x in t:
                res.append('1')
            else:
                res.append('0')
        
        return ''.join(res)
''',
    call='Solution().findSpecialNodes(7, [[0,1],[1,2],[2,3],[1,4],[4,5],[0,6]])',
    expect='0001011',
    setup='',
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='q', label='q（BFS 访问顺序，蓝框 = 当前这一层 q[head:tail]）', cell=60, h=120,
             pointers={'head': 'blue', 'tail': 'pink'}),
        dict(type='array', var='dis', label='dis（到出发点的距离，-1 = 还没到）', cell=60, h=110),
        dict(type='set', var='t', label='t：直径端点集合', h=110, fmt=lambda x: str(x)),
    ],
    watch=[('head', 'head', 'blue'), ('tail', 'tail', 'pink'), ('now', "now if 'now' in _inner else ''", 'yellow'), ('nxt', "nxt if 'nxt' in _inner else ''", 'orange')],
    skip=['for x, y in edges', 'g[x].append', 'g[y].append', 'for now in q[head: tail]', 'for nxt in g[now]', 'dis[nxt] = dis[now] + 1', 'if dis[nxt] == -1', 'for x in range(n)', 'if dis[x] == dis[q[-1]]', 'if x in t', 'else:', "res.append('0')", 'g = [[]', 'res = []', 'dis = [-1]'],
    max_steps=100,
    captions={
        'q = [0]': '第一趟 BFS：从任意点 `0` 出发，`q` 是队列，一层一层往外扩',
        'dis[0] = 0': '出发点距离为 0，其余 -1 表示还没到',
        'head, tail = 0, 1': '`q[head:tail]` 是当前这一层：先只有出发点',
        'while head < tail': lambda S, B, r: (f'这一层 `q[{S.head}:{S.tail}]` 不空 → 继续扩一层' if S.head < S.tail
                                              else '没有新的一层了：BFS 结束，`q[-1]` 是最后到达的点，也是一个最远点'),
        'q.append(nxt)': '`{now}` 的邻居 `{nxt}` 还没到过（`dis == -1`）→ `dis[{nxt}] = {dis[now]} + 1 = {dis[nxt]}`，入队：`q = {q}`；到过的邻居会被挡掉',
        'head, tail = tail, len(q)': '这一层的邻居都看完了：新的一层是 `q[{head}:{tail}]`',
        't = set()': '`t` 收集直径端点',
        't.add(x)': '`dis[{x}] = {dis[x]}` 等于最远距离 `dis[q[-1]] = {dis[q[-1]]}` → 最远点之一，加入 `t = {t}`',
        'q = [q[-1]]': '第二趟：从第一趟最后到达的点 `{q[0]}` 出发（它一定是某条直径的端点）',
        'dis[q[0]] = 0': '重新计距离：`dis[{q[0]}] = 0`，其余 -1',
        "res.append('1')": '`{x}` 在 `t` 里 → 是直径端点，记 `1`（不在 `t` 的记 `0`）：`res = {res}`',
        'return': '`res = {res}` → 拼成字符串 `{ret!r}`',
    },
    cards=dict(
        one_liner='两趟 BFS：两趟里所有「最远点」，就是全部直径端点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树，`n` 个点、`n-1` 条边',
                 '直径 = 树上最长的一条路径；若某点是==某条直径==的端点，就叫特殊节点',
                 '返回长度 `n` 的 0/1 字符串，`1` 表示特殊。示例：7 个点 → `"0001011"`'],
        quote='两趟bfs或者dfs到达的所有最远节点都必然是直径的端点。更进一步的，应该不存在其他的端点。',
        quote_src='—— yiduobo 题解原文',
        idea=['经典求直径：任选一点 BFS，到最远点 `A`；再从 `A` BFS，到最远点 `B`，`A-B` 就是直径',
              '本题要的是所有端点：每趟 BFS ==所有离出发点最远的点==都收进 `t`',
              '第一趟从 `0` 出发，第二趟从第一趟的最后一个点出发，两趟的并集就是答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：每趟要收的是==所有==最远点（`dis` 等于最大值的全部），不是只收 `q[-1]`',
                 '易错点：第二趟必须从第一趟的最远点出发，不能再从 0 出发',
                 '`head, tail` 划出 BFS 当前这一层，`q[head:tail]` 一层一层处理',
                 '原文是 Python 2 风格 `class Solution(object)`，在 Python 3 中可直接运行，未改动'],
    ),
)
