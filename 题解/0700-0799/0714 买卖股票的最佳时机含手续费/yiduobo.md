---
title: "714. 买卖股票的最佳时机含手续费"
aliases: ["yiduobo的每日leetcode 714.买卖股票的最佳时机含手续费"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/329026804"
zhihu_id: "329026804"
zhihu_title: "yiduobo的每日leetcode 714.买卖股票的最佳时机含手续费"
question_id: "714"
question: "买卖股票的最佳时机含手续费"
problem_url: "https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/"
difficulty: "Medium"
created: "2020-12-03T23:34:14+08:00"
updated: "2020-12-03T23:34:14+08:00"
upvotes: 0
comments: 0
---

# 714. 买卖股票的最佳时机含手续费

> **[yiduobo的每日leetcode 714.买卖股票的最佳时机含手续费](https://zhuanlan.zhihu.com/p/329026804) · 知乎 · 2020-12-03 · 赞同 0**
> 力扣：[714. 买卖股票的最佳时机含手续费](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/) · Medium · 灵茶山艾府：[【视频】教你一步步思考动态规划，股票买卖通用方法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

714.买卖股票的最佳时机含手续费

[力扣](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/)

买卖股票系列问题，依然是动态规划来解决。

令f[i]表示在第i天时持仓最大的收益，g[i]则表示第i天未持仓最大的收益。

对于f[i]，要么是第i - 1天持仓，第i天不进行任何操作，要么是第i - 1天不持仓，第i天买进，因此有

f[i] \= max(f[i - 1]，g[i - 1] - prices[i])

对于g[i]，要么是第i - 1天不持仓，第i天不进行任何操作，要么是第i - 1天持仓，第i天卖出，因此有

g[i] \= max(g[i - 1]，f[i - 1] + prices[i] - fee)

边界条件为f[0] \= -prices[0]，g[0] \= 0

注意到这里f和g的状态都只与前一天的状态有关，因此可以使用两个变量来滚动节省空间。

最后附上python代码，其中hold替代f数组，res替代g数组：

```python
class Solution(object):
    def maxProfit(self, prices, fee):
        """
        :type prices: List[int]
        :type fee: int
        :rtype: int
        """

        hold = -prices[0]
        res = 0
        for price in prices[1:]:
            tmp = hold
            hold = max(hold, res - price)
            res = max(res, tmp + price - fee)
        
        return res
```
