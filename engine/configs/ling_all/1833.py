CONFIG = dict(
    num=1833, title='雪糕的最大数量', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='贪心 · 计数排序',
    tags=['贪心与思维', '难度分 1253'],
    code='''
class Solution:
    def maxIceCream(self, costs: List[int], coins: int) -> int:
        mx = max(costs)
        cnt = [0] * (mx + 1)
        for cost in costs:
            cnt[cost] += 1

        # 按照价格从低到高买
        ans = 0
        for cost in range(1, mx + 1):
            if coins < cost:  # 钱不够
                break
            num = min(cnt[cost], coins // cost)
            coins -= cost * num  # 买 num 根雪糕
            ans += num
        return ans
''',
    call='Solution().maxIceCream([1,3,2,4,1], 7)',
    expect=4,
    views=[
        dict(type='array', var='costs', label='costs（雪糕价格）', pointers={}, h=150,
             color=lambda S, i, v: 'blue' if S.get('cost') == v and 'cnt' in S and S['_line'] < 8 else None),
        dict(type='array', var='cnt', label='cnt[价格] = 这个价格的雪糕数（下标 = 价格）', pointers={'cost': 'pink'}, h=200,
             dim=lambda S, i, v: 'ans' in S and i < S.get('cost', 0) and False),
        dict(type='text', h=90, size=30, fn=lambda S: (f"钱 `coins = {S['coins']}`，已买 `ans = {S['ans']}` 根" if 'ans' in S else '先用计数数组把价格排好序')),
    ],
    watch=[('cost', 'cost', 'pink'), ('coins', 'coins', 'orange'), ('num', 'num', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'mx = max': '最大价格 `mx = {mx}`，计数数组长度 `mx + 1`',
        'cnt = [0]': '`cnt[p]` 记录价格为 p 的雪糕有几根',
        'cnt[cost] += 1': '价格 `{cost}` 的雪糕多了一根：`cnt[{cost}] = {cnt[cost]}`',
        'for cost in range(1, mx + 1)': lambda S, B, r: f'从低到高枚举价格 `{S.cost}`（计数排序，不用真的排）',
        'if coins < cost': lambda S, B, r: (f'`coins = {S.coins} < {S.cost}`：连这个价格都买不起 → ==更贵的更买不起==，停止' if S.coins < S.cost
                                            else f'`coins = {S.coins} >= {S.cost}`：至少买得起一根'),
        'num = min': '买价格 `{cost}` 的：数量受限于库存 `{cnt[cost]}` 和钱能买几根 `{coins} // {cost}` → `num = {num}`',
        'coins -= cost * num': '花掉 `{cost} × {num}`，剩余 `coins = {coins}`',
        'ans += num': '`ans` 累加 {num} → =={ans}==',
        'return ans': '最多买 `{ans}` 根',
    },
    cards=dict(
        one_liner='先买便宜的：买到的根数一定最多',
        complexity='时间 `O(n + U)`，空间 `O(U)`（U = 最大价格）',
        problem=['`costs[i]` 是第 i 根雪糕的价格，手上有 `coins`，求最多能买几根',
                 '要求用计数排序',
                 '本视频：`costs = [1,3,2,4,1], coins = 7` → `4`'],
        quote='贪心地，按照价格从低到高购买，是最优的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['证明：若买了贵的、没买更便宜的，换成便宜的 ==根数不变，花得更少==',
              '价格范围小，用 `cnt` 数组计数代替排序',
              '每个价格最多买 `min(库存, coins // 价格)` 根'],
        summary=['时间 `O(n + U)`，空间 `O(U)`',
                 '写法一：`sort` 后逐个买，时间 `O(n log n)`，思路相同',
                 '价格 `cost` 买不起就可以直接 `break`：更贵的更买不起',
                 '易错：`cnt` 长度要 `mx + 1`，价格从 1 开始枚举'],
    ),
)
