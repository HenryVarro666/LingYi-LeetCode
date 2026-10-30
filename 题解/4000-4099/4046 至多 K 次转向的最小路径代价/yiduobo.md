---
title: "4046. 至多K次转向的最小路径代价"
aliases: ["yiduobo的每日leetcode 4046.至多K次转向的最小路径代价"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/shortest-path", "leetcode/dijkstra", "leetcode/heap-priority-queue"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2080416374900499034"
zhihu_id: "2080416374900499034"
zhihu_title: "yiduobo的每日leetcode 4046.至多K次转向的最小路径代价"
question_id: "4046"
question: "至多 K 次转向的最小路径代价"
problem_url: "https://leetcode.cn/problems/minimum-cost-path-with-at-most-k-turns/"
difficulty: "Hard"
created: "2026-09-07T22:26:38+08:00"
updated: "2026-09-07T22:26:38+08:00"
upvotes: 0
comments: 0
---

# 4046. 至多K次转向的最小路径代价

> **[yiduobo的每日leetcode 4046.至多K次转向的最小路径代价](https://zhuanlan.zhihu.com/p/2080416374900499034) · 知乎 · 2026-09-07 · 赞同 0**
> 力扣：[4046. 至多 K 次转向的最小路径代价](https://leetcode.cn/problems/minimum-cost-path-with-at-most-k-turns/) · Hard · 灵茶山艾府：[两种方法：Dijkstra / 动态规划（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4046.至多K次转向的最小路径代价

<https://leetcode.cn/problems/minimum-cost-path-with-at-most-k-turns/description/>

题目给出一个大小为m \* n的二维整数数组grid，其中m和n均不超过75，而grid[i][j]表示访问单元格(i, j)的代价，其数值在0到1000之间。另外给出一个整数k，其严格小于min(m, n)。

现在要求从左上角(0, 0)出发，到达右下角(m - 1, n - 1)。每一步都可以向上下左右四个方向之一移动一步。路径的代价是所有访问过的单元格的值之和，包括起点和终点。若同一个单元格被访问多次，那么其值每次都会被计入到代价中。

问转向次数不超过k次的前提下，到达终点所需的最小代价。若不存在合法的路径，则返回-1。转向指的是两次连续的移动之间的方向产生了改变。

分层图上的最短路径问题，建图后执行dijkstra是可行的选择。不过本题中要回到之前访问过的单元格，必然经历了至少一次转向操作，因此使用记忆化搜索也是可行的选择。

令f[nowx][nowy][nowk][nowd]表示从(nowx, nowy)出发，已经使用了nowk次转向的机会，同时目前方向为nowd时，到达终点所需的最小代价。

这里的nowd取值范围在0到3，我定义为分别表示右、下、左、上四个方向。

那么对于f[nowx][nowy][nowk][nowd]，若其已经来到终点，其值就是grid[nowx][nowy]，否则就需要枚举下一步的方向d，计算相邻单元格的位置(nxtx, nxty)，并根据d与nowd是否相同判断nxtk是nowk还是nowk + 1，然后递归计算f[nxtx][nxty][nxtk][nxtd]，并使用f[nxtx][nxty][nxtk][nxtd] + grid[nowx][nowy]来更新f[now_x][now_y][now_k][now_d]。递归计算的入口为f[0][0][0][0]与f[0][0][0][1]。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, grid, k):
        """
        :type grid: List[List[int]]
        :type k: int
        :rtype: int
        """
        

        m = len(grid)
        n = len(grid[0])

        f = [[[[None] * 4 for _ in range(k + 1)] for _ in range(n)] for _ in range(m)]
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        def calc(now_x, now_y, now_k, now_d):
            if f[now_x][now_y][now_k][now_d] is None:
                if now_x == m - 1 and now_y == n - 1:
                    f[now_x][now_y][now_k][now_d] = grid[now_x][now_y]
                else:
                    best = -1
                    for d in range(4):
                        nxt_x = now_x + dx[d]
                        nxt_y = now_y + dy[d]
                        nxt_k = now_k
                        if d != now_d:
                            nxt_k += 1
                        nxt_d = d
                        if 0 <= nxt_x < m and 0 <= nxt_y < n and nxt_k <= k:
                            cost = calc(nxt_x, nxt_y, nxt_k, nxt_d)
                            if cost != -1 and (best == -1 or best > cost + grid[now_x][now_y]):
                                best = cost + grid[now_x][now_y]

                    f[now_x][now_y][now_k][now_d] = best
            
            return f[now_x][now_y][now_k][now_d]
                     
        calc(0, 0, 0, 0)
        calc(0, 0, 0, 1)
        if f[0][0][0][0] == -1:
            return f[0][0][0][1]
        
        if f[0][0][0][1] == -1:
            return f[0][0][0][0]

        return min(f[0][0][0][0], f[0][0][0][1])
```
