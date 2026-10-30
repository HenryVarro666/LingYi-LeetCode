EDGES = [[0, 1, 2], [0, 2, 3], [1, 3, 3], [2, 3, 4]]
N, K, TT = 4, 2, 7
LINE_E = 'for x, y, wt in edges'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f = S.get('f')
    if f is None:
        return
    line = S.get('_inner', S).get('_line', S.get('_line'))
    cur_i = S.get('i')
    x, y = S.get('x'), S.get('y')
    live_edge = x is not None and 'wt' in S and S.get('_line', 0) >= 10
    # 边列表
    cv.text((x0 + 18, y0 + 4), f'edges（黄 = 当前边 x→y，权 wt）     t = {TT}：和必须 < {TT}', 22, T['muted'], bold=True)
    ex = x0 + 20
    for e in EDGES:
        s_ = f'{e[0]}→{e[1]}  w={e[2]}'
        w = cv.tlen(s_, 22, mono=True) + 24
        on = live_edge and [e[0], e[1]] == [x, y]
        cv.rect((ex, y0 + 40, ex + w, y0 + 82), fill=T['yellow'] if on else T['panel2'], outline=T['border'], r=10)
        cv.text((ex + w / 2, y0 + 61), s_, 22, T['bg'] if on else T['text'], anchor='mm', mono=True, bold=True)
        ex += w + 10
    # f 表：行 = 边数 i，列 = 终点节点
    gx, gy = x0 + 100, y0 + 160
    cw = (x1 - x0 - 120) / N
    ch = 100
    for c in range(N):
        cv.text((gx + c * cw + cw / 2, gy - 8), f'节点 {c}', 22, T['cyan'], anchor='mb', bold=True)
    for r in range(K + 1):
        cv.text((gx - 10, gy + r * ch + ch / 2), f'{r} 条边', 22, T['muted'], anchor='rm', bold=True)
        for c in range(N):
            st = f[r][c]
            bst = B['f'][r][c] if B.get('f') is not None else st
            new = set(st) - set(bst)
            src = live_edge and cur_i is not None and r == cur_i and c == x
            dst = live_edge and cur_i is not None and r == cur_i + 1 and c == y
            fill = T['panel2']
            X, Y = gx + c * cw, gy + r * ch
            cv.rect((X + 3, Y + 3, X + cw - 3, Y + ch - 3), fill=fill, r=8,
                    outline=T['pink'] if src else (T['yellow'] if (dst or new) else T['border']), width=4 if (src or dst or new) else 1)
            parts = sorted(st)
            txt = '{' + ','.join(str(v) for v in parts) + '}' if parts else '∅'
            cv.text((X + cw / 2, Y + ch / 2), txt, 26, T['dim'] if not parts else T['text'], anchor='mm', mono=True, bold=True)
            if new:
                cv.text((X + cw - 8, Y + 6), f'+{max(new)}', 20, T['green'], anchor='ra', bold=True)
    sy = gy + (K + 1) * ch + 14
    if live_edge and cur_i is not None:
        cv.text((gx, sy), f'粉框 = 起点集合 f[{cur_i}][{x}]，黄框 = 要加入的 f[{cur_i + 1}][{y}]', 22, T['muted'])


def _txt(S):
    if 'wt' in S and 's' in S and S.get('_line', 0) >= 12:
        return f"`s + wt = {S['s']} + {S['wt']} = {S['s'] + S['wt']}`，和 `t = {TT}` 比：{'更小，可以走' if S['s'] + S['wt'] < TT else '不小于 t，不能走'}"
    return ''


