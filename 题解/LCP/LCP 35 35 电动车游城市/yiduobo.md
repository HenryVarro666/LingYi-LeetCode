---
title: "LCP 35. 电动车游城市"
aliases: ["yiduobo的每日leetcode LCP35.电动车游城市"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/574958652"
zhihu_id: "574958652"
zhihu_title: "yiduobo的每日leetcode LCP35.电动车游城市"
question_id: "LCP 35"
question: "电动车游城市"
created: "2022-10-19T02:26:28+08:00"
updated: "2022-10-19T02:26:28+08:00"
upvotes: 0
comments: 0
---

# LCP 35. 电动车游城市

> **[yiduobo的每日leetcode LCP35.电动车游城市](https://zhuanlan.zhihu.com/p/574958652) · 知乎 · 2022-10-19 · 赞同 0**
> 力扣：LCP 35. 电动车游城市

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP35.电动车游城市

[力扣](https://leetcode.cn/problems/DFPeFJ/)

题目除了常规最短路问题中的距离外，还额外有一个油量的限制。不过这个油量的上限cnt规模很小，那么直接将其与原图中的节点组合编码完全是可行。这样一来，就得到了一张新图，其中的每个节点都表示为(node, cnt)，表示当前处于原图中的node这个节点，且剩余油量为cnt。

对于新图中的节点(now_node, now_cnt)而言：

1、可以枚举now_node在原图中的所有相邻节点next_node。若now_node到next_node在原图中的距离g[now_node][next_node]小于等于cnt，那么就可以从(now_node, now_cnt)走到(next_node, now_cnt - g[now_node][next_node]，距离与原图的距离相同

2、也可以原地挂机充电，那么就是从(now_node, now_cnt)走到(now_node, next_cnt)，距离为充单位时间的点所需的时间charge[now_node]

接下来就只需从(node \= start, cnt \= 0)这个节点开始做dijkstra，找到距离(node \= end, cnt \= k)的最短路就行了。

需要特别注意的是，题目中的原图可能有重边，因此在初始化g的时候需要注意取其中的较小值。

最后附上python代码：

```python
class Solution(object):
    def electricCarPlan(self, paths, cnt, start, end, charge):
        """
        :type paths: List[List[int]]
        :type cnt: int
        :type start: int
        :type end: int
        :type charge: List[int]
        :rtype: int
        """

        n = len(charge)
        g = {index : {} for index in range(n)}
        for x, y, v in paths:
            if y not in g[x]:
                g[x][y] = g[y][x] = v
            else:
                g[x][y] = min(g[x][y], v)
                g[y][x] = min(g[y][x], v)

        heap = [(0, start * (cnt + 1))]
        dis = {}
        while heap:
            d, now_state = heapq.heappop(heap)
            if now_state in dis:
                continue
            dis[now_state] = d
            now_node, now_cnt = now_state / (cnt + 1), now_state % (cnt + 1)
            if now_node == end:
                return d
            for next_node in g[now_node]:
                if g[now_node][next_node] <= now_cnt:
                    next_cnt = now_cnt - g[now_node][next_node]
                    next_state = next_node * (cnt + 1) + next_cnt
                    heapq.heappush(heap, (d + g[now_node][next_node], next_state))
            
            if now_cnt < cnt:
                heapq.heappush(heap, (d + charge[now_node], now_state + 1))

        return -1
```
