---
title: "3105. 最长的严格递增或递减子数组"
aliases: ["yiduobo的每日leetcode 3105.最长的严格递增或递减子数组"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/700186579"
zhihu_id: "700186579"
zhihu_title: "yiduobo的每日leetcode 3105.最长的严格递增或递减子数组"
question_id: "3105"
question: "最长的严格递增或递减子数组"
problem_url: "https://leetcode.cn/problems/longest-strictly-increasing-or-strictly-decreasing-subarray/"
difficulty: "Easy"
created: "2024-05-28T01:01:08+08:00"
updated: "2024-05-28T01:01:08+08:00"
upvotes: 1
comments: 0
---

# 3105. 最长的严格递增或递减子数组

> **[yiduobo的每日leetcode 3105.最长的严格递增或递减子数组](https://zhuanlan.zhihu.com/p/700186579) · 知乎 · 2024-05-28 · 赞同 1**
> 力扣：[3105. 最长的严格递增或递减子数组](https://leetcode.cn/problems/longest-strictly-increasing-or-strictly-decreasing-subarray/) · Easy · 灵茶山艾府：[O(n) 分组循环，附题单（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3105.最长的严格递增或递减子数组

[. - 力扣（LeetCode）](https://leetcode.cn/problems/longest-strictly-increasing-or-strictly-decreasing-subarray/description/)

先使用两个指针进行一趟遍历，找出nums中所有的递增子数组，接下来再使用两个指针进行一趟遍历，找出nums中所有的递减子数组，最后取其中最长的长度作为答案即可。

最后附上python代码：

```python
class Solution(object):
    def longestMonotonicSubarray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        p = 0
        while p < len(nums):
            q = p + 1
            while q < len(nums) and nums[q] > nums[q - 1]:
                q += 1
            res = max(res, q - p)
            p = q
        
        p = 0
        while p < len(nums):
            q = p + 1
            while q < len(nums) and nums[q] < nums[q - 1]:
                q += 1
            res = max(res, q - p)
            p = q
        
        return res
```
