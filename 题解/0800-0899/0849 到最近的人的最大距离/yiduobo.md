---
title: "849. 到最近的人的最大距离"
aliases: ["yiduobo的每日leetcode 849.到最近的人的最大距离"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/348104993"
zhihu_id: "348104993"
zhihu_title: "yiduobo的每日leetcode 849.到最近的人的最大距离"
question_id: "849"
question: "到最近的人的最大距离"
problem_url: "https://leetcode.cn/problems/maximize-distance-to-closest-person/"
created: "2021-01-31T21:39:12+08:00"
updated: "2021-01-31T21:39:12+08:00"
upvotes: 0
comments: 0
---

# 849. 到最近的人的最大距离

> **[yiduobo的每日leetcode 849.到最近的人的最大距离](https://zhuanlan.zhihu.com/p/348104993) · 知乎 · 2021-01-31 · 赞同 0**
> 力扣：[849. 到最近的人的最大距离](https://leetcode.cn/problems/maximize-distance-to-closest-person/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

849.到最近的人的最大距离

[力扣](https://leetcode-cn.com/problems/maximize-distance-to-closest-person/)

题目要求找到一个离两边的人最远的座位，那么对于一段连续的空位，若这一段空位位于两侧，就选择最边上的座位，否则就选择这一段空位最中间的座位。

最后附上python代码：

```python
class Solution(object):
    def maxDistToClosest(self, seats):
        """
        :type seats: List[int]
        :rtype: int
        """

        l = None
        res = 0
        for index, num in enumerate(seats):
            if num == 0:
                if l is None:
                    l = index
            else:
                if l is not None:
                    if l == 0:
                        res = max(res, index)
                    else:
                        res = max(res, (index - l + 1) / 2)
                l = None
        
        if l is not None:
            res = max(res, len(seats) - l)

        return res
```
