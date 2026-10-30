def _pts(S):
    i, j, n = S['i'], S['j'], S['n']
    return [(i, j), (j, n - 1 - i), (n - 1 - i, n - 1 - j), (n - 1 - j, i)]


_COL = ['blue', 'pink', 'green', 'orange']


def _color(S, i, j, v):
    if 'j' not in S:
        return None
    for k, p in enumerate(_pts(S)):
        if p == (i, j):
            return _COL[k]
    return None


def _group(S):
    if 'j' not in S:
        return '转 90°：位置 `(x, y)` 的数去到 `(y, n−1−x)`'
    M = S['matrix']
    (a, b), (c, d), (e, f), (g, h) = _pts(S)
    return (f'==蓝==上 `({a},{b})` → ==粉==右 `({c},{d})` → ==绿==下 `({e},{f})` → ==橙==左 `({g},{h})` → 上')


def _first(S):
    return S['i'] == 0 and S['j'] == 0


def _cap_y1(S, B, ret):
    if _first(S):
        return f'上边的点 `(x1, y1) = ({S["x1"]}, {S["y1"]})`：`x1 = i`；`y1` 从 `i` 到 `n - i - 2`，==排除右上角=='
    return f'上边的点 `(x1, y1) = ({S["x1"]}, {S["y1"]})`'


def _cap_y2(S, B, ret):
    if _first(S):
        return (f'右边的点：它离上边的距离 = 上边点离左边的距离 → `x2 = y1`；'
                f'`y2 = n - 1 - x1` → `({S["x2"]}, {S["y2"]})`')
    return f'右边的点 `(x2, y2) = (y1, n-1-x1) = ({S["x2"]}, {S["y2"]})`'


def _cap_y3(S, B, ret):
    if _first(S):
        return f'下边的点：同样的规律，`x3 = y2`，`y3 = n - 1 - x2` → `({S["x3"]}, {S["y3"]})`'
    return f'下边的点 `(x3, y3) = ({S["x3"]}, {S["y3"]})`'


def _cap_y4(S, B, ret):
    if _first(S):
        return f'左边的点：`x4 = y3`，`y4 = n - 1 - x3` → `({S["x4"]}, {S["y4"]})`。四个点都确定了'
    return f'左边的点 `(x4, y4) = ({S["x4"]}, {S["y4"]})`'


def _cap_tmp(S, B, ret):
    M = S['matrix']
    v = [M[S['x1']][S['y1']], M[S['x2']][S['y2']], M[S['x3']][S['y3']], M[S['x4']][S['y4']]]
    return f'这一组按 `{v[0]} → {v[1]} → {v[2]} → {v[3]} → {v[0]}` 轮换（每个数去下一个数的位置）；先存 `tmp = {S["tmp"]}`'


CONFIG = dict(
    num=48, title='旋转图像', difficulty='Medium', category='矩阵',
    author='yiduobo', technique='一圈一圈转 · 四个数一组轮换',
    code='''
class Solution(object):
    def rotate(self, matrix):
        n = len(matrix)
        for i in range(n // 2):
            for j in range(i, n - i - 1):
                x1 = i
                y1 = j

                x2 = y1
                y2 = n - 1 - x1

                x3 = y2
                y3 = n - 1 - x2

                x4 = y3
                y4 = n - 1 - x3

                tmp = matrix[x1][y1]
                matrix[x1][y1] = matrix[x4][y4]
                matrix[x4][y4] = matrix[x3][y3]
                matrix[x3][y3] = matrix[x2][y2]
                matrix[x2][y2] = tmp
''',
    call='''
mat = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
Solution().rotate(mat)
mat
''',
    expect=[[13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3], [16, 12, 8, 4]],
    views=[
        dict(type='text', h=56, size=27, fn=_group),
        dict(type='grid', var='matrix', cell=112, h=560, color=_color),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('tmp', 'tmp', 'cyan')],
    skip=['x1 = i', 'x2 = y1', 'x3 = y2', 'x4 = y3'],
    captions={
        'n = len': '`n = {n}`：从外往内一圈一圈转，共 `n // 2 = {n // 2}` 圈',
        'for i in range(n // 2)': lambda S, B, ret: ('所有圈都转完了' if B.get('i') == S['i']
                                                     else f'第 `{S["i"]}` 圈：边长 `{S["n"] - 2 * S["i"]}`，每条边取 `{S["n"] - 2 * S["i"] - 1}` 个数'),
        'for j in range(i, n - i - 1)': lambda S, B, ret: (f'第 `{S["i"]}` 圈的上边取完了' if B.get('j') == S['j']
                                                           else f'上边第 `{S["j"] - S["i"] + 1}` 个数 `matrix[{S["i"]}][{S["j"]}]`：开始一组 4 个数的轮换'),
        'y1 = j': _cap_y1,
        'y2 = n - 1 - x1': _cap_y2,
        'y3 = n - 1 - x2': _cap_y3,
        'y4 = n - 1 - x3': _cap_y4,
        'tmp = matrix[x1][y1]': _cap_tmp,
        'matrix[x1][y1] = matrix[x4][y4]': '左边的 `{matrix[x1][y1]}` 搬到上边 `({x1}, {y1})`',
        'matrix[x4][y4] = matrix[x3][y3]': '下边的 `{matrix[x4][y4]}` 搬到左边 `({x4}, {y4})`',
        'matrix[x3][y3] = matrix[x2][y2]': '右边的 `{matrix[x3][y3]}` 搬到下边 `({x3}, {y3})`',
        'matrix[x2][y2] = tmp': '原来上边的 `tmp = {tmp}` 放到右边 `({x2}, {y2})`，==这一组转完==',
    },
    max_steps=60,
    cards=dict(
        one_liner='正方形看成四条等长的边在轮转，对应位置 4 个数一组换位',
        complexity='时间 `O(n²)`，空间 `O(1)`',
        problem=['把 `n × n` 的矩阵==原地==顺时针旋转 90°，不能另开矩阵',
                 '例：4×4 矩阵按行填 `1..16`',
                 '转完后第一行是 `[13,9,5,1]`：原来的第一列倒过来'],
        quote='由于题目保证是正方形，因此可以将其看成是四条等长的边在轮转。……竖着看下来的话正好就是数字轮换的位置，即 1 -> 4 -> 16 -> 13 -> 1',
        quote_src='—— yiduobo 题解',
        idea=['外圈四条边：上 `1 2 3`，右 `4 8 12`，下 `16 15 14`，左 `13 9 5`',
              '每条边==不含最后一个角==，长度 `n−1−2i`，每个角只转一次',
              '同一列上下对齐的 4 个数为一组：`1→4→16→13→1`'],
        before=[],
        after=[dict(heading='坐标怎么推出来', lines=[
            '上边的点：`x1 = i`，`y1` 从 `i` 到 `n−i−2`',
            '右边：离上边的距离 = 上边点离左边的距离 → `x2 = y1`，`y2 = n−1−x1`',
            '下边：`x3 = y2`，`y3 = n−1−x2`；左边：`x4 = y3`，`y4 = n−1−x3`',
            '四次都是同一条规律：==`(x, y)` 转到 `(y, n−1−x)`==']),
        ],
        summary=['时间 `O(n²)`：每个数只搬一次；空间 `O(1)`，只用一个 `tmp`',
                 '圈数 `n // 2`；`n` 为奇数时正中心不用动',
                 '易错：`j` 的上界是 `n−i−1`（不含），多取一个角会被转两次',
                 '原文为 Python 2：`range(n / 2)` 改为 `n // 2`，删去 docstring'],
    ),
)
