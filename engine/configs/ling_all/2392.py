import math as _m


def _gdraw(cv, box, T, pos, edges, state, sub=None, hot=None, title='', R=30, fs=26):
    """有向图：pos={名字:(fx,fy)}，edges=[(a,b)]，state={名字:颜色名或None}，sub={名字:下方小字}，hot=高亮边 (a,b)"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    half = {k: max(R, (cv.tlen(k, fs, bold=True) + 30) / 2) for k in pos}
    mx = max(half.values())
    w, h = x1 - x0 - 2 * mx - 40, y1 - y0 - 2 * R - 100
    P = {k: (x0 + 20 + mx + fx * w, y0 + 50 + R + fy * h) for k, (fx, fy) in pos.items()}

    def edge_pt(k, ux, uy, pad):
        a, b = half[k] + pad, R + pad
        t = 1 / _m.sqrt((ux / a) ** 2 + (uy / b) ** 2)
        return t

    for a, b in edges:
        if a not in P or b not in P:
            continue
        (ax, ay), (bx, by) = P[a], P[b]
        d = _m.hypot(bx - ax, by - ay) or 1
        ux, uy = (bx - ax) / d, (by - ay) / d
        ta, tb = edge_pt(a, ux, uy, 3), edge_pt(b, ux, uy, 6)
        on = hot is not None and (a, b) == tuple(hot)
        cv.arrow((ax + ux * ta, ay + uy * ta), (bx - ux * tb, by - uy * tb),
                 T['yellow'] if on else T['dim'], width=6 if on else 3, head=16 if on else 13)
    for k, (cx, cy) in P.items():
        c = state.get(k)
        fill = T[c] if c else T['panel2']
        cv.rect((cx - half[k], cy - R, cx + half[k], cy + R), fill=fill, outline=T['border'], width=3, r=R)
        cv.text((cx, cy), k, fs, T['bg'] if c else T['text'], anchor='mm', bold=True)
        if sub and sub.get(k) not in (None, ''):
            cv.text((cx, cy + R + 6), sub[k], 22, T['muted'], anchor='mt', bold=True)


def _k(S):
    """当前这次出队里已解除了几个约束，以及 g[x]"""
    dec = len(S['edges']) - sum(S['in_deg'])
    before = sum(len(S['g'][p]) for p in S['order'][:-1])
    return dec - before, S['g'][S['x']]


RC = [[1, 2], [3, 2]]
CC = [[2, 1], [3, 2]]
POS = {1: (0.0, 0.85), 3: (0.5, 0.05), 2: (1.0, 0.85)}


def _draw(cv, S, B, box, T):
    edges = S.get('edges')
    outer = edges is None
    if outer:
        edges = CC if 'row' in S else RC
    is_row = edges == RC
    order = S.get('order')
    if outer:
        order = S.get('row') if is_row else S.get('col')
    in_deg, q = S.get('in_deg'), S.get('q')
    st, sub = {}, {}
    for v in POS:
        i = v - 1
        if q is not None and i in q:
            st[v] = 'cyan'
        if order is not None and i in order:
            st[v] = 'green'
            sub[v] = f'第 {order.index(i)} 位'
        elif in_deg is not None and not outer:
            sub[v] = f'入度 {in_deg[i]}'
    hot = None
    if 'x' in S and 'y' in S and not outer and 'order' in S and 14 <= S.get('_line', 0) <= 17:
        kk, lst = _k(S)
        if S['_line'] > 14 or kk < len(lst):
            hot = (S['x'] + 1, S['y'] + 1)
    elif 'x' in S and 'y' in S and not outer and 'order' not in S:
        hot = (S['x'], S['y'])
    name = '行约束（above → below）青 = 在队列 绿 = 已排好' if is_row else '列约束（left → right）青 = 在队列 绿 = 已排好'
    _gdraw(cv, box, T, POS, [tuple(e) for e in edges], st, sub, hot, name, R=30)


CONFIG = dict(
    num=2392, title='给定条件下构造矩阵', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='行、列分别拓扑排序',
    tags=['灵神题单', '图论算法', '难度分 1961'],
    code='''
class Solution:
    def buildMatrix(self, k: int, rowConditions: List[List[int]], colConditions: List[List[int]]) -> List[List[int]]:
        def topo_sort(edges: List[List[int]]) -> List[int]:
            g = [[] for _ in range(k)]
            in_deg = [0] * k
            for x, y in edges:
                g[x - 1].append(y - 1)  # 顶点编号从 0 开始，方便计算
                in_deg[y - 1] += 1
            order = []
            q = deque(i for i, d in enumerate(in_deg) if d == 0)
            while q:
                x = q.popleft()
                order.append(x)
                for y in g[x]:
                    in_deg[y] -= 1
                    if in_deg[y] == 0:
                        q.append(y)
            return order if len(order) == k else None

        if (row := topo_sort(rowConditions)) is None or (col := topo_sort(colConditions)) is None:
            return []
        pos = {x: i for i, x in enumerate(col)}
        ans = [[0] * k for _ in range(k)]
        for i, x in enumerate(row):
            ans[i][pos[x]] = x + 1
        return ans
''',
    call='Solution().buildMatrix(3, [[1,2],[3,2]], [[2,1],[3,2]])',
    expect=[[0, 0, 1], [3, 0, 0], [0, 2, 0]],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='order', label='order（拓扑序，存的是 数字 − 1）', h=170),
        dict(type='grid', var='ans', label='ans', h=230, color=lambda S, i, j, v: 'green' if v else None),
    ],
    watch=[('in_deg', 'in_deg', 'orange'), ('q', 'list(q)', 'yellow'), ('row', 'row', 'cyan'), ('col', 'col', 'purple')],
    max_steps=130,
    captions={
        'g = [[] for': '`g[x]`：数字 x（下标）要排在哪些数字前面',
        'in_deg = [0]': '`in_deg[y]`：有几个数字必须排在 y 前面',
        'for x, y in edges': lambda S, B, r: (f'这张图的 {len(S.edges)} 条约束都连好了' if B.get('x') == S.x and B.get('y') == S.y and B.get('g') == S.g
                                              else f'约束 `{S.x} 在 {S.y} 前`'),
        'g[x - 1].append': '连边 `{x} → {y}`，下标从 0 起：`g[{x-1}]` = {g[x-1]}',
        'in_deg[y - 1] += 1': '`{y}` 前面多了一个要求 → `in_deg[{y-1}]` = =={in_deg[y-1]}==',
        'order = []': '`order` 就是要求的相对顺序',
        'q = deque': '入度 0 = 没有任何约束要它靠后 → 先入队：`{list(q)}`（孤立点也在这里入队）',
        'while q': lambda S, B, r: (f'队列里还有 `{list(S.q)}`' if S.q else '队列空了：能排的都排完了'),
        'x = q.popleft()': '取出数字 `{x+1}`：它前面的要求都满足了，排到下一位',
        'order.append(x)': '`order` = {order}（数字 +1 才是题目里的数）',
        'for y in g[x]': lambda S, B, r: (lambda kk, lst: (
            f'数字 `{S.x + 1}` 不用约束任何后面的数字' if not lst else
            '它指向的数字都处理完了，回到 while' if kk >= len(lst) else
            (f'`{S.x + 1}` 排好了，解除它对 `{lst[kk] + 1}` 的约束' if kk == 0 else f'再解除它对 `{lst[kk] + 1}` 的约束')))(*_k(S)),
        'in_deg[y] -= 1': '数字 `{y+1}` 少一个前置要求：`in_deg[{y}]` = =={in_deg[y]}==',
        'if in_deg[y] == 0': lambda S, B, r: (f'数字 `{S.y+1}` 的 `in_deg` = 0：要求全满足 → ==入队==' if S.in_deg[S.y] == 0
                                              else f'数字 `{S.y+1}` 的 `in_deg` = {S.in_deg[S.y]} > 0：还要等别的数字'),
        'q.append(y)': '数字 `{y+1}` 入队：队列 `{list(q)}`',
        'return order if': lambda S, B, r: (f'`len(order) = {len(S.order)} == k` → 没有环，返回拓扑序 `{S.order}`' if len(S.order) == S.k
                                            else f'`len(order) = {len(S.order)} < k` → 有环，无解，返回 None'),
        'if (row := ': lambda S, B, r: ('行、列都有合法顺序，继续构造' if S.get('row') is not None and S.get('col') is not None
                                        else ('行顺序 `row` 算好了，再算列顺序' if S.get('row') is not None else '先对 `rowConditions` 拓扑排序')),
        'pos = ': '`pos[x]`：数字 x（下标）该放在第几列 = {pos}',
        'ans = [[0]': '`k × k` 的全 0 矩阵',
        'for i, x in enumerate(row)': lambda S, B, r: (f'第 `{S.i}` 行放数字 `{S.x + 1}`' if B.get('i') != S.i or B.get('x') != S.x else '每一行都放好了'),
        'ans[i][pos[x]]': '数字 `{x+1}`：行 = `{i}`（row 里的位置），列 = `{pos[x]}`（col 里的位置）',
        'return ans': '行列约束分开满足，矩阵 `{ans}`',
    },
    cards=dict(
        one_liner='行和列互不干扰：各做一次拓扑排序，再拼起来',
        complexity='时间 `O(k² + n + m)`，空间 `O(k + n + m)`',
        problem=['在 `k × k` 矩阵里放 `1 ~ k` 各一次，其余为 0',
                 '`rowConditions` 要求 above 所在行在 below 上面，`colConditions` 要求 left 在 right 左边',
                 '本视频：`k=3`，行 `[[1,2],[3,2]]`，列 `[[2,1],[3,2]]`'],
        quote='数字之间的约束只发生在行与行、列于列，而行与列之间没有直接约束。',
        quote_src='—— 灵茶山艾府题解',
        idea=['行约束连成有向图，拓扑序 = 每一行放哪个数字',
              '列约束同理，拓扑序 = 每一列放哪个数字',
              '拓扑序长度不足 `k` = 图里有环 = 无解；孤立点入度为 0，自动入队'],
        summary=['时间 `O(k² + n + m)`：两次拓扑排序加填 `k × k` 矩阵',
                 '顶点编号用 `x - 1` 从 0 开始，放进矩阵时要 `+ 1` 还原',
                 '答案不唯一，本例得到的矩阵和题面示例不同但同样合法',
                 '同类题：210 课程表 II、310 最小高度树'],
    ),
)
