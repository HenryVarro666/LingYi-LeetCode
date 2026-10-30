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
class Solution:
    def minTime(self, n: int, edges: List[List[int]]) -> int:
        g = [[] for _ in range(n)]
        for x, y, start, end in edges:
            g[x].append((y, start, end))

        dis = [inf] * n
        dis[0] = 0
        h = [(0, 0)]

        while h:
            dx, x = heappop(h)
            if dx > dis[x]:
                continue
            if x == n - 1:
                return dx
            for y, start, end in g[x]:
                new_dis = max(dx, start) + 1
                if new_dis - 1 <= end and new_dis < dis[y]:
                    dis[y] = new_dis
                    heappush(h, (new_dis, y))
        return -1
'''
FOR_LINE = _lineno(CODE, 'for y, start, end in g[x]')


def _inf(v):
    return '∞' if v == _m.inf else v


def _draw(cv, S, B, box, T):
    dis = S.get('dis')
    x = S.get('x') if 'dx' in S else None
    dx = S.get('dx')
    line = S.get('_line')
    y = S.get('y') if line in range(FOR_LINE, FOR_LINE + 6) else None
    ok = 'new_dis' in S and y is not None and line > FOR_LINE and S['new_dis'] - 1 <= S['end']

    def ncol(u):
        if dis is None or dis[u] == _m.inf:
            return T['panel2']
        if u == x:
            return T['blue']
        if dx is not None and dis[u] < dx:
            return T['green']
        return T['orange']

    def nsub(u):
        return None if dis is None else f'dis={_inf(dis[u])}'

    def ecol(u, v):
        if u == x and v == y:
            if line > FOR_LINE + 1 and 'new_dis' in S and not ok:
                return T['red'], 5
            return T['yellow'], 5
        return T['dim'], 3

    _graph(cv, T, box, POS, EDGES, ncol, nsub, ecol,
           '有向图（边标签 [start,end] = 可通行时间段；蓝 = 刚出堆，绿 = 已确定，橙 = 暂定）')


def _text(S, B):
    line = S.get('_line')
    if 'new_dis' in S and line is not None and line > FOR_LINE and S.get('y') is not None:
        return (f"边 `{S['x']}→{S['y']}` 时段 `[{S['start']},{S['end']}]`：出发 `max({S['dx']}, {S['start']}) = {max(S['dx'], S['start'])}`，"
                f"到达 =={S['new_dis']}==")
    if 'dx' in S:
        return f"刚出堆：`dx = {S['dx']}`，`x = {S['x']}`"
    return '堆里存 `(到达时间, 节点)`：每次弹出时间最早的节点'


def _skip(S, B, r):
    if S.dx > S.dis[S.x]:
        return f'`dx = {S.dx} > dis[{S.x}] = {S.dis[S.x]}`：==x 之前出堆过==，旧记录，跳过'
    return f'`dx = {S.dx} == dis[{S.x}]`：x ==首次出堆==，`dis[{S.x}]` 已最小，去更新邻居'


def _for(S, B, r):
    if 'y' in B and 'new_dis' in B and (B.y, B.start, B.end) == (S.y, S.start, S.end) and B.x == S.x:
        return f'`{S.x}` 的出边都看完了'
    return f'枚举 `{S.x}` 的出边 `{S.x} → {S.y}`，可用时段 `[{S.start}, {S.end}]`'


def _cmp(S, B, r):
    y = S.y
    if S.new_dis - 1 > S.end:
        return f'出发时间 `{S.new_dis - 1}` > `end = {S.end}`：==边已关闭==，走不了'
    if S.new_dis < S.dis[y]:
        return f'出发 `{S.new_dis - 1}` ≤ `end = {S.end}` 能走，且 `{S.new_dis} < dis[{y}] = {_inf(S.dis[y])}` → ==更新=='
    return f'边能走，但 `{S.new_dis} ≥ dis[{y}] = {S.dis[y]}`：不更优'


CONFIG = dict(
    num=3604, title='有向图中到达终点的最少时间', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='Dijkstra（动态边权）',
    tags=['灵神题单·图论算法', '难度分 1845'],
    code=CODE,
    call='Solution().minTime(4, %s)' % EDGES_IN,
    expect=5,
    skip=['for x, y, start, end in edges', 'g[x].append'],
    max_steps=80,
    views=[
        dict(type='text', fn=_text, h=56, size=24),
        dict(type='custom', draw=_draw, h=380),
        dict(type='array', var=lambda S: [_inf(v) for v in S['dis']] if 'dis' in S else None,
             label='dis[i]：到达 i 的最早时间', h=160, cell=90,
             color=lambda S, i, v: 'blue' if 'dx' in S and i == S['x'] else None),
        dict(type='heap', var='h', label='h（最小堆，元素 = (时间, 节点)）', h=130,
             fmt=lambda t: f'({t[0]},{t[1]})'),
    ],
    watch=[('dx', 'dx', 'blue'), ('x', 'x', 'blue'), ('y', 'y', 'yellow'), ('start', 'start'), ('end', 'end'),
           ('new_dis', 'new_dis', 'orange')],
    captions={
        'g = [[] for': '建邻接表：`g[x]` 存 `(y, start, end)`，只有出边',
        'dis = [inf] * n': '`dis[i]`：到达 i 的最早时间，先设为 ∞',
        'dis[0] = 0': '时间 0 从节点 `0` 出发',
        'h = [(0, 0)]': '起点 `(0, 0)` 入堆',
        'while h': lambda S, B, r: '堆非空，继续' if S.h else '堆空了：终点不可达',
        'dx, x = heappop': '弹出堆顶 `({dx}, {x})`：==到达时间最早==的节点',
        'if dx > dis[x]': _skip,
        'continue': '这条记录过时了：`x` 的邻居早被更早的时间更新过 → ==跳过==',
        'if x == n - 1': lambda S, B, r: f'`x = {S.x}` 是终点 `{S.n - 1}`：最早到达时间就是 `dx`' if S.x == S.n - 1 else f'`x = {S.x}` 不是终点 `{S.n - 1}`，继续扩展',
        'return dx': '终点首次出堆，最短时间 = =={dx}==',
        'for y, start, end in g[x]': _for,
        'new_dis = max': '边权是动态的：早到就==等到 start 再走==，出发 `max({dx}, {start}) = {new_dis - 1}`，到达 =={new_dis}==',
        'if new_dis - 1 <= end': _cmp,
        'dis[y] = new_dis': '更新 `dis[{y}]` = =={dis[y]}==',
        'heappush(h,': '`({new_dis}, {y})` 入堆（懒更新，旧记录出堆时被跳过）',
        'return -1': '堆空了仍没到终点 → 返回 `-1`',
    },
    cards=dict(
        one_liner='边权随到达时间动态变化，但始终非负，照样套 Dijkstra',
        complexity='时间 `O(n + m log m)`，空间 `O(n + m)`',
        problem=['有向图，边 `[u, v, start, end]` 只能在整数时刻 `start ≤ t ≤ end` 通过',
                 '时刻 0 从节点 0 出发，可以原地等待，每次移动花 1 个时间单位',
                 '求到达节点 `n-1` 的最少时间，不可达返回 `-1`',
                 '本视频：4 个节点、4 条边（示例 2）→ `5`'],
        quote='边权是动态计算的，即 max(dx, start) + 1 - dx。到达一个节点的时间早，边权就大；到达一个节点的时间晚，边权就小，最小是 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设 `dis[x]` 为到达 x 的最早时间；从 x 沿边走，出发时间 `max(dx, start)`',
              '出发时间必须 `≤ end`，到达时间 = 出发时间 + 1',
              '等价边权 `max(dx, start) + 1 - dx ≥ 1`，非负 → ==直接套 Dijkstra 模板=='],
        summary=['时间 `O(n + m log m)`，空间 `O(n + m)`',
                 '易错：判断条件写成 `new_dis - 1 <= end`（出发时间不超过 end），不是 `new_dis <= end`',
                 '易错：先判断 `x == n - 1` 再返回，终点首次出堆时才是最小值',
                 '同类题：3341/3342 到达最后一个房间的最少时间（网格里的动态边权）'],
    ),
)
