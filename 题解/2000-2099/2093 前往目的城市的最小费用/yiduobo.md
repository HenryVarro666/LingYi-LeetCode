---
title: "2093. 前往目的城市的最小费用"
aliases: ["yiduobo的每日leetcode 2093.前往目的城市的最小费用"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/626091311"
zhihu_id: "626091311"
zhihu_title: "yiduobo的每日leetcode 2093.前往目的城市的最小费用"
question_id: "2093"
question: "前往目的城市的最小费用"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-reach-city-with-discounts/"
created: "2023-05-01T06:13:43+08:00"
updated: "2023-05-01T06:13:43+08:00"
upvotes: 0
comments: 0
---

# 2093. 前往目的城市的最小费用

> **[yiduobo的每日leetcode 2093.前往目的城市的最小费用](https://zhuanlan.zhihu.com/p/626091311) · 知乎 · 2023-05-01 · 赞同 0**
> 力扣：[2093. 前往目的城市的最小费用](https://leetcode.cn/problems/minimum-cost-to-reach-city-with-discounts/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

2093.前往目的城市的最小费用

[力扣](https://leetcode.cn/problems/minimum-cost-to-reach-city-with-discounts/)

最短路算法问题的升级版，在常规最短路问题的基础上增加了可以使用discounts次折扣的条件，那么一个自然的想法就是将折扣使用的次数加入到最短路的状态表示中，也就是将dis[i]表示到达城市i的最小费用，升级成dis[i][level]表示到达城市i，使用了level次折扣的最小费用。

这样一来，问题就变成了分层图上的最短路问题。对于某个节点，其可以按照原价来到同层的相邻节点，或者以折扣价来到下一层，也就是当前level + 1层的相邻节点，也就是说对于图中的每条边，可以视为新增了一条折扣价的边，其连接的节点是下一层的对应节点，接下来只需要按照常规最短路的解决方法，使用dijkstra算法求解最短路即可。

具体实现上，并不需要重新建图，只需在状态中将当前所处的level表达出来即可。

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, n, highways, discounts):
        """
        :type n: int
        :type highways: List[List[int]]
        :type discounts: int
        :rtype: int
        """

        g = {index : {} for index in range(n)}
        for x, y, t in highways:
            g[x][y] = t
            g[y][x] = t

        dis = [[-1] * (discounts + 1) for _ in range(n)]

        heap = [[0, 0, 0]]
        while heap:
            d, now, level = heapq.heappop(heap)
            if dis[now][level] == -1:
                dis[now][level] = d
                if now == n - 1:
                    return d

                for next in g[now]:
                    if dis[next][level] == -1:
                        heapq.heappush(heap, [d + g[now][next], next, level])
                    if level < discounts and dis[next][level + 1] == -1:
                        heapq.heappush(heap, [d + g[now][next] / 2, next, level + 1])

        return -1
```
