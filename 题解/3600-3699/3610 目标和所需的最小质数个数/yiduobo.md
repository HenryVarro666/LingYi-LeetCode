---
title: "3610. 目标和所需的最小质数个数"
aliases: ["yiduobo的每日leetcode 3610.目标和所需的最小质数个数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1942984080728752230"
zhihu_id: "1942984080728752230"
zhihu_title: "yiduobo的每日leetcode 3610.目标和所需的最小质数个数"
question_id: "3610"
question: "目标和所需的最小质数个数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-primes-to-sum-to-target/"
created: "2025-08-24T16:22:47+08:00"
updated: "2025-08-24T16:22:47+08:00"
upvotes: 0
comments: 0
---

# 3610. 目标和所需的最小质数个数

> **[yiduobo的每日leetcode 3610.目标和所需的最小质数个数](https://zhuanlan.zhihu.com/p/1942984080728752230) · 知乎 · 2025-08-24 · 赞同 0**
> 力扣：[3610. 目标和所需的最小质数个数](https://leetcode.cn/problems/minimum-number-of-primes-to-sum-to-target/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3610.目标和所需的最小质数个数

[3610. 目标和所需的最小质数个数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-number-of-primes-to-sum-to-target/description/)

题目给出两个整数n和m，现在要求从前m个质数中选择一个多重集合，使得所选质数之和恰好为n，每个质数可以使用多次。问组成n所需的最小质数个数，若不可能，则返回-1。

非常标准的背包问题，令f[index]表示和为index所需的最少质数个数，那么对于前m个质数中的每个质数p，都有f[index] \= min(f[index], f[index - p] + 1)。需要注意的是，这里的每个质数可以使用多次，因此动态规划时应该正序枚举。

于是只需从2开始，往上找出前m个质数，然后利用上面的方法计算f数组即可。

最后附上python代码：

```python
class Solution(object):
    def minNumberOfPrimes(self, n, m):
        """
        :type n: int
        :type m: int
        :rtype: int
        """
        
        prime_list = []
        p = 2

        def check(p):
            x = 2
            while x * x <= p:
                if p % x == 0:
                    return False
                x += 1
            return True

        cnt = 0
        f = [-1] * (n + 1)
        f[0] = 0
        while cnt < m:
            while not check(p):
                p += 1
            cnt += 1

            for index in range(n - p + 1):
                if f[index] != -1 and (f[index + p] == -1 or f[index + p] > f[index] + 1):
                    f[index + p] = f[index] + 1

            p += 1

        
        return f[n]
```
