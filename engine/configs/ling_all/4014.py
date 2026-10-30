CONFIG = dict(
    num=4014, title='应用折扣后的最低总价', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='排序不等式：大折扣配贵商品',
    tags=['贪心与思维', '排序不等式', '难度分 1192'],
    code='''
class Solution:
    def minPrice(self, prices: list[int], discounts: list[int]) -> float:
        prices.sort(reverse=True)
        discounts.sort(reverse=True)

        # 更快的写法见另一份代码【Python3 写法二】
        s = 0
        for i, p in enumerate(prices):
            d = discounts[i] if i < len(discounts) else 0
            s += p * (100 - d)
        return s / 100  # 只做一次浮点运算
''',
    call='Solution().minPrice([10, 30, 21, 5], [50, 60])',
    expect=37.5,
    views=[
        dict(type='array', var='prices', h=200, label='prices（降序）', pointers={'i': 'blue'},
             color=lambda S, i, v: 'green' if 'i' in S and i < S['i'] else None),
        dict(type='array', var='discounts', h=200, label='discounts（降序，百分比）', pointers={'i': 'blue'},
             color=lambda S, i, v: 'green' if 'i' in S and i < S['i'] else None),
        dict(type='text', fn=lambda S: f"当前 `{S['p']} × (100 − {S['d']})` = =={S['p']*(100-S['d'])}==，累计 s = =={S['s']}==（单位：分，最后除以 100）" if 'd' in S and 'p' in S else '价格乘 100，折后价全是整数', h=90),
    ],
    watch=[('i', 'i', 'blue'), ('p', 'p', 'yellow'), ('d', 'd', 'pink'), ('s', 's', 'green')],
    captions={
        'prices.sort': '价格降序：`{prices}`',
        'discounts.sort': '折扣降序：`{discounts}`，最大的折扣排最前',
        's = 0': '`s` 累计「价格 × (100 − 折扣)」，相当于所有价格先乘了 100',
        'for i, p in enumerate': '第 `{i}` 贵的商品，价格 `p = {p}`',
        'd = discounts[i]': lambda S, B, r: (f'第 {S.i} 贵的商品配第 {S.i} 大的折扣 `d = {S.d}`' if S.i < len(S.discounts)
                                              else f'折扣用完了（只有 {len(S.discounts)} 个）→ `d = 0`，原价购买'),
        's += p': '`s += {p} × (100 − {d})` = `{p*(100-d)}` → s = =={s}==',
        'return s / 100': lambda S, B, ret: f'`s / 100` = `{S.s} / 100` = =={ret}==（只有一次浮点运算）',
    },
    cards=dict(
        one_liner='最大的折扣用在最贵的商品上',
        complexity='时间 `O(n log n + m log m)`，空间 `O(1)`',
        problem=['`prices` 是商品价格，`discounts` 是折扣百分比',
                 '每个折扣最多用一次，每件商品最多用一个折扣，也可以不用',
                 '本视频：`prices=[10,30,21,5]`，`discounts=[50,60]` → `37.5`'],
        quote='根据排序不等式，最优做法是把最大的折扣用在最贵的商品上。把 prices 和 discounts 降序排序，遍历，计算并累加折扣后的价格。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序不等式：两个序列「大配大」，乘积之和最大，省下的钱最多',
              '两个数组都降序排序，第 `i` 贵的商品配第 `i` 大的折扣',
              '折扣不够用的商品，折扣记 0，原价买'],
        summary=['时间 `O(n log n + m log m)`，空间 `O(1)`',
                 '价格先乘 100，折后价是整数，最后 `/ 100` 只有一次浮点运算，不会累积误差',
                 '商品比折扣多时要判断 `i < len(discounts)`',
                 '另一种写法用 `zip` 和 `sum` 一行算出总折扣；还可用计数排序优化折扣的排序'],
    ),
)
