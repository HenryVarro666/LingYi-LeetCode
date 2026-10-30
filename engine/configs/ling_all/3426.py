from math import comb as _C


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    m, n, k = S['m'], S['n'], S['k']
    done = S.get('_line') == 4 and 'MOD' in S and S.get('_done', False)
    cv.text((x0 + 18, y0 + 4), f'{m}×{n} 的格子，放 {k} 个棋子：拆成「横向差」和「纵向差」分别数', 24, T['muted'], bold=True)
    # 左：格子，示例一对棋子
    cell = min(78, (x1 - x0 - 60) / 2 / max(n, 1))
    gx, gy = x0 + 30, y0 + 70
    cv.text((gx, gy - 4), '任取一对棋子（蓝、粉）', 22, T['text'], bold=True, anchor='lb')
    for i in range(m):
        for j in range(n):
            fill = T['panel2']
            if (i, j) == (0, 0):
                fill = T['blue']
            if (i, j) == (m - 1, n - 1):
                fill = T['pink']
            cv.rect((gx + j * cell + 3, gy + 10 + i * cell + 3, gx + (j + 1) * cell - 3, gy + 10 + (i + 1) * cell - 3), fill=fill, r=8, outline=T['border'])
    gb = gy + 10 + m * cell
    cv.text((gx, gb + 12), f'横向差 |Δ列| = {n - 1}，纵向差 |Δ行| = {m - 1}', 22, T['muted'])
    cv.text((gx, gb + 44), f'其余 {k - 2} 个棋子放进剩下 {m * n - 2} 格', 22, T['yellow'], bold=True)
    cv.text((gx, gb + 78), f'C({m * n - 2}, {k - 2}) = {_C(m * n - 2, k - 2)} 种', 22, T['yellow'], bold=True)
    # 右：横向 / 纵向的绝对差计数
    rx = x0 + (x1 - x0) / 2 + 10
    def block(y, title, L, other, color):
        cv.text((rx, y), title, 22, color, bold=True)
        tot = 0
        for d in range(1, L):
            cnt = L - d
            tot += d * cnt
            yy = y + 36 + (d - 1) * 40
            cv.text((rx, yy + 4), f'差 {d}', 20, T['text'], mono=True)
            for t in range(cnt):
                cv.rect((rx + 70 + t * 34, yy, rx + 70 + t * 34 + 28, yy + 28), fill=color, r=6, alpha=200)
            cv.text((rx + 70 + cnt * 34 + 10, yy + 4), f'× {cnt} 种', 20, T['muted'])
        yy = y + 36 + max(L - 1, 1) * 40
        cv.text((rx, yy), f'Σ d·(L−d) = {tot} = C({L + 1}, 3)，再 × {other}² = =={tot * other * other}=='.replace('==', ''), 22, color, bold=True)
        return yy + 50
    ya = block(y0 + 70, f'横向（列相差 d，共 {n} 列）', n, m, T['blue'])
    yb = block(ya + 10, f'纵向（行相差 d，共 {m} 行）', m, n, T['pink'])
    # 底部：总式
    ty = max(yb + 10, gb + 130)
    a = _C(m * n - 2, k - 2)
    b = m * m * _C(n + 1, 3)
    c = n * n * _C(m + 1, 3)
    cv.text((x0 + 30, ty), f'答案 = C(mn−2, k−2) × ( m²·C(n+1,3) + n²·C(m+1,3) )', 24, T['text'], bold=True)
    cv.text((x0 + 30, ty + 40), f'= {a} × ( {b} + {c} ) = {a * (b + c)}', 28, T['green'], bold=True)


CONFIG = dict(
    num=3426, title='所有安放棋子方案的曼哈顿距离', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='贡献法 · 横纵拆分 + 组合数',
    tags=['灵神题单', '难度分 2443'],
    code='''
class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 1_000_000_007
        return comb(m * n - 2, k - 2) % MOD * (m * m * comb(n + 1, 3) + n * n * comb(m + 1, 3)) % MOD
''',
    setup='''
MOD = 1_000_000_007
MX = 100_000

fac = [0] * MX  # f[i] = i!
fac[0] = 1
for i in range(1, MX):
    fac[i] = fac[i - 1] * i % MOD

inv_f = [0] * MX  # inv_f[i] = i!^-1
inv_f[-1] = pow(fac[-1], -1, MOD)
for i in range(MX - 1, 0, -1):
    inv_f[i - 1] = inv_f[i] * i % MOD

def comb(n: int, m: int) -> int:
    return fac[n] * inv_f[m] * inv_f[n - m] % MOD
''',
    call='Solution().distanceSum(2, 3, 3)',
    expect=100,
    views=[
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=['m', 'n', 'k', ('MOD', 'MOD', 'yellow')],
    captions={
        'MOD = ': '答案要对 `10^9+7` 取模',
        'return comb': lambda S, B, r: (
            f"`C(mn−2, k−2) = C({S['m'] * S['n'] - 2}, {S['k'] - 2})` = {comb(S['m'] * S['n'] - 2, S['k'] - 2)}：固定一对后其余随便放；"
            f"横纵差之和 `{S['m'] ** 2 * comb(S['n'] + 1, 3)} + {S['n'] ** 2 * comb(S['m'] + 1, 3)}` → 返回 =={r}=="),
    },
    cards=dict(
        one_liner='每个绝对差出现几次？乘上其余棋子的放法就是答案',
        complexity='时间 `O(1)`，空间 `O(1)`（忽略预处理）',
        problem=['`m×n` 的格子里放 `k` 个相同的棋子，每格至多一个；求所有方案里每对棋子曼哈顿距离之和，对 `10^9+7` 取模',
                 '示例：`m=2, n=2, k=2` → `8`',
                 '本视频：`m=2, n=3, k=3` → `100`'],
        quote='本质上，答案是一堆 |x_i-x_j|+|y_i-y_j| 之和。拆分成 |x_i-x_j| 之和、|y_i-y_j| 之和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先看一行 `n` 个格子：绝对差为 `d` 的位置对有 `n−d` 种，每种在答案里出现 `C(mn−2, k−2)` 次',
              '推广到 `m` 行：两颗棋子不同列时，各自可以选任意一行，所以再乘 `m²`',
              '`Σ d·(n−d) = C(n+1, 3)`，纵向同理 → 答案 `C(mn−2,k−2)·(m²·C(n+1,3) + n²·C(m+1,3))`'],
        after=[dict(heading='公式怎么化简', lines=[
            '`Σ_{d=1}^{n-1} d(n−d) = n·n(n−1)/2 − n(n−1)(2n−1)/6`',
            '合并得 `(n+1)n(n−1)/6`，正好是 `C(n+1, 3)`',
            '所以不用循环，一个组合数公式 `O(1)` 出答案'])],
        summary=['时间 `O(1)`，预处理阶乘和逆元 `O(mn)`，预处理放在 setup 里（未追踪）',
                 '易错：`C(mn−2, k−2)` 是「选出这一对后其余棋子的放法」，不是总方案数',
                 '易错：横向差还要乘 `m²`，因为两颗棋子在各自的列里可以任选行',
                 '预处理版另有一个等价的 `(m·n·(m(n²−1)+n(m²−1)))//6` 写法，此处用主推导出的形式'],
    ),
)
