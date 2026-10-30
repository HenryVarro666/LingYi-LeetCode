import math as _m


def _fnum(v):
    if v is None:
        return '?'
    if isinstance(v, float) and _m.isinf(v):
        return '∞'
    return str(v)


def _gdraw(cv, box, T, pos, edges, ncol=None, nlab=None, ecol=None, elab=None, arrows=None, r=28, title=None, pad=70):
    """pos: [(fx,fy)]; edges: [(u,v,w)]; ncol(i)->(r,g,b)|None; nlab(i)->[str..] 画在节点下方;
    ecol(k)->((r,g,b), width)|None; elab(k)->str|None; arrows: set of (u,v) 有向画箭头"""
    x0, y0, x1, y1 = box
    if title:
        cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    ax0, ay0, ax1, ay1 = x0 + pad, y0 + 84, x1 - pad, y1 - 100
    P = [(ax0 + fx * (ax1 - ax0), ay0 + fy * (ay1 - ay0)) for fx, fy in pos]
    for k, (u, v, w) in enumerate(edges):
        c, wd = (ecol(k) if ecol else None) or (T['border'], 3)
        (xa, ya), (xb, yb) = P[u], P[v]
        L = _m.hypot(xb - xa, yb - ya) or 1
        ux, uy = (xb - xa) / L, (yb - ya) / L
        if arrows and (u, v) in arrows:
            cv.arrow((xa + ux * r, ya + uy * r), (xb - ux * (r + 4), yb - uy * (r + 4)), c, wd, head=16)
        elif arrows and (v, u) in arrows:
            cv.arrow((xb - ux * r, yb - uy * r), (xa + ux * (r + 4), ya + uy * (r + 4)), c, wd, head=16)
        else:
            cv.line([(xa, ya), (xb, yb)], c, wd)
    for k, (u, v, w) in enumerate(edges):
        t = elab(k) if elab else str(w)
        if t is None:
            continue
        c, wd = (ecol(k) if ecol else None) or (T['border'], 3)
        mx, my = (P[u][0] + P[v][0]) / 2, (P[u][1] + P[v][1]) / 2
        tw = cv.tlen(t, 22, bold=True) + 14
        cv.rect((mx - tw / 2, my - 15, mx + tw / 2, my + 15), fill=T['panel'], r=8)
        cv.text((mx, my), t, 22, c if c != T['border'] else T['muted'], anchor='mm', bold=True)
    for i, (X, Y) in enumerate(P):
        c = ncol(i) if ncol else None
        cv.d.ellipse((X - r, Y - r, X + r, Y + r), fill=c or T['panel2'], outline=T['border'] if not c else c, width=3)
        cv.text((X, Y), i if not isinstance(i, str) else i, 28, T['bg'] if c else T['text'], anchor='mm', bold=True, mono=True)
        for j, s in enumerate((nlab(i) if nlab else []) or []):
            if isinstance(s, tuple):
                s, sc = s
            else:
                sc = T['muted']
            cv.text((X, Y + r + 6 + j * 24), s, 20, sc, anchor='mt', bold=True, mono=True)

N = 5
ROADS = [[0, 1, 1], [0, 2, 1], [1, 3, 2], [2, 3, 2], [0, 3, 3], [3, 4, 1], [1, 4, 4]]
POS = [(0.0, 0.5), (0.33, 0.0), (0.33, 1.0), (0.68, 0.5), (1.0, 0.5)]


def _ncol(S, T):
    h = S.get('h') or []
    inheap = {x for _, x in h}
    dis = S.get('dis')

    def f(i):
        if dis is None:
            return None
        if S.get('x') is not None and i == S['x'] and S.get('_line') not in (None,):
            return T['pink']
        if S.get('y') is not None and i == S['y'] and 'new_dis' in S and S.get('_line', 0) >= 21:
            return T['blue']
        if isinstance(dis[i], float):
            return None
        return T['yellow'] if i in inheap else T['green']
    return f


def _draw(cv, S, B, box, T):
    dis, f = S.get('dis'), S.get('f')
    x, y = S.get('x'), (S.get('y') if 'new_dis' in S and S.get('_line', 0) >= 21 else None)

    def ecol(k):
        u, v, w = ROADS[k]
        if x is not None and y is not None and {u, v} == {x, y}:
            return (T['yellow'], 6)
        return None

    def nlab(i):
        if dis is None:
            return []
        return [(f'dis={_fnum(dis[i])}', T['cyan']), (f'f={f[i]}', T['green'])]
    _gdraw(cv, box, T, POS, ROADS, ncol=_ncol(S, T), nlab=nlab, ecol=ecol, r=30,
           title='粉 = 刚弹出的 x　蓝 = 在更新的 y　黄 = 在堆里　绿 = 已确定')


