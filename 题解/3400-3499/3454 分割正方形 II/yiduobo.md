---
title: "3454. 分割正方形II"
aliases: ["yiduobo的每日leetcode 3454.分割正方形II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/segment-tree", "leetcode/sorting", "leetcode/sweep-line", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1893857465495431027"
zhihu_id: "1893857465495431027"
zhihu_title: "yiduobo的每日leetcode 3454.分割正方形II"
question_id: "3454"
question: "分割正方形 II"
problem_url: "https://leetcode.cn/problems/separate-squares-ii/"
difficulty: "Hard"
rating: 2671
created: "2025-04-11T03:10:33+08:00"
updated: "2025-04-11T03:10:33+08:00"
upvotes: 1
comments: 0
---

# 3454. 分割正方形II

> **[yiduobo的每日leetcode 3454.分割正方形II](https://zhuanlan.zhihu.com/p/1893857465495431027) · 知乎 · 2025-04-11 · 赞同 1**
> 力扣：[3454. 分割正方形 II](https://leetcode.cn/problems/separate-squares-ii/) · Hard · 灵茶山艾府：[Lazy 线段树 + 扫描线（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3454.分割正方形II

[3454. 分割正方形 II - 力扣（LeetCode）](https://leetcode.cn/problems/separate-squares-ii/description/)

题目给出一个二维整数数组squares，其中squares\[index\] \= \[x\[index\], y\[index\], l\[index\]\]表示一个与x轴平行的正方形的左下角坐标以及边长。

现在要求找出一个最小的y坐标，对应一条水平线，这条线上方的正方形总面积等于这条线下方的正方形总面积。

正方形可能会重叠，对于重叠的部分，面积只计算一次。

本题题设与上一题类似，在大方向上本题的处理方法也与上一题相同，但是本题中重叠部分的面积只能被计算一次，因此在具体计算方法上略有不同。

依然是使用一条扫码先从下往上扫码，扫描线只会停留在所有的y以及y + l这些位置，而对于tot_l的计算，则不能按上一题的处理方法直接累加。

在这里可以设置一个数组arr，其中arr[index]表示当前生效的正方形是否包含了下标index，那么若当前的扫描线来到某个正方形(x, y, l)的下边，也就是这个正方形即将生效时，将arr中下标x到x + l这一段加上1；反之若当前扫描线来到某个正方形(x, y, k)的上边，也就是这个正方形即将失效时，将arr中下标x到x + l这一段减去1。这样一来，arr中非0元素的数量就是当前生效的tot_l。

这里是一个动态的区间修改以及查询的问题，那么在这里就可以使用线段树来维护arr。由于本题中x的取值范围很大，因此还需要先对x进行离散化，计算出所有出现过的x以及x + l的序并建立起双向的映射，接下来就可以使用这个序来作为线段树中使用的下标。需要注意在计算非0元素的数目时需要将序映射回原始的x。

另外由于本题中的总面积无法一开始就计算得到，因此在扫描线每次移动时，都需要将移动前后的面积以及tot_l都记录下来，扫码完成得到总面积后，再进行一趟遍历计算最终答案。

最后附上python代码：

```python
class Solution(object):
    def separateSquares(self, squares):
        """
        :type squares: List[List[int]]
        :rtype: float
        """

        x_set = set()
        for x, y, l in squares:
            x_set.add(x)
            x_set.add(x + l)
        
        x_mapping = {}
        re_x_mapping = sorted(list(x_set))
        for index, x in enumerate(re_x_mapping):
            x_mapping[x] = index
        
        m = len(x_mapping)
        
        lines = []
        for x, y, l in squares:
            lines.append((y, x_mapping[x], x_mapping[x + l], 1))
            lines.append((y + l, x_mapping[x], x_mapping[x + l], -1))

        def get(p, left, right):
            if g[p] is None:
                if f[p] > 0:
                    g[p] = re_x_mapping[right + 1] - re_x_mapping[left]
                elif left == right:
                    g[p] = 0
                else:
                    mid = (left + right) >> 1
                    g[p] = get(p * 2 + 1, left, mid) + get(p * 2 + 2, mid + 1, right)
            return g[p]

        def put(p, left, right, i, j, delta):
            g[p] = None
            if left == i and right == j:
                f[p] += delta
            else:
                mid = (left + right) >> 1
                if j <= mid:
                    put(p * 2 + 1, left, mid, i, j, delta)
                elif i > mid:
                    put(p * 2 + 2, mid + 1, right, i, j, delta)
                else:
                    put(p * 2 + 1, left, mid, i, mid, delta)
                    put(p * 2 + 2, mid + 1, right, mid + 1, j, delta)

        lines.sort()
        pre_y = lines[0][0]
        f = [0] * (m * 4)
        g = [None] * (m * 4)
        s = 0
        area_list = []
        for y, start_x, end_x, delta in lines:
            if pre_y != y:
                tot_l = get(0, 0, m - 1)
                s += (y - pre_y) * tot_l
                area_list.append((s, tot_l, pre_y, y))

            put(0, 0, m - 1, start_x, end_x - 1, delta)
            pre_y = y

        for below, tot_l, pre_y, y in area_list:
            if below * 2 >= s:
                pre_below = below - (y - pre_y) * tot_l
                return pre_y + (s / 2.0 - pre_below) / tot_l
```
