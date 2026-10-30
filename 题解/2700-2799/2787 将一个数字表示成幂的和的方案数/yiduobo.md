---
title: "2787. 将一个数字表示成幂的和的方案数"
aliases: ["yiduobo的每日leetcode 2787.将一个数字表示成幂的和的方案数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/三-背包"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/656578478"
zhihu_id: "656578478"
zhihu_title: "yiduobo的每日leetcode 2787.将一个数字表示成幂的和的方案数"
question_id: "2787"
question: "将一个数字表示成幂的和的方案数"
problem_url: "https://leetcode.cn/problems/ways-to-express-an-integer-as-sum-of-powers/"
difficulty: "Medium"
rating: 1818
created: "2023-09-16T05:28:27+08:00"
updated: "2023-09-16T05:29:39+08:00"
upvotes: 1
comments: 1
---

# 2787. 将一个数字表示成幂的和的方案数

> **[yiduobo的每日leetcode 2787.将一个数字表示成幂的和的方案数](https://zhuanlan.zhihu.com/p/656578478) · 知乎 · 2023-09-16 · 赞同 1**
> 力扣：[2787. 将一个数字表示成幂的和的方案数](https://leetcode.cn/problems/ways-to-express-an-integer-as-sum-of-powers/) · Medium · 灵茶山艾府：[0-1 背包模板题（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2787.将一个数字表示成幂的和的方案数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/ways-to-express-an-integer-as-sum-of-powers/)

由于题目中的n规模不大，因此可以先一趟遍历，计算出所有值的大小不超过n的幂，并将这些值记录在数组中。接下来的问题就是从这些数组中选出一些数来组合成n，是经典的背包问题。

令f[i]表示组成i的方案数，初始状态下f[i] \= 0。接下来，首先遍历所有可用的幂v，接下来从f[n]倒序遍历到f[v]，使用f[i] +\= f[i - v]进行更新。这里倒序遍历的理由是每种幂只能使用一次，在一维的状态表示下，必须倒序遍历防止本轮计算出来的状态值再次更新本轮接下来的状态值。

计算完成后，f[n]即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def numberOfWays(self, n, x):
        """
        :type n: int
        :type x: int
        :rtype: int
        """

        candidate = []
        b = 1
        while True:
            v = b ** x
            if v > n:
                break
            candidate.append(v)
            b += 1
        
        f = [0] * (n + 1)
        f[0] = 1
        mod = 10 ** 9 + 7
        for v in candidate:
            for i in range(n, v - 1, -1):
                f[i] += f[i - v]
                if f[i] >= mod:
                    f[i] -= mod
        
        return f[n]
```
