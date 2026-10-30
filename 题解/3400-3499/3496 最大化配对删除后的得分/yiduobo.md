---
title: "3496. 最大化配对删除后的得分"
aliases: ["yiduobo的每日leetcode 3496.最大化配对删除后的得分"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1899627573568308953"
zhihu_id: "1899627573568308953"
zhihu_title: "yiduobo的每日leetcode 3496.最大化配对删除后的得分"
question_id: "3496"
question: "最大化配对删除后的得分"
problem_url: "https://leetcode.cn/problems/maximize-score-after-pair-deletions/"
created: "2025-04-28T21:24:03+08:00"
updated: "2025-04-28T21:24:03+08:00"
upvotes: 0
comments: 0
---

# 3496. 最大化配对删除后的得分

> **[yiduobo的每日leetcode 3496.最大化配对删除后的得分](https://zhuanlan.zhihu.com/p/1899627573568308953) · 知乎 · 2025-04-28 · 赞同 0**
> 力扣：[3496. 最大化配对删除后的得分](https://leetcode.cn/problems/maximize-score-after-pair-deletions/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3496.最大化配对删除后的得分

[3496. 最大化配对删除后的得分 - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-score-after-pair-deletions/description/)

题目给出一个整数数组nums，当数组中元素超过两个时，需要重复执行以下三个操作之一：

1、删除最前面的两个元素

2、删除最后面的两个元素

3、删除第一个和最后一个元素

对于每次操作，都将删除的元素之和累积到总分上。问可以达成的最高分数是多少。

当nums中有奇数个元素时，无论怎样执行删除操作，最后nums中都只会剩下唯一一个元素。为了使得删除的元素之和最大，就应该让剩下的元素最小。因此对于这种情况，最终答案就是nums中所有元素之和减去nums中的最小值。

与奇数的情况类似，当nums中有偶数个元素时，最后剩下的一定是两个相邻的元素，那么只需一趟遍历，找出和最小的相邻元素对，最终答案就是nums中所有元素之和减去这个和最小的相邻元素对之和。

最后附上python代码：

```python
class Solution(object):
    def maxScore(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        if n % 2 == 1:
            mi = min(nums)
        else:
            mi = nums[0] + nums[1]
            for index in range(2, n):
                mi = min(mi, nums[index - 1] + nums[index])
        
        return sum(nums) - mi
```
