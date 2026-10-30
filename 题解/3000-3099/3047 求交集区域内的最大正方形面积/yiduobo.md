---
title: "3047. 求交集区域内的最大正方形面积"
aliases: ["yiduobo的每日leetcode 3047.求交集区域内的最大正方形面积"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/696266596"
zhihu_id: "696266596"
zhihu_title: "yiduobo的每日leetcode 3047.求交集区域内的最大正方形面积"
question_id: "3047"
question: "求交集区域内的最大正方形面积"
problem_url: "https://leetcode.cn/problems/find-the-largest-area-of-square-inside-two-rectangles/"
difficulty: "Medium"
created: "2024-05-07T02:07:37+08:00"
updated: "2024-05-07T02:07:37+08:00"
upvotes: 1
comments: 0
---

# 3047. 求交集区域内的最大正方形面积

> **[yiduobo的每日leetcode 3047.求交集区域内的最大正方形面积](https://zhuanlan.zhihu.com/p/696266596) · 知乎 · 2024-05-07 · 赞同 1**
> 力扣：[3047. 求交集区域内的最大正方形面积](https://leetcode.cn/problems/find-the-largest-area-of-square-inside-two-rectangles/) · Medium · 灵茶山艾府：[枚举 + 最优性剪枝（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3047.求交集区域内的最大正方形面积

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-largest-area-of-square-inside-two-rectangles/description/)

题目的数据规模不大，完全可以两两枚举矩形，那么问题就变成了给出两个矩形，计算相交部分中的正方形面积。另一方面，由于矩形的摆放是平行于坐标轴的，因此可以分别从横纵坐标两个方面分别考虑，取这两个方向交集的较小值即为相交部分的正方形边长，那么问题进一步转化，变成了给出两条线段，问线段重叠部分的长度。

对于线段相交的问题，如果两条线段相交，那么起点中的较大值必然要小于另一条线段的终点，而重叠部分的长度则为终点的较小值减去起点的较大值。

根据上面的结论，只需两两遍历矩形，分别从横纵坐标两个角度计算矩形边长重叠的长度，取其中的较小值作为重叠部分正方形的边长并更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def largestSquareArea(self, bottomLeft, topRight):
        """
        :type bottomLeft: List[List[int]]
        :type topRight: List[List[int]]
        :rtype: int
        """

        n = len(bottomLeft)
        res = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                x = max(0, min(topRight[i][0], topRight[j][0]) - max(bottomLeft[i][0], bottomLeft[j][0]))
                y = max(0, min(topRight[i][1], topRight[j][1]) - max(bottomLeft[i][1], bottomLeft[j][1]))
                res = max(res, min(x, y) ** 2)
        
        return res
```
