CONFIG = dict(
    num=2466, title='统计构造好字符串的方案数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='爬楼梯 DP + GCD 缩小规模',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1694'],
    setup='from math import gcd',
    code='''
class Solution:
    def countGoodStrings(self, low: int, high: int, zero: int, one: int) -> int:
        g = gcd(zero, one)
        low = (low - 1) // g + 1
        high //= g
        zero //= g
        one //= g

        MOD = 1_000_000_007
        f = [1] + [0] * high  # f[i] 表示构造长为 i 的字符串的方案数
        for i in range(1, high + 1):
            if i >= zero: f[i] = f[i - zero]
            if i >= one:  f[i] = (f[i] + f[i - one]) % MOD
        return sum(f[low:]) % MOD
''',
    call='Solution().countGoodStrings(3, 9, 2, 4)',
    expect=10,
    views=[
        dict(type='array', var='f', pointers={'i': 'blue'}, h=260,
             label='f[i]：构造长为 i 的字符串的方案数',
             color=lambda S, i, v: ('green' if S['_line'] >= 11 and i >= S['low'] else None)),
        dict(type='text', size=28, fn=lambda S: (f"缩小后：`low={S['low']}, high={S['high']}, zero={S['zero']}, one={S['one']}`（原 low=3, high=9, zero=2, one=4，g={S['g']}）" if 'g' in S and 'one' in S else '')),
        dict(type='text', size=28, fn=lambda S: (f"`f[{S['i']}] = f[{S['i']}-{S['zero']}] + f[{S['i']}-{S['one']}]`" if 'i' in S and 'f' in S and S['_line'] in (13, 14) else '')),
    ],
    watch=['g', 'low', 'high', 'zero', 'one', ('i', 'i', 'blue')],
    captions={
        'g = gcd': '`zero = 2` 和 `one = 4` 的最大公约数 `g = {g}`：所有长度都是 `g` 的倍数',
        'low = (low - 1)': '`low` 上取整：`ceil({B.low}/{g}) = ({B.low}-1)//{g}+1 = {low}`（长度不足的取不到）',
        'high //= g': '`high` 下取整：`{B.high}//{g} = {high}`',
        'zero //= g': '`zero` 缩小：`{B.zero}//{g} = {zero}`',
        'one //= g': '`one` 缩小：`{B.one}//{g} = {one}`；问题化为小规模爬楼梯',
        'f = [1]': '`f[0] = 1`：空串也算一种方案（什么也不做）；其余先填 0',
        'for i in range': lambda S, B, r: (f'算长为 `{S.i}` 的字符串方案数' if S.i <= S.high and B.get('i') != S.i else '`i` 走到 `high`，f 算完'),
        'if i >= zero': '`i = {i} ≥ zero = {zero}`？可在长 `{i-zero}` 的串后加 `zero` 个 0，`f[{i}] = f[{i-zero}] = {f[i]}`' if False else lambda S, B, r: (f'`i = {S.i} ≥ zero = {S.zero}`：末尾加 `zero` 个 0，直接赋值 `f[{S.i}] = f[{S.i - S.zero}] = {S.f[S.i]}`' if S.i >= S.zero else f'`i = {S.i} < zero = {S.zero}`：加不了 0，跳过'),
        'if i >= one': lambda S, B, r: (f'`i = {S.i} ≥ one = {S.one}`：末尾加 `one` 个 1，累加 `f[{S.i - S.one}]` → `f[{S.i}] = {S.f[S.i]}`' if S.i >= S.one else f'`i = {S.i} < one = {S.one}`：加不了 1，跳过'),
        'return sum': lambda S, B, r: f'长度在 `[{S.low}, {S.high}]` 的 f 之和：`sum(f[{S.low}:]) = {" + ".join(str(x) for x in S.f[S.low:])} = {r}`',
    },
    cards=dict(
        one_liner='每次加 zero 或 one 个字符：就是爬楼梯，再把长度 ÷ gcd',
        complexity='时间 `O(high/g)`，空间 `O(high/g)`',
        problem=['每步在末尾加 `zero` 个 `0` 或 `one` 个 `1`，求长度在 `[low, high]` 的不同字符串数',
                 '示例：`low=2, high=3, zero=1, one=2` → `5`',
                 '本视频：`low=3, high=9, zero=2, one=4` → `10`'],
        quote='每次可以爬 $zero$ 或 $one$ 个台阶，返回爬 $low$ 到 $high$ 个台阶的方案数。……得 $f[i] = f[i-zero] + f[i-one]$。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i]` = 长为 `i` 的构造方案数：末尾是 `zero` 个 0 或 `one` 个 1，两类互斥 → 加法原理',
              '`f[0] = 1`：什么都不做也算一种',
              '`zero`、`one` 的公因数 `g` 可以约掉：长度必是 `g` 的倍数，规模缩小 `g` 倍'],
        summary=['时间、空间都是 `O(high/g)`',
                 '易错点：==`f[0] = 1`==；`low` 要上取整、`high` 下取整',
                 '上取整公式：`ceil(a/b) = (a-1)//b + 1`',
                 '灵神还给了记忆化搜索（逐个 `dfs(i)` 求和）和不带 GCD 的递推写法，这里选最后的优化写法',
                 '同类题：70. 爬楼梯、2266. 统计打字方案数'],
    ),
)
