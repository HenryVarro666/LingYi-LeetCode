CONFIG = dict(
    num=3908, title='有效数字整数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='逐位取模 · 停在最高位',
    code='''
class Solution:
    def validDigit(self, n: int, x: int) -> bool:
        has_x = False
        while n >= 10:
            if n % 10 == x:
                has_x = True
            n //= 10
        return has_x and n != x
''',
    call='Solution().validDigit(30120, 0)',
    expect=True,
    views=[
        dict(type='string', var=lambda S: str(S['n']), label='n 的各位数字（右端是当前末位）', h=200, cell=110,
             color=lambda S, i, v: ('green' if v == str(S['x']) else 'blue') if i == len(str(S['n'])) - 1 else None),
        dict(type='text', size=34, fn=lambda S: f"当前 n = =={S['n']}==，末位 `{S['n'] % 10}`，x = `{S['x']}`" if 'n' in S else ''),
        dict(type='text', size=30, fn=lambda S: ('n < 10：只剩最高位 ==' + str(S['n']) + '==' if S['n'] < 10 else '循环中：n ≥ 10，最高位还没露出来') if 'n' in S else ''),
        dict(type='text', size=30, fn=lambda S: ('has_x = ==' + str(S['has_x']) + '==') if 'has_x' in S else ''),
    ],
    watch=['n', 'x', ('has_x', 'has_x', 'green')],
    captions={
        'has_x = False': '先假设：还没见过数字 `x`',
        'while n >= 10': lambda S, B, r: (f'`n = {S.n} >= 10`：还有不止一位，继续剥末位' if S.n >= 10 else f'`n = {S.n} < 10`：只剩一位，它就是==最高位==，停止'),
        'if n % 10 == x': '末位 `{n % 10}` 和 `x = {x}` 比较 → ' + '{"相等，见到了 x" if n % 10 == x else "不等"}',
        'has_x = True': '这一位是 `x`：`has_x = True`',
        'n //= 10': '去掉末位：`n` 变成 `{n}`',
        'return': lambda S, B, r: f'`has_x = {S.has_x}`，最高位 `{S.n}` vs `x = {S.x}` → 返回 =={r}==',
    },
    cards=dict(
        one_liner='剥掉末位，停在最高位：最高位单独判断',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['给整数 `n` 和数字 `x`，有效 = ==含有 x 且不以 x 开头==',
                 '示例：`n=101, x=0` → `true`；`n=232, x=2` → `false`',
                 '本视频：`n=30120, x=0` → `true`'],
        quote='本题还需要获取最高位，我们可以在 `n<10` 时停止循环，此时 `n` 即为最高位。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不断 `n //= 10`，`n % 10` 依次是每个数位（从低到高）',
              '循环条件写成 `n >= 10`：停下时 `n` 恰好是最高位',
              '最高位不进循环，所以最后单独判断 `n != x`'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错：循环到 `n > 0` 会把最高位也算进 has_x，无法区分“开头是 x”',
                 '`n = 0` 时直接不进循环，最高位就是 0'],
    ),
)
