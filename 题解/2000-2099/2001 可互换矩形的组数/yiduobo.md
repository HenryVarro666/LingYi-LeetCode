---
title: "2001. 可互换矩形的组数"
aliases: ["yiduobo的每日leetcode 2001.可互换矩形的组数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/math", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/502139915"
zhihu_id: "502139915"
zhihu_title: "yiduobo的每日leetcode 2001.可互换矩形的组数"
question_id: "2001"
question: "可互换矩形的组数"
problem_url: "https://leetcode.cn/problems/number-of-pairs-of-interchangeable-rectangles/"
difficulty: "Medium"
rating: 1436
created: "2022-04-21T00:25:26+08:00"
updated: "2022-04-21T00:25:26+08:00"
upvotes: 0
comments: 0
---

# 2001. 可互换矩形的组数

> **[yiduobo的每日leetcode 2001.可互换矩形的组数](https://zhuanlan.zhihu.com/p/502139915) · 知乎 · 2022-04-21 · 赞同 0**
> 力扣：[2001. 可互换矩形的组数](https://leetcode.cn/problems/number-of-pairs-of-interchangeable-rectangles/) · Medium · 灵茶山艾府：[统计比值的最简分数](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2001.可互换矩形的组数

[力扣](https://leetcode-cn.com/problems/number-of-pairs-of-interchangeable-rectangles/)

题目中宽与高之比相同的矩形可以互换，那么一个自然的想法就是利用哈希表记录每种宽高之比出现的次数。对于某种宽高之比，若其出现的次数为k，那么从这k个矩形中任选两个都可以互换，将会提供k \* (k - 1) / 2组可行的答案。

在这里宽高之比不一定是整数，不方便直接哈希，那么可以先对宽和高进行约分，然后以二元组的形式保存这个最简分数。

最后附上python代码：

```python
class Solution(object):
    def interchangeableRectangles(self, rectangles):
        """
        :type rectangles: List[List[int]]
        :rtype: int
        """

        rec_dict = {}

        for w, h in rectangles:
            if w > h:
                x, y = w, h
            else:
                x, y = h, w

            while y:
                x, y = y, x % y
            
            w /= x
            h /= x
            rec_dict[(w, h)] = rec_dict.get((w, h), 0) + 1

        res = 0
        for v in rec_dict.values():
            res += v * (v - 1) / 2
        
        return res
```
