G = [[1, 0, 2], [1, 0, 2]]


def _col(S, a, b, v):
    if 'i' not in S or 'j' not in S:
        return None
    i, j = S['i'], S['j']
    if (a, b) == (i, j):
        return 'blue'
    if S['_line'] in (5, 6):
        if b == j - 1 and a == i and j:
            return 'pink'
        if a == i - 1 and b == j and i:
            return 'pink'
    if (a, b) < (i, j):
        return 'green'
    return None


def _txt(S):
    if 'x' not in S:
        return '规则：同一列要相等，同一行相邻要不等'
    i, j, x, g = S['i'], S['j'], S['x'], S['grid']
    left = f"左边 `{g[i][j - 1]}`" if j else '没有左边'
    up = f"上边 `{g[i - 1][j]}`" if i else '没有上边'
    return f"格子 `({i},{j}) = {x}`：{left}，{up}"


CONFIG = dict(
    num=3142, title='判断矩阵是否满足条件', difficulty='Easy', category='网格图',
    author='灵茶山艾府', technique='遍历 + 比较左边和上边',
    tags=[],
    code='''
class Solution:
    def satisfiesConditions(self, grid: List[List[int]]) -> bool:
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                if j and x == row[j - 1] or i and x != grid[i - 1][j]:
                    return False
        return True
''',
    call=f'Solution().satisfiesConditions({G})',
    expect=True,
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 当前格，粉 = 要比较的左 / 上邻居，绿 = 已检查通过）', cell=110, h=360,
             color=_col, cursors=[('i', 'j', 'yellow')]),
        dict(type='text', fn=_txt, size=28, h=110),
    ],
    watch=['i', 'j', 'x'],
    captions={
        'for i, row': lambda S, B, r: (f'检查第 `{S.i}` 行：`row = {S.row}`' if S.i != B.get('i', -1) or S.get('j') is None else '全部行检查完毕'),
        'for j, x': lambda S, B, r: (f'取格子 `grid[{S.i}][{S.j}] = {S.x}`' if (S.i, S.j) != (B.get('i'), B.get('j')) or B.get('j') is None else f'第 `{S.i}` 行检查完毕'),
        'if j and': lambda S, B, r: (lambda l, u: f"左边：{'无（j=0）' if not S.j else f'`{S.x} == {S.row[S.j - 1]}`？' + ('==相等，违规==' if l else '不等，合格')}；上边：{'无（i=0）' if not S.i else f'`{S.x} != {S.grid[S.i - 1][S.j]}`？' + ('==不等，违规==' if u else '相等，合格')}" + ('' if (l or u) else ' → 这格没问题'))(bool(S.j and S.x == S.row[S.j - 1]), bool(S.i and S.x != S.grid[S.i - 1][S.j])),
        'return False': '有格子违规，直接 ==返回 False==',
        'return True': '所有格子都没违规 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='每个格子只看左边和上边：左不能相等，上必须相等',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`m×n` 矩阵：每个格子要等于它下面的格子，且不等于它右边的格子',
                 '全部满足返回 `true`，否则 `false`',
                 '示例：`[[1,0,2],[1,0,2]]` → `true`；`[[1,1,1],[0,0,0]]` → `false`',
                 '`[[1],[2],[3]]` → `false`（同一列不相等）'],
        quote='遍历矩阵，挨个判断 grid[i][j]：如果 j>0 且 grid[i][j]=grid[i][j-1]，返回 false；如果 i>0 且 grid[i][j]≠grid[i-1][j]，返回 false。',
        quote_src='—— 灵茶山艾府题解',
        idea=['「下面要相等」「右边要不等」换个角度：从每个格子看==左边和上边==',
              '这样每对相邻格子恰好检查一次，且不用判断越界下界',
              '`j and ...` 用 `j` 当 `j > 0`，写得很短'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '易错：列要 ==相等==（`!=` 才违规），行要 ==不等==（`==` 才违规），别写反',
                 '第一行没有上边，第一列没有左边，用 `i and`、`j and` 挡住'],
    ),
)
