N, K = 4, 2          # 点数 n、线段数 k
BALLS = N + K        # 小球数 n + k
GROUPS = 2 * K + 1   # 盒子数 2k + 1
CUT = [1, 2, 4, 5]   # 示例方案「{(0,1),(2,3)}」对应的隔板位置（第 g 个空隙 = 第 g 与 g+1 个球之间）
NAMES = ['e0', 'x1', 'e1', 'x2', 'e2']


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '数轴上的点 0 ~ n−1，和一种方案 {(0,1), (2,3)}', 24, T['muted'], bold=True)
    # 上：数轴与线段
    cell = 150
    sx = x0 + (x1 - x0 - cell * (N - 1)) / 2
    ay = y0 + 100
    segs = [(0, 1, 'blue'), (2, 3, 'pink')]
    for a, b, c in segs:
        cv.rect((sx + a * cell, ay - 8, sx + b * cell, ay + 8), fill=T[c], r=8)
    for i in range(N):
        X = sx + i * cell
        cv.rect((X - 14, ay - 14, X + 14, ay + 14), fill=T['panel2'], outline=T['border'], r=14)
        cv.text((X, ay + 28), i, 22, T['dim'], anchor='mt', mono=True)
    cv.text((sx + 0.5 * cell, ay - 28), 'x1 = 1', 24, T['blue'], anchor='mb', bold=True)
    cv.text((sx + 2.5 * cell, ay - 28), 'x2 = 1', 24, T['pink'], anchor='mb', bold=True)
    cv.text((sx + 1.5 * cell, ay + 30), 'd1 = 1', 24, T['muted'], anchor='mt', bold=True)
    # 中：n+k 个球，2k 个隔板
    cv.text((x0 + 18, y0 + 200), f'{BALLS} 个球排成一行，{BALLS - 1} 个空隙里选 {2 * K} 个插板 → {GROUPS} 组（每组至少 1 个）', 24, T['muted'], bold=True)
    bsz = 100
    bx = x0 + (x1 - x0 - bsz * BALLS) / 2
    by = y0 + 290
    cols = ['cyan', 'blue', 'cyan', 'pink', 'cyan']
    grp = 0
    for i in range(BALLS):
        X = bx + i * bsz
        cv.rect((X + 14, by, X + bsz - 14, by + bsz - 28), fill=T[cols[grp]], r=24)
        cv.text((X + bsz / 2, by + (bsz - 28) / 2), i + 1, 24, T['bg'], anchor='mm', bold=True)
        if i + 1 in CUT:
            cv.line([(X + bsz, by - 22), (X + bsz, by + bsz)], T['orange'], 6)
            grp += 1
    for g in range(1, BALLS):
        if g not in CUT:
            X = bx + g * bsz
            cv.dashed((X, by - 12), (X, by + bsz - 10), T['dim'], 2)
    # 组名
    gx = bx
    sizes = [1, 1, 2, 1, 1]
    for gi, sz in enumerate(sizes):
        mid = gx + sz * bsz / 2
        c = 'blue' if gi == 1 else 'pink' if gi == 3 else 'cyan'
        cv.text((mid, by + bsz + 10), NAMES[gi] + f'={sz}', 22, T[c], anchor='mt', bold=True)
        gx += sz * bsz
    cv.text((x0 + 18, y1 - 100), '青色 e = d + 1（空白长度 + 1），蓝/粉 x = 线段长度；橙色竖线 = 隔板', 22, T['muted'])
    cv.text((x0 + 18, y1 - 60), f'方案数 = C(n+k−1, 2k) = C({N + K - 1}, {2 * K}) = ' + str(S['ret']) if S.get('ret') is not None else f'方案数 = C(n+k−1, 2k) = C({N + K - 1}, {2 * K})', 30, T['green'], bold=True)


CONFIG = dict(
    num=1621, title='大小为 K 的不重叠线段的数目', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='隔板法 · 组合数',
    tags=['灵神题单', '数学算法', '难度分 2198'],
    code='''
class Solution:
    def numberOfSets(self, n: int, k: int) -> int:
        return comb(n + k - 1, k * 2) % 1_000_000_007
''',
    call=f'Solution().numberOfSets({N}, {K})',
    expect=5,
    views=[dict(type='custom', draw=_draw, h=560)],
    watch=[('n', 'n', 'blue'), ('k', 'k', 'pink')],
    captions={
        'return comb': '`n + k − 1 = {n + k - 1}`，`2k = {2 * k}`：隔板法的组合数 `C({n + k - 1}, {2 * k})`，再对 `10^9+7` 取模 → =={ret}==',
    },
    cards=dict(
        one_liner='把线段长度和空白长度写成方程，用隔板法数正整数解',
        complexity='时间 `O(1)`，空间 `O(1)`（不计预处理）',
        problem=['`n` 个点在 `x = 0 … n−1`，选恰好 `k` 条不重叠的线段，每条至少覆盖两个点，端点是整数、可以重合',
                 '求方案数，对 `10^9+7` 取模',
                 '示例：`n = 4, k = 2` → `5`'],
        quote='所有长度相加，等于从 0 到 n−1 的长度 n−1：d0 + x1 + d1 + x2 + d2 + ⋯ + xk + dk = n−1，其中 xi ≥ 1，di ≥ 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x_i` 是第 `i` 条线段的长度（≥ 1），`d_i` 是它们之间和两端的空白长度（≥ 0）',
              '令 `e_i = d_i + 1`，方程右边变成 `n−1+(k+1) = n+k`，`2k+1` 个变量都是正整数',
              '==隔板法==：`n+k` 个球有 `n+k−1` 个空隙，选 `2k` 个插板 → `C(n+k−1, 2k)`',
              '代入 `n=4, k=2`：`C(5, 4) = 5`'],
        before=[dict(heading='先把几何问题变成方程', lines=[
            '`x_i`：第 `i` 条线段的长度，`x_i >= 1`',
            '`d_i`：线段之间、两端的空白长度，`d_i >= 0`',
            '`d0 + x1 + d1 + x2 + d2 + … + xk + dk = n − 1`',
            '示例 `n=4, k=2` 的方案 `{(0,1),(2,3)}`：`x1 = x2 = 1`，`d1 = 1`，其余为 0'])],
        after=[dict(heading='隔板法怎么数', lines=[
            '`e_i = d_i + 1`，方程变成 `e0 + x1 + e1 + … + ek = n + k`，每个变量 `>= 1`',
            '`n + k` 个球排成一行，有 `n + k − 1` 个空隙',
            '选 `2k` 个空隙插板，就把球分成 `2k + 1` 组，一一对应一种方案',
            '`n=4, k=2`：`C(5, 4) = 5`，和示例一致'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '关键是把「几何位置」变成「长度之和」的方程，避开 DP',
                 '写法二：预处理阶乘 `fac` 和逆元阶乘 `inv_f`，查表算组合数，思路相同；本视频选 `comb` 写法',
                 '易错：返回前别忘了取模；`comb` 需要 Python 3.8+',
                 '同类题：灵神数学题单 2.2「组合计数」'],
    ),
)
