import math as _m


def _graph(cv, T, box, pos, edges, ncol, nsub, ecol, title, directed=True):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    R = 30
    L, Rr, Tp, Bt = x0 + 70, x1 - 70, y0 + 70 + R, y1 - R - 34
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
        cv.rect((mx - 17, my - 15, mx + 17, my + 15), fill=T['bg'], r=6)
        cv.text((mx, my), w, 22, c if c != T['dim'] else T['muted'], anchor='mm', bold=True, mono=True)
    for u, (px, py) in pos.items():
        px, py = P[u]
        fc = ncol(u)
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fc, outline=T['border'], width=2)
        cv.text((px, py), u, 28, T['bg'] if fc != T['panel2'] else T['text'], anchor='mm', bold=True)
        s = nsub(u)
        if s is not None:
            if py < (Tp + Bt) / 2 - 5:
                cv.text((px, py - R - 4), s, 20, T['yellow'], anchor='mb', bold=True, mono=True)
            else:
                cv.text((px, py + R + 4), s, 20, T['yellow'], anchor='mt', bold=True, mono=True)

N = 5
EDGES = [(0, 1, 2), (1, 2, 1), (0, 2, 4), (2, 3, 1), (3, 4, 3)]
DISAPPEAR = [1, 2, 5, 6, 9]
POS = {0: (0.02, 0.5), 1: (0.3, 0.04), 2: (0.34, 0.96), 3: (0.68, 0.5), 4: (0.98, 0.5)}

CODE = '''
class Solution(object):
    def minimumTime(self, n, edges, disappear):

        g = [{} for _ in range(n)]
        for x, y, w in edges:
            if y not in g[x] or g[x][y] > w:
                g[x][y] = g[y][x] = w
        
        dis = [-1] * n
        heap = [[0, 0]]
        while heap:
            d, x = heapq.heappop(heap)
            if dis[x] == -1:
                dis[x] = d
                for y, w in g[x].items():
                    if dis[y] == -1 and dis[x] + w < disappear[y]:
                        heapq.heappush(heap, [dis[x] + w, y])
        
        return dis
'''
_L = CODE.strip('\n').split('\n')
FOR_LINE = next(i + 1 for i, l in enumerate(_L) if 'for y, w in g[x].items()' in l)


def _draw(cv, S, B, box, T):
    dis = S.get('dis')
    line = S.get('_line')
    heap = S.get('heap') or []
    inheap = {e[1] for e in heap}
    x = S.get('x') if 'd' in S else None
    y = S.get('y') if line in (FOR_LINE, FOR_LINE + 1, FOR_LINE + 2) else None
    end = line == len(_L)

    def ncol(u):
        if dis is None:
            return T['panel2']
        if u == x and line is not None and FOR_LINE - 4 <= line <= FOR_LINE + 2:
            return T['blue']
        if dis[u] != -1:
            return T['green']
        if u in inheap:
            return T['orange']
        return T['panel2']

    def nsub(u):
        d = '?' if dis is None else ('-' if dis[u] < 0 else dis[u])
        return f'dis={d}  消失@{DISAPPEAR[u]}'

    def ecol(u, v):
        if y is not None and {u, v} == {x, y}:
            return T['yellow'], 6
        return T['dim'], 3

    _graph(cv, T, box, POS, EDGES, ncol, nsub, ecol,
           '绿 = 出堆定下最短路，橙 = 在堆里等待，灰 = 没到；黄字 = 最短路 / 消失时刻', directed=False)


def _text(S, B):
    line = S.get('_line')
    if 'y' in S and line == FOR_LINE + 1:
        y = S['y']
        t = S['dis'][S['x']] + S['w']
        if S['dis'][y] != -1:
            return f"`{y}` 已经定下最短路 `{S['dis'][y]}`，不用再考虑"
        return f"到 `{y}` 的时刻 `{t}`，`{y}` 在 `{S['disappear'][y]}` 消失 → " + ('==来得及，入堆==' if t < S['disappear'][y] else '==来不及，丢弃==')
    if 'd' in S and 'x' in S:
        return f"当前出堆：`d = {S['d']}`，`x = {S['x']}`"
    return '堆里存 `[到达时间, 节点]`，先出时间最小的'


