ORIG = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]   # 输入的原始值（只用于画面说明）


def _color(S, i, j, v):
    if 'j' not in S:
        return None
    ci, cj = S['i'], S['j']
    if (i, j) == (ci, cj - 1) and ci >= 0:
        return 'pink' if cj > 0 else None        # 左
    if (i, j) == (ci - 1, cj):
        return 'blue'                            # 上
    if (i, j) < (ci, cj):
        return 'green'                           # 已经变成 f 值
    return None


def _formula(S):
    if 'j' not in S:
        return '原地 DP：算完的格子直接存 `f[i][j]`，覆盖 `grid[i][j]`'
    i, j, g = S['i'], S['j'], S['grid']
    x = ORIG[i][j]
    if i == 0 and j == 0:
        return f'情况 1：起点 `f[0][0] = grid[0][0]` = =={x}=='
    if i == 0:
        return f'情况 2：只能从左来 `f[0][{j}] = f[0][{j - 1}] + {x}` = {g[0][j - 1]} + {x} = =={g[0][j - 1] + x}=='
    if j == 0:
        return f'情况 3：只能从上来 `f[{i}][0] = f[{i - 1}][0] + {x}` = {g[i - 1][0]} + {x} = =={g[i - 1][0] + x}=='
    a, b = g[i][j - 1], g[i - 1][j]
    return f'情况 4：`f[{i}][{j}] = min(左 {a}, 上 {b}) + {x}` = =={min(a, b) + x}=='


CONFIG = dict(
    num=64, title='最小路径和', difficulty='Medium', category='多维动态规划',
    author='yiduobo', technique='网格 DP · 分四种情况 · 原地修改',
    code='''
class Solution(object):
    def minPathSum(self, grid):

        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        continue
                    else:
                        grid[i][j] += grid[i][j - 1]
                elif j == 0:
                    grid[i][j] += grid[i - 1][j]
                else:
                    grid[i][j] += min(grid[i][j - 1], grid[i - 1][j])
        return grid[m - 1][n - 1]
''',
    call='Solution().minPathSum([[1,3,1],[1,5,1],[4,2,1]])',
    expect=7,
    skip=['for i in range(m)', 'for j in range(n)', 'n = len(grid[0])'],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='grid', var='grid', label='grid 就是 f 表（绿 = 已是 f 值，灰 = 还是原值；粉 = 左，蓝 = 上）',
             rows=lambda S: ['i=0', 'i=1', 'i=2'], cols=lambda S: ['j=0', 'j=1', 'j=2'],
             cursors=[('i', 'j', 'yellow')], color=_color, cell=110, h=440),
        dict(type='grid', var=lambda S: ORIG, label='原始 grid（对照）', cursors=[('i', 'j', 'yellow')], cell=46, h=190),
    ],
    watch=['i', 'j', ('grid[i][j]', 'grid[i][j]', 'yellow'), 'm', 'n'],
    captions={
        'm = len(grid)': '`f[i][j]` = 走到第 i 行第 j 列的最小路径和；==直接存回 grid==，不开新数组',
        'elif j == 0': lambda S, B, ret: f'`j == 0`？ → {"是，在第一列" if S.j == 0 else "否 → 情况 4"}',
        'if i == 0:': lambda S, B, ret: (f'第 `{S.i}` 行开始。' if S.j == 0 else '') + f'`i == 0`？ → {"是，在第一行" if S.i == 0 else "否"}',
        'if j == 0:': lambda S, B, ret: f'`j == 0`？ → {"是：起点" if S.j == 0 else "否"}',
        'continue': '情况 1：起点 `f[0][0] = grid[0][0]`，本来就对，直接 `continue`',
        'grid[i][j] += grid[i][j - 1]': '情况 2：第一行==只能从左侧走过来==：`{B.grid[i][j]} + {grid[i][j-1]} = {grid[i][j]}`',
        'grid[i][j] += grid[i - 1][j]': '情况 3：第一列==只能从上边走过来==：`{B.grid[i][j]} + {grid[i-1][j]} = {grid[i][j]}`',
        'grid[i][j] += min(': '情况 4：左 `{grid[i][j-1]}`、上 `{grid[i-1][j]}` 取小的，加上原值 `{B.grid[i][j]}` → =={grid[i][j]}==',
        'return grid[m - 1][n - 1]': '右下角存的就是 `f[m-1][n-1]` = =={ret}==',
    },
    cards=dict(
        one_liner='四种情况讨论，直接在 grid 上原地递推',
        complexity='时间 `O(mn)`，额外空间 `O(1)`',
        problem=['`m × n` 网格 `grid` 里都是非负整数，==每次只能向下或向右==走一步',
                 '求从左上角到右下角，路径上数字总和的最小值',
                 '示例：`[[1,3,1],[1,5,1],[4,2,1]]` → `7`'],
        quote='i和j都不为0。此时可以从左侧或者上边走过来，因此有f[i][j] = min(f[i - 1][j], f[i][j - 1]) + grid[i][j]',
        quote_src='—— yiduobo 题解',
        idea=['按 `i`、`j` 是否为 0 分四种情况：起点 / 第一行 / 第一列 / 其他',
              '第一行只能从左来，第一列只能从上来，其余取 ==min(左, 上)==',
              '按行从左到右算：用到的左边、上边一定已经算好',
              '「直接在 grid 上计算来节省空间」：算完的格子覆盖原值，后面不再需要原值'],
        summary=['时间 `O(mn)`，额外空间 `O(1)`（但会修改输入）',
                 '易错：第一行 / 第一列不能用 `min`，否则会越界或取到错误的值',
                 '同一思路也可用滚动数组，不改输入，空间 `O(n)`',
                 '原文为 Python 2 写法，仅删去了 `"""type"""` 文档字符串，代码逻辑未改'],
    ),
)
