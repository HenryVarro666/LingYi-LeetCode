import math as _m

ADJ = [[2, 4], [1, 3], [2, 4], [1, 3]]
POS = {1: (0, 0), 2: (1, 0), 3: (1, 1), 4: (0, 1)}   # 正方形布局

SETUP = '''
class Node(object):
    def __init__(self, val = 0, neighbors = []):
        self.val = val
        self.neighbors = neighbors

    def __repr__(self):
        return f'Node({self.val})'
'''


def _adj(node):
    """把克隆图还原成邻接表（用于校验答案）"""
    seen, order, q = {node.val: node}, [], [node]
    while q:
        x = q.pop()
        for y in x.neighbors:
            if y.val not in seen:
                seen[y.val] = y
                q.append(y)
    return [[y.val for y in seen[v].neighbors] for v in sorted(seen)]


def _graph(cv, cx, cy, size, title, edges, colors, T, arrows=False, present=None, ring=None):
    cv.text((cx, cy - size / 2 - 48), title, 22, T['muted'], anchor='mm', bold=True)
    pts = {v: (cx + (x - 0.5) * size, cy + (y - 0.5) * size) for v, (x, y) in POS.items()}
    R = 30
    for a, b, col in edges:
        (x0, y0), (x1, y1) = pts[a], pts[b]
        d = _m.hypot(x1 - x0, y1 - y0)
        ux, uy = (x1 - x0) / d, (y1 - y0) / d
        if arrows:   # 有向的“邻居列表”边：错开一点，两个方向都能看到
            ox, oy = -uy * 7, ux * 7
            cv.arrow((x0 + ux * R + ox, y0 + uy * R + oy), (x1 - ux * (R + 2) + ox, y1 - uy * (R + 2) + oy), col, 4, 12)
        else:
            cv.line([(x0 + ux * R, y0 + uy * R), (x1 - ux * R, y1 - uy * R)], col, 4)
    for v, (x, y) in pts.items():
        if present is not None and v not in present:
            cv.rect((x - R, y - R, x + R, y + R), outline=T['border'], width=2, r=R)
            continue
        fill = colors.get(v, T['panel2'])
        cv.rect((x - R, y - R, x + R, y + R), fill=fill, outline=ring.get(v) if ring and v in ring else T['border'],
                width=5 if ring and v in ring else 2, r=R)
        cv.text((x, y), v, 28, T['text'], anchor='mm', bold=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = S.get('g') or {}
    now, nb = S.get('now'), S.get('neighbor')
    nowv = now.val if now is not None else None
    nbv = nb.val if nb is not None and S['_line'] in (15, 16, 17, 20) else None
    size = min(200, (y1 - y0) - 130)
    cy = y0 + 70 + size / 2
    # 原图
    q = S.get('q') or []
    l = S.get('l', 0)
    qv = [x.val for x in q]
    col = {}
    for k, v in enumerate(qv):
        col[v] = (70, 76, 86) if k < l else (40, 84, 140)    # 已出队 / 在队列里
    ring = {}
    if nowv is not None:
        ring[nowv] = T['yellow']
    if nbv is not None:
        ring[nbv] = T['pink']
    edges = [(a, b, T['border']) for a in range(1, 5) for b in ADJ[a - 1] if a < b]
    _graph(cv, x0 + (x1 - x0) * 0.25, cy, size, '原图（蓝 = 在队列中，灰 = 已出队）', edges, col, T, ring=ring)
    # 新图
    cedges = []
    for v, c in g.items():
        for y in c.neighbors:
            hot = S['_line'] == 20 and v == nowv and y.val == nbv and c.neighbors and c.neighbors[-1] is y
            cedges.append((v, y.val, T['yellow'] if hot else T['cyan']))
    ccol = {v: (24, 110, 104) for v in g}
    _graph(cv, x0 + (x1 - x0) * 0.75, cy, size, '新图（g 中已建好的克隆节点）', cedges, ccol, T, arrows=True,
           present=set(g), ring={nowv: T['yellow']} if nowv in g else None)
    cv.arrow((x0 + (x1 - x0) * 0.47, cy), (x0 + (x1 - x0) * 0.53, cy), T['muted'], 3, 12)


def _while(S, B, ret):
    if B.l < B.r:
        return f'`l = {B.l} < r = {B.r}`：队列里还有节点没处理'
    return f'`l = r = {B.r}`：BFS 结束，所有节点都克隆好了'


def _if(S, B, ret):
    v = S.neighbor.val
    if v not in S.g:
        return f'`{v}` 不在 `g` 里 → 还没遍历到它，新图里也还没有它'
    return f'`{v}` 已在 `g` 里 → 新图中已有对应节点，不用再建'


def _nbs(S):
    if 'g' not in S:
        return None
    return {k: '[' + ','.join(str(y.val) for y in c.neighbors) + ']' for k, c in S['g'].items()}


CONFIG = dict(
    num=133, title='克隆图', difficulty='Medium', category='图论',
    author='yiduobo', technique='BFS + 用节点值作 key 的哈希表',
    tags=['面试经典150'],
    setup=SETUP,
    code='''
class Solution(object):
    def cloneGraph(self, node):

        if not node:
            return node

        g = {}
        g[node.val] = Node(node.val, [])
        q = [node]
        l = 0
        r = 1
        while l < r:
            now = q[l]
            l += 1
            for neighbor in now.neighbors:
                if neighbor.val not in g:
                    g[neighbor.val] = Node(neighbor.val, [])
                    q.append(neighbor)
                    r += 1
                g[now.val].neighbors.append(g[neighbor.val])

        return g[node.val]
''',
    call='''n = [Node(i, []) for i in range(5)]
for i, a in enumerate([[2, 4], [1, 3], [2, 4], [1, 3]], 1):
    n[i].neighbors = [n[j] for j in a]
Solution().cloneGraph(n[1])''',
    result_fn=_adj,
    expect=ADJ,
    skip=['l += 1', 'r += 1', 'q.append(neighbor)', 'l = 0', 'r = 1', 'if not node'],
    views=[
        dict(type='custom', draw=_draw, h=340),
        dict(type='array', var=lambda S: [x.val for x in S['q']] if 'q' in S else None, pointers={'l': 'blue'},
             label='q（BFS 队列，l 指向队首）', cell=70, h=150),
        dict(type='map', var=_nbs, label='g：值 → 新节点（显示它的邻居列表）', h=110, fmt=lambda k, v: f'{k}:{v}'),
    ],
    watch=[('now', lambda S: S['now'].val if S.get('now') else None, 'yellow'),
           ('neighbor', lambda S: S['neighbor'].val if S.get('neighbor') else None, 'pink'),
           ('l', 'l', 'blue'), ('r', 'r')],
    captions={
        'g = {}': '题目保证节点值 = 编号 → 用值作 key，`g` 存==新图中的节点==',
        'g[node.val] = Node(node.val, [])': '先给起点建好新节点：`g[{node.val}]`',
        'q = [node]': '从给定的 `node` 开始 BFS；`l`、`r` 是队首和队尾',
        'while l < r': _while,
        'now = q[l]': '出队 `now = {now.val}`，枚举它在原图中的邻居',
        'for neighbor in now.neighbors': lambda S, B, ret: (f'邻居 `neighbor = {S.neighbor.val}`'
                                                            if B.get('neighbor') is None or B['neighbor'].val != S['neighbor'].val or B.get('now').val != S['now'].val or B['_line'] != 15
                                                            else f'`{S.now.val}` 的邻居枚举完'),
        'if neighbor.val not in g': _if,
        'g[neighbor.val] = Node': '在新图里建出 `{neighbor.val}`，存进 `g`，原节点 `{neighbor.val}` 入队',
        'g[now.val].neighbors.append': '`g[{now.val}].neighbors.append(g[{neighbor.val}])`：新图连边 `{now.val} → {neighbor.val}`',
        'return g[node.val]': '返回 `node` 在新图中的对应节点 `g[{node.val}]`',
    },
    max_steps=70,
    cards=dict(
        one_liner='BFS 原图，用值作 key 的 dict 存新图节点，边跟着连',
        complexity='时间 `O(n + m)`，空间 `O(n)`',
        problem=['给无向连通图中一个节点的引用，返回该图的==深拷贝==（克隆）',
                 '每个节点有 `val` 和邻居列表 `neighbors`；节点值 = 编号（1..n）',
                 '示例：`adjList = [[2,4],[1,3],[2,4],[1,3]]` → 结构相同的新图'],
        quote='若neighbor.val没有在dict中，说明未遍历到neighbor，新图中还没有neighbor对应的节点……于是就有==dict[now.val].neighbor.append(dict[neighbor.val])==。',
        quote_src='—— yiduobo 题解原文',
        idea=['节点值和索引相同 → 用值作 key，`dict` 储存新图节点',
              'BFS 到 `now`：邻居不在 dict 中就新建并入队',
              '再把邻居的新节点加入 `now` 新节点的邻居列表'],
        result='新图邻接表 `[[2,4],[1,3],[2,4],[1,3]]`，和原图一模一样 ✓',
        summary=['时间 `O(n + m)`：每个点入队一次，每条边两个方向各连一次',
                 '先建节点、再连边：连边时邻居的新节点一定已存在',
                 '`neighbor` 已在 dict 里也要连边，只是不再入队',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串；`Node` 类按 LeetCode 定义预置'],
    ),
)
