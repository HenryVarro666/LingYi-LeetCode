MATRIX = [[3, 0, 1], [5, 6, 3], [1, 2, 0]]
QUERIES = [(1, 1, 2, 2), (0, 1, 1, 2), (1, 0, 2, 1)]
ASSIGN = (11, 13, 15)  # 三个 += 行


def _q(S):
    return 'row1' in S and 'col2' in S


def _sm(S):
    return S.get('self.sum_matrix')


def _orig_color(S, i, j, v):
    if _q(S):
        return 'green' if S['row1'] <= i <= S['row2'] and S['col1'] <= j <= S['col2'] else None
    if 'i' in S and 'j' in S and (i, j) == (S['i'], S['j']):
        return 'orange'
    return None


def _sum_color(S, i, j, v):
    if _q(S):
        r1, c1, r2, c2 = S['row1'], S['col1'], S['row2'], S['col2']
        if (i, j) == (r2, c2):
            return 'green'
        if (i, j) in ((r2, c1 - 1), (r1 - 1, c2)) and min(i, j) >= 0:
            return 'red'
        if (i, j) == (r1 - 1, c1 - 1):
            return 'blue'
        return None
    if 'i' in S and 'j' in S:
        a, b = S['i'], S['j']
        if S.get('_line') in ASSIGN:
            if (i, j) == (a, b):
                return 'green'
            if (i, j) in ((a - 1, b), (a, b - 1)):
                return 'blue'
            if (i, j) == (a - 1, b - 1):
                return 'red'
        if (i, j) < (a, b) or (S.get('_line') in ASSIGN + (9,) and (i, j) == (a, b)):
            return 'cyan'
    return None


def _formula(S):
    sm = _sm(S)
    if sm is None:
        return ''
    if _q(S):
        return '绿 − 红(S1, S2+S3) + 蓝(S3)：==越界的项直接不写=='
    if 'i' in S and 'j' in S:
        return f'`(x, y) = ({S["i"]}, {S["j"]})`：绿 = 原值 + 蓝(上) + 蓝(左) − 红(左上)'
    return '==原地==把 matrix 变成前缀和：`sum[x][y]` = `(0,0)` 到 `(x,y)` 的和'


def _cap_if_i(S, B, ret):
    return (f'`i == 0`：第 0 行，==上面没有格子==，只能从左边累加' if S['i'] == 0
            else f'`i = {S["i"]}`，不在第 0 行')


def _cap_if_j(S, B, ret):
    return (f'`j == 0`：第 0 列，==左边没有格子==' if S['j'] == 0 else f'`j = {S["j"]}`，左边有格子')


def _cap_row0(S, B, ret):
    i, j = S['i'], S['j']
    return f'第 0 行只加左边：`{B.self.sum_matrix[i][j]} + sum[0][{j - 1}] ({S["self"].sum_matrix[i][j - 1]})` = =={S["self"].sum_matrix[i][j]}=='


def _cap_col0(S, B, ret):
    i, j = S['i'], S['j']
    return f'第 0 列只加上边：`{B.self.sum_matrix[i][j]} + sum[{i - 1}][0] ({S["self"].sum_matrix[i - 1][j]})` = =={S["self"].sum_matrix[i][j]}=='


def _cap_full(S, B, ret):
    i, j = S['i'], S['j']
    m = S['self'].sum_matrix
    return (f'原值 `{B.self.sum_matrix[i][j]}` + 上 `{m[i - 1][j]}` + 左 `{m[i][j - 1]}` − 左上 `{m[i - 1][j - 1]}`'
            f'（==上和左都含左上，加了两次==）= =={m[i][j]}==')


def _cap_q(S, B, ret):
    r1, c1, r2, c2 = S['row1'], S['col1'], S['row2'], S['col2']
    if r1 == 0 and c1 == 0:
        return f'贴着左上角：答案就是 `sum[{r2}][{c2}]` = =={ret}=='
    if r1 == 0:
        return f'`row1 = 0`：==上方没有 S1==，只减左边 S2+S3 = `sum[{r2}][{c1 - 1}]` → =={ret}=='
    if c1 == 0:
        return f'`col1 = 0`：==左边没有 S2==，只减上方 S1 = `sum[{r1 - 1}][{c2}]` → =={ret}=='
    return f'整块 − S1 − (S2+S3) + S3：减掉上方和左边，再补回被减两次的左上 → =={ret}=='


