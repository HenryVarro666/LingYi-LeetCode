def _fcolor(S, i, v):
    s, vv = S.get('s'), S.get('v')
    if s is None or vv is None or S.get('_line') not in (8, 9):
        return None
    if i == s:
        return 'yellow'
    if i == s - vv:
        return 'blue'
    return None


def _formula(S):
    s, v = S.get('s'), S.get('v')
    if v is None:
        return '`f[s]` = 凑出和恰好为 `s` 的方案数；物品 = `1^x, 2^x, 3^x ...`'
    if s is None or S.get('_line') not in (8, 9):
        return f'当前物品体积 `v = {S["i"]}^{S["x"]} = {v}`，每个物品只能用一次'
    return f'`f[{s}] += f[{s}-{v}]`：不用 `{v}` 的方案 + 用了 `{v}` 的方案（`f[{s - v}]` = {S["f"][s - v]}）'


CONFIG = dict(
    num=2787, title='将一个数字表示成幂的和的方案数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='恰好装满型 0-1 背包',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1818'],
    code='''
class Solution:
    def numberOfWays(self, n: int, x: int) -> int:
        f = [1] + [0] * n
        for i in range(1, n + 1):
            v = i ** x
            if v > n:
                break
            for s in range(n, v - 1, -1):
                f[s] += f[s - v]
        return f[n] % 1_000_000_007
''',
    call='Solution().numberOfWays(6, 1)',
    expect=4,
    views=[
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='array', var='f', label='f[s]：恰好凑出 s 的方案数（黄 = 正在更新，蓝 = 被加进来的 f[s-v]）', h=260, cell=90,
             color=lambda S, i, v: _fcolor(S, i, v)),
    ],
    watch=[('i', 'i', 'blue'), ('v', 'v', 'purple'), ('s', 's', 'yellow'), ('f[n]', 'f[n]', 'green')],
    captions={
        'f = [1]': '`f[0] = 1`：什么都不选，恰好凑出 0，有 1 种方案；其余先是 0',
        'for i in range': lambda S, B, r: (f'枚举底数 `i = {S.i}`，对应物品 `{S.i}^{S.x}`' if S.i != B.get('i') else '`i` 枚举完了，循环结束'),
        'v = i ** x': '物品体积 `v = {i}^{x}`，即 =={v}==',
        'if v > n': lambda S, B, r: (f'`v = {S.v} > n = {S.n}`：这个物品和后面的都装不下 → `break`' if S.v > S.n
                                     else f'`v = {S.v} ≤ n = {S.n}`，还装得下，继续'),
        'for s in range': '`s` 从 `n` 倒序到 `v`：==倒序==保证每个物品只用一次',
        'f[s] += f[s - v]': '`f[{s}] += f[{s - v}]`：用 `{v}` 的方案数 `{f[s - v]}` 加进来 → ==`{f[s]}`==',
        'return f[n]': '`f[{n}] % (10^9+7)` = =={ret}==：本题答案没超 64 位，最后再取模即可',
    },
    cards=dict(
        one_liner='n 当背包容量，k^x 当物品：恰好装满的 0-1 背包',
        complexity='时间 `O(n·n^(1/x))`，空间 `O(n)`',
        problem=['给两个正整数 `n` 和 `x`，把 `n` 写成若干 ==互不相同== 整数的 `x` 次幂之和',
                 '求方案数，对 `10^9 + 7` 取模',
                 '示例：`n = 10, x = 2` → `1`（`10 = 3^2 + 1^2`）；本视频用 `n = 6, x = 1`'],
        quote='把 n 看成背包容量，1^x, 2^x, 3^x, … 看成物品，本题是恰好装满型 0-1 背包的方案数，做法同 494. 目标和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['物品 `1^x, 2^x, ...` 每个只能用一次 → 0-1 背包',
              '`f[s]` 是恰好凑出 `s` 的方案数：`f[s] += f[s - v]`，初始 `f[0] = 1`',
              '最坏 `n = 300, x = 1` 的答案不超过 64 位整数，所以可以最后再取模'],
        summary=['时间 `O(n·n^(1/x))`：外层只有 `n^(1/x)` 个物品，内层 `O(n)`',
                 '易错：`s` 必须==倒序==，正序会把同一个物品用多次（变成完全背包）',
                 '`v > n` 就 `break`，后面的幂只会更大',
                 '另一种写法：预处理 `x = 1..5` 的全部答案，查询时 `O(1)`'],
    ),
)
