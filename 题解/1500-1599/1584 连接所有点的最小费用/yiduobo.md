---
title: "1584. 连接所有点的最小费用"
aliases: ["yiduobo的每日leetcode 1584.连接所有点的最小费用"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/430438947"
zhihu_id: "430438947"
zhihu_title: "yiduobo的每日leetcode 1584.连接所有点的最小费用"
question_id: "1584"
question: "连接所有点的最小费用"
problem_url: "https://leetcode.cn/problems/min-cost-to-connect-all-points/"
created: "2021-11-07T14:56:25+08:00"
updated: "2021-11-07T14:56:25+08:00"
upvotes: 0
comments: 0
---

# 1584. 连接所有点的最小费用

> **[yiduobo的每日leetcode 1584.连接所有点的最小费用](https://zhuanlan.zhihu.com/p/430438947) · 知乎 · 2021-11-07 · 赞同 0**
> 力扣：[1584. 连接所有点的最小费用](https://leetcode.cn/problems/min-cost-to-connect-all-points/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1584.连接所有点的最小费用

[力扣](https://leetcode-cn.com/problems/min-cost-to-connect-all-points/)

又是最小生成树的问题。由于题目中的点数规模不大，因此可以直接两两枚举点对，计算距离形成边，这样一来边的规模就是O(n^2)。得到边之后，使用kurskal算法求解最小生成树即可，最终的时间复杂度就是O(n^2 \* logn)。

另外，这里二维平面上的曼哈顿距离应该可以使用一些计算几何知识来优化掉很多没用的边，简单举例，三个点形成的三角形中，最长边显然是用不上的。我在这里没有想到高效的选边方法，就没有做相应的优化了。

最后附上python代码：

```python
class Solution(object):
    def minCostConnectPoints(self, points):
        """
        :type points: List[List[int]]
        :rtype: int
        """

        n = len(points)
        edges = []
        for i in range(n - 1):
            for j in range(i + 1, n):
                edges.append([i, j, abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])])
        
        fa = range(n)
        res = 0
        for x, y, l in sorted(edges, key=lambda d:d[2]):
            fa_x = self.find(x, fa)
            fa_y = self.find(y, fa)
            if fa_x != fa_y:
                if fa_x < fa_y:
                    fa[fa_y] = fa_x
                else:
                    fa[fa_x] = fa_y
                res += l
        
        return res

    def find(self, now, fa):
        if fa[now] != now:
            fa[now] = self.find(fa[now], fa)
        return fa[now]
```
