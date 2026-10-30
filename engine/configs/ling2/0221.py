M = [["1", "1", "0", "1"],
     ["1", "1", "1", "1"],
     ["0", "1", "1", "1"]]


def _live(S):
    return 'j' in S and 'i' in S and S.get('_line') in (6, 7, 8)


def _mat_color(S, r, c, v):
    # 赋值那一步：把刚算出的正方形在 matrix 上涂绿
    if S.get('_line') == 8:
        i, j = S['i'], S['j']
        k = S['f'][i + 1][j + 1]
        if i - k < r <= i and j - k < c <= j:
            return 'green'
    return 'blue' if v == '1' else None


def _f_color(S, r, c, v):
    if not _live(S):
        if S.get('_line') == 9 and v == max(map(max, S['f'])) and v > 0:
            return 'green'
        return None
    i, j = S['i'], S['j']
    if S['_line'] in (7, 8) and S['ch'] == '1' and (r, c) in ((i, j), (i, j + 1), (i + 1, j)):
        nb = (S['f'][i][j], S['f'][i][j + 1], S['f'][i + 1][j])
        return 'cyan' if v == min(nb) else 'purple'
    return None


def _formula(S):
    if not _live(S):
        if S.get('_line') == 9:
            mx = max(map(max, S['f']))
            return f'`f` 中最大边长 `{mx}` → 面积 `{mx}² = {mx * mx}`'
        return '`f[i+1][j+1]`：右下角在 `(i, j)` 的全 1 正方形的==最大边长=='
    i, j, f = S['i'], S['j'], S['f']
    if S['ch'] != '1':
        return f"`matrix[{i}][{j}] = '0'` → `f[{i + 1}][{j + 1}] = 0`"
    a, b, c = f[i][j], f[i][j + 1], f[i + 1][j]
    return (f"`f[{i + 1}][{j + 1}] = min(左上 {a}, 上 {b}, 左 {c}) + 1` = =={min(a, b, c) + 1}==")


def _if(S, B, ret):
    if S.ch == '1':
        return f"`matrix[{S.i}][{S.j}] = '1'` → 看==左上、上、左==三个正方形"
    return f"`matrix[{S.i}][{S.j}] = '0'`：不可能是全 1 正方形的右下角，`f` 保持 0"


def _assign(S, B, ret):
    i, j, f = S.i, S.j, S.f
    a, b, c = f[i][j], f[i][j + 1], f[i + 1][j]
    v = f[i + 1][j + 1]
    head = f'`f[{i + 1}][{j + 1}] = min({a}, {b}, {c}) + 1 = {v}`'
    if min(a, b, c) == 0:
        return head + '：邻居里有 0 → 只能是 ==1×1== 的正方形'
    if a == b == c:
        return head + f'：三个方向都有边长 {a} 的正方形 → ==扩展成 {v}×{v}=='
    return head + f'：==被最小的 {min(a, b, c)} 卡住== → 边长 {v}'


CONFIG = dict(
    num=221, title='最大正方形', difficulty='Medium', category='多维动态规划',
    author='灵茶山艾府', technique='二维 DP · 左上/上/左取 min 加一',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        m, n = len(matrix), len(matrix[0])
        f = [[0] * (n + 1) for _ in range(m + 1)]
        for i, row in enumerate(matrix):
            for j, ch in enumerate(row):
                if ch == '1':
                    f[i + 1][j + 1] = min(f[i][j], f[i][j + 1], f[i + 1][j]) + 1
        return max(map(max, f)) ** 2
''',
    call=f'Solution().maximalSquare({M})',
    expect=4,
    views=[
        dict(type='grid', var='matrix', label='matrix（黄框 = (i, j)，蓝 = 1，绿 = 刚算出的正方形）', cell=74, h=290,
             color=_mat_color, cursors=[('i', 'j', 'yellow')],
             rows=[0, 1, 2], cols=[0, 1, 2, 3]),
        dict(type='text', fn=_formula, h=60, size=25),
        dict(type='grid', var='f', label='f（第 0 行/列是哨兵 0；黄框 = f[i+1][j+1]，紫/青 = 三个邻居，青 = 最小）', cell=62, h=330,
             color=_f_color, cursors=[('i + 1', 'j + 1', 'yellow')],
             rows=[0, 1, 2, 3], cols=[0, 1, 2, 3, 4]),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('ch', 'ch')],
    skip=['for j, ch in'],
    captions={
        'm, n = len': '`m = {m}` 行，`n = {n}` 列',
        'f = [[0]': '`f` 在最上边加一行 0、最左边加一列 0：==避免 i-1、j-1 出现负数下标==',
        'for i, row in': lambda S, B, r: (f"第 `i = {S.i}` 行：`{''.join(S.row)}`" if 'i' not in B or S.i != B.i
                                          else '所有行处理完毕'),
        'for j, ch in': lambda S, B, r: (f"看 `matrix[{S.i}][{S.j}] = '{S.ch}'`" if 'j' not in B or S.j != B.j or S.i != B.i
                                         else f'第 {S.i} 行处理完'),
        "if ch == '1'": _if,
        'f[i + 1][j + 1] = min': _assign,
        'return max': lambda S, B, r: f'`f` 的最大值是最大边长 `{int(round(r ** 0.5))}`，==面积要平方==：返回 `{r}`',
    },
    cards=dict(
        one_liner='右下角能扩多大，取决于左上、上、左三个正方形中最小的那个',
        complexity='时间 `O(mn)`，空间 `O(mn)`（可优化到 `O(n)`）',
        problem=["在由 `'0'` 和 `'1'` 组成的二维矩阵内，找到==只包含 '1'== 的最大正方形，返回面积",
                 '示例：4×5 的矩阵中最大全 1 正方形边长为 2 → 返回 `4`',
                 '本视频：3×4 矩阵，答案也是 `4`'],
        quote='定义 `f[i][j]` 为右下角在 `(i,j)` 的全 1 正方形的最大边长。……为避免出现负数下标，可以==在 f 矩阵的最上边添加一行 0，最左边添加一列 0==。',
        quote_src='—— 灵茶山艾府题解「方法一：动态规划」',
        idea=["`matrix[i][j] = '0'`：`f` 为 0",
              "`'1'`：`f[i+1][j+1] = min(f[i][j], f[i][j+1], f[i+1][j]) + 1`",
              '只有 `f` 的下标加一，==matrix 的下标不用变==；答案是 `f` 最大值的平方'],
        result='最大边长 2 → 面积 `4` ✓',
        summary=['时间 `O(mn)`；空间可以像 1143 题那样压成一维 `O(n)`',
                 '易错：DP 求的是==边长==，返回前要平方',
                 '易错：`f` 多了一行一列，下标 +1，但 `matrix[i][j]` 不用 +1',
                 '方法二：逐行算柱高，套用 84 题单调栈，正方形边长取 `min(高, 宽)`'],
    ),
)
