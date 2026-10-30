CONFIG = dict(
    num=1029, title='两地调度', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='先全去 A · 按差值 delta 排序',
    tags=['贪心与思维'],
    code='''
class Solution(object):
    def twoCitySchedCost(self, costs):
        delta = sorted([x[1] - x[0] for x in costs])
        res = sum(x[0] for x in costs) + sum(delta[:len(costs) // 2])
        return res
''',
    call='Solution().twoCitySchedCost([[10,20],[30,200],[400,50],[30,20]])',
    expect=110,
    views=[
        dict(type='table', var='costs', label='costs[i] = [去 A 的费用, 去 B 的费用]', rows=lambda S: [f'人{i}' for i in range(len(S['costs']))],
             cols=['A', 'B'], h=230),
        dict(type='array', var='delta', label='delta = B − A（排序后，前 n/2 个绿色 = 改去 B 的人）', cell=110,
             color=lambda S, i, v: 'green' if i < len(S['costs']) // 2 else None, h=180),
        dict(type='text', fn=lambda S: ('先假设所有人都去 A：`sum(A) = ' + str(sum(c[0] for c in S['costs'])) + '`' +
                                        (f'，再加上最小的 {len(S["costs"]) // 2} 个 delta' if 'delta' in S else '')), size=26, h=60),
    ],
    watch=[('res', 'res', 'green'), ('delta', 'delta', 'blue')],
    captions={
        'delta = sorted': '`delta[i] = cost[i][1] − cost[i][0]`：第 i 个人从 A 改去 B 多花的钱，排序后 → `{delta}`',
        'res = sum': '全去 A 的总费用 `{sum(x[0] for x in costs)}`，再加最小的 `{len(costs) // 2}` 个 delta 之和 `{sum(delta[:len(costs) // 2])}` → `res = {res}`',
        'return res': '一共 =={res}==',
    },
    cards=dict(
        one_liner='先让所有人去 A，再挑 n/2 个改去 B 代价最小的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`2n` 个人面试，`costs[i] = [aCost, bCost]`',
                 '要求恰好 `n` 人去 A 城、`n` 人去 B 城，求最小总费用',
                 '示例：`[[10,20],[30,200],[400,50],[30,20]]` → `110`'],
        quote='不妨先假设所有的人都去的A地，那么此时的总代价为sum(cost[i][0])。接下里，我们需要将其中n/2个人移动到B地。',
        quote_src='—— yiduobo 题解原文',
        idea=['DP 是 `O(n^2)`：`f[i][j]` = 前 i 人中 j 人去 A 的最小代价',
              '更好的做法：先全去 A，改去 B 的代价 `delta[i] = cost[i][1] − cost[i][0]`',
              '要移动 `n/2` 个人，取最小的 `n/2` 个 `delta` 求和加到答案上'],
        result='`sum(A) = 470`，最小的两个 delta：`-350`、`-10`，`470 − 360 = 110` ✓',
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：delta 可以为负，负的越多越优先改去 B',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '只需要对 delta 排序，不用记具体是谁去哪'],
    ),
)
