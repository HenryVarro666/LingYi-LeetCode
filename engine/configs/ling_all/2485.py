CONFIG = dict(
    num=2485, title='找出中枢整数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='数学公式 · 开平方',
    tags=[],
    code='''
class Solution:
    def pivotInteger(self, n: int) -> int:
        m = n * (n + 1) // 2
        x = isqrt(m)
        return x if x * x == m else -1
''',
    call='[Solution().pivotInteger(n) for n in (8, 4)]',
    expect=[6, -1],
    views=[
        dict(type='text', h=160, size=30,
             fn=lambda S: (f"`1+…+x` = `x(x+1)/2`，`x+…+n` = `(n(n+1) − x(x−1))/2`" )),
        dict(type='text', h=160, size=32,
             fn=lambda S: (f"两边相等 → `x² = n(n+1)/2 = {S['m']}`" if 'm' in S else '')),
        dict(type='text', h=160, size=32,
             fn=lambda S: (f"`isqrt({S['m']}) = {S['x']}`，`{S['x']}² = {S['x']*S['x']}`，{'==等于 m，是中枢整数==' if S['x']*S['x'] == S['m'] else '==不等于 m，不存在=='}" if 'x' in S and 'm' in S else '')),
    ],
    watch=[('n', 'n', 'blue'), ('m', 'm', 'yellow'), ('x', 'x', 'green')],
    captions={
        'm = n': '`m = n(n+1)/2 = {m}`，这是 `x²` 必须等于的值（`n = {n}`）',
        'x = isqrt': '`isqrt({m})` 取整数平方根 → `x = {x}`',
        'return x if': '`{x}² = {x*x}`，{"等于 m → x 就是中枢整数" if x*x == m else "不等于 m → 平方根不是整数，不存在中枢整数"}，返回 =={ret}==',
    },
    cards=dict(
        one_liner='两段和相等，化简后 x² = n(n+1)/2：开平方判断是否整数',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['正整数 `n`，找 `x` 使 `1..x` 的和等于 `x..n` 的和',
                 '不存在就返回 `-1`',
                 '示例：`n=8` → `6`（`21 = 21`）；`n=4` → `-1`'],
        quote='两式相等，简化后即 x = sqrt(n(n+1)/2)。如果 x 不是整数则返回 -1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`1..x` 的和是 `x(x+1)/2`；`x..n` 的和是 `n(n+1)/2` 减去 `1..x-1` 的和',
              '两边相等化简得 `x² = n(n+1)/2`',
              '用 `isqrt` 取整数平方根，再检验平方是否回到 `m`'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：用 `isqrt` 而不是浮点 `sqrt`，避免精度问题',
                 '`x * x == m` 不成立就说明没有整数解，返回 `-1`',
                 '方法二：范围内只有 `n = 1, 8, 49, 288` 有解，直接查表',
                 '视频依次演示 `n = 8` 和 `n = 4`'],
    ),
)
