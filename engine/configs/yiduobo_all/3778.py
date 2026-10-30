import math as _m


def _graph(cv, T, box, pos, edges, ncol, nsub, ecol, title, directed=True, R=30, top=60, bot=34):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    L, Rr, Tp, Bt = x0 + 70, x1 - 70, y0 + top + R, y1 - R - bot
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
    for u in pos:
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

N = 4
EDGES = [(0, 1, 3), (1, 2, 5), (2, 3, 2), (0, 2, 8)]
POS = {0: (0.0, 0.5), 1: (0.4, 0.0), 2: (0.58, 1.0), 3: (1.0, 0.5)}

CODE = '''
class Solution(object):
    def minCostExcludingMax(self, n, edges):

        dis = [[None] * 2 for _ in range(n)]
        heap = [(0, 0, 0)]

        g = [{} for _ in range(n)]
        for x, y, w in edges:
            g[x][y] = w
            g[y][x] = w

        while heap:
            d, x, level = heapq.heappop(heap)
            if dis[x][level] is not None:
                continue
            dis[x][level] = d
            for y in g[x]:
                nxt_d = d + g[x][y]
                if dis[y][level] is None:
                    heapq.heappush(heap, (nxt_d, y, level))
                if level == 0 and dis[y][level + 1] is None:
                    heapq.heappush(heap, (d, y, level + 1))

        return dis[-1][1]
'''
_L = CODE.strip('\n').split('\n')
POP_LINE = next(i + 1 for i, l in enumerate(_L) if 'heappop' in l)
FOR_LINE = next(i + 1 for i, l in enumerate(_L) if 'for y in g[x]' in l)
RET_LINE = next(i + 1 for i, l in enumerate(_L) if 'return dis' in l)


def _cur(S):
    line = S.get('_line') or 0
    if line >= POP_LINE and line < RET_LINE and all(k in S for k in ('x', 'level', 'd', 'dis')):
        return S['x'], S['level']
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cur = _cur(S)
    line = S.get('_line') or 0
    y = S.get('y') if cur and line >= FOR_LINE and 'y' in S else None
    dis = S.get('dis')
    midy = (y0 + y1) / 2
    for lv, (bx0, by0, bx1, by1) in ((1, (x0, y0, x1, midy)), (0, (x0, midy, x1, y1))):
        def ncol(u, lv=lv):
            if cur == (u, lv):
                return T['blue']
            if dis is not None and dis[u][lv] is not None:
                return T['green'] if (u, lv) == (N - 1, 1) else T['orange']
            return T['panel2']

        def nsub(u, lv=lv):
            if dis is None or dis[u][lv] is None:
                return None
            return f'{dis[u][lv]}'

        def ecol(u, v, lv=lv):
            if y is not None and cur and cur[1] == lv and {u, v} == {cur[0], y}:
                return T['yellow'], 6
            return T['dim'], 3

        _graph(cv, T, (bx0, by0, bx1, by1), POS, EDGES, ncol, nsub, ecol,
               ('上层 level 1：已经免掉了一条边' if lv else '下层 level 0：还没免边'), directed=False, R=24, top=30, bot=20)
    cv.text((x1 - 16, midy - 6), '免边 ⇅ 跨层', 20, T['orange'], anchor='rb', bold=True)


def _text(S, B):
    cur = _cur(S)
    if cur is None:
        return '建两层图：走一条边时可以「免费」跨到上层，且只能跨一次'
    lv = '上层（已免边）' if cur[1] else '下层（还没免边）'
    return f"当前：节点 `{cur[0]}` · {lv}，距离 `{S['d']}`"


def _skip(S, B, r):
    return f'`dis[{S.x}][{S.level}] = {S.dis[S.x][S.level]}` 已确定 → 这是旧记录，==跳过=='


_V = {}


def _forcap(S, B, r):
    k = (S.x, S.level)
    c = _V.get(k, 0)
    nb = list(S.g[S.x])
    if c >= len(nb):
        _V.pop(k, None)
        return f'`{S.x}` 的邻居都看完了'
    _V[k] = c + 1
    return f'枚举邻居 `{nb[c]}`，边权 `{S.g[S.x][nb[c]]}`'


def _stay(S, B, r):
    if S.dis[S.y][S.level] is None:
        return f'`dis[{S.y}][{S.level}]` 还没确定 → 层内走边：距离 `{S.nxt_d}`，入堆'
    return f'`dis[{S.y}][{S.level}] = {S.dis[S.y][S.level]}` 已确定 → 不入堆'


