MAT = [[1, 0, 0], [0, 2, 1]]


def _k(S):
    if 'st' not in S:
        return None
    if 'ans' in S:
        inn = S['_inner']
        if inn.get('k1') is None or inn.get('k2') is None:
            return None
        return inn['k1'], inn['k2']
    return S.get('k1', 0), S.get('k2', 0)


def _layer(S):
    k = _k(S)
    if k is None:
        return None
    try:
        return S['st'][k[0]][k[1]]
    except Exception:
        return None


def _layer_label(S):
    k = _k(S)
    if k is None:
        return '二维 ST 表（查询时显示当前用到的那一层）'
    return f'`st[{k[0]}][{k[1]}]`：每格 = 以它为左上角、{1 << k[0]} 行 × {1 << k[1]} 列的子矩阵最大值'


def _mcolor(S, a, b, v):
    if 'ans' not in S or 'x' not in S or S['_inner'].get('x') is None and 'i' not in S:
        return None
    i, j, x = S['i'], S['j'], S['x']
    if x <= 0:
        return None
    da, db = abs(a - i), abs(b - j)
    if (a, b) == (i, j):
        return 'yellow'
    if da <= x and db <= x and not (da == x and db == x):
        return 'red' if v > x else 'cyan'
    return None


def _txt(S):
    if 'ans' not in S:
        return '先预处理二维 ST 表，之后每次查询子矩阵最大值都是 O(1)'
    if 'x' not in S:
        return f'已找到 `ans = {S["ans"]}` 个局部最大值'
    i, j, x = S['i'], S['j'], S['x']
    return f'检查 `({i},{j})`，`x = {x}`：青色 = 要考虑的格子（去掉四个角），红色 = 比 x 大的'


def _qtxt(S):
    r1, c1, r2, c2 = S['_inner'].get('r1'), S['_inner'].get('c1'), S['_inner'].get('r2'), S['_inner'].get('c2')
    return None


