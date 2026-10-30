CONFIG = dict(
    num=3622, title='判断整除性', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='模 10 除 10 拆数位',
    tags=[],
    code='''
class Solution(object):
    def checkDivisibility(self, n):
        
        s = 0
        m = 1
        x = n
        while x:
            d = x % 10
            s += d
            m *= d
            x //= 10
        
        return n % (s + m) == 0
''',
    call='Solution().checkDivisibility(23)',
    expect=False,
    views=[
        dict(type='text', fn=lambda S: f"`n = {S['n']}`，正在拆的 `x = {S['x']}`" if 'x' in S else '', size=30),
        dict(type='text', fn=lambda S: f"数字和 `s = {S['s']}`，数字积 `m = {S['m']}`" if 's' in S and 'm' in S else '', size=30),
    ],
    watch=['n', 'x', 'd', ('s', 's', 'blue'), ('m', 'm', 'pink')],
    captions={
        's = 0': '`s` 记数字和，初值 0',
        'm = 1': '`m` 记数字积，初值 ==1==（乘法单位元）',
        'x = n': '`x` 是 `n` 的拷贝，避免破坏 `n`，后面还要用 `n` 做取模',
        'while x': lambda S, B, ret: (f"`x = {S.x}` 非零，还有数位" if S.x else '`x = 0`，每一位都分离完了'),
        'd = x % 10': '模 10 取出最低位 `d = {d}`',
        's += d': '数字和：`s = {s}`',
        'm *= d': '数字积：`m = {m}`',
        'x //= 10': '除 10 去掉最低位：`x = {x}`',
        'return': '`n % (s + m) = {n} % {s + m} = {n % (s + m)}` → `{ret}`',
    },
    cards=dict(
        one_liner='模 10 除 10 分离每一位，顺便求和与积',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['给正整数 `n`，判断它是否能被「各位数字之和 + 各位数字之积」整除',
                 '示例：`99` → `true`；`23`：`5 + 6 = 11`，`23 % 11 != 0` → `false`'],
        quote='通过模10除10的方法分离出n的每一位，在这个过程中顺便计算数字和s以及数字积m，计算完成后判断n是否为s与m之和的倍数即可。',
        quote_src='—— yiduobo 题解',
        idea=['`x % 10` 是最低位，`x //= 10` 去掉最低位',
              '循环结束时 `s`、`m` 就是数字和与数字积',
              '最后一次取模判断即可'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错：`m` 初值为 1；除法要用 `//`',
                 '`n` 为正，故 `s >= 1`，不会除零',
                 '分离数位的标准写法，同类题很多'],
    ),
)
