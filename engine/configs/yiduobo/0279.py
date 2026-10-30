import math as _m

INPUTS = (12, 13, 28)
EXPECT = [3, 2, 4]
_GROUP = {n: k + 1 for k, n in enumerate(INPUTS)}
_ACC = (45, 212, 191)


def _checks(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'n' not in S:
        return
    n = S['n']
    cv.text((x0 + 18, y0 + 4), f'第 {_GROUP.get(n, "?")} 组输入：n = {n}　　yiduobo 的判定顺序', 24, T['muted'], bold=True)
    y = y0 + 50
    lines = []
    if 't' in S:
        t = S['t']
        ok = t * t == n
        lines.append(f"① 是完全平方数？ `t = int(√{n}) = {t}`，`{t}² = {t * t}` " +
                     ('= n → ==答案 1==' if ok else '≠ n ×'))
    if 'pow4' in S:
        p = S['pow4']
        if n % (p * 4) == 0:
            lines.append(f'② 除掉因子 4：`pow4 = {p}`，`{n}` 还能被 `{p * 4}` 整除 → 继续')
        else:
            q = n // p
            hit = q % 8 == 7
            lines.append(f'② `{n} = {p} × {q}`（除尽 4），`{q} % 8 = {q % 8}` ' +
                         ('= 7 → ==答案 4==' if hit else '≠ 7 ×'))
    if 'j' in S:
        parts = []
        for jj in range(1, S['j'] + 1):
            r = n - jj * jj
            s = int(_m.sqrt(r))
            ok = s * s == r
            done = jj < S['j'] or 'tmp' in S
            if not done:
                break
            parts.append(f'`{n}-{jj}²={r}`' + (' ✓' if ok else ' ×'))
        lines.append('③ 枚举 j，看 `n - j²` 是不是平方数：' + '　'.join(parts))
    for ln in lines:
        h = cv.rich(x0 + 30, y, ln, x1 - x0 - 60, size=27, accent=_ACC, line_gap=1.45)
        y += h + 18
    if not lines:
        cv.text((x0 + 30, y + 10), '开始判断…', 26, T['dim'])


def _squares(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'n' not in S:
        return
    n = S['n']
    t = int(_m.sqrt(n))
    cv.text((x0 + 18, y0 + 4), f'不超过 {n} 的完全平方数 j²（第 ③ 步逐个尝试）', 24, T['muted'], bold=True)
    cell = 96
    sx = x0 + 30
    cj = S.get('j')
    for k in range(1, t + 1):
        X = sx + (k - 1) * (cell + 12)
        fill = T['panel2']
        if cj == k:
            r = n - k * k
            s = int(_m.sqrt(r))
            fill = T['green'] if ('tmp' in S and s * s == r) else T['orange']
        elif cj is not None and k < cj:
            fill = (40, 45, 53)
        cv.rect((X, y0 + 44, X + cell, y0 + 44 + 70), fill=fill, outline=T['border'], width=1, r=10)
        cv.text((X + cell / 2, y0 + 79), f'{k * k}', 30, T['bg'] if fill in (T['green'], T['orange']) else T['text'],
                anchor='mm', bold=True)
        cv.text((X + cell / 2, y0 + 120), f'j={k}', 18, T['dim'], anchor='mt', mono=True)


def _cap_if1(S, B, ret):
    t, n = S.t, S.n
    if t * t == n:
        return f'`{t}² = {n}`：n 本身是完全平方数 → ==1 个=='
    return f'`{t}² = {t * t} ≠ {n}`：不是完全平方数，答案至少是 2'


def _cap_while(S, B, ret):
    p, n = B.pow4, B.n
    if n % (p * 4) == 0:
        return f'`{n} % {p * 4} = 0`：还含因子 4 → 继续除'
    return f'`{n} % {p * 4} = {n % (p * 4)}`：因子 4 已除尽，`pow4 = {p}`'


def _cap_mod8(S, B, ret):
    q = S.n // S.pow4
    if q % 8 == 7:
        return f'`{S.n} // {S.pow4} = {q}`，`{q} % 8 = 7` → 形如 `4^k(8m+7)`：==答案就是 4=='
    return f'`{S.n} // {S.pow4} = {q}`，`{q} % 8 = {q % 8}` ≠ 7 → 答案不是 4，只剩 ==2 或 3=='


def _cap_if2(S, B, ret):
    t, j, n = S.tmp, S.j, S.n
    s = t * t + j * j
    if s == n:
        return f'`{t}² + {j}² = {s}` = n ✓ → 能拆成两个平方数'
    return f'`{t}² + {j}² = {s} ≠ {n}` ×'


CONFIG = dict(
    num=279, title='完全平方数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='找规律：四平方和 · O(√n)',
    code='''
class Solution(object):
    def numSquares(self, n):
        \'\'\'
        f = []
        f.append(1)

        for i in range(1, n + 1):
            t = int(sqrt(i))
            if t * t == i:
                f.append(1)
            else:
                f.append(f[-1] + 1)
                for j in range(2, t + 1):
                    f[-1] = min(f[-1], f[i - j * j] + 1)

        return f[n]
        \'\'\'

        t = int(sqrt(n))
        if t * t == n:
            return 1

        pow4 = 1
        while n % (pow4 * 4) == 0:
            pow4 *= 4

        if n // pow4 % 8 == 7:
            return 4

        for j in range(1, t + 1):
            tmp = int(sqrt(n - j * j))
            if tmp * tmp + j * j == n:
                return 2

        return 3
''',
    setup='from math import sqrt',
    call=f'[Solution().numSquares(n) for n in {INPUTS}]',
    expect=EXPECT,
    views=[
        dict(type='custom', draw=_checks, h=330),
        dict(type='custom', draw=_squares, h=170),
    ],
    watch=[('n', 'n', 'orange'), 't', 'pow4', ('j', 'j', 'green'), 'tmp'],
    skip=['for j in range(1, t + 1)'],
    captions={
        't = int(sqrt(n))': lambda S, B, ret: f'第 {_GROUP.get(S.n, "?")} 组 `n = {S.n}`：先算 `t = int(√{S.n}) = {S.t}`',
        'if t * t == n': _cap_if1,
        'return 1': 'n 是完全平方数，返回 ==1==',
        'pow4 = 1': '准备把 n 中的因子 4 全部除掉：`pow4` 记录 `4^k`',
        'while n % (pow4 * 4)': _cap_while,
        'pow4 *= 4': '`pow4` 变成 `{pow4}`',
        'if n // pow4 % 8 == 7': _cap_mod8,
        'return 4': '返回 ==4==（原文 `n / pow4`，Python 3 改成整除 `//`）',
        'tmp = int(sqrt(n - j * j))': '试 `j = {j}`：`n - j² = {n - j * j}`，`int(√{n - j * j}) = {tmp}`',
        'if tmp * tmp + j * j == n': _cap_if2,
        'return 2': '`{n} = {tmp}² + {j}²` → 返回 ==2==',
        'return 3': '所有 j 都试过了，凑不成 2 个 → ==只能是 3==（`12 = 4 + 4 + 4`）',
    },
    cards=dict(
        result='三组依次返回 `3`、`2`、`4`：`12 = 4+4+4`，`13 = 9+4`，`28 = 25+1+1+1` ✓',
        one_liner='先写 DP 打表找规律：答案只有 1~4，按 1 → 4 → 2 → 3 依次判定',
        complexity='时间 `O(√n)`，空间 `O(1)`',
        problem=['给你整数 `n`，返回==和为 n 的完全平方数的最少数量==',
                 '示例：`n = 12` → `3`（`4 + 4 + 4`）；`n = 13` → `2`（`4 + 9`）',
                 '演示：依次跑 `n = 12, 13, 28`'],
        before=[dict(heading='yiduobo：第一眼是动态规划', chapter='② 思路', lines=[
            '`f[i]` = 数字 i 最少由几个完全平方数组成',
            'i 是完全平方数 → `f[i] = 1`；否则 `f[i] = min(f[i - j²]) + 1`',
            '复杂度 `O(n√n)`；原文把这段 DP 代码==注释==在了最终代码里',
        ])],
        quote='仔细观察前200的f数组，可以发现==f最大不超过4==……若某个数x除以4^k之后，模8余7，那么其对应的f[x]就是4，在小范围内也得到了验证。',
        quote_src='—— yiduobo 题解（打表找规律）',
        idea=['等于 4 的数：`7, 15, 23, 28, 31, …` → 大多 ==模 8 余 7==',
              '剩下的 `28 = 4×7`、`60 = 4×15`、`112 = 16×7` → 先除掉 `4^k` 再看',
              '判定：是平方数 → 1；`4^k(8m+7)` → 4；能拆成 `j² + 平方数` → 2；否则 3'],
        after=[dict(heading='这个规律是对的吗？', lines=[
            '作者原话：「虽然不知道如何证明，但是在小范围内是正确的」',
            '它正是==四平方和定理==（每个数 ≤ 4 个平方数）+ ==勒让德三平方和定理==',
            '三平方和定理：n 不能写成 3 个平方数之和 ⇔ `n = 4^k(8m+7)`',
        ])],
        summary=['时间 `O(√n)`：只有判定 2 时要枚举 j；空间 `O(1)`',
                 '原文为 Python 2 写法：`n / pow4` 已改为 `n // pow4`，并删去 docstring',
                 '要先==除尽所有的 4==，再判断模 8 余 7（如 `28`、`112`）',
                 '判定顺序 1 → 4 → 2 → 3：最后剩下的一定是 3',
                 '面试更通用的做法仍是完全背包 DP（`O(n√n)`）'],
    ),
)
