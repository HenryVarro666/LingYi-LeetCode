---
title: "309. 最佳买卖股票时机含冷冻期"
aliases: ["yiduobo的每日leetcode 309.最佳买卖股票时机含冷冻期"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/158771300"
zhihu_id: "158771300"
zhihu_title: "yiduobo的每日leetcode 309.最佳买卖股票时机含冷冻期"
question_id: "309"
question: "买卖股票的最佳时机含冷冻期"
problem_url: "https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-cooldown/"
difficulty: "Medium"
created: "2020-07-11T18:58:30+08:00"
updated: "2020-07-11T18:58:30+08:00"
upvotes: 0
comments: 2
---

# 309. 最佳买卖股票时机含冷冻期

> **[yiduobo的每日leetcode 309.最佳买卖股票时机含冷冻期](https://zhuanlan.zhihu.com/p/158771300) · 知乎 · 2020-07-11 · 赞同 0**
> 力扣：[309. 买卖股票的最佳时机含冷冻期](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-cooldown/) · Medium · 灵茶山艾府：[【视频】教你一步步思考动态规划！股票问题通用解法！（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

309.最佳买卖股票时机含冷冻期<https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/>

又是股票系列问题。做法与之前类似，也是使用动态规划，状态为每天持仓或者卖出时的最佳收益，不过这里还需要额外添加一个冷冻期状态。

于是这里使用三个数组hold，sell，cold来分别表示持有股票、卖出股票以及冷冻期，那么对于第i天：

1、对于hold[i]，表示其在第i天持有股票，那么可以是从第i - 1天继续持仓，也可以是第i - 1天为冷冻期，然后在第i天买入，于是有

hold[i] \= max(hold[i - 1]，cold[i - 1] - prices[i])

2、对于sell[i]，表示其在第i天卖出了股票，于是其在第i - 1天必须持仓，于是有

sell[i] \= hold[i - 1] + prices[i]

3、对于cold[i]，表示其在第i天为冷冻期，那么可能是在第i - 1天卖出了股票导致第i天必须为冷冻期，也可能是第i - 1天就是冷冻期，而第i天什么都没有做，因此有

cold[i] \= max(cold[i - 1]，sell[i - 1])

于是，最后的答案就是max(sell[-1]，cold[-1])

边界条件为hold[0] \= -prices[0]，sell[0] \= None，cold[0] \= 0

可以发现，所有的状态转移都只与前一天的状态有关，于是可以使用滚动数组来进行优化。需要注意的是，三种状态与前一天的状态都互相交织，因此需要使用临时变量储存前一天的状态才能更新今天的状态。

最后附上python代码：

```python
class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        
        if len(prices) < 2:
            return 0

        hold = -prices[0]
        cold = 0
        sell = None
        
        for price in prices[1:]:
            tmp_hold = hold
            hold = max(hold, cold - price)
            if sell is not None:
                cold = max(cold, sell)
            sell = tmp_hold + price

        return max(sell, cold)
```
