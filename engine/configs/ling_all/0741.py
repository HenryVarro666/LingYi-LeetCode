GR = [[0, 1, -1], [1, 0, -1], [1, 1, 1]]


def _calc(S):
    t, j, k, f, g = S['t'], S['j'], S['k'], S['f'], S['grid']
    best = max(f[j + 1][k + 1], f[j + 1][k], f[j][k + 1], f[j][k])
    return best, best + g[t - j][j] + (g[t - k][k] if k != j else 0)


def _ok(S):
    t, j, k, g = S['t'], S['j'], S['k'], S['grid']
    return g[t - j][j] >= 0 and g[t - k][k] >= 0


def _ftab(S):
    f = S.get('f')
    if f is None:
        return None
    if 'k' in S and S.get('_line') == 9:
        f = [row[:] for row in f]
        f[S['j'] + 1][S['k'] + 1] = _calc(S)[1] if _ok(S) else -inf
    return f


def _fc(S, r, c, v):
    if 'k' not in S or S.get('_line') != 9:
        return None
    j, k = S['j'], S['k']
    if (r, c) == (j + 1, k + 1):
        return 'yellow'
    if _ok(S) and (r, c) in ((j + 1, k), (j, k + 1), (j, k), (j + 1, k + 1)):
        return 'blue'
    return None


def _gcell(S, i, j, v):
    if v < 0:
        return 'red'
    return None


def _cond(S, B, r):
    t, j, k, g = S.t, S.j, S.k, S.grid
    a, b = g[t - j][j], g[t - k][k]
    head = f'A 在 `({t-j},{j})` = `{a}`，B 在 `({t-k},{k})` = `{b}`：'
    if a < 0 or b < 0:
        who = 'A' if a < 0 else 'B'
        return head + f'{who} 踩到荆棘 → `f[{j+1}][{k+1}] = -inf`，==这个状态不可达=='
    best, tot = _calc(S)
    return head + f'都能走 → 蓝格（A、B 各 往下/往右 的 4 种来源）取最大 `{best}`，加 `{a}`' + ('，同格只加一次' if k == j else f' + `{b}`') + f' = ==`{tot}`=='


CONFIG = dict(
    num=741, title='摘樱桃', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='往返 = 两人同时走 · f[t][j][k] 滚动数组',
    tags=['灵神题单', '网格图 DP'],
    code='''
class Solution:
    def cherryPickup(self, grid: List[List[int]]) -> int:
        n = len(grid)
        f = [[-inf] * (n + 1) for _ in range(n + 1)]
        f[1][1] = grid[0][0]
        for t in range(1, n * 2 - 1):
            for j in range(min(t, n - 1), max(t - n, -1), -1):
                for k in range(min(t, n - 1), j - 1, -1):
                    if grid[t - j][j] < 0 or grid[t - k][k] < 0:
                        f[j + 1][k + 1] = -inf
                    else:
                        f[j + 1][k + 1] = max(f[j + 1][k + 1], f[j + 1][k], f[j][k + 1], f[j][k]) + \\
                                          grid[t - j][j] + (grid[t - k][k] if k != j else 0)
        return max(f[n][n], 0)
''',
    call=f'Solution().cherryPickup({GR})',
    expect=5,
    skip=['for j in range', 'for k in range', 10, 12, 13],
    views=[
        dict(type='grid', var='grid', label='grid（红 = 荆棘；蓝 = A 在 (t-j, j)，粉 = B 在 (t-k, k)，同一条反对角线）', cell=64, h=250,
             color=_gcell, cursors=[('t - j', 'j', 'blue', ''), ('t - k', 'k', 'pink', '')]),
        dict(type='table', var=_ftab, label='f[j+1][k+1]：A 在第 j 列、B 在第 k 列（黄 = 正在算，蓝 = 4 个来源）', cell=70, h=330,
             rows=['', 'j=0', 'j=1', 'j=2'], cols=['', 'k=0', 'k=1', 'k=2'], color=_fc),
    ],
    watch=[('t', 't'), ('j', 'j', 'blue'), ('k', 'k', 'pink')],
    captions={
        'n = len(grid)': '`n = {n}`',
        'f = [[-inf]': '`f[j+1][k+1]`：两人都走了 `t` 步，A 在 `(t-j, j)`、B 在 `(t-k, k)` 的最多樱桃；`-inf` = 到不了；第 0 行第 0 列是越界哨兵',
        'f[1][1] = grid[0][0]': '`t = 0`：两人都在 `(0,0)`，只摘一次 → `f[1][1] = {f[1][1]}`',
        'for t in range': lambda S, B, r: (f'`t = {S.t}`：两人都走了 `{S.t}` 步，只在 `i + j = {S.t}` 这条对角线上' if S.t != B.get('t') else '所有步数都推完'),
        'if grid[t - j][j] < 0': _cond,
        'return max': '终点 `f[n][n]` 是两人都到 `(n-1,n-1)` 的最大值；若是 `-inf`（路被堵死）就取 `0` → =={ret}==',
    },
    cards=dict(
        one_liner='一去一回 = 两个人同时从起点走到终点，每一步同步',
        complexity='时间 `O(n^3)`，空间 `O(n^2)`',
        problem=['`n × n` 网格：`1` 樱桃，`0` 空，`-1` 荆棘',
                 '从 `(0,0)` 走到 `(n-1,n-1)`，再走回来，摘过的樱桃变成 `0`',
                 '示例：`[[0,1,-1],[1,0,-1],[1,1,1]]` → `5`'],
        quote='所以必须同时考虑两条路径。……把子问题定义成两个人都走了同样的步数，也就是 p=q 的情况，才能直接计算出重复经过的情况，也就是两人走到同一个格子。',
        quote_src='—— 灵茶山艾府题解',
        idea=['跑两次 DP 是错的（有反例）；回程反过来看，就是第二个人也从起点出发',
              '`i + j = t` → 两人走了 `t` 步，`i` 可由 `t` 和 `j` 推出，状态降到 `(t, j, k)`',
              '去掉第一维，倒序枚举 `j`、`k`，跟 0-1 背包一样原地更新'],
        summary=['时间 `O(n^3)`，空间 `O(n^2)`',
                 '`k` 从 `j` 开始：假定 A 在下轮廓、B 在上轮廓，求并集后看不出区别',
                 '易错：荆棘要置回 `-inf`；答案是 `-inf` 时返回 `0`',
                 '灵神还给了记忆化搜索、三维 `f` 递推两种写法，本视频演示最后的空间优化版'],
    ),
)
