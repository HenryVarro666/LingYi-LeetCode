GRID = [[0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]]
L_FOR1, L_FOR2, L_IF2, L_RES = 8, 15, 17, 18   # 两个 `for i` 行、第二遍的 `if` 行、`res += ...` 行


def _j(S):
    if 'i' not in S or 'j' not in S or S['_line'] in (L_FOR1, L_FOR2):
        return None
    return S['j']


def _color(S, i, j, v):
    ci, cj = S.get('i'), _j(S)
    if 'res' in S and S['_line'] in (L_IF2, L_RES) and cj is not None and S['grid'][ci][cj] == 1 and v == 1:
        if (i, j) == (ci, cj):
            return 'green'
        if i == ci:
            return 'cyan'
        if j == cj:
            return 'purple'
    return 'blue' if v == 1 else None


def _formula(S):
    if 'row' not in S:
        return '先统计每行、每列各有几个 1，再枚举每个 1 当直角顶点'
    if 'res' not in S:
        return f'第一遍：`row[i]` = 第 i 行 1 的个数，`col[j]` = 第 j 列 1 的个数'
    j = _j(S)
    if j is None or 'i' not in S:
        return '第二遍：每个值为 1 的格子当直角顶点，累加 `(row[i] − 1) × (col[j] − 1)`'
    i = S['i']
    if S['grid'][i][j] != 1:
        return f'`({i}, {j})` 是 0，不能作顶点'
    x, y = S['row'][i] - 1, S['col'][j] - 1
    return f'顶点 `({i}, {j})`：同行另选 `{x}` 个（青）× 同列另选 `{y}` 个（紫）= =={x * y}=='


CONFIG = dict(
    num=3128, title='直角三角形', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举直角顶点 · 预处理每行每列 1 的个数',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1541'],
    code='''
class Solution(object):
    def numberOfRightTriangles(self, grid):
        m = len(grid)
        n = len(grid[0])

        row = [0] * m
        col = [0] * n
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    row[i] += 1
                    col[j] += 1

        res = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    res += (row[i] - 1) * (col[j] - 1)

        return res
''',
    call=f'Solution().numberOfRightTriangles({GRID})',
    expect=4,
    skip=['m = len(grid)', 'n = len(grid[0])', 'for j in range(n)'],
    views=[
        dict(type='text', fn=_formula, size=28, h=70),
        dict(type='grid', var='grid', label='grid（蓝 = 1）', cell=84, color=_color,
             cursors=[('i', _j, 'yellow', '(i,j)')], h=300),
        dict(type='array', var='row', label='row[i]：第 i 行 1 的个数', cell=72, pointers={'i': 'blue'}),
        dict(type='array', var='col', label='col[j]：第 j 列 1 的个数', cell=72, pointers={_j: 'pink'},
             pointer_labels={_j: 'j'}),
    ],
    watch=['i', ('j', _j, 'pink'), ('row[i]', 'row[i]', 'orange'), ('col[j]', 'col[j]', 'purple'), ('res', 'res', 'green')],
    captions={
        'row = [0] * m': '`row[i]` 记录第 `i` 行有几个 1',
        'col = [0] * n': '`col[j]` 记录第 `j` 列有几个 1',
        'for i in range(m)': lambda S, B, ret: (
            ('第一遍：统计行列计数，' if 'res' not in S else '第二遍：枚举每个 1 作直角顶点，')
            + ('扫完所有行了' if 'i' in B and S.i == B.i and S._line == B._line and B.get('j') == S.get('j') and S.i == len(S.grid) - 1
               else f'处理第 `{S.i}` 行')),
        'if grid[i][j] == 1': lambda S, B, ret: (
            (f'`grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]}`' + ('，是 1 → 统计进 `row[i]` 和 `col[j]`' if S.grid[S.i][S.j] == 1 else '，是 0 → 跳过'))
            if 'res' not in S else
            (f'`grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]}`' + ('，是 1 → 可以作直角顶点' if S.grid[S.i][S.j] == 1 else '，是 0 → 不能作顶点'))),
        'row[i] += 1': '`row[{i}]` → {row[i]}',
        'col[j] += 1': '`col[{j}]` → {col[j]}',
        'res = 0': '`res = 0`，第二遍遍历累加每个直角顶点的三角形个数',
        'res += (row[i] - 1) * (col[j] - 1)': ('顶点 `({i},{j})`：同行另一个 1 有 `{row[i]} − 1 = {row[i] - 1}` 种，同列另一个 1 有 '
                                               '`{col[j]} − 1 = {col[j] - 1}` 种 → 乘法原理 `{(row[i] - 1) * (col[j] - 1)}`，`res` = =={res}=='),
        'return res': '返回 `res = {res}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='直角顶点同行同列各再选一个 1：(行内 1 的个数 − 1) × (列内 1 的个数 − 1)',
        complexity='时间 `O(mn)`，空间 `O(m + n)`',
        problem=['01 矩阵里，3 个 `1` 组成==直角三角形==：一个 1 与另一个 1 同行，与第三个 1 同列',
                 '三个 1 不必相邻',
                 '示例：`[[0,1,0],[0,1,1],[0,1,0]]` → `2`',
                 '本视频：十字形 `[[0,1,0],[1,1,1],[0,1,0]]` → `4`'],
        quote='可以尝试枚举所有直角位置的1，对于位于(i, j)的1，若i这一行存在x个1，j这一列存在y个1，那么从i这一行中另外x - 1个1中任选一个，从j这一列中另外y - 1个1中任选一个，就能构成一个直角三角形。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一遍遍历：`row[i]`、`col[j]` 记下每行每列 1 的个数',
              '第二遍遍历：遇到 1 就当直角顶点，同行另选一个、同列另选一个',
              '每个三角形的直角顶点唯一，所以不会重复计数'],
        summary=['时间 `O(mn)`，空间 `O(m + n)`：遍历两遍矩阵',
                 '易错：别忘了 `− 1`，顶点本身不能再被选作另外两个顶点',
                 '只对值为 1 的格子累加；值为 0 的格子行列有 1 也不能作顶点',
                 '原文为 Python 2 风格写法（`class Solution(object)`），代码未改，只去掉了空行里的缩进空格',
                 '对比灵神：灵神把 `−1` 提前、同行求和提到括号外，只用 `col_sum` 一个数组，逐行 `sum`'],
    ),
)
