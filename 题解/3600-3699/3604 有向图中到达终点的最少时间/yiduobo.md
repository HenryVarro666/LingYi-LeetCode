---
title: "3604. 有向图中到达终点的最少时间"
aliases: ["yiduobo的每日leetcode 3604.有向图中到达终点的最少时间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/shortest-path", "leetcode/heap-priority-queue", "题单/图论算法", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1942057591787226172"
zhihu_id: "1942057591787226172"
zhihu_title: "yiduobo的每日leetcode 3604.有向图中到达终点的最少时间"
question_id: "3604"
question: "有向图中到达终点的最少时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-reach-destination-in-directed-graph/"
difficulty: "Medium"
rating: 1845
created: "2025-08-22T04:15:28+08:00"
updated: "2025-08-22T04:15:28+08:00"
upvotes: 0
comments: 0
---

# 3604. 有向图中到达终点的最少时间

> **[yiduobo的每日leetcode 3604.有向图中到达终点的最少时间](https://zhuanlan.zhihu.com/p/1942057591787226172) · 知乎 · 2025-08-22 · 赞同 0**
> 力扣：[3604. 有向图中到达终点的最少时间](https://leetcode.cn/problems/minimum-time-to-reach-destination-in-directed-graph/) · Medium · 灵茶山艾府：[Dijkstra 求最短路（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3604.有向图中到达终点的最少时间

[3604. 有向图中到达终点的最少时间 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-time-to-reach-destination-in-directed-graph/description/)

题目给出一个整数n以及一张有向图，图中有n个节点，编号从0到n - 1。图由一个二维数组edges表示，其中edges\[index\] \= \[u\[index\], v\[index\], start\[index\], end\[index\]\]，表示从节点u\[index\]到v\[index\]的一条边，这条边只在时刻start\[index\]到end\[index\]之间开放。

现在要求从时刻0从节点0出发，在一个时间单位内，可以在原地挂机，也可以通过一条开放的边沿出边方向到达另一个节点。问到达n - 1所需的最小时间。若无法到达，则返回-1。

最短路问题的变种，依然可以使用dijkstra算法求解，不过在距离的更新上略有不同。对于堆顶节点now，若到达now的最短时间为d，那么在使用now更新到达其他从未到达过的相邻节点的最短时间时，若对应边还未开放，那么就必须等到这条边开放然后再走，对应的时间为开放时间start再加上1；若对应边已经开放，那么就直接走过去，对应的时间为d + 1；若对应边已经关闭，那么就不能走了，只能跳过这个节点。

计算完成后，到达n - 1的最短时间即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minTime(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: int
        """
        
        g = [[] for _ in range(n)]
        for u, v, start, end in edges:
            g[u].append((v, start, end))
        dis = [None] * n

        heap = [(0, 0)]
        while heap:
            d, now = heapq.heappop(heap)
            if dis[now] is None:
                dis[now] = d
                for v, start, end in g[now]:
                    if start > d:
                        heapq.heappush(heap, (start + 1, v))
                    elif start <= d <= end:
                        heapq.heappush(heap, (d + 1, v))

        if dis[-1] is None:
            return -1
        return dis[-1]
```
