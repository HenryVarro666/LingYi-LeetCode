---
title: "1637. 两点之间不包含任何点的最宽垂直面积"
aliases: ["yiduobo的每日leetcode 1637.两点之间不包含任何点的最宽垂直面积"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/438388181"
zhihu_id: "438388181"
zhihu_title: "yiduobo的每日leetcode 1637.两点之间不包含任何点的最宽垂直面积"
question_id: "1637"
question: "两点之间不包含任何点的最宽垂直面积"
problem_url: "https://leetcode.cn/problems/widest-vertical-area-between-two-points-containing-no-points/"
created: "2021-11-27T12:44:03+08:00"
updated: "2021-11-27T12:44:03+08:00"
upvotes: 0
comments: 0
---

# 1637. 两点之间不包含任何点的最宽垂直面积

> **[yiduobo的每日leetcode 1637.两点之间不包含任何点的最宽垂直面积](https://zhuanlan.zhihu.com/p/438388181) · 知乎 · 2021-11-27 · 赞同 0**
> 力扣：[1637. 两点之间不包含任何点的最宽垂直面积](https://leetcode.cn/problems/widest-vertical-area-between-two-points-containing-no-points/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1637.两点之间不包含任何点的最宽垂直面积

[力扣](https://leetcode-cn.com/problems/widest-vertical-area-between-two-points-containing-no-points/)

根据题目描述，虽然是平面上的点，但是实际上只需要关心x这一维，所求的就是相邻x之间的最大间隔。于是可以按x从小到大进行排序，然后一趟扫描求解即可。

最后附上python代码：

```python
class Solution(object):
    def maxWidthOfVerticalArea(self, points):
        """
        :type points: List[List[int]]
        :rtype: int
        """

        res = None
        last_x = None
        for x, y in sorted(points, key=lambda d:d[0]):
            if last_x is not None:
                if res is None or res < x - last_x:
                    res = x - last_x
            
            last_x = x
        
        return res
```
