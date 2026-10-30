---
title: "469. 凸多边形"
aliases: ["yiduobo的每日leetcode 469.凸多边形"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/599992875"
zhihu_id: "599992875"
zhihu_title: "yiduobo的每日leetcode 469.凸多边形"
question_id: "469"
question: "凸多边形"
problem_url: "https://leetcode.cn/problems/convex-polygon/"
created: "2023-01-19T03:29:37+08:00"
updated: "2023-01-19T03:29:37+08:00"
upvotes: 0
comments: 0
---

# 469. 凸多边形

> **[yiduobo的每日leetcode 469.凸多边形](https://zhuanlan.zhihu.com/p/599992875) · 知乎 · 2023-01-19 · 赞同 0**
> 力扣：[469. 凸多边形](https://leetcode.cn/problems/convex-polygon/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

469.凸多边形

[力扣](https://leetcode.cn/problems/convex-polygon/)

题目给出平面上的一些点，要求判断这些点是否都属于同一个凸包。在这里可以直接套用凸包的算法，检测是否所有点都没有被丢弃掉。

凸包的具体实现可以参考之前的

[yiduobo：yiduobo的每日leetcode 587.安装栅栏](https://zhuanlan.zhihu.com/p/267147402)

最后附上python代码：

```python
class Solution(object):
    def isConvex(self, points):
        """
        :type points: List[List[int]]
        :rtype: bool
        """

        def Xmul(p1, p2, p3):
            x1 = p2[0] - p1[0]
            y1 = p2[1] - p1[1]
            x2 = p3[0] - p2[0]
            y2 = p3[1] - p2[1]

            return x1 * y2 - x2 * y1

        def sort_cmp(x, y):
            tmp = Xmul(left, x, y)
            if tmp > 0:
                return -1
            elif tmp < 0:
                return 1
            elif (x[0] - left[0]) ** 2 + (x[1] - left[1]) ** 2 < (y[0] - left[0]) ** 2 + (y[1] - left[1]) ** 2:
                return -1        

            return 1
        
        left = points[0]
        pos = 0
        for index, point in enumerate(points[1:]):
            if point[0] < left[0] or (point[0] == left[0] and point[1] > left[1]):
                left = point
                pos = index + 1
        
        points[0], points[pos] = points[pos], points[0]
        sorted_points = sorted(points[1:], sort_cmp)

        reverse_pos = len(sorted_points) - 1
        while reverse_pos > 0 and Xmul(left, sorted_points[reverse_pos], sorted_points[reverse_pos - 1]) == 0:
            reverse_pos -= 1

        for index in range(reverse_pos, reverse_pos + (len(sorted_points) - reverse_pos) / 2):
            swap_pos = len(sorted_points) - 1 - index + reverse_pos
            sorted_points[index], sorted_points[swap_pos] = sorted_points[swap_pos], sorted_points[index]

        last_one = left
        last_two = None
        for point in sorted_points:
            if last_two is not None and Xmul(last_one, last_two, point) > 0:
                return False
            last_two, last_one = last_one, point
        
        return True
```
