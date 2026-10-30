---
title: "2765. 最长交替子序列"
aliases: ["yiduobo的每日leetcode 2765.最长交替子序列"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/654981305"
zhihu_id: "654981305"
zhihu_title: "yiduobo的每日leetcode 2765.最长交替子序列"
question_id: "2765"
question: "最长交替子数组"
problem_url: "https://leetcode.cn/problems/longest-alternating-subarray/"
difficulty: "Easy"
rating: 1581
created: "2023-09-08T04:07:45+08:00"
updated: "2023-09-08T04:07:45+08:00"
upvotes: 0
comments: 0
---

# 2765. 最长交替子序列

> **[yiduobo的每日leetcode 2765.最长交替子序列](https://zhuanlan.zhihu.com/p/654981305) · 知乎 · 2023-09-08 · 赞同 0**
> 力扣：[2765. 最长交替子数组](https://leetcode.cn/problems/longest-alternating-subarray/) · Easy · 灵茶山艾府：[教你一次性把代码写对！O(n) 分组循环（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2765.最长交替子序列

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/longest-alternating-subarray/)

题目的数据规模很小，直接暴力枚举然后检测是完全可行的。我在这里采用的做法是枚举左边界，然后找出最大的符合条件的右边界。

左边界left初始情况下等于0，接下来每一轮，先检测nums[left + 1]是否等于nums[left] + 1。

若不满足，那么就不存在以left为左边界的子序列，此时应该将left加上1。

反之若满足，就让right从left + 2开始向后扩展直到right来到数组边界或者nums[right]不等于nums[right - 2]为止，此时left到right - 1之间这一段就是一个合法的子序列，使用其长度right - left更新答案，然后在这里就可以直接将left跳转到right - 1。

这里跳转到right - 1的理由是以left + 1到right - 2之间的所有数为左边界的合法子序列，其右边界都是right - 1，因此没有必要再进行计算了，而对于right - 1自身，其可能与right和后面的数组成合法子序列，因此left应该跳转到right - 1而不是right。

最后附上python代码：

```python
class Solution(object):
    def alternatingSubarray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        left = 0
        res = -1
        while left < len(nums):
            if left + 1 < len(nums) and nums[left + 1] == nums[left] + 1:
                right = left + 2
                while right < len(nums) and nums[right] == nums[right - 2]:
                    right += 1
                
                res = max(res, right - left)
                left = right - 1
            else:
                left += 1
        
        return res
```
