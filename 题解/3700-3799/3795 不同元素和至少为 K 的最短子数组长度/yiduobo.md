---
title: "3795. 不同元素和至少为K的最短子数组长度"
aliases: ["yiduobo的每日leetcode 3795.不同元素和至少为K的最短子数组长度"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1992058763352486963"
zhihu_id: "1992058763352486963"
zhihu_title: "yiduobo的每日leetcode 3795.不同元素和至少为K的最短子数组长度"
question_id: "3795"
question: "不同元素和至少为 K 的最短子数组长度"
problem_url: "https://leetcode.cn/problems/minimum-subarray-length-with-distinct-sum-at-least-k/"
difficulty: "Medium"
rating: 1505
created: "2026-01-07T02:33:51+08:00"
updated: "2026-01-07T02:33:51+08:00"
upvotes: 0
comments: 0
---

# 3795. 不同元素和至少为K的最短子数组长度

> **[yiduobo的每日leetcode 3795.不同元素和至少为K的最短子数组长度](https://zhuanlan.zhihu.com/p/1992058763352486963) · 知乎 · 2026-01-07 · 赞同 0**
> 力扣：[3795. 不同元素和至少为 K 的最短子数组长度](https://leetcode.cn/problems/minimum-subarray-length-with-distinct-sum-at-least-k/) · Medium · 灵茶山艾府：[不定长滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3795.不同元素和至少为K的最短子数组长度

[3795. 不同元素和至少为 K 的最短子数组长度 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-subarray-length-with-distinct-sum-at-least-k/)

题目给出一个由正整数组成的数组nums以及一个整数k，要求从nums中找出一个最短的子数组，这个子数组中不同值之和至少为k。若不存在这样的子数组，则返回-1。

由于nums是由正整数构成的，那么对于一个固定了起点为left的子数组，随着其终点right的向右移动，其中不同元素之和也是逐渐增大的。另一方面，对于某个起点为left的子数组，若其满足条件的最小右边界为right，那么对于左边界为left + 1的子数组，其满足条件的最小右边界必然大于等于right。也就是说，在这里可以使用变长滑动窗口进行求解。

与常规滑动窗口不同的是，本题需要计算窗口中不同元素之和，因此在这里需要使用一个哈希表记录窗口中每种元素出现的次数。当某个元素出现次数从0变成1时，说明其首次出现在窗口中，因此需要将其累加到窗口中不同元素之和当中；同样的，当窗口左边界向右移动时，若原始位于左边界的元素的出现次数从1变成0，说明其不再出现在窗口中，因此需要将其从窗口中不同元素之和中减去。对于其他的情况，则只需要修改出现次数，而不需要修改不同元素之和。

最后附上python代码：

```python
class Solution(object):
    def minLength(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        s = 0
        p = 0
        cnt = {}
        res = -1
        for index in range(len(nums)):
            while p < len(nums) and s < k:
                cnt[nums[p]] = cnt.get(nums[p], 0) + 1
                if cnt[nums[p]] == 1:
                    s += nums[p]
                p += 1
            
            if s < k:
                break
            
            if res == -1 or res > p - index:
                res = p - index
            
            cnt[nums[index]] -= 1
            if cnt[nums[index]] == 0:
                s -= nums[index]
        
        return res
```
