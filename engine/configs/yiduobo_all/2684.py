G = [[2, 4, 3, 5], [5, 4, 9, 3], [3, 4, 2, 11]]


def _lst(S, k):
    try:
        return list(S[k])
    except Exception:
        return []


def _col(S, i, j, v):
    if 'j' not in S or 'f' not in S:
        return None
    jj = S['j']
    if j == jj + 1 and S.get('g') is not None and S['g'][i] >= 0:
        return None
    if j == jj + 1:
        return 'blue'
    return None


def _cell(S, i, j, v):
    if 'j' not in S:
        return None
    if j == S['j']:
        return 'yellow'
    if j == S['j'] + 1:
        return 'blue'
    return None


CONFIG = dict(
    num=2684, title='矩阵中移动的最大次数', difficulty='Medium', category='网格图',
    author='yiduobo', technique='按列倒推的动态规划（滚动数组）',
    tags=['灵神核心路线', '灵神题单·网格图', '难度分 1626'],
    code='''
class Solution(object):
    def maxMoves(self, grid):

        m = len(grid)
        n = len(grid[0])

        f = [0] * m
        for j in range(n - 2, -1, -1):
            g = f[:]
            f = [0] * m
            for i in range(m):
                if i > 0 and grid[i][j] < grid[i - 1][j + 1]:
                    f[i] = max(f[i], g[i - 1] + 1)
                if grid[i][j] < grid[i][j + 1]:
                    f[i] = max(f[i], g[i] + 1)
                if i < m - 1 and grid[i][j] < grid[i + 1][j + 1]:
                    f[i] = max(f[i], g[i + 1] + 1)
            

        return max(f)
''',
    call=f'Solution().maxMoves({G})',
    expect=3,
    skip=['m = len', 'n = len', 'for i in range(m)'],
    max_steps=80,
    views=[
        dict(type='grid', var='grid', label='grid（黄 = 当前列 j，蓝 = 右边一列 j+1）', cell=96, h=300,
             color=_cell, cursors=[('i', 'j', 'pink', '(i,j)')]),
        dict(type='array', var=lambda S: _lst(S, 'g') if 'g' in S else None,
             label='g = 右边一列的 f（从 (i, j+1) 出发还能走几步）', cell=70, h=130),
        dict(type='array', var='f', label='f = 当前列的 f（从 (i, j) 出发最多还能走几步）', cell=70, h=130,
             color=lambda S, i, v: 'green' if 'i' in S and i == S['i'] and v > 0 else None,
             pointers={'i': 'pink'}),
    ],
    watch=[('j', 'j', 'blue'), ('i', 'i', 'pink'), ('f', 'f', 'green')],
    captions={
        'f = [0] * m': lambda S, B, r: ('`f[i]` = 从第 `i` 行当前列出发最多还能走几步；最右一列走不动，全是 0' if 'j' not in S else '`f` 清零：下面重新算当前列的值'),
        'for j in range(n - 2': lambda S, B, r: (f'从右往左倒推，现在算第 `{S.j}` 列：它的下一步只会落在第 `{S.j+1}` 列' if S.get('j') != B.get('j')
                                                  else '第 0 列也算完了，倒推结束'),
        'g = f[:]': '把右边一列的 `f` 备份成 `g`，`f` 重新清零来装当前列的值',
        'for i in range(m)': '逐行算当前列 `({i},{j})` 的 `f[{i}]`',
        'if i > 0 and': lambda S, B, r: ('`i = 0` 在最上一行，没有右上格' if S.i == 0 else
                                         (f'右上 `grid[{S.i-1}][{S.j+1}] = {S.grid[S.i-1][S.j+1]}` 大于当前 `{S.grid[S.i][S.j]}` → 能走'
                                          if S.grid[S.i][S.j] < S.grid[S.i-1][S.j+1]
                                          else f'右上 `{S.grid[S.i-1][S.j+1]}` 不大于当前 `{S.grid[S.i][S.j]}` → 不能走')),
        'f[i] = max(f[i], g[i - 1] + 1)': '走右上：右上格还能走 `{g[i-1]}` 步，再加这一步 → `f[{i}] = {f[i]}`',
        'if grid[i][j] < grid[i][j + 1]': lambda S, B, r: (f'正右 `{S.grid[S.i][S.j+1]}` 大于当前 `{S.grid[S.i][S.j]}` → 能走'
                                                           if S.grid[S.i][S.j] < S.grid[S.i][S.j+1]
                                                           else f'正右 `{S.grid[S.i][S.j+1]}` 不大于当前 `{S.grid[S.i][S.j]}` → 不能走'),
        'f[i] = max(f[i], g[i] + 1)': '走正右：正右格还能走 `{g[i]}` 步，再加这一步 → `f[{i}] = {f[i]}`',
        'if i < m - 1 and': lambda S, B, r: (f'`i = {S.i}` 在最下一行，没有右下格' if S.i == S.m - 1 else
                                             (f'右下 `{S.grid[S.i+1][S.j+1]}` 大于当前 `{S.grid[S.i][S.j]}` → 能走'
                                              if S.grid[S.i][S.j] < S.grid[S.i+1][S.j+1]
                                              else f'右下 `{S.grid[S.i+1][S.j+1]}` 不大于当前 `{S.grid[S.i][S.j]}` → 不能走')),
        'f[i] = max(f[i], g[i + 1] + 1)': '走右下：右下格还能走 `{g[i+1]}` 步，再加这一步 → `f[{i}] = {f[i]}`',
        'return max(f)': '第 0 列的 `f` 是 `{f}`，起点任选 → 取最大值 =={max(f)}==',
    },
    cards=dict(
        one_liner='f[i][j] = 从该格出发还能走几步，从右往左一列列推',
        complexity='时间 `O(mn)`，空间 `O(m)`',
        problem=['`m × n` 正整数矩阵，从第 0 列任意格出发',
                 '每步走到右上 / 右 / 右下，且==值严格更大==',
                 '求最多能移动几次',
                 '示例：`[[2,4,3,5],[5,4,9,3],[3,4,2,11]]` → `3`'],
        quote='令f[i][j]表示从第i行第j列这个单元格出发可移动的最大移动次数，那么可以初始化所有的f[i][n - 1]为0，也就是位于最右侧这一列的所有位置都已经无法移动了。',
        quote_src='—— yiduobo 题解原文',
        idea=['最右一列走不动：`f = 0`',
              '从右往左，每格看右上 / 正右 / 右下三个邻居',
              '邻居更大就能走：`f[i] = max(f[i], 邻居的 f + 1)`',
              '`f` 只依赖右边一列，滚动数组省掉 `j` 这一维'],
        summary=['时间 `O(mn)`，空间 `O(m)`（滚动数组）',
                 '易错：必须从右往左算，且三个方向都要“严格大于”才转移',
                 '`g = f[:]` 要先备份，再把 `f` 清零，否则会读到被改过的值',
                 '答案是第 0 列 `f` 的最大值，不是某个固定起点',
                 '原文已是 Python 3 可运行写法，代码未改'],
    ),
)
