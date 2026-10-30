G = [[1, 0, 1], [1, 0, 0]]


def _col(S, a, b, v):
    if 'i' not in S or 'j' not in S:
        return None
    i, j = S['i'], S['j']
    if (a, b) == (i, j):
        return 'blue'
    if S['_line'] == 8:
        if (a, b) == (i + 1, j) and i < S['m'] - 1:
            return 'pink'
        if (a, b) == (i, j + 1) and j < S['n'] - 1:
            return 'orange'
    if (a, b) < (i, j):
        return 'green'
    return None


def _txt(S):
    if 'i' not in S or 'j' not in S:
        return '条件 1：下面存在则必须相等；条件 2：右边存在则必须不等'
    g, i, j, m, n = S['grid'], S['i'], S['j'], S['m'], S['n']
    d = f"下 `{g[i + 1][j]}`" if i < m - 1 else '无下'
    r = f"右 `{g[i][j + 1]}`" if j < n - 1 else '无右'
    return f"格子 `({i},{j}) = {g[i][j]}`：{d}，{r}"


CONFIG = dict(
    num=3142, title='判断矩阵是否满足条件', difficulty='Easy', category='网格图',
    author='yiduobo', technique='按题意逐格检查（下 / 右）',
    tags=[],
    code='''
class Solution(object):
    def satisfiesConditions(self, grid):

        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            for j in range(n):
                if (i < m - 1 and grid[i][j] != grid[i + 1][j]) or (j < n - 1 and grid[i][j] == grid[i][j + 1]):
                    return False
        
        return True
''',
    call=f'Solution().satisfiesConditions({G})',
    expect=False,
    skip=['m = len', 'n = len'],
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 当前格，粉 = 下邻居，橙 = 右邻居，绿 = 已通过）', cell=110, h=360,
             color=_col, cursors=[('i', 'j', 'yellow')]),
        dict(type='text', fn=_txt, size=28, h=110),
    ],
    watch=['m', 'n', 'i', 'j'],
    captions={
        'for i in range': lambda S, B, r: (f'检查第 `{S.i}` 行（共 m = {S.m} 行）' if S.i != B.get('i', -1) else '所有行检查完毕'),
        'for j in range': lambda S, B, r: (f'看格子 `grid[{S.i}][{S.j}]`（共 n = {S.n} 列）' if (S.i, S.j) != (B.get('i'), B.get('j')) else f'第 `{S.i}` 行检查完毕'),
        'if (i < m - 1': lambda S, B, r: (lambda g, i, j, m, n: (
            f"下：{'无（最后一行）' if i >= m - 1 else f'`{g[i][j]} != {g[i + 1][j]}`？' + ('==不相等，违反条件 1==' if g[i][j] != g[i + 1][j] else '相等，满足')}；"
            f"右：{'无（最后一列）' if j >= n - 1 else f'`{g[i][j]} == {g[i][j + 1]}`？' + ('==相等，违反条件 2==' if g[i][j] == g[i][j + 1] else '不等，满足')}"))(S.grid, S.i, S.j, S.m, S.n),
        'return False': '这个格子违反了条件，直接 ==返回 False==',
        'return True': '全部格子都满足条件 → 返回 {ret}',
    },
    cards=dict(
        after=[dict(heading='全部通过的例子', lines=['`[[1,0,2],[1,0,2]]`：每列上下相等，每行相邻不等', '所有格子都通过检查，才会走到最后的 `return True`', '只要有一个格子违规，就在那一刻提前返回 False'])],
        one_liner='照着题意，对每个格子检查「下面相等、右边不等」',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['矩阵每个格子 `grid[i][j]`：下面的格子存在则 ==相等==',
                 '右边的格子存在则 ==不相等==',
                 '全部满足返回 `true`，否则 `false`',
                 '演示：`[[1,0,1],[1,0,0]]`，第 0 行最后一格下面是 0，不等'],
        quote='只需对grid一趟遍历，按照题目要求判断每个单元格是否符合条件即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['没有技巧，直接把两条规则写成一个 if',
              '「存在」靠边界判断：`i < m - 1`、`j < n - 1`',
              '任何一个格子违规就能提前返回 False'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '易错：下面要 ==相等==（`!=` 违规），右边要 ==不等==（`==` 违规）',
                 '易错：别漏掉边界判断，否则越界',
                 '代码照搬原文，没有改动'],
    ),
)
