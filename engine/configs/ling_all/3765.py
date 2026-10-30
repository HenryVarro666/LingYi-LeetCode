def _kind(S):
    """x 当前对应前缀 / 后缀 / 整个数（只靠 x 和 s 推断，不依赖会被 is_prime 里的 i 遮住的外层 i）"""
    s, x = S.get('s'), S.get('x')
    if not isinstance(s, str) or x is None:
        return None
    k = len(str(x))
    if x == int(s):
        return 'both', k
    if x == int(s[:k]):
        return 'pre', k
    if x == int(s[-k:]):
        return 'suf', k
    return None


def _col(S, k, v):
    r = _kind(S)
    if r is None:
        return None
    kd, m = r
    n = len(S['s'])
    if kd == 'both':
        return 'green'
    if kd == 'pre' and k < m:
        return 'blue'
    if kd == 'suf' and k >= n - m:
        return 'pink'
    return None


def _top(S):
    r = _kind(S)
    if r is None:
        return ''
    kd, m = r
    if kd == 'both':
        return f"整个数 `{S['x']}`：既是最长的前缀，也是最长的后缀"
    if kd == 'pre':
        return f"前缀 `s[:{m}] = {S['s'][:m]}`（蓝）"
    return f"后缀 `s[{len(S['s']) - m}:] = {S['s'][-m:]}`（粉）"


CONFIG = dict(
    num=3765, title='完全质数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='枚举前后缀 + 试除到 sqrt',
    tags=['灵神题单', '难度分 1378'],
    code='''
def is_prime(n: int) -> bool:
    for i in range(2, isqrt(n) + 1):
        if n % i == 0:
            return False
    return n >= 2  # 1 不是质数

class Solution:
    def completePrime(self, num: int) -> bool:
        s = str(num)
        for i in range(len(s)):
            # 前缀
            x = int(s[:i + 1])
            if not is_prime(x):
                return False

            # 后缀
            x = int(s[i:])
            if not is_prime(x):
                return False

        return True
''',
    call='Solution().completePrime(23)',
    expect=True,
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='string', var='s', label='s = str(num)（蓝 = 前缀，粉 = 后缀）', cell=120,
             color=_col, h=230),
        dict(type='text', fn=lambda S: (f"`is_prime({S['n']})`：试除 `2 ~ isqrt({S['n']}) = {S['n'] and __import__('math').isqrt(S['n'])}`"
                                         if 'n' in S.get('_inner', {}) else ''), size=26),
    ],
    watch=['x'],
    captions={
        'for i in range(2, isqrt(n) + 1)': '试除 `i = {i}`（只需试到 `isqrt({n}) = {isqrt(n)}`，更大的因子必有一个更小的搭档）',
        'if n % i == 0': '`{n} % {i} = {n % i}` → {"==整除，不是质数==" if n % i == 0 else "不整除，继续"}',
        'return False': lambda S, B, r: (f'`{S.n}` 有因子 `{S.i}` → 不是质数' if 'n' in S._inner
                                         else '有一个前缀或后缀不是质数 → ==完全质数不成立==，返回 `False`'),
        'return n >= 2': lambda S, B, r: (f'`n = {S.n} < 2`：==1 不是质数== → `False`' if S.n < 2
                                          else f'没有 `2 ~ isqrt({S.n})` 的因子 → `{S.n}` 是质数'),
        's = str(num)': '转成字符串 `"{s}"`，前缀 / 后缀用切片取',
        'for i in range(len(s))': '`i = {i}`：同时检查前缀 `s[:{i + 1}]` 和后缀 `s[{i}:]`',
        'x = int(s[:i + 1])': '前缀（前 `{i + 1}` 位）：`x = {x}`',
        'x = int(s[i:])': '后缀（从第 `{i}` 位起）：`x = {x}`',
        'if not is_prime(x)': '`x = {x}` 是质数吗？不是的话，整个数立刻判 `False`',
        'return True': '每个前缀、后缀都是质数 → 完全质数，返回 `True`',
    },
    cards=dict(
        one_liner='枚举每个前缀和后缀，逐个试除判质数',
        complexity='时间 `O(√num)`，空间 `O(log num)`',
        problem=['若 `num` 的==每个前缀和每个后缀==都是质数，则称为完全质数',
                 '前缀 = 前 `k` 位，后缀 = 后 `k` 位；单个数字只有是质数才算',
                 '示例：`23` 的前缀 2、23，后缀 3、23 都是质数 → `true`；`39` → `false`'],
        quote='如果 n 不能被 √n 以内的（大于 1 的）整数整除，但可以被大于 √n 的整数 d 整除，那么必然还有一个数 n/d 也能整除 n……矛盾。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`s = str(num)`，第 `i` 轮取前缀 `s[:i+1]` 和后缀 `s[i:]`',
              '判质数只需试除到 `isqrt(n)`：大因子必有小搭档',
              '任何一个不是质数就立刻返回 `False`'],
        summary=['时间 `O(√num)`：最大那个数的试除次数占主导，空间 `O(log num)`（字符串）',
                 '易错：==1 不是质数==，`is_prime` 末尾 `return n >= 2`',
                 '`int(s[i:])` 会自动忽略前导零，此时后缀位数其实更少，但题目保证 `num` 无前导零',
                 '`isqrt` 来自 `math`，Python 3.8+ 可用'],
    ),
)
