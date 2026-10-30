CONFIG = dict(
    num=1833, title='雪糕的最大数量', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='排序 + 先买便宜的',
    tags=['灵神题单', '难度分 1253'],
    code='''
class Solution(object):
    def maxIceCream(self, costs, coins):

        n = len(costs)
        costs = sorted(costs)
        for index in range(n):
            if costs[index] <= coins:
                coins -= costs[index]
            else:
                return index
                
        return n
''',
    call='Solution().maxIceCream([1,3,2,4,1], 7)',
    expect=4,
    views=[
        dict(type='array', var='costs', label='costs（排序后从小到大买）', pointers={'index': 'blue'}, h=220,
             color=lambda S, i, v: 'green' if 'index' in S and i < S['index'] else None,
             dim=lambda S, i, v: False),
        dict(type='text', h=90, size=30, fn=lambda S: (f"手上还剩 `{S['coins']}` 元，已买 `{S['index']}` 根" if 'index' in S else f"手上有 `{S['coins']}` 元")),
    ],
    watch=[('index', 'index', 'blue'), ('coins', 'coins', 'orange')],
    captions={
        'n = len': '共 `n = {n}` 根雪糕',
        'costs = sorted': '价格从小到大排序：`{costs}`',
        'for index in range': lambda S, B, r: f'看第 `{S.index}` 根，价格 `{S.costs[S.index]}`',
        'if costs[index] <= coins': lambda S, B, r: (f'`{S.costs[S.index]} <= {S.coins}`：钱够，买下' if S.costs[S.index] <= S.coins
                                                     else f'`{S.costs[S.index]} > {S.coins}`：钱不够，==后面的更贵，也都买不起=='),
        'coins -= costs[index]': '买下，剩余 `coins = {coins}`',
        'return index': '前 `{index}` 根都买了，返回 `{index}`',
        'return n': '全部买完，返回 `n = {n}`',
    },
    cards=dict(
        one_liner='不要求花光钱，只要根数多：先买便宜的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每根雪糕有价格，手上有 `coins` 块钱，求最多买几根',
                 '本视频：`costs = [1,3,2,4,1], coins = 7` → `4`'],
        quote='题目只要求买到的雪糕尽量多，但是没有要求必须把钱给花完，那么在这里显然应该先买便宜的。',
        quote_src='—— yiduobo 题解原文',
        idea=['按价格从小到大排序，一趟遍历',
              '钱够就买；不够，说明剩下的钱买不起任何一根剩余的雪糕，直接返回已买数量 `index`',
              '能走完循环 = 全买下，返回 `n`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（`sorted` 产生新列表）',
                 '返回 `index` 就是已买根数（下标从 0 开始）',
                 '易错：别忘了循环正常结束时返回 `n`',
                 '对比灵神：灵神用计数排序做到 `O(n + U)`'],
    ),
)
