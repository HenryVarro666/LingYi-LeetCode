GRID = [[5, 3], [4, 0], [2, 1]]
MC = [[9, 8], [1, 5], [10, 12], [18, 6], [2, 4], [14, 3]]

CONFIG = dict(
    num=2304, title='网格中的最小路径代价', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='逐行 DP · 滚动数组 f/g',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1658'],
    code='''
class Solution(object):
    def minPathCost(self, grid, moveCost):
        f = grid[0][:]
        m = len(grid)
        n = len(grid[0])
        for i in range(1, m):
            g = []
            for j in range(n):
                g.append(None)
                for k in range(n):
                    if g[-1] is None or g[-1] > f[k] + moveCost[grid[i - 1][k]][j] + grid[i][j]:
                        g[-1] = f[k] + moveCost[grid[i - 1][k]][j] + grid[i][j]
            
            f = g[:]
        return min(f)
''',
    call=f'Solution().minPathCost({GRID}, {MC})',
    expect=17,
    skip=['for j in range', 'for k in range', 'g.append', 'm = len', 'n = len'],
    views=[
        dict(type='grid', var='grid', label='grid（黄 = 当前格 (i,j)，蓝 = 上一行枚举的起点 k）', cell=84, h=290,
             cursors=[('i', 'j', 'yellow'), ('i - 1 if _line in (10, 11, 12) else None', 'k', 'blue')]),
        dict(type='array', var='f', label='f（上一行：到 grid[i-1][k] 的最小代价）', cell=90, h=150,
             pointers={'k': 'blue'}),
        dict(type='array', var='g', label='g（当前行：正在算）', cell=90, h=150),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('k', 'k', 'blue')],
    captions={
        'f = grid[0][:]': '第 0 行：`f[j] = grid[0][j]`，还没移动，只有格子的值 → {f}',
        'for i in range': lambda S, B, r: ('所有行都处理完了' if S.i == B.get('i') else f'`i = {S.i}`：用上一行 `f` 算当前行 `g`'),
        'g = []': '`g` 存当前行每格的最小代价',
        'if g[-1] is None or': lambda S, B, r: (
            f'`g[-1] = {S.g[-1]}`，候选：`f[{S.k}] + moveCost[{S.grid[S.i-1][S.k]}][{S.j}] + grid[{S.i}][{S.j}]` = '
            f'`{S.f[S.k]} + {S.moveCost[S.grid[S.i-1][S.k]][S.j]} + {S.grid[S.i][S.j]}` = {S.f[S.k] + S.moveCost[S.grid[S.i-1][S.k]][S.j] + S.grid[S.i][S.j]}'
            + (' → ==更新==（' + ('还没有旧值' if S.g[-1] is None else '比旧值小') + '）' if S.g[-1] is None or S.g[-1] > S.f[S.k] + S.moveCost[S.grid[S.i-1][S.k]][S.j] + S.grid[S.i][S.j] else ' → 不更小，保留')),
        'g[-1] = f[k]': '更新 `g[{j}]` = =={g[-1]}=={}'.replace('{}', ''),
        'f = g[:]': '这一行算完，`g` 变成新的 `f`：滚动数组 → {f}',
        'return min(f)': '最后一行取 `min(f)` = =={ret}==',
    },
    cards=dict(
        one_liner='枚举上一行从哪一列走来，只留一行的滚动数组',
        complexity='时间 `O(mn^2)`，空间 `O(n)`',
        problem=['从第一行任意格出发，每步移到下一行任意格，到最后一行',
                 '代价 = 经过格子的值之和 + `moveCost[上一格的值][目标列]`',
                 '示例：`grid=[[5,3],[4,0],[2,1]]` → `17`'],
        quote='grid[i][j]可以从i - 1层的任何一个位置走过来，因此需要枚举上一层的起点k。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j] = min(f[i-1][k] + moveCost[grid[i-1][k]][j] + grid[i][j])`，`k` 取遍上一行',
              '第 0 行就是 `grid[0]`',
              '每行只依赖上一行，用 `f`、`g` 两个数组滚动'],
        summary=['时间 `O(mn^2)`，空间 `O(n)`',
                 '易错：`moveCost` 的行下标是上一格的==值== `grid[i-1][k]`',
                 '易错：`g[-1]` 初始为 `None`，第一个候选直接赋值',
                 '对比灵神：灵神自底向上、从当前格往下枚举；yiduobo 自顶向下、枚举上一行'],
    ),
)
