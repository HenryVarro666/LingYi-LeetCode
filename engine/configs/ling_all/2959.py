N0 = 3
MAXD = 5
ROADS = [[0, 1, 2], [1, 2, 10], [0, 2, 10]]
POS = {0: (0.50, 0.12), 1: (0.14, 0.86), 2: (0.86, 0.86)}


def _kept(s):
    return [i for i in range(N0) if s >> i & 1]


def _bad(S):
    """pair (i,j) kept in s whose f[s][i][j] > maxDistance (only meaningful after the DP row is computed)"""
    s = S.get('s')
    if s is None or 'ok' not in S or S.get('_line', 0) not in (20, 21):
        return None
    f = S['f'][s]
    for i in range(N0):
        for j in range(i):
            if s >> i & 1 and s >> j & 1 and f[i][j] > MAXD:
                return (i, j)
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s = S.get('s')
    cv.text((x0 + 18, y0 + 4), '绿圈 = 保留的分部，灰 × = 关闭的分部；线上是道路长度', 21, T['muted'], bold=True)
    gx0, gy0 = x0 + 120, y0 + 60
    gw, gh = (x1 - x0) - 240, (y1 - y0) - 110
    P = {k: (gx0 + v[0] * gw, gy0 + v[1] * gh) for k, v in POS.items()}
    bad = _bad(S)
    for x, y, w in ROADS:
        both = s is not None and (s >> x & 1) and (s >> y & 1)
        isbad = bad is not None and {x, y} == set(bad)
        col = T['red'] if isbad else (T['blue'] if both else (70, 76, 86))
        cv.line([P[x], P[y]], col, 8 if isbad else (6 if both else 3))
        mx, my = (P[x][0] + P[y][0]) / 2, (P[x][1] + P[y][1]) / 2
        if x == 1 and y == 2:
            my += 4
        cv.rect((mx - 30, my - 17, mx + 30, my + 17), fill=T['bg'], r=8)
        cv.text((mx, my), w, 24, T['text'] if both else T['dim'], anchor='mm', bold=True, mono=True)
    if bad:
        i, j = bad
        cx = sum(p[0] for p in P.values()) / 3
        cy = sum(p[1] for p in P.values()) / 3 + 38
        cv.rect((cx - 112, cy - 20, cx + 112, cy + 20), fill=T['bg'], outline=T['red'], width=3, r=10)
        cv.text((cx, cy), f'最短路 {S["f"][s][i][j]} > {MAXD}', 22, T['red'], anchor='mm', bold=True)
    for k in range(N0):
        X, Y = P[k]
        on = s is not None and (s >> k & 1)
        if on:
            cv.rect((X - 34, Y - 34, X + 34, Y + 34), fill=T['panel2'], outline=T['green'], width=6, r=34)
            cv.text((X, Y), k, 32, T['text'], anchor='mm', bold=True)
        else:
            cv.rect((X - 34, Y - 34, X + 34, Y + 34), fill=T['bg'], outline=(80, 86, 96), width=3, r=34)
            cv.text((X, Y), k, 30, T['dim'], anchor='mm', bold=True)
            if s is not None:
                cv.text((X + 44, Y - 30), '×', 30, T['red'], anchor='mm', bold=True)


def _txt(S):
    s = S.get('s')
    if s is None:
        return '枚举保留集合 `s`：二进制第 i 位为 1 表示保留分部 i'
    n = N0
    bits = format(s, f'0{n}b')
    keep = '{' + ','.join(map(str, _kept(s))) + '}'
    k = S.get('k')
    ext = f'　最高位 `k = {k}`，`t = {S["t"]}`' if k is not None and 't' in S and S.get('_line', 0) >= 13 else ''
    return f'`s = {s}` = 二进制 `{bits}` → 保留 =={keep}=={ext}'


def _cell(S, i, j, v):
    s = S.get('s')
    if s is None or not (s >> i & 1 and s >> j & 1) or i == j:
        return None
    if S.get('_line', 0) not in (20, 21):
        return None
    return 'red' if v > MAXD else 'green'


def _fs(S):
    s = S.get('s')
    return S['f'][s if s is not None else 0]


def _ans_cap(S, B, r):
    s = S.s
    keep = '{' + ','.join(map(str, _kept(s))) + '}'
    b = _bad(S)
    if len(_kept(s)) <= 1:
        why = f'保留 {keep} 至多一个分部，没有点对要检查'
    elif b is None:
        why = f'保留 {keep} 内所有点对的最短路都 ≤ {MAXD}'
    else:
        why = f'保留 {keep} 中 `f[{s}][{b[0]}][{b[1]}] = {S.f[s][b[0]][b[1]]}` > {MAXD}'
    return f'{why} → `ok = {S.ok}`，`ans` 变成 =={S.ans}=='


