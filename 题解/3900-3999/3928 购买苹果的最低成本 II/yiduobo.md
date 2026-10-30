---
title: "3928. 购买苹果的最低成本II"
aliases: ["yiduobo的每日leetcode 3928.购买苹果的最低成本II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/enumeration", "leetcode/shortest-path", "leetcode/heap-priority-queue", "leetcode/bao-li", "题单/图论算法", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2038386283551118634"
zhihu_id: "2038386283551118634"
zhihu_title: "yiduobo的每日leetcode 3928.购买苹果的最低成本II"
question_id: "3928"
question: "购买苹果的最低成本 II"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-buy-apples-ii/"
difficulty: "Hard"
rating: 2187
created: "2026-05-14T22:43:54+08:00"
updated: "2026-05-14T22:43:55+08:00"
upvotes: 1
comments: 0
---

# 3928. 购买苹果的最低成本II

> **[yiduobo的每日leetcode 3928.购买苹果的最低成本II](https://zhuanlan.zhihu.com/p/2038386283551118634) · 知乎 · 2026-05-14 · 赞同 1**
> 力扣：[3928. 购买苹果的最低成本 II](https://leetcode.cn/problems/minimum-cost-to-buy-apples-ii/) · Hard · 灵茶山艾府：[跑 2n 次 Dijkstra + 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3928.购买苹果的最低成本II

<https://leetcode.cn/problems/minimum-cost-to-buy-apples-ii/description/>

题目给出一个整数n和一个长度为n的整数数组prices，其中prices[index]表示商店index中苹果的价格。这里的n不超过1000。

另外给出一个二维整数数组roads，长度不超过2000。其中roads\[index\] \= \[u\[index\], v\[index\], cost\[index\], tax\[index\]\]，表示一条双向道路：

- u和v是道路连接的两个商店
- cost表示在不携带苹果时该道路的费用
- tax表示在携带苹果时，这条道路需要在cost的基础上的乘数

对于每个商店，可以选择就地购买苹果，或者是去另一家商店，买完苹果之后再返回。需要注意去另一家商店和回来的路径可以不同。

要求返回一个长度为n的数组ans，表示从每个商店出发购买苹果所需的最小总花费。

对于题目中的每个商店，最直观的做法自然是计算空手从当前商店出发到达任意商店的距离，以及携带苹果时从任意商店出发，返回当前商店的距离。由于题目中的图是无向图，因此后面这个部分也可以认为是携带苹果时从当前商店出发到达任意商店的距离。可以发现，这实际上就是在两张不同的图上的单源最短路问题。

计算完成后，只需遍历所有商店，计算去这个商店的代价，从这个商店购买苹果的代价，以及返回起始商店的代价这三者之和，取其中的最小值即为当前商店对应的答案。

到了这里，问题就转化成了单源最短路问题。注意到题目中点和边的数量都比较小，因此在这里可以直接暴力枚举每个商店，然后在两张图上分别执行带堆dijkstra计算最短路即可。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, n, prices, roads):
        """
        :type n: int
        :type prices: List[int]
        :type roads: List[List[int]]
        :rtype: List[int]
        """
        
        g = [[] for _ in range(n)]
        t = [[] for _ in range(n)]
        for x, y, cost, tax in roads:
            g[x].append((y, cost))
            t[x].append((y, cost * tax))
            g[y].append((x, cost))
            t[y].append((x, cost * tax))
        
        def dijkstra(start, f, dis):
            heap = [(0, start)]
            while heap:
                d, x = heapq.heappop(heap)
                if dis[x] is None:
                    dis[x] = d
                    for y, w in f[x]:
                        if dis[y] is None and d + w < prices[start]:
                            heapq.heappush(heap, (d + w, y))

        res = []
        for start in range(n):
            to = [None] * n
            dijkstra(start, g, to)
            back = [None] * n
            dijkstra(start, t, back)

            cost = prices[start]
            for index in range(n):
                if to[index] is not None and back[index] is not None:
                    cost = min(cost, to[index] + back[index] + prices[index])
            res.append(cost)
        
        return res
```
