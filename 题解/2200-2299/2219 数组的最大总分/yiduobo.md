---
title: "2219. 数组的最大总分"
aliases: ["yiduobo的每日leetcode 2219.数组的最大总分"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/628132521"
zhihu_id: "628132521"
zhihu_title: "yiduobo的每日leetcode 2219.数组的最大总分"
question_id: "2219"
question: "数组的最大总分"
problem_url: "https://leetcode.cn/problems/maximum-sum-score-of-array/"
created: "2023-05-09T22:33:37+08:00"
updated: "2023-05-09T22:33:37+08:00"
upvotes: 0
comments: 0
---

# 2219. 数组的最大总分

> **[yiduobo的每日leetcode 2219.数组的最大总分](https://zhuanlan.zhihu.com/p/628132521) · 知乎 · 2023-05-09 · 赞同 0**
> 力扣：[2219. 数组的最大总分](https://leetcode.cn/problems/maximum-sum-score-of-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2219.数组的最大总分

[力扣](https://leetcode.cn/problems/maximum-sum-score-of-array/)

题目中每个位置的对应得分是以这个位置为终点的前缀和以及以这个位置为起点的后缀和中较大的那个，另一方面，这个前缀和与后缀和相加恰好就是数组总和再加上当前位置上的数，因此对于本题，可以先求出数组总和，接下来一趟遍历，一边计算前缀和一边通过前缀和以及总和减去前缀和得到的后缀和来更新最终答案。

最后附上python代码：

```python
class Solution(object):
    def maximumSumScore(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        s = sum(nums)
        res = max(nums[0], s)
        
        now = nums[0]
        for v in nums[1:]:
            res = max(res, now + v, s - now)
            now += v
        
        return res
```
