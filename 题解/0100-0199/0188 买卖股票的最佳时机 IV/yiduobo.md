---
title: "188. 买卖股票的最佳时机 IV"
aliases: ["yiduobo的每日leetcode 188.买卖股票的最佳时机 IV"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/面试经典-150-题", "题单/动态规划/六-状态机-DP", "题单/动态规划/十一-优化-DP", "题单/面试经典-150-题/多维动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/145446807"
zhihu_id: "145446807"
zhihu_title: "yiduobo的每日leetcode 188.买卖股票的最佳时机 IV"
question_id: "188"
question: "买卖股票的最佳时机 IV"
problem_url: "https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iv/"
difficulty: "Hard"
created: "2020-06-02T23:55:48+08:00"
updated: "2020-06-02T23:55:48+08:00"
upvotes: 1
comments: 0
---

# 188. 买卖股票的最佳时机 IV

> **[yiduobo的每日leetcode 188.买卖股票的最佳时机 IV](https://zhuanlan.zhihu.com/p/145446807) · 知乎 · 2020-06-02 · 赞同 1**
> 力扣：[188. 买卖股票的最佳时机 IV](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iv/) · Hard · 灵茶山艾府：[【视频】教你一步步思考动态规划！股票问题通用解法！（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

188.买卖股票的最佳时机 IV <https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-iv/>

这题居然有第四个版本了，可以预见的是应该还会有第五第六甚至更多版本。。。

题目这里指定了买卖的次数k，于是可以先讨论这个k与价格数组prices的长度n的关系。若k满足k >\= n/2，那么可以看做是不限次数的买入卖出股票，于是问题就退化到了122题买卖股票的最佳时机II（传送门在这里[yiduobo：yiduobo的每日leetcode 122.买卖股票的最佳时机II](https://zhuanlan.zhihu.com/p/139784662)）。

如果k \< n/2，那么就只能老老实实用动态规划来做了。具体的做法与123题买卖股票的最佳时机III（传送门在这里[yiduobo：yiduobo的每日leetcode 123.买卖股票的最佳时机III](https://zhuanlan.zhihu.com/p/139790696)）一样，设置状态f[i][j]表示前i天达成第j中状态时的最佳获利是多少。

j的取值从0到k \* 2 - 1，分别为：

j \= 0，表示刚进行了第一次买进。

j \= 1，表示刚进行了第一次卖出。

j \= 2，表示刚进行了第二次买进。

j \= 3，表示刚进行了第二次卖出。

...

j \= k \* 2 - 2，表示刚进行了第k次买进。

j \= k \* 2 - 1，表示刚进行了第k次卖出。

于是答案就是max(0, f[n][1], f[n][3], ... , f[n][k \* 2 - 1])。

状态转移的过程也与123题相同，所有j \= x的状态都是从j \= x - 1的状态转移过来的。边界条件j \= 0表示买入一次最少亏多少，取前i天中prices中最小值即可。

另外，由于所有的f都至于前一天的状态有关，于是还是可以用上滚动数组。不过同样需要注意滚动时需要从k + k - 1开始往0滚动，因为今天的k + k - 1需要昨天的k + k - 2来更新，所以不能先更新今天k + k - 2。

最后附上python代码，其中flag表示当前状态应该是买入还是卖出，这决定了prices的符号：

```python
class Solution(object):
    def maxProfit(self, k, prices):
        """
        :type k: int
        :type prices: List[int]
        :rtype: int
        """

        if len(prices) < 2 or not k:
            return 0

        if k >= len(prices) / 2:
            res = 0
            for index in range(1, len(prices)):
                if prices[index] > prices[index - 1]:
                    res += prices[index] - prices[index - 1]
            return res

        f = [None] * (k * 2)
        f[0] = -prices[0]
        for i in range(1, len(prices)):
            for j in range(k + k - 1, 0, -1):
                if j % 2 == 1:
                    flag = 1
                else:
                    flag = -1

                if f[j - 1] is not None:
                    if f[j] is None or f[j] < f[j - 1] + flag * prices[i]:
                        f[j] = f[j - 1] + flag * prices[i]

                f[0] = max(f[0], -prices[i])

        res = 0
        for i in range(k):
            if f[i * 2 - 1] is not None:
                res = max(res, f[i * 2 - 1])

        return res
```
