---
title: "3453. 分割正方形I"
aliases: ["yiduobo的每日leetcode 3453.分割正方形I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/math", "leetcode/binary-search", "leetcode/ordered-set", "leetcode/sorting", "题单/二分算法", "题单/常用数据结构", "题单/二分算法/二-二分答案", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1893839096247477500"
zhihu_id: "1893839096247477500"
zhihu_title: "yiduobo的每日leetcode 3453.分割正方形I"
question_id: "3453"
question: "分割正方形 I"
problem_url: "https://leetcode.cn/problems/separate-squares-i/"
difficulty: "Medium"
rating: 1735
created: "2025-04-11T02:45:45+08:00"
updated: "2025-04-11T02:45:45+08:00"
upvotes: 2
comments: 0
---

# 3453. 分割正方形I

> **[yiduobo的每日leetcode 3453.分割正方形I](https://zhuanlan.zhihu.com/p/1893839096247477500) · 知乎 · 2025-04-11 · 赞同 2**
> 力扣：[3453. 分割正方形 I](https://leetcode.cn/problems/separate-squares-i/) · Medium · 灵茶山艾府：[三种方法：浮点二分 / 整数二分 / 差分（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3453.分割正方形I

[3453. 分割正方形 I - 力扣（LeetCode）](https://leetcode.cn/problems/separate-squares-i/description/)

题目给出一个二维整数数组squares，其中squares\[index\] \= \[x\[index\], y\[index\], l\[index\]\]表示一个与x轴平行的正方形的左下角坐标以及边长。

现在要求找出一个最小的y坐标，对应一条水平线，这条线上方的正方形总面积等于这条线下方的正方形总面积。

正方形可能会重叠，对于重叠的部分，面积应该多次计算。

不妨想象有一条水平的扫码线从下往上移动，那么随着这条线的移动，线下方的面积会越来越大。当某一时刻这条线下方的面积等于总面积的一半时，这条线对应的y就是最终答案。

其中总面积的一半是很好计算的。由于本题中对于正方形重叠的部分会多次计算，因此只需遍历所有的正方形，将所有正方形的面积累加起来即为正方形的总面积。

接下来需要想办法计算扫描线下方的总面积。

由于数据规模的原因，在这里不能连续的去扫描，因此只能让扫描线在离散的点中从下往上进行移动。一个自然的想法就是对于所有的正方形(x, y, l)，都让扫描线在y和y + l处停留，因为只有当扫描线处于这两个位置之间时，这个正方形的面积才应该被计算进来。于是可以将所有正方形的y以及y + l收集起来，从小到大进行排序，然后让扫描线从下往上移动。当扫描线移动，扫描线下方新增的面积就是本次移动时扫过的面积，这个面积可以通过当前生效的tot_l，乘以扫描线移动的距离来计算得到。

这里的生效的tot_l指的是所有生效的正方形边长之和：若当前扫码线y \= t位于某个正方形的y到y + l之间时，这个正方形就是生效的。

理由是只有当t位于y到y + l之间时，扫描线才会扫过这个矩形，而扫过的面积就是这个正方形的边长l，乘以扫描线移动的距离。由于正方形重叠的部分面积会多次计算，因此在这里可以将扫过的所有正方形的l累加起来，也就是这里说的生效的tot_l。

可以发现，扫描线移动的距离是很好计算的，而对于生效的tot_l的长度，则可以利用类似差分数组的方式来处理。具体来说，当扫描线移动时，先通过当前生效的tot_l计算本次移动时扫过的正方形的面积，接下来若当前扫描线位于某个正方形的下边，那么就将这个正方形的边长l累加到tot_l中，反之若当前扫描线位于某个正方形的上边，那么就将这个正方形的边长l从tot_l中减去。

最后需要处理的问题是如何确定最终答案。样例2已经指出本题中的答案不一定处于某个正方形的y或者y + l处，需要想办法处理。在这里不妨设本次移动之前扫描线下方的面积之和为below，而本次移动扫过的面积为now，那么当below小于总面积s的一半，且below加上now大于等于s的一半时，就说明below加上now的一部分恰好就是s的一半，也就是说最终答案必然位于本次扫描线移动的两个y之间。此时只需将s的一半减去below，再除以当前生效的x，就可以得到使得now的一部分加上below恰好等于s的一半时扫描线应该移动的距离，将其与扫描线之前的位置相加即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def separateSquares(self, squares):
        """
        :type squares: List[List[int]]
        :rtype: float
        """
        
        s = 0
        points = []
        for x, y, l in squares:
            points.append((y, l))
            points.append((y + l, -l))
            s += l * l
        
        points.sort()
        below = 0
        pre_y = points[0][0]
        tot_l = points[0][1]
        for y, l in points[1:]:
            now = (y - pre_y) * tot_l
            if (below + now) * 2 >= s:
                return pre_y + (s / 2.0 - below) / tot_l
            
            tot_l += l
            pre_y = y
            below += now
```
