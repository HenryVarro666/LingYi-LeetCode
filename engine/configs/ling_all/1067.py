def _txt(S):
    if 'pow10' not in S or 'n' not in S:
        return '答案 = `calc(high, d)` − `calc(low−1, d)`：各算 ==1..n 中数字 d 出现几次=='
    n, d, p = S['n'], S['d'], S['pow10']
    if p > n:
        return f'`pow10 = {p} > n = {n}`：所有数位都枚举完，`ans = {S["ans"]}`'
    if 'M' not in S or S.get('_line', 0) < 8:
        return f'枚举 `m` 所在的数位：`pow10 = {p}`（个位、十位、百位…）'
    M, mp = S['M'], S['max_prefix']
    return f'`pow10 = {p}`：前缀上限 `{mp}`，n 在这一位 `M = {M}`，要数 `d = {d}`'


def _pos(S):
    if 'pow10' not in S or 'n' not in S or S['pow10'] > S['n']:
        return None
    return len(str(S['n'])) - len(str(S['pow10']))


def _col(S, i, v):
    p = _pos(S)
    return 'blue' if p is not None and i == p else None


CONFIG = dict(
    num=1067, title='范围内的数字计数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='数位统计 · 枚举 d 所在数位',
    tags=['灵神题单·动态规划'],
    code='''
class Solution:
    def calc(self, n: int, d: int) -> int:
        ans = 0
        pow10 = 1

        while pow10 <= n:
            max_prefix = n // (pow10 * 10)
            M = n // pow10 % 10

            # 1. prefix < max_prefix 时，低位不受约束
            # m 填 d，suffix 随便填
            # 如果 d = 0，需要注意 prefix = m = 0 的情况，m 是前导零，不能计入，减去
            ans += (max_prefix - (d == 0)) * pow10

            if M > d:
                # 2. prefix = max_prefix 且 M > d
                # m 填 1，suffix 随便填
                ans += pow10
            elif M == d:
                # 3. prefix = max_prefix 且 M = d
                # m 填 d，suffix 可以填 [0, max_suffix] 中的任意整数
                max_suffix = n % pow10
                ans += max_suffix + 1

            pow10 *= 10

        return ans

    def digitsCount(self, d: int, low: int, high: int) -> int:
        return self.calc(high, d) - self.calc(low - 1, d)
''',
    call='Solution().digitsCount(1, 13, 138)',
    expect=68,
    views=[
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='string', var=lambda S: str(S['n']) if 'n' in S else '', label='n 的各个数位（蓝 = 当前枚举的 m 位）', cell=100,
             color=_col, h=190),
        dict(type='text', fn=lambda S: (f"累计 `ans = {S['ans']}`" if 'ans' in S and 'pow10' in S else ''), size=30, h=70),
    ],
    watch=['d', 'n', 'pow10', 'max_prefix', 'M', ('ans', 'ans', 'green')],
    skip=['ans = 0', 'pow10 = 1', 'max_prefix =', 'M = n'],
    captions={
        'while pow10 <= n': lambda S, B, r: (f'`pow10 = {S.pow10} ≤ n = {S.n}`：还有数位没枚举，继续' if S.pow10 <= S.n
                                             else f'`pow10 = {S.pow10} > n = {S.n}`：数位用完，退出循环'),
        'ans += (max_prefix': '情况 1：前缀 `< {max_prefix}` 时低位随便填，`m` 填 `d`，共 `({max_prefix} − {int(d == 0)}) × {pow10}` 个 → `ans = {ans}`'
                              '{"（d = 0：扣掉前导零）" if d == 0 else ""}',
        'if M > d': lambda S, B, r: (f'`M = {S.M} > d = {S.d}`：前缀取满时 `m` 也能填 `d`，且 suffix 随便填' if S.M > S.d
                                     else f'`M = {S.M}` 不大于 `d = {S.d}`：先看是否相等'),
        'elif M == d': lambda S, B, r: (f'`M = {S.M} == d = {S.d}`：`m` 填 `d` 受 suffix ≤ n 的约束' if S.M == S.d
                                        else f'`M = {S.M} < d = {S.d}`：`m` 填不了 `d`（会超过 n），这一类没有贡献'),
        'ans += pow10': '`suffix` 在 `[0, {pow10-1}]` 随便填：`ans += {pow10}` → `ans = {ans}`',
        'max_suffix = n % pow10': '低位上限 `max_suffix = {max_suffix}`',
        'ans += max_suffix + 1': 'suffix 只能填 `[0, {max_suffix}]`：`ans += {max_suffix} + 1` → `ans = {ans}`',
        'pow10 *= 10': '`m` 上移一位：`pow10 = {pow10}`',
        'return ans': '`calc` 返回 `{ret}`',
        'return self.calc(high, d)': '`calc(high, d) − calc(low−1, d)`：先算 `high = {high}`，再算 `low − 1 = {low-1}`，相减',
    },
    cards=dict(
        one_liner='区间计数拆成前缀相减，再逐位统计 d 出现几次',
        complexity='时间 `O(log high)`，空间 `O(1)`',
        problem=['给定数字 `d`（0–9）和区间 `[low, high]`，数出 `d` 在区间内所有整数里==一共出现了多少次==',
                 '示例：`d = 1, low = 13, high = 138` → `68`',
                 '`d` 是数位，不是整数；`10` 里出现一次 `1`'],
        quote='拆分成 [1,high] 中的数字 d 的个数，以及 [1,low−1] 中的数字 d 的个数，二者相减，即为答案。……如果 prefix=0 且 m=0，那么 m 是前导零，不能计入。减去这种情况即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数字写成 `prefix | m | suffix`，`m` 是要看的那一位，逐位枚举 `m`',
              '`prefix` 小于 n 的前缀：低位不受约束，`m` 填 `d`，suffix 随便填',
              '`prefix` 等于 n 的前缀：看 n 在这一位的数字 `M` 与 `d` 的大小，分三类处理'],
        summary=['时间 `O(log high)`：每位只做 O(1) 计算，循环 `log10 n` 次',
                 '易错：`d = 0` 要扣前导零 `(max_prefix − 1)`；`calc(low−1)` 里 `low−1` 可能为 0',
                 '同类：233. 数字 1 的个数（本题 d = 1 的情形）；也可用数位 DP 做'],
    ),
)
