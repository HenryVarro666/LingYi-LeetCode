EDGES = [[0, 1, 2], [0, 2, 3], [1, 3, 3], [2, 3, 4]]
N, K, TT = 4, 2, 7


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f = S.get('f')
    if f is None or 'now' not in S:
        f = S.get('f')
        if f is None:
            return
    now, kk = S.get('now'), S.get('k')
    nxt = S.get('nxt')
    cv.text((x0 + 18, y0 + 4), f'f[now][k]：从 now 出发恰好走 k 条边的所有合法边权和（t = {TT}）；? = 还没算', 22, T['muted'], bold=True)
    gx, gy = x0 + 110, y0 + 86
    cw = (x1 - x0 - 130) / (K + 1)
    ch = 64
    for c in range(K + 1):
        cv.text((gx + c * cw + cw / 2, gy - 8), f'k = {c}', 22, T['cyan'], anchor='mb', bold=True)
    for r in range(N):
        cv.text((gx - 10, gy + r * ch + ch / 2), f'节点 {r}', 22, T['muted'], anchor='rm', bold=True)
        for c in range(K + 1):
            st = f[r][c]
            bst = B['f'][r][c] if B.get('f') is not None else st
            changed = (st is not None and bst is not None and set(st) != set(bst)) or (st is not None and bst is None)
            cur = now is not None and (r, c) == (now, kk)
            nb = nxt is not None and kk is not None and (r, c) == (nxt, kk - 1) and S.get('_line', 0) >= 23
            X, Y = gx + c * cw, gy + r * ch
            oc = T['yellow'] if cur else (T['pink'] if nb else T['border'])
            cv.rect((X + 3, Y + 3, X + cw - 3, Y + ch - 3), fill=T['panel2'], r=8, outline=oc, width=4 if (cur or nb) else 1)
            if st is None:
                txt, col = '?', T['dim']
            elif not st:
                txt, col = '∅', T['muted']
            else:
                txt, col = '{' + ','.join(str(v) for v in sorted(st)) + '}', T['green'] if changed else T['text']
            cv.text((X + cw / 2, Y + ch / 2), txt, 26, col, anchor='mm', mono=True, bold=True)
    cv.text((gx, gy + N * ch + 6), '黄框 = 正在算的 f[now][k]，粉框 = 要用到的 f[nxt][k-1]', 22, T['muted'])


def _stk(S, B, r):
    pass


