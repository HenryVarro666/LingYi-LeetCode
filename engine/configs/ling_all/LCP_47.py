CONFIG = dict(
    num='LCP 47', title='入场安检', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='01 背包求方案数（Go 原文转写）',
    tags=['动态规划'],
    code='''
class Solution:
    def securityCheck(self, capacities: List[int], k: int) -> int:
        dp = [0] * (k + 1)
        dp[0] = 1
        for x in capacities:
            x -= 1
            for s in range(k, x - 1, -1):
                dp[s] = (dp[s] + dp[s - x]) % int(1e9 + 7)
        return dp[k]
''',
    call='Solution().securityCheck([4,3,2,2], 6)',
    expect=2,
    skip=['dp = [0]', 'for s in range'],
    views=[
        dict(type='array', var='capacities', label='capacities（x = 容量 − 1 才是物品大小）', h=150, cell=70),
        dict(type='array', var='dp', label='dp[s]：恰好填满背包 s 的方案数（s = 0..k）', h=190, cell=80, pointers={'s': 'blue'},
             color=lambda S, i, v: 'yellow' if 'x' in S and 's' in S and S['_line'] >= 8 and i == S['s'] - S['x'] else None),
        dict(type='text', fn=lambda S: (f"物品大小 `x = {S['x']}`：`dp[s]` += `dp[s − {S['x']}]`" if 'x' in S else '栈安检室填 `容量−1` 人，就变成大小 1 的队列；这些 x 之和要刚好是 k'), size=24, h=60),
    ],
    watch=['x', 's', ('k', 'k', 'pink'), ('dp[k]', 'dp[k]', 'green')],
    captions={
        'dp = [0]': '`dp` 长度 `k+1 = {k + 1}`',
        'dp[0] = 1': '一个都不选，刚好填满 0 的方案有 ==1== 种',
        'x -= 1': '设成栈要先填 `容量 − 1` 人 → 物品大小 `x = {x}`（设成队列就不选它）；`s` 从 k 倒序到 x，==01 背包倒序==，每个物品只用一次',
        'dp[s] = (dp[s]': '`dp[{s}]` = 不选 `{B.dp[s]}` + 选它 `dp[{s - x}] = {dp[s - x]}` → =={dp[s]}==',
        'return dp[k]': '凑出总和恰好 `k = {k}` 的方案数 = =={ret}==',
    },
    cards=dict(
        one_liner='栈型安检室先填满 容量−1 人，问题变成 01 背包方案数',
        complexity='时间 `O(N·k)`，空间 `O(k)`',
        problem=['若干安检室，每个可设成队列（先进先出）或栈（后进先出）',
                 '求有多少种设置，使编号 `k` 的观众第一个通过最后一个安检室',
                 '示例：`capacities=[4,3,2,2]`，`k=6` → `2`'],
        quote='我们可以对栈填充 x_i = capacities_i − 1 个人，这样可以将栈转换成一个大小为 1 的队列。……把 x_i 看成物品大小，k 看成背包容量，则该问题就转换成了一个经典模型——求 01 背包的方案数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['栈型安检室先填 `x = 容量 − 1` 人，之后它就像大小为 1 的队列',
              '要让 `k` 号第一个出来，栈型安检室的 `x` 之和必须恰好是 `k`',
              '于是：选一些物品，和恰好为 `k` 的方案数，01 背包倒序刷一维 `dp`'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(N·k)`，空间 `O(k)`，结果对 `10^9+7` 取模',
                 '易错：`x = 0`（容量为 1）时 `dp[s]` 加的是自己，方案数翻倍，倒序循环要到 `x` 为止',
                 '易错：Go 的 `1e9+7` 是整数常量，Python 里要写 `int(1e9 + 7)`',
                 '同类题：494. 目标和（01 背包方案数）'],
    ),
)
