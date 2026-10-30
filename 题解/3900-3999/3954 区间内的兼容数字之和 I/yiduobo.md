---
title: "3954. 区间内的兼容数字之和I"
aliases: ["yiduobo的每日leetcode 3954.区间内的兼容数字之和I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2047818137182136235"
zhihu_id: "2047818137182136235"
zhihu_title: "yiduobo的每日leetcode 3954.区间内的兼容数字之和I"
question_id: "3954"
question: "区间内的兼容数字之和 I"
problem_url: "https://leetcode.cn/problems/sum-of-compatible-numbers-in-range-i/"
difficulty: "Easy"
created: "2026-06-09T23:14:15+08:00"
updated: "2026-06-09T23:14:15+08:00"
upvotes: 2
comments: 0
---

# 3954. 区间内的兼容数字之和I

> **[yiduobo的每日leetcode 3954.区间内的兼容数字之和I](https://zhuanlan.zhihu.com/p/2047818137182136235) · 知乎 · 2026-06-09 · 赞同 2**
> 力扣：[3954. 区间内的兼容数字之和 I](https://leetcode.cn/problems/sum-of-compatible-numbers-in-range-i/) · Easy · 灵茶山艾府：[三种方法：暴力枚举 / 数位 DP / 贡献法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3954.区间内的兼容数字之和

<https://leetcode.cn/problems/sum-of-compatible-numbers-in-range-i/description/>

题目给出两个整数n和k，大小都在1到100之间。

若某个正整数x满足：

- abs(n - x) \<\= k
- n & x \=\= 0

那么就称x为兼容整数。

问所有兼容整数之和是多少。

由于题目的数据规模较小，在这里可以直接从max(1, n - k)到n + k枚举所有可能的x，若当前的x与n按位与结果为0，就将x累加到答案中。

最后附上python代码：

```python
class Solution(object):
    def sumOfGoodIntegers(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """
        
        res = 0
        for x in range(max(n - k, 1), n + k + 1):
            if (n & x) == 0:
                res += x

        return res
```
