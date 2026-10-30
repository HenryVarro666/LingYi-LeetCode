---
title: "3123. 最短路径中的边"
aliases: ["yiduobo的每日leetcode 3123.最短路径中的边"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/breadth-first-search", "leetcode/queue", "leetcode/shortest-path", "leetcode/heap-priority-queue", "题单/图论算法", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/701866392"
zhihu_id: "701866392"
zhihu_title: "yiduobo的每日leetcode 3123.最短路径中的边"
question_id: "3123"
question: "最短路径中的边"
problem_url: "https://leetcode.cn/problems/find-edges-in-shortest-paths/"
difficulty: "Hard"
rating: 2093
created: "2024-06-05T22:21:20+08:00"
updated: "2024-06-05T22:21:20+08:00"
upvotes: 1
comments: 0
---

# 3123. 最短路径中的边

> **[yiduobo的每日leetcode 3123.最短路径中的边](https://zhuanlan.zhihu.com/p/701866392) · 知乎 · 2024-06-05 · 赞同 1**
> 力扣：[3123. 最短路径中的边](https://leetcode.cn/problems/find-edges-in-shortest-paths/) · Hard · 灵茶山艾府：[Dijkstra 最短路 + DFS/BFS 找边（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3123.最短路径中的边

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-edges-in-shortest-paths/description/)

题目给出一张节点编号在0到n - 1之间的正权无向图，要求检测图中的每条边是否属于某条0到n - 1的最短路径上。

由于从0到n - 1的最短路径长度是固定的，那么对于图中的某条边(x, y, w)，如果其处于某条最短路径上，那么这条最短路径的构成必然是以下两种情况之一：

1、从0到x，经过(x, y, w)，然后从y到n - 1

2、从0到y，经过(x, y, w)，然后从x到n - 1

根据上面这个结论，就可以先通过两次dijkstra算法计算从0到图中其他节点的最短距离，以及从n - 1到图中其他节点的最短距离。接下来枚举图中的所有边，检测是否满足上面两种情况之一即可。

最后附上python代码：

```python
class Solution(object):
    def findAnswer(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: List[bool]
        """

        g = {index : {} for index in range(n)}
        for x, y, w in edges:
            g[x][y] = g[y][x] = w

        def dijkstra(start):
            dis = [-1] * n
            heap = [[0, start]]
            while heap:
                d, x = heapq.heappop(heap)
                if dis[x] == -1:
                    dis[x] = d
                    for y, w in g[x].items():
                        if dis[y] == -1:
                            heapq.heappush(heap, [d + w, y])
            
            return dis
        
        dis_start = dijkstra(0)
        dis_end = dijkstra(n - 1)

        res = [False] * len(edges)
        for index, (x, y, w) in enumerate(edges):
            if dis_start[x] != -1 and dis_end[y] != -1 and dis_start[x] + dis_end[y] + w == dis_start[-1]:
                res[index] = True
            if dis_start[y] != -1 and dis_end[x] != -1 and dis_start[y] + dis_end[x] + w == dis_start[-1]:
                res[index] = True
    
        return res
```
