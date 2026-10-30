CASES = [
    ('① prefix < max_prefix', '低位随便填：max_prefix × 570 − 45'),
    ('② prefix = max_prefix，l < L', '(121 + 15L − L²) × L ÷ 3'),
    ('③ l = L，m < M', '峰 (L+M)·max(M−L−1,0)/2 + 谷 (19−min)·min/2'),
    ('④ l = L，m = M，r < R', 'L<M：min(M,R)；L>M：max(R−M−1,0)'),
    ('⑤ l = L，m = M，r = R', '是峰/谷：max_suffix + 1'),
]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    line = S.get('_line', 0)
    if 'n' not in S:
        a, b = S['num1'], S['num2']
        cv.text((x0 + 30, y0 + 70), f'区间 [{a}, {b}]', 36, T['cyan'], mono=True, bold=True)
        cv.text((x0 + 30, y0 + 150), f'答案 = f({b}) − f({a - 1})', 36, T['yellow'], mono=True, bold=True)
        cv.text((x0 + 30, y0 + 230), 'f(n)：[1, n] 里所有整数的波动值之和', 28, T['muted'])
        cv.text((x0 + 30, y0 + 280), '按「每个峰/谷出现在多少个数里」来数', 28, T['muted'])
        return
    if 'pow10' not in S:
        cv.text((x0 + 30, y0 + 70), f"f(n)，n = {S['n']}：从低到高枚举 (l, m, r) 的位置", 30, T['text'], bold=True)
        return
    n = S['n']
    pow10 = S['pow10']
    i = len(str(pow10)) - 1
    ds = str(n)
    k = len(ds)
    cv.text((x0 + 18, y0 + 4), f'f(n)，n = {n}：把每个数拆成 prefix | l | m | r | suffix', 24, T['muted'], bold=True)
    cell = 96
    segs = []
    idx_r, idx_m, idx_l = k - 1 - i, k - 2 - i, k - 3 - i
    cols = {}
    for p in range(k):
        if p > idx_l - 1 and p == idx_l:
            cols[p] = ('l', T['cyan'])
        elif p == idx_m:
            cols[p] = ('m', T['yellow'])
        elif p == idx_r:
            cols[p] = ('r', T['pink'])
        elif p > idx_r:
            cols[p] = ('suffix', T['dim'])
        else:
            cols[p] = ('prefix', T['blue'])
    sx = x0 + ((x1 - x0) - cell * k) / 2
    ys = y0 + 70
    for p, ch in enumerate(ds):
        name, col = cols[p]
        X = sx + p * cell
        cv.rect((X + 6, ys, X + cell - 6, ys + 100), fill=col, alpha=50, outline=col, r=12)
        cv.text((X + cell / 2, ys + 50), ch, 54, T['text'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ys + 116), name, 20, col, anchor='mt', bold=True)
    # 当前 L M R
    if 'L' in S:
        L, M, R = S['L'], S['M'], S['R']
        kind = '峰' if L < M > R else '谷' if L > M < R else '不是峰谷'
        cv.text((x0 + 30, ys + 172), f'(L, M, R) = ({L}, {M}, {R})：{kind}', 30, T['text'], bold=True, mono=True)
    if 'max_prefix' in S:
        cv.text((x0 + 30, ys + 214), f"max_prefix = {S['max_prefix']}    pow10 = {pow10}（suffix 有 {pow10} 种填法）", 26, T['muted'], mono=True)
    # 五种情况
    yb = ys + 270
    cur_case = {18: 0, 21: 1, 24: 2, 25: 2, 28: 3, 29: 3, 30: 3, 31: 3, 37: 4, 38: 4, 39: 4}.get(line)
    for c, (h, f) in enumerate(CASES):
        y = yb + c * 50
        col = T['yellow'] if cur_case == c else T['dim']
        if cur_case == c:
            cv.rect((x0 + 14, y - 6, x1 - 14, y + 40), fill=T['yellow'], alpha=35, r=10)
        cv.text((x0 + 30, y), h, 24, col, bold=True)
        cv.text((x0 + 380, y), f, 22, col, mono=True)
    cv.text((x1 - 14, y1 - 10), f"cnt = {S.get('cnt', '—')}    ans = {S.get('ans', 0)}", 28, T['green'], anchor='rb', bold=True, mono=True)


