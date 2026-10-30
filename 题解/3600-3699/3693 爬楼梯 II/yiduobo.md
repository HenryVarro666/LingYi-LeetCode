---
title: "3693. 爬楼梯II"
aliases: ["yiduobo的每日leetcode 3693.爬楼梯II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/一-入门-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1956113872026047700"
zhihu_id: "1956113872026047700"
zhihu_title: "yiduobo的每日leetcode 3693.爬楼梯II"
question_id: "3693"
question: "爬楼梯 II"
problem_url: "https://leetcode.cn/problems/climbing-stairs-ii/"
difficulty: "Medium"
rating: 1560
created: "2025-09-30T22:45:13+08:00"
updated: "2025-09-30T22:45:15+08:00"
upvotes: 0
comments: 0
---

# 3693. 爬楼梯II

> **[yiduobo的每日leetcode 3693.爬楼梯II](https://zhuanlan.zhihu.com/p/1956113872026047700) · 知乎 · 2025-09-30 · 赞同 0**
> 力扣：[3693. 爬楼梯 II](https://leetcode.cn/problems/climbing-stairs-ii/) · Medium · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到空间优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3693.爬楼梯II

[3693. 爬楼梯 II - 力扣（LeetCode）](https://leetcode.cn/problems/climbing-stairs-ii/)

给出一个有n + 1级台阶的楼梯，编号为0到n。另外还给出一个长度为n的下标从1开始的整数数组costs，其中costs[i]表示第i级台阶的成本。

从第i级台阶出发，只能走到第i + 1、i + 2、i + 3级台阶之一。从台阶i跳到台阶j的成本为costs[j] + (j - i)^2。

现在要求计算从0走到n所需的最小成本。

非常经典的动态规划问题，令f[index]表示走到台阶index所需的最小成本，那么对于f[index]，可以从index - 1、index - 2、index - 3走来，对应的成本分别为f[index - 1] + 1 + costs[index]、f[index - 2] + 4 + costs[index]、f[index - 3] + 9 + costs[index]，取其中的最小值作为f[index]即可，当然，这里有一个前提是对应的f值需要存在。

另外，由于每一轮状态只与前三个状态有关，因此在这里可以使用f、g、h三变量迭代，省去数组的空间开销。

最后附上python代码：

```python
class Solution(object):
    def climbStairs(self, n, costs):
        """
        :type n: int
        :type costs: List[int]
        :rtype: int
        """
        
        f, g, h = None, None, 0
        for c in costs:
            best = c + 1 + h
            if g is not None and g + c + 4 < best:
                best = g + c + 4
            if f is not None and f + c + 9 < best:
                best = f + c + 9
            f, g, h = g, h, best
            
        return h
```
