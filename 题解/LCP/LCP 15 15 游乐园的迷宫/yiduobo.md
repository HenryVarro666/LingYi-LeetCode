---
title: "LCP 15. 游乐园的迷宫"
aliases: ["yiduobo的每日leetcode LCP15.游乐园的迷宫"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/571671070"
zhihu_id: "571671070"
zhihu_title: "yiduobo的每日leetcode LCP15.游乐园的迷宫"
question_id: "LCP 15"
question: "游乐园的迷宫"
problem_url: "https://leetcode.cn/problems/you-le-yuan-de-mi-gong/"
created: "2022-10-09T04:08:33+08:00"
updated: "2022-10-09T04:08:33+08:00"
upvotes: 0
comments: 0
---

# LCP 15. 游乐园的迷宫

> **[yiduobo的每日leetcode LCP15.游乐园的迷宫](https://zhuanlan.zhihu.com/p/571671070) · 知乎 · 2022-10-09 · 赞同 0**
> 力扣：[LCP 15. 游乐园的迷宫](https://leetcode.cn/problems/you-le-yuan-de-mi-gong/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP15.游乐园的迷宫

[力扣](https://leetcode.cn/problems/you-le-yuan-de-mi-gong/)

题目给出了一系列点以及一串方向标记，要求找出一条路径，满足路径上的转角与方向标识一一对应。

对于本题，我只想到了一种可行的构造方案，但是不知道如何给出严格的证明。一个直观的思路是，若接下来需要向左转，那么就提前走到剩下点中最右侧的那个点，反之，则走到剩下点中最左侧的那个点。这样做的好处是如果出现连续的左转或者右转操作，剩下的点也足够应付了，否则可能出现由于当前这一轮走到的目标点不够靠边，导致之后的操作点数不够。

接下来的问题就是如何判断左右。左右是一个相对的概念，在本题中，不妨设上一轮走到的点为p，接下来要选择本轮的目标点。一开始可以随机选择一个目标点，记为target，而对于剩下的点index，若index在p与target连线的左侧，那么就可以认为index在target更左边，否则index就在target更右边，接下来就可以根据这个判断是否需要使用index来更新target，从而完成每一轮目标点的选择。

最后的问题就是，如果判断一个点是否在一条线的左侧还是右侧。这是经典的计算几何问题，可以使用叉积来进行判断。

最后附上python代码：

```python
class Solution(object):
    def visitOrder(self, points, direction):
        """
        :type points: List[List[int]]
        :type direction: str
        :rtype: List[int]
        """

        n = len(points)
        rest = set(range(n))
        p = 0
        for index in range(1, len(points)):
            if points[index][0] < points[p][0] or (points[index][0] == points[p][0] and points[index][1] < points[p][1]):
                p = index
        
        rest.remove(p)
        res = [p]

        def X(p1, p2, p3):
            return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])

        for d in direction:
            if d == 'L':
                delta = 1
            else:
                delta = -1
            
            choose = None
            for index in rest:
                if choose is None or X(points[choose], points[p], points[index]) * delta > 0:
                    choose = index
            
            res.append(choose)
            rest.remove(choose)
            p = choose
        
        res.extend(list(rest))
        return res
```