CONFIG = dict(
    num=3753, title='范围内总波动值 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='贡献法 + 数学公式',
    tags=['灵神题单·动态规划', '难度分 2297'],
    code='''
class Solution:
    # 计算 [1, n] 中的整数的波动值之和
    def calc(self, n: int) -> int:
        ans = 0

        # 把整数划分成五段：prefix | l | m | r | suffix
        # 从低到高枚举 (l, m, r) 的位置，计算 (l, m, r) 对答案的贡献
        pow10 = 1
        while n >= pow10 * 100:
            max_prefix = n // (pow10 * 1000)
            n2 = n // pow10
            L = n2 // 100 % 10
            M = n2 // 10 % 10
            R = n2 % 10

            # 1. prefix < max_prefix 时，低位不受约束
            # 但 prefix=0 且 l=0 的情况是不合法的，需要减掉
            cnt = max_prefix * 570 - 45  # 先不与 pow10 相乘

            # 2. prefix = max_prefix 且 l < L
            cnt += (121 + L * 15 - L * L) * L // 3

            # 3. prefix = max_prefix 且 l = L 且 m < M
            cnt += (L + M) * max(M - L - 1, 0) // 2   # 峰
            cnt += (19 - min(L, M)) * min(L, M) // 2  # 谷

            # 4. prefix = max_prefix 且 l = L 且 m = M 且 r < R
            if L < M:  # 只能是峰
                cnt += min(M, R)
            elif L > M:  # 只能是谷
                cnt += max(R - M - 1, 0)

            # 到此为止，suffix 可以随便填，有 pow10 种填法
            ans += cnt * pow10

            # 5. prefix = max_prefix 且 l = L 且 m = M 且 r = R
            if (L - M) * (M - R) < 0:  # 峰或谷
                max_suffix = n % pow10
                ans += max_suffix + 1  # suffix 可以填 [0, max_suffix] 中的任意整数

            pow10 *= 10

        return ans

    def totalWaviness(self, num1: int, num2: int) -> int:
        return self.calc(num2) - self.calc(num1 - 1)
''',
    call='Solution().totalWaviness(1, 4848)',
    expect=5020,
    skip=['L = n2', 'M = n2', 'R = n2', 'pow10 = 1', 'ans = 0'],
    views=[dict(type='custom', draw=_draw, h=600)],
    watch=[('pow10', 'pow10', 'blue'), ('L', 'L', 'cyan'), ('M', 'M', 'yellow'), ('R', 'R', 'pink'), ('cnt', 'cnt', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'while n >= pow10 * 100': lambda S, B, r: (f'`n = {S.n} >= {S.pow10 * 100}`：n 至少还有 `l m r` 三位（再加 `{len(str(S.pow10)) - 1}` 位 suffix）→ 这个位置要数'
                                                   if S.n >= S.pow10 * 100 else f'`n = {S.n} < {S.pow10 * 100}`：凑不出 `l m r` 三位了 → 所有位置数完'),
        'max_prefix =': '`prefix` 最大能取 `n // 10^(i+3)` = =={max_prefix}==（前面的高位）',
        'n2 = n // pow10': '先砍掉 suffix：`n2 = {n2}`，它的末三位就是 `l m r`；并取 `L = {L}`、`M = {M}`、`R = {R}` 作为各位的上限',
        'cnt = max_prefix * 570': '情况1：`prefix` 比上限小，低位随便填。合法三元组 570 个 × `{max_prefix}`，再减 `prefix=0, l=0` 的 45 个 → `cnt` = =={cnt}==',
        'cnt += (121 + L': '情况2：`prefix` 贴上限，但 `l < L`（`l` 取 0..{L - 1}），`m r` 随便填 → `cnt` = =={cnt}==',
        'cnt += (L + M)': '情况3a：`l = L`、`m < M`，`l < m`，只能是峰，`r` 有 `m` 种填法 → `cnt` = =={cnt}==',
        'cnt += (19 - min': '情况3b：`l = L`、`m < M`，`l > m` 的谷（`r` 有 `9-m` 种）→ `cnt` = =={cnt}==',
        'if L < M': lambda S, B, r: (f'情况4：`l = L`、`m = M`、`r < R`。`L = {S.L} < M = {S.M}` → 只能是峰' if S.L < S.M else f'情况4：`l = L`、`m = M`、`r < R`。`L = {S.L}` 不小于 `M = {S.M}`，看是不是谷'),
        'cnt += min(M, R)': '峰要求 `r < m`，且 `r < R` → `r` 有 `min(M, R)` = {min(M, R)} 种 → `cnt` = =={cnt}==',
        'elif L > M': lambda S, B, r: (f'`L = {S.L} > M = {S.M}` → 只能是谷' if S.L > S.M else f'`L = M = {S.L}`：`l, m` 相等，不可能是峰谷，情况4贡献 0'),
        'cnt += max(R - M - 1': '谷要求 `r > m`，且 `r < R` → `r` 取 `[M+1, R-1]`，有 `max(R-M-1, 0)` 种 → `cnt` = =={cnt}==',
        'ans += cnt * pow10': '情况1~4里 `suffix` 随便填，有 `{pow10}` 种：`ans += {cnt} × {pow10}` → =={ans}==',
        'if (L - M) * (M - R) < 0': lambda S, B, r: (f'情况5：`(L, M, R) = ({S.L}, {S.M}, {S.R})` 恰好是峰或谷' if (S.L - S.M) * (S.M - S.R) < 0
                                                     else f'情况5：`(L, M, R) = ({S.L}, {S.M}, {S.R})` 不是峰谷，没有贡献'),
        'max_suffix = n % pow10': '情况5 里 `suffix` 也要贴着 `n`：`max_suffix = {max_suffix}`',
        'ans += max_suffix + 1': '`suffix` 取 `[0, {max_suffix}]`，共 `{max_suffix} + 1` 个数都含这个峰谷 → `ans` = =={ans}==',
        'pow10 *= 10': '`l m r` 整体往高位挪一格：`pow10` → {pow10}',
        'return ans': '`f(n)` = ==%s==；各位置的峰谷已经全部累加' % '{ans}',
        'return self.calc': '答案 = `f(num2) − f(num1 − 1)`；本例 `num1 = 1`，`f(0) = 0`',
    },
    cards=dict(
        result='`f(4848) − f(0) = 5020 − 0 = 5020`',
        one_liner='横看成岭侧成峰：数每个位置的峰谷，出现在几个数里',
        complexity='时间 `O(log num2)`，空间 `O(1)`',
        problem=['数字的波动值 = 峰（比两邻都大）+ 谷（比两邻都小）的个数，首尾数位不算',
                 '求 `[num1, num2]` 内所有数的波动值之和，`num2` 最大 `10^15`',
                 '示例：`[120, 130]` → `3`；本视频 `[1, 4848]` → `5020`'],
        quote='横看成岭侧成峰，对于 [1,n] 中的整数：在最低三位中，一共出现了多少个峰和谷？在低二位到低四位中呢？……',
        quote_src='—— 灵茶山艾府题解',
        idea=['答案 = `f(num2) − f(num1−1)`，`f(n)` 是 `[1, n]` 的波动值之和',
              '把每个数拆成 `prefix | l | m | r | suffix`，枚举 `(l,m,r)` 的位置',
              '对每个位置，按「贴上限到哪一位」分五种情况，用公式算出峰谷三元组个数',
              '情况1~4 里 `suffix` 随便填，要乘 `10^i`；情况5 贴着 `n`，只有 `suffix + 1` 个'],
        after=[dict(heading='另一种写法：数位 DP', lines=['题解方法一是数位 DP：`dfs(i, last_cmp, last_digit, limit_low, limit_high)`',
                                                        '返回「子树波动值之和」与「合法数字个数」，每个峰谷对后面所有填法各贡献一次',
                                                        '复杂度 `O(D²n)`；本视频演示的是 `O(log)` 的数学公式写法'])],
        summary=['时间 `O(log num2)`，空间 `O(1)`（数位 DP 为 `O(D²n)`）',
                 '`prefix = 0` 且 `l = 0` 是前导零，不合法，所以情况1 要减 45',
                 '峰、值的三元组个数：峰 285 个，谷 285 个，各自由 `m` 或 `9-m` 种 `r` 求和得到',
                 '`max(M-L-1, 0)` 之类的 `max` 避免出现负数，省去分类讨论',
                 '情况5 里 `suffix` 也要贴着 `n`，只有 `n % pow10 + 1` 种'],
    ),
)
