BOMBS = [[0, 0, 5], [4, 0, 3], [7, 0, 4], [4, 6, 1]]


def _bits(v, n):
    return [(v >> j) & 1 for j in range(n)]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f = S.get('f')
    if f is None:
        return
    n = len(BOMBS)
    minx = min(x - r for x, y, r in BOMBS)
    maxx = max(x + r for x, y, r in BOMBS)
    miny = min(y - r for x, y, r in BOMBS)
    maxy = max(y + r for x, y, r in BOMBS)
    pad = 24
    sc = min((x1 - x0 - 2 * pad) / (maxx - minx), (y1 - y0 - 2 * pad - 60) / (maxy - miny))
    ox = x0 + pad + ((x1 - x0 - 2 * pad) - sc * (maxx - minx)) / 2
    oy = y0 + 30 + pad + ((y1 - y0 - 2 * pad - 60) - sc * (maxy - miny)) / 2

    def P(k):
        return ox + (BOMBS[k][0] - minx) * sc, oy + (maxy - BOMBS[k][1]) * sc

    inn = S['_inner']
    floyd = 'k' in S and S['k'] is not None and 'dx' in S and False
    kk = S.get('k') if S.get('_line', 0) >= 14 else None
    ii = S.get('i') if S.get('_line', 0) >= 5 else None
    jj = S.get('j') if S.get('_line', 0) <= 10 else None
    cols = ['blue', 'pink', 'green', 'purple']
    cv.text((x0 + 16, y0 + 8), '炸弹平面（圆 = 爆炸范围，箭头 = i 能到达 j）', 20, T['dim'])
    for k, (x, y, r) in enumerate(BOMBS):
        X, Y = P(k)
        c = T[cols[k]]
        cv.d.ellipse((X - r * sc, Y - r * sc, X + r * sc, Y + r * sc), outline=c, width=4 if k == ii else 2)
    base = {(i, j) for i, (x, y, r) in enumerate(BOMBS) for j, (x2, y2, _) in enumerate(BOMBS)
            if i != j and (x - x2) ** 2 + (y - y2) ** 2 <= r * r}
    import math
    for i in range(n):
        for j in range(n):
            if i != j and (f[i] >> j) & 1:
                (ax, ay), (bx, by) = P(i), P(j)
                d = math.hypot(bx - ax, by - ay)
                ux, uy = (bx - ax) / d, (by - ay) / d
                off = 8
                sx, sy = -uy * off, ux * off
                derived = (i, j) not in base
                cv.arrow((ax + ux * 22 + sx, ay + uy * 22 + sy), (bx - ux * 26 + sx, by - uy * 26 + sy),
                         T['yellow'] if derived else T['muted'], 4 if derived else 3, 14)
    for k in range(n):
        X, Y = P(k)
        ring = T['yellow'] if k == kk else (T['blue'] if k == ii else None)
        cv.d.ellipse((X - 20, Y - 20, X + 20, Y + 20), fill=T[cols[k]], outline=ring, width=5 if ring else 1)
        cv.text((X, Y), k, 24, T['bg'], anchor='mm', bold=True)
    cv.text((x0 + 16, y1 - 22), '灰箭头 = 直接引爆，黄箭头 = 经过中转才能到达', 18, T['dim'], anchor='lm')


def _fcell(S, i, j, v):
    k = S.get('k') if S.get('_line', 0) >= 14 else None
    if v == 1 and k is not None and (i == S.get('i') and j == k):
        return 'yellow'
    if v == 1 and i == j:
        return None
    return 'green' if v == 1 else None


def _hit(S, B, ret):
    d2 = S.dx * S.dx + S.dy * S.dy
    if S.i == S.j:
        return f'炸弹 `{S.i}` 一定在自己的集合里：`f[{S.i}] |= 1 << {S.j}`'
    return f'距离² `{d2}` ≤ 半径² `{S.r * S.r}` → 炸弹 {S.i} 能引爆 {S.j}：`f[{S.i}]` 加入 {S.j}'


def _set(v):
    return '{' + ','.join(str(j) for j in range(8) if v >> j & 1) + '}'


def _chk(S, B, ret):
    i, k = S.i, S.k
    if i == k:
        return f'`i = k = {i}`：自己借自己，什么也不会变'
    if S.f[i] >> k & 1:
        return f'`f[{i}] = {_set(S.f[i])}`，包含 {k} → {i} 能到达 {k}，可以借用 `f[{k}] = {_set(S.f[k])}`'
    return f'`f[{i}] = {_set(S.f[i])}`，不含 {k} → {i} 到不了 {k}，不借用'


