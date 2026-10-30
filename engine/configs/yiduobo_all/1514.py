import math as _m

N = 4
EDGES = [[0, 1], [1, 2], [0, 2], [2, 3], [1, 3]]
PROB = [0.5, 0.5, 0.2, 0.8, 0.1]
START, END = 0, 3
POS = {0: (0.04, 0.5), 1: (0.42, 0.06), 2: (0.42, 0.94), 3: (0.96, 0.5)}
INIT = (15, 16)
LOOP = (26, 27, 28)


def _g(x):
    return f'{x:.4g}'


def _graph(cv, T, box, pos, edges, ncol, ecol, title):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    R = 32
    L, Rr, Tp, Bt = x0 + 70, x1 - 70, y0 + 64 + R, y1 - R - 30
    P = {u: (L + fx * (Rr - L), Tp + fy * (Bt - Tp)) for u, (fx, fy) in pos.items()}
    for u, v, w in edges:
        c, wd = ecol(u, v)
        (ax, ay), (bx, by) = P[u], P[v]
        dd = _m.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / dd, (by - ay) / dd
        cv.line([(ax + ux * R, ay + uy * R), (bx - ux * R, by - uy * R)], c, wd)
        mx, my = (ax + bx) / 2 - uy * 22, (ay + by) / 2 + ux * 22
        cv.rect((mx - 26, my - 15, mx + 26, my + 15), fill=T['bg'], r=6)
        cv.text((mx, my), w, 22, c if c != T['dim'] else T['muted'], anchor='mm', bold=True, mono=True)
    for u, (px, py) in P.items():
        fc = ncol(u)
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fc, outline=T['border'], width=2)
        cv.text((px, py), u, 28, T['bg'] if fc != T['panel2'] else T['text'], anchor='mm', bold=True)
        tag = '起点' if u == START else '终点' if u == END else None
        if tag:
            if py < (Tp + Bt) / 2 - 5:
                cv.text((px, py - R - 4), tag, 20, T['yellow'], anchor='mb', bold=True)
            else:
                cv.text((px, py + R + 4), tag, 20, T['yellow'], anchor='mt', bold=True)


def _draw(cv, S, B, box, T):
    line = S.get('_line')
    used = S.get('used')
    now = S.get('now') if 'now' in S else None
    if line in INIT:
        a, b = START, S.get('next')
    elif line in LOOP:
        a, b = now, S.get('next')
    else:
        a = b = None

    def ncol(u):
        if u == now and line not in INIT:
            return T['blue']
        if used is not None and u in used:
            return T['green']
        return T['panel2']

    def ecol(u, v):
        if {u, v} == {a, b}:
            return T['yellow'], 5
        return T['dim'], 3

    _graph(cv, T, box, POS, [(x, y, p) for (x, y), p in zip(EDGES, PROB)], ncol, ecol,
           '无向图，边上是成功概率（蓝 = 刚弹出的 now，绿 = 已处理 used）')


def _text(S):
    h = S.get('heap')
    if h is None:
        return '路径概率 = 路径上各边概率的==乘积==，求起点到终点的最大值'
    if not h:
        return '堆是空的'
    top = min(h)
    return f"堆里存 `[-概率, 点]`：堆顶 `[{_g(top[0])}, {top[1]}]` = 概率==最大==的点 `{top[1]}`（{_g(-top[0])}）"


def _for(items, S, B, a, b):
    items = list(items)
    cur = (S.get(a), S.get(b))
    if cur not in items:
        return None
    if a in B and b in B and (B[a], B[b]) == cur:
        return 'done'
    return 'go'


def _init_for(S, B, r):
    k = _for(S.g.get(S.start, {}).items(), S, B, 'next', 'v')
    if k == 'go':
        return f'起点的邻居 `{S.next}`，边的概率 `{_g(S.v)}`'
    return '起点的邻居都入堆了'


def _loop_for(S, B, r):
    k = _for(S.g.get(S.now, {}).items(), S, B, 'next', 'w')
    if k is None:
        return f'`{S.now}` 没有邻居'
    if k == 'done':
        return f'`{S.now}` 的邻居都看完了'
    return f'看 `{S.now}` 的邻居 `{S.next}`，边的概率 `{_g(S.w)}`'


def _isend(S, B, r):
    if S.now == S.end:
        return f'弹出的 `{S.now}` ==就是终点==！'
    return f'`{S.now}` 不是终点 `{S.end}`'


def _notused(S, B, r):
    if S.now in S.used:
        return f'`{S.now}` ==已处理过==：这是概率更小的旧记录 → 丢掉'
    return f'`{S.now}` 第一次弹出：它的最大概率就是 `{_g(-S.v)}`，用它去更新邻居'


