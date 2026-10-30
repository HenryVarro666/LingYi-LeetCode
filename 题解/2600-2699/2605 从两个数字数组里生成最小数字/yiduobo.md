---
title: "2605. 从两个数字数组里生成最小数字"
aliases: ["yiduobo的每日leetcode 2605.从两个数字数组里生成最小数字"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/644918515"
zhihu_id: "644918515"
zhihu_title: "yiduobo的每日leetcode 2605.从两个数字数组里生成最小数字"
question_id: "2605"
question: "从两个数字数组里生成最小数字"
problem_url: "https://leetcode.cn/problems/form-smallest-number-from-two-digit-arrays/"
difficulty: "Easy"
created: "2023-07-21T02:47:49+08:00"
updated: "2023-07-21T02:47:49+08:00"
upvotes: 0
comments: 0
---

# 2605. 从两个数字数组里生成最小数字

> **[yiduobo的每日leetcode 2605.从两个数字数组里生成最小数字](https://zhuanlan.zhihu.com/p/644918515) · 知乎 · 2023-07-21 · 赞同 0**
> 力扣：[2605. 从两个数字数组里生成最小数字](https://leetcode.cn/problems/form-smallest-number-from-two-digit-arrays/) · Easy · 灵茶山艾府：[两种做法：哈希表 / 位运算](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2605.从两个数字数组里生成最小数字

[力扣](https://leetcode.cn/problems/form-smallest-number-from-two-digit-arrays/)

首先从1到9遍历所有的1位数，若当前遍历到的数同时出现在两个数组中，那么直接返回这个数即可。

若不存在满足条件的1位数，那么就需要分别取两个数组中的最小值，将其中较小的作为十位数，较大的作为个位数拼接后返回。

最后附上python代码：

```python
class Solution(object):
    def minNumber(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        for v in range(1, 10):
            if v in nums1 and v in nums2:
                return v
        
        mi1 = min(nums1)
        mi2 = min(nums2)
        return min(mi1, mi2) * 10 + max(mi1, mi2)
```
