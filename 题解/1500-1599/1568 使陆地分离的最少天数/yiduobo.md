---
title: "1568. 使陆地分离的最少天数"
aliases: ["yiduobo的每日leetcode 1568.使陆地分离的最少天数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/428319356"
zhihu_id: "428319356"
zhihu_title: "yiduobo的每日leetcode 1568.使陆地分离的最少天数"
question_id: "1568"
question: "使陆地分离的最少天数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-days-to-disconnect-island/"
created: "2021-11-02T00:34:14+08:00"
updated: "2021-11-02T00:34:14+08:00"
upvotes: 0
comments: 0
---

# 1568. 使陆地分离的最少天数

> **[yiduobo的每日leetcode 1568.使陆地分离的最少天数](https://zhuanlan.zhihu.com/p/428319356) · 知乎 · 2021-11-02 · 赞同 0**
> 力扣：[1568. 使陆地分离的最少天数](https://leetcode.cn/problems/minimum-number-of-days-to-disconnect-island/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1568.使陆地分离的最少天数

[力扣](https://leetcode-cn.com/problems/minimum-number-of-days-to-disconnect-island/)

首先，若地图中一个1都没有，或者地图中存在两个连通分量，那么答案就是0。那么首先可以使用染色法对地图中的连通分量进行染色，若最终没有格子被染色，或者有超过一种颜色，那么就直接返回0。

接下来考察只有一个连通分量的情况。同样是先考虑边界情况。由于这是一个二维网格，因此对于网格角落上的格子而言，其最多也只能与两个格子相连，这也就意味着题目答案的上界为2，即去掉与这个角落格子相连的格子。那么是否存在某种情况的答案为1呢？答案是肯定的：

1、若地图上就只有一个格子，那么答案就是1

2、若将地图上的1视为一张无向连通图，那么如果将图中的某个割点删去，无向连通图就会变得不连通，此时的答案同样为1。于是此时的问题就变成了如何求解无向图中的割点。对于连通分量、割点、桥这连通性的问题，经典的做法就是tarjan算法。其思想简单来说就是对连通图的dfs树中节点进行编号，那么就可以根据某个节点自身以及可访问节点的编号，来判断图中是否存在从该节点出发的回边。具体算法在这里就不再展开了。

另外，除了常规的dfn和low的比较，判断割点时还有一种特殊情况，即dfs树的根节点。该节点无法通过dfn和low来进行判断，但如果根节点在dfs树中存在两个或以上的孩子节点，那么当删去根节点后，这两个孩子节点之间必然是不连通的，因此只需要在dfs过程中顺便记录节点的孩子数目，然后在dfs结束后判断根节点孩子的个数就能确定根节点是否为割点。

那么对于只有一个连通分量，且节点个数大于1的情况，则可以使用tarjan算法求解图中是否存在割点，若存在，那么答案为1，否则答案为2。

最后附上python代码：

```python
class Solution(object):
    def minDays(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        q = []
        l = r = 0
        used = [[False] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1 and not used[i][j]:
                    if r > 0:
                        return 0
                    q.append([i, j])
                    used[i][j] = True
                    r = 1
                    while l < r:
                        nowx, nowy = q[l]
                        l += 1
                        for index in range(4):
                            x = nowx + dx[index]
                            y = nowy + dy[index]
                            if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 1 and not used[x][y]:
                                q.append([x, y])
                                used[x][y] = True
                                r += 1

        if r == 1:
            return 1

        self.flag = False
        self.cnt = 0
        dfn = [[None] * n for _ in range(m)]
        low = [[None] * n for _ in range(m)]
        self.dfs(q[0][0], q[0][1], dfn, low, None, None, m, n, dx, dy, grid)
        if self.flag:
            return 1
        else:
            return 2

    def dfs(self, nowx, nowy, dfn, low, lastx, lasty, m, n, dx, dy, grid):
        self.cnt += 1
        dfn[nowx][nowy] = self.cnt
        low[nowx][nowy] = self.cnt

        child_cnt = 0
        for index in range(4):
            x = nowx + dx[index]
            y = nowy + dy[index]
            if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 1:
                if dfn[x][y] is None:
                    child_cnt += 1
                    self.dfs(x, y, dfn, low, nowx, nowy, m, n, dx, dy, grid)
                    if self.flag:
                        return
                    low[nowx][nowy] = min(low[nowx][nowy], low[x][y])
                    if lastx is not None and low[x][y] >= dfn[nowx][nowy]:
                        self.flag = True
                        return
                elif x != lastx or y != lasty:
                    low[nowx][nowy] = min(low[nowx][nowy], dfn[x][y])
        
        if lastx is None and child_cnt > 1:
            self.flag = True
```
