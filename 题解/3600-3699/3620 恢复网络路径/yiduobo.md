---
title: "3620. 恢复网络路径"
aliases: ["yiduobo的每日leetcode 3620.恢复网络路径"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/topological-sort", "leetcode/recursion", "leetcode/memoization", "leetcode/queue", "leetcode/binary-search", "leetcode/dynamic-programming", "题单/二分算法", "题单/动态规划", "题单/图论算法", "题单/二分算法/二-二分答案", "题单/动态规划/十三-图-DP", "题单/图论算法/二-拓扑排序"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1944522591659336141"
zhihu_id: "1944522591659336141"
zhihu_title: "yiduobo的每日leetcode 3620.恢复网络路径"
question_id: "3620"
question: "恢复网络路径"
problem_url: "https://leetcode.cn/problems/network-recovery-pathways/"
difficulty: "Hard"
rating: 1998
created: "2025-08-28T22:25:56+08:00"
updated: "2025-08-28T22:25:56+08:00"
upvotes: 0
comments: 0
---

# 3620. 恢复网络路径

> **[yiduobo的每日leetcode 3620.恢复网络路径](https://zhuanlan.zhihu.com/p/1944522591659336141) · 知乎 · 2025-08-28 · 赞同 0**
> 力扣：[3620. 恢复网络路径](https://leetcode.cn/problems/network-recovery-pathways/) · Hard · 灵茶山艾府：[二分答案 + DAG DP / 拓扑排序（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3620.恢复网络路径

<https://leetcode.cn/problems/network-recovery-pathways/description/>

题目给出一个包含n个节点的有向无环图，图中的节点从0到n - 1编号。另外给出一个长度为m的二维数组edges，其中edges\[index\] \= \[u\[index\], v\[index\], cost\[index\]\]，表示从u\[index\]到v\[index\]的单向通信，恢复成本为cost\[index\]。

一些节点可能处于离线状态，给出一个布尔数组online，其中online[index] \= true表示节点index在线。节点0和n - 1始终在线。

对于一条从0到n - 1的路径，如果这条路径上的所有节点都在线，同时这条路径上所有边的总恢复成本不超过k，那么就称这条路径是有效的，这条路径的分数定义为路径上的最小边成本。

要求找出所有有效路径中的最大路径成本，即最大的最小边成本。若不存在有效路径，则返回-1。

如果最大的最小边成本越小，那么可用的边就越多，存在有效路径的可能性就越大，因此在这里可以二分这个最大的最小边成本mid，然后检测如果只使用cost大于等于mid的边时是否存在有效路径。可以发现，实际上就是给出一张有向图，问0到n - 1的最短路长度是否小于等于k，对于这个问题，只需从0开始执行一趟dijkstra就行了。

在具体实现时，不需要真的将不可用的边去掉，而是在执行dijkstra时只选择符合条件的边更新距离即可。

最后附上python代码：

```python
class Solution(object):
    def findMaxPathScore(self, edges, online, k):
        """
        :type edges: List[List[int]]
        :type online: List[bool]
        :type k: int
        :rtype: int
        """
        
        left = -1
        right = k
        n = len(online)
        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append((y, w))

        while left < right:
            mid = (left + right + 1) // 2
            dis = [k + 1] * n

            heap = [(0, 0)]
            dis[0] = 0
            while heap:
                now, d = heapq.heappop(heap)
                if d > dis[now]:
                    continue
                for nxt, w in g[now]:
                    if online[nxt] and w >= mid and dis[nxt] > dis[now] + w:
                        dis[nxt] = dis[now] + w
                        heapq.heappush(heap, (nxt, dis[nxt]))

            if dis[-1] <= k:
                left = mid
            else:
                right = mid - 1
        
        return left
```
