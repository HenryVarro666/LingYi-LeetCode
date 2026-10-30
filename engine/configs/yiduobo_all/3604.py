import math as _m


def _graph(cv, T, box, pos, edges, ncol, nsub, ecol, title, directed=True):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    R = 32
    L, Rr, Tp, Bt = x0 + 60, x1 - 60, y0 + 64 + R, y1 - R - 30
    P = {u: (L + fx * (Rr - L), Tp + fy * (Bt - Tp)) for u, (fx, fy) in pos.items()}
    for u, v, w in edges:
        c, wd = ecol(u, v)
        (ax, ay), (bx, by) = P[u], P[v]
        dd = _m.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / dd, (by - ay) / dd
        if directed:
            cv.arrow((ax + ux * R, ay + uy * R), (bx - ux * (R + 2), by - uy * (R + 2)), c, wd, 16)
        else:
            cv.line([(ax + ux * R, ay + uy * R), (bx - ux * R, by - uy * R)], c, wd)
        mx, my = (ax + bx) / 2 - uy * 20, (ay + by) / 2 + ux * 20
        wl = max(34, cv.tlen(str(w), 22, bold=True, mono=True) + 14)
        cv.rect((mx - wl / 2, my - 15, mx + wl / 2, my + 15), fill=T['bg'], r=6)
        cv.text((mx, my), w, 22, c if c != T['dim'] else T['muted'], anchor='mm', bold=True, mono=True)
    for u, (px, py) in P.items():
        fc = ncol(u)
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fc, outline=T['border'], width=2)
        cv.text((px, py), u, 28, T['bg'] if fc != T['panel2'] else T['text'], anchor='mm', bold=True)
        s = nsub(u)
        if s is not None:
            if py < (Tp + Bt) / 2 - 5:
                cv.text((px, py - R - 4), s, 20, T['yellow'], anchor='mb', bold=True, mono=True)
            else:
                cv.text((px, py + R + 4), s, 20, T['yellow'], anchor='mt', bold=True, mono=True)


def _lineno(code, needle):
    return [s.strip() for s in code.strip().split('\n')].index(needle) + 1 if False else \
        next(i for i, s in enumerate(code.strip().split('\n'), 1) if needle in s)


EDGES_IN = [[0, 1, 0, 3], [1, 3, 7, 8], [0, 2, 1, 5], [2, 3, 4, 7]]
POS = {0: (0.06, 0.5), 1: (0.5, 0.08), 2: (0.5, 0.92), 3: (0.94, 0.5)}
EDGES = [(u, v, f'[{s},{e}]') for u, v, s, e in EDGES_IN]
CODE = '''
class Solution(object):
    def minTime(self, n, edges):
        g = [[] for _ in range(n)]
        for u, v, start, end in edges:
            g[u].append((v, start, end))
        dis = [None] * n

        heap = [(0, 0)]
        while heap:
            d, now = heapq.heappop(heap)
            if dis[now] is None:
                dis[now] = d
                for v, start, end in g[now]:
                    if start > d:
                        heapq.heappush(heap, (start + 1, v))
                    elif start <= d <= end:
                        heapq.heappush(heap, (d + 1, v))

        if dis[-1] is None:
            return -1
        return dis[-1]
'''
FOR_LINE = _lineno(CODE, 'for v, start, end in g[now]')
END_LINE = _lineno(CODE, 'if dis[-1] is None')


def _d(v):
    return '?' if v is None else v


def _draw(cv, S, B, box, T):
    dis = S.get('dis')
    now = S.get('now') if 'd' in S else None
    line = S.get('_line')
    v = S.get('v') if line is not None and FOR_LINE <= line < END_LINE else None
    d = S.get('d')

    def ncol(u):
        if dis is None or dis[u] is None:
            return T['panel2']
        return T['blue'] if u == now else T['green']

    def nsub(u):
        return None if dis is None else f'dis={_d(dis[u])}'

    def ecol(a, b):
        if a == now and b == v and line > FOR_LINE:
            return (T['yellow'], 5)
        return (T['dim'], 3)

    _graph(cv, T, box, POS, EDGES, ncol, nsub, ecol,
           '有向图（边标签 [start,end] = 开放时段；蓝 = 刚出堆，绿 = 最短时间已确定）')


def _text(S, B):
    line = S.get('_line')
    if 'd' in S and line is not None and FOR_LINE < line < END_LINE and 'start' in S and S.get('v') is not None:
        s, e, d = S['start'], S['end'], S['d']
        if s > d:
            return f"边 `{S['now']}→{S['v']}` 时段 `[{s},{e}]`：`start = {s} > d = {d}`，==还没开==，等到 {s} 再走，到达 `{s + 1}`"
        if d <= e:
            return f"边 `{S['now']}→{S['v']}` 时段 `[{s},{e}]`：`{s} ≤ d = {d} ≤ {e}`，==已开放==，直接走，到达 `{d + 1}`"
        return f"边 `{S['now']}→{S['v']}` 时段 `[{s},{e}]`：`d = {d} > end`，==已关闭==，走不了"
    if 'd' in S:
        return f"刚出堆：`d = {S['d']}`，`now = {S['now']}`"
    return '堆里存 `(到达时间, 节点)`：每次弹出时间最早的'


