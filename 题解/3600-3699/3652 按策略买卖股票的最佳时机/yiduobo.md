---
title: "3652. 按策略买卖股票的最佳时机"
aliases: ["yiduobo的每日leetcode 3652.按策略买卖股票的最佳时机"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/prefix-sum", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/常用数据结构", "题单/滑动窗口与双指针/一-定长滑动窗口", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1948879369784263835"
zhihu_id: "1948879369784263835"
zhihu_title: "yiduobo的每日leetcode 3652.按策略买卖股票的最佳时机"
question_id: "3652"
question: "按策略买卖股票的最佳时机"
problem_url: "https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-using-strategy/"
difficulty: "Medium"
rating: 1557
created: "2025-09-11T23:59:45+08:00"
updated: "2025-09-11T23:59:48+08:00"
upvotes: 0
comments: 0
---

# 3652. 按策略买卖股票的最佳时机

> **[yiduobo的每日leetcode 3652.按策略买卖股票的最佳时机](https://zhuanlan.zhihu.com/p/1948879369784263835) · 知乎 · 2025-09-11 · 赞同 0**
> 力扣：[3652. 按策略买卖股票的最佳时机](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-using-strategy/) · Medium · 灵茶山艾府：[两种方法：前缀和 / 定长滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3652.按策略买卖股票的最佳时机

<https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-using-strategy/description/>

题目给出两个整数数组prices和strategy，其中prices[index]表示第index天的股票价格，strategy[index]表示第index天的交易策略，-1表示买入，0表示不行动，1表示卖出。

另外给出一个偶数k，表示可以对strategy进行最多一次修改，从中选取k个连续元素，将前k / 2个元素设为0，后k / 2个元素设为1。

定义利润为所有天数中strategy[index] \* prices[index]之和，问可能获得的最大利润。

如果不考虑修改操作，最终答案就是strategy和prices的点积，可以先计算出来，作为答案的初始值。接下来对于修改操作，可以理解成使用一个长度为k的窗口从数组头部开始向后滑动。

对于最开始的k个元素，可以先将strategy[:k]与prices[:k]的点积从利润中减去，然后再将prices[k//2 : k]累加到利润中。

接下来，让窗口向后滑动。不妨设当前窗口的右边界移动到了index，那么:

1、此时原始窗口的左边界为index - k，也就是说strategy[index - k]将从0变回原始的strategy[index - k]，因此需要将strategy[index - k] \* prices[index - k]加回到利润中

2、此时窗口的前半段将移动到index - k + k // 2，也就是说其对应的strategy[index - k + k // 2]将从0变为1，因此需要将prices[index - k + k // 2]加入到利润中

3、此时窗口的右边界移动到了k，也就是说strategy[index]将变为1，因此需要将原始的strategy[index] \* prices[index]从利润中减去，然后再将prices[index]加入到利润中

完成一次移动后，使用当前利润更新最终答案，然后将窗口继续向后移动，直到移动到数组末尾即可。

最后附上python代码：

```python
class Solution(object):
    def maxProfit(self, prices, strategy, k):
        """
        :type prices: List[int]
        :type strategy: List[int]
        :type k: int
        :rtype: int
        """
        
        now = sum([p * s for p, s in zip(prices, strategy)])
        res = now

        for index in range(k):
            now -= prices[index] * strategy[index]
            if index >= k // 2:
                now += prices[index]

        res = max(res, now)
        for index in range(k, len(prices)):
            now += prices[index - k] * strategy[index - k]
            now -= prices[index - k + k // 2]
            now -= prices[index] * strategy[index]
            now += prices[index]
            res = max(res, now)

        return res
```
