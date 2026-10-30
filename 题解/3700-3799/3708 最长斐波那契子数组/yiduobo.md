---
title: "3708. 最长斐波那契子数组"
aliases: ["yiduobo的每日leetcode 3708.最长斐波那契子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/enumeration", "leetcode/bao-li", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1960750695553673201"
zhihu_id: "1960750695553673201"
zhihu_title: "yiduobo的每日leetcode 3708.最长斐波那契子数组"
question_id: "3708"
question: "最长斐波那契子数组"
problem_url: "https://leetcode.cn/problems/longest-fibonacci-subarray/"
difficulty: "Medium"
rating: 1381
created: "2025-10-12T17:04:27+08:00"
updated: "2025-10-12T17:04:27+08:00"
upvotes: 1
comments: 0
---

# 3708. 最长斐波那契子数组

> **[yiduobo的每日leetcode 3708.最长斐波那契子数组](https://zhuanlan.zhihu.com/p/1960750695553673201) · 知乎 · 2025-10-12 · 赞同 1**
> 力扣：[3708. 最长斐波那契子数组](https://leetcode.cn/problems/longest-fibonacci-subarray/) · Medium · 灵茶山艾府：[两种方法：暴力枚举 / 一次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3708.最长斐波那契子数组

[3708. 最长斐波那契子数组 - 力扣（LeetCode）](https://leetcode.cn/problems/longest-fibonacci-subarray/description/)

题目给出一个由正整数组成的数组nums。定义斐波那契数组为一个连续的子数组，且从其中第三项开始，每一项都等于前两项之和。

问nums中最长斐波那契子数组的长度。

由于题目要找的是符合条件的最长子数组，那么对于其中的每个元素，如果能加入到当前的子数组中，就应该加入进去，不存在选或者不选的问题。于是只需使用一个变量，从下标2开始向后遍历，若当前元素恰好等于前两个元素之和，说明当前元素可以加入到子数组中，此时应该继续向后扩展；反之，则说明之前子数组无法继续扩展，使用其长度更新答案，然后从停止的位置开始另起一个子数组，重复上面的扩展操作即可。

最后附上python代码：

```python
class Solution(object):
    def longestSubarray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        res = 2
        p = 2
        while p < len(nums):
            q = p
            while q < len(nums) and nums[q] == nums[q - 1] + nums[q - 2]:
                q += 1
            
            res = max(res, q - p + 2)
            if p == q:
                p += 1
            else:
                p = q
        
        return res
```
