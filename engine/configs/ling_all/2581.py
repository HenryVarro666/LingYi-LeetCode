import math as _m


def _tgraph(cv, T, box, pos, edges, ncol, nsub, ecol, title, R=30, bottom=62, side=None):
    """通用树/图：pos 为 0..1 的相对坐标；nsub 返回 str 或 [str]（画在节点下方）"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    L, Rr, Tp, Bt = x0 + 80, x1 - 80, y0 + 52 + R + (50 if 'a' in (side or {}).values() else 0), y1 - R - bottom
    P = {u: (L + fx * (Rr - L), Tp + fy * (Bt - Tp)) for u, (fx, fy) in pos.items()}
    for u, v in edges:
        c, wd = ecol(u, v)
        cv.line([P[u], P[v]], c, wd)
    for u, (px, py) in P.items():
        fc = ncol(u)
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fc, outline=T['border'], width=2)
        cv.text((px, py), u, 28, T['bg'] if fc != T['panel2'] else T['text'], anchor='mm', bold=True)
        s = nsub(u)
        if s is None:
            continue
        sd = (side or {}).get(u, 'b')
        for k, line in enumerate([s] if isinstance(s, str) else s):
            if sd == 'b':
                cv.text((px, py + R + 4 + k * 23), line, 20, T['yellow'], anchor='mt', bold=True, mono=True)
            elif sd == 'a':
                cv.text((px, py - R - 4 - (len(s) - 1 - k) * 23 if not isinstance(s, str) else py - R - 4), line, 20, T['yellow'], anchor='mb', bold=True, mono=True)
            elif sd == 'r':
                cv.text((px + R + 8, py - R - 4 + k * 23), line, 20, T['yellow'], anchor='lm', bold=True, mono=True)
            else:
                cv.text((px - R - 8, py - R - 4 + k * 23), line, 20, T['yellow'], anchor='rm', bold=True, mono=True)
EDGES = [(0, 1), (1, 2), (1, 3), (4, 2)]
GUESSES = [(1, 3), (0, 1), (1, 0), (2, 4)]
K = 3
POS = {0: (0.05, 0.12), 1: (0.34, 0.12), 2: (0.66, 0.12), 4: (0.95, 0.12), 3: (0.34, 1.0)}
SIDE = {0: 'b', 1: 'a', 2: 'b', 4: 'b', 3: 'b'}


def _parents(root):
    adj = {}
    for a, b in EDGES:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    par, seen, q = {root: None}, {root}, [root]
    for u in q:
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                par[v] = u
                q.append(v)
    return par


def _draw_guess(cv, T, box, root, ncol, nsub, ecol, title):
    x0, y0, x1, y1 = box
    par = _parents(root)
    R = 30
    L, Rr, Tp, Bt = x0 + 80, x1 - 80, y0 + 100 + R, y1 - R - 70
    P = {u: (L + fx * (Rr - L), Tp + fy * (Bt - Tp)) for u, (fx, fy) in POS.items()}
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    for u, v in EDGES:
        c, wd = ecol(u, v)
        cv.line([P[u], P[v]], c, wd)
    for u, v in GUESSES:
        (ax, ay), (bx, by) = P[u], P[v]
        d = _m.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / d, (by - ay) / d
        nx, ny = -uy * 13, ux * 13
        ok = par.get(v) == u
        c = T['green'] if ok else T['red']
        cv.arrow((ax + ux * (R + 6) + nx, ay + uy * (R + 6) + ny), (bx - ux * (R + 8) + nx, by - uy * (R + 8) + ny), c, 4 if ok else 2, 14)
    for u, (px, py) in P.items():
        fc = ncol(u)
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fc, outline=T['border'], width=2)
        cv.text((px, py), u, 28, T['bg'] if fc != T['panel2'] else T['text'], anchor='mm', bold=True)
        s = nsub(u)
        if s is not None:
            cv.text((px, py - R - 6), s, 22, T['yellow'], anchor='mb', bold=True, mono=True)
    cv.text((x0 + 18, y1 - 34), f'绿箭头 = 以 {root} 为根时猜对（u 是 v 的父节点），红箭头 = 猜错', 20, T['muted'])
def _ctx(S):
    inn = S['_inner']
    ph = 'reroot' if 'cnt' in inn else ('dfs' if 'fa' in inn else None)
    return ph, inn


def _draw(cv, S, B, box, T):
    ph, inn = _ctx(S)
    x = inn.get('x') if ph else None
    y = inn.get('y') if ph else None
    root = x if ph == 'reroot' else 0

    def ncol(u):
        if u == x:
            return T['blue']
        if u == y and ph:
            return T['yellow']
        return T['panel2']

    def nsub(u):
        if ph == 'reroot' and u == x:
            return f"cnt={inn['cnt']}"
        if ph == 'dfs' and u == x:
            return f"cnt0={S.get('cnt0')}"
        return None

    def ecol(u, v):
        if ph and x is not None and y is not None and {u, v} == {x, y}:
            return T['yellow'], 6
        return T['border'], 3

    _draw_guess(cv, T, box, root, ncol, nsub, ecol,
                '树 + 猜测（蓝 = 当前 x，黄 = 正要走过去的 y）')


def _txt(S):
    ph, inn = _ctx(S)
    if ph == 'reroot':
        x, cnt, k = inn['x'], inn['cnt'], S['k']
        return f"以 `{x}` 为根猜对 `cnt = {cnt}`，`k = {k}` → " + ('==达标，ans 计一个==' if cnt >= k else '不够，不计')
    if ph == 'dfs':
        return f"以 0 为根：目前猜对 `cnt0 = {S.get('cnt0')}`"
    return '先以 0 为根数一遍猜对次数，再换根'


CONFIG = dict(
    num=2581, title='统计可能的树根数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='换根 DP',
    tags=['灵神题单·动态规划', '难度分 2228'],
    code='''
class Solution:
    def rootCount(self, edges: List[List[int]], guesses: List[List[int]], k: int) -> int:
        g = [[] for _ in range(len(edges) + 1)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)  # 建图

        s = {(x, y) for x, y in guesses}  # guesses 转成哈希表 s

        ans = cnt0 = 0
        def dfs(x: int, fa: int) -> None:
            nonlocal cnt0
            for y in g[x]:
                if y != fa:
                    cnt0 += (x, y) in s  # 以 0 为根时，猜对了
                    dfs(y, x)
        dfs(0, -1)

        def reroot(x: int, fa: int, cnt: int) -> None:
            nonlocal ans
            ans += cnt >= k  # 此时 cnt 就是以 x 为根时的猜对次数
            for y in g[x]:
                if y != fa:
                    reroot(y, x, cnt - ((x, y) in s) + ((y, x) in s))
        reroot(0, -1, cnt0)
        return ans
''',
    call='Solution().rootCount([[0,1],[1,2],[1,3],[4,2]], [[1,3],[0,1],[1,0],[2,4]], 3)',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='calls', h=190),
    ],
    watch=[('x', lambda S: S['_inner'].get('x'), 'blue'), ('cnt0', 'cnt0', 'cyan'),
           ('cnt', lambda S: S['_inner'].get('cnt'), 'yellow'), ('ans', 'ans', 'green')],
    skip=['g[x].append(y)', 'g[y].append(x)', 'for x, y in edges', 'for y in g[x]', 'if y != fa', 'nonlocal'],
    max_steps=80,
    captions={
        'g = [[]': '先建邻接表 `g`（树无向）',
        's = {': '`guesses` 转成哈希集合 `s`：判断「x 是 y 的父」只需 `(x, y) in s`',
        'ans = cnt0 = 0': '`cnt0`：以 0 为根的猜对次数；`ans`：满足 `>= k` 的根的个数',
        'cnt0 += (x, y)': lambda S, B, r: (f"以 0 为根时 `{B.x}` 是 `{B.y}` 的父节点：" +
                                          (f'猜测 `[{B.x},{B.y}]` 存在 → ==猜对 +1==，`cnt0 = {S.cnt0}`' if (B.x, B.y) in S.s
                                           else f'没有猜测 `[{B.x},{B.y}]` → `cnt0` 不变 = {S.cnt0}')),
        'dfs(y, x)': '往下走到 `{B.y}`（父节点 `{B.x}`）',
        'dfs(0, -1)': '先 DFS 一次：以 0 为根，数出 `cnt0`',
        'ans += cnt >= k': ('以 `{x}` 为根的猜对次数 `cnt = {cnt}`，`{cnt} >= {k}` 为 ' + '{cnt >= k}' + ' → `ans = {ans}`'),
        'reroot(y, x, cnt': ('换根 `{B.x} → {B.y}`：只有 `[{B.x},{B.y}]`、`[{B.y},{B.x}]` 的对错变了\n'
                             '`{B.cnt} − {int((B.x, B.y) in B.s)} + {int((B.y, B.x) in B.s)} = {B.cnt - ((B.x, B.y) in B.s) + ((B.y, B.x) in B.s)}`'),
        'reroot(0, -1, cnt0)': '从 0 再 DFS 一次：`cnt0` 就是以 0 为根的答案，往邻居传递',
        'return ans': '满足 `cnt >= {k}` 的根一共 `{ans}` 个',
    },
    cards=dict(
        one_liner='先数出以 0 为根的猜对数，换根时只改两个猜测的对错',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['`edges` 是一棵 `n` 个点的树；Bob 猜了若干「u 是 v 的父节点」',
                 '至少猜对 `k` 个时，哪些点可能是根？返回这样的点的个数',
                 '示例：`k = 3`，`guesses = [[1,3],[0,1],[1,0],[2,4]]` → `3`'],
        quote='从「以 x 为根的树」变成「以 y 为根的树」，就只有 x 和 y 的父子关系改变了，==只有 [x,y] 和 [y,x] 这两个猜测的正确性变了==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举每个根各 DFS 一次要 `O(n^2)`',
              '先 DFS 求 `cnt0`：以 0 为根时猜对多少',
              '从 x 走到 y：有猜测 `[x,y]` 则 `-1`，有 `[y,x]` 则 `+1`',
              '换根的同时统计 `cnt >= k` 的点数'],
        summary=['两次 DFS：时间 `O(n+m)`，空间 `O(n+m)`',
                 '`guesses` 转哈希集合，查询 `(x, y) in s` 是 `O(1)`',
                 '换根方向别写反：x→y 时 x 不再是 y 的父，`[x,y]` 要减，`[y,x]` 要加',
                 '`ans += cnt >= k`：布尔值直接当 0/1 累加',
                 '思考题：改成「祖先」或带分数的猜测，思路类似'],
    ),
)
