import math


def _ln(code, sub):
    """1-based line number of the first code line containing sub (leading blank line stripped)"""
    for k, s in enumerate(code.strip('\n').split('\n')):
        if sub in s:
            return k + 1
    return -1


def _gdraw(cv, box, T, pos, E, node_fn, edge_fn, label_fn=None, title='', directed=True, R=30, base=0, above=None, elabel=None, left=None):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    w = x1 - x0 - 140
    h = y1 - y0 - 195
    P = [(x0 + 70 + fx * w, y0 + 100 + fy * h) for fx, fy in pos]
    es = set(E)
    for (a, b) in E:
        col, wd = edge_fn(a, b)
        (ax, ay), (bx, by) = P[a], P[b]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        off = 10 if (b, a) in es else 0
        nx, ny = -uy * off, ux * off
        p0 = (ax + ux * R + nx, ay + uy * R + ny)
        p1 = (bx - ux * (R + 2) + nx, by - uy * (R + 2) + ny)
        if elabel:
            t = elabel(a, b)
            if t:
                mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
                cv.text((mx + nx * 2.2 + 6, my + ny * 2.2 - 4), t, 20, col, anchor='lb', bold=True)
        if directed:
            cv.arrow(p0, p1, col, wd, head=16)
        else:
            cv.line([p0, p1], col, wd)
    for i, (x, y) in enumerate(P):
        fill, tc, ring = node_fn(i)
        cv.rect((x - R, y - R, x + R, y + R), fill=fill, r=R, outline=ring or T['border'], width=5 if ring else 1)
        cv.text((x, y), i + base, 26, tc, anchor='mm', bold=True)
        if label_fn:
            lab = label_fn(i)
            if lab:
                if left and left(i):
                    cv.text((x - R - 8, y), lab[0], 21, lab[1], anchor='rm', bold=True)
                elif above and above(i):
                    cv.text((x, y - R - 6), lab[0], 21, lab[1], anchor='mb', bold=True)
                else:
                    cv.text((x, y + R + 8), lab[0], 21, lab[1], anchor='mt', bold=True)


G = [1, 2, 0, 0, 3, 4, 7, 6]
POS = [(0.3, 0.4), (0.5, 0.05), (0.7, 0.4), (0.3, 0.9), (0.15, 0.9), (0.0, 0.9), (0.93, 0.1), (0.93, 0.8)]
CODE = '''
class Solution(object):
    def countVisitedNodes(self, edges):

        g = {}
        circle_list = []
        n = len(edges)
        vis = set()
        q = []
        
        for i in range(n):
            if i not in vis:
                q.append(i)
                vis.add(i)
                while edges[q[-1]] not in vis:
                    q.append(edges[q[-1]])
                    vis.add(q[-1])
                
                x = edges[q[-1]]
                if x not in g:
                    circle_list.append([])
                    while q[-1] != x:
                        g[q[-1]] = set()
                        circle_list[-1].append(q.pop())
                    
                    circle_list[-1].append(x)
                    g[x] = set()

                while q:
                    g[x].add(q[-1])
                    x = q.pop()
                    g[x] = set()
        
        res = [0] * n
        for circle in circle_list:
            for x in circle:
                q = [x]
                res[x] = len(circle)
                head, tail = 0, 1
                while head < tail:
                    now = q[head]
                    head += 1
                    for nxt in g[now]:
                        res[nxt] = res[now] + 1
                        q.append(nxt)
                        tail += 1
        
        return res
'''
L_P2 = None
for _k, _t in enumerate(CODE.strip('\n').split('\n')):
    if 'res = [0] * n' in _t:
        L_P2 = _k + 1