CONFIG = dict(
    num=3933, title='矩阵中的局部最大值 II', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='二维 ST 表 + 十字拆成两个矩形',
    tags=['灵神题单·常用数据结构'],
    code='''
class Solution:
    def countLocalMaximums(self, matrix: list[list[int]]) -> int:
        n, m = len(matrix), len(matrix[0])
        wn, wm = n.bit_length(), m.bit_length()

        # st[k1][k2][i][j] 表示左上角在 (i, j)，右下角在 (i+(1<<k1)-1, j+(1<<k2)-1) 的子矩阵最大值
        st = [[[[0] * m for _ in range(n)] for _ in range(wm)] for _ in range(wn)]

        # 初始值
        st[0][0] = matrix

        # 单独计算 k1 = 0
        for k2 in range(1, wm):
            half = 1 << (k2 - 1)
            for i in range(n):
                for j in range(m - (1 << k2) + 1):
                    st[0][k2][i][j] = max(st[0][k2 - 1][i][j], st[0][k2 - 1][i][j + half])

        for k1 in range(1, wn):
            half = 1 << (k1 - 1)
            for k2 in range(wm):
                for i in range(n - (1 << k1) + 1):
                    for j in range(m - (1 << k2) + 1):
                        st[k1][k2][i][j] = max(st[k1 - 1][k2][i][j], st[k1 - 1][k2][i + half][j])

        # 返回子矩阵最大值
        # 左闭右开，行号范围 [r1, r2)，列号范围 [c1, c2)
        def query(r1: int, c1: int, r2: int, c2: int) -> int:
            r1 = max(r1, 0)
            c1 = max(c1, 0)
            r2 = min(r2, n)
            c2 = min(c2, m)
            k1 = (r2 - r1).bit_length() - 1
            k2 = (c2 - c1).bit_length() - 1
            # 视作四个子矩阵的并集
            return max(st[k1][k2][r1][c1],
                       st[k1][k2][r2 - (1 << k1)][c1],
                       st[k1][k2][r1][c2 - (1 << k2)],
                       st[k1][k2][r2 - (1 << k1)][c2 - (1 << k2)])

        ans = 0
        for i, row in enumerate(matrix):
            for j, x in enumerate(row):
                if x > 0 and max(query(i - x, j - x + 1, i + x + 1, j + x), query(i - x + 1, j - x, i + x, j + x + 1)) <= x:
                    ans += 1
        return ans
''',
    call=f'Solution().countLocalMaximums({MAT})',
    expect=2,
    max_steps=64,
    skip=['n, m = len', 'wn, wm =', 'half = ', 'for i in range(n)', 'for j in range(m - (1 << k2)',
          'for i in range(n - (1 << k1)', 'for j in range(m - (1 << k2) + 1)', 'r1 = max', 'c1 = max', 'r2 = min', 'c2 = min', 37, 38, 39, 'k1 = (r2 - r1)',
          'st[0][k2][i][j] =', 'st[k1][k2][i][j] =', 'for k2 in range(wm)', 'st[0][0] = matrix'],
    views=[
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='grid', var='matrix', label='matrix（黄 = 当前格，青 = 考虑的格子，红 = 比 x 大）', cell=96, h=330, color=_mcolor),
        dict(type='text', fn=_layer_label, size=22, h=44),
        dict(type='grid', var=_layer, label='ST 表当前层', cell=70, h=200),
    ],
    watch=[('k1', "S['_inner'].get('k1')"), ('k2', "S['_inner'].get('k2')"), ('x', "S['_inner'].get('x')", 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'st = [[[[': '`st[k1][k2]` 是一张和 matrix 同大小的表：高 `2^k1`、宽 `2^k2` 的子矩阵最大值',
        'for k2 in range(1, wm)': '先填 `k1 = 0`（高 1）这一行：每个宽 `2^{k2}` 的区间最大值 = 两个宽 `2^{k2-1}` 的较大者',
        'for k1 in range(1, wn)': '再填 `k1 ≥ 1`：高 `2^{k1}` 的最大值 = 上下两个高 `2^{k1-1}` 的较大者，`k2` 全部枚举',
        'def query': '查询：用 4 个重叠的 `2^k1 × 2^k2` 矩形覆盖整块，取最大值',
                'k2 = (c2 - c1)': '裁剪后查 `[{r1},{r2}) × [{c1},{c2})`：{r2 - r1} 行 → `k1 = {k1}`，{c2 - c1} 列 → `k2 = {k2}`，矩形大小 `{1 << k1} × {1 << k2}`',
        'return max(st[k1][k2][r1][c1]': lambda S, B, r: ('用四个角上的 `{}×{}` 矩形（可重叠）盖住整块，取最大'.format(1 << S.k1, 1 << S.k2) if r is None else '这块子矩阵的最大值 =={}=='.format(r)),
        'ans = 0': '`ans` 统计局部最大值个数',
        'for i, row in enumerate': lambda S, B, r: ('逐行逐格枚举，每个非零格都要检查' if not ('x' in B and B.i == S.i) else '所有行枚举完了'),
        'for j, x in enumerate(row)': lambda S, B, r: (f'看格子 `({S.i},{S.j})`，`x = {S.x}`' if ('x' not in B or (S.j, S.i) != (B.j, B.i)) else '这一行枚举完了'),
        'if x > 0 and max(': lambda S, B, r: (f'`x = {S.x}`，是 0 → 不是局部最大值（必须非零）' if S.x == 0 else
                                               f'`x = {S.x}`：把“十字”拆成 `{2*S.x+1}×{2*S.x-1}` 和 `{2*S.x-1}×{2*S.x+1}` 两个矩形，各查最大值，都 ≤ x 才是局部最大值'),
        'ans += 1': '十字区域内没有比 `{x}` 更大的 → 局部最大值，`ans` = {ans}',
        'return ans': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='“十字”区域 = 两个矩形的并集，二维 ST 表 O(1) 查最大值',
        complexity='时间 `O(nm log n log m)`，空间 `O(nm log n log m)`',
        problem=['非零格 `(r, c)`，`x = matrix[r][c]`，看周围 `x` 行 `x` 列范围内的格子',
                 '行距、列距都恰好等于 `x` 的四个角要忽略',
                 '没有比 `x` 更大的值，就是局部最大值，数出个数',
                 '本视频：`[[0,1,0],[1,2,0],[0,0,1]]` → `2`'],
        quote='本题不能计入子矩阵的四个角，怎么办？我们可以把蓝色区域视作两个子矩阵的并集。',
        quote_src='—— 灵茶山艾府题解',
        idea=['二维 ST 表：`st[k1][k2][i][j]` 是左上角 `(i,j)`、高 `2^k1`、宽 `2^k2` 的子矩阵最大值',
              '查询用 4 个重叠的矩形覆盖目标区域，重叠不影响“最大值”',
              '去掉四个角：横着的 `(2x+1)×(2x-1)` 加竖着的 `(2x-1)×(2x+1)`，各查一次'],
        after=[dict(heading='另一种写法', lines=['方法二：线段树套 ST 表，上下边界固定时把每列压成最大值',
                                                  '时间 `O(nm(log n + log m))`，空间 `O(nm log m)`'])],
        summary=['预处理 `O(nm log n log m)`，查询 `O(1)`',
                 '查询用左闭右开 `[r1, r2) × [c1, c2)`，先把越界部分裁掉',
                 '易错：`x = 0` 的格子不算局部最大值；矩形要把中心 `x` 行 `x` 列算全',
                 '易错：两个矩形一个收窄行、一个收窄列，别写反'],
    ),
)
