CONFIG = dict(
    num=3345, title='最小可整除数位乘积 I', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='暴力枚举 · 至多 10 次',
    tags=[],
    setup='from itertools import count\nfrom operator import mul',
    code='''
class Solution:
    def smallestNumber(self, n: int, t: int) -> int:
        for x in count(n):  # 从 n 开始枚举
            prod = reduce(mul, map(int, str(x)))
            if prod % t == 0:
                return x
''',
    call='Solution().smallestNumber(91, 7)',
    expect=97,
    views=[
        dict(type='text', size=34, h=140, fn=lambda S: f"`x = {S['x']}`：数位乘积 =={S['prod']}==" + (f"，`{S['prod']} % {S['t']} = {S['prod'] % S['t']}`" if 'prod' in S else '') if 'prod' in S else ''),
        dict(type='text', size=28, h=100, fn=lambda S: f"从 `n = {S['n']}` 往上找，最迟遇到个位为 0 的数（乘积 0）就一定成功"),
    ],
    watch=[('n', 'n'), ('t', 't', 'pink'), ('x', 'x', 'blue'), ('prod', 'prod', 'green')],
    captions={
        'for x in count(n)': '从 `n = {n}` 开始，逐个枚举 `x` = =={x}==',
        'prod = reduce': '`x = {x}` 的数位乘积 `prod` = =={prod}==',
        'if prod % t == 0': lambda S, B, r: (
            f'`{S.prod} % {S.t} = {S.prod % S.t}` → ==整除==，`{S.x}` 就是最小的答案' if S.prod % S.t == 0
            else f'`{S.prod} % {S.t} = {S.prod % S.t} ≠ 0` → 不行，继续试 `x + 1`'),
        'return x': '返回 `{x}`',
    },
    cards=dict(
        one_liner='至多枚举 10 个数，一定会遇到个位是 0 的',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['找 ≥ `n` 的最小整数，使各数位之积能被 `t` 整除',
                 '示例：`n=10, t=2` → `10`（乘积 0）',
                 '本视频：`n=91, t=7` → `97`（乘积 63）'],
        quote='从 n 开始，至多循环 10 次，一定会遇到个位数为 0 的数，其数位乘积为 0，一定是 t 的倍数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['0 能被任何数整除，个位为 0 的数乘积必为 0',
              '连续 10 个数里必有一个个位是 0，所以暴力枚举 `n ~ n+9` 即可',
              '`count(n)` 从 `n` 无限递增，找到就 `return`'],
        summary=['时间 `O(log n)`：最多 10 个数，每个数拆数位',
                 '`count` 和 `mul` 来自 itertools / operator，视频里在 setup 里导入',
                 '另一种写法：用 `divmod(x, 10)` 取数位，不转字符串'],
    ),
)
