CONFIG = dict(
    num=3099, title='哈沙德数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='逐位分离累加',
    tags=[],
    code='''
class Solution(object):
    def sumOfTheDigitsOfHarshadNumber(self, x):

        tmp = x
        s = 0
        while tmp:
            s += tmp % 10
            tmp //= 10
        
        if x % s == 0:
            return s
        return -1
''',
    call='Solution().sumOfTheDigitsOfHarshadNumber(100)',
    expect=1,
    views=[
        dict(type='text', fn=lambda S: (f"`x = {S['x']}`，还没拆的部分 `tmp` = =={S['tmp']}==，数位和 `s` = =={S['s']}==" if 'tmp' in S and 's' in S else ''), size=26, h=80),
        dict(type='text', fn=lambda S: (f"`{S['x']} ÷ {S['s']}` 余 =={S['x'] % S['s']}==" if S.get('_line', 0) >= 10 and S.get('s') else ''), size=26, h=70),
        dict(type='string', var=lambda S: str(S['x']), h=220, label='x 的各个数位（从右往左拆，绿色 = 已加进 s）',
             color=lambda S, i, c: 'green' if 'tmp' in S and i >= (len(str(S['tmp'])) if S['tmp'] else 0) else None),
    ],
    watch=['x', 'tmp', ('s', 's', 'green')],
    max_steps=40,
    captions={
        'tmp = x': '`tmp` 是 x 的副本，用来一位位拆；`x` 留着最后判断',
        's = 0': '`s` 累加各个数位',
        'while tmp': lambda S, B, r: (f'`tmp = {S.tmp}`，还有数位' if S.tmp else '`tmp = 0`：数位拆完'),
        's += tmp % 10': '`{B.tmp} % 10` 取出个位 `{B.tmp % 10}` → `s` = =={s}==',
        'tmp //= 10': '`tmp //= 10`：去掉个位，剩下 =={tmp}==',
        'if x % s == 0': '`{x} % {s} = {x % s}` → {"==整除==" if x % s == 0 else "不能整除"}',
        'return s': '是哈沙德数，返回数位和 `{s}`',
        'return -1': '不是哈沙德数，返回 `-1`',
    },
    cards=dict(
        after=[dict(heading='不是哈沙德数的例子', lines=['`23`：`s = 3 + 2 = 5`，`23 % 5 = 3` ≠ 0 → 走到最后返回 `-1`', '所以返回值取决于最后这一次整除判断'])],
        one_liner='模 10 取出个位累加，除 10 丢掉个位',
        complexity='时间 `O(log x)`，空间 `O(1)`',
        problem=['如果 `x` 能被各位数字之和整除，就是哈沙德数',
                 '是则返回数位和，不是则返回 `-1`',
                 '示例：`18` → `9`；`23` → `-1`；本视频：`100` → `1`'],
        quote='通过模10除10的操作逐位分离x中的数位并累加到s中，然后判断x能否被s整除即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 `x` 复制给 `tmp`，对 `tmp` 反复“取个位、去个位”',
              '循环结束 `s` 就是数位和',
              '再用原来的 `x` 判断 `x % s == 0`'],
        summary=['时间 `O(log x)`，空间 `O(1)`',
                 '要保留原来的 `x`，所以拆数位用的是 `tmp`',
                 '先判断整除再返回：整除返回 `s`，否则 `-1`',
                 '原文已是 Python 3 写法（`//=`），未做修改'],
    ),
)
