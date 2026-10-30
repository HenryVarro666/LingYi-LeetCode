def _cell(S, i, j, v):
    ci, cj = S.get('i'), S.get('j')
    if ci is None or cj is None:
        return None
    if i == ci and j == cj:
        return 'yellow'
    if i == ci:
        return 'blue'
    if j == cj:
        return 'pink'
    return None


def _formula(S):
    if S['_line'] < 19 or 'res' not in S or 'max_row' not in S:
        return ''
    i, j = S['i'], S['j']
    r, c, g = S['max_row'][i], S['max_col'][j], S['grid'][i][j]
    return f"`min(max_row[{i}]={r}, max_col[{j}]={c}) − grid[{i}][{j}]={g}` = =={min(r, c) - g}=="


CONFIG = dict(
    num=807, title='保持城市天际线', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='先求行列最大值 · 再逐格累加',
    code='''
class Solution:
    def maxIncreaseKeepingSkyline(self, grid):

        m = len(grid)
        n = len(grid[0])
        max_row = [0] * m
        max_col = [0] * n
        for i in range(m):
            for j in range(n):
                if grid[i][j] > max_row[i]:
                    max_row[i] = grid[i][j]
                if grid[i][j] > max_col[j]:
                    max_col[j] = grid[i][j]
        

        res = 0
        for i in range(m):
            for j in range(n):
                res += min(max_row[i], max_col[j]) - grid[i][j]
        
        return res
''',
    call='Solution().maxIncreaseKeepingSkyline([[3,0,8],[2,4,5],[9,2,6]])',
    expect=16,
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 第 i 行，粉 = 第 j 列，黄 = 当前楼；左侧=行最大，上方=列最大）', cell=90, h=300, cursors=[], color=_cell,
             rows=lambda S: [f"{m}" for m in S['max_row']] if 'max_row' in S else None,
             cols=lambda S: [f"{m}" for m in S['max_col']] if 'max_col' in S else None),
        dict(type='text', h=70, size=28, fn=_formula),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('max_row', 'max_row', 'blue'), ('max_col', 'max_col', 'pink'), ('res', 'res', 'green')],
    skip=['m = len', 'n = len'],
    captions={
        'max_row = [0]': '`max_row[i]`：第 `i` 行的最大值，先都记 0',
        'max_col = [0]': '`max_col[j]`：第 `j` 列的最大值，先都记 0',
        'if grid[i][j] > max_row[i]': lambda S, B, r: (f"`grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]}` > `max_row[{S.i}] = {S.max_row[S.i]}` → 更大，更新行最大值" if S.grid[S.i][S.j] > S.max_row[S.i]
                                                      else f"`grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]}` 没超过 `max_row[{S.i}] = {S.max_row[S.i]}`，不更新"),
        'max_row[i] = grid[i][j]': '`max_row[{i}]` → =={max_row[i]}==',
        'if grid[i][j] > max_col[j]': lambda S, B, r: (f"`grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]}` > `max_col[{S.j}] = {S.max_col[S.j]}` → 更大，更新列最大值" if S.grid[S.i][S.j] > S.max_col[S.j]
                                                      else f"`grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]}` 没超过 `max_col[{S.j}] = {S.max_col[S.j]}`，不更新"),
        'max_col[j] = grid[i][j]': '`max_col[{j}]` → =={max_col[j]}==',
        'res = 0': '行列最大值都求好了：`max_row = {max_row}`，`max_col = {max_col}`；开始累加增量',
        'res += ': '`({i}, {j})` 至多加到 `min({max_row[i]}, {max_col[j]}) = {min(max_row[i], max_col[j])}`，增加 `{min(max_row[i], max_col[j])} − {grid[i][j]}` = =={min(max_row[i], max_col[j]) - grid[i][j]}==，`res = {res}`',
        'return res': '所有建筑可增加的高度总和 `{res}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='天际线 = 每行、每列的最大值；楼最多加到两者中较小的',
        complexity='时间 `O(mn)`，空间 `O(m+n)`',
        problem=['`grid[x][y]` 是街区上楼的高度，可以加高，但东南西北四个方向的==天际线不能变==',
                 '求所有楼能增加的高度总和的最大值',
                 '本视频：`[[3,0,8],[2,4,5],[9,2,6]]` → `16`'],
        quote='观察样例可以发现，所谓的天际线对于横向来说，就是每一行中的最大值，而对于竖向则是每一列中的最大值。',
        quote_src='—— yiduobo 题解原文',
        idea=['先扫一遍矩阵，求每行最大值 `max_row`、每列最大值 `max_col`',
              '位于 `(x, y)` 的楼，加高后不超过所在行和列的最大值都合法',
              '所以可增加 `min(max_row[x], max_col[y]) - grid[x][y]`，全部累加'],
        summary=['时间 `O(mn)`，空间 `O(m+n)`',
                 '先求行列最大，再第二轮累加，共扫描矩阵两遍',
                 '易错：增量要减去原高度；最大值数组别用 `-1`，题目高度可以是 0',
                 '原文为 Python 2 风格（`class Solution(object)`），这里只改成 `class Solution`'],
    ),
)
