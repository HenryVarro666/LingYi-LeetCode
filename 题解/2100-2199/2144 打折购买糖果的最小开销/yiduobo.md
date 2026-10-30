---
title: "2144. 打折购买糖果的最小开销"
aliases: ["yiduobo的每日leetcode 2144.打折购买糖果的最小开销"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/529368900"
zhihu_id: "529368900"
zhihu_title: "yiduobo的每日leetcode 2144.打折购买糖果的最小开销"
question_id: "2144"
question: "打折购买糖果的最小开销"
problem_url: "https://leetcode.cn/problems/minimum-cost-of-buying-candies-with-discount/"
difficulty: "Easy"
rating: 1261
created: "2022-06-15T22:35:24+08:00"
updated: "2022-06-15T22:35:24+08:00"
upvotes: 0
comments: 0
---

# 2144. 打折购买糖果的最小开销

> **[yiduobo的每日leetcode 2144.打折购买糖果的最小开销](https://zhuanlan.zhihu.com/p/529368900) · 知乎 · 2022-06-15 · 赞同 0**
> 力扣：[2144. 打折购买糖果的最小开销](https://leetcode.cn/problems/minimum-cost-of-buying-candies-with-discount/) · Easy · 灵茶山艾府：[如何证明贪心是对的？（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2144.打折购买糖果的最小开销

[力扣](https://leetcode.cn/problems/minimum-cost-of-buying-candies-with-discount/)

由于赠送的糖果价格不能超过购买的两颗糖果，因此最贵的两颗糖果就只能靠买的。购买了最贵的两颗糖果之后，可以免费获得一颗糖果，此时显然就应该选择获得第三贵的糖果，接下来只需要以此类推就行了。

于是可以将糖果按价格从大到小排序，之后所有下标模3余2的糖果都是免费获取的，那么只需将所有糖果价格的总和减去这些糖果的价格即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, cost):
        """
        :type cost: List[int]
        :rtype: int
        """

        res = sum(cost)
        sorted_cost = sorted(cost, reverse=True)
        for index in range(2, len(sorted_cost), 3):
            res -= sorted_cost[index]
        
        return res
```
