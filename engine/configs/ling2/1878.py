GRID = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
Q_LINES = (13, 17, 38, 39, 40, 41)   # 这些步骤里 x / y / k 被查询函数的参数遮住了


def _diamond_cells(i, j, k):
    if k == 0:
        return {(i, j)}
    cells = set()
    for t in range(k + 1):
        cells |= {(i - k + t, j + t), (i + t, j + k - t), (i + k - t, j - t), (i - t, j - k + t)}
    return cells


def _diamond_sum(g, i, j, k):
    return sum(g[a][b] for a, b in _diamond_cells(i, j, k))


def _top3(vals):
    x = y = z = 0
    for v in vals:
        if v > x:
            x, y, z = v, x, y
        elif x > v > y:
            y, z = v, y
        elif y > v > z:
            z = v
    return x, y, z


def _top3_now(S):
    """在查询函数里 x、y 被参数遮住：按枚举顺序重新模拟一遍得到当前的前三名"""
    if S.get('_line') not in Q_LINES:
        return S.get('x'), S.get('y'), S.get('z')
    g, ci, cj = S['grid'], S['i'], S['j']
    m, n = len(g), len(g[0])
    vals = []
    for i in range(m):
        for j in range(n):
            vals.append(g[i][j])
            if (i, j) == (ci, cj):
                return _top3(vals)
            for k in range(1, min(i, m - 1 - i, j, n - 1 - j) + 1):
                vals.append(_diamond_sum(g, i, j, k))
    return _top3(vals)


def _segment(S):
    """当前查询覆盖的格子、用到的两个前缀和下标"""
    line = S.get('_line')
    I = S.get('_inner') or {}
    if line in (13, 38, 39) and {'x', 'y', 'k'} <= set(I):
        x, y, k = I['x'], I['y'], I['k']
        return 'diag', [(x + t, y + t) for t in range(k)], (x + k, y + k), (x, y)
    if line in (17, 40, 41) and {'x', 'y', 'k'} <= set(I):
        x, y, k = I['x'], I['y'], I['k']
        return 'anti', [(x + t, y - t) for t in range(k)], (x + k, y + 1 - k), (x, y + 1)
    return None


def _table(cv, T, X, Y, tab, cell, title, hi_plus=None, hi_minus=None, color=None):
    cv.text((X, Y), title, 21, color or T['muted'], bold=True)
    Y += 30
    for r, row in enumerate(tab):
        for c, v in enumerate(row):
            fill, tc = T['panel2'], T['text']
            if hi_plus == (r, c):
                fill, tc = T['green'], T['bg']
            elif hi_minus == (r, c):
                fill, tc = T['red'], T['bg']
            cv.rect((X + c * cell + 2, Y + r * cell + 2, X + (c + 1) * cell - 2, Y + (r + 1) * cell - 2), fill=fill, r=6,
                    outline=T['border'])
            cv.text((X + c * cell + cell / 2, Y + r * cell + cell / 2), v, 20, tc, anchor='mm', bold=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    g = S.get('grid')
    if g is None:
        return
    m, n = len(g), len(g[0])
    seg = _segment(S)
    line = S.get('_line')
    cv.text((x0 + 18, y0 + 4), 'grid（黄框 = 菱形中心，橙 = 菱形边界，绿 = 正在求和的一条边）', 22, T['muted'], bold=True)
    cell = 84
    gx, gy = x0 + 40, y0 + 44
    ci, cj = S.get('i'), S.get('j')
    in_enum = isinstance(ci, int) and line is not None and line >= 24 or line in Q_LINES
    K = S.get('mx', 0) if (line in Q_LINES or line == 42 or (line in (24, 26, 28) and S.get('v', 0) > 9)) else 0
    dia = _diamond_cells(ci, cj, K) if in_enum and isinstance(ci, int) and K else set()
    segc = set(seg[1]) if seg else set()
    for r in range(m):
        for c in range(n):
            X, Y = gx + c * cell, gy + r * cell
            fill, tc = T['panel2'], T['text']
            if (r, c) in segc:
                fill, tc = T['green'], T['bg']
            elif (r, c) in dia:
                fill, tc = T['orange'], T['bg']
            cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=fill, r=8, outline=T['border'])
            cv.text((X + cell / 2, Y + cell / 2), g[r][c], 30, tc, anchor='mm', bold=True)
    if in_enum and isinstance(ci, int) and isinstance(cj, int) and 'mx' in S or line in (24, 26, 28, 33):
        if isinstance(ci, int) and isinstance(cj, int) and 0 <= ci < m and 0 <= cj < n and line not in (19, 44, 45, 46, 47):
            X, Y = gx + cj * cell, gy + ci * cell
            cv.rect((X, Y, X + cell, Y + cell), outline=T['yellow'], width=4, r=10)
    # 前三名
    tx = gx + n * cell + 60
    t3 = _top3_now(S) if 'x' in S else None
    cv.text((tx, gy), '当前前三名（互不相同）', 22, T['muted'], bold=True)
    if t3 and all(isinstance(t, int) for t in t3):
        for k, (nm, val) in enumerate(zip(('x 最大', 'y 次大', 'z 第三'), t3)):
            Y = gy + 40 + k * 62
            cv.rect((tx, Y, tx + 260, Y + 52), fill=T['panel2'], r=10, outline=T['border'])
            cv.text((tx + 16, Y + 26), nm, 22, T['muted'], anchor='lm')
            cv.text((tx + 244, Y + 26), val, 28, T['green'], anchor='rm', bold=True)
    # 两张前缀和表
    if 'diag_sum' not in S:
        return
    ty = gy + m * cell + 24
    tcell = 50
    _table(cv, T, x0 + 40, ty, S['diag_sum'], tcell, 'diag_sum（↘ 前缀和）', *(seg[2:] if seg and seg[0] == 'diag' else (None, None)),
           color=T['cyan'] if seg and seg[0] == 'diag' else None)
    if 'anti_sum' in S:
        _table(cv, T, x0 + 40 + (n + 1) * tcell + 70, ty, S['anti_sum'], tcell, 'anti_sum（↙ 前缀和）',
               *(seg[2:] if seg and seg[0] == 'anti' else (None, None)), color=T['cyan'] if seg and seg[0] == 'anti' else None)


