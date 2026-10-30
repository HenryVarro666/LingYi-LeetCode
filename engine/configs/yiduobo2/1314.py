MAT = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
S_LINES = (11, 13, 15, 17)
R_LINES = (28, 30, 32, 34)


def _phase2(S):
    return S.get('x1') is not None and S.get('_line') not in S_LINES


def _mat_color(S, i, j, v):
    if _phase2(S):
        if S['x1'] <= i <= S['x2'] and S['y1'] <= j <= S['y2']:
            return 'green'
        return None
    if S.get('_line') in S_LINES and i <= S['i'] and j <= S['j']:
        return 'cyan'
    return None


def _s_color(S, i, j, v):
    if _phase2(S):
        x1, y1, x2, y2 = S['x1'], S['y1'], S['x2'], S['y2']
        if (i, j) == (x2, y2):
            return 'green'
        if (i, j) in ((x1 - 1, y2), (x2, y1 - 1)):
            return 'pink'
        if (i, j) == (x1 - 1, y1 - 1):
            return 'blue'
        return None
    if S.get('_line') in S_LINES:
        ci, cj = S['i'], S['j']
        if (i, j) in ((ci - 1, cj), (ci, cj - 1)):
            return 'blue'
        if (i, j) == (ci - 1, cj - 1):
            return 'pink'
    return None


def _formula(S):
    ln = S.get('_line')
    if ln in S_LINES:
        i, j, s = S['i'], S['j'], S['s']
        up = s[i - 1][j] if i else 0
        left = s[i][j - 1] if j else 0
        diag = s[i - 1][j - 1] if i and j else 0
        return f'`s[{i}][{j}]` = 上 {up} + 左 {left} − 左上 {diag} + mat {MAT[i][j]} = =={s[i][j]}=='
    if _phase2(S):
        x1, y1, x2, y2, s = S['x1'], S['y1'], S['x2'], S['y2'], S['s']
        a = s[x2][y2]
        b = s[x1 - 1][y2] if x1 else 0
        c = s[x2][y1 - 1] if y1 else 0
        d = s[x1 - 1][y1 - 1] if x1 and y1 else 0
        tail = f' = =={S["res"][S["i"]][S["j"]]}==' if ln in R_LINES else ''
        return f'块和 = 绿 {a} − 粉 {b} − 粉 {c} + 蓝 {d}{tail}'
    return '`s[i][j]` = 以 `(0,0)` 为左上角、`(i,j)` 为右下角的矩形和'


def _cap_s(S, B, ret):
    i, j, s = S.i, S.j, S.s
    ln = S._line
    if ln == 11:
        return f'左上角：`s[0][0] = mat[0][0] = {s[0][0]}`'
    if ln == 13:
        return f'第 0 行没有「上」：`s[0][{j}] = 左 {s[0][j - 1]} + {MAT[0][j]} = {s[0][j]}`'
    if ln == 15:
        return f'第 0 列没有「左」：`s[{i}][0] = 上 {s[i - 1][0]} + {MAT[i][0]} = {s[i][0]}`'
    return (f'上 + 左 把左上那块==加了两次== → 减掉一次：'
            f'`{s[i - 1][j]} + {s[i][j - 1]} − {s[i - 1][j - 1]} + {MAT[i][j]}` = =={s[i][j]}==')


def _cap_box(S, B, ret):
    return (f'以 `({S.i},{S.j})` 为中心、半径 `k = {S.k}` 的方块，裁到矩阵里：'
            f'行 `{S.x1}..{S.x2}`，列 `{S.y1}..{S.y2}`')


def _cap_res(S, B, ret):
    i, j, x1, y1, x2, y2, s = S.i, S.j, S.x1, S.y1, S.x2, S.y2, S.s
    v = S.res[i][j]
    ln = S._line
    if ln == 28:
        return f'方块贴着左上角 → 直接就是前缀和：`res[{i}][{j}] = s[{x2}][{y2}]` = =={v}=='
    if ln == 30:
        return f'贴着上边：只减左边那条 `s[{x2}][{y1 - 1}]`：`{s[x2][y2]} − {s[x2][y1 - 1]}` = =={v}=='
    if ln == 32:
        return f'贴着左边：只减上面那条 `s[{x1 - 1}][{y2}]`：`{s[x2][y2]} − {s[x1 - 1][y2]}` = =={v}=='
    return (f'减上、减左，左上角被==减了两次==再加回来：'
            f'`{s[x2][y2]} − {s[x1 - 1][y2]} − {s[x2][y1 - 1]} + {s[x1 - 1][y1 - 1]}` = =={v}==')


