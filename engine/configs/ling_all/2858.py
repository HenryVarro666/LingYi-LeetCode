# 示例 1：n=4, edges=[[2,0],[2,1],[1,3]] -> [1,1,0,2]
POS_ = {2: (0.5, 0.14), 0: (0.2, 0.50), 1: (0.8, 0.50), 3: (0.8, 0.88)}
ORIG_ = [(2, 0), (2, 1), (1, 3)]
PRE_ = [0, 2, 1, 3]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    W, H = x1 - x0 - 160, y1 - y0 - 110
    P = {k: (x0 + 80 + v[0] * W, y0 + 55 + v[1] * H) for k, v in POS_.items()}
    inn = S.get('_inner', {})
    cx, cy = inn.get('x'), inn.get('y')
    cv.text((x0 + 18, y0 + 4), '有向边（箭头方向）；黄 = 正在走的树边，从 x 走向 y', 22, T['muted'], bold=True)
    for a, b in ORIG_:
        hot = (cx, cy) in ((a, b), (b, a))
        col = T['dim'] if not hot else (T['green'] if (cx, cy) == (a, b) else T['pink'])
        (ax, ay), (bx, by) = P[a], P[b]
        d = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5
        ux, uy = (bx - ax) / d, (by - ay) / d
        cv.arrow((ax + ux * 36, ay + uy * 36), (bx - ux * 36, by - uy * 36), col, 7 if hot else 4, 16)
        if hot:
            dv = 1 if (cx, cy) == (a, b) else -1
            mx, my = (ax + bx) / 2, (ay + by) / 2
            txt = 'dir=+1：x→y 顺着箭头，换根后 y 要反向' if dv == 1 else 'dir=−1：x→y 逆着箭头，换根后少一次反向'
            s = '+1' if dv == 1 else '−1'
            cv.text((mx + (30 if bx >= ax else -30), my), 'dir=' + s, 26, col, anchor='lm' if bx >= ax else 'rm', bold=True)
    ans = S.get('ans')
    reroot_phase = S.get('_line', 0) >= 16
    y_ = S.get('y') if reroot_phase else None
    known = set(PRE_[:PRE_.index(y_) + 1]) if y_ is not None else set()
    for k, (px, py) in P.items():
        cv.rect((px - 28, py - 28, px + 28, py + 28), fill=T['panel2'], outline=T['blue'], width=3, r=28)
        if k == cx:
            cv.rect((px - 36, py - 36, px + 36, py + 36), outline=T['yellow'], width=5, r=36)
        if k == cy:
            cv.rect((px - 36, py - 36, px + 36, py + 36), outline=T['pink'], width=5, r=36)
        cv.text((px, py), k, 30, T['text'], anchor='mm', bold=True)
        if reroot_phase and ans is not None and (ans[k] != 0 or k in known):
            lf = k == 0
            cv.text((px - 44 if lf else px + 44, py - 4), 'ans=%d' % ans[k], 26, T['orange'], anchor='rm' if lf else 'lm', bold=True, mono=True)
    if not reroot_phase and ans is not None:
        cv.text((x0 + 18, y1 - 40), f'以 0 为根，需要反向的边数 ans[0] = {ans[0]}', 28, T['orange'], bold=True)


def c_dfs(S, B, ret):
    x, y = S['_inner']['x'], S['_inner']['y']
    d = [d for yy, d in S.g[x] if yy == y][0]
    if d < 0:
        return f'走 `{x}→{y}`，建图时这条边记的是 `dir={d}`：原边是 `{y}→{x}`，==从根往下走要反向== → `ans[0]` 加 1'
    return f'走 `{x}→{y}`，`dir={d}`：原边正是 `{x}→{y}`，顺着走不用反向 → `ans[0]` 不变'


def c_re(S, B, ret):
    x, y = S['_inner']['x'], S['_inner']['y']
    d = S['dir']
    why = '原来 x→y 顺着箭头，换根后 y 要走回 x，这条边==变成要反向==' if d > 0 else '原来 x→y 逆着箭头（要反向），换根后 y→x 顺着箭头，==少一次反向=='
    return f'`ans[{y}] = ans[{x}] + dir` = {S.ans[x]} {"+" if d>0 else "−"} 1 = =={S.ans[y]}==：{why}'


CONFIG = dict(
    num=2858, title='可以到达每一个节点的最少边反转次数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='换根 DP · 边权 ±1',
    tags=['灵神题单', '动态规划', '难度分 2295'],
    code='''
class Solution:
    def minEdgeReversals(self, n: int, edges: List[List[int]]) -> List[int]:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append((y, 1))
            g[y].append((x, -1))  # 从 y 到 x 需要反向

        ans = [0] * n
        def dfs(x: int, fa: int) -> None:
            for y, dir in g[x]:
                if y != fa:
                    ans[0] += dir < 0
                    dfs(y, x)
        dfs(0, -1)

        def reroot(x: int, fa: int) -> None:
            for y, dir in g[x]:
                if y != fa:
                    ans[y] = ans[x] + dir  # dir 就是从 x 换到 y 的「变化量」
                    reroot(y, x)
        reroot(0, -1)
        return ans
''',
    call='Solution().minEdgeReversals(4, [[2,0],[2,1],[1,3]])',
    expect=[1, 1, 0, 2],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='array', var='ans', label='ans', h=95),
        dict(type='calls', h=140),
    ],
    watch=['x', 'y', 'dir'],
    skip=['g = [[]', 'g[x].append', 'g[y].append', 'for x, y in edges', 'if y != fa'],
    captions={
        'ans[0] += dir < 0': c_dfs,
        'ans = [0] * n': '`ans[0]` 先当计数器：数「以 0 为根时需要反向的边」',
        'dfs(0, -1)': '第一次 DFS：从 0 出发，沿树边往下走，统计要反向的边数',
        'reroot(0, -1)': '第二次 DFS：换根，`ans[y]` 只需在 `ans[x]` 上加减 1',
        'ans[y] = ans[x] + dir': c_re,
        'return ans': '每个点的答案都算出来了',
    },
    cards=dict(
        one_liner='建图时给边打上 ±1，换根就是 `ans[y] = ans[x] + dir`',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个点的有向图，忽略方向后是一棵树；反转一条边 = 改变它的方向',
                 '对每个点 `i`，求从 `i` 出发到达所有点最少要反转几条边',
                 '示例：`edges=[[2,0],[2,1],[1,3]]` → `[1,1,0,2]`'],
        quote='对于一条 x→y 的边，把 (y,1) 加到 x 的邻居，把 (x,-1) 加到 y 的邻居，从而可以在递归过程中统计有多少条边是需要反向的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['建图：顺着走记 `+1`，逆着走记 `−1`（逆着走说明这条边需要反转）',
              '第一次 DFS：以 0 为根，`dir < 0` 的边就是要反向的，累加到 `ans[0]`',
              '换根：从 x 到 y 只改变这一条边的父子关系，所以 `ans[y] = ans[x] + dir`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`dir` 的含义是「从 x 换到 y 的变化量」，和建图时的符号一致，别写反',
                 '`ans[0] += dir < 0`：布尔值当 0/1 加',
                 '类似题：2581 统计可能的树根数目'],
    ),
)
