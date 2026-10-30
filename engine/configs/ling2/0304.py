MATRIX = [[3, 0, 1, 4], [5, 6, 3, 2], [1, 2, 0, 1]]
QUERIES = [(1, 1, 2, 2), (0, 1, 2, 3)]


def _q(S):
    return 'r1' in S and 'c2' in S


def _init(S):
    return not _q(S) and 'i' in S and 'j' in S


def _mat_color(S, i, j, v):
    if _q(S):
        return 'green' if S['r1'] <= i <= S['r2'] and S['c1'] <= j <= S['c2'] else None
    if _init(S):
        if (i, j) == (S['i'], S['j']):
            return 'orange'
        if (i, j) < (S['i'], S['j']):
            return 'cyan'
    return None


def _s_color(S, i, j, v):
    if _q(S):
        r1, c1, r2, c2 = S['r1'], S['c1'], S['r2'], S['c2']
        if (i, j) == (r2 + 1, c2 + 1):
            return 'green'
        if (i, j) in ((r2 + 1, c1), (r1, c2 + 1)):
            return 'red'
        if (i, j) == (r1, c1):
            return 'blue'
        return None
    if _init(S) and S.get('_line') == 7:
        a, b = S['i'], S['j']
        if (i, j) == (a + 1, b + 1):
            return 'green'
        if (i, j) in ((a + 1, b), (a, b + 1)):
            return 'blue'
        if (i, j) == (a, b):
            return 'red'
    return None


def _formula(S):
    s = S.get('s')
    if not isinstance(s, list):
        return ''
    if _q(S):
        r1, c1, r2, c2 = S['r1'], S['c1'], S['r2'], S['c2']
        a, b, c, d = s[r2 + 1][c2 + 1], s[r2 + 1][c1], s[r1][c2 + 1], s[r1][c1]
        return f'==绿== − 红 − 红 + 蓝 = `{a} − {b} − {c} + {d}` = =={a - b - c + d}=='
    if _init(S) and S.get('_line') == 7:
        i, j = S['i'], S['j']
        return (f'`s[{i + 1}][{j + 1}]` = 蓝 + 蓝 − 红 + `x` = `{s[i + 1][j]} + {s[i][j + 1]} − {s[i][j]} + {S["x"]}`'
                f' = =={s[i + 1][j + 1]}==')
    return '`s[i+1][j+1]` = 左上角 `(0,0)` 到 `(i,j)` 的子矩阵元素和'


def _cap_init(S, B, ret):
    i, j, x = S['i'], S['j'], S['x']
    s = S['s']
    return (f'上方 `s[{i}][{j + 1}] = {s[i][j + 1]}` + 左方 `s[{i + 1}][{j}] = {s[i + 1][j]}`，'
            f'重叠部分 `s[{i}][{j}] = {s[i][j]}` ==加了两次要减掉==，再加 `x = {x}` → =={s[i + 1][j + 1]}==')


def _cap_ret(S, B, ret):
    r1, c1, r2, c2 = S['r1'], S['c1'], S['r2'], S['c2']
    extra = '；`r1 = 0` 时减的是 `s[0][..] = 0`，==不用特判==' if r1 == 0 else ''
    return f'`({r1},{c1})`~`({r2},{c2})` 的和 = 大矩形 − 上方 − 左方 + 左上（被减两次）= =={ret}=={extra}'


