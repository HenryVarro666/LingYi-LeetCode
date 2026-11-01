G = [[1, 3, 1, 15], [1, 3, 3, 1]]


def _ks(S):
    """(row0 里还没被取走的起点, row1 里已累计的列数)"""
    g = S['grid']
    if 'left1' not in S or 'j' not in S:
        return None
    a = 0
    s = sum(g[0])
    while a < len(g[0]) and s != S['left0']:
        s -= g[0][a]
        a += 1
    b, t = 0, 0
    while b < len(g[1]) and t != S['left1']:
        t += g[1][b]
        b += 1
    return a, b


def _col(S, i, j, v):
    k = _ks(S)
    if k is None:
        return None
    a, b = k
    if i == 0 and j >= a:
        return 'blue'
    if i == 1 and j < b:
        return 'pink'
    return None


def _txt(S):
    if 'left1' not in S or 'j' not in S:
        return '先算第一行的总和 `left0`；`left0` = 第一行拐弯点右边的点数'
    return f"第二个机器人只能取 `left0 = {S['left0']}`（上行后缀）或 `left1 = {S['left1']}`（下行前缀）的较大者 = =={max(S['left0'], S['left1'])}=="


CONFIG = dict(
    num=2017, title='网格游戏', difficulty='Medium', category='前缀和与差分',
    author='灵茶山艾府', technique='枚举拐弯位置 · 前后缀和（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def gridGame(self, grid: List[List[int]]) -> int:
        ans = inf
        left0 = 0
        for v in grid[0]:
            left0 += v
        left1 = 0
        for j, v in enumerate(grid[0]):  # 枚举第一个机器人在哪拐弯
            left0 -= v
            ans = min(ans, max(left0, left1))  # 第二个机器人只能取上下剩余部分中的最大值
            left1 += grid[1][j]
        return ans
''',
    call=f'Solution().gridGame({G})',
    expect=7,
    skip=['for v in grid[0]', 'left0 += v', 'ans = inf', 'left0 = 0', 'left1 = 0'],
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 上行剩余后缀 left0，粉 = 下行已有前缀 left1，黄框 = 拐弯列 j）', cell=110, h=300,
             color=_col, cursors=[(0, 'j', 'yellow'), (1, 'j', 'yellow')]),
        dict(type='text', fn=_txt, size=26, h=70),
    ],
    watch=[('j', 'j', 'yellow'), ('left0', 'left0', 'blue'), ('left1', 'left1', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'for j, v in enumerate': lambda S, B, r: ('每一列都试过了，循环结束' if 'j' in B and S.j == B.j
                                                  else f'枚举拐弯列 `j = {S.j}`：第一个机器人在第 0 行走到 `j`，再下到第 1 行'),
        'left0 -= v': '第一个机器人拿走了 `grid[0][{j}] = {v}`，上行剩余后缀 `left0` = =={left0}==',
        'ans = min(': '第二个机器人在上行后缀 `{left0}` 和下行前缀 `{left1}` 里只能选一条 → 取较大的 `{max(left0, left1)}`；第一个机器人要它最小：`ans` = =={ans}==',
        'left1 += grid[1][j]': '下行的 `grid[1][{j}] = {grid[1][j]}` 并入前缀：`left1` = =={left1}==',
        'return ans': '拐弯点全试完，第二个机器人最少能拿 =={ans}==',
    },
    cards=dict(
        one_liner='只有两行：枚举第一个机器人拐弯的位置，剩下只有两块',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`2 x n` 的网格，两个机器人先后从左上走到右下，只能向右或向下',
                 '第一个走过的格子清零；==第一个想让第二个得分最小，第二个想最大==',
                 '示例：`[[1,3,1,15],[1,3,3,1]]` → `7`'],
        quote='由于矩阵只有两行，我们可以枚举第一个机器人的拐弯位置，于是剩余的点数被划分成了两部分，即第一行的后缀和第二行的前缀，另一个机器人只能在这两部分中取最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['拐弯列 `j`：上行 `j` 右边剩 `left0`，下行 `j` 左边剩 `left1`',
              '第二个机器人只能走其中一块，当然取大的：`max(left0, left1)`',
              '第一个机器人从所有 `j` 里选最小的那个 → `ans`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Go，已按原逻辑逐行转写为 Python（`math.MaxInt` → `inf`，`range` → `enumerate`）',
                 '先 `left0 -= v` 再取 max；`left1` 要等取完 max 之后才加上当前列',
                 '最后一列：`left0 = 0`，答案可能就是整行下行前缀'],
    ),
)
