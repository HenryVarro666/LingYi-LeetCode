import math as _m

N = 4
FLIGHTS = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]
SRC, DST, KK = 0, 3, 2
POS = {0: (0.04, 0.5), 1: (0.42, 0.06), 2: (0.42, 0.94), 3: (0.96, 0.5)}
INNER = (15, 16, 17, 18, 19, 20)


def _graph(cv, T, box, pos, edges, ncol, ecol, title):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    R = 30
    L, Rr, Tp, Bt = x0 + 70, x1 - 70, y0 + 60 + R, y1 - R - 28
    P = {u: (L + fx * (Rr - L), Tp + fy * (Bt - Tp)) for u, (fx, fy) in pos.items()}
    for u, v, w in edges:
        c, wd = ecol(u, v)
        (ax, ay), (bx, by) = P[u], P[v]
        dd = _m.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / dd, (by - ay) / dd
        ox, oy = -uy * 7, ux * 7    # 0→2 / 2→0 这类双向边错开一点
        cv.arrow((ax + ux * R + ox, ay + uy * R + oy), (bx - ux * (R + 2) + ox, by - uy * (R + 2) + oy), c, wd, 15)
        sg = -1 if (u, v) == (0, 1) else 1    # 0→1 的价格标在线外侧，免得和 2→0 重叠
        mx, my = (ax + bx) / 2 - uy * 24 * sg, (ay + by) / 2 + ux * 24 * sg
        cv.rect((mx - 26, my - 15, mx + 26, my + 15), fill=T['bg'], r=6)
        cv.text((mx, my), w, 21, c if c != T['dim'] else T['muted'], anchor='mm', bold=True, mono=True)
    for u, (px, py) in P.items():
        fc = ncol(u)
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fc, outline=T['border'], width=2)
        cv.text((px, py), u, 26, T['bg'] if fc != T['panel2'] else T['text'], anchor='mm', bold=True)
        tag = 'src' if u == SRC else 'dst' if u == DST else None
        if tag:
            cv.text((px, py + R + 4), tag, 20, T['yellow'], anchor='mt', bold=True, mono=True)


def _cur(S):
    line = S.get('_line')
    if 'i' not in S or line not in (14,) + INNER:
        return None, None
    return S.get('x'), (S.get('y') if line in INNER else None)


def _draw(cv, S, B, box, T):
    x, y = _cur(S)

    def ncol(u):
        if u == x:
            return T['blue']
        if u == y:
            return T['yellow']
        return T['panel2']

    def ecol(a, b):
        if a == x and b == y:
            return T['yellow'], 5
        return T['dim'], 3

    _graph(cv, T, box, POS, FLIGHTS, ncol, ecol, '航线图（蓝 = 出发城市 x，黄 = 到达城市 y）')


def _fcol(S, i, j, v):
    x, y = _cur(S)
    if x is None:
        return None
    if i == S['i'] - 1 and j == x:
        return 'blue'
    if i == S['i'] and j == y:
        return 'yellow'
    return None


def _text(S):
    if 'f' not in S or 'res' not in S:
        return '`f[i][x]`：从 src 出发==恰好坐 i 趟航班==到 x 的最低价格'
    r = S['res']
    return (f"已知到 dst 的最低价 `res = {r}`" if r is not None else '还没到过 dst') + (f"　·　第 `i = {S['i']}` 轮：用第 {S['i'] - 1} 行推第 {S['i']} 行" if 'i' in S else '')


def _has(S, B, r):
    v = S.f[S.i - 1][S.x]
    if v is None:
        return f'`f[{S.i - 1}][{S.x}]` 是 None：坐 {S.i - 1} 趟到不了 `{S.x}`，跳过'
    return f'`f[{S.i - 1}][{S.x}] = {v}`：能到 `{S.x}` → 枚举从 `{S.x}` 出发的航班'


def _forv(S, B, r):
    ys = list(S.g.get(S.x, {}))
    if S.get('y') not in ys:
        return f'`{S.x}` 没有出发的航班'
    if 'y' in B and B.y == S.y and B.x == S.x and B.i == S.i:
        return f'`{S.x}` 出发的航班都看完了'
    return f'航班 `{S.x} → {S.y}`，价格 `{S.g[S.x][S.y]}`'


def _better(S, B, r):
    i, x, y = S.i, S.x, S.y
    new = S.f[i - 1][x] + S.g[x][y]
    old = S.f[i][y]
    if old is None:
        return f'`f[{i}][{y}]` 还是 None → 直接用 `{S.f[i - 1][x]} + {S.g[x][y]}` = =={new}=='
    if old > new:
        return f'`f[{i}][{y}] = {old} > {new}`：更便宜，==更新=='
    return f'`f[{i}][{y}] = {old} ≤ {new}`：不更便宜，不更新'


