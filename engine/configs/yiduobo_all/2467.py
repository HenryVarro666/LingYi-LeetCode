def _lay(edges):
    n = len(edges) + 1
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    depth, kids, seen, q = [0] * n, {i: [] for i in range(n)}, {0}, [0]
    for x in q:
        for y in g[x]:
            if y not in seen:
                seen.add(y)
                depth[y] = depth[x] + 1
                kids[x].append(y)
                q.append(y)
    pos, cnt = {}, [0]
    def go(x):
        if not kids[x]:
            pos[x] = cnt[0]
            cnt[0] += 1
        else:
            for y in kids[x]:
                go(y)
            pos[x] = (pos[kids[x][0]] + pos[kids[x][-1]]) / 2
    go(0)
    return pos, depth, cnt[0], max(depth) + 1, kids


def _tree(cv, T, edges, box, label, fill=None, ring=None, sub=None, title=None, r=26):
    """通用树绘制：label(i)=节点内文字，fill(i)=颜色名或None，ring(i)=描边颜色名，sub(i)=节点下方小字"""
    x0, y0, x1, y1 = box
    pos, depth, w, h, kids = _lay(edges)
    if title:
        cv.text((x0 + 14, y0 + 2), title, 22, T['muted'], bold=True)
        y0 += 36
    dx = min(110, (x1 - x0 - 2 * r - 20) / max(w - 1, 1)) if w > 1 else 0
    dy = min(120, (y1 - y0 - 2 * r - 30) / max(h - 1, 1)) if h > 1 else 0
    sx = (x0 + x1) / 2 - dx * (w - 1) / 2
    P = {i: (sx + pos[i] * dx, y0 + r + 10 + depth[i] * dy) for i in pos}
    for a, b in edges:
        cv.line([P[a], P[b]], T['border'], 3)
    for i, (X, Y) in P.items():
        f = fill(i) if fill else None
        rg = ring(i) if ring else None
        cv.rect((X - r, Y - r, X + r, Y + r), fill=T[f] if f else T['panel2'], outline=T[rg] if rg else T['border'], width=5 if rg else 2, r=r)
        cv.text((X, Y), label(i), 26, T['bg'] if f else T['text'], anchor='mm', bold=True)
        cv.text((X - r - 2, Y - r - 2), i, 16, T['dim'], anchor='rb', mono=True)
        if sub and sub(i):
            cv.text((X + r + 8, Y), sub(i), 20, T['muted'], anchor='lm', bold=True)

EDGES = [[0, 1], [1, 2], [1, 3], [3, 4]]


def _draw(cv, S, B, box, T):
    amt = S.get('amount', [-2, 4, 2, -4, 6])
    bp = S.get('bob_path')
    now = S.get('now')
    q = S.get('q') or []
    vs = {}
    if q and isinstance(q[0], list):
        vs = {a: b for a, b in q}
    zero = [i for i in range(len(amt)) if bp and i in bp and amt[i] == 0]
    def fill(i):
        if bp and i in bp:
            return 'orange'
        return None
    def ring(i):
        return 'yellow' if i == now else None
    def sub(i):
        return f'累计 {vs[i]}' if i in vs else ''
    _tree(cv, T, EDGES, box, lambda i: amt[i], fill=fill, ring=ring, sub=sub, r=26,
          title='节点里是当前 amount；橙 = Bob 到根的路径，黄框 = 正在处理的节点')


def _qtxt(S):
    q = S.get('q')
    if q is None:
        return ''
    if q and isinstance(q[0], list):
        return '队列 `q`（节点, 路径和）：' + '  '.join(f'({a},{b})' for a, b in q)
    return '队列 `q`（节点）：' + ' '.join(str(a) for a in q)


def _halve(S, B, ret):
    return f'路径长度为奇数：正中间的节点 `{S.bob_path[S.right]}` 两人同时到 → ==折半== `{B.amount[S.bob_path[S.right]]} // 2 = {S.amount[S.bob_path[S.right]]}`'


