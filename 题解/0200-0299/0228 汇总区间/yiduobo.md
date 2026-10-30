---
title: "228. 汇总区间"
aliases: ["yiduobo的每日leetcode 228.汇总区间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/149535333"
zhihu_id: "149535333"
zhihu_title: "yiduobo的每日leetcode 228.汇总区间"
question_id: "228"
question: "汇总区间"
problem_url: "https://leetcode.cn/problems/summary-ranges/"
created: "2020-06-19T21:47:40+08:00"
updated: "2020-06-19T21:47:40+08:00"
upvotes: 0
comments: 0
---

# 228. 汇总区间

> **[yiduobo的每日leetcode 228.汇总区间](https://zhuanlan.zhihu.com/p/149535333) · 知乎 · 2020-06-19 · 赞同 0**
> 力扣：[228. 汇总区间](https://leetcode.cn/problems/summary-ranges/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

228.汇总区间<https://leetcode-cn.com/problems/summary-ranges/>

比较基础的题目。

从左往右一趟扫描，若当前的数字等于上一个数字，那么将区间的右边界加一，否则输出当前区间即可。

需要注意只有一个数的区间。

最后附上python代码：

```python
class Solution(object):
    def summaryRanges(self, nums):
        """
        :type nums: List[int]
        :rtype: List[str]
        """

        if not nums:
            return []

        left = now = nums[0]
        res = []
        for num in nums[1:]:
            if num == now + 1:
                now += 1
            else:
                if now == left:
                    res.append(str(left))
                else:
                    res.append("%d->%d" % (left, now))
                now = left = num

        if now == left:
            return res + [str(left)]
        else:
            return res + ["%d->%d" % (left, now)]
```
