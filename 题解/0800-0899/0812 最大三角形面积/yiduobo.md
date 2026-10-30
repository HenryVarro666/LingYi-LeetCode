---
title: "812. 最大三角形面积"
aliases: ["yiduobo的每日leetcode 812.最大三角形面积"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/geometry", "leetcode/math", "leetcode/two-pointers", "leetcode/enumeration", "leetcode/bao-li", "题单/数学算法", "题单/数学算法/五-计算几何"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/343811176"
zhihu_id: "343811176"
zhihu_title: "yiduobo的每日leetcode 812.最大三角形面积"
question_id: "812"
question: "最大三角形面积"
problem_url: "https://leetcode.cn/problems/largest-triangle-area/"
difficulty: "Easy"
created: "2021-01-13T22:15:26+08:00"
updated: "2021-01-13T22:15:26+08:00"
upvotes: 0
comments: 0
---

# 812. 最大三角形面积

> **[yiduobo的每日leetcode 812.最大三角形面积](https://zhuanlan.zhihu.com/p/343811176) · 知乎 · 2021-01-13 · 赞同 0**
> 力扣：[812. 最大三角形面积](https://leetcode.cn/problems/largest-triangle-area/) · Easy · 灵茶山艾府：[两种方法：枚举 / 凸包+旋转卡壳（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

812.最大三角形面积

[力扣](https://leetcode-cn.com/problems/largest-triangle-area/)

判断能否形成三角形通常是两边长度之和大于第三边，而知道三条边的长度之和则可以使用海伦公式来求解三角形的面积。

由于题目给出的点数量非常少，因此可以直接枚举三个点的所有组合，计算出边的长度，判断能否形成三角形并使用海伦公式计算面积。

最后附上python代码：

```python
class Solution(object):
    def largestTriangleArea(self, points):
        """
        :type points: List[List[int]]
        :rtype: float
        """

        n = len(points)
        res = 0
        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    A = sqrt((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)
                    B = sqrt((points[i][0] - points[k][0]) ** 2 + (points[i][1] - points[k][1]) ** 2)
                    C = sqrt((points[j][0] - points[k][0]) ** 2 + (points[j][1] - points[k][1]) ** 2)
                    if A + B > C and A + C > B and B + C > A:
                        avg = (A + B + C) / 2
                        s = sqrt(avg * (avg - A) * (avg - B) * (avg - C))
                        res = max(s, res)
        
        return res
```
