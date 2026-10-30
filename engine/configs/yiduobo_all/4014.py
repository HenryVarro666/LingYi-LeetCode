CONFIG = dict(
    num=4014, title='应用折扣后的最低总价', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='两两交换论证 · 排序后逐个配对',
    tags=['贪心与思维', '排序不等式', '难度分 1192'],
    code='''
class Solution(object):
    def minPrice(self, prices, discounts):

        prices.sort(reverse=True)
        discounts.sort(reverse=True)

        res = 0
        for index in range(len(prices)):
            if index < len(discounts):
                res += prices[index] * (100 - discounts[index]) * 1.0 / 100
            else:
                res += prices[index]
        
        return res
''',
    call='Solution().minPrice([8, 20, 14, 6], [25, 50])',
    expect=34.5,
    views=[
        dict(type='array', var='prices', h=200, label='prices（降序）', pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if 'index' in S and i < S['index'] else None),
        dict(type='array', var='discounts', h=200, label='discounts（降序，百分比）', pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if 'index' in S and i < S['index'] else None),
        dict(type='text', fn=lambda S: f"已花费 res = =={S['res']}==" if 'res' in S else '大折扣配贵商品，花费最少', h=90),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'prices.sort': '价格从大到小：`{prices}`',
        'discounts.sort': '折扣从大到小：`{discounts}`',
        'res = 0': '`res` 累计最终花费',
        'for index in range': '处理第 `{index}` 贵的商品，价格 `{prices[index]}`',
        'if index < len': lambda S, B, r: (f'`{S.index} < {len(S.discounts)}`：还有折扣可用 → 用剩余里最大的' if S.index < len(S.discounts)
                                            else f'`{S.index} ≥ {len(S.discounts)}`：折扣用完了 → 原价购买'),
        '* 1.0 / 100': '`{B.res}` 加上 `{prices[index]} × (100 − {discounts[index]}) / 100` → res = =={res}==',
        'res += prices[index]\n': '原价加入：`res = {res}`',
        'return res': '最低总价 `{res}`',
    },
    cards=dict(
        one_liner='用交换论证：更大的折扣该给更贵的商品',
        complexity='时间 `O(n log n + m log m)`，空间 `O(1)`',
        problem=['`prices` 是商品价格，`discounts` 是折扣百分比',
                 '每个折扣最多用一次，每件商品最多一个折扣，可以不用',
                 '本视频：`prices=[8,20,14,6]`，`discounts=[25,50]` → `34.5`'],
        quote='即更大力度的折扣应该应用在价格更贵的物品上，这也是符合直觉的。',
        quote_src='—— yiduobo 题解原文',
        idea=['折扣能用就用，先用最大的',
              '两件商品 `p<q`、两个折扣 `a<b`：比较 `ap+bq` 与 `bp+aq`，右边更大，省得更多',
              '所以都降序排序，前面的商品配前面的折扣，没折扣了就原价'],
        summary=['时间 `O(n log n + m log m)`，空间 `O(1)`',
                 '要先判断 `index < len(discounts)`，否则下标越界',
                 '`* 1.0 / 100` 在 Python 3 里本来就是浮点除法，每件都做一次浮点运算',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
