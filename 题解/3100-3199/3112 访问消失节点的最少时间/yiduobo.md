---
title: "3112. 访问消失节点的最少时间"
aliases: ["yiduobo的每日leetcode 3112.访问消失节点的最少时间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/shortest-path", "leetcode/heap-priority-queue", "题单/图论算法", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/701026134"
zhihu_id: "701026134"
zhihu_title: "yiduobo的每日leetcode 3112.访问消失节点的最少时间"
question_id: "3112"
question: "访问消失节点的最少时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-visit-disappearing-nodes/"
difficulty: "Medium"
rating: 1757
created: "2024-06-01T01:45:50+08:00"
updated: "2024-06-01T01:45:50+08:00"
upvotes: 0
comments: 0
---

# 3112. 访问消失节点的最少时间

> **[yiduobo的每日leetcode 3112.访问消失节点的最少时间](https://zhuanlan.zhihu.com/p/701026134) · 知乎 · 2024-06-01 · 赞同 0**
> 力扣：[3112. 访问消失节点的最少时间](https://leetcode.cn/problems/minimum-time-to-visit-disappearing-nodes/) · Medium · 灵茶山艾府：[Dijkstra 算法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3112.访问消失节点的最少时间

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-time-to-visit-disappearing-nodes/description/)

题目给出一张节点编号为0到n - 1的正权无向图，边权代表从一个节点到达另一个节点所需的时间。其中每个节点在某个时刻后再也无法访问，现在问从0号节点出发到其他节点的最短时间是多少。

对于正权图上的单源最短路问题，自然想到使用dijkstra，但是在这里有一个节点过时就无法访问的机制，所以需要进行某些调整。一个直观的思路就是对于某个节点，如果到达该节点的最短时间大于等于其无法访问的时间，那么就置其为无法访问，同时也不再通过到达该节点的最短时间去更新到达剩下节点的最短时间。由于无效节点不会更新其他节点的最短路径，同时dijkstra是从近到远更新的，因此这样就能保证到达目标节点的路径上的所有节点在通过的时刻依然是有效的。

最后附上python代码：

```python
class Solution(object):
    def minimumTime(self, n, edges, disappear):
        """
        :type n: int
        :type edges: List[List[int]]
        :type disappear: List[int]
        :rtype: List[int]
        """

        g = [{} for _ in range(n)]
        for x, y, w in edges:
            if y not in g[x] or g[x][y] > w:
                g[x][y] = g[y][x] = w
        
        dis = [-1] * n
        heap = [[0, 0]]
        while heap:
            d, x = heapq.heappop(heap)
            if dis[x] == -1:
                dis[x] = d
                for y, w in g[x].items():
                    if dis[y] == -1 and dis[x] + w < disappear[y]:
                        heapq.heappush(heap, [dis[x] + w, y])
        
        return dis
```
