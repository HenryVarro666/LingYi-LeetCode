---
title: "2997. 使数组异或和等于k的最少操作次数"
aliases: ["yiduobo的每日leetcode 2997.使数组异或和等于k的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "题单/位运算", "题单/位运算/二-异或-XOR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/692678269"
zhihu_id: "692678269"
zhihu_title: "yiduobo的每日leetcode 2997.使数组异或和等于k的最少操作次数"
question_id: "2997"
question: "使数组异或和等于 K 的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-operations-to-make-array-xor-equal-to-k/"
difficulty: "Medium"
rating: 1525
created: "2024-04-16T00:55:49+08:00"
updated: "2024-04-24T19:51:04+08:00"
upvotes: 1
comments: 0
---

# 2997. 使数组异或和等于k的最少操作次数

> **[yiduobo的每日leetcode 2997.使数组异或和等于k的最少操作次数](https://zhuanlan.zhihu.com/p/692678269) · 知乎 · 2024-04-16 · 赞同 1**
> 力扣：[2997. 使数组异或和等于 K 的最少操作次数](https://leetcode.cn/problems/minimum-number-of-operations-to-make-array-xor-equal-to-k/) · Medium · 灵茶山艾府：[简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2997.使数组异或和等于k的最少操作次数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-number-of-operations-to-make-array-xor-equal-to-k/description/)

题目中的修改操作可以修改任意数的任意二进制位，实际上就相当于可以通过单次操作修改数组异或和的任意二进制位，于是只需计算数组异或和与k的不同数位数量即为最终答案。更进一步的，这个不同数位的数量实际上就是数组异或和与k再进行异或操作，得到的结果中的二进制位中一的数量。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        for v in nums:
            k ^= v
        
        res = 0
        while k:
            if k & 1:
                res += 1
            k >>= 1
        
        return res
```
