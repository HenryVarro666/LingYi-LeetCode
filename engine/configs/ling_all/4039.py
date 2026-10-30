def _dstr(S):
    d = S.get('d')
    return str(d) if d is not None else ''


def _split(S):
    d, x = S.get('d'), S.get('x')
    if d is None:
        return ''
    w = x % 10
    s = str(d)
    return f'`x = {x}` → `width = {w}`，`d = {d}`：前 {w} 位 ==`{s[:w]}`== 是底数，剩下 ==`{s[w:]}`== 是指数'


def _color(S, k, v):
    x = S.get('x')
    if x is None or S.get('d') is None:
        return None
    return 'blue' if k < x % 10 else 'pink'


def _pow_cap(S, B, ret):
    base, e = S.d // S.pow10, S.d % S.pow10
    return (f'底数 `d // pow10 = {base}`，指数 `d % pow10 = {e}`：用 `pow({base}, {e}, MOD)` 快速幂'
            f' = ==`{pow(base, e, 1_000_000_007)}`==，累加后 `ans = {S.ans}`')


CONFIG = dict(
    num=4039, title='解码值之和', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='模拟 + 快速幂',
    tags=[],
    code='''
class Solution:
    def sumDecoded(self, nums: list[int]) -> int:
        MOD = 1_000_000_007
        ans = 0
        for x in nums:
            d = x // 10

            # 计算 d 的十进制长度
            length_d = 0
            v = d
            while v > 0:
                length_d += 1
                v //= 10

            pow10 = 10 ** (length_d - x % 10)
            # 根据 pow10 求出 x = d//pow10 和 y = d%pow10
            ans += pow(d // pow10, d % pow10, MOD)
        return ans % MOD
''',
    call='Solution().sumDecoded([2522, 2101])',
    expect=1649,
    skip=['MOD = 1_000_000_007', 'ans = 0', 'length_d = 0'],
    views=[
        dict(type='array', var='nums', pointers={'x': 'blue'}, label='nums（编码值）', h=170, cell=120,
             color=lambda S, k, v: 'blue' if S.get('x') == v else None),
        dict(type='string', var=_dstr, label='d = x // 10 的十进制数位（蓝 = x 部分，粉 = y 部分）', h=200, cell=80, color=_color),
        dict(type='text', fn=_split, size=26, h=70),
        dict(type='text', fn=lambda S: f'`length_d = {S["length_d"]}`，`pow10 = {S["pow10"]}`' if 'pow10' in S else (f'已数出 `length_d = {S["length_d"]}`，`v = {S["v"]}`' if 'length_d' in S and 'v' in S else ''), size=26, h=60),
    ],
    watch=['x', 'd', 'length_d', 'pow10', ('ans', 'ans', 'green')],
    captions={
        'for x in nums': lambda S, B, r: ('nums 处理完了，退出循环' if B.get('x') == S.x else f'取下一个编码值 `x = {S.x}`'),
        'd = x // 10': '去掉最后一位 `width`：`d = {x} // 10 = {d}`，`width = {x % 10}`',
        'v = d': '用临时变量 `v` 数 `d` 有几位，不能破坏 `d`',
        'while v > 0': lambda S, B, r: (f'`v = {S.v} > 0`，还有数位 → 继续数' if S.v > 0 else f'`v = 0`：数完了，`d` 一共 =={S.length_d}== 位'),
        'length_d += 1': '多一位：`length_d = {length_d}`',
        'v //= 10': '去掉最低位：`v = {v}`',
        'pow10 = 10 **': '`pow10 = 10^({length_d} - {x % 10}) = {pow10}`：除以它得到前 width 位，取余得到剩下的位',
        'ans += pow(': _pow_cap,
        'return ans % MOD': '总和取模：`{ans} % MOD` = =={ans % 1_000_000_007}==',
    },
    cards=dict(
        one_liner='按题意模拟：拆出 x 和 y，快速幂算 x^y',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['每个 `nums[i]` 编码了 `x_i` 和 `y_i`：`width = nums[i] % 10`，`d = nums[i] // 10`',
                 '`x` 是 `d` 的前 `width` 位，`y` 是剩下的位，解码值为 `x^y`',
                 '示例：`[2522,2101]` → `625 + 1024 = 1649`'],
        quote='按题意要求模拟即可。其中 x^y 可以用快速幂计算。注意取模。为什么可以在中途取模？',
        quote_src='—— 灵茶山艾府题解',
        idea=['先数 `d` 的位数 `length_d`，再用 `pow10 = 10^(length_d - width)` 一刀切开',
              '`d // pow10` 是前 width 位 `x`，`d % pow10` 是后面的 `y`',
              'Python 内置 `pow(x, y, MOD)` 就是带取模的快速幂，累加时不必每次取模'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '`ans` 累加了很多模幂结果，只在最后统一 `% MOD`（Python 不怕大整数）',
                 '`pow10` 的指数是 `length_d - width`：要保留的是后面的 y 的位数',
                 '数位数时用临时变量 `v`，不要把 `d` 除没了'],
    ),
)
