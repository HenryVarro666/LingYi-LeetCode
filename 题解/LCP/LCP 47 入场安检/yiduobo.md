---
title: "LCP 47. 入场安检"
aliases: ["yiduobo的每日leetcode LCP47.入场安检"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/brainteaser", "leetcode/dynamic-programming", "leetcode/0-1-knapsack", "leetcode/dp", "leetcode/dp-2", "题单/动态规划", "题单/动态规划/三-背包"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/576914542"
zhihu_id: "576914542"
zhihu_title: "yiduobo的每日leetcode LCP47.入场安检"
question_id: "LCP 47"
question: "入场安检"
problem_url: "https://leetcode.cn/problems/oPs9Bm/"
difficulty: "Hard"
created: "2022-10-25T01:18:42+08:00"
updated: "2022-10-25T01:18:42+08:00"
upvotes: 0
comments: 0
---

# LCP 47. 入场安检

> **[yiduobo的每日leetcode LCP47.入场安检](https://zhuanlan.zhihu.com/p/576914542) · 知乎 · 2022-10-25 · 赞同 0**
> 力扣：[LCP 47. 入场安检](https://leetcode.cn/problems/oPs9Bm/) · Hard · 灵茶山艾府：[转换为 01 背包方案数](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP47.入场安检

[力扣](https://leetcode.cn/problems/oPs9Bm/)

leetcode如果找不到好的背景描述，我觉得直接用栈和队列说就行了，这强行搞个安检的背景，也不知道哪里的安检人进去之后就不让出来了的。

题目给出了若干个房间，其中第i个房间可以选择留下capacities[i] - 1名游客，或者不留下任何游客。问最终留下k - 1名游客的方案数量。这是一个典型的背包问题，直接使用经典的f[i][j]表示前i个房间留下j名游客的方案总数，那么对于f[i][j]，就有f[i][j] \= f[i - 1][j] + f[i - 1][j - (capacities[i] - 1)]，即选择不留下任何游客，或者留下capacities[i] - 1名游客。

动态规划完成后，f[-1][k]就是最终答案。

注意到这里的状态转移只与前一轮有关，那么还可以通过滚动数组省略掉i这一维。

最后附上python代码：

```python
class Solution(object):
    def securityCheck(self, capacities, k):
        """
        :type capacities: List[int]
        :type k: int
        :rtype: int
        """

        f = [0] * (k + 1)
        f[0] = 1
        mod = 10 ** 9 + 7
        for c in capacities:
            for j in range(k, c - 2, -1):
                f[j] += f[j - (c - 1)]
                if f[j] >= mod:
                    f[j] -= mod
        
        return f[k]
```
