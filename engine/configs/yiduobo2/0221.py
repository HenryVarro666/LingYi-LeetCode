M = [["1", "1", "0"],
     ["1", "1", "1"],
     ["0", "1", "1"]]


def _cell(S):
    return 'j' in S and 'i' in S and S.get('_line') in (14, 15, 16, 18, 19)


def _mat_color(S, r, c, v):
    if S.get('_line') in (16, 18, 19) and _cell(S):
        i, j = S['i'], S['j']
        k = S['f'][i][j]
        if i - k < r <= i and j - k < c <= j:
            return 'green'
    return 'blue' if v == '1' else None


def _f_color(S, r, c, v):
    if S.get('_line') == 21 and v == S['res'] and v > 0:
        return 'green'
    if not _cell(S) or S['matrix'][S['i']][S['j']] != '1':
        return None
    i, j = S['i'], S['j']
    if i > 0 and j > 0 and (r, c) in ((i, j - 1), (i - 1, j), (i - 1, j - 1)):
        f = S['f']
        nb = (f[i][j - 1], f[i - 1][j], f[i - 1][j - 1])
        return 'cyan' if v == min(nb) else 'purple'
    return None


def _formula(S):
    if not _cell(S):
        if 'res' in S and S.get('_line') == 21:
            return f"最大边长 `res = {S['res']}` → 面积 `res * res = {S['res'] ** 2}`"
        return '`f[i][j]`：以 `(i, j)` 为右下角的最大正方形的==边长=='
    i, j, f = S['i'], S['j'], S['f']
    if S['matrix'][i][j] != '1':
        return f"`matrix[{i}][{j}] = '0'` → `f[{i}][{j}]` 只能为 0"
    if i == 0 or j == 0:
        return f'`({i}, {j})` 在边界上 → `f[{i}][{j}] = 1`'
    a, b, c = f[i][j - 1], f[i - 1][j], f[i - 1][j - 1]
    return f'`min(左 {a}, 上 {b}, 左上 {c}) + 1` = =={min(a, b, c) + 1}=='


def _if1(S, B, ret):
    i, j = S.i, S.j
    if S.matrix[i][j] == '1':
        return f"`matrix[{i}][{j}] = '1'` → 它可以是某个正方形的右下角"
    return f"`matrix[{i}][{j}] = '0'`（情况 1）：`f[{i}][{j}]` 只能为 0"


def _if_border(S, B, ret):
    i, j = S.i, S.j
    if i == 0 or j == 0:
        return f'`i = {i}`、`j = {j}`，在==边界==上（情况 2）：往左上没有格子了'
    return f'`({i}, {j})` 不在边界（情况 3）：看左、上、左上能到多远'


def _assign(S, B, ret):
    i, j, f = S.i, S.j, S.f
    a, b, c = f[i][j - 1], f[i - 1][j], f[i - 1][j - 1]
    v = f[i][j]
    head = f'`f[{i}][{j}] = min({a}, {b}, {c}) + 1 = {v}`'
    if min(a, b, c) == 0:
        return head + '：有一个方向是 0 → 只能是 1×1'
    if v > 1 and a == b == c:
        return head + f'：三个方向都达到 {a} → ==能扩到 {v}×{v}=='
    return head + f'：最短的方向只有 {min(a, b, c)} → 边长 {v}'


CONFIG = dict(
    num=221, title='最大正方形', difficulty='Medium', category='多维动态规划',
    author='yiduobo', technique='二维 DP · 边界特判 + 三方向取 min',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution(object):
    def maximalSquare(self, matrix):
        if not matrix:
            return 0

        m = len(matrix)
        n = len(matrix[0])

        f = [[0] * n for _ in range(m)]
        res = 0

        for i in range(m):
            for j in range(n):
                if matrix[i][j] == '1':
                    if i == 0 or j == 0:
                        f[i][j] = 1
                    else:
                        f[i][j] = min(f[i][j - 1], f[i - 1][j], f[i - 1][j - 1]) + 1
                    res = max(res, f[i][j])

        return res * res
''',
    call=f'Solution().maximalSquare({M})',
    expect=4,
    skip=['m = len', 'n = len', 'for j in range'],
    views=[
        dict(type='grid', var='matrix', label='matrix（黄框 = (i, j)，蓝 = 1，绿 = 以它为右下角的正方形）', cell=80, h=300,
             color=_mat_color, cursors=[('i', 'j', 'yellow')], rows=[0, 1, 2], cols=[0, 1, 2]),
        dict(type='text', fn=_formula, h=60, size=25),
        dict(type='grid', var='f', label='f（黄框 = f[i][j]，紫/青 = 左、上、左上，青 = 最小）', cell=80, h=300,
             color=_f_color, cursors=[('i', 'j', 'yellow')], rows=[0, 1, 2], cols=[0, 1, 2]),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('res', 'res', 'green')],
    captions={
        'if not matrix': '矩阵非空，开始 DP',
        'f = [[0] * n': '`f[i][j]`：以 `(i, j)` 为右下角的最大正方形的边长，先全填 0',
        'res = 0': '`res` 记录最大边长',
        'for i in range': lambda S, B, r: (f'第 `i = {S.i}` 行' if 'i' not in B or S.i != B.i else '所有格子算完'),
        "if matrix[i][j] == '1'": _if1,
        'if i == 0 or j == 0': _if_border,
        'f[i][j] = 1': '边界上的 1 只能组成 ==1×1== 的小正方形：`f[{i}][{j}] = 1`',
        'f[i][j] = min(': _assign,
        'res = max': lambda S, B, r: (f'`res = max({B.res}, {S.f[S.i][S.j]})` = =={S.res}==' if S.res != B.res
                                      else f'`res` 仍是 `{S.res}`'),
        'return res * res': '最大边长 `{res}` → 面积 `{res} × {res}` = =={ret}==',
    },
    cards=dict(
        one_liner='三个方向（左、上、左上）能到多远，取最小值再加一',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=["在由 `'0'` 和 `'1'` 组成的二维矩阵内，找到==只包含 '1'== 的最大正方形，返回面积",
                 '示例：4×5 的矩阵中最大全 1 正方形边长为 2 → 返回 `4`',
                 '本视频：3×3 矩阵 → `4`'],
        quote='……换言之，就可以通过==min(f[i - 1][j]，f[i][j - 1]，f[i - 1][j - 1])==来判断当前以matrix[i][j]为右下角的正方形能到达多远',
        quote_src='—— yiduobo 题解',
        idea=["情况 1：`matrix[i][j] = '0'` → `f[i][j] = 0`",
              "情况 2：是 `'1'` 且在第 0 行或第 0 列 → `f[i][j] = 1`",
              '情况 3：`f[i][j] = min(左, 上, 左上) + 1`，顺手更新 `res`'],
        result='最大边长 `res = 2` → 面积 `4` ✓',
        summary=['时间 `O(mn)`；原文提到可以用==滚动数组==把空间降到 `O(n)`，这里图方便用了二维',
                 '边界单独处理，所以 `f` 不用多开一行一列（对比灵神的哨兵写法）',
                 '易错：`res` 是边长，返回 `res * res`',
                 '原文为 Python 2 风格，仅删去 docstring，代码未改'],
    ),
)