CONFIG = dict(
    num=2959, title='关闭分部的可行集合数目', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='状压 DP + Floyd（增量加点）',
    tags=['灵神题单·图论算法', '灵神题单·链表树与回溯', '难度分 2077'],
    code='''
class Solution:
    def numberOfSets(self, n: int, maxDistance: int, roads: List[List[int]]) -> int:
        g = [[inf] * n for _ in range(n)]
        for x, y, wt in roads:
            g[x][y] = min(g[x][y], wt)
            g[y][x] = min(g[y][x], wt)

        ans = 1  # s=0 一定满足要求
        f = [[[inf] * n for _ in range(n)] for _ in range(1 << n)]
        f[0] = g
        for s in range(1, 1 << n):
            k = s.bit_length() - 1
            t = s ^ (1 << k)
            ok = 1
            for i in range(n):
                for j in range(n):
                    f[s][i][j] = min(f[t][i][j], f[t][i][k] + f[t][k][j])  # 手动求 min 可以更快
                    if ok and j < i and s >> i & 1 and s >> j & 1 and f[s][i][j] > maxDistance:
                        ok = 0
            ans += ok
        return ans
''',
    call=f'Solution().numberOfSets(3, {MAXD}, {ROADS})',
    expect=5,
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='text', fn=_txt, size=28, h=60),
        dict(type='table', var=_fs, label='f[s]：中间点取自 s 的最短路矩阵（红 = 保留点对超过 maxDistance）',
             rows=['0', '1', '2'], cols=['0', '1', '2'], color=_cell, cell=84, h=290),
    ],
    watch=[('s', 's', 'blue'), ('k', 'k', 'pink'), ('t', 't', 'cyan'), ('ok', 'ok', 'yellow'), ('ans', 'ans', 'green')],
    skip=['for x, y, wt in roads', 'f = [[[inf]', 'k = s.bit_length', 'g[y][x] = min', 'f[s][i][j] = min', 'if ok and j < i', 'ok = 0', 'for i in range(n)', 'for j in range(n)'],
    captions={
        'g = [[inf]': '`g` 是邻接矩阵：`g[x][y]` = 两点间最短的直连道路，没有就是 `inf`',
        'g[x][y] = min': '道路 `{x}-{y}` 长 `{wt}` 写进邻接矩阵（无向，两个方向；重边取最小）：`g[{x}][{y}] = {g[x][y]}`',
        'ans = 1': '`s = 0`：全部关闭，没有分部，一定满足 → `ans = 1`',
        'f[0] = g': '`f[S][i][j]`：中间点只能取自集合 `S` 的最短路，共 `2^n` 个矩阵。`S = ∅` 没有中间点，最短路就是直连道路 `g`',
        'for s in range': lambda S, B, r: ('所有 `s` 都枚举完了' if B.get('s') == S.s else f'枚举 `s = {S.s}`（二进制 `{S.s:03b}`）：保留 {_kept(S.s)}，其余关闭'),
        't = s ^': '最高位 `k = {k}`：把分部 `{k}` 当作==最后加入==的中间点；`t = s ^ (1<<k)` = `{t}`（二进制 `{t:03b}`），`f[t]` 早已算好。对每个点对：`f[s][i][j] = min(f[t][i][j], f[t][i][k] + f[t][k][j])`，只要 `O(n²)`',
        'ok = 1': '先假设 `s` 满足要求；再把 `f[s]` 整个 3×3 算出来，检查保留点对的最短路是否超过 `{maxDistance}`',
        'ans += ok': _ans_cap,
        'return ans': '共 `{ans}` 种可行方案',
    },
    cards=dict(
        one_liner='枚举保留集合，Floyd 一次只加一个中间点，O(n²) 增量更新',
        complexity='时间 `O(m + n²·2^n)`，空间 `O(n²·2^n)`',
        problem=['`n` 个分部、若干道路。关闭一些分部（可以不关），使剩下的分部两两最短距离 `≤ maxDistance`，求方案数',
                 '关闭一个分部后，与它相连的道路不能再走；`n ≤ 10`',
                 '本视频：`n=3, maxDistance=5, roads=[[0,1,2],[1,2,10],[0,2,10]]` → `5`'],
        quote='把定义改成：f[S][i][j] 表示从 i 到 j 的最短路长度，并且这条最短路的中间节点编号在集合 S 中。',
        quote_src='—— 灵茶山艾府题解（方法二：状压 DP + Floyd）',
        idea=['`n ≤ 10`，所以枚举所有 `2^n` 个保留集合 `s`',
              '从 `T` 加入节点 `k` 得到 `S`：`f[S][i][j] = min(f[T][i][j], f[T][i][k] + f[T][k][j])`，只要 `O(n²)`',
              '`i`、`j` 都在 `S` 里时，`f[S][i][j]` 就是只走保留点的最短路，可直接和 `maxDistance` 比'],
        summary=['时间 `O(m + n²·2^n)`，空间 `O(n²·2^n)`',
                 '易错：`S` 只是中间点集合，计算时 `i`、`j` 不必在 `S` 中；==检查时==才要求 `i`、`j` 都在 `S` 中',
                 '`s = 0`（全关）一定可行，所以 `ans` 从 1 开始',
                 '方法一：对每个子集单独跑一遍 Floyd，`O(n³·2^n)`；方法二把 Floyd 的“加点”变成子集转移，省掉一个 n',
                 '同类题：2976、2977（Floyd），78、77（二进制枚举）'],
    ),
)
