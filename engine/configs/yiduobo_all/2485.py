CONFIG = dict(
    num=2485, title='找出中枢整数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='推导公式 · 检测整数解',
    tags=[],
    setup='from math import sqrt',
    code='''
class Solution(object):
    def pivotInteger(self, n):

        c = n * (n + 1) // 2
        x = int(sqrt(c))
        if x * x == c:
            return x
        
        return -1
''',
    call='[Solution().pivotInteger(n) for n in (8, 4)]',
    expect=[6, -1],
    views=[
        dict(type='text', h=200, size=30,
             fn=lambda S: '`1..x` 的和 = `(1+x)·x/2`；`x..n` 的和 = `(1+n)·n/2 − x(x−1)/2`'),
        dict(type='text', h=160, size=32,
             fn=lambda S: f"两边相等整理 → `x² = (1+n)·n/2 = {S['c']}`" if 'c' in S else ''),
        dict(type='text', h=160, size=32,
             fn=lambda S: (f"`int(sqrt({S['c']})) = {S['x']}`；`{S['x']}² = {S['x']*S['x']}`，{'==等于 c==' if S['x']*S['x'] == S['c'] else '==不等于 c=='}") if 'x' in S and 'c' in S else ''),
    ],
    watch=[('n', 'n', 'blue'), ('c', 'c', 'yellow'), ('x', 'x', 'green')],
    captions={
        'c = n': '`c = (1+n)·n/2 = {c}`：`x²` 应该等于它（`n = {n}`）',
        'x = int': '`sqrt({c})` 向下取整 → `x = {x}`',
        'if x * x == c': '`{x}×{x} = {x*x}`，{"等于 c → x 就是整数解" if x*x == c else "不等于 c → 没有整数解"}',
        'return x': 'x 满足条件，返回 `{x}`',
        'return -1': '检测不到整数解，返回 `-1`',
    },
    cards=dict(
        one_liner='把两段求和写成式子，整理成 x² = (1+n)n/2',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['正整数 `n`，找 `x` 使 `1..x` 的和等于 `x..n` 的和',
                 '不存在就返回 `-1`',
                 '示例：`n=8` → `6`；`n=4` → `-1`'],
        quote='这两部分相等，就有 x^2 + x = (1 + n) * n - x^2 + x，整理后就有 x^2 = (1 + n) * n / 2，接下来只需检测x是否存在整数解就行了',
        quote_src='—— yiduobo 题解原文',
        idea=['`1` 到 `x` 的和是 `(1+x)·x/2`',
              '`x` 到 `n` 的和是 `1..n` 的和减去 `1..x-1` 的和',
              '两边相等后 `x` 的一次项抵消，只剩 `x² = (1+n)n/2`'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '原文为 Python 2 写法，`/` 已改为 `//`；`sqrt` 需 `from math import sqrt`（放在 setup 里）',
                 '`n(n+1)` 一定是偶数，所以 `//2` 不丢精度',
                 '检验 `x * x == c`，非整数平方根时 `int(sqrt(c))` 的平方必然不等于 `c`',
                 '对比灵神：灵神用 `isqrt` 避免浮点误差，yiduobo 用 `sqrt` 再取整'],
    ),
)