CONFIG = dict(
    num=787, title='K站中转内最便宜的航班', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='按航班数分层的 DP',
    tags=['labuladong', '灵神题单·图论算法'],
    code='''
class Solution(object):
    def findCheapestPrice(self, n, flights, src, dst, K):
        g = {}
        for x, y, v in flights:
            if x not in g:
                g[x] = {}
            g[x][y] = v

        f = [[None] * n for _ in range(K + 2)]
        f[0][src] = 0
        res = None
        for i in range(1, K + 2):
            for x in range(n):
                if f[i - 1][x] is not None:
                    for y in g.get(x, {}):
                        if f[i][y] is None or f[i][y] > f[i - 1][x] + g[x][y]:
                            f[i][y] = f[i - 1][x] + g[x][y]
                            if y == dst:
                                if res is None or res > f[i][y]:
                                    res = f[i][y]


        if res is None:
            return -1

        return res
''',
    call=f'Solution().findCheapestPrice({N}, {FLIGHTS}, {SRC}, {DST}, {KK})',
    expect=400,
    skip=['for x, y, v in flights', 'if x not in g', 'g[x] = {}', 'g[x][y] = v', 'for x in range(n)'],
    views=[
        dict(type='text', fn=_text, h=56, size=24),
        dict(type='custom', draw=_draw, h=330),
        dict(type='table', var=lambda S: [['·' if v is None else v for v in row] for row in S['f']] if 'f' in S else None,
             label='f[i][x]（行 = 坐了 i 趟，列 = 城市 x；· = 到不了）', h=300,
             rows=lambda S: [f'i={k}' for k in range(len(S['f']))] if 'f' in S else None,
             cols=lambda S: [f'x={k}' for k in range(S['n'])] if 'n' in S else None,
             color=_fcol),
    ],
    watch=[('i', 'i', 'purple'), ('x', 'x', 'blue'), ('y', 'y', 'yellow'), ('res', 'res', 'green')],
    captions={
        'g = {}': '`g[x][y] = 价格`：从 x 飞往 y 的航班（已建好）',
        'f = [[None] * n': '`f[i][x]`：坐 ==恰好 i 趟==航班到 x 的最低价；最多 `K + 1 = {K + 1}` 趟，所以要 `K + 2` 行',
        'f[0][src] = 0': '边界：坐 0 趟只能在起点 `{src}`，花费 `0`',
        'res = None': '`res`：到 dst 的最低价，`None` 表示还没到过',
        'for i in range(1, K + 2)': lambda S, B, r: (f'`{S.K + 1}` 轮都做完了：最多坐 `K + 1` 趟' if B.get('i') == S.i
                                                  else f'第 `i = {S.i}` 轮：只用第 `{S.i - 1}` 行的状态往外飞一趟'),
        'if f[i - 1][x] is not None': _has,
        'for y in g.get(x, {})': _forv,
        'if f[i][y] is None or': _better,
        'f[i][y] = f[i - 1][x] + g[x][y]': '`f[{i}][{y}] = f[{i - 1}][{x}] + {g[x][y]}` = =={f[i][y]}==',
        'if y == dst': lambda S, B, r: (f'`{S.y}` ==就是终点== → 看能不能更新答案' if S.y == S.dst else f'`{S.y}` 不是终点'),
        'if res is None or res > f[i][y]': lambda S, B, r: (
            '还没有答案 → 记下' if S.res is None else
            (f'`{S.res} > {S.f[S.i][S.y]}` → 更便宜' if S.res > S.f[S.i][S.y] else f'`{S.res} ≤ {S.f[S.i][S.y]}` → 不更新')),
        'res = f[i][y]': '答案更新为 =={res}==（坐 {i} 趟 = 中转 {i - 1} 次）',
        'if res is None:': lambda S, B, r: '`res` 是 None：K 站内到不了' if S.res is None else f'`res = {S.res}`，有答案',
        'return -1': '到不了终点，返回 `-1`',
        'return res': '最便宜 =={ret}==',
    },
    cards=dict(
        one_liner='按“坐了几趟航班”分层：第 i 层只从第 i−1 层飞一趟过来',
        complexity='时间 `O(K · (n + m))`，空间 `O(K · n)`',
        problem=['`n` 个城市，`flights[i] = [from, to, price]` 是一趟航班',
                 '求从 `src` 到 `dst`、==最多中转 K 站==（最多坐 K+1 趟）的最低价格，没有就返回 `-1`',
                 '示例：`[[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]`，0 → 3',
                 '`k = 1` → `700`；本视频 `K = 2` → `400`（0→1→2→3）'],
        quote='f[i][x]表示从起点开始==走i步，走到节点x的最低价格==，边界条件自然是f[0][src] = 0。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举第 `i - 1` 轮能到的每个 `x`，再枚举从 `x` 出发的边 `(x, y)`',
              '转移：`f[i][y] = min(f[i][y], f[i - 1][x] + dis(x, y))`',
              '每当 `y` 是终点，就用 `f[i][y]` 尝试更新答案'],
        summary=['时间 `O(K · (n + m))`：共 `K + 1` 轮，每轮扫一遍点和边',
                 '`None` 表示到不了；比较前要先判断 `is None`',
                 '中转 K 站 = 坐 `K + 1` 趟：循环 `range(1, K + 2)`',
                 '原文提到也可以用类似 SPFA / Bellman-Ford 的做法，细节更多',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
