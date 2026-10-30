---
title: "3970. 最多K个连续相同字符的最短路径"
aliases: ["yiduobo的每日leetcode 3970.最多K个连续相同字符的最短路径"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/shortest-path", "leetcode/heap-priority-queue", "题单/图论算法", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2053247366791271596"
zhihu_id: "2053247366791271596"
zhihu_title: "yiduobo的每日leetcode 3970.最多K个连续相同字符的最短路径"
question_id: "3970"
question: "最多 K 个连续相同字符的最短路径"
problem_url: "https://leetcode.cn/problems/shortest-path-with-at-most-k-consecutive-identical-characters/"
difficulty: "Medium"
rating: 1840
created: "2026-06-25T21:40:21+08:00"
updated: "2026-06-25T21:40:26+08:00"
upvotes: 3
comments: 0
---

# 3970. 最多K个连续相同字符的最短路径

> **[yiduobo的每日leetcode 3970.最多K个连续相同字符的最短路径](https://zhuanlan.zhihu.com/p/2053247366791271596) · 知乎 · 2026-06-25 · 赞同 3**
> 力扣：[3970. 最多 K 个连续相同字符的最短路径](https://leetcode.cn/problems/shortest-path-with-at-most-k-consecutive-identical-characters/) · Medium · 灵茶山艾府：[Dijkstra 算法（分层图最短路）Python/Java/C++/Go](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3970.最多K个连续相同字符的最短路径

<https://leetcode.cn/problems/shortest-path-with-at-most-k-consecutive-identical-characters/description/>

题目给出一个整数n，表示一个有向加权图中的节点数目，节点编号从0到n - 1。这张图由二维数组edges表示，其中edges\[index\] \= \[u\[index\], v\[index\], w\[index\]\]，表示一条从u\[index\]指向v\[index\]，权重为w\[index\]的边。保证所有的权重都大于0。

另外给出一个长度为n的字符串labels，其中labels[index]是分配给节点index的字符，以及一个整数k，这里的k不超过50。

要求找出一条从0到n - 1的最短路径，这条路径上所有节点按labels拼接后，最多包含k个连续相同字符。若不存在合法的路径，则返回-1。

非常标准的分层图最短路问题。

对于本题最多连续k个相同字符的限制，可以通过构造一张k层的图来解决。

具体来说，对于原图中u到v的一条边，若u和v对应的label相同，那么在分层图中，u就要指向下一层的v，若u位于第k层，则不发出到v的边；反之，若u和v的label不同，那么u就指向第一层的v。这样一来，图中的路径必然是从第一层到某一层，然后回到第一层的循环，这些路径最多只能到第k层，也就是说连续相同字符最多出现k次。

题目需要计算从0到n - 1的最短路径，那么在分层图中从第一层的0号节点开始做一趟dijkstra即可。

在具体实现上，并不需要把图构造出来，而是使用一个二维的距离数组dis，其中dis[x][cnt]表示到达第cnt层的节点x的最短路径，那么对于x指向的y，若二者label相同，那么目的地就是下一层的y，即nxt_cnt \= cnt + 1，否则就是第一层的y，即cnt \= 1。若nxt_cnt不超过k，且第nxt_cnt层的y还没被访问过，就将其加入到堆中。

最后附上python代码：

```python
class Solution(object):
    def shortestPath(self, n, edges, labels, k):
        """
        :type n: int
        :type edges: List[List[int]]
        :type labels: str
        :type k: int
        :rtype: int
        """
        
        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append((y, w))
        
        heap = [(0, 0, 1)]
        dis = [[None] * (k + 1) for _ in range(n)]

        while heap:
            d, x, cnt = heapq.heappop(heap)
            if dis[x][cnt] is None:
                dis[x][cnt] = d
                for y, w in g[x]:
                    nxt_cnt = cnt
                    if labels[x] == labels[y]:
                        nxt_cnt += 1
                    else:
                        nxt_cnt = 1
                    
                    if nxt_cnt <= k and dis[y][nxt_cnt] is None:
                        heapq.heappush(heap, (d + w, y, nxt_cnt))
        
        res = -1
        for cnt in range(1, k + 1):
            if dis[-1][cnt] is not None and (res == -1 or res > dis[-1][cnt]):
                res = dis[-1][cnt]
        return res
```
