def _fv(S):
    return S['f'] if 'f' in S else None


def _gv(S):
    return S['g'] if 'g' in S else None


CONFIG = dict(
    num=2373, title='矩阵中的局部最大值', difficulty='Easy', category='网格图',
    author='yiduobo', technique='两步 2×2 取最大',
    tags=[],
    code='''
class Solution(object):
    def largestLocal(self, grid):

        n = len(grid)
        f = [[0] * (n - 1) for _ in range(n - 1)]
        for i in range(n - 1):
            for j in range(n - 1):
                f[i][j] = max(grid[i][j], grid[i + 1][j], grid[i][j + 1], grid[i + 1][j + 1])
        
        g = [[0] * (n - 2) for _ in range(n - 2)]
        for i in range(n - 2):
            for j in range(n - 2):
                g[i][j] = max(f[i][j], f[i + 1][j], f[i][j + 1], f[i + 1][j + 1])
        
        return g
''',
    call='Solution().largestLocal([[9,9,8,1],[5,6,2,6],[8,2,6,4],[6,2,2,2]])',
    expect=[[9, 9], [8, 6]],
    views=[
        dict(type='grid', var='grid', label='grid', cell=70, h=300,
             color=lambda S, i, j, v: 'blue' if 'i' in S and 'f' in S and 'g' not in S and S['i'] <= i <= S['i'] + 1 and S['j'] <= j <= S['j'] + 1 else None),
        dict(type='grid', var=_fv, label='f：每个 2×2 的最大值', cell=70, h=260,
             color=lambda S, i, j, v: 'blue' if 'g' in S and 'i' in S and S['i'] <= i <= S['i'] + 1 and S['j'] <= j <= S['j'] + 1 else None,
             cursors=[('i if "g" not in S else None', 'j', 'yellow')]),
        dict(type='grid', var=_gv, label='g：每个 3×3 的最大值（答案）', cell=70, h=200,
             cursors=[('i', 'j', 'yellow')]),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'n'],
    captions={
        'n = len': '`n = {n}`，数据规模小，可以直接枚举',
        'f = [[0]': '`f[i][j]`：以 `(i,j)` 为左上角的 ==2×2== 最大值，先全填 0',
        'f[i][j] = max': '`f[{i}][{j}]` = 四个格子的最大值 = =={f[i][j]}==',
        'g = [[0]': '`g[i][j]`：以 `(i,j)` 为左上角的 ==3×3== 最大值',
        'g[i][j] = max': '3×3 = 四个相邻 2×2 的并集：`g[{i}][{j}]` = =={g[i][j]}==',
        'return g': '`g` 就是答案',
    },
    cards=dict(
        one_liner='3×3 的最大值 = 四个 2×2 最大值的最大值，分两步算',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['`n × n` 矩阵 `grid`，求每个 3×3 子矩阵的最大值',
                 '结果是 `(n-2) × (n-2)` 的矩阵',
                 '示例：`[[9,9,8,1],[5,6,2,6],[8,2,6,4],[6,2,2,2]]` → `[[9,9],[8,6]]`'],
        quote='首先令f[i][j]表示以(i, j)为左上角的2*2矩阵中的最大值，……接下来再令g[i][j]表示以(i, j)为左上角的3*3矩阵中的最大值。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j] = max(grid[i][j], grid[i][j+1], grid[i+1][j], grid[i+1][j+1])`',
              '`g[i][j] = max(f[i][j], f[i][j+1], f[i+1][j], f[i+1][j+1])`',
              '`g` 就是题目要的结果'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`',
                 '易错：`f` 的大小是 `n-1`，`g` 的大小是 `n-2`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
