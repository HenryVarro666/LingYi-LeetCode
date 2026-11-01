G = [[1, 1, 1, 0], [1, 1, 1, 1], [0, 1, 1, 1]]


def _pass(S):
    return '第 1 遍：求正金字塔' if S.get('grid') == G else '第 2 遍：grid 已颠倒，求出的是倒金字塔'


def _fml(S):
    if S.get('_line') in (17, 18) and 'j' in S and S.get('i') is not None and S['i'] + 1 < len(S['dp']):
        i, j, dp = S['i'], S['j'], S['dp']
        a, b, c = dp[i + 1][j - 1], dp[i + 1][j], dp[i + 1][j + 1]
        return f'`dp[{i}][{j}] = min({a}, {c}, {b}) + 1` = =={min(a, b, c) + 1}==，新增金字塔 `{min(a, b, c)}` 个'
    return f"{_pass(S)}；目前 `ans = {S.get('ans', 0)}`"


def _dpc(S, i, j, v):
    ci, cj = S.get('i'), S.get('j')
    if S.get('_line') in (17, 18) and ci is not None and cj is not None and ci + 1 < len(S['dp']):
        if (i, j) == (ci, cj):
            return 'yellow'
        if i == ci + 1 and abs(j - cj) <= 1:
            return 'blue'
    return None


CONFIG = dict(
    num=2088, title='统计农场中肥沃金字塔的数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='自底向上 DP：套「∧ 型外壳」（Go 原文转写）',
    tags=['灵神题单·动态规划', '难度分 2105'],
    code='''
class Solution:
    def countPyramids(self, grid: List[List[int]]) -> int:
        ans = 0
        m, n = len(grid), len(grid[0])
        dp = [[0] * n for _ in range(m)]

        def f() -> None:
            nonlocal ans
            dp[m - 1] = grid[m - 1]
            for i in range(m - 2, -1, -1):
                dp[i][0] = grid[i][0]
                dp[i][n - 1] = grid[i][n - 1]
                for j in range(1, n - 1):
                    if grid[i][j] == 0:
                        dp[i][j] = 0
                    else:
                        dp[i][j] = min(dp[i + 1][j - 1], dp[i + 1][j + 1], dp[i + 1][j]) + 1
                        ans += dp[i][j] - 1

        f()  # 求正金字塔个数
        for i in range(m // 2):  # 上下颠倒
            grid[i], grid[m - 1 - i] = grid[m - 1 - i], grid[i]
        f()  # 再求一遍正金字塔个数
        return ans
''',
    call=f'Solution().countPyramids({G})',
    expect=6,
    skip=['ans = 0', 'm, n = len', 'dp = [[0]', 'nonlocal', 'for j in range', 'dp[i][n - 1] = grid'],
    max_steps=100,
    views=[
        dict(type='grid', var='grid', label='grid（0 = 贫瘠，1 = 肥沃）', cell=84, h=250,
             cursors=[('i', 'j', 'yellow')]),
        dict(type='table', var='dp', label='dp[i][j]：顶端在 (i,j) 的金字塔最大层数（黄 = 正在算，蓝 = 依赖的三格）', cell=84, h=250,
             color=_dpc),
        dict(type='text', fn=_fml, size=26, h=90),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'dp[m - 1] = grid[m - 1]': lambda S, B, r: f'{_pass(S)[:5]}：最后一行只有 1 层，`dp[m-1] = grid[m-1]`；从倒数第二行往上推',
        'for i in range(m - 2': lambda S, B, r: ('这一遍的所有行都算完了' if B.get('i') == S.get('i') else f'`i = {S.i}`：当前行，依赖下一行 `dp[{S.i + 1}]`'),
        'dp[i][0] = grid[i][0]': '最左一格没有左下角，最多 1 层：`dp[{i}][0] = grid[{i}][0]` = {dp[i][0]}（右端同理）',
        'if grid[i][j] == 0': lambda S, B, r: (f'`grid[{S.i}][{S.j}] = 0`：贫瘠，不可能是顶端' if S.grid[S.i][S.j] == 0
                                              else f'`grid[{S.i}][{S.j}] = 1`：肥沃，可以做顶端'),
        'dp[i][j] = 0': '贫瘠格：`dp[{i}][{j}] = 0`',
        'dp[i][j] = min(': '在下方金字塔上套外壳：取 `min({dp[i+1][j-1]}, {dp[i+1][j+1]}, {dp[i+1][j]}) + 1` = =={dp[i][j]}==',
        'ans += ': '最大 {dp[i][j]} 层，去掉 1 层的情况，顶端在这里的金字塔有 `{dp[i][j]} - 1` 个 → `ans` = =={ans}==',
        'f()  # 求正': '先求正金字塔个数',
        'for i in range(m // 2)': lambda S, B, r: ('倒金字塔 = 上下颠倒后的正金字塔，所以把 grid 上下翻转' if S.grid == G else '翻转完成'),
        'grid[i], grid[m - 1 - i]': '交换第 `{i}` 行和第 `{m - 1 - i}` 行',
        'f()  # 再求': '再求一遍，累加到同一个 `ans`',
        'return ans': '正、倒金字塔总数 = =={ret}==',
    },
    cards=dict(
        one_liner='dp 记录最大层数，倒金字塔就把 grid 上下颠倒再算一遍',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['农场是 `m × n` 的 0/1 网格，1 表示肥沃',
                 '金字塔：顶端在上，第 `k` 行宽 `2k-1`，全是肥沃的，且格子数大于 1',
                 '倒金字塔：顶端在下，形状上下颠倒',
                 '示例：`[[1,1,1,0],[1,1,1,1],[0,1,1,1]]` → `6`'],
        quote='转移的策略是在 (i+1,j) 处的最大金字塔上套一层 ∧ 型的「外壳」。……那么 (i,j) 处的最大金字塔的高度为「外壳」的高度与 (i+1,j) 处最大金字塔高度 +1 的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dp[i][j]` = 顶端在 `(i,j)` 的金字塔最大层数（1 层也算）',
              '`dp[i][j] = min(左下, 正下, 右下) + 1`，从最后一行往上推',
              '最大 `x` 层，就有 `x-1` 个金字塔（去掉 1 层的）',
              '倒金字塔：`grid` 上下颠倒，再求一遍正金字塔'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（闭包 `f` 用 `nonlocal ans`）',
                 '时间、空间都是 `O(mn)`',
                 '易错：最左、最右一列没有左下/右下，层数只能是 1，不累加答案',
                 '易错：不要漏掉 `- 1`，单个格子不算金字塔',
                 '相似题目：CF1393D Rarity and New Dress'],
    ),
)
