---
title: "322. 零钱兑换"
aliases: ["yiduobo的每日leetcode 322.零钱兑换"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/graph-theory", "题单/动态规划", "题单/图论算法", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/动态规划/三-背包", "题单/图论算法/一-图的遍历", "题单/LeetCode-热题-100/动态规划", "题单/面试经典-150-题/一维动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/160188516"
zhihu_id: "160188516"
zhihu_title: "yiduobo的每日leetcode 322.零钱兑换"
question_id: "322"
question: "零钱兑换"
problem_url: "https://leetcode.cn/problems/coin-change/"
difficulty: "Medium"
created: "2020-07-15T21:22:56+08:00"
updated: "2020-07-15T21:22:56+08:00"
upvotes: 1
comments: 0
---

# 322. 零钱兑换

> **[yiduobo的每日leetcode 322.零钱兑换](https://zhuanlan.zhihu.com/p/160188516) · 知乎 · 2020-07-15 · 赞同 1**
> 力扣：[322. 零钱兑换](https://leetcode.cn/problems/coin-change/) · Medium · 灵茶山艾府：[两种方法：完全背包 / BFS 最短路（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

322.零钱兑换<https://leetcode-cn.com/problems/coin-change/>

经典的动态规划问题，称作背包问题，具体解法是使用动态规划，f[i]表示凑够i块钱最少需要多少个硬币，那么就需要枚举每一种面值的硬币coin[j]，然后看做从i - coin[j]块钱这个状态拿了coin[j]之后达成了i块钱，于是有f[i] \= min(f[i - coin[j]) + 1。当然，这里的i必须大于等于coin[j]。边界条件自然是f[0] \= 0了。

两重循环，因此最终的时间复杂度为O(amounts \* len(coins))。

当然，注意到这里的硬币可以拿任意多次，因此理论上应该可以在硬币面值上做一些优化。例如样例中的1、2、5，面值为1的硬币就不应该拿两次或以上，因为拿两个1块的硬币就不如拿一个2块的硬币。同样的，2块的硬币不应该拿三次或以上，因为拿三个2块的硬币就不如拿一个1块和一个5块的硬币。

因此对于每种硬币应该都可以先算出其最多可以拿多少次然后可能可以利用起来加以优化，不够具体的做法我还没什么思路。这里就先按最简单的来实现：

```python
class Solution(object):
    def coinChange(self, coins, amount):
        """
        :type coins: List[int]
        :type amount: int
        :rtype: int
        """

        f = [-1] * (amount + 1)
        f[0] = 0
        for i in range(1, amount + 1):
            for coin in coins:
                if i >= coin and f[i - coin] >= 0 and (f[i] < 0 or f[i] > f[i - coin] + 1):
                    f[i] = f[i - coin] + 1

        return f[amount]
```