CONFIG = dict(
    num=1314, title='矩阵区域和', difficulty='Medium', category='子串',
    author='yiduobo', technique='二维前缀和 · 容斥求块和',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def matrixBlockSum(self, mat, k):
        m = len(mat)
        n = len(mat[0])
        s = [[0] * n for _ in range(m)]

        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        s[i][j] = mat[i][j]
                    else:
                        s[i][j] = s[i][j - 1] + mat[i][j]
                elif j == 0:
                    s[i][j] = s[i - 1][j] + mat[i][j]
                else:
                    s[i][j] = s[i - 1][j] + s[i][j - 1] - s[i - 1][j - 1] + mat[i][j]

        res = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                x1 = max(0, i - k)
                y1 = max(0, j - k)
                x2 = min(m - 1, i + k)
                y2 = min(n - 1, j + k)
                if x1 == 0:
                    if y1 == 0:
                        res[i][j] = s[x2][y2]
                    else:
                        res[i][j] = s[x2][y2] - s[x2][y1 - 1]
                elif y1 == 0:
                    res[i][j] = s[x2][y2] - s[x1 - 1][y2]
                else:
                    res[i][j] = s[x2][y2] - s[x1 - 1][y2] - s[x2][y1 - 1] + s[x1 - 1][y1 - 1]

        return res
''',
    call=f'Solution().matrixBlockSum({MAT}, 1)',
    expect=[[12, 21, 16], [27, 45, 33], [24, 39, 28]],
    skip=['m = len(mat)', 'for i in range(m)', 'for j in range(n)', 'if i == 0', 'if j == 0', 'elif j == 0',
          'x1 = max', 'y1 = max', 'x2 = min', 'if x1 == 0', 'if y1 == 0', 'elif y1 == 0'],
    views=[
        dict(type='text', fn=_formula, h=75),
        dict(type='grid', var='mat', label='mat（青 = s[i][j] 覆盖的矩形，绿 = 当前要求和的方块）', cell=72, h=290,
             color=_mat_color, cursors=[('i', 'j', 'yellow')]),
        dict(type='grid', var='s', label='s 二维前缀和（绿 + / 粉 − / 蓝 = 用到的项）', cell=72, h=290,
             color=_s_color, cursors=[(lambda S: S['i'] if S.get('_line') in S_LINES else None, 'j', 'yellow')]),
        dict(type='grid', var='res', label='res（答案）', cell=72, h=290,
             cursors=[(lambda S: S['i'] if S.get('_line') in R_LINES else None, 'j', 'yellow')]),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), 'k', ('x1', 'x1'), ('y1', 'y1'), ('x2', 'x2'), ('y2', 'y2')],
    captions={
        'n = len(mat[0])': '矩阵 `{m} × {n}`，`k = {k}`',
        5: '第一步：预处理==二维前缀和== `s`，`s[i][j]` 是 `(0,0)`~`(i,j)` 的矩形和',
        11: _cap_s, 13: _cap_s, 15: _cap_s, 17: _cap_s,
        19: '第二步：==枚举每个格子==，算出以它为中心的方块，用前缀和 `O(1)` 求和',
        'y2 = min': _cap_box,
        28: _cap_res, 30: _cap_res, 32: _cap_res, 34: _cap_res,
        'return res': '每个格子都算完：返回 `res`',
    },
    max_steps=40,
    cards=dict(
        one_liner='先建二维前缀和，再对每个格子用容斥 O(1) 求方块和',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['给 `m × n` 矩阵 `mat` 和整数 `k`，返回同样大小的 `answer`',
                 '`answer[i][j]`：所有满足 `|r−i| ≤ k` 且 `|c−j| ≤ k` 的 `mat[r][c]` 之和（越界的不算）',
                 '示例：`mat = [[1,2,3],[4,5,6],[7,8,9]]`，`k = 1`',
                 '→ `[[12,21,16],[27,45,33],[24,39,28]]`'],
        quote='矩阵区域和问题一般都会转化为==二维前缀和==来进行处理……先预处理出所有的二维前缀和，然后==枚举每个格子==，并计算以这个格子为中心的二维矩阵范围，然后利用前缀和求出矩阵和',
        quote_src='—— yiduobo 知乎题解',
        idea=['`s[i][j]` = 上 + 左 − 左上 + 自己（左上块被加了两次）',
              '方块范围：`x1 = max(0, i−k)`、`x2 = min(m−1, i+k)`，列同理',
              '块和 = `s[x2][y2]` − 上面一条 − 左边一条 + 左上角（被减了两次）',
              '下标从 0 开始，`x1 = 0` 或 `y1 = 0` 时没有上/左那条，要分情况'],
        summary=['时间 `O(mn)`：建前缀和、求每个答案都是 `O(1)`',
                 '易错：容斥的符号——左上角那块要==加回来==',
                 '原文 `s` 不多开一行一列，所以要按 `i == 0`、`j == 0` 分支；多开一圈 0 就能省掉所有特判',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改',
                 '同类题：304 二维区域和检索、1292 正方形最大边长（原文引用的前置题）'],
    ),
)
