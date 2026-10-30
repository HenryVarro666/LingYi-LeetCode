---
title: "4050. 得到恰好N分的最少天数"
aliases: ["yiduobo的每日leetcode 4050.得到恰好N分的最少天数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/graph-theory", "leetcode/shortest-path", "leetcode/complete-knapsack", "leetcode/heap-priority-queue"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2083321067498649172"
zhihu_id: "2083321067498649172"
zhihu_title: "yiduobo的每日leetcode 4050.得到恰好N分的最少天数"
question_id: "4050"
question: "得到恰好 N 分的最少天数"
problem_url: "https://leetcode.cn/problems/minimum-days-to-score-exactly-n-points/"
difficulty: "Medium"
created: "2026-09-15T22:34:44+08:00"
updated: "2026-09-15T22:34:44+08:00"
upvotes: 0
comments: 0
---

# 4050. 得到恰好N分的最少天数

> **[yiduobo的每日leetcode 4050.得到恰好N分的最少天数](https://zhuanlan.zhihu.com/p/2083321067498649172) · 知乎 · 2026-09-15 · 赞同 0**
> 力扣：[4050. 得到恰好 N 分的最少天数](https://leetcode.cn/problems/minimum-days-to-score-exactly-n-points/) · Medium · 灵茶山艾府：[两种方法：完全背包 / Dijkstra 最短路（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4050.得到恰好N分的最少天数

<https://leetcode.cn/problems/minimum-days-to-score-exactly-n-points/description/>

题目给出一个整数n，表示目标分数。

在初始情况下，拥有的分数为0，而每天可以选择获得分数，也可以选择跳过。

分数是在连胜期间获得的。在第一天，将获得1分，第二天获得2分，第三天获得3分，以此类推。跳过一天将获得0分，同时连胜将被重置，也就是说在跳过之后，下一次得分将重新从1分开始。

问恰好得到n分所需的最少天数（包括跳过的天数）。

题目实际上就是要用最少的(1 + k) \* k // 2来拼凑出n，这是一个标准的背包问题，因此可以先预处理出不超过n的所有(1 + k) \* k // 2，将其作为物品占用的体积，然后将k + 1作为使用这个物品的代价。这里额外的加1是因为选择不同物品之间需要有至少一天的跳过作为间隔，另外由于第一次选择不需要计算这个间隔，因此可以将背包的初始情况的代价设置为-1来抵消掉第一次选择多计算的这个代价。

最后附上python代码：

```python
class Solution(object):
    def minDays(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        candidate = [0]
        while candidate[-1] <= n:
            candidate.append(candidate[-1] + len(candidate))
        
        f = [None] * (n + 1)
        f[0] = -1
        for cost in range(len(candidate) - 1, 0, -1):
            v = candidate[cost]
            for x in range(v, n + 1):
                if f[x - v] is not None and (f[x] is None or f[x] > f[x - v] + cost + 1):
                    f[x] = f[x - v] + cost + 1
        
        return f[n]
```
