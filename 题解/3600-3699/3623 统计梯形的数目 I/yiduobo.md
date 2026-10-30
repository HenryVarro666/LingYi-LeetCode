---
title: "3623. 统计梯形的数目I"
aliases: ["yiduobo的每日leetcode 3623.统计梯形的数目I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/math", "leetcode/combinatorics", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1944894240850163001"
zhihu_id: "1944894240850163001"
zhihu_title: "yiduobo的每日leetcode 3623.统计梯形的数目I"
question_id: "3623"
question: "统计梯形的数目 I"
problem_url: "https://leetcode.cn/problems/count-number-of-trapezoids-i/"
difficulty: "Medium"
rating: 1580
created: "2025-08-29T23:01:50+08:00"
updated: "2025-08-29T23:01:50+08:00"
upvotes: 1
comments: 0
---

# 3623. 统计梯形的数目I

> **[yiduobo的每日leetcode 3623.统计梯形的数目I](https://zhuanlan.zhihu.com/p/1944894240850163001) · 知乎 · 2025-08-29 · 赞同 1**
> 力扣：[3623. 统计梯形的数目 I](https://leetcode.cn/problems/count-number-of-trapezoids-i/) · Medium · 灵茶山艾府：[枚举右，维护左（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3623.统计梯形的数目I

[3623. 统计梯形的数目 I - 力扣（LeetCode）](https://leetcode.cn/problems/count-number-of-trapezoids-i/description/)

题目给出一个二维整数数组points，其中points\[index\] \= \[x\[index\], y\[index\]\]，表示第index个点在笛卡尔平面上的坐标。水平梯形是指具有一对平行于x轴的边的凸四边形，问points总任选四个不同点可以组成的水平梯形的数目。

题目中虽然说的是水平梯形，但是按照这个定义平行四边形和矩形也算是水平梯形，也就是说这里只需要满足有两组不共线的水平边就行了。基于这一点，就可以通过容斥原理来计算。

具体来说，可以先以y作为key，利用哈希表收集处于同一水平线上的点的数量，在这里记为cnt，那么对于cnt[y]，其中任选两点都可以组成一条平行于x轴的边，因此一共可以组成line_y \= cnt[y] \* (cnt[y] - 1) // 2条边，可以将其累加到总的可用边数line中。计算完成后，从line中任选两条不同线的边就可以组成一个水平梯形，在这里可以认为是从line中任选两条边，减去其中共线的边。

任选两条边的方案有line \* (line - 1) // 2种，而共线的边则可以在计算每种line_y时顺便计算，也就是从每种y对应的line_y条边时选出两条边，一共有line_y \* (line_y - 1) // 2中方案。那么只需用前者减去所有y对应的后者，即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def countTrapezoids(self, points):
        """
        :type points: List[List[int]]
        :rtype: int
        """
        
        cnt = {}
        res = 0
        line = 0
        for x, y in points:
            cnt[y] = cnt.get(y, 0) + 1
        
        mod = 10 ** 9 + 7
        for y in cnt:
            line_y = cnt[y] * (cnt[y] - 1) // 2
            line += line_y
            res += (mod - line_y * (line_y - 1) // 2 % mod)
            res %= mod
        
        res += line * (line - 1) // 2 % mod
        return res % mod
```
