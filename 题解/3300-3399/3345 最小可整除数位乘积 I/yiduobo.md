---
title: "3345. 最小可整除数位乘积I"
aliases: ["yiduobo的每日leetcode 3345.最小可整除数位乘积I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/enumeration", "leetcode/bao-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/25845155432"
zhihu_id: "25845155432"
zhihu_title: "yiduobo的每日leetcode 3345.最小可整除数位乘积I"
question_id: "3345"
question: "最小可整除数位乘积 I"
problem_url: "https://leetcode.cn/problems/smallest-divisible-digit-product-i/"
difficulty: "Easy"
created: "2025-02-23T22:34:28+08:00"
updated: "2025-02-23T22:34:28+08:00"
upvotes: 1
comments: 0
---

# 3345. 最小可整除数位乘积I

> **[yiduobo的每日leetcode 3345.最小可整除数位乘积I](https://zhuanlan.zhihu.com/p/25845155432) · 知乎 · 2025-02-23 · 赞同 1**
> 力扣：[3345. 最小可整除数位乘积 I](https://leetcode.cn/problems/smallest-divisible-digit-product-i/) · Easy · 灵茶山艾府：[暴力枚举，至多循环 10 次（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3345.最小可整除数位乘积I

[3345. 最小可整除数位乘积 I - 力扣（LeetCode）](https://leetcode.cn/problems/smallest-divisible-digit-product-i/description/)

题目给出两个整数n和t，要求找出大于等于的n的最小整数，且这个整数的各数位之积能被t整除。

由于n和t的数据规模都很小，只需从n开始向上枚举答案，拆分数位相乘后检测是否能被t整除即可。

最后附上python代码：

```python
class Solution(object):
    def smallestNumber(self, n, t):
        """
        :type n: int
        :type t: int
        :rtype: int
        """
        
        def check(n):
            m = 1
            while n:
                m *= n % 10
                n //= 10
            return m % t == 0

        while not check(n):
            n += 1
        
        return n
```
