---
title: "3588. 找到最大三角形面积"
aliases: ["yiduobo的每日leetcode 3588.找到最大三角形面积"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1939091456468955904"
zhihu_id: "1939091456468955904"
zhihu_title: "yiduobo的每日leetcode 3588.找到最大三角形面积"
question_id: "3588"
question: "找到最大三角形面积"
problem_url: "https://leetcode.cn/problems/find-maximum-area-of-a-triangle/"
difficulty: "Medium"
created: "2025-08-13T22:44:36+08:00"
updated: "2025-08-13T22:44:36+08:00"
upvotes: 1
comments: 0
---

# 3588. 找到最大三角形面积

> **[yiduobo的每日leetcode 3588.找到最大三角形面积](https://zhuanlan.zhihu.com/p/1939091456468955904) · 知乎 · 2025-08-13 · 赞同 1**
> 力扣：[3588. 找到最大三角形面积](https://leetcode.cn/problems/find-maximum-area-of-a-triangle/) · Medium · 灵茶山艾府：[维护横纵坐标的最小值和最大值（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3588.找到最大三角形面积

<https://leetcode.cn/problems/find-maximum-area-of-a-triangle/description/>

题目给出一个二维数组coords，大小为n \* 2，表示一个无限笛卡尔平面上n个点的坐标。

现在要求找出一个最大的三角形，这个三角形的三个顶点来自coords中的任意三个点，且这个三角形至少有一条边与x轴或者y轴平行。要求返回这个最大三角形面积的两倍，若不存在这样的三角形，则返回-1。

由于题目要求寻找的三角形至少有一条边与x轴或者y轴平行，那么就说明三角形上有两点的横坐标或者纵坐标相同。以横坐标相同为例，此时第三个点的横坐标必然与这两个点不同，否则无法形成三角形。同时，这个三角形的面积也可以很方便计算：以相同横坐标的两点之间的线段作为底，过第三个点到这条线段所在直线的做的垂线作为高，即可计算这个三角形的面积。

为了使得面积尽量大，就应该让底和高都尽量大。不妨设现在已经规定了相同横坐标的两点的横坐标为x，那么对于底的计算，就应该让横坐标相同的这两个点离得尽量远，也就是说应该取横坐标为x的点中，纵坐标最小和最大的点对。而对于高的计算，则只取决于第三个点与x之差，因此只需取所有点中横坐标最小和最大的点，计算其与x之差的绝对值，取较大的即为高。

基于上面的结论，就可以先遍历所有的点，使用哈希表统计每种横坐标对应的最大和最小的纵坐标，以及每种纵坐标对应的最大和最小的横坐标，接下来再分别遍历所有的横纵坐标，按照上面的计算方式计算当前情况下可以得到的最大三角形面积，取其中的最大值乘以2之后即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxArea(self, coords):
        """
        :type coords: List[List[int]]
        :rtype: int
        """
        
        max_x = None
        min_x = None
        max_y = None
        min_y = None

        max_in_row = {}
        min_in_row = {}
        max_in_col = {}
        min_in_col = {}

        for x, y in coords:
            if max_x is None or x > max_x:
                max_x = x
            if min_x is None or x < min_x:
                min_x = x
            if max_y is None or y > max_y:
                max_y = y
            if min_y is None or y < min_y:
                min_y = y
            if x not in max_in_col or max_in_col[x] < y:
                max_in_col[x] = y
            if x not in min_in_col or min_in_col[x] > y:
                min_in_col[x] = y
            if y not in max_in_row or max_in_row[y] < x:
                max_in_row[y] = x
            if y not in min_in_row or min_in_row[y] > x:
                min_in_row[y] = x
        
        res = 0
        for x in max_in_col:
            res = max(res, (max_in_col[x] - min_in_col[x]) * max((max_x - x), (x - min_x)))
        for y in max_in_row:
            res = max(res, (max_in_row[y] - min_in_row[y]) * max((max_y - y), (y - min_y)))
        if res == 0:
            res = -1
        return res
```
