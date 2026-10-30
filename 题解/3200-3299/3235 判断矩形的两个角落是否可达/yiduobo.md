---
title: "3235. 判断矩形的两个角落是否可达"
aliases: ["yiduobo的每日leetcode 3235.判断矩形的两个角落是否可达"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/graph", "leetcode/geometry", "题单/常用数据结构", "题单/数学算法", "题单/常用数据结构/七-并查集", "题单/数学算法/五-计算几何"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/720471180"
zhihu_id: "720471180"
zhihu_title: "yiduobo的每日leetcode 3235.判断矩形的两个角落是否可达"
question_id: "3235"
question: "判断矩形的两个角落是否可达"
problem_url: "https://leetcode.cn/problems/check-if-the-rectangle-corner-is-reachable/"
difficulty: "Hard"
created: "2024-09-16T23:34:24+08:00"
updated: "2024-09-16T23:34:24+08:00"
upvotes: 0
comments: 0
---

# 3235. 判断矩形的两个角落是否可达

> **[yiduobo的每日leetcode 3235.判断矩形的两个角落是否可达](https://zhuanlan.zhihu.com/p/720471180) · 知乎 · 2024-09-16 · 赞同 0**
> 力扣：[3235. 判断矩形的两个角落是否可达](https://leetcode.cn/problems/check-if-the-rectangle-corner-is-reachable/) · Hard · 灵茶山艾府：[【图解】转换成图上 DFS + 避免浮点数的做法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3235.判断矩形的两个角落是否可达

[. - 力扣（LeetCode）](https://leetcode.cn/problems/check-if-the-rectangle-corner-is-reachable/description/)

题目给出两个正整数xCorner和yCorner，表示存在一个左下角在原点，右上角为(xCorner，yCorner)的矩形。接下来给出若干个三元组，其中第i个为(x[i], y[i], r[i])，表示有一个圆心在(x[i], y[i])，半径为r[i]的圆。

问是否存在一条从原点开始，到(xCorner，yCorner)结束的路径，这条路径在矩形内部，且除了起点和终点不会触碰到矩形的边界，同时这条路径也不能触碰到任何圆的边界或经过圆的内部。

直接找出这样的路径是非常困难的，从样例一就可以发现，可行路径可以是歪歪扭扭的，因此在这里就应该反过来思考，判断可行路径是否被完全阻断了。

首先最简单的情况就是水平或者竖直方向上被某条或者某些圆弧的组合完全阻断的。换一种说法就是某条或者某些圆弧连通了矩形的上边和下边，或者连通了矩形的左边和右边。

接下来观察样例3，可以发现由于两个圆弧的阻隔，路径压根就走不出左下角这个区域，也就是说如果某条或者某些圆弧连通了矩形的左边和下边，那么也不存在合法的路径。更进一步的，即使样例3的两个圆都往右上移动了一丢丢，这两个圆的圆弧也阻隔了右上角，也就是说如果某条或者某些圆弧连通了矩形的上边或者右边，那么同样也不存在合法的路径。

综合上面这些情况，就可以将矩形的四条边以及所有的圆视为图中的点，若圆与圆相交或者圆与矩形边相交或包含，那么就在其对应的点连上一条边。在完成建图后，若矩形的上边和下边，左边和右边，上边和右边，左边和下边这四组点中有任意一组处于同一个连通块中，那么就说明出现了阻隔线，不存在可达的路径，否则必然存在可达的路径。关于连通块的处理可以使用并查集，那么接下来的问题就变成了判断圆与矩形边相交或包含，以及圆与圆相交。

对于圆与圆相交时比较简单的，只需判断两圆的圆心距离是否小于等于两圆的半径之和就行了。

对于圆和矩形边的判断则相对复杂一点，可以分成两种情况：

1、若矩形边的某个端点出现在圆的内部，那么圆必然包含矩形边或者与矩形边相交。判断点是否出现在圆内部只需要判断点到圆心的距离是否小于等于圆的半径就行了。

2、若矩形边的两个端点都在圆的外部，那么就需要从圆心向矩形边所在的直线做一条垂线，这条垂线的长度必须要小于等于半径的长度，同时矩形边的两个端点必须位于这条垂线的两侧。由于题目中矩形的边都是水平或者竖直的，因此矩形边的两个端点必然在某个维度上是一样的，这个维度的值与圆心在这个维度值之差就是垂线的长度，而另一个维度的值只需分别处于圆心另一个维度值的两侧就行了。

到了这里，就得到了一种处理方法。

首先建图，为每个圆以及矩形的四条边新增一个节点。

接下来枚举所有圆，判断圆是否与矩形边相交或包含，若相交或包含则合并二者在图中对应的节点。然后再两两枚举每一组圆，若两圆相交，那么就合并二者在图中对应的节点。

最后考察上边和下边、左边和右边、上边和右边、下边和左边这四组节点，若某一组中的两个节点位于同一个连通块，那么说明不可达，否则可达。

---

到了这里还有一种情况我没有考虑到，就是圆相交于矩形外的情况。例如有一个case为矩形右上角位于(3, 3)，同时有两个圆(2, 1000, 997)以及(1000, 2, 997)。这两个圆分别与矩形的上边和右边相切，同时这两个圆相交，但是由于相交在矩形的外部，因此并没有阻断矩形上边和右边。

可以发现，当两个圆都没有同时连通上边和右边时，也就是单个圆不足以阻断上边和右边时，这两个圆相交的部分必然全部位于矩形的内部或者矩形的外部，当位于矩形内部时则会出现阻断，反之则不会。因此在这里只需要检测两圆相交部分是否位于矩形内部，若位于矩形内部则执行合并节点否则不执行。

而对于判断两圆相交是否位于矩形内部，则可以判断圆心连线按半径比切分的切分点是否位于矩形的内部。更具体的，不妨设两个圆的圆心分别为(x1, y1)，(x2, y2)，半径分别为r1、r2，那么目标点的横坐标就是从x1开始，向x2偏移r1 / (r1 + r2) \* abs(x1- x2)，考虑到x1和x2的相对位置，在这里可以直接写成x1 + (x2 - x1) \* r1 / (r1 + r2)，纵坐标同理。

接下来只需要判断这两个坐标是否分别小于等于xCorner以及yCorner就行了，即

x1 + (x2 - x1) \* r1 / (r1 + r2) \<\= xCorner

两边同时乘以(r1 + r2)，同时约掉x1 \* r1这一项，就有

x1 \* r2 + x2 \* r1 \<\= xCorner \* (r1 + r2)

对于纵坐标是完全对称的，即

y1 \* r2 + y2 \* r1 \<\= yCorner \* (r1 + r2)

若同时满足上面两点，则说明两圆交于矩形内部，需要合并两圆对应的节点，否则不需要。

最后附上python代码：

```python
class Solution(object):
    def canReachCorner(self, xCorner, yCorner, circles):
        """
        :type xCorner: int
        :type yCorner: int
        :type circles: List[List[int]]
        :rtype: bool
        """

        def find(fa, x):
            if fa[x] != x:
                fa[x] = find(fa, fa[x])
            return fa[x]

        def union(fa, x, y):
            fa_x = find(fa, x)
            fa_y = find(fa, y)
            if fa_x != fa_y:
                fa[fa_x] = fa_y

        def dis(p1, p2):
            return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

        def in_circle(circle, p):
            return dis((circle[0], circle[1]), p) <= circle[2] ** 2

        def rec_cross(circle, p1, p2):
            in1 = in_circle(circle, p1)
            in2 = in_circle(circle, p2)
            
            if in1 or in2:
                return True
            
            if p1[0] == p2[0]:
                same = 0
            else:
                same = 1
            
            other = 1 - same
            
            if p1[same] < circle[same] - circle[2] or p1[same] > circle[same] + circle[2]:
                return False
            
            if max(p1[other], p2[other]) < circle[other] or min(p1[other], p2[other]) > circle[other]:
                return False

            return True

        def circle_cross(circle1, circle2):
            return dis((circle1[0], circle1[1]), (circle2[0], circle2[1])) <= (circle1[2] + circle2[2]) ** 2

        def cross_in_rec(circle1, circle2, xCorner, yCorner):
            if circle1[0] * circle2[2] + circle2[0] * circle1[2] >= xCorner * (circle1[2] + circle2[2]):
                return False
            if circle1[1] * circle2[2] + circle2[1] * circle1[2] >= yCorner * (circle1[2] + circle2[2]):
                return False
            return True

        n = len(circles)
        fa = [index for index in range(n + 4)]
        rec_points = [(0, 0), (0, yCorner), (xCorner, yCorner), (xCorner, 0)]
        for i in range(n):
            for p in range(4):
                if rec_cross(circles[i], rec_points[p], rec_points[(p + 1) % 4]):
                    union(fa, i, n + p)
            
            for j in range(i + 1, n):
                if circle_cross(circles[i], circles[j]) and cross_in_rec(circles[i], circles[j], xCorner, yCorner):
                    union(fa, i, j)

        if find(fa, n) == find(fa, n + 2):
            return False

        if find(fa, n + 1) == find(fa, n + 3):
            return False

        if find(fa, n) == find(fa, n + 3):
            return False

        if find(fa, n + 1) == find(fa, n + 2):
            return False
        
        return True
```
