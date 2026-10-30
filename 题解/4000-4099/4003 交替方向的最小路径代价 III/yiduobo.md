---
title: "4003. 交替方向的最小路径代价III"
aliases: ["yiduobo的每日leetcode 4003.交替方向的最小路径代价III"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/graph", "leetcode/shortest-path", "leetcode/heap-priority-queue"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2065599354430284763"
zhihu_id: "2065599354430284763"
zhihu_title: "yiduobo的每日leetcode 4003.交替方向的最小路径代价III"
question_id: "4003"
question: "交替方向的最小路径代价 III"
problem_url: "https://leetcode.cn/problems/minimum-cost-path-with-alternating-directions-iii/"
difficulty: "Hard"
created: "2026-07-29T01:01:09+08:00"
updated: "2026-07-29T01:01:10+08:00"
upvotes: 0
comments: 0
---

# 4003. 交替方向的最小路径代价III

> **[yiduobo的每日leetcode 4003.交替方向的最小路径代价III](https://zhuanlan.zhihu.com/p/2065599354430284763) · 知乎 · 2026-07-29 · 赞同 0**
> 力扣：[4003. 交替方向的最小路径代价 III](https://leetcode.cn/problems/minimum-cost-path-with-alternating-directions-iii/) · Hard · 灵茶山艾府：[Dijkstra 最短路（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4003.交替方向的最小路径代价

<https://leetcode.cn/problems/minimum-cost-path-with-alternating-directions-iii/description/>

题目给出两个整数m和n，表示一个网格的行数和列数。现在要求从左上角单元格(0, 0)出发，到达右下角单元格(m - 1, n - 1)。另外给出一个m \* n的二维整数数组penalty。

进入某个单元格(i, j)的代价为(i + 1) \* (j + 1)。

从(0, 0)开始，最初需要支付入口代价。进入(0, 0)后执行的行动从1开始编号。

对于每次行动，可以移动到相邻的单元格，或者原地挂机。移动需要遵循以下规则：

- 若当前行动编号为奇数，那么可以向右或者向下移动
- 若当前行动编号为偶数，那么可以向左或者向上移动

行动的代价如下:

- 如果遵守移动的规则，那么只需要支付目标单元格的进入代价
- 如果违反移动的规则，那么除了需要支付目标单元格的进入代价，还需要额外支付penalty[i][j]，其中(i, j)是移动前所处的单元格
- 如果选择挂机，那么需要支付penalty[i][j]

每次行动或者等待后，行动编号增加1。问到达(m - 1, n - 1)所需的最小总代价。

非常标准的分层图最短路问题。将网格视为一个m \* n个节点的图，接下来这张图复制一份，得到的两张图分别对应奇数编号的行动以及偶数编号的行动。

接下来，对于奇数行动编号对应的图:

- 图中每个节点向偶数行动编号对应的图的相同节点，以及四个相邻节点(如果存在)，各发出一条边
- 到达偶数图中对应节点的边权为penalty[i][j]，意为原地挂机
- 到达偶数图中右侧以及下方相邻节点的边权为进入代价，表示按规则行动
- 到达偶数图中左侧以及上方相邻节点的边权为进入代价加上penalty[i][j]之和，表示违反规则行动

与之对称，对于偶数行动编号对应的图：

- 图中每个节点向奇数行动编号对应的图中对应的相同节点，以及四个相邻节点(如果存在)，各发出一条边
- 到达奇数图中对应节点的边权为penalty[i][j]，意为原地挂机
- 到达奇数图中右侧以及下方相邻节点的边权为进入代价加上penalty[i][j]之和，表示违反规则行动
- 到达奇数图中左侧以及上方相邻节点的边权为进入代价，表示按规则行动

建图之后，从奇数行动编号对应的图的节点(0, 0)出发，执行dijkstra算法，计算到达奇数图或者偶数图的(m - 1, n - 1)的最短路径即可。

在具体实现上，并不需要真的建图，只需要记录当前属于哪一层图，然后判断根据目标位置与当前所处层图计算边权并更新距离就行了。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, m, n, penalty):
        """
        :type m: int
        :type n: int
        :type penalty: List[List[int]]
        :rtype: int
        """
        
        dis = [[[None] * 2 for _ in range(n)] for _ in range(m)]
        heap = [(1, 0, 0, 1)]

        dx = [[-1, 0], [1, 0]]
        dy = [[0, -1], [0, 1]]

        res = 0
        while heap:
            d, x, y, r = heapq.heappop(heap)
            if dis[x][y][r] is None:
                if x == m - 1 and y == n - 1:
                    res = d
                    break
                
                dis[x][y][r] = d
                if dis[x][y][1 - r] is None:
                    heapq.heappush(heap, (d + penalty[x][y], x, y, 1 - r))

                for t in range(2):
                    if t != r:
                        p = penalty[x][y]
                    else:
                        p = 0

                    for index in range(2):
                        xx = x + dx[t][index]
                        yy = y + dy[t][index]
                        if 0 <= xx < m and 0 <= yy < n:
                            cost = (xx + 1) * (yy + 1) + p
                            if dis[xx][yy][1 - r] is None:
                                heapq.heappush(heap, (d + cost, xx, yy, 1 - r))

        return res
```
