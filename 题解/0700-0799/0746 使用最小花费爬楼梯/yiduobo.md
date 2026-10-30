---
title: "746. 使用最小花费爬楼梯"
aliases: ["yiduobo的每日leetcode 746.使用最小花费爬楼梯"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/一-入门-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/337472901"
zhihu_id: "337472901"
zhihu_title: "yiduobo的每日leetcode 746.使用最小花费爬楼梯"
question_id: "746"
question: "使用最小花费爬楼梯"
problem_url: "https://leetcode.cn/problems/min-cost-climbing-stairs/"
difficulty: "Easy"
rating: 1500
created: "2020-12-16T22:58:26+08:00"
updated: "2020-12-16T22:58:26+08:00"
upvotes: 0
comments: 0
---

# 746. 使用最小花费爬楼梯

> **[yiduobo的每日leetcode 746.使用最小花费爬楼梯](https://zhuanlan.zhihu.com/p/337472901) · 知乎 · 2020-12-16 · 赞同 0**
> 力扣：[746. 使用最小花费爬楼梯](https://leetcode.cn/problems/min-cost-climbing-stairs/) · Easy · 灵茶山艾府：[教你一步步思考动态规划：从记忆化搜索到递推（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

746.使用最小花费爬楼梯

[力扣](https://leetcode-cn.com/problems/min-cost-climbing-stairs/)

经典的动态规划问题，设f[i]表示走到第i级台阶最少需要花费的体力，那么对于f[i]，我们可以从f[i - 1]走一步，或者从f[i - 2]走两步到达f[i]，因此有f[i] \= min(f[i - 1], f[i - 2]) + cost[i]。

边界条件为f[0] \= cost[0], f[1] \= cost[1]。最终答案为min(f[-1]，f[-2])，因为最后也可以走一步或者走两步。

由于每一轮的状态只与前面两轮的状态有关，因此可以使用三个变量来进行滚动节省空间。

最后附上python代码：

```python
class Solution(object):
    def minCostClimbingStairs(self, cost):
        """
        :type cost: List[int]
        :rtype: int
        """

        a = cost[0]
        b = cost[1]
        for w in cost[2:]:
            c = min(a, b) + w
            a, b = b, c
        
        return min(a, b)
```
