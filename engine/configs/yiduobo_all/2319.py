def _cell(S, i, j, v):
    if 'n' not in S or 'j' not in S or (i, j) > (S['i'], S['j']):
        return None
    if i == j or i + j == S['n'] - 1:
        return 'red' if v == 0 else 'green'
    return 'red' if v != 0 else None


CONFIG = dict(
    num=2319, title='判断矩阵是否是一个 X 矩阵', difficulty='Easy', category='网格图',
    author='yiduobo', technique='遍历每格 + 对角线判断',
    code='''
class Solution(object):
    def checkXMatrix(self, grid):

        n = len(grid)
        for i in range(n):
            for j in range(n):
                if i == j or i + j == n - 1:
                    if grid[i][j] == 0:
                        return False
                elif grid[i][j] != 0:
                    return False
        
        return True
''',
    call='Solution().checkXMatrix([[5,0,1],[0,3,0],[2,0,0]])',
    expect=False,
    skip=['n = len(grid)', 'for i in range(n)'],
    views=[
        dict(type='grid', var='grid', label='grid（蓝框 = 当前格子，已检查的格子：绿 = 对角线上合格，红 = 违规）', cell=110, h=430,
             color=_cell, cursors=[('i', 'j', 'blue')]),
        dict(type='text', size=32, fn=lambda S: ('当前 `(i, j) = (' + str(S['i']) + ', ' + str(S['j']) + ')`：' +
                                                 ('==在对角线上==' if (S['i'] == S['j'] or S['i'] + S['j'] == S['n'] - 1) else '不在对角线上')) if 'j' in S and 'n' in S else ''),
    ],
    watch=['n', ('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'for j in range(n)': lambda S, B, r: (f'第 `{S.i}` 行的每一列都合格，换下一行' if ('j' in B and B.j == S.j)
                                              else f'看第 `{S.i}` 行第 `{S.j}` 列'),
        'if i == j or': lambda S, B, r: (f'`({S.i},{S.j})` 满足 `i == j` 或 `i + j == {S.n - 1}` → ==在对角线上==，这里必须非 0'
                                         if (S.i == S.j or S.i + S.j == S.n - 1) else
                                         f'`({S.i},{S.j})`：`i != j` 且 `i + j != {S.n - 1}` → 不在对角线上，这里必须是 0'),
        'if grid[i][j] == 0': lambda S, B, r: (f'对角线上的 `grid[{S.i}][{S.j}] = 0` → ==违反「对角线非 0」== → 马上返回 False'
                                              if S.grid[S.i][S.j] == 0 else f'对角线上的 `grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]}` 非 0，合格'),
        'elif grid[i][j] != 0': lambda S, B, r: (f'非对角线 `grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]}` 不是 0 → ==违反「其余为 0」== → 返回 False'
                                                if S.grid[S.i][S.j] != 0 else f'非对角线 `grid[{S.i}][{S.j}] = 0`，合格'),
        'return False': '只要有一个格子不合格，就不是 X 矩阵：返回 `False`',
        'return True': '所有格子都合格：返回 `True`',
    },
    cards=dict(
        one_liner='先判断格子在不在对角线上，再检查它该不该是 0',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['`n × n` 矩阵，==对角线上的数不为 0==，==其他位置全是 0== 才算 X 矩阵',
                 '示例 1：`[[2,0,0,1],[0,3,1,0],[0,5,2,0],[4,0,0,2]]` → `true`',
                 '本视频用 `[[5,0,1],[0,3,0],[2,0,0]]`：右下角对角线上是 0 → `false`'],
        quote='可以发现左对角线上的格子都满足横纵坐标相等，而右对角线上的格子则满足横纵坐标之和刚好等于n - 1，接下来只需遍历矩阵中的每个格子进行判断就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['观察样例得出：左对角线 `i == j`，右对角线 `i + j == n - 1`',
              '遍历每个格子：在对角线上就要求非 0，否则要求等于 0',
              '一旦发现不合格，立刻 `return False`'],
        summary=['时间 `O(n^2)`，空间 `O(1)`',
                 '两层判断：先分「对角线 / 非对角线」，再看值是否合格',
                 '对角线上是 0、非对角线上不是 0，都是违规',
                 '对比灵神：灵神用一个 `all` 表达式把两种情况合成 `(v != 0) == 在对角线上`'],
    ),
)
