---
title: "963. 最小面积矩形II"
aliases: ["yiduobo的每日leetcode 963.最小面积矩形II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/361144623"
zhihu_id: "361144623"
zhihu_title: "yiduobo的每日leetcode 963.最小面积矩形II"
question_id: "963"
question: "最小面积矩形II"
problem_url: "https://leetcode.cn/problems/minimum-area-rectangle-ii/"
created: "2021-03-30T22:14:19+08:00"
updated: "2021-03-30T22:14:19+08:00"
upvotes: 0
comments: 0
---

# 963. 最小面积矩形II

> **[yiduobo的每日leetcode 963.最小面积矩形II](https://zhuanlan.zhihu.com/p/361144623) · 知乎 · 2021-03-30 · 赞同 0**
> 力扣：[963. 最小面积矩形II](https://leetcode.cn/problems/minimum-area-rectangle-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

963.最小面积矩形II

[力扣](https://leetcode-cn.com/problems/minimum-area-rectangle-ii/)

在这里矩形不一定平行于坐标轴，那么此时就需要枚举至少三个点才能确定一个矩形。不妨设枚举到的三个点为i、j、k，那么我们首先需要判断边(i, j)是否与边(j, k)垂直。这里可以运用到计算几何中的一个技巧。

首先计算出这两条边的向量v1(x1, y1)与v2(x2, y2)，分别为

x1 \= x[j] - x[i]

y1 \= y[j] - y[i]

x2 \= x[j] - x[k]

y2 \= y[j] - y[k]

接下来，我们可以计算这两个向量的点积。由于点积满足v1·v2 \= |v1| \* |v2| \* cos(v1, v2)。由于这里的|v1|和|v2|都大于0，因此只要v1·v2等于0，就说明cos(v1, v2) \= 0，也就是说v1和v2夹角的cos等于0，即二者的夹角为90度，就可以得到v1和v2垂直了。

于是在这里我们可以利用这个结论判断边(i, j)是否与边(j, k)垂直。若垂直，那么我们可以计算出能与这三点形成矩形的第四个点的坐标。具体计算方式有很多，我这里采用的是利用对角线的中点来进行计算。矩形两条对角线的交点恰好能平分两条对角线，那么我们可以计算出i和k的中点mid，那么mid也是j与第四点的中点，此时就可以通过j与mid计算出第四点的坐标。

得到第四点之后，就只需要使用哈希表判断第四点是否存在，并计算矩形面积更新答案。

最后附上python代码：

```python
class Solution(object):
    def minAreaFreeRect(self, points):
        """
        :type points: List[List[int]]
        :rtype: float
        """

        n = len(points)

        point_set = set()
        for x, y in points:
            point_set.add(x * 40001 + y)

        res = None
        for i in range(n):
            for j in range(n):
                if i != j:
                    x1 = points[j][0] - points[i][0]
                    y1 = points[j][1] - points[i][1]
                    for k in range(n):
                        if i != k and j != k:
                            x2 = points[j][0] - points[k][0]
                            y2 = points[j][1] - points[k][1]
                            if x1 * x2 + y1 * y2 == 0:
                                x = points[i][0] + points[k][0] - points[j][0]
                                y = points[i][1] + points[k][1] - points[j][1]
                                if x * 40001 + y in point_set:
                                    area = sqrt(x1 ** 2 + y1 ** 2) * sqrt(x2 ** 2 + y2 ** 2)
                                    if res is None or res > area:
                                        res = area
        if res is None:
            res = 0
            
        return res
```
