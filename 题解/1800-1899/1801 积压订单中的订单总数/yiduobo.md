---
title: "1801. 积压订单中的订单总数"
aliases: ["yiduobo的每日leetcode 1801.积压订单中的订单总数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/464015588"
zhihu_id: "464015588"
zhihu_title: "yiduobo的每日leetcode 1801.积压订单中的订单总数"
question_id: "1801"
question: "积压订单中的订单总数"
problem_url: "https://leetcode.cn/problems/number-of-orders-in-the-backlog/"
created: "2022-02-04T23:22:12+08:00"
updated: "2022-02-04T23:22:12+08:00"
upvotes: 0
comments: 0
---

# 1801. 积压订单中的订单总数

> **[yiduobo的每日leetcode 1801.积压订单中的订单总数](https://zhuanlan.zhihu.com/p/464015588) · 知乎 · 2022-02-04 · 赞同 0**
> 力扣：[1801. 积压订单中的订单总数](https://leetcode.cn/problems/number-of-orders-in-the-backlog/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1801.积压订单中的订单总数

[力扣](https://leetcode-cn.com/problems/number-of-orders-in-the-backlog/)

每当新来一笔订单时，都需要找出之前积压订单中价格最高的采购订单或价格最低的销售订单，是一个动态的最大值或最小值问题，因此可以使用两个堆buy和sell分别维护当前积压的采购订单以及销售订单。当一笔新订单过来时：

1、若其是采购订单，那么对比其价格与sell堆顶订单的价格。若大于，那么说明sell堆顶的订单可以满足当前的采购订单，此时应该用sell堆顶订单去兑换当前的采购订单。若数量不够，那么就将sell堆顶弹出，然后重复此过程直到采购订单用完，或者sell堆中没有能够满足条件的订单。

若当前采购订单没有用完，那么就将剩下的订单加入到buy堆中。

2、若其是销售订单，与上面也类似，不过这里要求的是当前销售订单的价格要小于等于buy堆顶订单的价格。其他操作与上面都一致。

若当前销售订单没有用完，那么就将剩下的订单加入到sell堆中。

遍历完成后，堆中剩下的都是用不出去的订单，这些订单的总数就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def getNumberOfBacklogOrders(self, orders):
        """
        :type orders: List[List[int]]
        :rtype: int
        """

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
```
