CONFIG = dict(
    num=3099, title='哈沙德数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='模 10 除 10 拆数位',
    tags=[],
    code='''
class Solution:
    def sumOfTheDigitsOfHarshadNumber(self, x: int) -> int:
        s = 0
        v = x
        while v:
            v, d = divmod(v, 10)
            s += d
        return -1 if x % s else s
''',
    call='Solution().sumOfTheDigitsOfHarshadNumber(100)',
    expect=1,
    views=[
        dict(type='text', fn=lambda S: (f"`v` 还剩 =={S['v']}==，已拆出的数位和 `s` = =={S['s']}==" if 'v' in S else ''), size=26, h=70),
        dict(type='text', fn=lambda S: (f"x = `{S['x']}`" + (f"，刚拆出的个位 `d = {S['d']}`" if 'd' in S else '')) if 'x' in S else '', size=26, h=70),
        dict(type='string', var=lambda S: str(S['x']), h=220, label='x 的各个数位（从右往左拆，绿色 = 已加进 s）',
             color=lambda S, i, c: 'green' if 'v' in S and i >= (len(str(S['v'])) if S['v'] else 0) else None),
    ],
    watch=['x', 'v', 'd', ('s', 's', 'green')],
    max_steps=40,
    captions={
        's = 0': '`s` 用来累加各个数位',
        'v = x': '复制一份 `v = x`，拆数位时改 `v`，==保留 x== 最后还要用',
        'while v': lambda S, B, r: (f'`v = {S.v}` 不为 0，还有数位没拆' if S.v else '`v = 0`：所有数位都拆完了'),
        'v, d = divmod(v, 10)': '`divmod({B.v}, 10)`：商 `v = {v}`（去掉个位），余数 `d = {d}`（当前个位）',
        's += d': '数位和 `s` += `{d}` → =={s}==',
        'return -1 if x % s else s': '`{x} % {s} = {x % s}`：{"==能整除，是哈沙德数== → 返回 s" if x % s == 0 else "不能整除 → 返回 -1"}',
    },
    cards=dict(
        after=[dict(heading='不是哈沙德数的例子', lines=['`23`：拆出 `3`、`2`，`s = 5`，`23 % 5 = 3` 不为 0 → 返回 `-1`', '所以返回值取决于最后这一次整除判断'])],
        one_liner='模 10 取个位，除 10 去个位，数位和就出来了',
        complexity='时间 `O(log x)`，空间 `O(1)`',
        problem=['能被自己各位数字之和整除的数叫哈沙德数',
                 '是则返回数位和，否则返回 `-1`',
                 '示例：`18` → `9`；`23` → `-1`；本视频：`100` → `1`'],
        quote='对于数字 v=123，我们可以通过模 10 除以 10 的方式，从低到高遍历其各个数位',
        quote_src='—— 灵茶山艾府题解',
        idea=['`divmod(v, 10)` 一次得到商和余数：余数是个位，商是剩下的高位',
              '`v` 变成 0 就拆完了；`x` 要另存一份，最后判断整除',
              '`x % s` 为 0 才是哈沙德数'],
        summary=['时间 `O(log x)`，等于 x 的十进制位数',
                 '不能直接改 `x`，否则最后没法判断 `x % s`',
                 '`x ≥ 1` 所以 `s ≥ 1`，不会除以 0',
                 '同类：数位拆分、数位和相关题'],
    ),
)
