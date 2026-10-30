CONFIG = dict(
    num=3947, title='购买最多物品数目 II', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='买一送一 · 价格从低到高贪心',
    tags=['贪心与思维', '难度分 2215'],
    code='''
class Solution:
    def maximumSaleItems(self, items: list[list[int]], budget: int) -> int:
        n = len(items)
        cnt_factor = [0] * (n + 1)
        min_price = inf
        for factor, price in items:
            cnt_factor[factor] += 1
            min_price = min(min_price, price)

        cnt_multi = [0] * (n + 1)
        sum_cnt = defaultdict(int)  # price -> 相同 price 的 cnt 之和

        for factor, price in items:
            if price >= min_price * 2:
                continue

            if cnt_multi[factor] == 0:  # 之前没有计算过
                for j in range(factor, n + 1, factor):
                    cnt_multi[factor] += cnt_factor[j]

            cnt = cnt_multi[factor] - 1  # factor 的倍数不包括该物品
            if cnt > 0:
                sum_cnt[price] += cnt

        ans = 0
        for price in sorted(sum_cnt):
            if budget < price:  # 没钱了
                break
            c = min(sum_cnt[price], budget // price)  # 该物品最多买 c 个
            budget -= price * c
            ans += c * 2
        return ans + budget // min_price  # 剩余的钱买最便宜的物品
''',
    call='Solution().maximumSaleItems([[1,6],[2,4],[3,5]], 19)',
    expect=5,
    views=[
        dict(type='array', var='cnt_factor', label='cnt_factor[f]：factor 为 f 的物品个数', h=150),
        dict(type='array', var='cnt_multi', label='cnt_multi[f]：factor 是 f 的倍数的物品个数', h=150),
        dict(type='map', var='sum_cnt', fmt=lambda k, v: f'{k}: {v}', h=150),
        dict(type='text', fn=lambda S: (f"最便宜 `min_price = {S['min_price']}`；价格 `< {S['min_price']*2}` 的才值得买一送一" if 'min_price' in S and S['min_price'] != float('inf') else ''), size=28, h=70),
    ],
    watch=[('min_price', 'min_price', 'cyan'), 'budget', ('ans', 'ans', 'green')],
    captions={
        'cnt_factor[factor] += 1': '`factor = {factor}` 的物品又多一个：`cnt_factor` = {cnt_factor}',
        'min_price = min': '记录最便宜的价格 `min_price = {min_price}`（后面买一送一要和它比）',
        'if price >= min_price * 2': lambda S, B, r: (f'`price = {S.price} >= 2×{S.min_price} = {2*S.min_price}` → 买一送一也不如买两个最便宜的，==跳过=='
                                                    if S.price >= S.min_price * 2 else f'`price = {S.price} < {2*S.min_price}` → 买一送一值得考虑'),
        'if cnt_multi[factor] == 0': '这个 factor 之前算过倍数个数吗？`cnt_multi[{factor}] = {cnt_multi[factor]}`',
        'for j in range(factor': '枚举 `{factor}` 的倍数 `j`（调和级数，总共 `O(n log n)`）',
        'cnt_multi[factor] += cnt_factor[j]': '`factor = {j}` 的物品有 `{cnt_factor[j]}` 个 → `cnt_multi[{factor}]` = =={cnt_multi[factor]}=='.replace('{j}', '{j}'),
        'cnt = cnt_multi[factor] - 1': '其他物品里能被免费拿的有 `cnt = {cnt_multi[factor]} − 1` = =={cnt}== 个（不含自己）：前 {cnt} 次购买是买一送一',
        'if cnt > 0': lambda S, B, r: ('`cnt > 0`：这个价格有买一送一名额' if S.cnt > 0 else '`cnt = 0`：买它没有赠品，不如买最便宜的'),
        'sum_cnt[price] += cnt': '相同价格的名额合并：`sum_cnt[{price}]` = =={sum_cnt[price]}==',
        'for price in sorted': '价格从低到高：先去最便宜的“买一送一”商场，`price = {price}`',
        'if budget < price': lambda S, B, r: ('`budget < price`：没钱了 → 停' if S.budget < S.price else f'`budget = {S.budget} >= {S.price}`：还买得起'),
        'c = min(': '最多买 `min({sum_cnt[price]}, {budget} // {price})` = =={c}== 个',
        'budget -= price * c': '花掉 `{price}×{c}`，`budget` → =={budget}==',
        'ans += c * 2': '每买一个送一个：`ans` += `2×{c}` → =={ans}==',
        'return ans': '送完剩下的钱买最便宜的：`{B.ans} + {budget} // {min_price}` = =={ret}==',
    },
    cards=dict(
        one_liner='多家都是买一送一，先去最便宜的那家',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每种物品无限买，总花费不超过 `budget`',
                 '买物品 `i` 最多送一个 `factor` 是 `factor_i` 倍数的其他物品，同一个有序对只能送一次',
                 '示例：`items=[[1,6],[2,4],[3,5]], budget=19` → `5`'],
        quote='想象有多家商场做活动，都是买一送一，去哪家商场买东西？优先去最便宜的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['物品 `i` 前 `cnt_i` 次购买各得 2 个，之后只能得 1 个',
              '价格 `>= 2×minPrice` 的买一送一不如买两个最便宜的 → ==直接不要==',
              '剩下的按价格从低到高买满名额，最后用余钱买最便宜的'],
        summary=['时间 `O(n log n)`，空间 `O(n)`；`cnt_i` 用调和级数枚举倍数',
                 '`cnt` 要减 1：倍数不包括物品自己',
                 '相同价格的名额合并，缩短排序长度（题解的“小优化”写法）',
                 '另有“优化前”写法：用数组 `(price, cnt)` 排序，思路相同'],
    ),
)
