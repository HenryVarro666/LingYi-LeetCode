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
    dec = 2 - sum(S['ind'])
    before = sum(len(S['g'][p]) for p in S['q'][:S['l'] - 1])
    return dec - before, list(S['g'][S['now']])


RC = [[1, 2], [3, 2]]
CC = [[2, 1], [3, 2]]
POS = {1: (0.0, 0.85), 3: (0.5, 0.05), 2: (1.0, 0.85)}


def _draw(cv, S, B, box, T):
    outer = 'edges' not in S
    edges = S.get('edges') if not outer else (CC if isinstance(S.get('x'), list) else RC)
    is_row = [list(e) for e in edges] == RC
    st, sub = {}, {}
    q, ind = S.get('q'), S.get('ind')
    if outer:
        rk = S.get('y') if isinstance(S.get('y'), list) else S.get('x')
        for v in POS:
            if isinstance(rk, list) and len(rk) > v:
                st[v] = 'green'
                sub[v] = f'第 {rk[v]} 位'
    else:
        for v in POS:
            if q is not None and v in q:
                st[v] = 'green' if (S.get('_line', 0) >= 28 or q.index(v) < S.get('l', 0)) else 'cyan'
                if q.index(v) < S.get('l', 0) or S.get('_line', 0) >= 28:
                    sub[v] = f'第 {q.index(v)} 位'
            if ind is not None and v not in sub:
                sub[v] = f'入度 {ind[v]}'
    hot = None
    line = S.get('_line', 0)
    if not outer:
        if 'q' not in S and 'x' in S and 'y' in S and 9 <= line <= 11:
            hot = (S['x'], S['y'])
        elif 'now' in S and 'next' in S and 22 <= line <= 26:
            hot = (S['now'], S['next'])
    name = '行约束（above → below）' if is_row else '列约束（left → right）'
    _gdraw(cv, box, T, POS, [tuple(e) for e in edges], st, sub, hot, name + ' 青 = 在队列 绿 = 已排好', R=30)


