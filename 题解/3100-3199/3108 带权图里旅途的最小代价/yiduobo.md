---
title: "3108. 带权图里旅途的最小代价"
aliases: ["yiduobo的每日leetcode 3108.带权图里旅途的最小代价"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/union-find", "leetcode/recursion", "题单/位运算", "题单/图论算法", "题单/位运算/三-与或-AND/OR-的性质", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/700601833"
zhihu_id: "700601833"
zhihu_title: "yiduobo的每日leetcode 3108.带权图里旅途的最小代价"
question_id: "3108"
question: "带权图里旅途的最小代价"
problem_url: "https://leetcode.cn/problems/minimum-cost-walk-in-weighted-graph/"
difficulty: "Hard"
rating: 2109
created: "2024-05-29T23:28:01+08:00"
updated: "2024-05-29T23:28:01+08:00"
upvotes: 0
comments: 0
---

# 3108. 带权图里旅途的最小代价

> **[yiduobo的每日leetcode 3108.带权图里旅途的最小代价](https://zhuanlan.zhihu.com/p/700601833) · 知乎 · 2024-05-29 · 赞同 0**
> 力扣：[3108. 带权图里旅途的最小代价](https://leetcode.cn/problems/minimum-cost-walk-in-weighted-graph/) · Hard · 灵茶山艾府：[两种方法：DFS / 并查集（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3108.带权图里旅途的最小代价

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-cost-walk-in-weighted-graph/description/)

题目给出一张带权无向图以及若干询问，每个询问都是查询从一个点出发走到另一个点的路径最小代价。在这里的路径可以经过同一个点或者同一条边多次，且代价的计算方式是经过的所有边的按位与结果。

首先注意到代价的计算方式是所有边的按位与，同时要计算的又是最小的代价，换言之，在这里经过的边是越多越好的。另一方面，由于路径可以经过同一个点或者同一条边多次，那么如果询问中的两点属于同一个连通子图，那么就应该走遍这张子图中的所有边，这样一来才能使得路径的代价最小。

根据上面的结论，就可以先对所有节点进行一趟遍历，若当前节点没有被访问过，那么就从当前节点开始进行bfs，找出其所属的连通子图以及子图中的其他节点。

遍历完成后，再对所有边进行一趟遍历，将其权重按位与到其所属连通子图的最小代价中。

最后再遍历所有询问，若询问的节点属于同一连通子图，那么最小代价就是其所属连通子图的最小代价；若不属于同一连通子图，那么对应的答案就是-1。

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, n, edges, query):
        """
        :type n: int
        :type edges: List[List[int]]
        :type query: List[List[int]]
        :rtype: List[int]
        """

        g = [set() for index in range(n)]
        for x, y, w in edges:
            g[x].add(y)
            g[y].add(x)
        
        belong = [None] * n
        tot = 0
        for index in range(n):
            if belong[index] is None:
                belong[index] = tot
                q = [index]
                head, tail = 0, 1
                while head < tail:
                    for x in q[head : tail]:
                        for y in g[x]:
                            if belong[y] is None:
                                belong[y] = tot
                                q.append(y)

                    head, tail = tail, len(q)
                
                tot += 1
        
        val = [None] * tot
        for x, y, w in edges:
            if val[belong[x]] is None:
                val[belong[x]] = w
            else:
                val[belong[x]] &= w
        
        res = []
        for x, y in query:
            if belong[x] != belong[y]:
                res.append(-1)
            else:
                res.append(val[belong[x]])
        
        return res
```
