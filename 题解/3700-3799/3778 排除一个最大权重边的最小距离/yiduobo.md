---
title: "3778. 排除一个最大权重边的最小距离"
aliases: ["yiduobo的每日leetcode 3778.排除一个最大权重边的最小距离"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1986177836940280707"
zhihu_id: "1986177836940280707"
zhihu_title: "yiduobo的每日leetcode 3778.排除一个最大权重边的最小距离"
question_id: "3778"
question: "排除一个最大权重边的最小距离"
problem_url: "https://leetcode.cn/problems/minimum-distance-excluding-one-maximum-weighted-edge/"
created: "2025-12-21T22:56:30+08:00"
updated: "2025-12-21T22:56:31+08:00"
upvotes: 0
comments: 0
---

# 3778. 排除一个最大权重边的最小距离

> **[yiduobo的每日leetcode 3778.排除一个最大权重边的最小距离](https://zhuanlan.zhihu.com/p/1986177836940280707) · 知乎 · 2025-12-21 · 赞同 0**
> 力扣：[3778. 排除一个最大权重边的最小距离](https://leetcode.cn/problems/minimum-distance-excluding-one-maximum-weighted-edge/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3778.排除一个最大权重边的最小距离

[3778. 排除一个最大权重边的最小距离 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-distance-excluding-one-maximum-weighted-edge/description/)

题目给出一个正整数n，表示有一个带权连通简单无向图，其中包含n个节点，下标从0到n - 1编号。

另外给出一个二维整数数组edges，其中edges\[index\] \= \[u\[index\], v\[index\], w\[index\]\]，表示u\[index\]到v\[index\]有一条正权边w\[index\]。

路径的开销指的是路径中所有边的权重之和，再减去其中的最大边权。若存在多有最大边权，只减一次。

问0到n - 1的最小开销。

经典的分层图最短路问题。对于题目中给出的图，可以先在平面上画出来，然后想象将这张图原封不动复制一份，放到上面，也就是现在有上下两层图。接下来，对于原图中的每条边[u, v, w]，都建立从下层图的u到上层图的v，权重为w的有向边，以及下层图的v到上层图的u，权重为w的有向边。

这样一来，问题就转化成了从下层图的0号节点走到上层图的n - 1号节点的最短路了，而这条最短路径上必然有且仅有条从下层图到上层图的路径，这条路径对应的就是那条被减去边权的路径。

值得一提的是，题目在这里的要求是减去最大的边权，而对于以上的建图方式，并不能保证这条跨层的边在路径中权重最大。不过由于计算的是最短路径，那么最终答案对应的路径中，跨层的这条边一定是边权最大的。理由是如果其不是最大的，那么对于当前得到的最短路径，将跨层边修改成路径中边权最大的边，然后将原路径的跨层边以及新的跨层边之间其他的边从当前的层迁移到另一层，就可以得到另一条从0到n - 1的路径。这条路径与原路径只有跨层边的边权有区别，而新路径的路径和明显更小，与之前的假设矛盾了。

基于上面的结论，只需建立分层图然后在图上跑一趟dijkstra就行了。

在具体实现上，并不需要真的建图，而是只需要使用一个状态标记level表示目前处于哪一层就行了。

最后附上python代码：

```python
class Solution(object):
    def minCostExcludingMax(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: int
        """
        
        dis = [[None] * 2 for _ in range(n)]
        heap = [(0, 0, 0)]

        g = [{} for _ in range(n)]
        for x, y, w in edges:
            g[x][y] = w
            g[y][x] = w
        
        while heap:
            d, x, level = heapq.heappop(heap)
            if dis[x][level] is not None:
                continue
            dis[x][level] = d
            for y in g[x]:
                nxt_d = d + g[x][y]
                if dis[y][level] is None:
                    heapq.heappush(heap, (nxt_d, y, level))
                if level == 0 and dis[y][level + 1] is None:
                    heapq.heappush(heap, (d, y, level + 1))
        
        return dis[-1][1]
```