def _cond(S, B, r):
    y, t, dp = S.y, S.dis[S.x] + S.w, S.disappear[S.y]
    if S.dis[y] != -1:
        return f'`dis[{y}] = {S.dis[y]}` 已确定 → 跳过这个邻居'
    if t >= dp:
        return f'`{t} >= disappear[{y}] = {dp}`：到的时候 {y} 已消失 → ==不入堆，不能再从它扩展=='
    return f'`{t} < disappear[{y}] = {dp}`：来得及 → 入堆 `[{t}, {y}]`'


def _pop(S, B, r):
    return f'弹出 `[{S.d}, {S.x}]`：堆里==时间最小==的记录'


def _first(S, B, r):
    if S.dis[S.x] == -1:
        return f'`dis[{S.x}] == -1`：节点 {S.x} ==第一次出堆，这个 d 就是它的最短时间=='
    return f'`dis[{S.x}] = {S.dis[S.x]}` 早已确定，这条是重复记录 → 跳过'


CONFIG = dict(
    num=3112, title='访问消失节点的最少时间', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='Dijkstra：无效节点不参与更新',
    tags=['灵神题单·图论算法', '难度分 1757'],
    code=CODE,
    call=f'Solution().minimumTime({N}, {[list(e) for e in EDGES]}, {DISAPPEAR})',
    expect=[0, -1, 4, 5, 8],
    skip=['for x, y, w in edges', 'if y not in g[x]', 'g[x][y] = g[y][x] = w', 'dis = [-1]', 'heap = [[0, 0]]', 'g = [{}'],
    max_steps=80,
    views=[
        dict(type='text', fn=_text, h=56, size=24),
        dict(type='custom', draw=_draw, h=370),
        dict(type='array', var=lambda S: list(S['dis']) if 'dis' in S else None, label='dis[i]：最短时间（-1 = 还没确定 / 到不了）', h=150, cell=90,
             color=lambda S, i, v: 'green' if v >= 0 else None),
        dict(type='heap', var='heap', label='heap（元素 = [时间, 节点]）', h=130, fmt=lambda t: f'[{t[0]},{t[1]}]'),
    ],
    watch=[('d', 'd', 'blue'), ('x', 'x', 'blue'), ('y', 'y', 'yellow'), ('w', 'w')],
    captions={
        'while heap': lambda S, B, r: '堆非空，继续' if S.heap else '堆空了：所有「有效」节点都确定了最短时间',
        'd, x = heapq.heappop': _pop,
        'if dis[x] == -1': _first,
        'dis[x] = d': '`dis[{x}] = {d}`：确定节点 {x} 的最短时间',
        'for y, w in g[x].items()': lambda S, B, r: (f'`{S.x}` 的邻居看完了' if 'y' in B and (B.x, B.y, B.w) == (S.x, S.y, S.w) else f'看边 `{S.x} - {S.y}`，边权 `{S.w}`'),
        'if dis[y] == -1 and': _cond,
        'heapq.heappush': '`[{dis[x] + w}, {y}]` 入堆',
        'return dis': '无效节点从不入堆，所以 `dis` 里留下的 -1 就是答案',
    },
    cards=dict(
        one_liner='到达时间 >= 消失时间的点视为无效，不入堆、不扩展',
        complexity='时间 `O(n + m log m)`，空间 `O(n + m)`',
        problem=['无向正权图，节点 `i` 在 `disappear[i]` 时刻之后不能访问',
                 '求 `0` 到各点的最短时间，到不了为 `-1`',
                 '本视频：5 个点，`disappear = [1,2,5,6,9]`'],
        quote='如果到达该节点的最短时间大于等于其无法访问的时间，那么就置其为无法访问，同时也不再通过到达该节点的最短时间去更新到达剩下节点的最短时间。',
        quote_src='—— yiduobo 题解原文',
        idea=['正权图单源最短路，自然想到 Dijkstra，但要处理消失机制',
              '进堆前检查 `dis[x] + w < disappear[y]`，不满足就当它不存在',
              'Dijkstra 由近到远，所以路径上每个点经过时都还没消失'],
        summary=['时间 `O(n + m log m)`，空间 `O(n + m)`',
                 '原文用 `dis[x] == -1` 标记「还没出堆」，出堆时才写入最短时间',
                 '建图时用字典保留重边里最短的一条',
                 '对比灵神：灵神在更新 `dis` 时判断；这里在入堆前判断，出堆再定值'],
    ),
)
