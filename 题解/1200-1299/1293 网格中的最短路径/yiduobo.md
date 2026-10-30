---
title: "1293. 网格中的最短路径"
aliases: ["yiduobo的每日leetcode 1293.网格中的最短路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/390128399"
zhihu_id: "390128399"
zhihu_title: "yiduobo的每日leetcode 1293.网格中的最短路径"
question_id: "1293"
question: "网格中的最短路径"
problem_url: "https://leetcode.cn/problems/shortest-path-in-a-grid-with-obstacles-elimination/"
created: "2021-07-15T23:25:19+08:00"
updated: "2021-07-15T23:25:19+08:00"
upvotes: 0
comments: 0
---

# 1293. 网格中的最短路径

> **[yiduobo的每日leetcode 1293.网格中的最短路径](https://zhuanlan.zhihu.com/p/390128399) · 知乎 · 2021-07-15 · 赞同 0**
> 力扣：[1293. 网格中的最短路径](https://leetcode.cn/problems/shortest-path-in-a-grid-with-obstacles-elimination/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1293.网格中最短路径

[力扣](https://leetcode-cn.com/problems/shortest-path-in-a-grid-with-obstacles-elimination/)

经典的bfs问题，令f[x][y][s]表示走到位置(x, y)，过程中消除了s个障碍的最短路径长度，那么我们可以从f[0][0][0]开始，每次尝试往四个方向走。若当前走到的格子上有障碍，那么就需要将s加上1。若新的状态表示(x', y', s')满足(x', y')还在地图内，且s' \<\= k，那么就将其新的状态加入到bfs队列中。

若某一时刻走到了地图右下角，那么当前bfs的轮次就是最终答案。若bfs完成后依然没走到右下角，那么就返回-1。

最后附上python代码：

```python
class Solution(object):
    def shortestPath(self, grid, k):
        """
        :type grid: List[List[int]]
        :type k: int
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        if m == 1 and n == 1:
            return 0
        f = [[[False] * (k + 1) for j in range(n)] for i in range(m)]
        q = [[0, 0, 0]]
        f[0][0][0] = True
        l = 0
        r = 1
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        res = 0
        while l < r:
            res += 1
            for nowx, nowy, nows in q[l : r]:
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n:
                        s = nows + grid[x][y]
                        if s <= k and not f[x][y][s]:
                            f[x][y][s] = True
                            q.append([x, y, s])
                            if x == m - 1 and y == n - 1:
                                return res

            l, r = r, len(q)

        return -1
```
