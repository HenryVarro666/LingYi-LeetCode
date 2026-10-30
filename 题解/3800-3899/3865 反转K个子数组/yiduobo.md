---
title: "3865. 反转K个子数组"
aliases: ["yiduobo的每日leetcode 3865.反转K个子数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2017357998964634042"
zhihu_id: "2017357998964634042"
zhihu_title: "yiduobo的每日leetcode 3865.反转K个子数组"
question_id: "3865"
question: "反转K个子数组"
problem_url: "https://leetcode.cn/problems/reverse-k-subarrays/"
created: "2026-03-18T00:13:28+08:00"
updated: "2026-03-18T00:13:28+08:00"
upvotes: 1
comments: 0
---

# 3865. 反转K个子数组

> **[yiduobo的每日leetcode 3865.反转K个子数组](https://zhuanlan.zhihu.com/p/2017357998964634042) · 知乎 · 2026-03-18 · 赞同 1**
> 力扣：[3865. 反转K个子数组](https://leetcode.cn/problems/reverse-k-subarrays/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3865.反转K个子数组

<https://leetcode.cn/problems/reverse-k-subarrays/description/>

题目给出一个长度为n的整数数组nums以及一个整数k，n可以被k整除。

现在要求将其划分为k个长度相等的连续子数组，并反转每个子数组。

由于题目要求划分成连续子数组，那么最终只能从左至右，以长度k将数组分段，也就是说，这些子数组的起点分别为0、k、2k、...，由于长度为k，那么对应的终点就是k - 1、2k - 1、3k - 1、...。

于是可以从左至右，以步长k遍历所有的起点left。对于当前的left，先计算出对应的终点right，接下来left和right相向移动，在这个过程中交换left和right指向的元素，直到left大于等于right为止。

最后附上python代码：

```python
class Solution(object):
    def reverseSubarrays(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        
        n = len(nums)
        length = n // k
        for index in range(0, n, length):
            left, right = index, index + length - 1
            while left < right:
                nums[left], nums[right] = nums[right], nums[left]
                left += 1
                right -= 1
        
        return nums
```
