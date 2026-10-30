S0 = '223'


def _isp(n):
    return n >= 2 and all(n % i for i in range(2, int(n ** 0.5) + 1))


def _table(s):
    """(x, 此刻 primes) -> (i, j)，用来在 is_prime 里（外层 i 被遮住）还原当前子串"""
    t, primes = {}, set()
    for i in range(len(s)):
        x = 0
        for j in range(i, len(s)):
            x = x * 10 + int(s[j])
            t[(x, frozenset(primes))] = (i, j)
            if _isp(x):
                primes.add(x)
                t[(x, frozenset(primes))] = (i, j)
    return t


_T = _table(S0)


def _span(S):
    inner = S.get('_inner', {})
    ln = S.get('_line')
    if 'n' in inner:                       # 在 is_prime 里
        try:
            return _T.get((S['x'], frozenset(S['primes'])))
        except Exception:
            return None
    if ln in (13, 14, 15) and S.get('x'):
        i = S['i']
        return (i, i + len(str(S['x'])) - 1)
    return None


def _col(S, k, v):
    sp = _span(S)
    if sp and sp[0] <= k <= sp[1]:
        return 'green' if (S.get('_line') == 15) else 'blue'
    if S.get('_line') in (10, 11, 12) and 'n' not in S.get('_inner', {}) and k == S.get('i'):
        return 'yellow'
    return None


def _top(S):
    sp = _span(S)
    if sp is None:
        return ''
    return f"当前子串 `s[{sp[0]}:{sp[1] + 1}] = {S['s'][sp[0]:sp[1] + 1]}` → `x = {S['x']}`"


def _tryi(S, B):
    a, b = S['_inner'], B['_inner']
    if 'i' not in a or ('i' in b and b['i'] == a['i']):
        raise ValueError  # 循环结束 → 用默认字幕
    return f"试除 `i = {a['i']}`（只需试到 `isqrt({a['n']})`）"


def _fin(S):
    if S.get('_line') == 16 and 'primes' in S:
        a = sorted(S['primes'])
        return f"排序去重后 `{a}`，取最大的三个 `{a[-3:]}`，求和"
    return ''


CONFIG = dict(
    num=3556, title='最大质数子字符串之和', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='枚举子串 + 试除判质数 + 集合去重',
    tags=['灵神题单', '难度分 1440'],
    code='''
def is_prime(n: int) -> bool:
    for i in range(2, isqrt(n) + 1):
        if n % i == 0:
            return False
    return n >= 2

class Solution:
    def sumOfLargestPrimes(self, s: str) -> int:
        primes = set()
        for i in range(len(s)):
            x = 0
            for ch in s[i:]:
                x = x * 10 + int(ch)
                if is_prime(x):
                    primes.add(x)
        return sum(sorted(primes)[-3:])
''',
    call=f'Solution().sumOfLargestPrimes("{S0}")',
    expect=249,
    max_steps=68,
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='string', var='s', label='s（蓝 = 当前子串，绿 = 刚加入集合）', cell=110, color=_col, h=220),
        dict(type='set', var='primes', label='primes（去重的集合）', h=150),
        dict(type='text', fn=_fin, size=26),
    ],
    watch=['x', ('primes', 'sorted(primes)', 'green')],
    captions={
        'for i in range(2, isqrt(n) + 1)': lambda S, B, r: _tryi(S, B),
        'if n % i == 0': '`{n} % {i} = {n % i}` → {"==整除，不是质数==" if n % i == 0 else "不整除，继续"}',
        'return False': '`{n}` 有因子 `{i}` → 不是质数',
        'return n >= 2': lambda S, B, r: (f'`n = {S.n} < 2`：==1 不是质数== → `False`' if S.n < 2
                                          else f'试除到 `isqrt({S.n})` 没有因子 → `{S.n}` 是质数'),
        'primes = set()': '用集合存质数：同一个质数出现多次也只算一次',
        'for i in range(len(s))': '枚举子串的起点 `i = {i}`',
        'x = 0': '`x` 存当前子串对应的整数，从空串（0）开始',
        'for ch in s[i:]': '起点固定，向右一位一位延长子串',
        'x = x * 10 + int(ch)': '子串末尾接上 `{ch}`：`{B.x} × 10 + {ch}` = =={x}==（自动忽略前导零）',
        'if is_prime(x)': lambda S, B, r: (f'`{S.x}` 是质数 → ==加入集合==' if r is not None and False else f'`{S.x}` 是质数吗？'),
        'primes.add(x)': '`{x}` 是质数，加入集合（已有则无变化）：`primes = {sorted(primes)}`',
        'return sum': '集合里所有质数排序，取最大的三个求和 → `{sorted(primes)[-3:]}` 之和 = =={ret}==',
    },
    cards=dict(
        one_liner='枚举所有子串，是质数就放进集合，最后取最大的三个',
        complexity='时间 `O(10^{n/2})`，空间 `O(n²)`',
        problem=['字符串 `s` 的所有子串（转成整数，忽略前导零）里，找==三个最大的不同质数==求和',
                 '不足三个就求所有不同质数之和；同一个质数只算一次',
                 '示例：`"12234"` → `1223 + 223 + 23 = 1469`；本视频用 `"223"` → `249`'],
        quote='本题可以枚举所有 n(n+1)/2 个子串，判断子串对应的十进制数是否为质数。把质数加到一个列表中，排序去重后，计算前三大之和，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['外层枚举起点 `i`，内层向右延长：`x = x * 10 + int(ch)` 一路算出各个子串的值',
              '`is_prime` 试除到 `isqrt(n)`，是质数就加入 `set`，顺便去重',
              '最后 `sorted(primes)[-3:]` 取最大三个（不足三个就是全部）'],
        summary=['时间 `O(10^{n/2})`：长为 k 的子串试除 `10^{k/2}` 次，错位相减后由最长子串主导；空间 `O(n²)`',
                 '易错：==1 不是质数==；同一个质数要去重（用集合）',
                 '`sorted(primes)[-3:]` 在不足三个时直接给出全部，不用特判',
                 '另一种写法：先筛出 10^5 以内的质数，再用质数试除，更快，其余逻辑不变'],
    ),
)
