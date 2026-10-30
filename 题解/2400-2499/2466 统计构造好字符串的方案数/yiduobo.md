---
title: "2466. 统计构造好字符串的方案数"
aliases: ["yiduobo的每日leetcode 2466.统计构造好字符串的方案数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/一-入门-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/587217512"
zhihu_id: "587217512"
zhihu_title: "yiduobo的每日leetcode 2466.统计构造好字符串的方案数"
question_id: "2466"
question: "统计构造好字符串的方案数"
problem_url: "https://leetcode.cn/problems/count-ways-to-build-good-strings/"
difficulty: "Medium"
rating: 1694
created: "2022-11-27T23:00:43+08:00"
updated: "2022-11-27T23:00:43+08:00"
upvotes: 0
comments: 0
---

# 2466. 统计构造好字符串的方案数

> **[yiduobo的每日leetcode 2466.统计构造好字符串的方案数](https://zhuanlan.zhihu.com/p/587217512) · 知乎 · 2022-11-27 · 赞同 0**
> 力扣：[2466. 统计构造好字符串的方案数](https://leetcode.cn/problems/count-ways-to-build-good-strings/) · Medium · 灵茶山艾府：[爬楼梯换皮（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2466.统计构造好字符串的方案数

[力扣](https://leetcode.cn/problems/count-ways-to-build-good-strings/)

非常经典的动态规划问题。令f[i]表示构造长度为i的好字符串的方案数，那么就有f[0] \= 1，表示空串，接下来对于f[i]，先初始化f[i] \= 0，接下来：

1、若i >\= zero，说明可以在这个字符串的尾部放置zero个0，那么就有

f[i] +\= f[i - zero]

2、若i >\= one，说明可以在这个字符串的尾部放置one个1，那么就有

f[i] +\= f[i - one]

由于题目要求的是长度在low到high之间的好字符串数目，那么在计算的过程中顺便统计f[low]到f[high]之间的累加和即可。

最后附上python代码：

```python
class Solution(object):
    def countGoodStrings(self, low, high, zero, one):
        """
        :type low: int
        :type high: int
        :type zero: int
        :type one: int
        :rtype: int
        """

        f = [1]
        res = 0
        mod = 10 ** 9 + 7
        for index in range(1, high + 1):
            f.append(0)
            if index >= zero:
                f[-1] += f[index - zero]
                if f[-1] >= mod:
                    f[-1] -= mod
            if index >= one:
                f[-1] += f[index - one]
                if f[-1] >= mod:
                    f[-1] -= mod
        
            if index >= low:
                res += f[-1]
                if res >= mod:
                    res -= mod
        
        return res
```
