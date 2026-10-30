---
title: "376. 摆动序列"
aliases: ["yiduobo的每日leetcode 376.摆动序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/166036835"
zhihu_id: "166036835"
zhihu_title: "yiduobo的每日leetcode 376.摆动序列"
question_id: "376"
question: "摆动序列"
problem_url: "https://leetcode.cn/problems/wiggle-subsequence/"
created: "2020-08-02T00:10:07+08:00"
updated: "2020-08-02T00:10:07+08:00"
upvotes: 0
comments: 0
---

# 376. 摆动序列

> **[yiduobo的每日leetcode 376.摆动序列](https://zhuanlan.zhihu.com/p/166036835) · 知乎 · 2020-08-02 · 赞同 0**
> 力扣：[376. 摆动序列](https://leetcode.cn/problems/wiggle-subsequence/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

376.摆动序列<https://leetcode-cn.com/problems/wiggle-subsequence/>

我在这里采用的是贪心法。

首先，对于连续的相同数字，最多也只可能选取其中的一个，而选择哪一个是没有区别的，因此首先可以对连续的相邻数字做去重操作。

接下来，可以发现剩下的数字一定是构成上下起伏的折线形式，那么对于一个单调上升或单调下降的区间，除去起点之外，剩下的数只能选择一个。对于单调上升区间，应该选择最大的那一个数，而对于单调下降区间，则应该选择最小的那一个数，原因是之后的区间必须满足单调性相反，那么在当前区间中选择最大或者最小的数有助于后续形成更多有效的区间。可以发现，选择的点正好对应到折线的各个拐点，于是我们只需要统计拐点的数目，再加上最初的起点即可。

最后附上python代码：

```python
class Solution(object):
    def wiggleMaxLength(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        if len(nums) < 2:
            return len(nums)

        diff = 0
        res = 1
        
        for index in range(1, len(nums)):
            now_diff = nums[index] - nums[index - 1]
            if now_diff == 0:
                continue
            if diff == 0:
                diff = now_diff
                res += 1
            elif diff > 0 and now_diff < 0:
                res += 1
                diff = now_diff
            elif diff < 0 and now_diff > 0:
                res += 1
                diff = now_diff
        
        return res
```