CONFIG = dict(
    num=1976, title='到达目的地的方案数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='堆优化 Dijkstra · 最短路计数',
    tags=['图论算法', '难度分 2095'],
    code='''
class Solution:
    def countPaths(self, n: int, roads: List[List[int]]) -> int:
        g = [[] for _ in range(n)]  # 邻接表
        for x, y, d in roads:
            g[x].append((y, d))
            g[y].append((x, d))

        dis = [inf] * n
        dis[0] = 0
        f = [0] * n
        f[0] = 1
        h = [(0, 0)]
        while True:
            dx, x = heappop(h)
            if x == n - 1:
                # 不可能找到比 dis[-1] 更短，或者一样短的最短路了（注意本题边权都是正数）
                return f[-1]
            if dx > dis[x]:
                continue
            for y, d in g[x]:  # 尝试更新 x 的邻居的最短路
                new_dis = dx + d
                if new_dis < dis[y]:
                    # 就目前来说，最短路必须经过 x
                    dis[y] = new_dis
                    f[y] = f[x]
                    heappush(h, (new_dis, y))
                elif new_dis == dis[y]:
                    # 和之前求的最短路一样长
                    f[y] = (f[y] + f[x]) % 1_000_000_007
''',
    call=f'Solution().countPaths({N}, {ROADS})',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='heap', var='h', fmt=lambda p: f'{p[1]}:{p[0]}', label='堆 h（点:距离）', top_color='purple', h=110),
    ],
    watch=[('dx', 'dx', 'purple'), ('x', 'x', 'pink'), ('y', 'y', 'blue'), ('new_dis', 'new_dis', 'orange'),
           ('f[n-1]', lambda S: S['f'][N - 1] if 'f' in S else None, 'green')],
    skip=['g[x].append', 'g[y].append', 'for x, y, d in roads', 'new_dis = dx + d', 'g = [[]', 'dis[0] = 0', 'f[0] = 1', 'f = [0] * n'],
    captions={
        'dis = [inf] * n': '`dis[i]`：从 0 到 i 的最短路长度，一开始都是 ∞；`f[i]`：最短路的条数；`dis[0] = 0`，`f[0] = 1`（原地不动算一种）',
        'h = [(0, 0)]': '堆里放 `(距离, 点)`，先放起点 `(0, 0)`',
        'dx, x = heappop(h)': '弹出堆顶：离起点最近、还没处理的点 `{x}`，它的最短路 =={dx}==',
        'if x == n - 1': lambda S, B, r: (f'`x = {S.x}` 是终点：边权全为正，后面不可能再出现更短或一样短的路 → ==f[终点] 已定型==' if S.x == S.n - 1
                                          else f'`x = {S.x}` 还不是终点 `{S.n - 1}`，继续'),
        'if dx > dis[x]': lambda S, B, r: (f'`{S.dx} > dis[{S.x}] = {S.dis[S.x]}`：这是旧的重复项，`{S.x}` 之前出堆过，跳过' if S.dx > S.dis[S.x]
                                           else f'`{S.dx} > {S.dis[S.x]}` 不成立：`{S.x}` 第一次出堆，用它更新邻居'),
        'for y, d in g[x]': lambda S, B, r: (f'`{S.x}` 的邻居都看完了，回到堆里取下一个' if B.get('x') == S.x and B.get('y') == S.y
                                             else f'看 `{S.x}` 的邻居 `{S.y}`，路长 `{S.d}`'),
        'if new_dis < dis[y]': lambda S, B, r: (f'经 `{S.x}` 到 `{S.y}`：`{S.dx} + {S.d}` = =={S.new_dis}==，`{S.new_dis} < {_fnum(S.dis[S.y])}` → 更短！之前的路径全作废' if S.new_dis < S.dis[S.y]
                                                else f'经 `{S.x}` 到 `{S.y}`：`{S.dx} + {S.d}` = =={S.new_dis}==，`{S.new_dis} < {_fnum(S.dis[S.y])}` 不成立，看是否一样长'),
        'dis[y] = new_dis': '`dis[{y}]` 更新为 =={dis[y]}=='
        ,
        'f[y] = f[x]': '最短路变了，方案数重来：`f[{y}] = f[{x}]` = =={f[y]}=='
        ,
        'heappush': '`({new_dis}, {y})` 入堆，等着被弹出',
        'elif new_dis == dis[y]': lambda S, B, r: (f'`{S.new_dis} == dis[{S.y}] = {S.dis[S.y]}`：一样短！又发现一批最短路' if S.new_dis == S.dis[S.y]
                                                   else f'`{S.new_dis}` 比 `dis[{S.y}] = {S.dis[S.y]}` 长，不是最短路，忽略'),
        'f[y] = (f[y] + f[x])': '一样长 → 方案数相加：`f[{y}] = {B.f[y]} + {f[x]}` = =={f[y]}==',
        'return f[-1]': '终点最短路条数 =={ret}==',
    },
    max_steps=110,
    cards=dict(
        one_liner='Dijkstra 更新最短路时顺手维护条数：更短就重置，一样长就累加',
        complexity='时间 `O(m log m)`，空间 `O(m)`',
        problem=['城市有 `n` 个路口，双向道路带耗时；求从 `0` 到 `n-1` ==耗时最少==的路径有几条（对 `10^9+7` 取模）',
                 '示例：`n=7` 时答案是 `4`',
                 '本视频：`n=5` 的小图，有三条等长最短路经过点 3'],
        quote='如果 dis[x] + g[x][y] < dis[y]，说明从 0 到 x 再到 y 的路径是目前最短的，所以更新 f[y] 为 f[x]。……如果 dis[x] + g[x][y] = dis[y]，……所以把 f[y] 增加 f[x]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['定义 `f[i]` = 从 0 到 i 的最短路条数，初始 `f[0] = 1`',
              '更新 `dis[y]` 时：更短 → `f[y] = f[x]`；一样短 → `f[y] += f[x]`',
              '终点第一次出堆就可以直接返回：边权为正，之后不会再有同样短的路'],
        after=[dict(heading='另一种写法', lines=['写法一：朴素 Dijkstra（邻接矩阵 + `done` 数组）',
                                              '时间 `O(n²)`，稠密图更合适', '逻辑完全一样，只是找最小值不用堆'])],
        summary=['时间 `O(m log m)`，空间 `O(m)`；稠密图用朴素 Dijkstra 的 `O(n²)` 更好',
                 '==更短时用赋值，一样长时用累加==，别写反',
                 '终点出堆就返回，省去后面的无用计算（只对正权边成立）',
                 '加法后取模：`f[y] = (f[y] + f[x]) % 1_000_000_007`',
                 '同类：最短路计数、图 DP'],
    ),
)
