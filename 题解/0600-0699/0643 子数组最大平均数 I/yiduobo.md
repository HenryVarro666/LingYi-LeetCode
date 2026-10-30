---
title: "643. 子数组最大平均数I"
aliases: ["yiduobo的每日leetcode 643.子数组最大平均数I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/273733683"
zhihu_id: "273733683"
zhihu_title: "yiduobo的每日leetcode 643.子数组最大平均数I"
question_id: "643"
question: "子数组最大平均数 I"
problem_url: "https://leetcode.cn/problems/maximum-average-subarray-i/"
difficulty: "Easy"
created: "2020-11-04T22:36:43+08:00"
updated: "2020-11-04T22:36:43+08:00"
upvotes: 0
comments: 0
---

# 643. 子数组最大平均数I

> **[yiduobo的每日leetcode 643.子数组最大平均数I](https://zhuanlan.zhihu.com/p/273733683) · 知乎 · 2020-11-04 · 赞同 0**
> 力扣：[643. 子数组最大平均数 I](https://leetcode.cn/problems/maximum-average-subarray-i/) · Easy · 灵茶山艾府：[【模板】定长滑动窗口（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

643.子数组最大平均数I

[力扣](https://leetcode-cn.com/problems/maximum-average-subarray-i/)

注意到题目要找到是长度为k的连续子数组，因此可以用滑动窗口来处理。

维护一个长度为k的滑动窗口，逐步往右滑动。每次将nums[index]加入到滑动窗口中，同时将nums[index - k]从中移除，那么此时滑动窗口中数字之和就要加上nums[index]然后减去nums[index - k]。记录滑动过程中窗口最大的和，然后除以k就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def findMaxAverage(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: float
        """

        now = 0
        for index in range(k):
            now += nums[index]
        
        res = now
        for index in range(k, len(nums)):
            now += nums[index] - nums[index - k]
            res = max(now, res)

        return res * 1.0 / k
```
