---
title: "2473. 购买苹果的最低成本"
aliases: ["yiduobo的每日leetcode 2473.购买苹果的最低成本"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/632277121"
zhihu_id: "632277121"
zhihu_title: "yiduobo的每日leetcode 2473.购买苹果的最低成本"
question_id: "2473"
question: "购买苹果的最低成本"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-buy-apples/"
created: "2023-05-26T01:19:06+08:00"
updated: "2023-05-26T01:19:06+08:00"
upvotes: 0
comments: 0
---

# 2473. 购买苹果的最低成本

> **[yiduobo的每日leetcode 2473.购买苹果的最低成本](https://zhuanlan.zhihu.com/p/632277121) · 知乎 · 2023-05-26 · 赞同 0**
> 力扣：[2473. 购买苹果的最低成本](https://leetcode.cn/problems/minimum-cost-to-buy-apples/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2473.购买苹果的最低成本

[力扣](https://leetcode.cn/problems/minimum-cost-to-buy-apples/)

首先，题目要求一来一回，但是可以走重复的路径，因此来回必然都是走的最短路，在这里就可以直接将图中的所有边先乘以(k + 1)，来代替返回路径的计算。

接下来，除了图中边上的花销外，对于目标终点也有花销。一种常见的处理方法就是将这个点拆开成为两个点，这两个点之间有一条边，权重就是这个点的权重。更进一步的，本题需要在某个节点停止，那么不妨将拆开的点重叠在一起，认为最终都走到了这个重叠的点target。

最后，由于这是无向图，因此a到b的最短路与b到a的最短路必然是同一条。本题要求的是所有点到target的最短距离，不妨反过来求解从target出发到其他所有点的最短距离。

到了这里，使用dijkstra算法跑一趟从target出发到其他节点的最短路即可。

在具体实现上，并不需要真的拆点，而是将target出发到每个节点的边加入到初始的堆中即可，这些边的权重也就是每个节点的点权。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, n, roads, appleCost, k):
        """
        :type n: int
        :type roads: List[List[int]]
        :type appleCost: List[int]
        :type k: int
        :rtype: List[int]
        """

        g = [[] for _ in range(n + 1)]
        for x, y, v in roads:
            g[x].append([y, v * (k + 1)])
            g[y].append([x, v * (k + 1)])
        
        heap = []
        for index in range(n):
            heapq.heappush(heap, [appleCost[index], index + 1])
        
        dis = [None] * (n + 1)
        while heap:
            nowd, now = heapq.heappop(heap)
            if dis[now] is not None:
                continue
            
            dis[now] = nowd
            for next, v in g[now]:
                if dis[next] is None:
                    heapq.heappush(heap, [nowd + v, next])
        
        return dis[1:]
```
