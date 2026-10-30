---
title: "698. 划分为k个相等的子集"
aliases: ["yiduobo的每日leetcode 698.划分为k个相等的子集"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/316512991"
zhihu_id: "316512991"
zhihu_title: "yiduobo的每日leetcode 698.划分为k个相等的子集"
question_id: "698"
question: "划分为k个相等的子集"
problem_url: "https://leetcode.cn/problems/partition-to-k-equal-sum-subsets/"
created: "2020-11-27T23:45:44+08:00"
updated: "2020-11-27T23:45:44+08:00"
upvotes: 0
comments: 0
---

# 698. 划分为k个相等的子集

> **[yiduobo的每日leetcode 698.划分为k个相等的子集](https://zhuanlan.zhihu.com/p/316512991) · 知乎 · 2020-11-27 · 赞同 0**
> 力扣：[698. 划分为k个相等的子集](https://leetcode.cn/problems/partition-to-k-equal-sum-subsets/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

698.划分为k个相等的子集

[力扣](https://leetcode-cn.com/problems/partition-to-k-equal-sum-subsets/)

这一题是473题的翻版。

[yiduobo：yiduobo的每日leetcode 473.火柴拼正方形](https://zhuanlan.zhihu.com/p/235648886)

有一个小小的区别是从正方形变成了正k边形，但是具体的做法还是一样。

最后附上python代码：

```python
class Solution(object):
    def canPartitionKSubsets(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: bool
        """

        n = len(nums)
        s = sum(nums)
        if s % k != 0:
            return False
        
        part_s = s / k

        f = [None] * (1 << n)
        f[0] = True

        return self.dfs((1 << n) - 1, f, n, nums, set(range(n)), 0, part_s)

    def dfs(self, now, f, n, nums, candidate, now_s, part_s):
        if f[now] is None:
            f[now] = False
            if now_s == part_s:
                now_s = 0
            for index in list(candidate):
                if now_s + nums[index] <= part_s:
                    candidate.remove(index)
                    if self.dfs(now - (1 << index), f, n, nums, candidate, now_s + nums[index], part_s):
                        return True
                    candidate.add(index)

        return f[now]
```
