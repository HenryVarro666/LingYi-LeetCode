---
title: "3364. 最小正和子数组"
aliases: ["yiduobo的每日leetcode 3364.最小正和子数组"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/enumeration", "leetcode/ordered-set", "leetcode/prefix-sum", "leetcode/sliding-window", "leetcode/bao-li", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/27738461594"
zhihu_id: "27738461594"
zhihu_title: "yiduobo的每日leetcode 3364.最小正和子数组"
question_id: "3364"
question: "最小正和子数组"
problem_url: "https://leetcode.cn/problems/minimum-positive-sum-subarray/"
difficulty: "Easy"
created: "2025-03-04T00:15:23+08:00"
updated: "2025-03-04T00:15:23+08:00"
upvotes: 1
comments: 0
---

# 3364. 最小正和子数组

> **[yiduobo的每日leetcode 3364.最小正和子数组](https://zhuanlan.zhihu.com/p/27738461594) · 知乎 · 2025-03-04 · 赞同 1**
> 力扣：[3364. 最小正和子数组](https://leetcode.cn/problems/minimum-positive-sum-subarray/) · Easy · 灵茶山艾府：[两种方法：暴力枚举 / 前缀和+定长滑窗+有序集合（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3364.最小正和子数组

[3364. 最小正和子数组 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-positive-sum-subarray/description/)

题目给出一个整数数组nums以及两个整数l和r，要求找出其中长度在l到r之间，且数组和大于0的最小子数组和。若不存在合法的子数组，则返回-1。

本题的数据规模比较小，因此可以直接暴力枚举子数组的起点和终点并计算子数组和。若子数组长度达标，就用子数组和更新答案。

最后附上python代码：

```python
class Solution(object):
    def minimumSumSubarray(self, nums, l, r):
        """
        :type nums: List[int]
        :type l: int
        :type r: int
        :rtype: int
        """
        
        n = len(nums)
        res = -1
        for start in range(n):
            s = 0
            length = 0
            for end in range(start, n):
                s += nums[end]
                length += 1

                if l <= length <= r and s > 0:
                    if res == -1 or res > s:
                        res = s
        
        return res
```
