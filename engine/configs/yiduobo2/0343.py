TESTS = [2, 9, 8, 10]


def _orig(S):
    """还原本次调用的原始 n（代码里 n %= 3 会改掉它）"""
    if 'n' not in S:
        return None
    if 'pow3' not in S or S['_line'] == 8:
        return S['n']
    n, p = S['n'], S['pow3']
    dec = n == 1 and S['_line'] in (12, 13, 17, 18)
    return 3 * (p + (1 if dec else 0)) + n


def _pieces(N):
    if N == 2:
        return [1, 1]
    if N == 3:
        return [1, 2]
    q, r = divmod(N, 3)
    if r == 0:
        return [3] * q
    if r == 1:
        return [3] * (q - 1) + [4]
    return [3] * q + [2]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    N = _orig(S)
    if N is None:
        return
    line = S['_line']
    cv.text((x0 + 18, y0 + 4), f'把 n = {N} 拆成若干段（每格 = 1），乘积最大？蓝 = 3，橙 = 余数段', 24, T['muted'], bold=True)
    decided = 'pow3' in S and line != 8 or line in (4, 6)
    pcs = _pieces(N) if decided else [1] * N
    cell = min(90, (x1 - x0 - 80) / N)
    sx = x0 + ((x1 - x0) - cell * N) / 2
    top, bot = y0 + 170, y0 + 280
    k = 0
    for j, p in enumerate(pcs):
        last_rem = decided and p != 3 and N > 3
        c = T['orange'] if last_rem or (N <= 3 and decided) else (T['blue'] if decided else T['dim'])
        # 余数段在 res 定下来之前先画成灰色
        if last_rem and line in (9, 10, 11) and not (line == 11 and S['n'] == 0):
            c = T['dim']
        X0, X1 = sx + k * cell, sx + (k + p) * cell
        cv.rect((X0 + 3, top, X1 - 3, bot), fill=c, r=10)
        for t in range(1, p):
            cv.dashed((X0 + t * cell, top + 8), (X0 + t * cell, top + 30), T['bg'], 2, 6, 6)
            cv.dashed((X0 + t * cell, bot - 30), (X0 + t * cell, bot - 8), T['bg'], 2, 6, 6)
        cv.text(((X0 + X1) / 2, (top + bot) / 2), p, 34, T['bg'], anchor='mm', bold=True)
        k += p
    for i in range(N + 1):
        cv.text((sx + i * cell, bot + 10), i, 18, T['dim'], anchor='mt', mono=True)
    if decided:
        prod = 1
        for p in pcs:
            prod *= p
        s = ' × '.join(map(str, pcs)) + f' = {prod}'
        cv.text(((x0 + x1) / 2, bot + 130), s, 52, T['green'], anchor='mm', bold=True, mono=True)
        if N > 3 and N % 3 == 1:
            cv.text(((x0 + x1) / 2, bot + 230), '余 1 时：不要 3 × 1 = 3，把它换成 4（= 2 × 2）', 28, T['orange'], anchor='mm', bold=True)
        elif N > 3 and N % 3 == 2:
            cv.text(((x0 + x1) / 2, bot + 230), '余 2 时：多出来的 2 单独成一段，乘上 2', 28, T['orange'], anchor='mm', bold=True)
        elif N > 3:
            cv.text(((x0 + x1) / 2, bot + 230), '正好整除：全部拆成 3', 28, T['blue'], anchor='mm', bold=True)
        else:
            cv.text(((x0 + x1) / 2, bot + 230), '至少拆成两段：2 = 1 + 1，3 = 1 + 2，特判', 28, T['orange'], anchor='mm', bold=True)


def _rem(S, B, ret):
    if S.n == 1:
        return f'余数是 1：`3 × 1` 不如 `2 × 2`，所以==少拆一个 3==，凑成 4'
    return f'余数是 {S.n}，不等于 1'


def _rem2(S, B, ret):
    if S.n == 2:
        return f'余数是 2：多出的 2 单独成一段'
    return f'余数是 0：==正好全拆成 3==，`res` 保持 1'


