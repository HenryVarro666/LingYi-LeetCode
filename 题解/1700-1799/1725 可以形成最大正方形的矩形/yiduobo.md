---
title: "1725. 可以形成最大正方形的矩形"
aliases: ["yiduobo的每日leetcode 1725.可以形成最大正方形的矩形"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/451868834"
zhihu_id: "451868834"
zhihu_title: "yiduobo的每日leetcode 1725.可以形成最大正方形的矩形"
question_id: "1725"
question: "可以形成最大正方形的矩形"
problem_url: "https://leetcode.cn/problems/number-of-rectangles-that-can-form-the-largest-square/"
created: "2021-12-30T23:40:42+08:00"
updated: "2021-12-30T23:40:42+08:00"
upvotes: 0
comments: 0
---

# 1725. 可以形成最大正方形的矩形

> **[yiduobo的每日leetcode 1725.可以形成最大正方形的矩形](https://zhuanlan.zhihu.com/p/451868834) · 知乎 · 2021-12-30 · 赞同 0**
> 力扣：[1725. 可以形成最大正方形的矩形](https://leetcode.cn/problems/number-of-rectangles-that-can-form-the-largest-square/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1725.可以形成最大正方形的矩形

[力扣](https://leetcode-cn.com/problems/number-of-rectangles-that-can-form-the-largest-square/)

对于一个矩形而言，可以切割出来的最大正方形边长就是min(l, w)，那么可以一趟扫描遍历所有的矩形，计算出每个矩形能切割的最大正方形边长，然后找出其中的最大值并统计出现次数。

最后附上python代码：

```python
class Solution(object):
    def countGoodRectangles(self, rectangles):
        """
        :type rectangles: List[List[int]]
        :rtype: int
        """

        m = 0
        res = 0
        for l, w in rectangles:
            max_l = min(l, w)
            if m == max_l:
                res += 1
            elif m < max_l:
                m = max_l
                res = 1

        return res
```