CONFIG = dict(
    num=1514, title='概率最大的路径', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='Dijkstra（最大堆存概率）',
    tags=['labuladong', '灵神题单·图论算法'],
    code='''
class Solution(object):
    def maxProbability(self, n, edges, succProb, start, end):
        g = {}
        m = len(edges)
        for index in range(m):
            x, y = edges[index]
            v = succProb[index]
            if x not in g:
                g[x] = {}
            if y not in g:
                g[y] = {}
            g[x][y] = g[y][x] = v

        heap = []
        for next, v in g.get(start, {}).items():
            heapq.heappush(heap, [-v, next])

        used = set([start])
        while heap:
            v, now = heapq.heappop(heap)
            if now == end:
                return -v

            if now not in used:
                used.add(now)
                for next, w in g.get(now, {}).items():
                    if next not in used:
                        heapq.heappush(heap, [v * w, next])

        return 0.0
''',
    call=f'Solution().maxProbability({N}, {EDGES}, {PROB}, {START}, {END})',
    expect=0.2,
    skip=['m = len(edges)', 'for index in range(m)', 'x, y = edges[index]', 'v = succProb[index]',
          'if x not in g', 'g[x] = {}', 'if y not in g', 'g[y] = {}', 'g[x][y] = g[y][x]'],
    views=[
        dict(type='text', fn=_text, h=56, size=24),
        dict(type='custom', draw=_draw, h=420),
        dict(type='heap', var='heap', label='heap（元素 = [-概率, 点]）', h=130,
             fmt=lambda t: f'[{_g(t[0])},{t[1]}]'),
        dict(type='set', var='used', label='used（已处理的点）', h=110),
    ],
    watch=[('now', 'now', 'blue'), ('概率 -v', lambda S: round(-S['v'], 4) if S.get('_line', 0) >= 20 and 'now' in S else None, 'orange'),
           ('next', 'next', 'yellow'), ('w', 'w')],
    captions={
        'g = {}': '无向图：`g[x][y] = g[y][x] = 概率`（已建好）',
        'heap = []': '堆存 `[-概率, 点]`：最小堆取负 → ==弹出的是概率最大的==',
        'for next, v in g.get(start': _init_for,
        'heapq.heappush(heap, [-v, next])': lambda S, B, r: f'`[{_g(-S.v)}, {S.next}]` 入堆：从起点一步到 `{S.next}` 的概率',
        'used = set([start])': '起点 `{start}` 已处理',
        'while heap': lambda S, B, r: '堆非空，继续' if S.heap else '堆空了：到不了终点',
        'v, now = heapq.heappop': lambda S, B, r: f'弹出 `[{_g(S.v)}, {S.now}]`：当前概率==最大==的点 `{S.now}`，概率 `{_g(-S.v)}`',
        'if now == end': _isend,
        'return -v': lambda S, B, r: f'概率只会越乘越小，第一次弹出终点时就是==最大概率==：返回 `{_g(r)}`',
        'if now not in used': _notused,
        'used.add(now)': '`{now}` 加入 `used`',
        'for next, w in g.get(now': _loop_for,
        'if next not in used': lambda S, B, r: (f'`{S.next}` 已处理，跳过' if S.next in S.used
                                                else f'`{S.next}` 还没处理 → 可以从 `{S.now}` 走过去'),
        'heapq.heappush(heap, [v * w, next])': lambda S, B, r: (
            f'`{_g(-S.v)} × {_g(S.w)} = {_g(-S.v * S.w)}`：`[{_g(S.v * S.w)}, {S.next}]` 入堆（`v` 是负数，乘完仍是负数）'),
        'return 0.0': '起点到不了终点，返回 `0`',
    },
    cards=dict(
        one_liner='概率越乘越小，满足“三角形不等式” → 用 Dijkstra 每次取概率最大的点',
        complexity='时间 `O(m log m)`，空间 `O(n + m)`',
        problem=['`n` 个点的无向图，`edges[i] = [a, b]` 这条边的成功概率是 `succProb[i]`',
                 '求从 `start` 到 `end` 成功概率最大的路径（概率 = 各边概率相乘），到不了返回 `0`',
                 '示例：`n=3, edges=[[0,1],[1,2],[0,2]], succProb=[0.5,0.5,0.2]`，0 → 2 答案 `0.25`',
                 '本视频：4 个点、5 条边，0 → 3，答案 `0.2`'],
        quote='边上的为概率值，也就是说这些值的范围在0到1之间，那么这里实际上是==满足三角形不等式的==，因此就可以使用基于贪心算法的dijkstra算法来解决这个问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['概率都在 `[0, 1]`：多乘一条边只会变小，就像最短路里多走一条边只会变长',
              '每次找剩余点中==概率最大==的点：堆里存 `-概率`，最小堆弹出的就是最大概率',
              '直到弹出 `end` 为止，那时的概率就是答案'],
        summary=['时间 `O(m log m)`：每条边的端点至多入堆一次',
                 '取负技巧：`heapq` 是最小堆，存 `-p`；`v * w` 中 `v` 已是负数，乘积仍为负',
                 '起点不入堆，而是先把起点的邻居入堆，并把起点放进 `used`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
