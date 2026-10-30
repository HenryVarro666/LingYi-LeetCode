---
title: "3650. 边反转的最小路径总成本"
aliases: ["yiduobo的每日leetcode 3650.边反转的最小路径总成本"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/shortest-path", "leetcode/heap-priority-queue", "题单/图论算法", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1948194863343436018"
zhihu_id: "1948194863343436018"
zhihu_title: "yiduobo的每日leetcode 3650.边反转的最小路径总成本"
question_id: "3650"
question: "边反转的最小路径总成本"
problem_url: "https://leetcode.cn/problems/minimum-cost-path-with-edge-reversals/"
difficulty: "Medium"
rating: 1854
created: "2025-09-10T22:25:24+08:00"
updated: "2025-09-10T22:25:28+08:00"
upvotes: 0
comments: 0
---

# 3650. 边反转的最小路径总成本

> **[yiduobo的每日leetcode 3650.边反转的最小路径总成本](https://zhuanlan.zhihu.com/p/1948194863343436018) · 知乎 · 2025-09-10 · 赞同 0**
> 力扣：[3650. 边反转的最小路径总成本](https://leetcode.cn/problems/minimum-cost-path-with-edge-reversals/) · Medium · 灵茶山艾府：[Dijkstra 模板题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3650.边反转的最小路径成本

[3650. 边反转的最小路径总成本 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-cost-path-with-edge-reversals/)

题目给出一个包含n个节点的有向带权图，节点编号为0到n - 1。另外给出一个数组edges，其中edges\[index\] \= \[u\[index\], v\[index\], w\[index\]\]，表示一条从u\[index\]到v\[index\]的有向边，其成本为w\[index\]。图中边的权重都为正数。

对于每个节点v[index]，都有一个最多可以使用一次的开关。使用开关后，可以选择一条从u[index]到v[index]的边，以w[index] \* 2的成本从v[index]反向到达u[index]。

问从0到n - 1所需的最小总成本。若无法到达，则返回-1。

如果不考虑开关的情况，那么本题就是一个标准的最短路的问题，使用dijkstra计算0到n - 1的最短距离就行了。接下来对于有开关的情况，由于在最优路径上每个节点也最多经过一次，因此这个开关只能用一次的条件可以直接无视，而使用开关就相当于在原始(u[index], v[index], w[index])的基础上，新建立了一条(v[index], u[index], w[index] \* 2)的边，因此完全可以在一开始建图的时候将这些边都加上，然后再照常执行一次dijkstra，求解0到n - 1的最短路径就行了。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: int
        """
        
        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append((y, w))
            g[y].append((x, w * 2))

        dis = [-1] * n
        heap = [(0, 0)]
        while heap:
            d, now = heapq.heappop(heap)
            if dis[now] != -1:
                continue
            dis[now] = d
            for nxt, w in g[now]:
                if dis[nxt] == -1:
                    heapq.heappush(heap, (d + w, nxt))
                    
        return dis[-1]
```
