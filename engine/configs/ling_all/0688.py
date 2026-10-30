from fractions import Fraction

_DIRS = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
_RET_LINE = 12  # return 行（代码从 DIRS 起算 1）


def _fr(v):
    if v == 0:
        return '0'
    f = Fraction(v).limit_denominator(1 << 14)
    return str(f.numerator) if f.denominator == 1 else f'{f.numerator}/{f.denominator}'


def _cur(S):
    """(step, i, j, 是否在算某个格子)"""
    if 'step' not in S or 'j' not in S or 'i' not in S:
        return None
    if S.get('_line', 0) not in (10, 11):
        return None
    return S['step'], S['i'], S['j']


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f, n = S['f'], S['n']
    size = n + 4
    cur = _cur(S)
    if cur:
        step = cur[0]
    elif S.get('_line', 0) >= _RET_LINE:
        step = S['k']
    elif 'step' in S:
        step = S['step']
    else:
        step = 0
    layers = [(step - 1, '走 step-1 步（来源）'), (step, '走 step 步（正在算）')] if step >= 1 else [(0, 'f[0]：走 0 步，棋盘内都是 1')]
    gap = 30
    cell = min(66, ((x1 - x0 - 40 - gap) / len(layers) - 36) / size, (y1 - y0 - 120) / size)
    cell = max(cell, 30)
    gw = cell * size
    total = gw * len(layers) + gap * (len(layers) - 1) + 36 * len(layers)
    sx0 = x0 + 20 + ((x1 - x0 - 40) - total) / 2
    srcs = set()
    if cur and cur[0] >= 1:
        srcs = {(cur[1] + dx, cur[2] + dy) for dx, dy in _DIRS}
    for li, (ly, title) in enumerate(layers):
        ox = sx0 + li * (gw + gap + 36) + 36
        oy = y0 + 92
        cv.text((ox + gw / 2, oy - 44), f'f[{ly}]：走 {ly} 步', 24, T['muted'], anchor='mm', bold=True)
        for c in range(size):
            cv.text((ox + c * cell + cell / 2, oy - 6), str(c - 2), 16, T['dim'], anchor='mb', mono=True)
            cv.text((ox - 8, oy + c * cell + cell / 2), str(c - 2), 16, T['dim'], anchor='rm', mono=True)
        for i in range(size):
            for j in range(size):
                v = f[ly][i][j]
                inside = 2 <= i < n + 2 and 2 <= j < n + 2
                X, Y = ox + j * cell, oy + i * cell
                fill = T['panel2'] if inside else (22, 26, 32)
                ol, wd = T['border'], 1
                tc = T['text'] if inside else T['dim']
                if cur and ly == cur[0] and (i, j) == (cur[1], cur[2]):
                    fill, tc = T['yellow'], T['bg']
                elif cur and ly == cur[0] - 1 and (i, j) in srcs:
                    fill, tc = T['blue'], T['bg']
                elif S.get('_line', 0) >= _RET_LINE and ly == S['k'] and (i, j) == (S['row'] + 2, S['column'] + 2):
                    fill, tc = T['green'], T['bg']
                cv.rect((X + 1, Y + 1, X + cell - 1, Y + cell - 1), fill=fill, outline=ol, width=wd, r=4)
                if v != 0 or inside:
                    s = _fr(v)
                    cv.text((X + cell / 2, Y + cell / 2), s, 20 if len(s) <= 3 else 15, tc, anchor='mm', bold=True)


def _formula(S):
    c = _cur(S)
    if c is None or c[0] < 1:
        return '`f[step][i][j]` = 从 `(i,j)` 出发走 `step` 步后仍在棋盘上的概率；棋盘外一圈圈补 0'
    step, i, j = c
    f = S['f']
    vals = [f[step - 1][i + dx][j + dy] for dx, dy in _DIRS]
    tot = sum(vals)
    return f'`({i-2},{j-2})`：8 个落点的概率之和 `{_fr(tot)}` ÷ 8 = ==`{_fr(tot / 8)}`=='


def _cap_cell(S, B, ret):
    step, i, j = S.step, S.i, S.j
    vals = [S.f[step - 1][i + dx][j + dy] for dx, dy in _DIRS]
    nz = sum(1 for v in vals if v)
    tot = sum(vals)
    return (f'`({i-2},{j-2})` 的 8 个落点里有 {nz} 个概率非 0（其余出界或为 0），之和 `{_fr(tot)}`，除以 8 → '
            f'`f[{step}][{i-2}][{j-2}]` = =={_fr(S.f[step][i][j])}==')


