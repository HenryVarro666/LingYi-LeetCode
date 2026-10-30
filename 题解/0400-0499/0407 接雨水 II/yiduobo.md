---
title: "407. 接雨水II"
aliases: ["yiduobo的每日leetcode 407.接雨水II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/186228138"
zhihu_id: "186228138"
zhihu_title: "yiduobo的每日leetcode 407.接雨水II"
question_id: "407"
question: "接雨水 II"
problem_url: "https://leetcode.cn/problems/trapping-rain-water-ii/"
difficulty: "Hard"
created: "2020-08-16T18:40:34+08:00"
updated: "2020-08-16T18:40:34+08:00"
upvotes: 0
comments: 0
---

# 407. 接雨水II

> **[yiduobo的每日leetcode 407.接雨水II](https://zhuanlan.zhihu.com/p/186228138) · 知乎 · 2020-08-16 · 赞同 0**
> 力扣：[407. 接雨水 II](https://leetcode.cn/problems/trapping-rain-water-ii/) · Hard · 灵茶山艾府：[短板效应（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

407.接雨水II <https://leetcode-cn.com/problems/trapping-rain-water-ii/>

二维的接雨水问题，相比一维的情况需要维护四个方向的高度，暂时还没想出什么好的优化方式。

第一种想法是先找到当前的最矮高度min_height，然后通过dfs找出所有的min_height形成的若干个区域，以及这些区域周边的围墙的最矮高度min_wall。对于这些区域，若当前区域没有与地图边界相连，那么当前区域可以接的水量就是(min_wall - min_height) \* S，其中S为当前区域的面积。接下来，将当前区域的所有格子填充到min_wall的高度，然后继续迭代。

需要最矮区域以及对应的min_wall和面积S都可以通过一次dfs搞定，那么时间复杂度就是O(mn)。而需要填充的次数则与地图的构造有关，在最坏情况下应该是需要对每个柱子都会被当做min_wall进行一次填充，那么最终的时间复杂度应该是O((mn) ^ 2)。

上面的做法感觉复杂度还是太高了，于是转换思路，不考察最矮的格子，而是考察最矮的边界。首先，初始的边界就是最外围的这一圈柱子，然后还是优先考察最矮的边界。若这个边界相邻的格子并没有被考察过，且高度比边界要矮，那么这个相邻格子就能储水。计算储水的量之后，这个格子就可以作为新的边界加入到边界中，而高度则应该取边界以及当前格子高度的较大值。

地图中的每个格子只需要计算一次，而每次是找出最小的格子进行计算，那么使用堆进行优化之后，最终的时间复杂度就是O(mn \* log(mn))。

最后附上python代码：

```python
import heapq

class Solution(object):
    def trapRainWater(self, heightMap):
        """
        :type heightMap: List[List[int]]
        :rtype: int
        """

        if len(heightMap) <= 2:
            return 0

        if len(heightMap[0]) <= 2:
            return 0

        m = len(heightMap)
        n = len(heightMap[0])

        used = [[False] * n for _ in range(m)]
        heap = []
        for index in range(1, m - 1):
            heap.append([heightMap[index][0], [index, 0]])
            used[index][0] = True
            heap.append([heightMap[index][n - 1], [index, n - 1]])
            used[index][n - 1] = True

        for index in range(1, n - 1):
            heap.append([heightMap[0][index], [0, index]])
            used[0][index] = True
            heap.append([heightMap[m - 1][index], [m - 1, index]])
            used[m - 1][index] = True

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        res = 0
        heapq.heapify(heap)
        while heap:
            now_height, pos = heapq.heappop(heap)
            nowx, nowy = pos
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x > 0 and x < m - 1 and y > 0 and y < n - 1 and not used[x][y]:
                    if now_height > heightMap[x][y]:
                        res += now_height - heightMap[x][y]
                        heapq.heappush(heap, [now_height, [x, y]])
                    else:
                        heapq.heappush(heap, [heightMap[x][y], [x, y]])
                    used[x][y] = True
        return res
```
