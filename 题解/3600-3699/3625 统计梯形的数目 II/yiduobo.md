---
title: "3625. 统计梯形的数目II"
aliases: ["yiduobo的每日leetcode 3625.统计梯形的数目II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/geometry", "leetcode/hash-table", "leetcode/math", "题单/数学算法", "题单/数学算法/五-计算几何"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1945171251908813378"
zhihu_id: "1945171251908813378"
zhihu_title: "yiduobo的每日leetcode 3625.统计梯形的数目II"
question_id: "3625"
question: "统计梯形的数目 II"
problem_url: "https://leetcode.cn/problems/count-number-of-trapezoids-ii/"
difficulty: "Hard"
rating: 2643
created: "2025-08-30T17:23:20+08:00"
updated: "2025-08-30T17:23:20+08:00"
upvotes: 0
comments: 0
---

# 3625. 统计梯形的数目II

> **[yiduobo的每日leetcode 3625.统计梯形的数目II](https://zhuanlan.zhihu.com/p/1945171251908813378) · 知乎 · 2025-08-30 · 赞同 0**
> 力扣：[3625. 统计梯形的数目 II](https://leetcode.cn/problems/count-number-of-trapezoids-ii/) · Hard · 灵茶山艾府：[统计直线 + 去掉重复统计的平行四边形，附思考题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3625.统计梯形的数目II

<https://leetcode.cn/problems/count-number-of-trapezoids-ii/description/>

题目给出一个二维整数数组points，其中points\[index\] \= \[x\[index\], y\[index\]\]，表示第index个点在笛卡尔平面上的坐标。梯形是指具有至少一对平行边的凸四边形，问points中任选四个不同点可以组成的梯形的数目。

之前3623题的加强版，不能直接照搬，但是可以沿用其中容斥原理的思路：

[yiduobo的每日leetcode 3623.统计梯形的数目I](https://zhuanlan.zhihu.com/p/1944894240850163001)

本题中的梯形边不一定平行于x轴，因此在这里需要先计算出所有的点对形成的直线方程。方便期间，在这里应该写成标准式，即Ax + By + C \= 0的形式。另外在这里应该让A和B约到互质。不妨设A和B的最大公约数为g，那么最终A和B需要同时除以g，而C可能无法被g整除，因此在这里需要用分数的形式来表示C/g，理由是对于标准式的两条直线，如果(A, B)相同，那么二者要么平行，要么共线，这里的平行是后续计算的前提。

接下来就可以利用容斥原理来进行计算了。具体来说，对于所有(A, B)相同的直线对，如果二者不共线，那么就可以形成一个梯形，因此在这里可以使用直线对的总数，减去共线直线对的总数来进行计算。其中共线直线是在(A, B)相同的前提下，C/g相同的直线对是共线的。

需要特别注意的是，上面还额外重复计算了平行四边形与矩形，因为这两种图形的两组对边都是平行的。由于平行四边形和矩形的对边的长度必然相等，因此在这里可以通过点对间的距离来判断形成的是否为平行四边形，因此在这里只需减去平行且点对距离相等的直线对数目的一半即可。

更进一步的，如果在这里直接使用(A, B)相同且点对距离相等来计算平行四边形和矩形数目的话，还会额外将共线且点对距离相等的情况计算进来。这种情况在计算共线时减去了一次，在计算平行四边形和矩形时又减去了一次，因此在这里还需要将这种情况加回来。

最后附上python代码：

```python
class Solution(object):
    def countTrapezoids(self, points):
        """
        :type points: List[List[int]]
        :rtype: int
        """
        
        def gcd(x, y):
            while y > 0:
                x, y = y, x % y
            return x

        lines = {}
        for i, (x1, y1) in enumerate(points):
            for j, (x2, y2) in enumerate(points[i + 1:]):
                A = y1 - y2
                B = x2 - x1
                C = x1 * y2 - x2 * y1
                if A == 0 or B == 0:
                    g = max(abs(A), abs(B))
                else:
                    g = gcd(abs(A), abs(B))
                
                A //= g
                B //= g
                if A < 0:
                    A = -A
                    B = -B
                    C = -C
                elif A == 0 and B < 0:
                    B = -B
                    C = -C
                
                if C != 0:
                    t = gcd(g, abs(C))
                    g //= t
                    C //= t
                else:
                    g = 0
                
                key = (A, B)
                if key not in lines:
                    lines[key] = []
                lines[key].append((C, g, (x1 - x2) ** 2 + (y1 - y2) ** 2))

        pair = 0
        same_dis_pair = 0
        same_line_same_dis_pair = 0
        for key in lines:
            tot = len(lines[key])
            pair += tot * (tot - 1) // 2
            c_dict = {}
            dis_dict = {}
            all_dict = {}
            for C, g, dis in lines[key]:
                key_c = (C, g)
                c_dict[key_c] = c_dict.get(key_c, 0) + 1
                key_all = (C, g, dis)
                all_dict[key_all] = all_dict.get(key_all, 0) + 1 
                dis_dict[dis] = dis_dict.get(dis, 0) + 1
            
            for key_c in c_dict:
                same_line = c_dict[key_c]
                pair -= same_line * (same_line - 1) // 2
            
            for dis in dis_dict:
                same_dis = dis_dict[dis]
                same_dis_pair += same_dis * (same_dis - 1) // 2

            for key_all in all_dict:
                same_line_same_dis = all_dict[key_all]
                same_line_same_dis_pair += same_line_same_dis * (same_line_same_dis - 1) // 2

        return pair - same_dis_pair // 2 + same_line_same_dis_pair // 2
```
