---
title: "2662. 前往目标的最小代价"
aliases: ["yiduobo的每日leetcode 2662.前往目标的最小代价"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/shortest-path", "题单/图论算法", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/648378816"
zhihu_id: "648378816"
zhihu_title: "yiduobo的每日leetcode 2662.前往目标的最小代价"
question_id: "2662"
question: "前往目标的最小代价"
problem_url: "https://leetcode.cn/problems/minimum-cost-of-a-path-with-special-roads/"
difficulty: "Medium"
rating: 2154
created: "2023-08-07T01:15:30+08:00"
updated: "2023-08-07T01:15:30+08:00"
upvotes: 0
comments: 0
---

# 2662. 前往目标的最小代价

> **[yiduobo的每日leetcode 2662.前往目标的最小代价](https://zhuanlan.zhihu.com/p/648378816) · 知乎 · 2023-08-07 · 赞同 0**
> 力扣：[2662. 前往目标的最小代价](https://leetcode.cn/problems/minimum-cost-of-a-path-with-special-roads/) · Medium · 灵茶山艾府：[无需建图，直接朴素 Dijkstra 求最短路（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2662.前往目标的最小代价

[力扣](https://leetcode.cn/problems/minimum-cost-of-a-path-with-special-roads/)

由于题目中路径长度的计算方式是曼哈顿距离，因此除了起点、终点以及特殊路径中位置点之外，是没有必要走到其他无关点位上的，因为这样并不会使得最终代价更小。换言之，问题就变成了最多只有两百零二个点的最短路径问题，因此可以对这些点建图，然后使用dijkstra算法求解。

由于这些点之间都可以互相到达，因此这是一个稠密图上的最短路问题，使用dijkstra算法时不应该使用堆优化。另外题目中的特殊路径是有向边，同时特殊路径的代价并不一定比直接走更优，在使用需要注意。

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, start, target, specialRoads):
        """
        :type start: List[int]
        :type target: List[int]
        :type specialRoads: List[List[int]]
        :rtype: int
        """

        if start == target:
            return 0

        node_list = [start, target]
        node_dict = {}
        node_dict[(start[0], start[1])] = 0
        node_dict[(target[0], target[1])] = 1

        sp_dict = {}

        for x1, y1, x2, y2, cost in specialRoads:
            if (x1, y1) not in node_dict:
                node_dict[(x1, y1)] = len(node_list)
                node_list.append([x1, y1])
            
            if (x2, y2) not in node_dict:
                node_dict[(x2, y2)] = len(node_list)
                node_list.append([x2, y2])
            
            id1 = node_dict[(x1, y1)]
            id2 = node_dict[(x2, y2)]
            if abs(x1 - x2) + abs(y1 - y2) > cost:
                if (id1, id2) not in sp_dict or sp_dict[(id1, id2)] > cost:
                    sp_dict[(id1, id2)] = cost
            
        n = len(node_list)
        dis = [None] * n
        dis[0] = 0
        vis = set()
        for _ in range(n):
            mi = None
            for i in range(n):
                if i not in vis and dis[i] is not None and (mi is None or dis[mi] > dis[i]):
                    mi = i
            
            vis.add(mi)
            for i in range(n):
                if i not in vis:
                    cost = abs(node_list[i][0] - node_list[mi][0]) + abs(node_list[i][1] - node_list[mi][1])
                    if (mi, i) in sp_dict and cost > sp_dict[(mi, i)]:
                        cost = sp_dict[(mi, i)]

                    if dis[i] is None or dis[i] > dis[mi] + cost:
                        dis[i] = dis[mi] + cost

        return dis[1]
```
