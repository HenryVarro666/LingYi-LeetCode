---
title: "561. 数组拆分I"
aliases: ["yiduobo的每日leetcode 561.数组拆分I"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/266050537"
zhihu_id: "266050537"
zhihu_title: "yiduobo的每日leetcode 561.数组拆分I"
question_id: "561"
question: "数组拆分I"
problem_url: "https://leetcode.cn/problems/array-partition-i/"
created: "2020-10-15T21:58:16+08:00"
updated: "2020-10-15T21:58:16+08:00"
upvotes: 0
comments: 0
---

# 561. 数组拆分I

> **[yiduobo的每日leetcode 561.数组拆分I](https://zhuanlan.zhihu.com/p/266050537) · 知乎 · 2020-10-15 · 赞同 0**
> 力扣：[561. 数组拆分I](https://leetcode.cn/problems/array-partition-i/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

561.数组拆分I <https://leetcode-cn.com/problems/array-partition-i/>

题目要求两两分组，使每组中较小数之后最大，那么一个自然的想法就是小的跟小的一起，大的跟大的一起，免得小的影响了大的。这个做法是可以得到最优解的，使用反证法可以很快证明处理。

于是现在就可以将所有数从小到大进行排序，按顺序两两进行分组，因此所有偶数项之和就是最后的答案。

最后附上python代码：

```python
class Solution(object):
    def arrayPairSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        nums = sorted(nums)
        res = 0
        for index in range(0, len(nums), 2):
            res += nums[index]
        return res
```
