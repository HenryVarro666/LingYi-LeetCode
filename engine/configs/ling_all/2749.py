def _t1(S):
    if 'k' not in S or 'x' not in S:
        return ''
    return f'k = =={S["k"]}==，x = num1 − num2×k = {S["num1"]} − ({S["num2"]})×{S["k"]} = =={S["x"]}==（二进制 `{S["x"]:b}`）'


def _t2(S):
    if 'x' not in S or S.get('_line', 0) < 5:
        return ''
    x, k = S['x'], S['k']
    return f'x 能拆成的 2 的幂个数：下界 `{x.bit_count()}`（1 的个数）～ 上界 `{x}`（全拆成 1）'


def _t3(S):
    if 'x' not in S or S.get('_line', 0) < 5:
        return ''
    x, k = S['x'], S['k']
    ok = x.bit_count() <= k <= x
    return f'k = {k} {"在" if ok else "不在"}区间 [{x.bit_count()}, {x}] 内 → ' + ('==能拆出恰好 k 个==' if ok else '继续试下一个 k')


CONFIG = dict(
    num=2749, title='得到整数零需要执行的最少操作数', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='枚举 k + 拆分上下界',
    tags=['位运算', '贪心与思维', '难度分 2132'],
    code='''
class Solution:
    def makeTheIntegerZero(self, num1: int, num2: int) -> int:
        for k in count(1):  # 枚举 k=1,2,3,...
            x = num1 - num2 * k
            if k > x:
                return -1
            if k >= x.bit_count():
                return k
''',
    call='Solution().makeTheIntegerZero(3, -2)',
    expect=3,
    setup='from itertools import count',
    views=[
        dict(type='text', fn=_t1, size=28, h=70),
        dict(type='text', fn=_t2, size=28, h=70),
        dict(type='text', fn=_t3, size=28, h=70),
    ],
    watch=['num1', 'num2', 'k', 'x'],
    captions={
        'for k in count': lambda S, B, r: f'枚举操作次数 `k = {S.k}`：做 k 次后，num1 变成 `num1 − num2×k` 再减去 k 个 2 的幂',
        'x = num1': '`x = {num1} − ({num2})×{k} = {x}`：问题变成「x 能否拆成恰好 {k} 个 2 的幂」',
        'if k > x': lambda S, B, r: (f'`k = {S.k} > x = {S.x}`：x 最多拆成 x 个 1，不够 k 个 → 以后 k 更大也不行，返回 -1' if S.k > S.x
                                     else f'`k = {S.k} ≤ x = {S.x}`：没超过上界，继续看下界'),
        'return -1': '上界都不满足，无解：返回 `-1`',
        'if k >= x.bit_count()': lambda S, B, r: (f'`k = {S.k} ≥ popcount = {S.x.bit_count()}`：至少需要 {S.x.bit_count()} 个幂，k 够了；区间内任意个数都能拆 → 找到最小的 k，==答案 {S.k}=='
                                                   if S.k >= S.x.bit_count() else f'`k = {S.k} < popcount = {S.x.bit_count()}`：拆不出这么少，k 太小，试下一个'),
        'return k': '返回最小的 `k = {k}`',
    },
    cards=dict(
        one_liner='做 k 次后，剩下的值能否拆成恰好 k 个 2 的幂',
        complexity='时间 `O(log)`（k ≤ 36），空间 `O(1)`',
        problem=['每步选 `i ∈ [0,60]`，`num1 -= 2^i + num2`',
                 '求让 `num1` 变成 0 的最少步数，不可能返回 -1',
                 '示例：`num1=3, num2=-2` → `3`'],
        quote='能否把 num1 变成 0，等价于：能否把 num1 − num2·k 拆分成恰好 k 个 2 的幂之和？',
        quote_src='—— 灵茶山艾府题解',
        idea=['设 `x = num1 − num2·k`，要把 x 拆成恰好 k 个 2 的幂',
              '下界 = x 二进制 1 的个数，上界 = x（全拆成 1），中间每个数都能拆出',
              '从小到大枚举 k，`k > x` 就无解，`k ≥ popcount(x)` 就是答案'],
        summary=['时间：k 最多约 36，几乎 `O(1)`；空间 `O(1)`',
                 '`x.bit_count()` 需要 Python 3.10+',
                 '易错：`k > x` 要先判（上界），再判下界',
                 '`num2 + 1 ≤ 0` 时上界恒成立，一定有解；否则可能无解'],
    ),
)
