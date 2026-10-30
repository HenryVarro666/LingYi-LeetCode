---
title: "3512. 使数组和能被K整除的最少操作次数"
aliases: ["yiduobo的每日leetcode 3512.使数组和能被K整除的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1902520450350838864"
zhihu_id: "1902520450350838864"
zhihu_title: "yiduobo的每日leetcode 3512.使数组和能被K整除的最少操作次数"
question_id: "3512"
question: "使数组和能被 K 整除的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-array-sum-divisible-by-k/"
difficulty: "Easy"
created: "2025-05-06T00:03:30+08:00"
updated: "2025-05-06T00:03:30+08:00"
upvotes: 0
comments: 0
---

# 3512. 使数组和能被K整除的最少操作次数

> **[yiduobo的每日leetcode 3512.使数组和能被K整除的最少操作次数](https://zhuanlan.zhihu.com/p/1902520450350838864) · 知乎 · 2025-05-06 · 赞同 0**
> 力扣：[3512. 使数组和能被 K 整除的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-make-array-sum-divisible-by-k/) · Easy · 灵茶山艾府：[求和模 k（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3512.使数组和能被K整除的最少操作次数

[3512. 使数组和能被 K 整除的最少操作次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-make-array-sum-divisible-by-k/description/)

题目给出一个整数数组nums以及一个整数k。现在可以对nums执行以下操作任意次。每次操作，可以将其中任意元素nums[index]替换为nums[index] - 1。

问最少需要多少次操作才能使得nums元素之和可以被k整除。

每次操作都可以使得nums的元素之和对k的余数减少1，于是可以直接计算nums元素之和，对k取模即为需要的操作次数。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        return sum(nums) % k
```
