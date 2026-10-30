---
title: "2907. 价格递增的最大利润三元组I"
aliases: ["yiduobo的每日leetcode 2907.价格递增的最大利润三元组I"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/664008000"
zhihu_id: "664008000"
zhihu_title: "yiduobo的每日leetcode 2907.价格递增的最大利润三元组I"
question_id: "2907"
question: "价格递增的最大利润三元组I"
problem_url: "https://leetcode.cn/problems/maximum-profitable-triplets-with-increasing-prices-i/"
created: "2023-10-30T04:07:32+08:00"
updated: "2023-10-30T04:07:32+08:00"
upvotes: 0
comments: 0
---

# 2907. 价格递增的最大利润三元组I

> **[yiduobo的每日leetcode 2907.价格递增的最大利润三元组I](https://zhuanlan.zhihu.com/p/664008000) · 知乎 · 2023-10-30 · 赞同 0**
> 力扣：[2907. 价格递增的最大利润三元组I](https://leetcode.cn/problems/maximum-profitable-triplets-with-increasing-prices-i/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2907.价格递增的最大利润三元组I

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-profitable-triplets-with-increasing-prices-i/)

对于这类三元组问题，通常的处理方法是枚举中间的j，那么问题就变成了给出prices[j]和profits[j]，要求找出j左侧的i，满足prices[i]小于prices[j]且profits[i]最大，以及找出j右侧的k，满足prices[j]小于prices[k]且profits[k]最大。由于题目中prices的取值范围在可接受的范围内，因此就可以利用树状数组来得到前缀中，价格小于等于某个阈值的最大profit。同样的，也可以反向遍历，得到后缀中价格大于等于某个阈值的最大profit，不过在这里需要进行一些变形来适配树状数组。接下来就只需一趟遍历枚举j，利用这两个树状数组计算答案了。

我在这里并未采取枚举j的方式，因为感觉反向处理感觉比较别扭。为了适配树状数组的特性，我在这里采取的枚举k的做法，同样是使用两个树状数组来进行处理。

其中第一个树状数组维护前缀中单件商品价格不超过某个阈值的最大profit，而第二个树状数组则是针对前缀中两件商品的组合。若两件商品满足下标较小的商品价格小于下标较大的商品，那么就可以通过树状数组维护较贵商品的价格不超过某个阈值时，这两件商品的最大profit和。

更形式化的说，第一个树状数组维护的就是前缀中最优的i，而第二个树状数组维护的则是前缀中最优的(i, j)对，那么对于枚举的k，先使用第二个树状数组更新答案，然后利用第一个树状数组与prices[k]以及profits[k]更新第二个树状数组，最后利用prices[k]以及profits[k]更新第一个树状数组即可。

需要注意的是，由于第二个树状数组的下标是两件商品的价格之和，因此在这里需要为其开到两倍的空间。

最后附上python代码：

```python
class Solution(object):
    def maxProfit(self, prices, profits):
        """
        :type prices: List[int]
        :type profits: List[int]
        :rtype: int
        """

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
```
