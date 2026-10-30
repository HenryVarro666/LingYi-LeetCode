---
title: "1786. 从第一个节点出发到最后一个节点的受限路径数"
aliases: ["yiduobo的每日leetcode 1786.从第一个节点出发到最后一个节点的受限路径数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/463061326"
zhihu_id: "463061326"
zhihu_title: "yiduobo的每日leetcode 1786.从第一个节点出发到最后一个节点的受限路径数"
question_id: "1786"
question: "从第一个节点出发到最后一个节点的受限路径数"
problem_url: "https://leetcode.cn/problems/number-of-restricted-paths-from-first-to-last-node/"
created: "2022-01-29T22:03:03+08:00"
updated: "2022-01-29T22:03:04+08:00"
upvotes: 0
comments: 0
---

# 1786. 从第一个节点出发到最后一个节点的受限路径数

> **[yiduobo的每日leetcode 1786.从第一个节点出发到最后一个节点的受限路径数](https://zhuanlan.zhihu.com/p/463061326) · 知乎 · 2022-01-29 · 赞同 0**
> 力扣：[1786. 从第一个节点出发到最后一个节点的受限路径数](https://leetcode.cn/problems/number-of-restricted-paths-from-first-to-last-node/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1786.从第一个节点出发到最后一个节点的受限路径数

[力扣](https://leetcode-cn.com/problems/number-of-restricted-paths-from-first-to-last-node/)

题目中合法路径要求路径中的点必须满足与节点n的距离越来越近，那么在这里可以先通过dijkstra算法计算出n到各个节点的距离，然后从n开始进行拓扑排序，优先处理离n较近的节点，并在这个过程中通过动态规划计算出从每个点出发到n的首先路径数。

具体来说，拓扑图的建图需要在dijkstra算法中完成，而具体的时机就是每次从边的堆中取出带来最短距离的边时，若边两侧的节点满足当前节点与n的距离大于前置节点与n的距离，或者当前节点与n的距离还未被计算出来，那么就说明这条边是拓扑图中的一条边，且边的方向是从前置节点指向当前节点。在这里无需重新建图，只需要记录每个节点在拓扑图中的入度。

dijkstra算法完成后，现在就得到了拓扑图中各个节点的入度，接下来就可以从n开始进行拓扑排序。对于当前节点now，令f[now]表示从now出发到n的受限路径数目。此时应该遍历原图中与now相连的所有边，若边的另一侧next满足dis[next] > dis[now]，说明当前边属于拓扑图，那么此时应该使用f[now]去更新f[next]，同时将next的入度减去1。当next的入度为0时，则将其加入拓扑排序的队列中。

拓扑排序完成后，f[0]就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def countRestrictedPaths(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: int
        """

        g = {}
        for x, y, w in edges:
            x -= 1
            y -= 1
            if x not in g:
                g[x] = {}
            if y not in g:
                g[y] = {}
            g[x][y] = g[y][x] = w

        heap = [[0, n - 1, None]]
        dis = [None] * n
        ind = [0] * n
        f = [0] * n
        mod = 10 ** 9 + 7
        while heap:
            d, now, prev = heapq.heappop(heap)
            if dis[now] is not None:
                if prev is not None and dis[now] > dis[prev]:
                    ind[now] += 1
            else:
                dis[now] = d
                if prev is not None:
                    ind[now] += 1
                for next, w in g.get(now, {}).items():
                    if dis[next] is None or dis[next] >= d + w:
                        heapq.heappush(heap, [d + w, next, now])

        
        q = [n - 1]
        f[n - 1] = 1
        l = 0
        r = 1
        while l < r:
            now = q[l]
            l += 1
            for next in g.get(now, {}):
                if dis[next] > dis[now]:
                    f[next] += f[now]
                    if f[next] >= mod:
                        f[next] -= mod
                    
                    ind[next] -= 1
                    if ind[next] == 0:
                        q.append(next)
                        r += 1
        
        return f[0]
```
