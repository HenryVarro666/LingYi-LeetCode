---
title: "3286. 穿越网格图的安全路径"
aliases: ["yiduobo的每日leetcode 3286.穿越网格图的安全路径"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/graph", "leetcode/queue", "leetcode/shortest-path", "题单/网格图", "题单/网格图/三-网格图-0-1-BFS"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/854716790"
zhihu_id: "854716790"
zhihu_title: "yiduobo的每日leetcode 3286.穿越网格图的安全路径"
question_id: "3286"
question: "穿越网格图的安全路径"
problem_url: "https://leetcode.cn/problems/find-a-safe-walk-through-a-grid/"
difficulty: "Medium"
created: "2024-10-07T22:22:21+08:00"
updated: "2024-10-07T22:22:21+08:00"
upvotes: 0
comments: 0
---

# 3286. 穿越网格图的安全路径

> **[yiduobo的每日leetcode 3286.穿越网格图的安全路径](https://zhuanlan.zhihu.com/p/854716790) · 知乎 · 2024-10-07 · 赞同 0**
> 力扣：[3286. 穿越网格图的安全路径](https://leetcode.cn/problems/find-a-safe-walk-through-a-grid/) · Medium · 灵茶山艾府：[0-1 BFS 线性做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3286.穿越网格图的安全路径

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-a-safe-walk-through-a-grid/description/)

题目给出一个m \* n的二进制矩阵grid，另外给出一个整数health，表示玩家的初始血量。一开始玩家位于左上角(0, 0)，要求通过向相邻格子移动来到达矩阵右下角(m - 1, n - 1)，移动过程中每经过一个值为1的单元格血量都会减少1，问是否可以在保持血量始终为正数的前提下到达目的地。

经典的分层图bfs的问题，在常规bfs的基础上需要新增当前血量这一状态。初始情况下玩家位于(0, 0)，血量为health - grid[0][0]，即初始状态为(0, 0, health - grid[0][0])，接下来从这个状态开始进行bfs。

对于当前状态(nowx, nowy, nowh)，尝试向四个相邻的单元格移动，若目的地坐标(x, y)没有出界，且新的血量h \= nowh - grid[x][y]依然大于0，同时(x, y, h)这个状态没有被访问过，那么就将其加入到bfs队列并将这个状态标记为访问过。若bfs过程中到达了(m - 1, n - 1)，那么就返回true，否则返回false。

最后附上python代码：

```python
class Solution(object):
    def findSafeWalk(self, grid, health):
        """
        :type grid: List[List[int]]
        :type health: int
        :rtype: bool
        """

        if health - grid[0][0] == 0:
            return False

        m = len(grid)
        n = len(grid[0])

        f = [[[False] * (m + n + 1) for _ in range(n)] for _ in range(m)]
        f[0][0][health - grid[0][0]] = True
        q = [[0, 0, health - grid[0][0]]]
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        head, tail = 0, 1
        while head < tail:
            for nowx, nowy, nowh in q[head : tail]:
                for d in range(4):
                    x = nowx + dx[d]
                    y = nowy + dy[d]
                    if 0 <= x < m and 0 <= y < n:
                        h = nowh - grid[x][y]
                        if h > 0 and not f[x][y][h]:
                            q.append([x, y, h])
                            f[x][y][h] = True
                            if x == m - 1 and y == n - 1:
                                return True

            head, tail = tail, len(q)
        
        return False
```