CONFIG = dict(
    num=3543, title='K 条边路径的最大边权和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='记忆化 DFS · 状态存可行边权和的集合',
    tags=['灵神题单·动态规划', '难度分 2110'],
    code='''
class Solution(object):
    def maxWeight(self, n, edges, k, t):

        f = [[None for _ in range(k + 1)] for _ in range(n)]

        g = [[] for _ in range(n)]
        ind = [0] * n
        for x, y, w in edges:
            g[x].append((y, w))
        
        def dfs(now, k, f):
            if f[now][k] is None:
                f[now][k] = set()
                if k == 0:
                    f[now][k].add(0)
                else:
                    for nxt, w in g[now]:
                        dfs(nxt, k - 1, f)
                        for v in f[nxt][k - 1]:
                            if v + w < t:
                                f[now][k].add(v + w)

        res = -1
        for x in range(n):
            dfs(x, k, f)
            if f[x][k]:
                res = max(res, max(f[x][k]))
        
        return res
''',
    call=f'Solution().maxWeight({N}, {EDGES}, {K}, {TT})',
    expect=5,
    views=[
        dict(type='custom', draw=_draw, h=380),
        dict(type='calls', h=170, hide=('f', 'edges')),
    ],
    watch=['now', 'k', 'nxt', 'w', 'v', ('res', 'res', 'green')],
    skip=['ind = [0] * n', 'g[x].append', 'for x, y, w in edges', 'for nxt, w in g[now]', 'for v in f[nxt][k - 1]'],
    captions={
        'f = [[None': '`f[now][k]` 记录「从 now 出发、恰好 k 条边」的==全部==合法边权和；`None` 表示还没算',
        'g = [[] for': '`g[x]` 存 x 出发的边 `(y, w)`',
        'if f[now][k] is None': lambda S, B, r: (f'`f[{S.now}][{S.k}]` 还没算 → 现在算' if S.f[S.now][S.k] is None
                                                  else f'`f[{S.now}][{S.k}]` 已经算过 = `{sorted(S.f[S.now][S.k])}` → ==直接复用==，不再递归'),
        'f[now][k] = set()': '先放一个空集合，后面往里加',
        'if k == 0': lambda S, B, r: ('`k = 0`：不用走边，边权和只有 `0`' if S.k == 0 else f'`k = {S.k}`：还要走 {S.k} 条边，枚举 `{S.now}` 的出边'),
        'f[now][k].add(0)': '`f[{now}][0] = {{0}}`',
        'dfs(nxt, k - 1, f)': lambda S, B, r: (f'走边 `{B.now} → {B.nxt}`（权 {B.w}）：先要知道 `f[{B.nxt}][{B.k - 1}]`' +
                                               ('，还没算 → ==递归进去算==' if B.f[B.nxt][B.k - 1] is None else f' = `{sorted(B.f[B.nxt][B.k - 1])}`，已算过')),
        'if v + w < t': lambda S, B, r: (f'取 `f[{S.nxt}][{S.k - 1}]` 里的和 `v = {S.v}`，接上边权：`{S.v} + {S.w} = {S.v + S.w}`，要 `< t = {S.t}` → ' +
                                         ('==成立==' if S.v + S.w < S.t else '==不成立==，丢掉；==不能只存最大值==，因为大的会超 t，小的才可能合法')),
        'f[now][k].add(v + w)': '`{v + w}` 加入 `f[{now}][{k}]` → `{sorted(f[now][k])}`',
        'res = -1': '`res` 记录所有起点中的最大边权和',
        'for x in range(n)': lambda S, B, r: (f'枚举起点 `x = {S.x}`' if S.x != B.get('x') or B.get('x') is None else '所有起点都试过了'),
        'dfs(x, k, f)': '从起点 `{x}` 出发，要走 `{k}` 条边：调用 `dfs` 算 `f[{x}][{k}]`',
        'if f[x][k]': lambda S, B, r: (f'`dfs` 算完：`f[{S.x}][{S.k}] = {sorted(S.f[S.x][S.k])}` 非空 → 取最大值去更新 `res`' if S.f[S.x][S.k] else f'`f[{S.x}][{S.k}]` 为空：从 {S.x} 出发凑不出合法路径'),
        'res = max': '`res = max({B.res}, {max(f[x][k])}) = {res}`',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='最大值不能直接传递，要把所有可行的边权和都记下来',
        complexity='时间 `O(n·k·t + m·k·t)`，空间 `O(n·k·t)`',
        problem=['有向无环图，找==恰好 k 条边==、边权和==小于 t==的路径，求最大边权和，没有则 -1',
                 '本视频：`n=4`，边 `0→1(2) 0→2(3) 1→3(3) 2→3(4)`，`k=2, t=7`',
                 '路径 `0→1→3` 和为 5；`0→2→3` 和为 7，不小于 t，所以答案 `5`'],
        quote='对于有限制的最大值问题，一般的最大值状态表示是不可行的。……因为从某个节点出发的最优路径不一定可以更新其前置节点的最优路径。',
        quote_src='—— yiduobo 题解原文',
        idea=['只存「最大和」会出错：例如 `1→3(6)` 大，但接到前面 `0→1(3)` 就 9 > 8，而 `1→2(4)` 才合法',
              '所以令 `f[now][k]` = 从 now 出发走 k 条边的==所有合法边权和集合==',
              '记忆化 DFS：`k=0` 只有 `{0}`；否则枚举出边，把 `f[nxt][k-1]` 里每个 `v` 加上 `w`，小于 t 才收下'],
        summary=['时间 `O(m·k·t)`，空间 `O(n·k·t)`；集合最多 t 个数',
                 '易错：`v + w < t` 是==严格小于==；集合为空要跳过，不能取 max',
                 '`dfs` 的形参 `k`、`f` 把外层同名变量遮住了，看递归栈时别混淆',
                 '对比灵神：灵神从边数 i 往后推（正向刷表），yiduobo 从终点往回递归（反向记忆化）'],
    ),
)