CONFIG = dict(
    num=343, title='整数拆分', difficulty='Medium', category='数学',
    author='yiduobo', technique='尽量拆 3，余 1 时换成 2×2',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def integerBreak(self, n):
        if n == 2:
            return 1
        elif n == 3:
            return 2
        else:
            pow3 = n // 3
            n %= 3
            res = 1
            if n == 1:
                pow3 -= 1
                res = 4
            elif n == 2:
                res = 2

            res *= 3 ** pow3
            return res
''',
    call='[' + ', '.join(f'Solution().integerBreak({t})' for t in TESTS) + ']',
    expect=[1, 27, 18, 36],
    views=[
        dict(type='text', fn=lambda S: f'当前输入：`n = {_orig(S)}`（依次测试 `{TESTS}`）' if _orig(S) is not None else '', h=60),
        dict(type='custom', draw=_draw, h=440),
    ],
    watch=['n', 'pow3', ('res', 'res', 'green')],
    captions={
        3: lambda S, B, r: ('`n = 2`：只能拆成 `1 + 1`，特判' if S.n == 2 else f'`n = {S.n}` 不是 2'),
        'return 1': '必须拆成至少两段：`1 × 1` = ==1==',
        'elif n == 3': lambda S, B, r: ('`n = 3`：只能拆成 `1 + 2`，特判' if S.n == 3 else f'`n = {S.n}` 也不是 3 → 走一般情况'),
        'return 2': '`1 × 2` = ==2==（不拆反而是 3，但题目要求至少两段）',
        'pow3 = n // 3': '尽量多拆 3：最多能拆 `{n} // 3 = {pow3}` 个 3',
        'n %= 3': '看余数：`n` 变成 `{n}`',
        'res = 1': '`res` 先放余数段的乘积，初始 1',
        'if n == 1': _rem,
        'pow3 -= 1': '拿出一个 3 和余下的 1 合并：`pow3` → {pow3}',
        'res = 4': '`3 + 1` 换成 `2 + 2`：乘积从 3 变成 ==4==',
        14: _rem2,
        'res = 2': '余数段 2 → `res = 2`',
        'res *= 3 ** pow3': '`res` = `{B.res} × 3^{pow3}` = =={res}==',
        'return res': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='尽量拆成 3；余 1 时把一个 3 和 1 换成 2×2',
        complexity='时间 `O(1)`（只算一次幂），空间 `O(1)`',
        problem=['把正整数 `n` 拆成==至少两个==正整数之和，使它们的乘积最大，返回最大乘积',
                 '示例：`n = 2` → `1`（1+1）；`n = 10` → `36`（3+3+4）',
                 f'本视频依次跑 `n = {TESTS}`，覆盖特判和余数 0/1/2 三种情况'],
        quote='经典的数学题，具体原理不知道应该怎么证明，总而言之就是==尽量拆3==，不过对于4的情况则是拆成2*2更好。',
        quote_src='—— yiduobo 题解原文',
        idea=['拆出 1 白白浪费；段长 ≥ 5 时再拆更划算（`5 < 2×3`）→ 只用 2 和 3',
              '`2+2+2` 不如 `3+3`（`8 < 9`）→ ==2 最多两个==，其余全是 3',
              '按 `n % 3` 分类：余 0 全拆 3；余 2 再乘 2；余 1 退一个 3 凑成 4'],
        after=[dict(heading='为什么是 3？', lines=[
            '段长 `x ≥ 5`：拆成 `2 + (x−2)`，`2(x−2) = 2x − 4 > x` → 越拆越大',
            '段长 4：`2 × 2 = 4`，拆不拆一样；所以只剩 2、3（4 当作两个 2）',
            '三个 2 换成两个 3：`2^3 = 8 < 3^2 = 9` → 3 越多越好',
        ])],
        summary=['时间 `O(1)`，空间 `O(1)`；本质是贪心 + 数学结论',
                 '易错：`n = 2, 3` 必须特判（至少拆两段，答案比 n 本身还小）',
                 '易错：余 1 时别乘 1，要把一个 3 拿出来凑成 `2 × 2`',
                 '原文为 Python 2 写法，`n / 3` 已改为 `n // 3`，并删去类型说明文档字符串',
                 '也可以用 DP：`dp[i] = max(j × (i−j), j × dp[i−j])`，`O(n^2)`'],
    ),
)