CONFIG = dict(
    num=304, title='二维区域和检索 - 矩阵不可变', difficulty='Medium', category='子串',
    author='yiduobo', technique='二维前缀和 · 原地累加 + 分情况处理边界',
    tags=['字节3个月', '字节6个月'],
    code='''
class NumMatrix(object):

    def __init__(self, matrix):
        self.sum_matrix = matrix[:]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if i == 0:
                    if j == 0:
                        continue
                    else:
                        self.sum_matrix[i][j] += self.sum_matrix[i][j - 1]
                elif j == 0:
                    self.sum_matrix[i][j] += self.sum_matrix[i - 1][j]
                else:
                    self.sum_matrix[i][j] += self.sum_matrix[i - 1][j] + self.sum_matrix[i][j - 1] - self.sum_matrix[i - 1][j - 1]

    def sumRegion(self, row1, col1, row2, col2):
        if row1 == 0:
            if col1 == 0:
                return self.sum_matrix[row2][col2]
            else:
                return self.sum_matrix[row2][col2] - self.sum_matrix[row2][col1 - 1]
        else:
            if col1 == 0:
                return self.sum_matrix[row2][col2] - self.sum_matrix[row1 - 1][col2]
            else:
                return self.sum_matrix[row2][col2] - self.sum_matrix[row2][col1 - 1] - self.sum_matrix[row1 - 1][col2] + self.sum_matrix[row1 - 1][col1 - 1]
''',
    call=f'''nm = NumMatrix({MATRIX})
[nm.sumRegion(*q) for q in {QUERIES}]''',
    expect=[11, 10, 14],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='grid', var=lambda S: MATRIX, label='matrix 原始值（橙 = 当前格；查询时绿 = 要求和的矩形）',
             rows=[0, 1, 2], cols=[0, 1, 2], color=_orig_color, cell=70, h=270),
        dict(type='grid', var=_sm, label='sum_matrix（青 = 已变成前缀和，其余还是原值）',
             rows=[0, 1, 2], cols=[0, 1, 2], color=_sum_color, cell=70, h=270),
    ],
    watch=['i', 'j', ('row1', 'row1'), ('col1', 'col1'), ('row2', 'row2'), ('col2', 'col2')],
    captions={
        'self.sum_matrix = matrix[:]': '`matrix[:]` 是==浅拷贝==：行还是同一批 list，等于在 matrix 上原地累加',
        'for i in range(len(matrix))': lambda S, B, r: (f'第 `{S.i}` 行' if B.get('i') != S.i else '整张前缀和表建好了'),
        'if i == 0': _cap_if_i,
        8: _cap_if_j,
        'continue': '`(0, 0)` 的前缀和==就是它自己==，跳过',
        'self.sum_matrix[i][j] += self.sum_matrix[i][j - 1]': _cap_row0,
        12: lambda S, B, r: ('`j == 0`：第 0 列，==左边没有格子==' if S.j == 0 else f'`j = {S.j}`，上边和左边都有格子 → 走 else'),
        13: _cap_col0,
        15: _cap_full,
        'if row1 == 0': lambda S, B, r: (f'查询 `({S.row1},{S.col1})`~`({S.row2},{S.col2})`：'
                                         + ('`row1 == 0`，上方没有要去掉的部分' if S.row1 == 0 else '`row1 > 0`，上方有 S1 要去掉')),
        'if col1 == 0': lambda S, B, r: ('`col1 == 0`，左边没有要去掉的部分' if S.col1 == 0 else '`col1 > 0`，左边有 S2 要去掉'),
        'return self.sum_matrix': _cap_q,
    },
    skip=['for j in range'],
    cards=dict(
        one_liner='维护左上角 (0,0) 到 (x,y) 的和，查询时减去上方 S1、左边 S2',
        complexity='初始化 `O(mn)`，`sumRegion` `O(1)`；额外空间 `O(1)`（原地）',
        problem=['给定二维矩阵 `matrix`，多次查询子矩阵元素和',
                 '子矩阵左上角 `(row1, col1)`，右下角 `(row2, col2)`',
                 '实现 `NumMatrix(matrix)` 和 `sumRegion(row1, col1, row2, col2)`',
                 '本视频：`3 × 3` 矩阵，三次查询分别覆盖 ==一般 / row1 = 0 / col1 = 0== 三种情况'],
        quote='在二维的情况下，需要维护的是==从矩阵左上角(0, 0)到当前位置(x, y)这个矩阵中所有数的和==。另外，在预处理以及求解的过程中都需要注意x或y等于0的情况。',
        quote_src='—— yiduobo 知乎题解',
        idea=['从 `sum[x2][y2]` 去掉上方 `S1 = sum[x1-1][y2]` 和左边 `S2`',
              '`S2` 不是前缀，补上左上 `S3`：`S2 + S3 = sum[x2][y1-1]`，`S3 = sum[x1-1][y1-1]`',
              '答案 `= sum[x2][y2] - S1 - (S2+S3) + S3`；预处理用同样的容斥递推'],
        result='三次查询依次返回 `[11, 10, 14]` ✓',
        summary=['初始化 `O(mn)`，查询 `O(1)`；`matrix[:]` 是浅拷贝，==输入矩阵被原地改成了前缀和==',
                 '没有多开一行一列，所以 x 或 y 为 0 时==要分情况==，否则 `-1` 下标会绕到最后一行/列',
                 '对比灵神：`s` 多开一行一列 0，四种情况合成一个公式',
                 '原文为 Python 2 风格：已删去文档字符串和 LeetCode 模板注释，代码未改'],
    ),
)
