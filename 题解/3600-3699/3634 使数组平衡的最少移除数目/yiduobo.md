---
title: "3634. 使数组平衡的最少移除数目"
aliases: ["yiduobo的每日leetcode 3634.使数组平衡的最少移除数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1946759899217400486"
zhihu_id: "1946759899217400486"
zhihu_title: "yiduobo的每日leetcode 3634.使数组平衡的最少移除数目"
question_id: "3634"
question: "使数组平衡的最少移除数目"
problem_url: "https://leetcode.cn/problems/minimum-removals-to-balance-array/"
difficulty: "Medium"
rating: 1453
created: "2025-09-04T02:31:45+08:00"
updated: "2025-09-04T02:31:45+08:00"
upvotes: 2
comments: 0
---

# 3634. 使数组平衡的最少移除数目

> **[yiduobo的每日leetcode 3634.使数组平衡的最少移除数目](https://zhuanlan.zhihu.com/p/1946759899217400486) · 知乎 · 2025-09-04 · 赞同 2**
> 力扣：[3634. 使数组平衡的最少移除数目](https://leetcode.cn/problems/minimum-removals-to-balance-array/) · Medium · 灵茶山艾府：[排序+滑动窗口（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3634.使数组平衡的最少移除数目

[3634. 使数组平衡的最少移除数目 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-removals-to-balance-array/description/)

给你一个整数数组nums以及一个整数k。

对于一个数组，若其中最大元素的值至多是最小元素的k倍，那么就称该数组是平衡的。现在可以从nums中移除任意数量的元素，但不能将其情况。问最少移除多少个元素，才能使得数组平衡。

首先可以明确的是，一个平衡数组中元素的最小值越大，那么其中可以包含的最大值也越大，也就是说如果按照从小到大的顺序枚举最终答案数组中的最小元素，那么其中的最大元素的大小也是单调递增的。换言之，如果将nums先从小到大进行排序，就可以通过变长滑动窗口来求解这个问题了。

将nums从小到大进行排序，然后一趟遍历枚举左边界，同时使用一个变量p记录当前左边界对应的最靠后的右边界。随着左边界的向后移动，合法的最大右边界也必然是跟着向后移动的，而窗口中的元素即为一个可行的平衡数组，使用原数组的长度减去其中最长的平衡数组的长度即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minRemoval(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        nums.sort()
        p = 0
        res = 0
        for index, v in enumerate(nums):
            while p < len(nums) and nums[p] <= v * k:
                p += 1
            
            res = max(res, p - index)
        
        return len(nums) - res
```
