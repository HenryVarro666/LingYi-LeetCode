---
title: "2585. 获得分数的方法数"
aliases: ["yiduobo的每日leetcode 2585.获得分数的方法数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/三-背包"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/642978229"
zhihu_id: "642978229"
zhihu_title: "yiduobo的每日leetcode 2585.获得分数的方法数"
question_id: "2585"
question: "获得分数的方法数"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-earn-points/"
difficulty: "Hard"
rating: 1910
created: "2023-07-12T00:58:09+08:00"
updated: "2023-07-12T00:58:09+08:00"
upvotes: 0
comments: 0
---

# 2585. 获得分数的方法数

> **[yiduobo的每日leetcode 2585.获得分数的方法数](https://zhuanlan.zhihu.com/p/642978229) · 知乎 · 2023-07-12 · 赞同 0**
> 力扣：[2585. 获得分数的方法数](https://leetcode.cn/problems/number-of-ways-to-earn-points/) · Hard · 灵茶山艾府：[【模板】多重背包求方案数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2585.获得分数的方法数

[力扣](https://leetcode.cn/problems/number-of-ways-to-earn-points/)

经典的背包问题。令f\[k\]\[i\]表示前k类题目获得i分的方案数，那么对于f\[k\]\[i\]，可以从0到count\[k - 1\]枚举第k - 1题的数目j，那么就有f\[k\]\[i\] \= f\[k - 1\]\[i\] + f\[k - 1\]\[i - marks\[k - 1\]\] + f\[k - 1\]\[i - marks\[k - 1\] \* 2\] + ... + f\[k - 1\]\[i - marks\[k - 1\] \* count\[k - 1\]\]。由于f每一轮只与上一轮有关，因此可以通过倒序枚举i来省去k这一维。

最后附上python代码：

```python
class Solution(object):
    def waysToReachTarget(self, target, types):
        """
        :type target: int
        :type types: List[List[int]]
        :rtype: int
        """

        f = [0] * (target + 1)
        f[0] = 1
        mod = 10 ** 9 + 7
        for count, mark in types:
            for i in range(target, -1, -1):
                for j in range(1, count + 1):
                    if i >= j * mark:
                        f[i] += f[i - j * mark]
                        if f[i] >= mod:
                            f[i] -= mod
        
        return f[target]
```
