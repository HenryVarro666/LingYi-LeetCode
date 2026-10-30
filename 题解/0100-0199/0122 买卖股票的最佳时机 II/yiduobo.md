---
title: "122. 买卖股票的最佳时机II"
aliases: ["yiduobo的每日leetcode 122.买卖股票的最佳时机II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/di-tui", "题单/动态规划", "题单/面试经典-150-题", "题单/动态规划/六-状态机-DP", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/139784662"
zhihu_id: "139784662"
zhihu_title: "yiduobo的每日leetcode 122.买卖股票的最佳时机II"
question_id: "122"
question: "买卖股票的最佳时机 II"
problem_url: "https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/"
difficulty: "Medium"
created: "2020-05-11T22:35:27+08:00"
updated: "2020-05-11T22:35:27+08:00"
upvotes: 0
comments: 0
---

# 122. 买卖股票的最佳时机II

> **[yiduobo的每日leetcode 122.买卖股票的最佳时机II](https://zhuanlan.zhihu.com/p/139784662) · 知乎 · 2020-05-11 · 赞同 0**
> 力扣：[122. 买卖股票的最佳时机 II](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/) · Medium · 灵茶山艾府：[【视频】教你一步步思考动态规划，股票问题通用解法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

122.买卖股票的最佳时机II<https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-ii/>

上一题的升级版本，可以用贪心法来做。

首先可以明确的是，股价连续保持不变的情况在这里是没有意义的，因此实际上可以分为两种波动情况，即连续上涨与连续下降。

若价格连续上涨，即prices[k] \< prices[k + 1] \< prices[k + 2] \< ... \< prices[m]，那么这里

1、在k买进，在m卖出，收益为prices[m] - prices[k]

2、在k买进，在k + 1卖出，同时在k + 1买进，在k + 2卖出...，收益为

(prices[k +1] - prices[k])+(prices[k + 2] - prices[k + 1])+ ... +(prices[m] - prices[m - 1])

化简后依然是prices[m] - prices[k]

若价格连续下降，那么不应当进行操作，高位接盘是不明智的。

于是可以一趟扫描，每次对比prices[k]与prices[k - 1]。若prices[k - 1] \< prices[k]，那么在k - 1买入，在k卖出。若prices[k - 1] >\= prices[k]，则什么都不做。

最后附上python代码：

```python
class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """

        ans = 0
        if not prices:
            return 0

        for index in range(1, len(prices)):
            if prices[index] > prices[index - 1]:
                ans += prices[index] - prices[index - 1]

        return ans
```
