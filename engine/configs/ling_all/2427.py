def _marks(S):
    g = S['g']
    seq = []
    for d in range(1, g + 1):
        if d * d > g:
            break
        if g % d == 0:
            seq.append(d)
            if d * d < g:
                seq.append(g // d)
    return set(seq[:S['ans']])


def _txt(S):
    if 'i' not in S:
        return '公因子一定整除 `gcd(a, b)`：只需要数 `g` 的因数'
    g, i = S['g'], S['i']
    if i * i > g:
        return f'`i × i = {i * i} > {g}`：成对的因数都找完了，共 =={S["ans"]}== 个'
    return f'试除 `i = {i}`：`{g} % {i} = {g % i}`，成对因数 `i` 和 `g / i` 一次数两个'


CONFIG = dict(
    num=2427, title='公因子的数目', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='gcd + 枚举因子对',
    tags=['数论', '难度分 1172'],
    code='''
class Solution:
    def commonFactors(self, a: int, b: int) -> int:
        g = gcd(a, b)
        ans, i = 0, 1
        while i * i <= g:
            if g % i == 0:
                ans += 1  # i 是公因子
                if i * i < g:
                    ans += 1  # g/i 是公因子
            i += 1
        return ans
''',
    call='Solution().commonFactors(20, 30)',
    expect=4,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var=lambda S: list(range(1, S['g'] + 1)) if 'g' in S else [], label='1 … g（绿 = 已经数到的公因子）',
             pointers={'i': 'blue'}, color=lambda S, k, v: 'green' if v in _marks(S) else None,
             dim=lambda S, k, v: 'i' in S and v * v <= S['g'] and v < S['i'] and v not in _marks(S), cell=84, h=230),
    ],
    watch=['g', ('i', 'i', 'blue'), ('ans', 'ans', 'green')],
    skip=[],
    captions={
        'g = gcd': '`g = gcd({a}, {b}) = {g}`：==公因子 = g 的因数==，范围一下缩小到 g',
        'ans, i = 0, 1': '计数 `ans = 0`，从 `i = 1` 开始试除',
        'while i * i <= g': lambda S, B, r: (f'`{S.i}² = {S.i * S.i} ≤ {S.g}`，继续' if S.i * S.i <= S.g else f'`{S.i}² = {S.i * S.i} > {S.g}`：更大的因数都已经作为 `g/i` 数过了 → 结束'),
        'if g % i == 0': '`{g} % {i} = {g % i}` → ' + '{"整除，i 是公因子" if g % i == 0 else "不整除，跳过"}',
        '# i 是公因子': '`i = {i}` 是公因子 → `ans = {ans}`',
        'if i * i < g': lambda S, B, r: (f'`{S.i}² < {S.g}`：`g/i = {S.g // S.i}` 和 `i` 不是同一个数 → 还要再数一个' if S.i * S.i < S.g else f'`{S.i}² = {S.g}`：`g/i` 就是 `i` 自己，不能重复数'),
        '# g/i 是公因子': '`g/i = {g // i}` 也是公因子 → `ans = {ans}`',
        'i += 1': '`i` → {i}',
        'return ans': '共 `{ret}` 个公因子',
    },
    cards=dict(
        one_liner='公因子就是 gcd 的因数：只枚举到 sqrt(g)，每次成对数',
        complexity='时间 `O(√min(a,b))`，空间 `O(1)`',
        problem=['给两个正整数 `a`、`b`，求能同时整除它们的 `x` 的个数',
                 '示例：`a = 12, b = 6` → `4`（1、2、3、6）',
                 '本视频：`a = 20, b = 30` → `4`（1、2、5、10）'],
        quote='枚举因子，挨个判断能否整除 a 和 b。改进方案是==枚举 a 和 b 的最大公因数的因子==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x` 同时整除 `a`、`b` ⇔ `x` 整除 `gcd(a, b)`',
              '`g` 的因数成对出现：`i` 和 `g / i`，所以 `i` 只枚举到 `i² ≤ g`',
              '`i² = g` 时两个因数相同，只能数一次'],
        summary=['时间 `O(√min(a,b))`，空间 `O(1)`',
                 '易错：`i * i == g` 时 `g/i` 与 `i` 相同，不要数两次',
                 '朴素写法：枚举 `1..min(a,b)` 逐个判断，数据小也能过',
                 '同类：因数个数、完全数、三除数等枚举因子题'],
    ),
)
