CONFIG = dict(
    num=1801, title='积压订单中的订单总数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='买卖两个堆撮合订单',
    tags=['堆（优先队列）'],
    code='''
class Solution(object):
    def getNumberOfBacklogOrders(self, orders):

        sell = []
        buy = []

        for price, amount, orderType in orders:
            if orderType == 0:
                while sell and sell[0][0] <= price:
                    if amount > sell[0][1]:
                        amount -= sell[0][1]
                        heapq.heappop(sell)
                    else:
                        sell[0][1] -= amount
                        amount = 0
                        break
                if amount > 0:
                    heapq.heappush(buy, [-price, amount])
            
            else:
                while buy and -buy[0][0] >= price:
                    if amount > buy[0][1]:
                        amount -= buy[0][1]
                        heapq.heappop(buy)
                    else:
                        buy[0][1] -= amount
                        amount = 0
                        break
                if amount > 0:
                    heapq.heappush(sell, [price, amount])

        mod = 10 ** 9 + 7
        res = 0
        for price, amount in sell:
            res += amount
            if res >= mod:
                res -= mod
        
        for price, amount in buy:
            res += amount
            if res >= mod:
                res -= mod

        return res
''',
    call='Solution().getNumberOfBacklogOrders([[10,5,0],[15,2,1],[25,1,1],[30,4,0],[9,3,1]])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"当前订单：价格 `{S['price']}`，数量 `{S['amount']}`，" + ('==采购==' if S['orderType'] == 0 else '==销售==') if 'orderType' in S else '订单依次到来：采购(0) 找最低卖价，销售(1) 找最高买价')),
        dict(type='array', var='[f"{p},{a},{t}" for p, a, t in orders]', pointers={}, cell=130, h=170, label='orders：价格,数量,类型（0 采购，1 销售）'),
        dict(type='heap', var='buy', fmt=lambda x: f'价{-x[0]}×{x[1]}', h=170, label='buy：积压采购单（最大堆，价格存负数，堆顶价最高）'),
        dict(type='heap', var='sell', fmt=lambda x: f'价{x[0]}×{x[1]}', h=170, label='sell：积压销售单（最小堆，堆顶价最低）'),
    ],
    watch=[('price', 'price', 'blue'), ('amount', 'amount', 'yellow'), ('orderType', 'orderType', 'purple'), ('res', 'res', 'green')],
    captions={
        'sell = []': '`sell` 堆：积压的销售订单，==价格最低的在堆顶==',
        'buy = []': '`buy` 堆：积压的采购订单，价格取负数，==最高价在堆顶==',
        'for price, amount, orderType': lambda S, B, r: ('所有订单处理完毕' if 'price' in B and (S.price, S.amount, S.orderType) == (B.price, B.amount, B.orderType) else f'新订单：价格 `{S.price}`，数量 `{S.amount}`，类型 `{S.orderType}`'),
        'if orderType == 0': lambda S, B, r: ('`orderType = 0` → 采购订单：去找 sell 里最便宜的卖家' if S.orderType == 0 else '`orderType = 1` → 销售订单：去找 buy 里出价最高的买家'),
        'while sell and sell[0][0] <= price': lambda S, B, r: (f'sell 为空 → 没有可成交的卖单，退出' if not S.sell else
                f'最低卖价 `{S.sell[0][0]}` <= 采购价 `{S.price}`？{"成立：可以成交" if S.sell[0][0] <= S.price else "不成立：卖价太高，退出"}'),
        'if amount > sell[0][1]': '采购量 `{amount}` 比堆顶卖单量 `{sell[0][1]}` {"多：把这张卖单吃完" if amount > sell[0][1] else "少或相等：卖单有剩余"}',
        'amount -= sell[0][1]': '吃掉整张卖单：采购单还剩 `{amount}`',
        'heapq.heappop(sell)': '这张卖单被吃完，弹出',
        'sell[0][1] -= amount': '采购单被吃完，卖单剩下 `{sell[0][1]}`',
        'amount = 0': '`amount = 0`：订单用完',
        'break': '订单用完，不再找下一张',
        'heapq.heappush(buy': '还有 `{amount}` 没买到：积压到 buy，存 `[-{price}, {amount}]`',
        'while buy and -buy[0][0] >= price': lambda S, B, r: (f'buy 为空 → 没有可成交的买单，退出' if not S.buy else
                f'最高买价 `{-S.buy[0][0]}` >= 销售价 `{S.price}`？{"成立：可以成交" if -S.buy[0][0] >= S.price else "不成立：出价太低，退出"}'),
        'if amount > buy[0][1]': '销售量 `{amount}` 比堆顶买单量 `{buy[0][1]}` {"多：把这张买单吃完" if amount > buy[0][1] else "少或相等：买单有剩余"}',
        'amount -= buy[0][1]': '吃掉整张买单：销售单还剩 `{amount}`',
        'heapq.heappop(buy)': '这张买单被吃完，弹出',
        'buy[0][1] -= amount': '销售单被吃完，买单剩下 `{buy[0][1]}`',
        'heapq.heappush(sell': '还有 `{amount}` 没卖出：积压到 sell，存 `[{price}, {amount}]`',
        'mod = ': '答案对 `10^9+7` 取模',
        'for price, amount in sell': '累加 sell 里剩下的数量',
        'for price, amount in buy': '累加 buy 里剩下的数量',
        'return res': '积压订单总数 `{res}`',
    },
    cards=dict(
        one_liner='两个堆分别盯住最高买价和最低卖价，能成交就撮合',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`orders[i] = [价格, 数量, 类型]`，类型 0 是采购订单，1 是销售订单',
                 '新采购单与价格最低的积压销售单成交（卖价 ≤ 买价）；新销售单与价格最高的积压采购单成交（买价 ≥ 卖价）',
                 '没成交完的积压，最后返回积压订单总数（对 `10^9+7` 取模）；本视频：`[[10,5,0],[15,2,1],[25,1,1],[30,4,0],[9,3,1]]` → `3`'],
        quote='每当新来一笔订单时，都需要找出之前积压订单中价格最高的采购订单或价格最低的销售订单，是一个动态的最大值或最小值问题，因此可以使用两个堆buy和sell。',
        quote_src='—— yiduobo 题解原文',
        idea=['`buy` 存负价格实现最大堆，`sell` 是最小堆',
              '新单只要满足价格条件，就和堆顶成交：吃完堆顶则弹出，否则减少堆顶数量',
              '没用完的部分压进自己那一边的堆，最后把两个堆剩余数量加起来'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错点：采购堆存 `-price`，比较时要再取负',
                 '易错点：成交后直接改堆顶数量不影响堆序（价格没变）',
                 '易错点：累加时取模；题面简报缺失，题意按 LeetCode 1801 原题补写'],
    ),
)
