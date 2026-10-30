def _done_src(S, i, j, v):  # matrix 中已经搬过去的格子
    if 'i' not in S or 'j' not in S:
        return None
    ci, cj = S['i'], S['j']
    moved = (i, j) <= (ci, cj) and S['ans'][j][i] == S['matrix'][i][j]
    return 'green' if moved else None


def _done_dst(S, r, c, v):  # ans[r][c] 来自 matrix[c][r]
    return _done_src(S, c, r, v)


def show(S):
    if 'ans' not in S:
        return '转置：`ans[j][i] = matrix[i][j]`'
    if 'j' in S and S.get('_line') == 7:
        return f"`ans[{S['j']}][{S['i']}] = matrix[{S['i']}][{S['j']}] = {S['x']}`"
    if 'j' in S and 'i' in S:
        return f"第 `{S['i']}` 行的第 `{S['j']}` 个数 `{S['x']}` → 去 `ans` 的第 `{S['j']}` 行第 `{S['i']}` 列"
    return f"`matrix` 是 `{S['m']}×{S['n']}`，`ans` 是 `{S['n']}×{S['m']}`"


CONFIG = dict(
    num=867, title='转置矩阵', difficulty='Easy', category='矩阵',
    author='灵茶山艾府', technique='新建 n×m 矩阵 · ans[j][i] = matrix[i][j]',
    tags=['List.md'],
    code='''
class Solution:
    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        m, n = len(matrix), len(matrix[0])
        ans = [[0] * m for _ in range(n)]
        for i, row in enumerate(matrix):
            for j, x in enumerate(row):
                ans[j][i] = x
        return ans
''',
    call='Solution().transpose([[1,2,3],[4,5,6]])',
    expect=[[1, 4], [2, 5], [3, 6]],
    views=[
        dict(type='grid', var='matrix', label='matrix（m × n = 2 × 3，黄框 = (i, j)，绿 = 已搬走）', h=250, cell=80,
             rows=lambda S: list(range(len(S['matrix']))), cols=lambda S: list(range(len(S['matrix'][0]))),
             cursors=[('i', 'j', 'yellow')], color=_done_src),
        dict(type='grid', var='ans', label='ans（n × m = 3 × 2，粉框 = (j, i)）', h=300, cell=80,
             rows=lambda S: list(range(len(S['ans']))), cols=lambda S: list(range(len(S['ans'][0]))),
             cursors=[('j', 'i', 'pink')], color=_done_dst),
        dict(type='text', fn=show, size=28, h=60),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'pink'), ('x', 'x'), ('row', 'row')],
    captions={
        'm, n = len(matrix)': '`matrix` 有 `m = {m}` 行、`n = {n}` 列',
        'ans = [[0] * m': '新建 `ans`：==n 行 m 列==（`{n}×{m}`），行数和列数正好反过来',
        'for i, row in enumerate(matrix)': lambda S, B, ret: (f'取 `matrix` 的第 `{S.i}` 行 `{S.row}`'
                                                              if S.get('i') != B.get('i') else '每一行都搬完了'),
        'for j, x in enumerate(row)': lambda S, B, ret: (f'第 `{S.j}` 列：`x = matrix[{S.i}][{S.j}] = {S.x}`'
                                                         if (S.get('j'), S.get('i')) != (B.get('j'), B.get('i')) or 'j' not in B
                                                         else f'第 `{S.i}` 行的数都放好了'),
        'ans[j][i] = x': lambda S, B, ret: (f'`ans[{S.j}][{S.i}] = {S.x}`：==行号和列号交换==，放到主对角线另一侧的对称位置'
                                            if S.j == 1 and S.i == 0 else
                                            f'`ans[{S.j}][{S.i}] = {S.x}`：matrix 的第 `{S.i}` 行 → ans 的第 `{S.i}` 列'),
        'return ans': '返回 `ans = {ret}`',
    },
    cards=dict(
        one_liner='新建一个 n×m 的矩阵，把 matrix[i][j] 放到 ans[j][i]',
        complexity='时间 `O(mn)`，空间 `O(1)`（返回值不计入）',
        problem=['给你一个 `m×n` 的二维数组 `matrix`，返回它的==转置矩阵==',
                 '转置：沿主对角线翻转，==交换行索引与列索引==',
                 '示例：`[[1,2,3],[4,5,6]]` → `[[1,4],[2,5],[3,6]]`'],
        quote='创建一个新的 n×m 的矩阵 ans。……把这一列中的元素 `matrix[i][j]` 填到 `ans[j][i]` 中。',
        quote_src='—— 灵茶山艾府题解「简单题，简单做」',
        idea=['转置后形状从 `m×n` 变成 `n×m`，所以要==新建==矩阵，不能原地交换（非方阵时放不下）',
              '遍历 `matrix` 的每个元素 `matrix[i][j]`，直接写到 `ans[j][i]`'],
        result='返回 `[[1,4],[2,5],[3,6]]`：原来的第 0 行变成了第 0 列 ✓',
        summary=['时间 `O(mn)`，空间 `O(1)`（返回值不计入）',
                 '易错：`ans` 是 `n` 行 `m` 列，写成 `[[0] * n for _ in range(m)]` 会越界',
                 '易错：`[[0] * m] * n` 的每一行是同一个列表，改一处全变',
                 '灵神还给了库函数写法：`list(zip(*matrix))`'],
    ),
)
