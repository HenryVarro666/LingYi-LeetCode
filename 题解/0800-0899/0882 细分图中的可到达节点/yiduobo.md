---
title: "882. 细分图中的可到达结点"
aliases: ["yiduobo的每日leetcode 882.细分图中的可到达结点"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/graph", "leetcode/shortest-path", "leetcode/heap-priority-queue", "题单/图论算法", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/351336447"
zhihu_id: "351336447"
zhihu_title: "yiduobo的每日leetcode 882.细分图中的可到达结点"
question_id: "882"
question: "细分图中的可到达节点"
problem_url: "https://leetcode.cn/problems/reachable-nodes-in-subdivided-graph/"
difficulty: "Hard"
rating: 2328
created: "2021-02-19T00:07:29+08:00"
updated: "2021-02-19T00:07:29+08:00"
upvotes: 0
comments: 0
---

# 882. 细分图中的可到达结点

> **[yiduobo的每日leetcode 882.细分图中的可到达结点](https://zhuanlan.zhihu.com/p/351336447) · 知乎 · 2021-02-19 · 赞同 0**
> 力扣：[882. 细分图中的可到达节点](https://leetcode.cn/problems/reachable-nodes-in-subdivided-graph/) · Hard · 灵茶山艾府：[【图解】转换成单源最短路问题，附题单（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

882.细分图中的可到达结点

[力扣](https://leetcode-cn.com/problems/reachable-nodes-in-subdivided-graph/)

对于图中的原始节点，可以将细分边的细分节点数量视为边长，那么此时执行一次单源最短路就可以得到从0出发到达图中原始节点的移动次数，从而得到是否可以到达图中的原始节点。那么此时还需要解决的问题就是如何判断能否到达一条边上的细分点。

对于一条边[u, v, cnt]而言，其中的细分点要么是从0开始走到u，然后再走到细分点，要么就是从0开始走到v，然后再走到细分点。于是我们可以利用上面步骤的结论，设0到u和v的距离为dis[u]以及dis[v]，接下来就可以讨论dis[u]、dis[v]以及maxMoves的大小关系：

这里以u为例：

1-1、若maxMoves \< dis[u]，说明根本就达到不了节点u，因此也不可能从0出发走到u然后再走到uv上的细分点

1-2、若maxMoves >\= dis[u] + cnt，说明此时可以从0出发走到u，然后再完整地走完uv这条边，因此uv上的所有细分点都可以走到

1-3、若maxMoves >\= dis[u]，但maxMoves \< dis[u] + cnt，说明此时可以从0出发走到u，但是只能再从u开始往v走maxMoves - dis[u]个细分点

对于v也是同样的处理逻辑。综合u和v的结论：

2-1、若u满足1-2或v满足1-2，那么uv上的所有细分点都可以到达，此时应该将答案加上cnt

2-2、若对于u和v而言都满足1-1，那么uv上任何细分点都无法到达

2-3、若u满足1-1，v满足1-3，那么将答案加上maxMoves - dis[v]

2-4、若v满足1-1，u满足1-3，那么将答案加上maxMoves - dis[u]

2-5、若u和v都满足1-3，那么将答案加上(maxMoves - dis[u]) + (maxMoves - dis[v])。不过此时需要一种特殊情况，即二者之和大于cnt，此时说明uv这条边可以被完全覆盖住，但是其中仅有cnt个细分点，因此答案应该只加上cnt。

在实现中，我采用的是带二叉堆的dijkstra算法来计算原始图的单源最短路。

最后附上python代码：

```python
class Solution(object):
    def reachableNodes(self, edges, maxMoves, n):
        """
        :type edges: List[List[int]]
        :type maxMoves: int
        :type n: int
        :rtype: int
        """
        
        g = {index : {} for index in range(n)}
        for u, v, w in edges:
            g[u][v] = w + 1
            g[v][u] = w + 1
        
        dis = [maxMoves + 1] * n
        heap = [[0, 0]]
        used = set()
        while heap and heap[0][0] <= maxMoves:
            now_dis, now = heapq.heappop(heap)
            if now not in used:
                used.add(now)
                dis[now] = now_dis
                for next in g[now]:
                    if next not in used:
                        heapq.heappush(heap, [g[now][next] + now_dis, next])
        
        res = 0
        for index in range(n):
            if dis[index] <= maxMoves:
               res += 1
            else:
                dis[index] = maxMoves

        for u, v, w in edges:
            if maxMoves - min(dis[u], dis[v]) >= w:
                res += w
            else:
                res += min(maxMoves - dis[u] + maxMoves - dis[v], w)
        
        return res
```
