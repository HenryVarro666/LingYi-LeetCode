def _txt(S):
    if 'n' not in S or 'M' not in S:
        return ''
    n, M = S['n'], S['M']
    if n < M // 10:
        return f'`n = {n} < M // 10 = {M // 10}`：剩下的数字不足 `k` 位，结束'
    x = n % M
    return f'`n % M = {n} % {M}` = =={x}==（`n` 末尾 `k` 位）；`num % x` = {S["num"] % x if x else "—"}'


CONFIG = dict(
    num=2269, title='找到一个数字的 K 美丽值', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='数学 · 取模取末尾 k 位',
    tags=[],
    code='''
class Solution:
    def divisorSubstrings(self, num: int, k: int) -> int:
        M = 10 ** k
        ans = 0
        n = num
        while n >= M // 10:
            x = n % M
            if x > 0 and num % x == 0:
                ans += 1
            n //= 10
        return ans
''',
    call='Solution().divisorSubstrings(430043, 2)',
    expect=2,
    skip=['n = num'],
    views=[
        dict(type='string', var=lambda S: str(S['num']), label='num 的各位（亮 = 还留在 n 里的数字，黄框 = n 的末尾 k 位）', cell=90,
             window=('len(str(n)) - k', 'len(str(n)) - 1'),
             dim=lambda S, i, v: 'n' in S and i >= len(str(S['n'])) if S.get('n', 0) > 0 else False, h=230),
        dict(type='text', fn=_txt, size=28, h=70),
    ],
    watch=[('M', 'M', 'blue'), ('n', 'n', 'pink'), ('x', 'x', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'M = 10 ** k': '`M = 10^k = {M}`：`n % M` 恰好取出 `n` 的末尾 `k` 位',
        'ans = 0': '`ans` 统计 K 美丽值',
        'while n >= M // 10': lambda S, B, r: ('`n = {0} ≥ M // 10 = {1}`：`n` 至少还有 `k` 位，继续'.format(S.n, S.M // 10) if S.n >= S.M // 10
                                                else '`n = {0} < M // 10 = {1}`：`n` 不足 `k` 位，没有更多子串，结束'.format(S.n, S.M // 10)),
        'x = n % M': '`x = {n} % {M} = {x}`：这是当前最右边的长为 `k` 的子串',
        'if x > 0 and num % x == 0': lambda S, B, r: (
            '`x = 0`：0 不能整除任何数 → 不计数' if S.x == 0
            else '`num % x = {0} % {1} = {2}` → {3}'.format(S.num, S.x, S.num % S.x, '==整除，是 K 美丽子串==' if S.num % S.x == 0 else '不能整除')),
        'ans += 1': '`ans` → {ans}',
        'n //= 10': '去掉 `n` 的个位：`n` → {n}，下一轮取左边一位开始的子串',
        'return ans': '子串都检查完，返回 `{ans}`',
    },
    cards=dict(
        one_liner='用 n % 10^k 取末尾 k 位，每次去掉个位，滑过所有子串',
        complexity='时间 `O(n - k)`（`n` 为位数），空间 `O(1)`',
        problem=['`num` 的 ==k 美丽值==：`num` 中长为 `k`、且能整除 `num` 的子串个数',
                 '子串允许有前导 0；`0` 不能整除任何数',
                 '示例：`num = 430043`，`k = 2` → `2`（`43` 出现两次且能整除）'],
        quote='设 m=10^k=100。计算 n mod m，这是最右边的长为 k 的子串。判断是否合法。然后去掉 n 的个位数，也就是把 n 除以 10 下取整。……n 的十进制长度不足 k，结束。',
        quote_src='—— 灵茶山艾府题解（方法二：数学）',
        idea=['不转字符串：`n % 10^k` 就是 `n` 末尾的 `k` 位数字',
              '检查完这个子串，`n //= 10` 去掉个位，窗口就往左滑一格',
              '`n >= 10^(k-1)` 时 `n` 至少还有 `k` 位；否则结束'],
        summary=['时间 `O(n - k)`，空间 `O(1)`，`n` 是 `num` 的位数',
                 '易错：`x = 0` 时不能做 `num % x`，要先判 `x > 0`',
                 '易错：循环条件是 `n >= M // 10`，不是 `n > 0`，否则会算到不足 k 位的数',
                 '方法一：转字符串，枚举长为 `k` 的子串 `int(s[i-k:i])`，同样判断 `x > 0`'],
    ),
)