CONFIG = dict(
    num=304, title='二维区域和检索 - 矩阵不可变', difficulty='Medium', category='子串',
    author='灵茶山艾府', technique='二维前缀和 · 容斥',
    tags=['字节3个月', '字节6个月'],
    code='''
class NumMatrix:
    def __init__(self, matrix: List[List[int]]):
        m, n = len(matrix), len(matrix[0])
        s = [[0] * (n + 1) for _ in range(m + 1)]
        for i, row in enumerate(matrix):
            for j, x in enumerate(row):
                s[i + 1][j + 1] = s[i + 1][j] + s[i][j + 1] - s[i][j] + x
        self.s = s

    # 返回左上角在 (r1, c1) 右下角在 (r2, c2) 的子矩阵元素和
    def sumRegion(self, r1: int, c1: int, r2: int, c2: int) -> int:
        s = self.s
        return s[r2 + 1][c2 + 1] - s[r2 + 1][c1] - s[r1][c2 + 1] + s[r1][c1]
''',
    call=f'''nm = NumMatrix({MATRIX})
[nm.sumRegion(*q) for q in {QUERIES}]''',
    expect=[11, 19],
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='grid', var=lambda S: MATRIX, label='matrix（橙 = 当前 x；查询时绿 = 要求和的子矩形）',
             rows=[0, 1, 2], cols=[0, 1, 2, 3], color=_mat_color, cell=66, h=250),
        dict(type='grid', var='s', label='s（多一行一列 0；s[i+1][j+1] = 左上角到 (i,j) 的和）',
             rows=lambda S: list(range(len(S['s']))), cols=lambda S: list(range(len(S['s'][0]))),
             color=_s_color, cell=66, h=320),
    ],
    watch=['i', 'j', 'x', ('r1', 'r1'), ('c1', 'c1'), ('r2', 'r2'), ('c2', 'c2')],
    captions={
        'm, n = len': '`m = {m}` 行，`n = {n}` 列',
        's = [[0] * (n + 1)': '前缀和矩阵开 `(m+1) × (n+1) = {m+1} × {n+1}`：==第 0 行、第 0 列全是 0==，省去边界特判',
        'for i, row in enumerate': lambda S, B, r: (f'第 `{S.i}` 行：`row = {S.row}`' if B.get('i') != S.i
                                                   else '所有前缀和都算好了'),
        's[i + 1][j + 1] =': _cap_init,
        'self.s = s': '预处理完成：`O(mn)`；之后每次查询 ==只用 4 个数==，`O(1)`',
        's = self.s': '查询 `({r1},{c1})`~`({r2},{c2})`：用 4 个前缀和容斥',
        'return s[r2 + 1]': _cap_ret,
    },
    skip=['for j, x in enumerate'],
    cards=dict(
        one_liner='一张图秒懂：大矩形 − 上 − 左 + 左上，就是任意子矩形的和',
        complexity='初始化 `O(mn)`，`sumRegion` `O(1)`；空间 `O(mn)`',
        problem=['给定二维矩阵 `matrix`，多次查询子矩阵元素和',
                 '子矩阵左上角 `(row1, col1)`，右下角 `(row2, col2)`',
                 '实现 `NumMatrix(matrix)` 和 `sumRegion(row1, col1, row2, col2)`',
                 '本视频：`3 × 4` 矩阵，查询 `(1,1,2,2)` → `11`，`(0,1,2,3)` → `19`'],
        quote='【图解】==一张图秒懂二维前缀和！== 返回左上角在 (r1, c1) 右下角在 (r2, c2) 的子矩阵元素和：`s[r2+1][c2+1] - s[r2+1][c1] - s[r1][c2+1] + s[r1][c1]`',
        quote_src='—— 灵茶山艾府题解（标题 + 代码注释）',
        idea=['`s[i+1][j+1]` 表示左上角 `(0,0)` 到右下角 `(i,j)` 的子矩阵和，多开一行一列 0',
              '递推：上方 + 左方 − ==重叠的左上== + 当前数 `x`',
              '查询同理：整块 − 上方条 − 左方条 + ==被减了两次的左上角=='],
        result='两次查询依次返回 `[11, 19]` ✓',
        summary=['初始化 `O(mn)`，每次查询 `O(1)`，空间 `O(mn)`',
                 '下标偏移：`s` 比 `matrix` 多一行一列，查询用 `r2+1`、`c2+1`',
                 '易错：容斥时左上角被减了两次，==要加回来一次==',
                 '同类：303 一维前缀和、1314 矩阵区域和、363 不超过 K 的最大矩形和'],
    ),
)
