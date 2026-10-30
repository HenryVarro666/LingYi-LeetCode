---
title: "2614. 对角线上的质数"
aliases: ["yiduobo的每日leetcode 2614.对角线上的质数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/645927270"
zhihu_id: "645927270"
zhihu_title: "yiduobo的每日leetcode 2614.对角线上的质数"
question_id: "2614"
question: "对角线上的质数"
problem_url: "https://leetcode.cn/problems/prime-in-diagonal/"
difficulty: "Easy"
rating: 1375
created: "2023-07-26T00:33:05+08:00"
updated: "2023-07-26T00:33:05+08:00"
upvotes: 0
comments: 0
---

# 2614. 对角线上的质数

> **[yiduobo的每日leetcode 2614.对角线上的质数](https://zhuanlan.zhihu.com/p/645927270) · 知乎 · 2023-07-26 · 赞同 0**
> 力扣：[2614. 对角线上的质数](https://leetcode.cn/problems/prime-in-diagonal/) · Easy · 灵茶山艾府：[判断质数（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2614.对角线上的质数

[力扣](https://leetcode.cn/problems/prime-in-diagonal/)

题目描述中已经指明了每一行位于对角线上的数是哪两个，于是只需遍历每行，检测当前行位于对角线上的数是否为质数，如果是，则更新答案。

至于检测质数的方法，由于最多只有2n个数需要检测，因此既可以先提前使用筛法找出范围内的所有质数，也可以直接暴力求解。

最后附上python代码：

```python
class Solution(object):
    def diagonalPrime(self, nums):
        """
        :type nums: List[List[int]]
        :rtype: int
        """

        def check(x):
            if x == 1:
                return False
            p = 2
            while p * p <= x:
                if x % p == 0:
                    return False
                p += 1
            
            return True

        n = len(nums)
        res = 0
        for i in range(n):
            if nums[i][i] > res and check(nums[i][i]):
                res = nums[i][i]
            if nums[i][n - i - 1] > res and check(nums[i][n - i - 1]):
                res = nums[i][n - i - 1]
        
        return res
```
