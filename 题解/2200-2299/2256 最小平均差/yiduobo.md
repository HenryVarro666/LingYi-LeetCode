---
title: "2256. 最小平均差"
aliases: ["yiduobo的每日leetcode 2256.最小平均差"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/prefix-sum", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/547396411"
zhihu_id: "547396411"
zhihu_title: "yiduobo的每日leetcode 2256.最小平均差"
question_id: "2256"
question: "最小平均差"
problem_url: "https://leetcode.cn/problems/minimum-average-difference/"
difficulty: "Medium"
rating: 1395
created: "2022-07-28T23:56:28+08:00"
updated: "2022-07-28T23:56:28+08:00"
upvotes: 0
comments: 0
---

# 2256. 最小平均差

> **[yiduobo的每日leetcode 2256.最小平均差](https://zhuanlan.zhihu.com/p/547396411) · 知乎 · 2022-07-28 · 赞同 0**
> 力扣：[2256. 最小平均差](https://leetcode.cn/problems/minimum-average-difference/) · Medium · 灵茶山艾府：[前后缀分解](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2256.最小平均差

[力扣](https://leetcode.cn/problems/minimum-average-difference/)

题目要求找出一个下标index，使得nums[0]到nums[index]的平均值与nums[index + 1]到nums[n - 1]的平均值之差最小。

题目需要求解平均值，为了求解平均值就需要直到区间和以及区间长度。在这里区间长度是很好求的，0到index的长度就是index + 1，剩下的部分自然是n - index - 1。而对于区间和的求解，本质上就一个前缀和与一个后缀和，更进一步的，这个后缀和可以通过数组总和减去前缀和得到，因此实际上需要求解的只有一个前缀和。

于是可以先计算出数组的总和s，然后从头开始向后遍历分割的下标index，同时使用一个变量now维护当前的前缀和。每遍历到一个index，首先将nums[index]加入到now中更新前缀和，那么此时左半边的平均值就是now / (index + 1)，右半边的则是(s - now) / (n - index - 1)，使用这两个数差的绝对值来更新答案，然后继续向后处理下一个index即可。

需要特别注意的是，当遍历到index \= n - 1时，右半边的长度为0，此时不能再通过除法计算右半边的平均值，而应该直接置为0。

最后附上python代码：

```python
class Solution(object):
    def minimumAverageDifference(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        s = sum(nums)
        n = len(nums)

        min_diff = None
        res = None
        now = 0
        for index, num in enumerate(nums):
            now += num
            if index == n - 1:
                diff = s / n
            else:
                diff = abs(now / (index + 1) - (s - now) / (n - index - 1))
            if min_diff is None or min_diff > diff:
                min_diff = diff
                res = index
        
        return res
```
