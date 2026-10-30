S0, N0 = '10111000', 8
# 本例中长为 3 和长为 4 的窗口都两两不同，所以可由 x 反推窗口位置（代码里没有下标变量）


def _win(S):
    if 'seen' not in S or 'x' not in S or S['_line'] not in (16, 17, 20, 21, 22):
        return None
    k, x, s = S['k'], S['x'], S['s']
    if S['_line'] == 16:
        return 0, k - 2
    for j in range(len(s) - k + 1):
        if int(s[j:j + k], 2) == x:
            return j, j + k - 1
    return 0, k - 2


def _wl(S):
    w = _win(S)
    return w and w[0]


def _wr(S):
    w = _win(S)
    return w and w[1]


def _txt(S):
    if 'lower' not in S:
        if 'k' in S:
            return f"`n = {S['n']}` = `{S['n']:b}`：二进制长 `k + 1 = {S['k'] + 1}`，只需检查长为 `k` 和 `k + 1` 的两组"
        return '只需检查两组：`[n/2 + 1, 2^k − 1]`（长 k）和 `[2^k, n]`（长 k+1）'
    k, lo, hi = S['k'], S['lower'], S['upper']
    if lo > hi:
        return f'长为 `{k}` 的组：`[{lo}, {hi}]` 为空，不用检查'
    want = ' '.join(f'`{v:b}`' if v not in S.get('seen', ()) else f'=={v:b}==' for v in range(lo, hi + 1))
    return f'长为 `{k}` 的组 `[{lo}, {hi}]`：{want}（高亮 = 已找到）'


CONFIG = dict(
    num=1016, title='子串能表示从 1 到 N 数字的二进制串', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='数学分析 + 两个定长滑窗',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution:
    def queryString(self, s: str, n: int) -> bool:
        if n == 1:
            return '1' in s

        m = len(s)
        k = n.bit_length() - 1
        if m < max(n - (1 << k) + k + 1, (1 << (k - 1)) + k - 1):
            return False

        # 对于长为 k 的在 [lower, upper] 内的二进制数，判断这些数 s 是否都有
        def check(k: int, lower: int, upper: int) -> bool:
            if lower > upper: return True
            seen = set()
            mask = (1 << (k - 1)) - 1
            x = int(s[:k - 1], 2)
            for c in s[k - 1:]:
                # & mask 可以去掉最高比特位，从而实现滑窗的「出」
                # << 1 | int(c) 即为滑窗的「入」
                x = ((x & mask) << 1) | int(c)
                if lower <= x <= upper:
                    seen.add(x)
            return len(seen) == upper - lower + 1

        return check(k, n // 2 + 1, (1 << k) - 1) and check(k + 1, 1 << k, n)
''',
    call=f'Solution().queryString({S0!r}, {N0})',
    expect=True,
    views=[
        dict(type='string', var='s', label='s（框 = 当前长为 k 的窗口）', h=210, cell=96, window=(_wl, _wr)),
        dict(type='text', h=90, size=28, fn=_txt),
        dict(type='set', var='seen', label='seen（落在 [lower, upper] 内的窗口值）', h=150, font=32,
             fmt=lambda v: f'{v:b} ({v})'),
        dict(type='calls', h=130),
    ],
    watch=[('k', 'k'), ('lower', 'lower'), ('upper', 'upper'), ('x', 'x', 'orange'), ('mask', 'mask')],
    captions={
        'if n == 1': '`n = {n}` 不是 1，不用特判',
        'm = len(s)': '`m = len(s) = {m}`',
        'k = n.bit_length() - 1': '`n = {n}` 的二进制 `{n:b}` 长 `{k + 1}` → `k = {k}`',
        'if m < max': lambda S, B, r: (f'长 k+1 的数要 `≥ {S.n - (1 << S.k) + S.k + 1}` 个字符，长 k 的要 `≥ {(1 << (S.k - 1)) + S.k - 1}` 个；'
                                       f'`m = {S.m}` 够了' if S.m >= max(S.n - (1 << S.k) + S.k + 1, (1 << (S.k - 1)) + S.k - 1)
                                       else '`m` 太短，s 不可能装下这么多不同的子串'),
        'def check': '`check(k, lower, upper)`：用长为 `k` 的滑窗，看 `[lower, upper]` 是否都出现',
        'if lower > upper': lambda S, B, r: ('`lower > upper`：区间为空，直接 True' if S.lower > S.upper
                                             else f'检查长为 `{S.k}` 的 `[{S.lower}, {S.upper}]`'),
        'seen = set()': '`seen` 记录找到了哪些数',
        'mask = (1 << (k - 1)) - 1': '`mask = {mask:b}`：保留低 `k − 1` 位',
        'x = int(s[:k - 1], 2)': '先读入前 `k − 1` 个字符：`x = {x:b}`',
        'for c in s[k - 1:]': '窗口右移一格（读完 s 就结束）',
        'x = ((x & mask)': '`& mask` 去掉最高位（出），`<< 1 | {c}`（入）→ 窗口 `{x:0{k}b}` = {x}',
        'if lower <= x <= upper': lambda S, B, r: (f'`{S.lower} ≤ {S.x} ≤ {S.upper}`：是要找的数' if S.lower <= S.x <= S.upper
                                                   else (f'`{S.x} < {S.lower}`：更小的数==已被保证==，不用管' if S.x < S.lower
                                                         else f'`{S.x} > {S.upper}`：超出范围，不是要找的')),
        'seen.add(x)': '记下 `{x}`，已找到 `{len(seen)}` / `{upper - lower + 1}` 个',
        'return len(seen) ==': '`len(seen) = {len(seen)}`，需要 `{upper - lower + 1}` 个 → `{ret}`',
        'return check(': lambda S, B, r: ('先查长为 k 的一组，再查长为 k+1 的一组（`and` 短路）' if r is None else f'两组都齐 → `{r}`'),
    },
    max_steps=70,
    cards=dict(
        one_liner='n 很大时 s 根本装不下，能装下时只需查最长的两组',
        complexity='时间 `O(m)`，空间 `O(min(m, n))`（m = len(s)）',
        problem=['给二进制串 `s` 和 `n`，判断 `1..n` 的二进制是否==都是== `s` 的子串',
                 '示例：`s = "0110", n = 3` → `true`；`n = 4` → `false`',
                 '本视频：`s = "10111000", n = 8` → `true`'],
        quote='如果 s 包含 [2^(k-1), 2^k-1] 内的所有二进制数，那么必然也包含 [2^(k-2), 2^(k-1)-1] 内的所有二进制数……所以只需要考虑 s 是否包含 [2^(k-1), 2^k-1] 和 [2^k, n] 内的所有二进制数即可。',
        quote_src='—— 灵茶山艾府题解（精确分析）',
        idea=['长 `k+1` 的数有 `n − 2^k + 1` 个，长 `k` 的有 `2^(k−1)` 个 → `m` 不够直接 False',
              '更短的数是长 k 的数右移得到的，==自动被包含==',
              '[2^k, n] 右移一位覆盖了 [2^(k−1), n/2]，所以长 k 的只查 `n/2 + 1` 起'],
        summary=['时间 `O(m)`：两个定长滑窗各扫一遍',
                 '易错：`n == 1` 时 `k = 0`，要特判',
                 '算法一：直接 `all(bin(i)[2:] in s ...)`，因为分析保证循环次数约 `2m` 才不超时',
                 '算法二：枚举 `s[i] = 1` 的起点往后扩，`x > n` 就停'],
    ),
)
