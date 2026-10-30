---
title: "3667. 按绝对值排序数组"
aliases: ["yiduobo的每日leetcode 3667.按绝对值排序数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1950326280013734595"
zhihu_id: "1950326280013734595"
zhihu_title: "yiduobo的每日leetcode 3667.按绝对值排序数组"
question_id: "3667"
question: "按绝对值排序数组"
problem_url: "https://leetcode.cn/problems/sort-array-by-absolute-value/"
created: "2025-09-18T22:41:12+08:00"
updated: "2025-09-18T22:41:14+08:00"
upvotes: 0
comments: 0
---

# 3667. 按绝对值排序数组

> **[yiduobo的每日leetcode 3667.按绝对值排序数组](https://zhuanlan.zhihu.com/p/1950326280013734595) · 知乎 · 2025-09-18 · 赞同 0**
> 力扣：[3667. 按绝对值排序数组](https://leetcode.cn/problems/sort-array-by-absolute-value/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3667.按绝对值排序数组

[3667. 按绝对值排序数组 - 力扣（LeetCode）](https://leetcode.cn/problems/sort-array-by-absolute-value/description/)

给定一个整数数组nums，将nums中的元素按照它们额绝对值按非递减的顺序排列。

按照题目要求，直接调用sort，并使用lambda表达式来排就行了，比较条件为abs(x)。

最后附上python代码：

```python
class Solution(object):
    def sortByAbsoluteValue(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        return sorted(nums, key=lambda d:abs(d))
```
