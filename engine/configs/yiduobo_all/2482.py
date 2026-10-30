G = [[0, 1, 1], [1, 0, 1], [0, 0, 1]]

CONFIG = dict(
    num=2482, title='行和列中一和零的差值', difficulty='Medium', category='模拟',
    author='yiduobo', technique='模拟 · 四个计数数组',
    tags=[],
    code='''
class Solution(object):
    def onesMinusZeros(self, grid):

        m = len(grid)
        n = len(grid[0])

        ones_row = [0] * m
        ones_col = [0] * n
        zeros_row = [0] * m
        zeros_col = [0] * n
        
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 0:
                    zeros_row[i] += 1
                    zeros_col[j] += 1
                else:
                    ones_row[i] += 1
                    ones_col[j] += 1
        
        res = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                res[i][j] = ones_row[i] + ones_col[j] - zeros_row[i] - zeros_col[j]
        
        return res
''',
    call=f'Solution().onesMinusZeros({G!r})',
    expect=[[0, 0, 4], [0, 0, 4], [-2, -2, 2]],
    views=[
        dict(type='grid', var='grid', label='grid', cursors=[('i', 'j', 'yellow', '(i,j)')], h=260, cell=80,
             color=lambda S, i, j, v: 'green' if v == 1 else None),
        dict(type='grid', var='res', label='res（差值矩阵）', cursors=[('i', 'j', 'yellow', '(i,j)')], h=260, cell=80),
        dict(type='text', h=110, size=26,
             fn=lambda S: (f"行 `{S['i']}`：一 {S['ones_row'][S['i']]} 零 {S['zeros_row'][S['i']]}；列 `{S['j']}`：一 {S['ones_col'][S['j']]} 零 {S['zeros_col'][S['j']]}"
                           if 'ones_row' in S and 'i' in S and 'j' in S else '')),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ones_row', 'ones_row', 'green'), ('zeros_row', 'zeros_row', 'orange'),
           ('ones_col', 'ones_col', 'green'), ('zeros_col', 'zeros_col', 'orange')],
    captions={
        'ones_row = [0]': '`ones_row[i]`：第 `i` 行一的个数，共 `{m}` 行',
        'ones_col = [0]': '`ones_col[j]`：第 `j` 列一的个数，共 `{n}` 列',
        'zeros_row = [0]': '`zeros_row[i]`：第 `i` 行零的个数',
        'zeros_col = [0]': '`zeros_col[j]`：第 `j` 列零的个数',
        'if grid[i][j] == 0': '`grid[{i}][{j}] = {grid[i][j]}` → {"是 0，记到零的行列计数" if grid[i][j] == 0 else "是 1，记到一的行列计数"}',
        'zeros_row[i] += 1': '第 `{i}` 行零数 → {zeros_row[i]}',
        'zeros_col[j] += 1': '第 `{j}` 列零数 → {zeros_col[j]}',
        'ones_row[i] += 1': '第 `{i}` 行一数 → {ones_row[i]}',
        'ones_col[j] += 1': '第 `{j}` 列一数 → {ones_col[j]}',
        'res = [[0]': '新建与 `grid` 同样大小的 `res`，下面按题目公式逐格填',
        'res[i][j] =': '`res[{i}][{j}] = {ones_row[i]} + {ones_col[j]} − {zeros_row[i]} − {zeros_col[j]}` = =={res[i][j]}==',
        'return res': '差值矩阵构造完成：`{res}`',
    },
    max_steps=100,
    cards=dict(
        one_liner='按题目的定义老老实实构造：四个数组 + 一个答案矩阵',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['二进制矩阵 `grid`，`diff[i][j] = 行 i 的一数 + 列 j 的一数 − 行 i 的零数 − 列 j 的零数`',
                 '返回差值矩阵 `diff`',
                 '示例：`[[0,1,1],[1,0,1],[0,0,1]]` → `[[0,0,4],[0,0,4],[-2,-2,2]]`'],
        quote='由于题目并没有对额外空间使用的要求，那么可以按照题目描述构造四个数组ones_row、ones_col、zeros_row以及zeros_col',
        quote_src='—— yiduobo 题解原文',
        idea=['第一轮遍历 `grid`，一次更新四个数组中的两个',
              '再建一个同样大小的 `res`，第二轮按题目公式逐格计算',
              '不抠空间：题意清楚，代码和题目描述一一对应'],
        summary=['时间 `O(mn)`，空间 `O(mn)`（`res` 加四个数组）',
                 '原文本来就是 Python 3 写法，无需修改',
                 '易错：行数组长度是 `m`，列数组长度是 `n`，别写反',
                 '对比灵神：灵神把 0 当 −1 只用两个数组，并原地写回 `grid`'],
    ),
)
