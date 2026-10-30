---
title: "2250. 统计包含每个点的矩形数目"
aliases: ["yiduobo的每日leetcode 2250.统计包含每个点的矩形数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/binary-search", "leetcode/ordered-set", "leetcode/sorting", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/546922399"
zhihu_id: "546922399"
zhihu_title: "yiduobo的每日leetcode 2250.统计包含每个点的矩形数目"
question_id: "2250"
question: "统计包含每个点的矩形数目"
problem_url: "https://leetcode.cn/problems/count-number-of-rectangles-containing-each-point/"
difficulty: "Medium"
created: "2022-07-27T21:51:32+08:00"
updated: "2022-07-27T21:51:32+08:00"
upvotes: 0
comments: 0
---

# 2250. 统计包含每个点的矩形数目

> **[yiduobo的每日leetcode 2250.统计包含每个点的矩形数目](https://zhuanlan.zhihu.com/p/546922399) · 知乎 · 2022-07-27 · 赞同 0**
> 力扣：[2250. 统计包含每个点的矩形数目](https://leetcode.cn/problems/count-number-of-rectangles-containing-each-point/) · Medium · 灵茶山艾府：[排序 + 排序 + 排序（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2250.统计包含每个点的矩形数目

[力扣](https://leetcode.cn/problems/count-number-of-rectangles-containing-each-point/)

题目给出若干矩形和点，问每个点在多少个矩形内。

注意到题目中的矩形左下角都是(0, 0)，同时每个点的坐标(x, y)满足x和y都大于等于1，因此判断某个点是否在矩形内就只需要考虑矩形右上角的点，也就是说问题转化成了判断对于点(x, y)，有多少个矩形右上角的点(l, h)满足l >\= x且h >\= y。

对于这类多个维度对比的问题，通常的做法是对其中某些维度进行排序，然后利用数据结构来处理剩下的维度。对于本题，注意到x的取值范围非常大但是y的取值范围很小，因此在这里就应该将所有点以及所有矩形右上角的点分别按照x坐标从大到小进行排序，得到两个排序后的数组sorted_points和sorted_rectangles。

接下来遍历sorted_points中的所有点，并维护一个变量p，满足对于当前遍历到的点(x, y)，都满足sorted_rectangles[p][0] >\= x，即sorted_rectangles[0]到sorted_rectangles[p]这些矩阵右上角的横坐标l都大于等于当前处理的点的横坐标x。由于这两个数组都是排好序的，因此随着点的遍历，p也会跟着向后移动，也就是说可以在均摊O(1)的时间内确定每个点对应的p。

接下来的问题就是判断sorted_rectangles[0]到sorted_rectangles[p]这些点中，有多少个点的纵坐标h大于等于当前处理点的纵坐标y。由于纵坐标的取值范围很小，因此直接使用朴素算法来统计应该也是可以的。我在这里使用的是树状数组，将sorted_rectangles[0]到sorted_rectangles[p]这些点的纵坐标加入到树状数组中，然后反过来统计当前树状数组中小于y的值有多少个，记为k，那么剩下的p - k个值必然都大于等于y，也就是题目要求的包含了这个点的矩形数目。

需要注意的是，一开始对点的排序打乱了点的顺序，因此在填充答案时需要通过点在原始数组中的下标来标记填充答案的位置。

最后附上python代码：

```python
class Solution(object):
    def countRectangles(self, rectangles, points):
        """
        :type rectangles: List[List[int]]
        :type points: List[List[int]]
        :rtype: List[int]
        """

        m = len(rectangles)
        n = len(points)

        sorted_rectangles = sorted(rectangles, key=lambda d:d[0], reverse=True)
        sorted_points = sorted([[x, y, index] for index, [x, y] in enumerate(points)], key=lambda d:d[0], reverse=True)

        res = [0] * n
        f = [0] * 101
        p = 0
        for x, y, index in sorted_points:
            while p < m and sorted_rectangles[p][0] >= x:
                now = sorted_rectangles[p][1]
                while now <= 100:
                    f[now] += 1
                    now += now & -now
                p += 1

            res[index] = p
            now = y - 1
            while now > 0:
                res[index] -= f[now]
                now -= now & -now
        
        return res
```
