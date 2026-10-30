CONFIG = dict(
    num=3622, title='判断整除性', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='模拟 · 逐位取数',
    tags=[],
    code='''
class Solution:
    def checkDivisibility(self, n: int) -> bool:
        s, m = 0, 1
        x = n
        while x:
            x, d = divmod(x, 10)
            s += d
            m *= d
        return n % (s + m) == 0
''',
    call='Solution().checkDivisibility(99)',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: f"剩余 `x = {S['x']}`，已取出的最低位 `d = {S['d']}`" if 'd' in S and 'x' in S else (f"`n = {S['n']}`" if 'n' in S else ''), size=30),
        dict(type='text', fn=lambda S: f"数字和 `s = {S['s']}`，数字积 `m = {S['m']}`" if 's' in S and 'm' in S else '', size=30),
        dict(type='text', fn=lambda S: f"`s + m = {S['s'] + S['m']}`，`n % (s+m) = {S['n'] % (S['s'] + S['m'])}`" if S.get('_line') == 9 and S['s'] + S['m'] > 0 else '', size=30),
    ],
    watch=['n', 'x', 'd', ('s', 's', 'blue'), ('m', 'm', 'pink')],
    captions={
        's, m = 0, 1': '数字和从 0 开始，数字积从 1 开始（乘法的单位元）',
        'x = n': '拷贝一份 `x = {x}`，用它来逐位拆',
        'while x': lambda S, B, ret: (f"`x = {S.x}` 还没拆完" if S.x else '`x = 0`，所有数位都取完了'),
        'divmod': '`divmod(x, 10)`：商是去掉最低位，余数是最低位 → `x = {x}`，`d = {d}`',
        's += d': '数字和累加：`s = {s}`',
        'm *= d': '数字积累乘：`m = {m}`',
        'return': '`n % (s + m) = {n} % {s + m} = {n % (s + m)}` → ==能整除== 即 `{ret}`' ,
    },
    cards=dict(
        one_liner='模 10 取最低位、除 10 去掉最低位，顺手算和与积',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['正整数 `n`，判断它能否被「数字和 + 数字积」整除',
                 '示例：`99`：和 `18`，积 `81`，`99 % 99 == 0` → `true`；`23`：`5 + 6 = 11`，不整除 → `false`'],
        quote='代码实现时，可以不用转成字符串处理，而是不断取最低位（模 10），去掉最低位（除以 10），直到数字为 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`divmod(x, 10)` 一次得到「去掉最低位的数」和「最低位」',
              '边拆边累加 `s`、累乘 `m`',
              '`n > 0` 所以 `s > 0`，`s + m` 不会是 0，不会除零'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错：积的初值是 `1` 而不是 `0`',
                 '数位含 0 时积为 0，此时只看数字和',
                 '相似题：2520. 统计能整除数字的位数'],
    ),
)
