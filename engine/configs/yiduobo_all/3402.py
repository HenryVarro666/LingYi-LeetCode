G = [[3, 2], [1, 3], [3, 4], [0, 1]]

CONFIG = dict(
    num=3402, title='使每一列严格递增的最少操作次数', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='逐列遍历，原地抬高',
    tags=['灵神题单', '难度分 1246'],
    code='''
class Solution(object):
    def minimumOperations(self, grid):
        
        m = len(grid)
        n = len(grid[0])

        res = 0
        for j in range(n):
            for i in range(1, m):
                if grid[i][j] <= grid[i - 1][j]:
                    res += grid[i - 1][j] + 1 - grid[i][j]
                    grid[i][j] = grid[i - 1][j] + 1
        
        return res
''',
    call=f'Solution().minimumOperations({G})',
    expect=15,
    skip=['m = len', 'n = len', 'res = 0'],
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 上方相邻元素，粉 = 当前元素；被抬高后的值直接写回）', cell=96, h=420,
             cursors=[('i - 1 if i >= 1 else None', 'j', 'blue'), ('i', 'j', 'pink')]),
        dict(type='text', fn=lambda S: (f"当前 `grid[{S['i']}][{S['j']}] = {S['grid'][S['i']][S['j']]}`，上方 `{S['grid'][S['i']-1][S['j']]}`" if 'i' in S and 'j' in S and S['i'] >= 1 else ''), size=30),
    ],
    watch=[('j', 'j', 'blue'), ('i', 'i', 'pink'), ('res', 'res', 'green')],
    captions={
        'for j in range(n)': lambda S, B, r: (f'列与列无关，==每一列单独考虑==：现在处理第 `{S.j}` 列' if S.j != B.get('j', -1) else '所有列都扫完了'),
        'for i in range(1, m)': '从第 1 行开始，和上方相邻元素比较（第 0 行不用动）',
        'if grid[i][j] <= grid[i - 1][j]': lambda S, B, r: (f'`{B.grid[B.i][B.j]} <= {B.grid[B.i-1][B.j]}`：不比上面大 → 要抬高'
                                                           if B.grid[B.i][B.j] <= B.grid[B.i - 1][B.j]
                                                           else f'`{B.grid[B.i][B.j]} > {B.grid[B.i-1][B.j]}`：已经严格递增，无需操作'),
        'res += ': '需要 `上方 + 1 - 当前` 次操作：累计 `res = {res}`',
        'grid[i][j] = grid[i - 1][j] + 1': '把它抬到「上方 + 1」并写回 `grid`：==越小越好==，不拖累下面的元素',
        'return res': '所有列处理完，返回 `{res}`',
    },
    cards=dict(
        one_liner='每列从上往下，不够大就抬到上方 + 1',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`m×n` 非负矩阵，每次操作可把一个元素加 1',
                 '求让每一列都==严格递增==的最少操作次数',
                 '示例：`[[3,2],[1,3],[3,4],[0,1]]` → `15`'],
        quote='对于靠前的行就应该在满足递增的前提下越小越好，于是对于每列，只需从第1行开始遍历，对于当前元素，若其小于等于上面的相邻元素，就将其增加到上面相邻元素加1并更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['列与列之间无关，逐列处理',
              '只能加 1：靠前的行越小越好',
              '原地把元素改成「上方 + 1」，下一行比较的就是改后的值'],
        summary=['时间 `O(mn)`，直接修改了输入 `grid`',
                 '易错：抬高后必须写回 `grid`，否则下一行比较的是旧值',
                 '原文已是 Python 3 可运行写法，代码未改'],
    ),
)
