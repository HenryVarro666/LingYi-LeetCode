---
title: "2249. 统计圆内格点数目"
aliases: ["yiduobo的每日leetcode 2249.统计圆内格点数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/geometry", "leetcode/enumeration", "leetcode/sorting", "leetcode/bao-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/546523027"
zhihu_id: "546523027"
zhihu_title: "yiduobo的每日leetcode 2249.统计圆内格点数目"
question_id: "2249"
question: "统计圆内格点数目"
problem_url: "https://leetcode.cn/problems/count-lattice-points-inside-a-circle/"
difficulty: "Medium"
created: "2022-07-27T00:00:29+08:00"
updated: "2022-07-27T00:05:41+08:00"
upvotes: 0
comments: 0
---

# 2249. 统计圆内格点数目

> **[yiduobo的每日leetcode 2249.统计圆内格点数目](https://zhuanlan.zhihu.com/p/546523027) · 知乎 · 2022-07-27 · 赞同 0**
> 力扣：[2249. 统计圆内格点数目](https://leetcode.cn/problems/count-lattice-points-inside-a-circle/) · Medium · 灵茶山艾府：[排序优化 + 枚举所有点](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2249.统计圆内格点数目

[力扣](https://leetcode.cn/problems/count-lattice-points-inside-a-circle/)

由于圆心坐标和半径的最大值都是100，也就是说在圆内个点的横纵坐标最大不超过200，因此可以枚举200\*200这个网格内的所有点，然后判断当前点是否在任意圆中。

当然，也可以进行一点小优化。

对于一个圆(xi, yi, ri)和一条垂直于x轴的直线x \= p，只需要通过解方程就可以求出该直线上位于圆内的各点纵坐标的取值范围。具体来说，就是直线上的点(p, q)需要满足(p - xi) ^ 2 + (q - yi) ^ 2 \<\= ri ^ 2，此时已经确定了除q之外的所有变量的值，那么可以求出一组关于yi对称的q1和q2，在区间[q1, q2]内的q都满足格店(p, q)位于圆(xi, yi, ri)内。

更进一步，如果将每个圆对应的q1和q2都求出来，那么对于位于直线x \= p上的点，只要其纵坐标位于任意圆求出来的区间[q1, q2]中，就说明这个点在对应的圆上。于是此时只需要求出所有关于q的区间上有多少个点就行了。这个问题可以使用排序后区间合并或者差分数组来高效求解。

此时就得到了一种优化后的做法。从0开始向右移动直线x \= p，对于当前的p遍历每个圆，求出对应的q1和q2，然后使用区间合并或者差分数组计算这些q形成的区间中点的总数并累加到答案中。

最后附上python代码：

```python
class Solution(object):
    def countLatticePoints(self, circles):
        """
        :type circles: List[List[int]]
        :rtype: int
        """

        min_x = min_y = 200
        max_x = max_y = 0
        for x, y, r in circles:
            min_x = min(min_x, x - r)
            max_x = max(max_x, x + r)
            min_y = min(min_y, y - r)
            max_y = max(max_y, y + r)

        res = 0
        for p in range(min_x, max_x + 1):
            q_list = [0] * 201
            for x, y, r in circles:
                if x - r <= p <= x + r:
                    delta = int(sqrt(r * r - (x - p) * (x - p)))
                    q1, q2 = y - delta, y + delta
                    q_list[q1] += 1
                    if q2 + 1 <= max_y:
                        q_list[q2 + 1] -= 1
            
            cnt = 0
            for q in range(min_y, max_y + 1):
                cnt += q_list[q]
                if cnt > 0:
                    res += 1
        
        return res
```
