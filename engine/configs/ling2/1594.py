GRID = [[1, -2, 1], [1, -2, 1], [3, -4, 1]]


def f_view(cv, S, B, box, T):
    """f[i][j] = (最小乘积, 最大乘积)：每格上面是最大（绿），下面是最小（粉）；蓝/橙框 = 本步用到的上边/左边"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'f[i][j]：上 = 最大乘积 max，下 = 最小乘积 min（蓝框 = 上边，橙框 = 左边）', 24, T['muted'], bold=True)
    f = S.get('f')
    if f is None:
        cv.text((x0 + 18, y0 + 50), '（尚未创建）', 24, T['dim'])
        return
    m, n = len(f), len(f[0])
    cw = min(150, (x1 - x0 - 120) / n, (y1 - y0 - 76) / m)
    sx = x0 + (x1 - x0 - cw * n) / 2
    sy = y0 + 66
    line = S.get('_line')
    i, j = S.get('i'), S.get('j')
    dep = None
    if line == 16:
        dep = (i - 1, j, T['blue'])
    elif line == 20:
        dep = (i, j - 1, T['orange'])
    bf = B.get('f')
    for r in range(m):
        cv.text((sx - 14, sy + r * cw + cw / 2), f'i={r}', 18, T['dim'], anchor='rm', mono=True)
        for c in range(n):
            X, Y = sx + c * cw, sy + r * cw
            v = f[r][c]
            cur = (r, c) == (i, j)
            changed = bf is not None and bf[r][c] != v
            oc, ow = (T['yellow'], 4) if cur else (T['border'], 1)
            if dep and (r, c) == dep[:2]:
                oc, ow = dep[2], 5
            cv.rect((X + 4, Y + 4, X + cw - 4, Y + cw - 4), fill=(52, 46, 24) if changed else T['panel2'],
                    outline=oc, width=ow, r=10)
            if v is None:
                cv.text((X + cw / 2, Y + cw / 2), '·', 30, T['dim'], anchor='mm')
            else:
                cv.text((X + cw / 2, Y + cw * 0.34), str(v[1]), 32, T['green'], anchor='mm', bold=True, mono=True)
                cv.text((X + cw / 2, Y + cw * 0.70), str(v[0]), 26, T['pink'], anchor='mm', bold=True, mono=True)
    for c in range(n):
        cv.text((sx + c * cw + cw / 2, sy - 4), f'j={c}', 18, T['dim'], anchor='mb', mono=True)


def _formula(S):
    line = S.get('_line', 0)
    if 'x' not in S or line < 8:
        return '最后一步从==上边==或==左边==来；乘上负数会让最小变最大 → ==最小、最大都要算=='
    i, j, x = S['i'], S['j'], S['x']
    if line == 16:
        mn, mx = S['mn'], S['mx']
        return f"从上 `({i-1},{j})`：`({mn}, {mx}) × {x}` → 候选 `{mn * x}`、`{mx * x}`"
    if line == 20:
        mn, mx = S['mn'], S['mx']
        return f"从左 `({i},{j-1})`：`({mn}, {mx}) × {x}` → 候选 `{mn * x}`、`{mx * x}`"
    if line == 22:
        return f"`f[{i}][{j}] = (min, max) = {S['f'][i][j]}`"
    return f"当前格 `({i},{j})`，`x = {x}`"


def _cap_up(S, B, ret):
    mn, mx, x = S.mn, S.mx, S.x
    return (f'从上边 `({S.i-1},{S.j})` 来：`{mn}×{x} = {mn*x}`，`{mx}×{x} = {mx*x}` → '
            f'`res_min = {S.res_min}`，`res_max = {S.res_max}`')


def _cap_left(S, B, ret):
    mn, mx, x = S.mn, S.mx, S.x
    merge = '第一行==只能从左边来==' if S.i == 0 else '和上边的结果合并'
    return (f'从左边 `({S.i},{S.j-1})` 来：`{mn}×{x} = {mn*x}`，`{mx}×{x} = {mx*x}`，{merge} → '
            f'`({S.res_min}, {S.res_max})`')


def _cap_set(S, B, ret):
    v = S.f[S.i][S.j]
    tip = '（x < 0：==最小 × 负数 = 最大==，所以必须存最小值）' if S.x < 0 and v[0] != v[1] else ''
    if S.j == 0:
        tip = '（第一列只能从上边来）'
    return f'`f[{S.i}][{S.j}] = {v}`{tip}'


CONFIG = dict(
    num=1594, title='矩阵的最大非负积', difficulty='Medium', category='多维动态规划',
    author='灵茶山艾府', technique='网格图 DP：同时维护最小、最大乘积',
    tags=['字节30天'],
    code='''
class Solution:
    def maxProductPath(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        f = [[None] * n for _ in range(m)]

        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                if i == j == 0:
                    f[0][0] = (x, x)
                    continue

                res_min, res_max = inf, -inf
                if i > 0:
                    mn, mx = f[i - 1][j]
                    res_min = min(mn * x, mx * x)
                    res_max = max(mn * x, mx * x)
                if j > 0:
                    mn, mx = f[i][j - 1]
                    res_min = min(res_min, mn * x, mx * x)
                    res_max = max(res_max, mn * x, mx * x)

                f[i][j] = (res_min, res_max)

        ans = f[-1][-1][1]
        return -1 if ans < 0 else ans % 1_000_000_007
''',
    call=f'Solution().maxProductPath({GRID})',
    expect=8,
    views=[
        dict(type='text', fn=_formula, size=26, h=70),
        dict(type='grid', var='grid', label='grid（黄框 = 当前格 x）', cursors=[('i', 'j', 'yellow')], cell=70, h=230),
        dict(type='custom', draw=f_view, h=330),
    ],
    watch=[('i', 'i'), ('j', 'j'), ('x', 'x', 'yellow'), ('res_min', 'res_min', 'pink'), ('res_max', 'res_max', 'green')],
    captions={
        'm, n = len(grid)': '网格 `{m} × {n}`，每步只能向右或向下',
        'f = [[None]': '`f[i][j]` = 左上角到 `(i,j)` 的 ==(最小乘积, 最大乘积)==，翻译自 `dfs(i,j)`',
        'f[0][0] = (x, x)': '递归边界：起点只有它自己 → `f[0][0] = ({x}, {x})`',
        'res_max = max(mn * x, mx * x)': _cap_up,
        'res_max = max(res_max, mn * x, mx * x)': _cap_left,
        'f[i][j] = (res_min, res_max)': _cap_set,
        'ans = f[-1][-1][1]': '右下角的==最大==乘积：`ans = {ans}`',
        'return -1 if ans < 0': lambda S, B, r: (f'`ans = {S.ans} ≥ 0` → ==算完了再取模==，返回 `{r}`' if S.ans >= 0
                                                 else '`ans < 0`：没有非负积 → 返回 `-1`'),
    },
    skip=['for i, row in enumerate(grid)', 'for j, x in enumerate(row)', 'if i == j == 0', 'continue',
          'res_min, res_max = inf', 'if i > 0', 'if j > 0', 'mn, mx = f[i - 1][j]', 'mn, mx = f[i][j - 1]',
          'res_min = min(mn * x', 'res_min = min(res_min'],
    cards=dict(
        one_liner='负负得正：除了最大乘积，还要记最小乘积',
        complexity='时间 `O(mn)`，空间 `O(mn)`（可优化到 `O(n)`）',
        problem=['`m × n` 矩阵 `grid`，从左上角出发，每步只能==向右或向下==，走到右下角',
                 '路径的积 = 路径上所有数的乘积；返回==最大非负积==模 `10^9+7`，最大积为负数返回 `-1`',
                 '注意：==取余是在得到最大积之后==执行的',
                 '示例：`[[1,-2,1],[1,-2,1],[3,-4,1]]` → `8`（`1×1×(-2)×(-4)×1`）'],
        quote='思路和 152 题是一样的，除了计算最大路径乘积，==还要计算最小路径乘积（因为负负得正）==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i,j)` 返回左上角到 `(i,j)` 的 (最小乘积, 最大乘积)',
              '从上边或左边来：`mn·x`、`mx·x` 里取最小、最大；两种来源再合并',
              '1:1 翻译成递推：`f[i][j]` 就是 `dfs(i,j)`，从左上到右下依次计算'],
        result='返回 `8`：路径 `1 → 1 → -2 → -4 → 1` ✓',
        summary=['时间 `O(mn)`，空间 `O(mn)`；空间优化版用两个一维数组 `f_min`、`f_max`',
                 '易错：==不能中途取模==，否则取模后的大小关系会错（如 `10^9+8` 模完变成 1）',
                 '易错：x 为负时，最大值来自 `mn × x`，所以必须同时维护最小值',
                 '原文共三种写法：记忆化搜索 → 递推（本视频）→ 空间优化'],
    ),
)
