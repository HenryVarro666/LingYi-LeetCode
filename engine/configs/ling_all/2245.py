GRID = [[4, 5], [25, 2], [5, 20]]


def _arms(S):
    """(up?, col j, row i) for the current step, or None before the column loops"""
    if 'j' not in S or 'i' not in S or 's2' not in S or 'col' not in S or S.get('_line', 0) < 13:
        return None
    return S['_line'] >= 18, S['j'], S['i']


def _cell(S, i, j, v):
    a = _arms(S)
    if a is None:
        return None
    up, cj, ci = a
    if i == ci and j == cj:
        return 'yellow'
    if j == cj and ((not up and i < ci) or (up and i > ci)):
        return 'blue'
    return None


def _parts(S):
    up, cj, ci = _arms(S)
    s, n = S['s'], len(S['grid'][0])
    s2, s5 = S['s2'], S['s5']
    L2, L5 = s[ci][cj][0], s[ci][cj][1]
    R2, R5 = s[ci][n][0] - s[ci][cj + 1][0], s[ci][n][1] - s[ci][cj + 1][1]
    return s2, s5, L2, L5, R2, R5


def _txt(S):
    a = _arms(S)
    if a is None:
        return '`c2[v]` / `c5[v]`：v 含因子 2 / 5 的个数；尾随零 = `min(因子 2 总数, 因子 5 总数)`'
    up, cj, ci = a
    if S['_line'] in (16, 22):
        s2, s5, L2, L5, R2, R5 = _parts(S)
        return (f'竖直段 `s2={s2}, s5={s5}`　左拐 `min({s2 + L2}, {s5 + L5})` = =={min(s2 + L2, s5 + L5)}=='
                f'　右拐 `min({s2 + R2}, {s5 + R5})` = =={min(s2 + R2, s5 + R5)}==')
    return f'第 {cj} 列，{"从下往上" if up else "从上往下"}：蓝色 = 已走的竖直段，黄色 = 当前拐点'


def _ans_cap(S, B, r):
    s2, s5, L2, L5, R2, R5 = _parts(S)
    a, b = min(s2 + L2, s5 + L5), min(s2 + R2, s5 + R5)
    return (f'拐点 `({S.i},{S.j})`：竖直段 `{s2}` 个 2、`{s5}` 个 5；左拐 =={a}==，右拐 =={b}==，`ans` = =={max(min(B.ans, S.ans), a, b)}==')


CONFIG = dict(
    num=2245, title='转角路径的乘积中最多能有几个尾随零', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='每行前缀和 + 枚举拐点上下方向',
    tags=['灵神题单·常用数据结构', '难度分 2037'],
    setup='''
c2, c5 = [0] * 1001, [0] * 1001
for i in range(2, 1001):  # 预处理：递推算出每个数的因子 2 的个数和因子 5 的个数
    if i % 2 == 0: c2[i] = c2[i // 2] + 1
    if i % 5 == 0: c5[i] = c5[i // 5] + 1
''',
    code='''
class Solution:
    def maxTrailingZeros(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        s = [[None] * (n + 1) for _ in range(m)]
        for i, row in enumerate(grid):
            s[i][0] = (0, 0)
            for j, v in enumerate(row):  # 计算 grid 每行因子 2 和 5 的前缀和
                s[i][j + 1] = (s[i][j][0] + c2[v], s[i][j][1] + c5[v])

        ans = 0
        for j, col in enumerate(zip(*grid)):
            s2 = s5 = 0
            for i, v in enumerate(col):  # 从上往下，枚举左拐还是右拐
                s2 += c2[v]
                s5 += c5[v]
                ans = max(ans, min(s2 + s[i][j][0], s5 + s[i][j][1]),
                               min(s2 + s[i][n][0] - s[i][j + 1][0], s5 + s[i][n][1] - s[i][j + 1][1]))
            s2 = s5 = 0
            for i in range(m - 1, -1, -1):  # 从下往上，枚举左拐还是右拐
                s2 += c2[col[i]]
                s5 += c5[col[i]]
                ans = max(ans, min(s2 + s[i][j][0], s5 + s[i][j][1]),
                               min(s2 + s[i][n][0] - s[i][j + 1][0], s5 + s[i][n][1] - s[i][j + 1][1]))
        return ans
''',
    call=f'Solution().maxTrailingZeros({GRID})',
    expect=4,
    views=[
        dict(type='text', fn=_txt),
        dict(type='grid', var='grid', color=_cell, cursors=[], h=330, cell=96),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('s2', 's2', 'orange'), ('s5', 's5', 'cyan'), ('ans', 'ans', 'green')],
    skip=['m, n = len', 's = [[None]', 's[i][0] = (0, 0)', 'for i, row in enumerate', 'for j, v in enumerate(row)',
          's2 += c2', 's5 += c5', 'min(s2 + s[i][n]'],
    max_steps=90,
    captions={
        's[i][j + 1] =': '行 `{i}` 前 `{j + 1}` 格共 `{s[i][j + 1][0]}` 个 2、`{s[i][j + 1][1]}` 个 5',
        'ans = 0': '每一行的因子前缀和算好了；现在逐列枚举「竖直段」，拐向左或右都用前缀和 `O(1)` 取',
        'for j, col in enumerate': '第 `{j}` 列 `{col}`：把它当作路径的竖直部分',
        'for i, v in enumerate(col)': '从上往下走，每走一格就多一个拐点：`s2`、`s5` 累加这一格的因子',
        'for i in range(m - 1': '再从下往上走一遍，因为竖直段也可能向上延伸',
        16: _ans_cap,
        22: _ans_cap,
        'return ans': '所有拐点里最大的 `min(s2, s5)` 就是答案 `{ans}`',
    },
    cards=dict(
        one_liner='尾零个数 = min(因子 2 总数, 因子 5 总数)；枚举拐点，行用前缀和',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['网格里每格是正整数，转角路径==至多拐一次弯==，横竖各一段',
                 '乘积的尾随零个数最多是多少？',
                 '本视频：`[[4,5],[25,2],[5,20]]` → `4`（`4×25×5×20 = 10000`）'],
        quote='尾零的个数就是路径上的数的因子 2 的个数和，与因子 5 的个数之和的较小值。那么数越多越好，路径的起点和终点都应该在边界上。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数越多越好（没有 0）→ 路径一端必在边界，可以延伸到底',
              '预处理每行因子 2 / 5 的前缀和，横向的一段 `O(1)` 取',
              '竖直段按列逐格累加 `s2`、`s5`，上下两个方向各扫一遍，每格再试左拐 / 右拐'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '`c2`、`c5` 是类外预处理（视频里在 setup 里提前算好）',
                 '拐点那一格只能算一次：竖直段已含它，所以左段是 `s[i][j]`，右段是 `s[i][n] − s[i][j+1]`',
                 '只扫列、用行前缀和；也可以反过来，思路对称'],
    ),
)
