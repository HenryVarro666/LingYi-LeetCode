CONFIG = dict(
    num=2907, title='价格递增的最大利润三元组 I', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举 k + 两个树状数组',
    tags=[],
    code='''
class Solution(object):
    def maxProfit(self, prices, profits):

        max_price = max(prices)
        single = [-1] * (max_price + 1)
        pair = [-1] * (max_price * 2 + 1)

        def get(f, x):
            ma = -1
            while x > 0:
                ma = max(ma, f[x])
                x -= x & -x
            
            return ma
        
        
        def put(f, x, v):
            while x < len(f):
                f[x] = max(f[x], v)
                x += x & -x

        res = -1
        for price, profit in zip(prices, profits):
            pair_max = get(pair, price - 1)
            if pair_max > 0:
                res = max(res, pair_max + profit)
            
            single_max = get(single, price - 1)
            if single_max > 0:
                put(pair, price, single_max + profit)
            
            put(single, price, profit)
        
        return res
''',
    call='Solution().maxProfit([4,2,5,6], [3,4,1,5])',
    expect=10,
    views=[
        dict(type='array', var='prices', label='prices（蓝色 = 当前商品）', h=140,
             color=lambda S, i, v: 'blue' if 'price' in S and v == S['price'] else None),
        dict(type='array', var='profits', label='profits', h=140,
             color=lambda S, i, v: 'blue' if 'price' in S and S['prices'][i] == S['price'] else None),
        dict(type='array', var='single', label='single（价格 ≤ x 的最大 profit，树状数组）', h=150, cell=60),
        dict(type='array', var='pair', label='pair（两件商品的最大 profit 和，下标=较贵价格）', h=150, cell=44),
    ],
    watch=['price', 'profit', 'pair_max', 'single_max', ('res', 'res', 'green')],
    captions={
        'pair_max = get': '当前商品当 k：到 pair 里查价格 < `{price}` 的最大两件和（-1 表示没有）',
        'if pair_max > 0': '`pair_max = {pair_max}`：{"有合法的 (i, j)，能接上当前 k" if pair_max > 0 else "还没有合法的 (i, j)，当前不能当 k"}',
        'res = max': '三件凑齐：`max({B.res}, {pair_max} + {profit})` = =={res}==',
        'single_max = get': '当前商品当 j：到 single 里查价格 < `{price}` 的最大单件 profit',
        'if single_max > 0': '`single_max = {single_max}`：{"前面有更便宜的商品当 i，当前商品可以当 j" if single_max > 0 else "前面没有更便宜的商品，当不了 j"}',
        'put(pair': '当前商品当 j：把 `{single_max} + {profit}` 记到 pair 的价格 `{price}` 位置',
        'put(single': '当前商品入库：把 `{profit}` 记到 single 的价格 `{price}` 位置',
        'ma = max': '树状数组向下爬：`ma = max(ma, f[x])` = {ma}',
        'x -= x & -x': '`x` 去掉最低位 1 → {x}，继续向前合并区间',
        'f[x] = max': '更新这一格：`f[{x}] = max(旧值, {v})` = {f[x]}',
        'x += x & -x': '`x` 加上最低位 1 → {x}，向上更新覆盖它的格子',
    },
    skip=['ma = -1', 'while x', 'x -= x & -x', 'x += x & -x'],
    max_steps=110,
    cards=dict(
        one_liner='枚举最后一件 k，两个树状数组分别记住最优 i 和最优 (i,j)',
        complexity='时间 `O(n log P)`，空间 `O(P)`，P 为最大价格',
        problem=['选下标 `i<j<k` 且 `prices[i]<prices[j]<prices[k]`，使 `profits` 之和最大',
                 '不存在这样的三元组返回 `-1`',
                 '示例：prices=`[4,2,5,6]`，profits=`[3,4,1,5]` → `10`'],
        quote='第一个树状数组维护前缀中单件商品价格不超过某个阈值的最大profit，而第二个树状数组则是针对前缀中两件商品的组合。',
        quote_src='—— yiduobo 题解',
        idea=['通常枚举中间的 j，这里 yiduobo 觉得反向处理别扭，改成枚举 k',
              '对每个 k：先用 pair 更新答案，再用 single 更新 pair，最后更新 single',
              'pair 的下标是较贵商品的价格，所以要开两倍空间'],
        summary=['时间 `O(n log P)`，树状数组按价格下标，查询 `price-1` 保证严格递增',
                 '==三步顺序不能换==：先查 pair，再写 pair，最后写 single，否则同一件商品会重复使用',
                 '`profits` 为正，所以用 `> 0` 判断有没有合法前驱',
                 '第二个数组大小 `2*max_price+1`，因为存的是两件的价格和'],
    ),
)