def _cross(S, B, r):
    if S.level != 0:
        return '`level = 1`：已经免过边了，不能再跨层'
    if S.dis[S.y][1] is None:
        return f'`level == 0` 且 `dis[{S.y}][1]` 没确定 → ==跨层==：走边 `{S.x}-{S.y}` 但距离不增（还是 `{S.d}`），入堆'
    return f'`dis[{S.y}][1] = {S.dis[S.y][1]}` 已确定 → 不必再入堆'


CONFIG = dict(
    num=3778, title='排除一个最大权重边的最小距离', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='两层图 Dijkstra',
    tags=['灵神题单·图论算法'],
    code=CODE,
    call=f'Solution().minCostExcludingMax({N}, {[list(e) for e in EDGES]})',
    expect=2,
    skip=['for x, y, w in edges', 'g[x][y] = w', 'g[y][x] = w'],
    max_steps=78,
    views=[
        dict(type='text', fn=_text, h=56, size=24),
        dict(type='custom', draw=_draw, h=470),
        dict(type='heap', var='heap', label='heap：(距离, 节点, 层)', h=110, fmt=lambda t: f'({t[0]},{t[1]},{t[2]})'),
    ],
    watch=[('d', 'd', 'blue'), ('x', 'x', 'blue'), ('level', 'level', 'orange'), ('y', 'y', 'yellow'), ('nxt_d', 'nxt_d', 'cyan')],
    captions={
        'dis = [[None]': '`dis[x][level]`：到节点 x、处在第 level 层的最短距离（level 0 = 还没免边，1 = 已免边）',
        'heap = [(0, 0, 0)]': '从下层的 0 号点出发：`(距离 0, 节点 0, 层 0)`',
        'g = [{} for': '`g[x][y]`：邻接字典，无向边两个方向都存',
        'while heap': lambda S, B, r: '堆非空，继续' if S.heap else '堆空了，所有状态都定下来了',
        'heapq.heappop': '弹出距离最小的状态：节点 `{x}`，层 `{level}`，距离 `{d}`',
        'if dis[x][level] is not None': lambda S, B, r: (f'`dis[{S.x}][{S.level}]` 已有值 → 成立：旧记录' if S.dis[S.x][S.level] is not None else f'`dis[{S.x}][{S.level}]` 还是空 → 不成立：第一次出堆，距离最短'),
        'continue': _skip,
        'dis[x][level] = d': '确定 `dis[{x}][{level}]` = =={d}==',
        'for y in g[x]': _forcap,
        'nxt_d = d + g[x][y]': '不免边走到 `{y}`：`{d} + {g[x][y]}` = =={nxt_d}==',
        'if dis[y][level] is None': _stay,
        'heapq.heappush(heap, (nxt_d': '`({nxt_d}, {y}, {level})` 入堆：同层走边，距离累加',
        'if level == 0 and': _cross,
        'heapq.heappush(heap, (d, y': '`({d}, {y}, {level + 1})` 入堆：==跨到上层，这条边的权重不算==',
        'return dis[-1][1]': '答案 = 上层终点 `dis[{n-1}][1]` = =={dis[-1][1]}==：恰好免了一条边的最短路',
    },
    cards=dict(
        one_liner='复制一层图：跨层的那条边免费，且只能跨一次',
        complexity='时间 `O(m log m)`，空间 `O(n + m)`',
        problem=['无向连通图，路径开销 = 边权之和 − 路径上最大的那条边（只减一次）',
                 '求 `0` 到 `n-1` 的最小开销',
                 '本视频：4 个点，边 `0-1:3, 1-2:5, 2-3:2, 0-2:8`，答案 `2`'],
        quote='对于原图中的每条边[u, v, w]，都建立从下层图的u到上层图的v，权重为w的有向边……问题就转化成了从下层图的0号节点走到上层图的n - 1号节点的最短路。',
        quote_src='—— yiduobo 题解原文',
        idea=['每条边可以在层内走（付 w），也可以跨层走（本题把它当免费）',
              '为什么免的就是最大边？若不是，换成最大边免费会更短，矛盾',
              '所以不用管「最大」，直接跑最短路，最短路自然免最大的那条'],
        summary=['时间 `O(m log m)`，状态数 `2n`',
                 '易错：跨层入堆的距离是 `d`（不加 `w`），层内才是 `d + w`',
                 '易错：只有 `level == 0` 才能跨层，保证至多免一次',
                 '原文为 Python 2 风格，无需改动即可在 Python 3 运行'],
    ),
)
