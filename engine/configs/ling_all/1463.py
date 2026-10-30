G = [[3, 1, 1], [2, 5, 1], [1, 5, 5], [2, 1, 1]]


def _pre_color(S, r, c, v):
    if 'k' not in S or S.get('_inner', S).get('k') is None:
        return None
    j, k = S['j'], S['k']
    if j <= r <= j + 2 and k <= c <= k + 2:
        return 'blue'
    return None


def _cur_color(S, r, c, v):
    if 'k' not in S:
        return None
    if (r, c) == (S['j'] + 1, S['k'] + 1):
        return 'yellow'
    return None


def _calc(S):
    i, j, k = S['i'], S['j'], S['k']
    pre = S['pre']
    best = max(pre[a][b] for a in (j, j + 1, j + 2) for b in (k, k + 1, k + 2))
    return best, best + S['grid'][i][j] + S['grid'][i][k]


def _cur(S):
    cur = S.get('cur')
    if cur is None:
        return None
    if 'k' in S and S['_line'] == 13:
        cur = [row[:] for row in cur]
        cur[S['j'] + 1][S['k'] + 1] = _calc(S)[1]
    return cur


def _f(S):
    if 'k' not in S or S['_line'] != 13:
        return 'A 从 `(i,j)`、B 从 `(i,k)` 出发，到最后一行：`cur[j+1][k+1]` 里存的就是这个最大值（下标整体 +1 留出越界位）'
    i, j, k = S['i'], S['j'], S['k']
    best, tot = _calc(S)
    return f"`cur[{j+1}][{k+1}]` = 下一行 3×3 里最大 `{best}` + `{S['grid'][i][j]}` + `{S['grid'][i][k]}` = =={tot}=="


CONFIG = dict(
    num=1463, title='摘樱桃 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='两个机器人同步走 · 三维 DP 滚动数组',
    tags=['灵神题单', '网格图 DP'],
    code='''
class Solution:
    def cherryPickup(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        pre = [[0] * (n + 2) for _ in range(n + 2)]
        cur = [[0] * (n + 2) for _ in range(n + 2)]
        for i in range(m - 1, -1, -1):
            for j in range(min(n, i + 1)):
                for k in range(max(j + 1, n - 1 - i), n):
                    cur[j + 1][k + 1] = max(
                        pre[j][k], pre[j][k + 1], pre[j][k + 2],
                        pre[j + 1][k], pre[j + 1][k + 1], pre[j + 1][k + 2],
                        pre[j + 2][k], pre[j + 2][k + 1], pre[j + 2][k + 2],
                    ) + grid[i][j] + grid[i][k]
            pre, cur = cur, pre  # 下一个 i 的 pre 是 cur
        return pre[1][n]
''',
    call=f'Solution().cherryPickup({G})',
    expect=24,
    skip=['for j in range', 'for k in range', 9, 10, 11, 12],
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 机器人 A 在 (i,j)，粉 = 机器人 B 在 (i,k)）', cell=48, h=190,
             cursors=[('i', 'j', 'blue'), ('i', 'k', 'pink')]),
        dict(type='table', var=lambda S: S.get('pre'), label='pre = f[i+1]（蓝 = 要取最大的 3×3）', cell=60, h=225, color=_pre_color),
        dict(type='table', var=_cur, label='cur = f[i]（黄 = 正在算）', cell=60, h=225, color=_cur_color),
    ],
    watch=[('i', 'i'), ('j', 'j', 'blue'), ('k', 'k', 'pink')],
    captions={
        'm, n = len(grid)': '`m = {m}` 行，`n = {n}` 列',
        'pre = [[0]': '`pre` = 下一行的状态，初值 0；多开一圈，==越界直接读到 0==，不用判断边界',
        'cur = [[0]': '`cur` = 当前行的状态',
        'for i in range': lambda S, B, r: (f'从最后一行往上算：`i = {S.i}`，只依赖下一行 `pre`' if S.i != B.get('i') else '第 0 行也算完，答案在 `pre[1][n]`'),
        ') + grid[i][j]': lambda S, B, r: f'A 在 `({S.i},{S.j})`、B 在 `({S.i},{S.k})`：下一步各 3 种共 9 种，取蓝色 3×3 的最大，再加两格 → `cur[{S.j+1}][{S.k+1}]` = `{_calc(S)[0]} + {S.grid[S.i][S.j]} + {S.grid[S.i][S.k]}` = =={_calc(S)[1]}==',
        'pre, cur = cur, pre': '这一行算完：`cur` 变成上一行的 `pre`，两个数组交换复用',
        'return pre[1][n]': 'A 从 `(0,0)`、B 从 `(0,n-1)` 出发：`pre[1][{n}]` = =={ret}==',
    },
    cards=dict(
        one_liner='两个机器人同时下一行，状态只看 (行, A 的列, B 的列)',
        complexity='时间 `O(mn^2)`，空间 `O(n^2)`',
        problem=['`grid` 每格是樱桃数，机器人 1 从 `(0,0)`、机器人 2 从 `(0,cols-1)` 出发',
                 '每步下移一行，列可 `-1/0/+1`；同格只能被摘一次',
                 '示例：`[[3,1,1],[2,5,1],[1,5,5],[2,1,1]]` → `24`'],
        quote='A 走的是两条路径的左轮廓，B 走的是两条路径的右轮廓（求并集后看不出区别），所以只需计算 k≥j 的状态。……A 和 B 走到同一个格子是没有意义的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i,j,k)`：A 在 `(i,j)`、B 在 `(i,k)` 到最后一行的最大值，每人 3 种走法共 9 种',
              '1:1 翻译成递推，下标整体 `+1` 当作越界哨兵，值为 0',
              '只依赖下一行，再用 `pre`、`cur` 两个二维数组滚动'],
        summary=['时间 `O(mn^2)`，空间 `O(n^2)`',
                 '`k` 从 `max(j+1, n-1-i)` 开始：保证 A 在左、B 在右，且是能到的位置',
                 '易错：循环结束要交换 `pre, cur`；这里值非负，越界读到 0 不影响',
                 '灵神还给了记忆化搜索和三维 `f` 数组写法，本视频演示最后的滚动数组'],
    ),
)