CONFIG = dict(
    num=688, title='骑士在棋盘上的概率', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='概率 DP · 1:1 翻译成递推',
    tags=['灵神题单·动态规划', '灵神题单·数学算法'],
    code='''
DIRS = (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)

class Solution:
    def knightProbability(self, n: int, k: int, row: int, column: int) -> float:
        f = [[[0] * (n + 4) for _ in range(n + 4)] for _ in range(k + 1)]
        for i in range(2, n + 2):
            f[0][i][2: n + 2] = [1] * n
        for step in range(1, k + 1):
            for i in range(2, n + 2):
                for j in range(2, n + 2):
                    f[step][i][j] = sum(f[step - 1][i + dx][j + dy] for dx, dy in DIRS) / 8
        return f[k][row + 2][column + 2]
''',
    call='Solution().knightProbability(3, 2, 0, 0)',
    expect=0.0625,
    skip=[],
    max_steps=90,
    views=[
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=[('step', 'step', 'yellow'), ('i', 'i-2', 'blue'), ('j', 'j-2', 'pink'), ('f[step][i][j]', 'f[step][i][j]', 'green')],
    captions={
        'DIRS =': '马的 8 种走法，每种概率 `1/8`',
        'f = [[[0]': '`f[step][i][j]`：马从 `(i,j)` 出发走 `step` 步后仍在棋盘上的概率。棋盘四周各多补 2 圈 0：马一步最多跳出 2 格，这样越界直接读到 0，省掉判断',
        'f[0][i][2: n + 2]': '`step = 0`：第 {i-2} 行棋盘内的格子，一步都不用走，概率 ==1==',
        'for i in range': lambda S, B, r: (f'`i = {S.i - 2}`：棋盘内的第 {S.i - 2} 行' if S.get('i') != B.get('i') else '这几行都处理完了'),
        'for step in range': lambda S, B, r: (f'开始算走 `{S.step}` 步：只依赖走 `{S.step - 1}` 步的结果，所以==步数从小到大==' if S.get('step') != B.get('step') else '所有步数都算完，答案在 `f[k]` 里'),
        'for j in range': lambda S, B, r: (f'`j = {S.j - 2}`，正在算 `({S.i - 2},{S.j - 2})`' if S.get('j') != B.get('j') else '这一行算完了'),
        'f[step][i][j] = sum': _cap_cell,
        'return f[k]': lambda S, B, r: f'起点 `(row, column)` 要 `+2`（补了两圈）：`f[{S.k}][{S.row + 2}][{S.column + 2}]` = =={_fr(r)}== = {r}',
    },
    cards=dict(
        one_liner='概率 = 8 个落点概率之和 ÷ 8；出界概率 0，走完仍在棋盘上概率 1',
        complexity='时间 `O(kn^2)`，空间 `O(kn^2)`（滚动数组可降到 `O(n^2)`）',
        problem=['`n x n` 棋盘，骑士从 `(row, column)` 出发，每步等概率选 8 种走法之一（可以走出棋盘）',
                 '走了 `k` 步或出界就停下，求停下时仍在棋盘上的概率',
                 '示例：`n=3, k=2, (0,0)` → `0.0625`'],
        quote='马从 (i,j) 出发，走 k 步后仍然在棋盘上的概率 = 1/8 × 八个方向走一步后，再走 k-1 步仍然在棋盘上的概率之和。……为避免下标出现负数，把棋盘的边界从 [0,n-1] 调整为 [2,n+1]。',
        quote_src='—— 灵茶山艾府题解（状态转移 / 1:1 翻译成递推）',
        idea=['`dfs(k,i,j) = 1/8 × Σ dfs(k-1,x,y)`：走一步，问题变成少走一步的同类问题',
              '边界：出界为 0，`k = 0` 且在棋盘内为 1',
              '递推把棋盘外补两圈 0，出界的落点直接读到 0，不用写 `if`'],
        summary=['时间 `O(kn^2)`，空间 `O(kn^2)`',
                 '起点下标要 `+2`：因为棋盘整体向右下平移了两格',
                 '补两圈 0 是因为骑士一步最多跳 2 格',
                 '灵神原题解还给了记忆化搜索写法（`@cache` + 出界返回 0），本视频用的是递推版'],
    ),
)
