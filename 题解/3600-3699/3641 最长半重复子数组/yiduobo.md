---
title: "3641. 最长半重复子数组"
aliases: ["yiduobo的每日leetcode 3641.最长半重复子数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1947685538560714281"
zhihu_id: "1947685538560714281"
zhihu_title: "yiduobo的每日leetcode 3641.最长半重复子数组"
question_id: "3641"
question: "最长半重复子数组"
problem_url: "https://leetcode.cn/problems/longest-semi-repeating-subarray/"
created: "2025-09-06T15:51:00+08:00"
updated: "2025-09-06T15:51:00+08:00"
upvotes: 1
comments: 0
---

# 3641. 最长半重复子数组

> **[yiduobo的每日leetcode 3641.最长半重复子数组](https://zhuanlan.zhihu.com/p/1947685538560714281) · 知乎 · 2025-09-06 · 赞同 1**
> 力扣：[3641. 最长半重复子数组](https://leetcode.cn/problems/longest-semi-repeating-subarray/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3641.最长半重复子数组

[3641. 最长半重复子数组 - 力扣（LeetCode）](https://leetcode.cn/problems/longest-semi-repeating-subarray/description/)

题目给出一个长度为n的整数数组以及一个整数k，另外定义半重复子数组为最多有k个元素重复的连续子数组。问nums中最长半重复子数组的长度。

对于数组中的某个下标index，若以index为左边界的最长半重复子数组的右边界为r，那么对于以index + 1为左边界的最长半重复子数组而言，且右边界必然是大于等于r的。基于这一点，本题就可以通过变长滑动窗口来进行求解。

为了记录窗口内重复元素的数目，需要使用一个哈希表cnt记录其中每种元素出现的次数，同时还需要一个变量dup记录其中重复元素的数量。

接下来一趟遍历，枚举所有子数组的左边界index，对于当前的index，需要在上一轮的基础上确定当前窗口的最大右边界。若当前窗口右侧的下一个位置p，那么窗口扩展后nums[p]出现的次数就应该加上1。若此时窗口内nums[p]的出现次数恰好为一次，那么在加入nums[p]后，nums[p]将变为重复，此时应该将dup加上1，因此只有当nums[p]在窗口内出现的次数不为一次，或者dup小于k时，才能将窗口右边界移动到p。不断将窗口右边界向右移动，直到不满足条件为止，此时的p - 1就是index对应的最长半重复子数组的右边界，使用p - index更新答案即可。接下来，还需要将窗口左边界向右移动，也就是将nums[index]移出窗口。此时应该将nums[index]在窗口内出现的次数减去1，若本次减少操作后nums[index]在窗口内的出现次数从两次变为一次，说明nums[index]不再重复，此时则需要将dup减去1。

最后附上python代码：

```python
class Solution(object):
    def longestSubarray(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        cnt = {}
        p = 0
        dup = 0
        res = 0
        for index, v in enumerate(nums):
            while p < len(nums):
                x = nums[p]
                if cnt.get(x, 0) == 1 and dup == k:
                    break
                cnt[x] = cnt.get(x, 0) + 1
                if cnt[x] == 2:
                    dup += 1
                p += 1
            
            res = max(res, p - index)
            cnt[v] -= 1
            if cnt[v] == 1:
                dup -= 1
        
        return res
```