def _draw(cv, S, B, box, T):
    edges = S.get('edges') or G
    line = S.get('_line', 0)
    q = S.get('q') or []
    path = set(q) if line < L_P2 else set()
    circ = set()
    for c in (S.get('circle_list') or []):
        circ |= set(c)
    vis = S.get('vis') or set()
    res = S.get('res')
    p2 = line >= L_P2
    cur = None
    if p2 and S.get('now') is not None:
        cur = S['now']
    elif not p2 and q:
        cur = q[-1]

    def node(i):
        ring = T['yellow'] if cur == i else None
        if p2 and res and res[i] > 0:
            return (T['green'] if i in circ else T['cyan']), T['bg'], ring
        if i in circ:
            return T['green'], T['bg'], ring
        if i in path:
            return T['blue'], T['bg'], ring
        if i in vis:
            return (70, 76, 86), T['text'], ring
        return T['panel2'], T['muted'], ring

    def edge(a, b):
        if a in circ and b in circ:
            return T['green'], 5
        if a in path and b in path:
            return T['blue'], 4
        if a in vis and b in vis:
            return (130, 138, 150), 3
        return T['dim'], 3

    def lab(i):
        if p2 and res and res[i] > 0:
            return (f'res={res[i]}', T['green'] if i in circ else T['cyan'])
        return None
    E = [(i, e) for i, e in enumerate(edges)]
    _gdraw(cv, box, T, POS, E, node, edge, lab, '蓝 = 本轮路径 q，灰 = 已访问，绿 = 环，青 = 树上节点，黄圈 = 当前点',
           above=lambda i: i in (1, 6), left=lambda i: i == 0)


