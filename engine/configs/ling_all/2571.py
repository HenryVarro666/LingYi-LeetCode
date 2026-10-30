def _b(x, w=8):
    return format(x, 'b').zfill(w)


def _fn(S):
    if 'n' not in S:
        return ''
    n = S['n']
    s = f"n = `{_b(n)}`（{n}）　已操作 `ans` = =={S.get('ans', 0)}=="
    if 'lb' in S and n:
        s += f"　　lowbit = `{_b(S['lb'])}`"
    return s


def _color(S, i, v):
    n = S.get('n')
    if n is None:
        return None
    pos = 7 - i
    lb = S.get('lb')
    if lb and (lb >> pos) & 1:
        return 'yellow'
    return 'green' if v == '1' else None


CONFIG = dict(
    num=2571, title='将整数减少到零需要的最少操作数', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='从低位贪心：连续 1 加、单个 1 减',
    tags=['灵神题单·位运算', '灵神题单·贪心与思维', '难度分 1649'],
    code='''
class Solution:
    def minOperations(self, n: int) -> int:
        ans = 1
        while n & (n - 1):  # 不是 2 的幂次
            lb = n & -n
            if n & (lb << 1): n += lb  # 多个连续 1
            else: n -= lb  # 单个 1
            ans += 1
        return ans
''',
    call='Solution().minOperations(39)',
    expect=3,
    views=[
        dict(type='text', fn=_fn, size=30, h=80),
        dict(type='string', var=lambda S: _b(S['n']) if 'n' in S else '', color=_color, label='n 的二进制（黄 = lowbit）', h=220),
    ],
    watch=['n', ('lb', "S.get('lb')", 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = 1': '先记 1 次：最后剩下的那个 2 的幂次，还要 ==1 次操作== 减掉',
        'while n & (n - 1)': lambda S, B, r: (f'`n & (n-1) = {S.n & (S.n - 1)}` ≠ 0：还有不止一个 1，继续消除' if S.n & (S.n - 1)
                                              else f'`n = {S.n}` 是 2 的幂次（只剩一个 1）：减一次就到 0，结束循环'),
        'lb = n & -n': '最低位的 1：`lowbit = {lb}`。它不受别的位影响，==优先消除它==',
        'if n & (lb << 1)': lambda S, B, r: (f'`lowbit` 的上一位也是 1（连续的 1）→ ==加== `lowbit`，一次消掉整段：`n` → {S.n}' if S.n != B.n and S.n > B.n
                                             else f'`lowbit` 的上一位是 0（单个 1）→ ==减== `lowbit`，一次消掉这个 1'),
        'n += lb': '连续 1：`n += {lb}` → `{n}`，进位把一整段 1 变成一个更高位的 1',
        'n -= lb': '单个 1：`n -= {lb}` → `{n}`，直接去掉这个 1（加的话会进位产生新的 1，不划算）',
        'ans += 1': '本轮用掉 1 次操作：`ans` = =={ans}==',
        'return ans': '循环里的操作 + 最后减掉 2 的幂次的 1 次 = =={ans}==',
    },
    cards=dict(
        one_liner='先消最低位的 1：连续 1 用加法，单个 1 用减法',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['正整数 `n`，每次可以 ==加上或减去一个 2 的幂==',
                 '求把 `n` 变成 0 的最少操作数',
                 '示例：`39` → `3`（+1、−8、−32）'],
        quote='贪心的策略是：如果有多个连续 1，那么采用加法是更优的，可以一次消除多个 1；否则对于单个 1，减法更优。',
        quote_src='—— 灵茶山艾府题解',
        idea=['高位的 1 会被低位的加减影响，最低位的 1 没有这个约束 → ==优先消 lowbit==',
              '`lb = n & -n` 取最低位的 1，看它上面一位是不是 1',
              '循环到只剩一个 1（2 的幂次）停下，最后再 +1 次'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '循环条件是 `n & (n-1)`，剩下 2 的幂次时直接算 1 次，所以 `ans` 初值为 1',
                 '题解另给位运算优化：答案 = `(3*n ^ n).bit_count()`，一行搞定',
                 '另附记忆化搜索：`1 + min(dfs(x+lb), dfs(x-lb))`，两种操作都试'],
    ),
)