CONFIG = dict(
    num=2392, title='给定条件下构造矩阵', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='行、列各做一次拓扑排序（BFS 数组队列）',
    tags=['灵神题单', '图论算法', '难度分 1961'],
    code='''
class Solution(object):
    def buildMatrix(self, k, rowConditions, colConditions):

        def get_order(edges):
            g = {num : set() for num in range(1, k + 1)}
            ind = [0] * (k + 1)

            for x, y in edges:
                if y not in g[x]:
                    g[x].add(y)
                    ind[y] += 1
            
            q = []
            for num in range(1, k + 1):
                if ind[num] == 0:
                    q.append(num)
            
            l, r = 0, len(q)
            while l < r:
                now = q[l]
                l += 1
                for next in g[now]:
                    ind[next] -= 1
                    if ind[next] == 0:
                        q.append(next)
                        r += 1

            if len(q) < k:
                return []

            res = [0] * (k + 1)
            for index in range(k):
                res[q[index]] = index
            
            return res
        
        x = get_order(rowConditions)
        y = get_order(colConditions)

        if len(x) < k or len(y) < k:
            return []

        res = [[0] * k for _ in range(k)]
        for num in range(1, k + 1):
            res[x[num]][y[num]] = num
        
        return res
''',
    call='Solution().buildMatrix(3, [[1,2],[3,2]], [[2,1],[3,2]])',
    expect=[[0, 0, 1], [3, 0, 0], [0, 2, 0]],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='q', label='q（拓扑序，l = 队首，r = 队尾后一位）', pointers={'l': 'blue', 'r': 'pink'}, h=190),
        dict(type='grid', var=lambda S: S['res'] if isinstance(S.get('res'), list) and S['res'] and isinstance(S['res'][0], list) else None,
             label='res（矩阵）', h=200, color=lambda S, i, j, v: 'green' if v else None),
    ],
    watch=[('ind', 'ind', 'orange'), ('l', 'l', 'blue'), ('r', 'r', 'pink')],
    max_steps=130,
    skip=['g = {num', 'ind = [0]', 'q = []', 'for x, y in edges', 'l += 1', 'r += 1', 'for index in range(k)', 'res = [0] * (k + 1)', 'if y not in g[x]', 'if ind[next] == 0', 'for num in range(1, k + 1)'],
    captions={
        'g[x].add(y)': '约束 `{x}` 在 `{y}` 前 → 连边 `{x} → {y}`（`set` 去重）：`g[{x}]` = {g[x]}',
        'ind[y] += 1': '`{y}` 前面多一个要求 → `ind[{y}]` = =={ind[y]}==',
        'if ind[num] == 0': lambda S, B, r: (f'数字 `{S.num}`：`ind = 0`，没有谁要求它靠后 → ==先入队==' if S.ind[S.num] == 0
                                             else f'数字 `{S.num}`：`ind = {S.ind[S.num]}`，要等前面的数字'),
        'q.append(num)': '`{num}` 入队：`q` = {q}（孤立点也在这里入队）',
        'l, r = 0, len(q)': '`[l, r)` 是待处理的队列区间：`l = {l}`，`r = {r}`',
        'while l < r': lambda S, B, r_: (f'`l = {S.l} < r = {S.r}`，队里还有数字没处理' if S.l < S.r else f'`l = {S.l} = r`：队列处理完'),
        'now = q[l]': '取队首 `now = {now}`：它排在拓扑序第 `{l}` 位，`l` 随后右移出队',
        'for next in g[now]': lambda S, B, r_: (lambda kk, lst: (
            f'`{S.now}` 不指向任何数字，直接跳过' if not lst else
            '它指向的数字都处理完了，回到 while' if kk >= len(lst) else
            f'`{S.now}` 排好了，解除它对 `{lst[kk]}` 的约束' if kk == 0 else f'再解除它对 `{lst[kk]}` 的约束'))(*_k(S)),
        'ind[next] -= 1': lambda S, B, r_: f'`{S.next}` 少一个前置要求：`ind[{S.next}]` = =={S.ind[S.next]}==' + ('，要求全满足 → ==入队==' if S.ind[S.next] == 0 else '，还要等别的数字'),
        'q.append(next)': '`{next}` 入队：`q` = {q}，队尾 `r` 随后右移',
        'if len(q) < k': lambda S, B, r_: (f'`len(q) = {len(S.q)} < k` → 有环，无解，返回空' if len(S.q) < S.k
                                           else f'`len(q) = {len(S.q)} = k` → 没有环，每个数字都排上了：拓扑序 `{S.q}`，下面把它转成「数字 → 位置」'),
        'res = [0] * (k + 1)': '`res[num]` 记录数字 `num` 在拓扑序里排第几',
        'x = get_order': '`x[num]`：数字 `num` 所在的==行== = {x}',
        'y = get_order': '`y[num]`：数字 `num` 所在的==列== = {y}',
        'if len(x) < k': '行、列都能排出顺序（长度够 `k`），继续',
        'res = [[0]': '`k × k` 的全 0 矩阵',
        'res[q[index]] = index': '数字 `{q[index]}` 排第 `{index}` 位',
        'res[x[num]][y[num]]': '数字 `{num}` 放到 第 `{x[num]}` 行、第 `{y[num]}` 列',
        'return res': lambda S, B, r_: (f'矩阵 `{S.res}`' if isinstance(S.res[0], list) else f'`res[num]` = 数字 `num` 的位置：`{S.res}`'),
    },
    cards=dict(
        one_liner='行列互不影响：各自拓扑排序，序号就是行号、列号',
        complexity='时间 `O(k² + n + m)`，空间 `O(k + n + m)`',
        problem=['在 `k × k` 矩阵里放 `1 ~ k` 各一次，其余为 0',
                 '`rowConditions` 要求 above 所在行在 below 上面，`colConditions` 要求 left 在 right 左边',
                 '本视频：`k=3`，行 `[[1,2],[3,2]]`，列 `[[2,1],[3,2]]`'],
        quote='题目中的行和列是互补影响的，那么可以将行和列分开来考虑。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个数当节点，(above, below) 当作 above → below 的有向边',
              '拓扑序里 above 一定在 below 前面，所以==拓扑序号直接当行号==',
              '列同理；任一方向拓扑序不足 `k` 说明有环，返回空矩阵'],
        summary=['时间 `O(k² + n + m)`，两次拓扑排序加 `k × k` 矩阵',
                 '`g` 用 `set` 去重，重复约束不会多算入度',
                 '`get_order` 返回的 `res[num]` 是数字的行号（或列号），无解时返回 `[]`',
                 '原文本身是 Python 3 可运行的写法，代码未改动',
                 '对比灵神：灵神返回拓扑序 `order`，yiduobo 直接返回「数字 → 位置」'],
    ),
)