CONFIG = dict(
    num=2876, title='有向图访问计数', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='先找环建树 · 再从环出发 BFS',
    tags=['灵神题单·图论算法', '难度分 2210'],
    code=CODE,
    call=f'Solution().countVisitedNodes({G})',
    expect=[3, 3, 3, 4, 5, 6, 2, 2],
    skip=['n = len(edges)', 'g = {}', 'circle_list = []', 'vis = set()', 'q = []', 'vis.add(', 'circle_list.append([])', 'g[x] = set()', 'g[q[-1]] = set()', 'head, tail', 'head += 1', 'tail += 1', 'for circle in circle_list', 'for x in circle', 'for i in range', 'while q:', 'while head < tail', 'for nxt in g[now]', 'q.append(nxt)'],
    max_steps=120,
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='array', var='q', label='q（第一阶段 = 本轮路径；第二阶段 = BFS 队列）', h=115, cell=56),
        dict(type='text', fn=lambda S: ('环：' + '，'.join('{' + ','.join(str(v) for v in c) + '}' for c in S['circle_list'])) if S.get('circle_list') else '环：暂无', size=26, h=50),
        dict(type='array', var='res', label='res', h=115, cell=56),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'yellow')],
    captions={
        'for i in range': lambda S, B, r: (f'枚举起点 `{S.i}`' if S.get('i') is not None else '枚举起点'),
        'if i not in vis': lambda S, B, r: (f'枚举起点 `{S.i}`：还没访问 → 从它开始走一轮' if S.i not in S.vis
                                           else f'枚举起点 `{S.i}`：已访问过 → 它所在的路径早就处理过，跳过'),
        'q.append(i)': '起点 `{i}` 还没访问：开一轮，`q` 记录本轮路径，`vis` 标记已访问',
        'while edges[q[-1]] not in vis': lambda S, B, r: (
            f'`{S.edges[S.q[-1]]}` 没访问过 → 继续走' if S.edges[S.q[-1]] not in S.vis
            else f'`{S.edges[S.q[-1]]}` 已经访问过 → 这一轮走到头了'),
        'q.append(edges[q[-1]])': '走到 `{q[-1]}`',
        'vis.add(q[-1])': '`vis` 标记 `{q[-1]}` 已访问',
        'x = edges[q[-1]]': '路径末端 `{q[-1]}` 的下一个点是 `x = {x}`（已访问过）',
        'if x not in g': lambda S, B, r: (f'`x = {S.x}` 不在 `g` 里：它是==本轮新走出来的环上的点==，要收集这个环' if S.x not in S.g
                                          else f'`x = {S.x}` 已在 `g` 里：撞上了以前处理过的部分，没有新环'),
        'circle_list.append([])': '开一个新环的列表',
        'while q[-1] != x': lambda S, B, r: ('开一个新环；从路径末尾往回弹，弹到 `x` 为止，弹出的点就是环上的点' if not S.circle_list[-1] else '继续往回弹，直到 `q[-1] == x`' if S.q[-1] != S.x else '弹到 `x` 了，停'),
        'g[q[-1]] = set()': '`g[{q[-1]}]` 先建空集合，存它的子节点（树的方向：环 → 外）',
        'circle_list[-1].append(q.pop())': '弹出 `{circle_list[-1][-1]}` 放进环：`{circle_list[-1]}`',
        'circle_list[-1].append(x)': '`x = {x}` 也在环上：环 = `{circle_list[-1]}`；这些点的 `g` 先建空集合',
        'g[x] = set()': '`g[{x}]` 建空集合',
        'while q': lambda S, B, r: (f'`q` 里还剩 `{S.q}`：这些是接在环（或旧节点）上的树枝' if S.q else '树枝都接好了'),
        'g[x].add(q[-1])': lambda S, B, r: (f'`q[-1]` 就是 `x = {S.x}` 本身（环的入口），这步是空操作，下面 `g[x]` 会被重置' if S.q[-1] == S.x else f'`x = {S.x}` 的子节点加入 `{S.q[-1]}`：反向建树，`g[{S.x}] = {S.g[S.x]}`'),
        'x = q.pop()': '弹出 `{x}`，继续把它当作父节点',
        'res = [0] * n': '第二阶段：环已找出，树也建好。对每个环上的点做 BFS',
        'for circle in circle_list': '处理环 `{circle}`',
        'for x in circle': '从环上的点 `{x}` 出发',
        'q = [x]': '从环 `{circle}` 上的点 `{x}` 出发，BFS 队列 `q = [{x}]`',
        'res[x] = len(circle)': '环上的点：答案 = 环长 `{len(circle)}`',
        'head, tail': '`head`、`tail` 是队列的头尾指针',
        'while head < tail': lambda S, B, r: ('队列没空，继续' if S.head < S.tail else '队列空了，这个点的树走完了'),
        'now = q[head]': '取出 `now = {now}`',
        'res[nxt] = res[now] + 1': '`now` 的子节点 `{nxt}`：`res[{nxt}] = res[{now}] + 1 = {res[nxt]}`，比父节点多走一步，随后入队',
        'return res': '环上点 = 环长，树上点 = 到环的步数 + 环长；答案 =={ret}==',
    },
    cards=dict(
        one_liner='先把环和树枝拆出来，再从环往外 BFS 一层层加一',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个点 `n` 条边，`edges[i]` 是 i 的出边终点，从每个点出发一直走，直到再次走到访问过的点',
                 '`answer[i]` = 从 i 出发能访问到的==不同节点数==',
                 '示例：`[1,2,0,0]` → `[3,3,3,4]`；本视频用 8 个点、两个连通块'],
        quote='对于环上的节点，其对应的答案就是环上的长度，而对于树上的节点，其对应的答案则是其走到环上所需的步数再加上环的长度',
        quote_src='—— yiduobo 题解原文',
        idea=['每个点只有一条出边：形态是若干个环，环外挂着树',
              '第一阶段：从每个点出发一路走，==走到访问过的点==就停；若撞上的是本轮的点，就把环弹出来；剩下的路径反向接成树',
              '第二阶段：环上的点答案 = 环长；从每个环点往外 BFS，每深一层 +1'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`g` 是“环 → 外”方向的树（子节点集合），不是原图',
                 '`x not in g` 区分“新环”和“撞上旧部分”',
                 '`q` 在两个阶段含义不同：先当栈，后当 BFS 队列',
                 '对比灵神：灵神用拓扑排序剪枝找环，再在反图上 DFS；yiduobo 走路径找环，再 BFS'],
    ),
)
