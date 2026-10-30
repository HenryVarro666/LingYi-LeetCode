M = [[0, 1, 1, 1], [1, 1, 1, 1], [0, 1, 1, 1]]


def _col(S, i, j, v):
    if 'matrix' not in S:
        return None
    if v >= 3:
        return 'purple'
    if v == 2:
        return 'green'
    return None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or 'matrix' not in S or 'x' not in S:
        return '`f[i][j]` = 以 `(i,j)` 为右下角的全 1 正方形最大边长，也等于以它为右下角的正方形个数'
    m = S['matrix']
    if S.get('_line') in (5, 6) and i and j and S['x']:
        return f'`f[{i}][{j}] = min(上 {m[i-1][j]}, 左上 {m[i-1][j-1]}, 左 {m[i][j-1]}) + 1`'
    return f'当前格 `({i},{j})` 的值 = {m[i][j]}'


CONFIG = dict(
    num=1277, title='统计全为 1 的正方形子矩阵', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='原地 DP：右下角最大边长之和',
    tags=['单调栈'],
    code='''
class Solution:
    def countSquares(self, matrix: List[List[int]]) -> int:
        for i, row in enumerate(matrix):
            for j, x in enumerate(row):
                if x and i and j:
                    row[j] += min(matrix[i - 1][j], matrix[i - 1][j - 1], row[j - 1])
        return sum(map(sum, matrix))
''',
    call=f'Solution().countSquares({M})',
    expect=15,
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='grid', var='matrix', label='matrix 原地改成 f（黄 = 当前格；绿 = 边长 2；紫 = 边长 3）', cell=110, h=330,
             color=_col, cursors=[('i', 'j', 'yellow')]),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'x'],
    captions={
        'if x and i and j': lambda S, B, r: (
            f'`({S.i},{S.j})` 是 {S.x}：不是 1，没有正方形以它为右下角' if not S.x else
            f'`({S.i},{S.j})` 在第一行或第一列：最多只有边长 1 的正方形，保持 {S.x}' if not (S.i and S.j) else
            f'`({S.i},{S.j})` 是 1 且不在边缘 → ==用上、左上、左三个格子推出边长=='),
        'row[j] +=': '右下角在 `({i},{j})` 的最大边长 = 三个邻居最小值 + 1 = =={row[j]}==，同时也是以它为右下角的正方形个数',
        'return sum': '整个矩阵的元素和 = 所有正方形的个数 = ==`{ret}`==',
    },
    cards=dict(
        one_liner='右下角最大边长 f，同时就是以它为右下角的正方形个数',
        complexity='时间 `O(mn)`，空间 `O(1)`（原地修改）',
        problem=['`m × n` 的 0/1 矩阵，统计全由 1 组成的==正方形==子矩阵个数',
                 '示例：`[[0,1,1,1],[1,1,1,1],[0,1,1,1]]` → `15`',
                 '边长 1 有 10 个，边长 2 有 4 个，边长 3 有 1 个'],
        quote='根据图中的结论（**正方形个数等价于正方形最大边长**），答案为整个 $f$ 矩阵的元素和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i][j]` 为右下角在 `(i,j)` 的最大边长，边长为 k 就意味着有 k 个正方形以它为右下角',
              '转移：上、左上、左三个格子的最小值 + 1',
              '直接把 `matrix` 当作 `f` 原地改，最后求和'],
        summary=['时间 `O(mn)`，原地修改后空间 `O(1)`',
                 '第一行、第一列不转移，值本来就是 0 或 1',
                 '==必须取三个邻居的最小值==，只看其中两个会多算',
                 '灵神另给两种写法：枚举上下边界（`O(m²n)`）、单调栈（`O(mn)`，做完 85 题再看）；视频演示 DP 优化写法'],
    ),
)
