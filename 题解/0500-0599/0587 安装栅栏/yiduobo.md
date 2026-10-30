---
title: "587. 安装栅栏"
aliases: ["yiduobo的每日leetcode 587.安装栅栏"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/267147402"
zhihu_id: "267147402"
zhihu_title: "yiduobo的每日leetcode 587.安装栅栏"
question_id: "587"
question: "安装栅栏"
problem_url: "https://leetcode.cn/problems/erect-the-fence/"
created: "2020-10-20T21:34:16+08:00"
updated: "2020-10-20T21:34:16+08:00"
upvotes: 0
comments: 0
---

# 587. 安装栅栏

> **[yiduobo的每日leetcode 587.安装栅栏](https://zhuanlan.zhihu.com/p/267147402) · 知乎 · 2020-10-20 · 赞同 0**
> 力扣：[587. 安装栅栏](https://leetcode.cn/problems/erect-the-fence/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

587.安装栅栏<https://leetcode-cn.com/problems/erect-the-fence/>

计算几何中经典的凸包问题，一般的做法有卷包裹法、格拉汉姆扫描法、快速凸包法以及旋转卡壳法。

起先注意到题目中保证每个点下标都是整数，且都在0到100之间，感觉可以用一些非常规手段来做，但是搞到后面变成了解析几何形式的凸包，还不如直接使用经典做法。

我在这里采用的是格拉汉姆扫描法，具体为：

1、首先找出所有点中最左边的点，若纵坐标相等，则选择最下面的点，设为left。

2、将其他的点，按其到left的连线按逆时针进行排序。位于同一条线上的点则按到left的距离从近到远排序，其中最后一条线上的点则反过来按从远到近排序。样例一中，left点为(1,1)，其他点排好序之后依次为(2, 0), (4, 2), (2, 2), (3, 3), (2, 4)。

3、选择left为凸包的起点，接下来将排好序的点依次尝试加入凸包。当某个点加入凸包时，其与之前凸包中的最后一个点以及倒数第二个点可能形成凸的形状，也可能形成凹的形状。考察这个形状，若其为凹时，说明当前凸包的最后一个点不应该位于凸包上，因此将其移除，直到当前点以及凸包中的最后两个点形成的性质为凸。这一步可以使用栈来完成。

对于步骤2中的排序以及步骤3中的形状考察，本质上就是判断两条线的空间关系，在计算几何当中一般是使用向量的差积来进行判断。

最后附上python代码，代码中Xmul即为向量差积的计算：

```python
class Solution(object):

    def Xmul(self, p1, p2, p3):
        x1 = p2[0] - p1[0]
        y1 = p2[1] - p1[1]
        x2 = p3[0] - p2[0]
        y2 = p3[1] - p2[1]

        return x1 * y2 - x2 * y1

    def sort_cmp(self, x, y):
        tmp = self.Xmul(self.left, x, y)
        if tmp > 0:
            return -1
        elif tmp < 0:
            return 1
        elif (x[0] - self.left[0]) ** 2 + (x[1] - self.left[1]) ** 2 < (y[0] - self.left[0]) ** 2 + (y[1] - self.left[1]) ** 2:
            return -1        

        return 1

    def outerTrees(self, points):
        """
        :type points: List[List[int]]
        :rtype: List[List[int]]
        """

        if len(points) < 3:
            return points

        self.left = points[0]
        pos = 0
        for index, point in enumerate(points[1:]):
            if point[0] < self.left[0] or (point[0] == self.left[0] and point[1] < self.left[1]):
                self.left = point
                pos = index + 1
        
        points[0], points[pos] = points[pos], points[0]
        sorted_points = sorted(points[1:], self.sort_cmp)

        reverse_pos = len(sorted_points) - 1
        while reverse_pos > 0 and self.Xmul(self.left, sorted_points[reverse_pos], sorted_points[reverse_pos - 1]) == 0:
            reverse_pos -= 1

        for index in range(reverse_pos, reverse_pos + (len(sorted_points) - reverse_pos) / 2):
            swap_pos = len(sorted_points) - 1 - index + reverse_pos
            sorted_points[index], sorted_points[swap_pos] = sorted_points[swap_pos], sorted_points[index]

        res = [self.left]
        for point in sorted_points:
            while len(res) >1 and self.Xmul(res[-1], res[-2], point) > 0:
                res.pop()
            
            res.append(point)

        return res
```
