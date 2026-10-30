---
title: "3573. 买卖股票的最佳时机V"
aliases: ["yiduobo的每日leetcode 3573.买卖股票的最佳时机V"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/六-状态机-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1936927292673728949"
zhihu_id: "1936927292673728949"
zhihu_title: "yiduobo的每日leetcode 3573.买卖股票的最佳时机V"
question_id: "3573"
question: "买卖股票的最佳时机 V"
problem_url: "https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-v/"
difficulty: "Medium"
rating: 1777
created: "2025-08-08T00:40:07+08:00"
updated: "2025-08-08T00:40:08+08:00"
upvotes: 1
comments: 0
---

# 3573. 买卖股票的最佳时机V

> **[yiduobo的每日leetcode 3573.买卖股票的最佳时机V](https://zhuanlan.zhihu.com/p/1936927292673728949) · 知乎 · 2025-08-08 · 赞同 1**
> 力扣：[3573. 买卖股票的最佳时机 V](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-v/) · Medium · 灵茶山艾府：[状态机 DP：在 188 题的基础上增加一个状态（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3573.买卖股票的最佳时机V

[3573. 买卖股票的最佳时机 V - 力扣（LeetCode）](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-v/description/)

题目给出一个整数数组prices，长度不超过1000。其中prices[index]表示第index天的股票价格。另外给出一个整数k，表示最多可以进行k笔交易，k不超过prices长度的一半。

每笔交易可以是一下类型之一：

1、普通交易：在第i天买入，然后在之后的第j天卖出，其中i \< j，得到的利润为prices[j] - prices[i]。

2、做空交易：在第i天卖出，然后在之后的第j天买回，其中i \< j，得到的利润为prices[i] - prices[j]。

需要注意，在开始下一笔交易之前必须完成当前交易，另外也不能在买入和卖出的同一天再次买入或者卖出。

问经过最多k笔交易可以获得的最大利润。

从题目给出的数据规模来看，O(n^2)的算法是比较合适的，比较直观的思路就是使用动态规划，记录前i天完成j笔交易时的最大收益。

注意到题中有不持仓、持有多单、持有空单这三种状态，于是可以令long_hold[i][j]表示前i天完成j笔交易，目前持有多单股票时的最大收益，同样的，令short_hold[i][j]表示持有空单股票时的最大收益，unhold[i][j]则表示没有持仓时的最大收益。

接下来对于long_hold[i][j]和short_hold[i][j]，可以直接从long_hold[i - 1][j]和short_hold[i - 1][j]转移过来，表示对prices[i]不进行操作，也可以从unhold[i - 1][j]转移过来，不同之处在于long_hold[i][j]将买入prices[i]，而short_hold[i][j]则应该卖出prices[i][j]，即

long_hold[i][j] \= max(long_hold[i - 1][j], unhold[i - 1][j] - prices[i])

short_hold[i][j] \= max(short_hold[i - 1][j], unhold[i - 1][j] + prices[i])

而对于unhold[i][j]，其可以从unhold[i - 1][j]转移过来，表示对prices[i]不进行操作，也可以从long_hold[i - 1][j - 1]或者short_hold[i - 1][j - 1]转移过来，表示通过卖出或者买入prices[i]完成了j对应的这一笔交易，即

unhold[i][j] \= max(unhold[i - 1][j], long_hold[i - 1][j - 1] + prices[i], short_hold[i - 1][j - 1] - prices[i])

全部计算完成后，最终答案就是max(unhold[-1])。

另外注意到所有的转移方程中，i对应的项都只与i - 1对应的项有关，因此只需要限定j从大到小进行更新，同时先更新long_hold与short_hold，再更新unhold，就能省去i这一维。这个更新的顺序取决于转移方程中j的关系，具体问题需要具体分析，不过总的原则是被依赖的项需要后更新，如果互相依赖，就需要同时更新或者通过保存副本来进行更新。

最后附上python代码：

```python
class Solution(object):
    def maximumProfit(self, prices, k):
        """
        :type prices: List[int]
        :type k: int
        :rtype: int
        """
        
        long_hold = [None] * (k + 1)
        short_hold = [None] * (k + 1)
        unhold = [None] * (k + 1)
        unhold[0] = 0

        for p in prices:
            for index in range(k, 0, -1):
                if index < k and unhold[index] is not None:
                    if long_hold[index] is None or long_hold[index] < unhold[index] - p:
                        long_hold[index] = unhold[index] - p
                    if short_hold[index] is None or short_hold[index] < unhold[index] + p:
                        short_hold[index] = unhold[index] + p
                
                if short_hold[index - 1] is not None:
                    if unhold[index] is None or unhold[index] < short_hold[index - 1] - p:
                        unhold[index] = short_hold[index - 1] - p
                
                if long_hold[index - 1] is not None:
                    if unhold[index] is None or unhold[index] < long_hold[index - 1] + p:
                        unhold[index] = long_hold[index - 1] + p

            if long_hold[0] is None or long_hold[0] < -p:
                long_hold[0] = -p
            if short_hold[0] is None or short_hold[0] < p:
                short_hold[0] = p

        return max(unhold)
```
