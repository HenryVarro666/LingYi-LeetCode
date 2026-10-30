GRID = [['X', 'Y', '.'], ['Y', '.', '.']]


def _dep(S, which):
    """赋值那几行：当前格黄，依赖的格子蓝（要加的），左上角粉（重叠部分，要减掉）"""
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S['_line'] <= 9:
        return {}
    out = {(i, j): 'yellow'}
    if 17 <= S['_line'] <= 29:
        if i == 0 and j > 0:
            out[(0, j - 1)] = 'blue'
        elif j == 0 and i > 0:
            out[(i - 1, 0)] = 'blue'
        elif i > 0 and j > 0:
            out[(i - 1, j)] = 'blue'
            out[(i, j - 1)] = 'blue'
            out[(i - 1, j - 1)] = 'pink'
    return out


def _tcolor(which):
    def f(S, a, b, v):
        return _dep(S, which).get((a, b))
    return f


def _gcolor(S, a, b, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S['_line'] <= 9:
        return None
    if a <= i and b <= j:
        return 'blue' if (a, b) != (i, j) else None
    return None


def _text(S):
    i, j = S.get('i'), S.get('j')
    if 'x' not in S:
        return '`x[i][j]`、`y[i][j]`：左上角 `(0,0)`、右下角 `(i,j)` 的子矩阵里 X、Y 的个数'
    if i is None or S['_line'] <= 9:
        return '二维前缀和：每个 `(i, j)` 都在前面的结果上推出来'
    ln = S['_line']
    if ln == 10:
        return f"枚举右下角 `({i},{j})`，这一格是 `'{GRID[i][j]}'`"
    if ln <= 15:
        return f"看格子 `grid[{i}][{j}] = '{GRID[i][j]}'`：`delta_x = {S.get('delta_x')}`，`delta_y = {S.get('delta_y')}`"
    if ln >= 31:
        return f"`x = {S['x'][i][j]}`，`y = {S['y'][i][j]}`：" + ('相等且 `x > 0` → 合法' if S['x'][i][j] == S['y'][i][j] and S['x'][i][j] > 0 else '不满足条件')
    if i == 0 and j == 0:
        return '情形 1：只有 `(0,0)` 一个格子，`x = delta_x`'
    if i == 0:
        return '情形 2：第 0 行，在左边一格的基础上加当前格'
    if j == 0:
        return '情形 3：第 0 列，在上面一格的基础上加当前格'
    return '情形 4：`x[i][j] = 上 + 左 − 左上 + delta_x`（蓝 = 加，粉 = 减）'


def _cap_if_x(S, B, r):
    if S.grid[S.i][S.j] == 'X':
        return f"`grid[{S.i}][{S.j}] = 'X'` → 这一格是 X，要 `delta_x = 1`"
    return f"`grid[{S.i}][{S.j}] = '{S.grid[S.i][S.j]}'` 不是 X，看是不是 Y"


def _cap_if_y(S, B, r):
    if S.grid[S.i][S.j] == 'Y':
        return f"`grid[{S.i}][{S.j}] = 'Y'` → 这一格是 Y，要 `delta_y = 1`"
    return f"`grid[{S.i}][{S.j}] = '.'` 两个都不是：`delta_x = delta_y = 0`"


def _four(name):
    def f(S, B, r):
        a = S[name]
        i, j = S.i, S.j
        d = S['delta_' + name]
        return (f'`{name}[{i}][{j}] = {name}[{i-1}][{j}] + {name}[{i}][{j-1}] − {name}[{i-1}][{j-1}] + delta_{name}`'
                f' = `{a[i-1][j]} + {a[i][j-1]} − {a[i-1][j-1]} + {d}` = =={a[i][j]}==')
    return f


def _cap_cmp(S, B, r):
    a, b = S.x[S.i][S.j], S.y[S.i][S.j]
    if a > 0 and a == b:
        return f'`x = y = {a} > 0` → 以 `(0,0)` 为左上角、`({S.i},{S.j})` 为右下角的矩阵==合法=='
    if a == b:
        return '`x = y = 0`：相等但没有 X，==不合法=='
    return f'`x = {a}`，`y = {b}`：个数不等，不合法'


CONFIG = dict(
    num=3212, title='统计 X 和 Y 频数相等的子矩阵数量', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='二维前缀和 · 分四种情形递推',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1673'],
    code='''
class Solution(object):
    def numberOfSubmatrices(self, grid):
        m = len(grid)
        n = len(grid[0])
        x = [[0] * n for _ in range(m)]
        y = [[0] * n for _ in range(m)]
        res = 0

        for i in range(m):
            for j in range(n):
                delta_x, delta_y = 0, 0
                if grid[i][j] == 'X':
                    delta_x = 1
                elif grid[i][j] == 'Y':
                    delta_y = 1

                if i == 0:
                    if j == 0:
                        x[0][0] = delta_x
                        y[0][0] = delta_y
                    else:
                        x[0][j] = x[0][j - 1] + delta_x
                        y[0][j] = y[0][j - 1] + delta_y
                elif j == 0:
                    x[i][0] = x[i - 1][0] + delta_x
                    y[i][0] = y[i - 1][0] + delta_y
                else:
                    x[i][j] = x[i - 1][j] + x[i][j - 1] - x[i - 1][j - 1] + delta_x
                    y[i][j] = y[i - 1][j] + y[i][j - 1] - y[i - 1][j - 1] + delta_y

                if x[i][j] > 0 and x[i][j] == y[i][j]:
                    res += 1

        return res
''',
    call=f'Solution().numberOfSubmatrices({GRID})',
    expect=3,
    views=[
        dict(type='text', fn=_text, size=26, h=70),
        dict(type='grid', var='grid', label='grid（蓝 = 以 (0,0) 为左上角、(i,j) 为右下角的子矩阵）', cell=84, h=250,
             color=_gcolor, cursors=[('i', 'j', 'yellow')]),
        dict(type='table', var='x', label='x[i][j]：子矩阵里 X 的个数', cell=84, h=220, color=_tcolor('x')),
        dict(type='table', var='y', label='y[i][j]：子矩阵里 Y 的个数', cell=84, h=220, color=_tcolor('y')),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('delta_x', 'delta_x', 'blue'), ('delta_y', 'delta_y', 'pink'), ('res', 'res', 'green')],
    max_steps=90,
    skip=['m = len', 'n = len', 'delta_x, delta_y = 0, 0'],
    captions={
        'x = [[0] * n': '`x[i][j]`：`(0,0)` 到 `(i,j)` 的子矩阵里 ==X 的个数==，先全填 0',
        'y = [[0] * n': '`y[i][j]`：同样的子矩阵里 ==Y 的个数==',
        'res = 0': '`res` 统计合法的子矩阵：必须含 `grid[0][0]` → 只会是这种前缀矩阵',
        'for i in range': lambda S, B, r: ('所有行都处理完了' if 'i' in B and B.i == S.i else f'第 `{S.i}` 行：逐个枚举右下角 `(i, j)`'),
        'for j in range': lambda S, B, r: ('这一行的右下角都枚举完了' if 'j' in B and B.j == S.j and B.i == S.i else f'`({S.i}, {S.j})` 作为右下角'),
        "if grid[i][j] == 'X'": _cap_if_x,
        'delta_x = 1': '`delta_x = 1`',
        "elif grid[i][j] == 'Y'": _cap_if_y,
        'delta_y = 1': '`delta_y = 1`',
        17: lambda S, B, r: ('`i = 0`：在第 0 行，没有上一行可以参考' if S.i == 0 else f'`i = {S.i} > 0`：有上一行，接着看 `j`'),
        18: lambda S, B, r: ('`j = 0`：第 0 行第 0 列 → 情形 1，只有这一个格子' if S.j == 0 else f'`j = {S.j} > 0`：左边还有格子 → 情形 2'),
        'x[0][0] = delta_x': '情形 1：`x[0][0] = delta_x = {x[0][0]}`',
        'y[0][0] = delta_y': '`y[0][0] = delta_y = {y[0][0]}`',
        'x[0][j] = x[0][j - 1] + delta_x': '情形 2：左边一格 `x[0][{j-1}] = {x[0][j-1]}`，加上当前格 `{delta_x}` → `x[0][{j}] = {x[0][j]}`',
        'y[0][j] = y[0][j - 1] + delta_y': '`y[0][{j}] = y[0][{j-1}] + {delta_y}` = =={y[0][j]}==',
        24: lambda S, B, r: (f'`i = {S.i} > 0`，`j = 0`：第 0 列 → 情形 3，只能参考上面一格' if S.j == 0 else f'`i = {S.i} > 0`，`j = {S.j} > 0`：上、左、左上都在 → 情形 4'),
        'x[i][0] = x[i - 1][0] + delta_x': '情形 3：上面一格 `x[{i-1}][0] = {x[i-1][0]}`，加上当前格 `{delta_x}` → `x[{i}][0] = {x[i][0]}`',
        'y[i][0] = y[i - 1][0] + delta_y': '`y[{i}][0] = y[{i-1}][0] + {delta_y}` = =={y[i][0]}==',
        'x[i][j] = x[i - 1][j] + x[i][j - 1] - x[i - 1][j - 1] + delta_x': _four('x'),
        'y[i][j] = y[i - 1][j] + y[i][j - 1] - y[i - 1][j - 1] + delta_y': _four('y'),
        'if x[i][j] > 0 and x[i][j] == y[i][j]': _cap_cmp,
        'res += 1': '`res` → =={res}==',
        'return res': '所有右下角都检查完了，答案 =={ret}==',
    },
    cards=dict(
        one_liner='合法子矩阵必含左上角 → 二维前缀和，分四种情形递推',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['二维字符矩阵 `grid`，每格是 `X`、`Y` 或 `.`',
                 '数有多少子矩阵==包含 `grid[0][0]`==、X 和 Y 个数相等、至少含一个 X',
                 '示例：`[["X","Y","."],["Y",".","."]]` → `3`',
                 '三个合法矩阵的右下角分别是 `(0,1)`、`(0,2)`、`(1,0)`'],
        quote='注意到题目要求的子矩阵必须包含grid[0][0]，那么就说明合法子矩阵必然是前缀矩阵，于是可以使用二维前缀和来求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['`x[i][j]`、`y[i][j]`：`(0,0)` 到 `(i,j)` 里 X、Y 的个数',
              '边界分三种：`(0,0)`、第 0 行、第 0 列，只能从一个方向推',
              '一般情形：`x[i][j] = 上 + 左 − 左上 + delta_x`，左上被加了两次，要减掉一次'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '易错：`x[i][j] > 0` 不能漏，全是 `.` 时 `x = y = 0` 也相等',
                 '易错：第 0 行、第 0 列没有 `i-1` / `j-1`，不能走一般公式（会取到负下标）',
                 '原文在 Python 3 下可直接运行，代码未做修改',
                 '对比灵神：灵神用 `ord(c) & 1` 省掉字母判断，还可只存每列计数，空间 `O(n)`'],
    ),
)
