---
title: "2541. 使数组中所有元素相等的最小操作数II"
aliases: ["yiduobo的每日leetcode 2541.使数组中所有元素相等的最小操作数II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/637861550"
zhihu_id: "637861550"
zhihu_title: "yiduobo的每日leetcode 2541.使数组中所有元素相等的最小操作数II"
question_id: "2541"
question: "使数组中所有元素相等的最小操作数 II"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-array-equal-ii/"
difficulty: "Medium"
rating: 1620
created: "2023-06-19T22:33:32+08:00"
updated: "2023-06-19T22:33:32+08:00"
upvotes: 0
comments: 0
---

# 2541. 使数组中所有元素相等的最小操作数II

> **[yiduobo的每日leetcode 2541.使数组中所有元素相等的最小操作数II](https://zhuanlan.zhihu.com/p/637861550) · 知乎 · 2023-06-19 · 赞同 0**
> 力扣：[2541. 使数组中所有元素相等的最小操作数 II](https://leetcode.cn/problems/minimum-operations-to-make-array-equal-ii/) · Medium · 灵茶山艾府：[转换+一次遍历](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2541.使数组中所有元素相等的最小操作数II

[力扣](https://leetcode.cn/problems/minimum-operations-to-make-array-equal-ii/)

首先考虑特殊情况。当k \= 0时，数组是无法发生任何变动的，在这种情况下，若一开始num1就和nums2相同，那么答案就为0，否则答案为-1。

接下来是k > 0的情况。由于每次操作nums的变化必须是k的倍数，因此对于任何下标index，都必须满足(nums1[index] - nums2[index]) % k \= 0。另一方面，题目中的操作并不会影响nums1的数组总和，因此必须满足nums1中的数字之和必须等于nums2中的数字之和。若有一个条件不满足，那么答案就是-1，否则就可以通过统计所有大于0的nums1[index] - nums2[index]，计算将这些差变为0所需的操作总数。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums1, nums2, k):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type k: int
        :rtype: int
        """

        if k == 0:
            if nums1 == nums2:
                return 0
            return -1

        n = len(nums1)
        diff = []
        res = 0
        s = 0
        for index in range(n):
            diff = nums1[index] - nums2[index]
            s += diff
            if diff % k != 0:
                return -1
            elif diff > 0:
                res += diff / k
        
        if s == 0:
            return res
        
        return -1
```