def _cap_assign(kind):
    def f(S, B, ret):
        if kind == 'x':
            return f'`{S.v}` 比最大值 `{B.x}` 还大 → 依次后移：`x, y, z = {S.x}, {S.y}, {S.z}`'
        if kind == 'y':
            return f'`{S.x} > {S.v} > {B.y}` → 成为次大：`y, z = {S.y}, {S.z}`'
        return f'`{S.y} > {S.v} > {B.z}` → 成为第三大：`z = {S.z}`'
    return f


def _cap_q(name, desc):
    def f(S, B, ret):
        I = S.get('_inner') or {}
        return f'菱形=={name}==的边：{desc(B)}，`{"query_diagonal" if "↘" in desc(B) else "query_anti_diagonal"}({I.get("x")}, {I.get("y")}, {I.get("k")})`'
    return f


CONFIG = dict(
    num=1878, title='矩阵中最大的三个菱形和', difficulty='Medium', category='矩阵',
    author='灵茶山艾府', technique='斜向前缀和 · 枚举中心和半径',
    tags=['字节30天'],
    code='''
class Solution:
    def getBiggestThree(self, grid: List[List[int]]) -> List[int]:
        m, n = len(grid), len(grid[0])
        diag_sum = [[0] * (n + 1) for _ in range(m + 1)]  # ↘ 前缀和
        anti_sum = [[0] * (n + 1) for _ in range(m + 1)]  # ↙ 前缀和
        for i, row in enumerate(grid):
            for j, v in enumerate(row):
                diag_sum[i + 1][j + 1] = diag_sum[i][j] + v
                anti_sum[i + 1][j] = anti_sum[i][j + 1] + v

        # 从 (x,y) 开始，向 ↘，连续 k 个数的和
        def query_diagonal(x: int, y: int, k: int) -> int:
            return diag_sum[x + k][y + k] - diag_sum[x][y]

        # 从 (x,y) 开始，向 ↙，连续 k 个数的和
        def query_anti_diagonal(x: int, y: int, k: int) -> int:
            return anti_sum[x + k][y + 1 - k] - anti_sum[x][y + 1]

        x = y = z = 0  # 最大，次大，第三大

        def update(v: int) -> None:
            nonlocal x, y, z
            if v > x:
                x, y, z = v, x, y
            elif x > v > y:
                y, z = v, y
            elif y > v > z:
                z = v

        # 枚举菱形正中心 (i,j)
        for i, row in enumerate(grid):
            for j, v in enumerate(row):
                update(v)  # 一个数也算菱形
                # 枚举菱形顶点到正中心的距离 k，注意菱形顶点不能出界
                # i-k >= 0 且 i+k <= m-1，所以 k <= min(i, m-1-i)，对于 j 同理
                mx = min(i, m - 1 - i, j, n - 1 - j)
                for k in range(1, mx + 1):
                    a = query_diagonal(i - k, j, k)                   # 菱形右上的边
                    b = query_diagonal(i, j - k, k)                   # 菱形左下的边
                    c = query_anti_diagonal(i - k + 1, j - 1, k - 1)  # 菱形左上的边
                    d = query_anti_diagonal(i, j + k, k + 1)          # 菱形右下的边
                    update(a + b + c + d)

        ans = [x, y, z]
        while ans[-1] == 0:  # 不同的和少于三个
            ans.pop()
        return ans
''',
    call=f'Solution().getBiggestThree({GRID})',
    expect=[20, 9, 8],
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'yellow'), ('mx', 'mx'),
           ('a,b,c,d', lambda S: (S['a'], S['b'], S['c'], S['d']) if all(t in S for t in 'abcd') else None)],
    captions={
        'm, n = len': '`m = {m}` 行，`n = {n}` 列',
        'diag_sum = [[0]': '`diag_sum[i+1][j+1]`：从上边或左边出发，==向 ↘== 走到 `(i,j)` 的元素和',
        'anti_sum = [[0]': '`anti_sum[i+1][j]`：从上边或右边出发，==向 ↙== 走到 `(i,j)` 的元素和',
        'x = y = z = 0': '两张表递推建好：`diag_sum[i+1][j+1] = diag_sum[i][j] + v`（↙ 同理）；`x, y, z` 记最大、次大、第三大',
        'update(v)  #': lambda S, B, ret: f'中心 `({B.i},{B.j})`：==一个数也算菱形==（面积为 0）→ `update({B.v})`',
        'x, y, z = v, x, y': _cap_assign('x'),
        'y, z = v, y': _cap_assign('y'),
        '                z = v': _cap_assign('z'),
        'mx = min': lambda S, B, ret: (f'`mx = min({S.i}, {S.m - 1 - S.i}, {S.j}, {S.n - 1 - S.j}) = 0`：中心在边上，再大的菱形顶点会出界'
                                       if S.mx == 0 else
                                       f'`mx = {S.mx}`：顶点到中心的距离 `k` 可以取 `1..{S.mx}`，四个顶点都不出界'),
        'a = query_diagonal': lambda S, B, ret: f'菱形==右上==的边：从上顶点 `({B.i - B.k},{B.j})` 向 ↘ 连续 `{B.k}` 个数',
        'b = query_diagonal': lambda S, B, ret: f'菱形==左下==的边：从左顶点 `({B.i},{B.j - B.k})` 向 ↘ 连续 `{B.k}` 个数',
        'c = query_anti_diagonal': lambda S, B, ret: (f'菱形==左上==的边（两端顶点已被别的边算过）：从 `({B.i - B.k + 1},{B.j - 1})` 向 ↙ 连续 `{B.k - 1}` 个'
                                                      + ('，即 ==0 个==' if B.k == 1 else '')),
        'd = query_anti_diagonal': lambda S, B, ret: f'菱形==右下==的边：从右顶点 `({B.i},{B.j + B.k})` 向 ↙ 连续 `{B.k + 1}` 个（含下顶点）',
        'return diag_sum[x + k]': lambda S, B, ret: (
            f'两个前缀和之差：`diag_sum[{S.x + S.k}][{S.y + S.k}] − diag_sum[{S.x}][{S.y}]` = '
            f'`{S.diag_sum[S.x + S.k][S.y + S.k]} − {S.diag_sum[S.x][S.y]}` = =={ret}=='),
        'return anti_sum[x + k]': lambda S, B, ret: (
            f'两个前缀和之差：`anti_sum[{S.x + S.k}][{S.y + 1 - S.k}] − anti_sum[{S.x}][{S.y + 1}]` = '
            f'`{S.anti_sum[S.x + S.k][S.y + 1 - S.k]} − {S.anti_sum[S.x][S.y + 1]}` = =={ret}=='),
        'update(a + b + c + d)': lambda S, B, ret: f'菱形和 = `{B.a} + {B.b} + {B.c} + {B.d}` = =={B.a + B.b + B.c + B.d}== → `update`',
        'ans = [x, y, z]': '`ans = [{x}, {y}, {z}]`',
        'while ans[-1] == 0': lambda S, B, ret: ('末尾是 0：不同的和不足三个，弹掉' if B.ans[-1] == 0 else '三个都不是 0 → 不用删'),
        'return ans': '返回 `{ret}`',
    },
    skip=[6, 7, 8, 9, 23, 25, 27, 31, 32, 37],
    max_steps=60,
    cards=dict(
        one_liner='枚举菱形中心和半径，四条边用斜向前缀和 O(1) 求出',
        complexity='时间 `O(mn·min(m,n))`，空间 `O(mn)`',
        problem=['菱形和：正方形旋转 45° 后，==边界==上格子的元素和（面积为 0 的单个格子也算）',
                 '按降序返回 grid 中==最大的三个互不相同==的菱形和，不足三个就全部返回',
                 '示例：`[[1,2,3],[4,5,6],[7,8,9]]` → `[20,9,8]`'],
        quote='如果确定了菱形的==正中心 (i,j)==，以及菱形==顶点到正中心的距离 k==，就确定了菱形的四个顶点的位置。……可以用==斜向前缀和==加速。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`diag_sum`：↘ 方向的前缀和；`anti_sum`：↙ 方向的前缀和（下标 +1 免特判）',
              '从 `(x,y)` 向 ↘ 连续 k 个数 = `diag_sum[x+k][y+k] − diag_sum[x][y]`',
              '四条边各取一段，顶点不重不漏；`update` 维护互不相同的前三名'],
        result='最大的三个菱形和：`[20, 9, 8]` ✓',
        summary=['时间 `O(mn·min(m,n))`：中心 `mn` 个，半径最多 `min(m,n)/2` 种',
                 '易错：四条边分段要==不重不漏==：左上的边只取中间 `k−1` 个，右下的边取 `k+1` 个',
                 '`update` 里用 `x > v > y` 这样的严格不等式，自动去掉重复的和',
                 '相似题：1895. 最大的幻方'],
    ),
)
