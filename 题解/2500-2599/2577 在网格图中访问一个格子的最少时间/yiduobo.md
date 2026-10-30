---
title: "2577. 在网格图中访问一个格子的最少时间"
aliases: ["yiduobo的每日leetcode 2577.在网格图中访问一个格子的最少时间"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/breadth-first-search", "leetcode/graph", "leetcode/binary-search", "leetcode/matrix", "leetcode/shortest-path", "题单/网格图", "题单/图论算法", "题单/网格图/五-综合应用", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/642242983"
zhihu_id: "642242983"
zhihu_title: "yiduobo的每日leetcode 2577.在网格图中访问一个格子的最少时间"
question_id: "2577"
question: "在网格图中访问一个格子的最少时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-visit-a-cell-in-a-grid/"
difficulty: "Hard"
rating: 2382
created: "2023-07-08T03:29:24+08:00"
updated: "2023-07-08T03:29:24+08:00"
upvotes: 0
comments: 0
---

# 2577. 在网格图中访问一个格子的最少时间

> **[yiduobo的每日leetcode 2577.在网格图中访问一个格子的最少时间](https://zhuanlan.zhihu.com/p/642242983) · 知乎 · 2023-07-08 · 赞同 0**
> 力扣：[2577. 在网格图中访问一个格子的最少时间](https://leetcode.cn/problems/minimum-time-to-visit-a-cell-in-a-grid/) · Hard · 灵茶山艾府：[两种方法：Dijkstra/二分答案+BFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2577.在网格图中访问一个格子的最少时间

[力扣](https://leetcode.cn/problems/minimum-time-to-visit-a-cell-in-a-grid/)

题目要求每一时刻都进行移动，但是没有规定同一个格子不能访问多次，这也就意味着可以在两个相邻的格子之间反复横跳。换言之，只要单元格(0, 1)和(1, 0)，有一个格子的最早可访问时间小于等于1，那么就必然可以到达矩阵右下角，反之就是无解，直接返回-1。

另一方面， 时刻移动这一条件也决定了到达横纵坐标之和为偶数的单元格时，时间点一定是偶数，反之到达横纵坐标之和为奇数的单元格时，时间点一定是奇数。根据这一点，就需要对每个单元格的最早可访问时间进行修正。具体来说，就是对于最早可到达时间与横纵坐标奇偶性不能的单元格，需要将其最早可到达时间加上1，使得二者的奇偶性相同。

接下来对于有解的情况，可以使用类似dijkstra算法的方法来进行处理。在这里贪心成立的证明也很简单，对于两个单元格(x1, y1)以及(x2, y2)，若当前可到达(x1, y1)的最早时间t1要小于等于可到达(x2, y2)的最早时间t2，那么先走到(x2, y2)再从(x2, y2)走到(x1, y1)所需的时间必然是大于t1的，也就表明了如果每次都选择未到达节点中，预计可到达时间最短的节点，就能保证到达每个节点的时间都是最早的。

根据上面的结论，就可以令f[i][j]表示最早可达到单元格(i, j)的时间，并使用一个堆来维护当前到达单元格的可行方案。每一轮都从堆中选出一个当前还未到达，且预计可到达时间最早的单元格，将其对应的f值置为当前的时间，并将其相邻四个单元格中还未到达的单元格也加入到堆中。需要特别注意的是，这里相邻单元格的预计可到达时间应该取该单元格最早可访问时间以及当前时间点加1这两者中的较大值。在到达右下角节点(m - 1, n - 1)后，其对应的f值即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minimumTime(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        if grid[1][0] > 1 and grid[0][1] > 1:
            return -1
        
        f = [[None] * n for _ in range(m)]
        heap = [[0, 0, 0]]
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while heap:
            nowt, nowx, nowy = heapq.heappop(heap)
            if f[nowx][nowy] is None:
                f[nowx][nowy] = nowt
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and f[x][y] is None:
                        delta = (grid[x][y] % 2)^((x + y) % 2)
                        if grid[x][y] + delta <= nowt + 1:
                            heapq.heappush(heap, [nowt + 1, x, y])
                        else:
                            heapq.heappush(heap, [grid[x][y] + delta, x, y])
        

        return f[-1][-1]
```
