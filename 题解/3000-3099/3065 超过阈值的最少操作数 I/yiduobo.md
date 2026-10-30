---
title: "3065. 超过阈值的最少操作数I"
aliases: ["yiduobo的每日leetcode 3065.超过阈值的最少操作数I"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/696865093"
zhihu_id: "696865093"
zhihu_title: "yiduobo的每日leetcode 3065.超过阈值的最少操作数I"
question_id: "3065"
question: "超过阈值的最少操作数 I"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-exceed-threshold-value-i/"
difficulty: "Easy"
created: "2024-05-09T22:40:45+08:00"
updated: "2024-05-09T22:40:45+08:00"
upvotes: 1
comments: 0
---

# 3065. 超过阈值的最少操作数I

> **[yiduobo的每日leetcode 3065.超过阈值的最少操作数I](https://zhuanlan.zhihu.com/p/696865093) · 知乎 · 2024-05-09 · 赞同 1**
> 力扣：[3065. 超过阈值的最少操作数 I](https://leetcode.cn/problems/minimum-operations-to-exceed-threshold-value-i/) · Easy · 灵茶山艾府：[统计小于 k 的元素个数（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3065.超过阈值的最少操作数I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-exceed-threshold-value-i/description/)

题目中的每次操作只能删去数组中最小的数，而要求计算的是需要多少轮操作才能使得数组中的所有数都大于等于k，那么只需一趟遍历，统计数组中小于k的数的数目即可。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        res = 0
        for v in nums:
            if v < k:
                res += 1
        
        return res
```
