---
title: "1928. 规定时间内到达终点的最小花费"
aliases: ["yiduobo的每日leetcode 1928.规定时间内到达终点的最小花费"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/487010644"
zhihu_id: "487010644"
zhihu_title: "yiduobo的每日leetcode 1928.规定时间内到达终点的最小花费"
question_id: "1928"
question: "规定时间内到达终点的最小花费"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-reach-destination-in-time/"
created: "2022-03-24T21:37:13+08:00"
updated: "2022-03-24T21:37:13+08:00"
upvotes: 0
comments: 0
---

# 1928. 规定时间内到达终点的最小花费

> **[yiduobo的每日leetcode 1928.规定时间内到达终点的最小花费](https://zhuanlan.zhihu.com/p/487010644) · 知乎 · 2022-03-24 · 赞同 0**
> 力扣：[1928. 规定时间内到达终点的最小花费](https://leetcode.cn/problems/minimum-cost-to-reach-destination-in-time/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1928.规定时间内到达终点的最小花费

[力扣](https://leetcode-cn.com/problems/minimum-cost-to-reach-destination-in-time/)

题目给出一张无向图，要求从起点出发，在规定时间内到达终点，且到达终点时的花费最小。与常规的最短路问题不同，这里有时间、花费两个因素需要考虑，因此不能直接使用一般的最短路算法。

由于题目最终还是要求花费最小，而时间只需要在规定范围之内，那么一个自然的想法就是将时间变成参数。令f[i][j]表示在时刻i恰好到达节点j所需的最小花费。对于f[i][j]，可以枚举与j相邻的所有节点k，那么就有

f\[i\]\[j\] \= min(f\[i\]\[j\], f\[i - time_cost\[j\]\[k\]\]\[k\] + passingFees\[j\])

初始状态下，位于节点0，花费为passingFees[j]，所以初始状态就是f[0][0] \= passingFees[0]。接下来只需要从1到maxTime枚举i，然后对每个i枚举所有城市j，并计算对应的f[i][j]即可。

当然，上面这个计算过程中可能会枚举到很多根本不可能出现的f[i][j]，而由于题目图中的边权都是正数，那么就必然不会出现f[i][j]通过f[i][k]转移过来的这种情况。换言之，在计算所有的f时只需要严格保证是按i这一维，也就是时间从小到大计算过来的就行了。

有了这个结论，就可以省去i这一维，直接用f[j]表示在规定时间内到达j的最小花费。而为了保证时间是从小到大计算的，那么可以使用类似dijkstra + SPFA的做法来进行状态转移：

每次都对距离最近的点计算f，为了满足最近这个需求，自然是使用一个堆来维护当前可计算的节点。

对于当前堆顶的节点，如果其花销大于当前的f，那么就没必要再对这个节点进行处理，否则无论其相邻节点是否被计算过，都需要使用当前堆顶节点更新相邻节点的花销，然后将相邻的节点以及其对应的花销再次加入到堆中。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, maxTime, edges, passingFees):
        """
        :type maxTime: int
        :type edges: List[List[int]]
        :type passingFees: List[int]
        :rtype: int
        """

        n = len(passingFees)
        cost = [-1] * n
        heap = [[0, 0, passingFees[0]]]
        g = {x : {} for x in range(n)}
        for x, y, t in edges:
            if t <= maxTime:
                if y not in g[x]:
                    g[x][y] = g[y][x] = t
                else:
                    g[x][y] = min(g[x][y], t)
                    g[y][x] = min(g[y][x], t)

        while heap:
            t, now, c = heapq.heappop(heap)
            if cost[now] != -1 and c >= cost[now]:
                continue
            
            cost[now] = c

            for next in g[now]:
                if t + g[now][next] <= maxTime and ((cost[next] == -1) or (c + passingFees[next] < cost[next])):
                    heapq.heappush(heap, [t + g[now][next], next, c + passingFees[next]])

        return cost[-1]
```