CONFIG = dict(
    num=2467, title='树上最大得分和路径', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='先改点权消除 Bob，再 BFS 求最大路径和',
    tags=['灵神题单·链表树与回溯', '难度分 2053'],
    code='''
class Solution(object):
    def mostProfitablePath(self, edges, bob, amount):

        n = len(edges) + 1
        g = {index : set() for index in range(n)}

        for x, y in edges:
            g[x].add(y)
            g[y].add(x)

        q = [bob]
        vis = set([bob])
        prev = {}
        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            for next in g[now]:
                if next not in vis:
                    vis.add(next)
                    prev[next] = now
                    q.append(next)
                    tail += 1
        
        bob_path = []
        now = 0
        while now != bob:
            bob_path.append(now)
            now = prev[now]
        bob_path.append(bob)
        
        left = 0
        right = len(bob_path) - 1
        while left < right:
            amount[bob_path[right]] = 0
            left += 1
            right -= 1

        if left == right:
            amount[bob_path[right]] //= 2
        
        res = None
        q = [[0, amount[0]]]
        head, tail = 0, 1
        vis = set([0])
        while head < tail:
            now, v = q[head]
            if now != 0 and len(g[now]) == 1 and (res is None or res < v):
                res = v

            head += 1
            for next in g[now]:
                if next not in vis:
                    vis.add(next)
                    q.append([next, v + amount[next]])
                    tail += 1

        return res
''',
    call='Solution().mostProfitablePath([[0,1],[1,2],[1,3],[3,4]], 3, [-2,4,2,-4,6])',
    expect=6,
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='text', fn=_qtxt, size=26, h=60),
        dict(type='array', var='bob_path', label='bob_path（从根 0 到 bob）', cell=64, h=120,
             pointers={'left': 'blue', 'right': 'pink'}),
        dict(type='array', var='amount', label='amount（会被原地修改）', cell=64, h=120),
    ],
    watch=[('now', 'now', 'yellow'), 'left', 'right', ('res', 'res', 'green')],
    skip=['for x, y in edges', 'g[x].add(y)', 'g[y].add(x)', 'head += 1', 'tail += 1', 'while head < tail', 'for next in g[now]', 'if next not in vis', 'vis.add(next)', 'q.append(next)', 'vis = set', 'prev = {}', 'head, tail', 'now = q[head]'],
    captions={
        'g = {index': '建无向图：每个点一个邻居集合，每条边两个方向都加',
        'q = [bob]': '第一次 BFS 从 ==bob== 出发，目的是记下每个点的父亲 `prev`（节点没法直接访问父亲）',
        'prev[next] = now': '`prev[{next}] = {now}`：从 `{now}` 第一次走到 `{next}`',
        'now = 0': '回溯：从根 0 开始沿 `prev` 走向 bob',
        'bob_path.append(now)': '`bob_path = {bob_path}`',
        'bob_path.append(bob)': '补上 bob 自己：`bob_path = {bob_path}`（从根 0 到 bob，共 {len(bob_path)} 个点）',
        'now = prev[now]': '沿 `prev` 走到 `{now}`',
        'left = 0': '双指针 `left`、`right` 从路径两端往中间：==后半段（靠 bob）Alice 到不了比 Bob 早==',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`：还有成对的点' if S.left < S.right else f'`left = {S.left}`，`right = {S.right}`：两指针相遇或错开 → 结束'),
        'amount[bob_path[right]] = 0': '路径靠 bob 的一半：Bob ==先到==，Alice 来时门已开 → `amount[{bob_path[right]}] = 0`',
        'left += 1': '`left` → {left}',
        'right -= 1': '`right` → {right}',
        'if left == right': lambda S, B, r: (f'`left == right`：路径长度是奇数，中间点 `{S.bob_path[S.right]}` 两人同时到' if S.left == S.right else '`left != right`：路径长度是偶数，没有同时到的点'),
        'amount[bob_path[right]] //= 2': _halve,
        'q = [[0, amount[0]]]': '第二次 BFS 从根出发，队列里存 `[节点, 路径和]`，起点路径和是 `amount[0]`',
        'now, v = q[head]': '取出节点 `{now}`，从根到它的路径和 `v = {v}`',
        'if now != 0': lambda S, B, r: (f'`{S.now}` 是叶子（度数 1，且不是根）→ 路径和 `{S.v}` 可以参与比较，`res` 目前是 `{B.res}`' if S.now != 0 and len(S.g[S.now]) == 1 else ('`0` 是根：==根不算叶子==（否则根只有一个孩子时会被误判）→ 不比较' if S.now == 0 else f'`{S.now}` 有 {len(S.g[S.now])} 个邻居，不是叶子 → 不比较')),
        'q.append([next, v + amount[next]])': '孩子 `{next}` 入队，路径和 `{v} + {amount[next]} = {v + amount[next]}`',
        'res = v': '更新答案：`res = {res}`',
        'return res': 'Alice 的最大得分 `{res}`',
    },
    cards=dict(
        one_liner='把 Bob 的影响直接改进点权里，再当普通最大路径和做',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['无向树，根是 0；Alice 从 0 走向叶子，Bob 从 `bob` 走向 0，每秒一步',
                 '先到者开门拿分；同时到则平分；门已开则无分',
                 '求 Alice 能拿到的最大得分。示例：`bob = 3` → `6`'],
        quote='如果没有bob的存在，本题就是常规的bfs或者dfs，计算从根节点到当前节点的路径和，然后找出其中路径和最大的叶子节点。',
        quote_src='—— yiduobo 题解原文',
        idea=['Bob 只会影响他到根路径上的==前半段==点：Bob 先到，Alice 去时已无分，直接改成 0',
              '路径长度为奇数时，正中间的点两人同时到 → 折半，不是 0',
              '改完之后，再 BFS 找路径和最大的叶子'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，`amount[...] /= 2` 已改为 `//= 2`',
                 '易错：中间点是折半而不是置零；根节点不算叶子',
                 '对比灵神：灵神记 Bob 到达时间并比较；yiduobo 一次性改点权，更直观'],
    ),
)
