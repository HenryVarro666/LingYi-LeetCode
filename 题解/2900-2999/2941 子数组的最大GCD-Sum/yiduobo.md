---
title: "2941. 子数组的最大GCD-Sum"
aliases: ["yiduobo的每日leetcode 2941.子数组的最大GCD-Sum"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/691194067"
zhihu_id: "691194067"
zhihu_title: "yiduobo的每日leetcode 2941.子数组的最大GCD-Sum"
question_id: "2941"
question: "子数组的最大GCD-Sum"
problem_url: "https://leetcode.cn/problems/maximum-gcd-sum-of-a-subarray/"
created: "2024-04-08T01:05:09+08:00"
updated: "2024-04-08T01:05:09+08:00"
upvotes: 1
comments: 0
---

# 2941. 子数组的最大GCD-Sum

> **[yiduobo的每日leetcode 2941.子数组的最大GCD-Sum](https://zhuanlan.zhihu.com/p/691194067) · 知乎 · 2024-04-08 · 赞同 1**
> 力扣：[2941. 子数组的最大GCD-Sum](https://leetcode.cn/problems/maximum-gcd-sum-of-a-subarray/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2941.子数组的最大GCD-Sum

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-gcd-sum-of-a-subarray/)

没有想到太好的做法，不过注意到随着数组长度的扩展，gcd衰减的速度是很快的，因此在这里应该可以直接使用暴力的动态规划。

令f[i][g]表示以nums[i]结尾的子数组，子数组的最大公约数为g时，可以得到的最大子数组和以及最长子数组长度，那么对于f[i]，可以枚举f[i - 1]中的所有g，计算nums[i]与g的最大公约数new_g，然后使用new_g来更新f[i]。对于得到的f[i]，若其中的f[i][new_g]的长度达标，那么就用new_g乘以f[i][new_g]的数组和来更新答案。

由于题目最终要求的是长度达标的子数组和与gcd相乘最大，因此在这里对于gcd相同的情况而言，由于限定了子数组右边界为nums[i]，那么数组的和越大就意味着数组越长，也就是说这样既保证了数组长度能尽量达标，又能让数组和尽量大从而使得答案尽量大。

另外需要特别注意的是，当k等于1时，单独取nums[i]作为子数组长度也是达标的，因此需要对这种情况进行特殊处理。

最后附上python代码：

```python
class Solution(object):
    def maxGcdSum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        if k == 1:
            res = nums[0] * nums[0]
        else:
            res = 0

        f = {nums[0]: [nums[0], 1]}

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        for v in nums[1:]:
            tmp = {v : [v, 1]}
            for g in f:
                new_g = gcd(g, v)
                if new_g not in tmp or tmp[new_g][0] < f[g][0] + v:
                    tmp[new_g] = [f[g][0] + v, f[g][1] + 1]
            
            f = tmp
            for new_g in f:
                if f[new_g][1] >= k:
                    res = max(res, f[new_g][0] * new_g)
        
        return res
```
