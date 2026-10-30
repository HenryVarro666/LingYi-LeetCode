GRID = [[1, 0, 0, 1],
        [1, 1, 0, 0],
        [0, 1, 1, 1],
        [1, 0, 0, 1]]
M, N = len(GRID), len(GRID[0])
L_ROWSUM, L_ADD = 6, 7          # `row_sum = ...` / `ans += ...` 所在行


def _ri(S):
    """当前行下标：row 是 grid 里的同一个列表对象"""
    row = S.get('row')
    if row is None:
        return None
    for i, r in enumerate(S['grid']):
        if r is row:
            return i
    return None


def _table(S):
    g = S['grid']
    m, n = len(g), len(g[0])
    ri = _ri(S)
    cs = S.get('col_sum')
    rows = []
    for i in range(m):
        shown = ri is not None and (i < ri or (i == ri and S['_line'] >= L_ROWSUM) or S['_line'] > L_ADD and i == ri)
        done = ri is not None and (i < ri or (i == ri and S['_line'] >= L_ADD))
        rows.append(list(g[i]) + [sum(g[i]) - 1 if (shown or done) else ''])
    rows.append([c for c in cs] + [''] if cs is not None else [''] * (n + 1))
    return rows


def _color(S, i, j, v):
    m, n = len(S['grid']), len(S['grid'][0])
    ri = _ri(S)
    ln = S['_line']
    if i == m:  # col_sum 行
        if j < n and ri is not None and ln == L_ADD and S['grid'][ri][j]:
            return 'green'
        return 'purple' if v != '' else None
    if j == n:  # row_sum 列
        return 'orange' if v != '' else None
    if v == 1:
        return 'cyan' if (ri is not None and i == ri) else 'blue'
    return None


def _formula(S):
    ri = _ri(S)
    if 'col_sum' not in S:
        return '直角顶点 `(i, j)`：同行另选一个 1，同列另选一个 1 —— 乘法原理'
    if ri is None:
        return '所有行都处理完了'
    g, cs = S['grid'], S['col_sum']
    ln = S['_line']
    if ln >= L_ADD and 'row_sum' in S:
        terms = [cs[j] for j in range(len(cs)) if g[ri][j]]
        t = ' + '.join(str(x) for x in terms) or '0'
        return f'第 {ri} 行：`row_sum × (Σ col_sum) = {S["row_sum"]} × ({t}) =` =={S["row_sum"] * sum(terms)}=='
    if ln >= L_ROWSUM and 'row_sum' in S:
        return f'第 {ri} 行有 `{sum(g[ri])}` 个 1，`row_sum = {S["row_sum"]}`'
    return f'枚举第 {ri} 行'


CONFIG = dict(
    num=3128, title='直角三角形', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举直角顶点 · 行列计数 + 乘法原理',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1541'],
    code='''
class Solution:
    def numberOfRightTriangles(self, grid: List[List[int]]) -> int:
        col_sum = [sum(col) - 1 for col in zip(*grid)]  # 提前减一
        ans = 0
        for row in grid:
            row_sum = sum(row) - 1  # 提前减一
            ans += row_sum * sum(cs for x, cs in zip(row, col_sum) if x)
        return ans
''',
    call=f'Solution().numberOfRightTriangles({GRID})',
    expect=17,
    views=[
        dict(type='text', fn=_formula, size=28, h=90),
        dict(type='table', var=_table, rows=[f'行{i}' for i in range(M)] + ['col'], cols=[f'列{j}' for j in range(N)] + ['row'],
             cell=100, color=_color, h=520,
             label='grid（蓝 = 1，青 = 当前行）；紫 = col_sum；橙 = row_sum（都已减一）'),
    ],
    watch=[('row_sum', 'row_sum', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'col_sum = [': '`zip(*grid)` 把行转成列：每列 1 的个数再减一 → `col_sum = {col_sum}`（直角顶点在该列时，同列另一个 1 的选法数）',
        'ans = 0': '`ans` 累加所有直角顶点对应的三角形个数',
        'for row in grid': lambda S, B, ret: ('所有行都枚举完了' if _ri(S) is None or _ri(S) == _ri(B)
                                              else f'枚举第 `{_ri(S)}` 行：这一行里每个 1 都可以作==直角顶点==。三个顶点里先定「中间」的直角顶点最简单'),
        'row_sum = sum(row) - 1': lambda S, B, ret: (f'第 `{_ri(S)}` 行有 `{sum(S.row)}` 个 1，减一：`row_sum = {S.row_sum}`，'
                                                     f'即同行另一个 1 的选法数'),
        'ans += row_sum * sum(': lambda S, B, ret: (
            f'直角顶点 `(i,j)` 有 `row_sum × col_sum[j]` 种；这一行把 `x = 1` 的列的 `col_sum` 加起来再乘 `row_sum`：'
            f'`{S.row_sum} × ({" + ".join(str(S.col_sum[j]) for j in range(len(S.col_sum)) if S.row[j]) or 0})` = '
            f'`{S.ans - B.ans}`，`ans` = =={S.ans}=='),
        'return ans': '所有行都处理完，返回 `ans = {ans}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='枚举直角顶点：同行另选一个 1 × 同列另选一个 1',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['二维 01 矩阵 `grid`，数由 3 个 `1` 组成的==直角三角形==',
                 '其中一个 1 与另一个 1 同行，并且与第三个 1 同列（不必相邻）',
                 '示例：`[[0,1,0],[0,1,1],[0,1,0]]` → `2`',
                 '本视频：4×4 的矩阵 → `17`'],
        quote='套路：有三个顶点，枚举「中间」的直角顶点更容易计算。设第 i 行有 rowSum 个 1，第 j 列有 colSum 个 1。根据乘法原理，直角顶点为 (i,j) 的「直角三角形」有 (rowSum−1)·(colSum−1) 个。',
        quote_src='—— 灵茶山艾府题解',
        idea=['直角顶点 `(i, j)` 必须是 1；同行另一个 1 有 `rowSum−1` 种，同列另一个 1 有 `colSum−1` 种',
              '乘法原理：`(rowSum−1) × (colSum−1)` 个三角形，每个三角形的直角顶点唯一，不重不漏',
              '代码把「减一」提前做掉，并把同一行的求和提到括号外：`row_sum × Σ(col_sum[j])`'],
        summary=['时间 `O(mn)`，空间 `O(n)`（`col_sum`）',
                 '`row_sum`、`col_sum` 都==提前减一==，所以公式里不再减',
                 '全 0 的行 `row_sum = -1`，但后面求和为 0，乘积还是 0，不影响答案',
                 '题解另有一行写法：把整个循环写成一个 `sum(...)` 推导式，思路相同',
                 '同类套路：枚举中间（2242、2867）'],
    ),
)
