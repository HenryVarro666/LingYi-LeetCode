---
title: "3341. 到达最后一个房间的最少时间I & 3342. 到达最后一个房间的最少时间II"
aliases: ["yiduobo的每日leetcode 3341.到达最后一个房间的最少时间I && 3342.到达最后一个房间的最少时间II", "3341. 到达最后一个房间的最少时间I", "3342. 到达最后一个房间的最少时间II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/shortest-path", "leetcode/heap-priority-queue", "题单/图论算法", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/25483054590"
zhihu_id: "25483054590"
zhihu_title: "yiduobo的每日leetcode 3341.到达最后一个房间的最少时间I && 3342.到达最后一个房间的最少时间II"
question_id: ["3341", "3342"]
question: ["到达最后一个房间的最少时间 I", "到达最后一个房间的最少时间 II"]
problem_url: ["https://leetcode.cn/problems/find-minimum-time-to-reach-last-room-i/", "https://leetcode.cn/problems/find-minimum-time-to-reach-last-room-ii/"]
difficulty: "Medium"
rating: ["1721", "1862"]
created: "2025-02-22T00:14:55+08:00"
updated: "2025-02-22T00:14:55+08:00"
upvotes: 1
comments: 0
---

# 3341. 到达最后一个房间的最少时间I & 3342. 到达最后一个房间的最少时间II

> **[yiduobo的每日leetcode 3341.到达最后一个房间的最少时间I && 3342.到达最后一个房间的最少时间II](https://zhuanlan.zhihu.com/p/25483054590) · 知乎 · 2025-02-22 · 赞同 1**
> 力扣：[3341. 到达最后一个房间的最少时间 I](https://leetcode.cn/problems/find-minimum-time-to-reach-last-room-i/) · Medium · 灵茶山艾府：[Dijkstra 最短路（Python/Java/C++/Go）](../3341%20到达最后一个房间的最少时间%20I/灵茶山艾府.md)
> 力扣：[3342. 到达最后一个房间的最少时间 II](https://leetcode.cn/problems/find-minimum-time-to-reach-last-room-ii/) · Medium · 灵茶山艾府：[Dijkstra 最短路（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3341.到达最后一个房间的最少时间I

[3341. 到达最后一个房间的最少时间 I - 力扣（LeetCode）](https://leetcode.cn/problems/find-minimum-time-to-reach-last-room-i/description/)

3342.到达最后一个房间的最少时间II

[3342. 到达最后一个房间的最少时间 II - 力扣（LeetCode）](https://leetcode.cn/problems/find-minimum-time-to-reach-last-room-ii/description/)

题目给出一个大小为n \* m的二维数组moveTime，表示有一个n \* m的矩阵，必须在moveTime[i][j]之后才能移动到第i行第j列的单元格。问如果在时刻t \= 0开始从单元格(0, 0)出发，每次只能移动到相邻的单元格，那么到达(n - 1, m - 1)所需的最少时间是多少。

其中3341题中移动到相邻单元格所需的时间为1秒，而3342题中移动到相邻的单元格时，奇数次移动所需的时间为1秒，而偶数次移动所需的时间为2秒。

将这n \* m个单元格都视为图中的点，那么每个点最多只会和相邻的四个点连上边，问题就变成了稀疏无向图中的最短路径问题，使用堆优化的dijkstra算法直接跑一遍就行了。另外需要注意的是在更新到达每个单元格的最短路径时，除了常规的距离迭代，还需要将单元格对应的moveTime也考虑进去。

关于单次移动的代价，对于3341题就是常规的加一，而对于3342题，由于每次移动都是在相邻单元格之间，因此奇数次的移动一定是从行列和为偶数的单元格移动到行列和为奇数的单元格，而偶数次的移动则相反，因此可以通过目的地单元格的行列和来判断当前这次移动的代价。

最后附上3342题的python代码：

```python
class Solution(object):
    def minTimeToReach(self, moveTime):
        """
        :type moveTime: List[List[int]]
        :rtype: int
        """
        
        n = len(moveTime)
        m = len(moveTime[0])
        dis = [[None] * m for _ in range(n)]

        q = [(0, 0, 0)]
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while q:
            now_t, now_x, now_y = heapq.heappop(q)
            if dis[now_x][now_y] is None:
                dis[now_x][now_y] = now_t
            else:
                continue

            if now_x == n - 1 and now_y == m - 1:
                return now_t

            for d in range(4):
                nxt_x = now_x + dx[d]
                nxt_y = now_y + dy[d]
                if 0 <= nxt_x < n and 0 <= nxt_y < m and dis[nxt_x][nxt_y] is None:
                    nxt_t = max(now_t, moveTime[nxt_x][nxt_y]) + 2 - (nxt_x + nxt_y) % 2
                    heapq.heappush(q, (nxt_t, nxt_x, nxt_y))

        return dis[n - 1][m - 1]
```
