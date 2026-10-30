GRID = [[1, -2, 3], [2, -1, -3], [-2, 0, 4]]

# 每一行用到的“上一步”：(表名, [(di, dj), ...])
DEPS = {14: ('f', [(0, -1)]), 16: ('f', [(-1, 0)]),
        18: ('f', [(0, -1), (-1, 0)]), 19: ('g', [(0, -1), (-1, 0)]),
        21: ('g', [(0, -1), (-1, 0)]), 22: ('f', [(0, -1), (-1, 0)])}


def _dep_color(name):
    def color(S, r, c, v):
        d = DEPS.get(S.get('_line'))
        if d and d[0] == name and (r - S['i'], c - S['j']) in d[1]:
            cross = S['_line'] in (21, 22)
            return 'pink' if cross else 'blue'
        return None
    return color


def pair_view(cv, S, B, box, T):
    """f（最大）和 g（最小）左右并排；蓝 = 同表转移用到的格，粉 = 交叉转移用到的格，黄框 = 当前格"""
    x0, y0, x1, y1 = box
    half = (x1 - x0) / 2
    for k, (name, title) in enumerate((('f', 'f：最大乘积'), ('g', 'g：最小乘积'))):
        bx0 = x0 + k * half
        cv.text((bx0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
        tb = S.get(name)
        if tb is None:
            cv.text((bx0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
            continue
        m, n = len(tb), len(tb[0])
        cw = min(96, (half - 60) / n, (y1 - y0 - 60) / m)
        sx = bx0 + (half - cw * n) / 2
        sy = y0 + 48
        colf = _dep_color(name)
        btb = B.get(name)
        for r in range(m):
            for c in range(n):
                v = tb[r][c]
                X, Y = sx + c * cw, sy + r * cw
                cc = colf(S, r, c, v) if 'i' in S else None
                cur = 'i' in S and (r, c) == (S['i'], S['j'])
                changed = btb is not None and btb[r][c] != v
                fill = T[cc] if cc else T['panel2']
                oc, ow = (T['yellow'], 4) if (cur or changed) else (T['border'], 1)
                cv.rect((X + 3, Y + 3, X + cw - 3, Y + cw - 3), fill=fill, outline=oc, width=ow, r=8)
                cv.text((X + cw / 2, Y + cw / 2), '·' if v is None else str(v), 30,
                        T['bg'] if cc else (T['dim'] if v is None else T['text']), anchor='mm', bold=True, mono=True)


def _formula(S):
    line = S.get('_line', 0)
    if 'j' not in S:
        return '`f[i][j]` = 到 `(i,j)` 的==最大==乘积，`g[i][j]` = ==最小==乘积'
    i, j = S['i'], S['j']
    x = GRID[i][j]
    if line in (18, 19):
        return f"`grid[{i}][{j}] = {x} > 0`：最大 × 正 = 最大，最小 × 正 = 最小（蓝 = 用到的格）"
    if line in (21, 22):
        return f"`grid[{i}][{j}] = {x} < 0`：==最小×负 → 最大==，最大×负 → 最小（粉 = 交叉使用）"
    if line == 24:
        return f"`grid[{i}][{j}] = 0`：怎么走乘积都是 0"
    return f"第一行 / 第一列：只有一条路可走，`f = g`"


def _cap_f_pos(S, B, ret):
    i, j = S.i, S.j
    a, b = S.f[i][j - 1], S.f[i - 1][j]
    return f'`{GRID[i][j]} > 0`：希望上一步==尽可能大== → `f = max({a}, {b}) × {GRID[i][j]} = {S.f[i][j]}`'


def _cap_g_pos(S, B, ret):
    i, j = S.i, S.j
    a, b = S.g[i][j - 1], S.g[i - 1][j]
    return f'同理最小：`g = min({a}, {b}) × {GRID[i][j]} = {S.g[i][j]}`'


def _cap_f_neg(S, B, ret):
    i, j = S.i, S.j
    a, b = S.g[i][j - 1], S.g[i - 1][j]
    return f'`{GRID[i][j]} < 0`：要最大，就希望上一步是==负数且尽可能小== → `f = min(g…) = min({a}, {b}) × {GRID[i][j]} = {S.f[i][j]}`'


def _cap_g_neg(S, B, ret):
    i, j = S.i, S.j
    a, b = S.f[i][j - 1], S.f[i - 1][j]
    return f'反过来，最小来自上一步的最大：`g = max({a}, {b}) × {GRID[i][j]} = {S.g[i][j]}`'


CONFIG = dict(
    num=1594, title='矩阵的最大非负积', difficulty='Medium', category='多维动态规划',
    author='yiduobo', technique='f 记最大、g 记最小，按 grid 的正负分类讨论',
    tags=['字节30天'],
    code='''
class Solution(object):
    def maxProductPath(self, grid):
        m = len(grid)
        n = len(grid[0])
        f = [[None] * n for _ in range(m)]
        g = [[None] * n for _ in range(m)]

        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        f[i][j] = g[i][j] = grid[i][j]
                    else:
                        f[i][j] = g[i][j] = f[i][j - 1] * grid[i][j]
                elif j == 0:
                    f[i][j] = g[i][j] = f[i - 1][j] * grid[i][j]
                elif grid[i][j] > 0:
                    f[i][j] = max(f[i][j - 1], f[i - 1][j]) * grid[i][j]
                    g[i][j] = min(g[i][j - 1], g[i - 1][j]) * grid[i][j]
                elif grid[i][j] < 0:
                    f[i][j] = min(g[i][j - 1], g[i - 1][j]) * grid[i][j]
                    g[i][j] = max(f[i][j - 1], f[i - 1][j]) * grid[i][j]
                else:
                    f[i][j] = g[i][j] = 0

        if f[-1][-1] < 0:
            return -1

        return f[-1][-1] % (10 ** 9 + 7)
''',
    call=f'Solution().maxProductPath({GRID})',
    expect=72,
    views=[
        dict(type='text', fn=_formula, size=26, h=70),
        dict(type='grid', var='grid', label='grid（黄框 = 当前格）', cursors=[('i', 'j', 'yellow')], cell=64, h=230),
        dict(type='custom', draw=pair_view, h=330),
    ],
    watch=[('i', 'i'), ('j', 'j'), ('grid[i][j]', 'grid[i][j]', 'yellow'),
           ('f[i][j]', 'f[i][j]', 'green'), ('g[i][j]', 'g[i][j]', 'pink')],
    captions={
        'm = len(grid)': '`m = {m}` 行',
        'n = len(grid[0])': '`n = {n}` 列',
        'f = [[None]': '`f[i][j]`：以 `(i,j)` 结尾的路径的==最大==乘积',
        'g = [[None]': '`g[i][j]`：以 `(i,j)` 结尾的路径的==最小==乘积（为负数格子准备）',
        'f[i][j] = g[i][j] = grid[i][j]': '起点：`f = g = grid[0][0] = {f[0][0]}`',
        'f[i][j] = g[i][j] = f[i][j - 1]': '第一行只能从左边来，只有一条路：`f = g = {f[i][j - 1]} × {grid[i][j]} = {f[i][j]}`',
        'f[i][j] = g[i][j] = f[i - 1][j]': '第一列只能从上边来：`f = g = {f[i - 1][j]} × {grid[i][j]} = {f[i][j]}`',
        'elif grid[i][j] > 0': lambda S, B, r: (f'`grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]} > 0` → 情况 1'
                                               if S.grid[S.i][S.j] > 0 else f'`{S.grid[S.i][S.j]}` 不是正数'),
        'f[i][j] = max(f[i][j - 1]': _cap_f_pos,
        'g[i][j] = min(g[i][j - 1]': _cap_g_pos,
        'elif grid[i][j] < 0': lambda S, B, r: (f'`grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]} < 0` → 情况 3：f、g ==交叉转移=='
                                               if S.grid[S.i][S.j] < 0 else f'`grid[{S.i}][{S.j}] = 0` → 情况 2'),
        'f[i][j] = min(g[i][j - 1]': _cap_f_neg,
        'g[i][j] = max(f[i][j - 1]': _cap_g_neg,
        'f[i][j] = g[i][j] = 0': '`grid[i][j] = 0`：无论怎么走 `f = g = 0`',
        'if f[-1][-1] < 0': lambda S, B, r: (f'`f[-1][-1] = {S.f[-1][-1]} ≥ 0`，有非负积' if S.f[-1][-1] >= 0
                                            else '最大积是负数 → 返回 -1'),
        'return f[-1][-1] %': '返回 `{f[-1][-1]} % (10^9 + 7)` = =={ret}==',
    },
    skip=['for i in range(m)', 'for j in range(n)', 'if i == 0:', 'if j == 0:', 'elif j == 0:'],
    cards=dict(
        one_liner='f 记最大、g 记最小；格子为负时，最大来自上一步的最小',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m × n` 矩阵 `grid`，从左上角出发，每步只能==向右或向下==，走到右下角',
                 '路径的积 = 路径上所有数的乘积；返回==最大非负积==模 `10^9+7`，最大积为负数返回 `-1`',
                 '示例：`[[1,-2,1],[1,-2,1],[3,-4,1]]` → `8`',
                 '本视频：`[[1,-2,3],[2,-1,-3],[-2,0,4]]` → `72`（`1×(-2)×3×(-3)×4`）'],
        quote='若grid[i][j]为负数，那么此时照搬上面转移方程得到的==反而是以第i行第j列结尾的路径的最小乘积==……可以记这个最小值为g[i][j]。',
        quote_src='—— yiduobo 知乎题解',
        idea=['没有负数时：`f[i][j] = max(左, 上) × grid[i][j]`',
              '`grid > 0`：f 取 f 的最大、g 取 g 的最小；`grid = 0`：f = g = 0',
              '`grid < 0`：==f 取 g 的最小 × grid，g 取 f 的最大 × grid==（交叉）'],
        result='返回 `72` ✓ 路径 `1 → -2 → 3 → -3 → 4`',
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '易错：负数格子要交叉使用 f、g；0 的格子单独处理',
                 '最后先判断 `f[-1][-1] < 0` 再取模（==不能中途取模==）',
                 '对比灵神：灵神把 `mn·x`、`mx·x` 一起取 min/max，不用按正负分类，写法更统一',
                 '原文为 Python 2 风格：删去了文档字符串，代码未改'],
    ),
)