def _first(S, B, r):
    if S.dis[S.now] is None:
        return f'`dis[{S.now}]` 还是空：`{S.now}` ==首次出堆==，最早到达时间 = `{S.d}`'
    return f'`dis[{S.now}] = {S.dis[S.now]}` 已有值：这是旧记录 → 丢弃'


def _for(S, B, r):
    if 'v' in B and 'now' in B and B.now == S.now and (B.v, B.start, B.end) == (S.v, S.start, S.end) and 'dis' in B and B.dis[S.now] is not None:
        return f'`{S.now}` 的出边都看完了'
    return f'枚举 `{S.now}` 的出边 `{S.now} → {S.v}`，开放时段 `[{S.start}, {S.end}]`'


def _push_wait(S, B, r):
    return f'边还没开放：==等到 `{S.start}` 再走==，到达 `({S.start}+1, {S.v}) = ({S.start + 1}, {S.v})` 入堆'


def _push_go(S, B, r):
    return f'边开放着：直接走，到达 `({S.d}+1, {S.v}) = ({S.d + 1}, {S.v})` 入堆'


CONFIG = dict(
    num=3604, title='有向图中到达终点的最少时间', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='Dijkstra（等待开放）',
    tags=['灵神题单·图论算法', '难度分 1845'],
    code=CODE,
    call='Solution().minTime(4, %s)' % EDGES_IN,
    expect=5,
    skip=['for u, v, start, end in edges', 'g[u].append'],
    max_steps=80,
    views=[
        dict(type='text', fn=_text, h=56, size=22),
        dict(type='custom', draw=_draw, h=380),
        dict(type='array', var=lambda S: [_d(v) for v in S['dis']] if 'dis' in S else None,
             label='dis[i]：最早到达时间（? = 还没确定）', h=160, cell=90,
             color=lambda S, i, v: 'blue' if 'd' in S and i == S['now'] else None),
        dict(type='heap', var='heap', label='heap（最小堆，元素 = (时间, 节点)）', h=130,
             fmt=lambda t: f'({t[0]},{t[1]})'),
    ],
    watch=[('d', 'd', 'blue'), ('now', 'now', 'blue'), ('v', 'v', 'yellow'), ('start', 'start'), ('end', 'end')],
    captions={
        'g = [[] for': '建邻接表：`g[u]` 存 `(v, start, end)`',
        'dis = [None] * n': '`dis[i]` 用 `None` 表示还没确定最短时间',
        'heap = [(0, 0)]': '时刻 0 在节点 0：`(0, 0)` 入堆',
        'while heap': lambda S, B, r: '堆非空，继续' if S.heap else '堆空了，开始看终点有没有被到达',
        'd, now = heapq.heappop': '弹出 `({d}, {now})`：堆里==时间最早==的',
        'if dis[now] is None': _first,
        'dis[now] = d': '`dis[{now}] = {d}`：确定下来，不会再变',
        'for v, start, end in g[now]': _for,
        'if start > d': lambda S, B, r: (f'`start = {S.start} > d = {S.d}`：边==还未开放==' if S.start > S.d else f'`start = {S.start} ≤ d = {S.d}`：边已经开了，再看有没有关'),
        'heapq.heappush(heap, (start + 1, v))': _push_wait,
        'elif start <= d <= end': lambda S, B, r: (f'`{S.start} ≤ {S.d} ≤ {S.end}` 成立：边开放中' if S.start <= S.d <= S.end else f'`d = {S.d} > end = {S.end}`：边==已关闭==，跳过'),
        'heapq.heappush(heap, (d + 1, v))': _push_go,
        'if dis[-1] is None': lambda S, B, r: '终点从没出堆 → 到不了' if S.dis[-1] is None else f'终点 `dis[-1] = {S.dis[-1]}` 已算出',
        'return -1': '终点不可达 → `-1`',
        'return dis[-1]': '到达终点的最少时间 =={dis[-1]}==',
    },
    cards=dict(
        one_liner='边没开就等到它开：到达时间 = start + 1',
        complexity='时间 `O(n + m log m)`，空间 `O(n + m)`',
        problem=['有向图，边 `[u, v, start, end]` 只在时刻 `start ~ end` 开放',
                 '时刻 0 从节点 0 出发，可以原地挂机，每次移动 1 个时间单位',
                 '求到达 `n-1` 的最少时间，到不了返回 `-1`',
                 '本视频：4 个节点、4 条边（示例 2）→ `5`'],
        quote='若对应边还未开放，那么就必须等到这条边开放然后再走，对应的时间为开放时间start再加上1；若对应边已经开放，那么就直接走过去，对应的时间为d + 1；若对应边已经关闭，那么就不能走了。',
        quote_src='—— yiduobo 题解原文',
        idea=['最短路的变种，仍用堆 + Dijkstra，只是更新到达时间的方式不同',
              '三种情况：`start > d` 等到 start；`start ≤ d ≤ end` 直接走；`d > end` 跳过',
              '节点首次出堆时 `dis` 才赋值（`None` 表示未确定），之后的旧记录直接忽略'],
        summary=['时间 `O(n + m log m)`，空间 `O(n + m)`',
                 '易错：`start > d` 时到达时间是 `start + 1`，不是 `d + 1`',
                 '易错：关闭的边要跳过，不能入堆',
                 '写法和灵神的区别：不维护 `dis` 做松弛，入堆不判断，出堆时用 `dis[now] is None` 去重'],
    ),
)