CONFIG = dict(
    num=3543, title='K 条边路径的最大边权和', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='按边数分层的一般图 DP · 集合记录可达边权和',
    tags=['灵神题单·动态规划', '难度分 2110'],
    code='''
class Solution:
    def maxWeight(self, n: int, edges: List[List[int]], k: int, t: int) -> int:
        if n <= k:
            return -1

        f = [[set() for _ in range(n)] for _ in range(k + 1)]
        for i in range(n):
            f[0][i].add(0)
        for i in range(k):
            for x, y, wt in edges:
                for s in f[i][x]:
                    if s + wt < t:
                        f[i + 1][y].add(s + wt)
        return max((max(st) for st in f[k] if st), default=-1)
''',
    call=f'Solution().maxWeight({N}, {EDGES}, {K}, {TT})',
    expect=5,
    views=[
        dict(type='text', fn=_txt, h=50),
        dict(type='custom', draw=_draw, h=450),
    ],
    watch=['i', 'x', 'y', 'wt', 's'],
    skip=['for s in f[i][x]'],
    captions={
        'if n <= k': lambda S, B, r: (f'`n = {S.n} > k = {S.k}`：DAG 最长路径至多 `n-1 = {S.n - 1}` 条边，够用，继续' if S.n > S.k
                                      else '`n <= k`：DAG 里凑不出 k 条边 → 直接 -1'),
        'f = [[set()': '`f[i][x]` = 一个==集合==：终点在 `x`、恰好 `i` 条边的路径，所有可能的边权和（不只存最大值！）',
        'f[0][i].add(0)': '0 条边时，每个点单独是一条路径，边权和 `0`：`f[0][{i}] = {{0}}`',
        'for i in range(k)': lambda S, B, r: ('所有层都推完了，`f[k]` 里就是 k 条边路径的全部边权和' if S.i == B.i else
                                              f'按边数从小到大：用 `f[{S.i}]` 层（{S.i} 条边）去推 `f[{S.i + 1}]` 层'),
        'for x, y, wt in edges': lambda S, B, r: ('这一层的边都处理完了' if (S.x, S.y) == (B.get('x'), B.get('y')) else
                                                  f'无需建图，直接遍历有向边 `{S.x} → {S.y}`，边权 `wt = {S.wt}`' +
                                                  ('' if S.f[S.i][S.x] else f'；`f[{S.i}][{S.x}]` 是空集，没有路径可延伸')),
        'if s + wt < t': lambda S, B, r: (f'`f[{S.i}][{S.x}]` 里的和 `s = {S.s}`，再走这条边：`{S.s} + {S.wt} = {S.s + S.wt}`，要 `< t = {S.t}` → ' +
                                          ('==成立==' if S.s + S.wt < S.t else '==不成立==：等于 t 也不行（严格小于），丢掉')),
        'f[i + 1][y].add': '`{s + wt}` 合法 → 加进 `f[{i + 1}][{y}]`，现在是 `{sorted(f[i + 1][y])}`',
        'return max': lambda S, B, r: f'答案：`f[k]` 这一层所有节点的集合里取最大值 = ==`{r}`==（都为空则 -1）',
    },
    cards=dict(
        one_liner='按边数分层，每个状态存「所有可能的边权和」',
        complexity='时间 `O(m·k·t)`，空间 `O(n·k·t)`（可滚动数组优化）',
        problem=['有向无环图，每条边有权值；找==恰好 k 条边==、边权和==严格小于 t==的路径',
                 '返回满足条件的最大边权和，没有就返回 -1',
                 '本视频：`n=4`，边 `0→1(2) 0→2(3) 1→3(3) 2→3(4)`，`k=2, t=7`，答案 `5`'],
        quote='在方法一和方法二中，边的个数 i 是递增的，我们可以从 i 入手计算状态。……==无需建图==，遍历 edges，对于边权为 w 的有向边 x→y，如果 f[i][x] 中有 s 且 s+w<t，那么把 s+w 加到 f[i+1][y] 中。',
        quote_src='—— 灵茶山艾府题解 方法三',
        idea=['`f[i][x]`：终点在 x、有 i 条边的路径，边权和的==集合==',
              '把 i 放到最外层，一层层往下推：这样图有没有环都对，因为 i 一直在增加',
              '最后看 `f[k]`，每个集合里取最大值，再对所有节点取最大'],
        summary=['时间 `O(m·k·t)`，空间 `O(n·k·t)`；忽略建表，用滚动数组可降到 `O(n·t)`',
                 '易错：是 `s + wt < t`，==严格小于==，等于 t 也不行',
                 '开头的 `n <= k` 判断：DAG 路径至多 `n-1` 条边，直接返回 -1',
                 '题解另有两种写法：记忆化 DFS、拓扑序 DP，以及用二进制数当 bitset 的优化，思路相同'],
    ),
)