CONFIG = dict(
    num=2101, title='引爆最多的炸弹', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='Bitset 优化 Floyd 传递闭包',
    tags=['灵神题单', '图论算法', '难度分 1880'],
    code='''
class Solution:
    def maximumDetonation(self, bombs: List[List[int]]) -> int:
        n = len(bombs)
        f = [0] * n
        for i, (x, y, r) in enumerate(bombs):
            for j, (x2, y2, _) in enumerate(bombs):
                dx = x - x2
                dy = y - y2
                if dx * dx + dy * dy <= r * r:
                    f[i] |= 1 << j  # i 可以到达 j

        for k in range(n):
            for i in range(n):
                if f[i] >> k & 1:  # i 可以到达 k
                    f[i] |= f[k]  # i 也可以到 k 可以到达的点

        return max(s.bit_count() for s in f)  # 集合大小的最大值
''',
    call=f'Solution().maximumDetonation({BOMBS})',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='grid', var=lambda S: [[(S['f'][i] >> j) & 1 for j in range(len(S['f']))] for i in range(len(S['f']))] if 'f' in S else [[0]],
             rows=lambda S: [f'f[{i}]' for i in range(len(S['f']))] if 'f' in S else ['f'],
             cols=lambda S: [str(j) for j in range(len(S['f']))] if 'f' in S else ['0'],
             color=_fcell, cell=64, h=270, label='f[i] 的第 j 位 = 1：i 能引爆 j'),
    ],
    watch=[('i', lambda S: S.get('i'), 'blue'), ('j', lambda S: S.get('j') if S.get('_line', 0) <= 10 else None, 'pink'),
           ('k', lambda S: S.get('k') if S.get('_line', 0) >= 14 else None, 'yellow')],
    skip=['n = len', 'for i, (x, y, r)', 'for j, (x2', 'dx = x', 'dy = y', 'if dx * dx', 'for k in range', 'for i in range(n)'],
    max_steps=90,
    captions={
        'f = [0] * n': '`f[i]` 是一个 ==二进制数==，第 j 位为 1 表示 i 能到达 j（集合 → 位运算）',
        'f[i] |= 1 << j': _hit,
        'if f[i] >> k & 1': _chk,
        'f[i] |= f[k]': lambda S, B, ret: (f'`f[{S.i}] |= f[{S.k}]`：i = k，自己并自己，不变' if S.i == S.k else
                                            f'`f[{S.i}] |= f[{S.k}]`：取==并集==：{S.i} 能到的 = 自己的 ∪ {S.k} 能到的 → `f[{S.i}] = {_set(S.f[S.i])}`'),
        'return max': lambda S, B, ret: f'每个 `f[i]` 的 1 的个数 = {[s.bit_count() for s in S.f]}，最大值 =={ret}== 个炸弹',
    },
    cards=dict(
        one_liner='把「i 能引爆谁」存成位集合，用 Floyd 求传递闭包',
        complexity='时间 `O(n³/w)`，空间 `O(n²/w)`',
        problem=['炸弹 `[x, y, r]`：引爆一个炸弹，圆内的炸弹都会被引爆，连锁反应',
                 '选一个炸弹引爆，最多能引爆多少个？',
                 '本视频：4 个炸弹，`0→1→2` 连锁，3 号孤立，答案 `3`'],
        quote='定义 f[i] 表示 i 可以到达的节点集合。注意 i 一定在 f[i] 中。如果 i 可以到达 k，那么 k 能到的点，i 也可以到达，于是 f[i] = f[i] ∪ f[k]。',
        quote_src='—— 灵茶山艾府题解 · 方法二',
        idea=['炸弹引爆是==有向==关系（半径不同），所以是有向图的可达性，不是并查集',
              'Floyd 的三重循环里，把「最短路」换成「能否到达」，再把 bool 数组压成整数位集合',
              '`f[i] |= f[k]` 一次并集处理 n 位，所以复杂度除以 `w`'],
        summary=['时间 `O(n³/w)`，空间 `O(n²/w)`（`w` 为机器字长）',
                 '==循环顺序必须是 k 在最外层==，和 Floyd 一致',
                 '初始 `f[i]` 要包含自己：`i == j` 时距离 0 ≤ r²，自然满足',
                 '`int.bit_count()` 需要 Python 3.10+',
                 '方法一：对每个起点 DFS 数能访问的点，`O(n³)`；并集查集会算错有向关系'],
    ),
)
