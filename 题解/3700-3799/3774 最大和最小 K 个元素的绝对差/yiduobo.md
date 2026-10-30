---
title: "3774. 最大和最小K个元素的绝对差"
aliases: ["yiduobo的每日leetcode 3774.最大和最小K个元素的绝对差"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/quickselect", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1984012886054547572"
zhihu_id: "1984012886054547572"
zhihu_title: "yiduobo的每日leetcode 3774.最大和最小K个元素的绝对差"
question_id: "3774"
question: "最大和最小 K 个元素的绝对差"
problem_url: "https://leetcode.cn/problems/absolute-difference-between-maximum-and-minimum-k-elements/"
difficulty: "Easy"
created: "2025-12-15T21:35:55+08:00"
updated: "2025-12-15T21:35:55+08:00"
upvotes: 1
comments: 0
---

# 3774. 最大和最小K个元素的绝对差

> **[yiduobo的每日leetcode 3774.最大和最小K个元素的绝对差](https://zhuanlan.zhihu.com/p/1984012886054547572) · 知乎 · 2025-12-15 · 赞同 1**
> 力扣：[3774. 最大和最小 K 个元素的绝对差](https://leetcode.cn/problems/absolute-difference-between-maximum-and-minimum-k-elements/) · Easy · 灵茶山艾府：[排序 / 快速选择（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3774.最大和最小K个元素的绝对差

[3774. 最大和最小 K 个元素的绝对差 - 力扣（LeetCode）](https://leetcode.cn/problems/absolute-difference-between-maximum-and-minimum-k-elements/description/)

题目给出一个整数数组nums以及一个整数k。

要求计算nums中k个最大元素之和，与k个最小元素之和的差值。

将nums按从小到大的顺序排序，然后使用后k个元素之和减去前k个元素之和即可。

最后附上python代码：

```python
class Solution(object):
    def absDifference(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        nums.sort()
        return sum(nums[-k:]) - sum(nums[:k])
```
