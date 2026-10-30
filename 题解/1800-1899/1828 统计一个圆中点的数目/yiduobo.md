---
title: "1828. 统计一个圆中点的数目"
aliases: ["yiduobo的每日leetcode 1828.统计一个圆中点的数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/467479425"
zhihu_id: "467479425"
zhihu_title: "yiduobo的每日leetcode 1828.统计一个圆中点的数目"
question_id: "1828"
question: "统计一个圆中点的数目"
problem_url: "https://leetcode.cn/problems/queries-on-number-of-points-inside-a-circle/"
created: "2022-02-14T23:07:35+08:00"
updated: "2022-02-14T23:07:35+08:00"
upvotes: 0
comments: 0
---

# 1828. 统计一个圆中点的数目

> **[yiduobo的每日leetcode 1828.统计一个圆中点的数目](https://zhuanlan.zhihu.com/p/467479425) · 知乎 · 2022-02-14 · 赞同 0**
> 力扣：[1828. 统计一个圆中点的数目](https://leetcode.cn/problems/queries-on-number-of-points-inside-a-circle/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1828.统计一个圆中点的数目

[力扣](https://leetcode-cn.com/problems/queries-on-number-of-points-inside-a-circle/)

由于题目的数据规模很小，所以朴素的算法是可行的。枚举每个query中的圆，然后遍历所有的点，判断点是否在圆中。具体判断的依据就是点与圆心的距离是否小于等于圆的半径。

感觉可以用计算几何的知识来优化，但是没有什么好的想法。

最后附上python代码：

```python
class Solution(object):
    def countPoints(self, points, queries):
        """
        :type points: List[List[int]]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        res = []
        for cx, cy, r in queries:
            res.append(0)
            for x, y in points:
                if (x - cx) ** 2 + (y - cy) ** 2 <= r ** 2:
                    res[-1] += 1
        
        return res
```
