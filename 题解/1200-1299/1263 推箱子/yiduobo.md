---
title: "1263. 推箱子"
aliases: ["yiduobo的每日leetcode 1263.推箱子"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/386934015"
zhihu_id: "386934015"
zhihu_title: "yiduobo的每日leetcode 1263.推箱子"
question_id: "1263"
question: "推箱子"
problem_url: "https://leetcode.cn/problems/minimum-moves-to-move-a-box-to-their-target-location/"
created: "2021-07-05T22:46:13+08:00"
updated: "2021-07-05T22:46:13+08:00"
upvotes: 2
comments: 0
---

# 1263. 推箱子

> **[yiduobo的每日leetcode 1263.推箱子](https://zhuanlan.zhihu.com/p/386934015) · 知乎 · 2021-07-05 · 赞同 2**
> 力扣：[1263. 推箱子](https://leetcode.cn/problems/minimum-moves-to-move-a-box-to-their-target-location/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1263.推箱子

[力扣](https://leetcode-cn.com/problems/minimum-moves-to-move-a-box-to-their-target-location/)

经典的搜索问题，可以使用启发式搜索算法，并利用图论中割点相关的知识来进行优化。我在这里采用的是最朴素的bfs，令状态(x, y, 0)到(x, y, 3)分别表示箱子在位置(x, y)，人在箱子的上、下、左、右四个相邻位置。

初始状态下，我们先从S所在位置开始进行寻路bfs，尝试走到箱子的四个方向上的相邻位置，若可以走到，则将对应的状态加入到推箱子的队列中。

接下来开始进行推箱子的bfs，对于当前状态(x, y, k)，我们按照当前方向推动一个格子，那么此时就来到了(x', y', k)。若这个状态没有被访问过，那么将其加入到队列中，并从人所在的位置进行寻路bfs，尝试走到当前箱子的新位置(x', y')四个方向上的相邻位置上，若可以走到，则将对应的状态加入到推箱子的队列中。

若最终箱子可以到达T，那么当前推箱子bfs的轮次就是最终答案，否则返回-1。

最后附上python代码，其中main中的bfs就是推箱子的bfs，而check_path则为寻路bfs：

```python
class Solution(object):
    def minPushBox(self, grid):
        """
        :type grid: List[List[str]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 'T':
                    tx = i
                    ty = j
                elif grid[i][j] == 'B':
                    bx = i
                    by = j
                elif grid[i][j] == 'S':
                    px = i
                    py = j

        if bx == tx and by == ty:
            return 0

        dx = [1, 0, -1, 0]
        dy = [0, -1, 0, 1]

        near_pos = self.check_path(grid, m, n, bx, by, px, py, dx, dy)
        if len(near_pos) == 0:
            return -1
        
        used = [[[False] * 4 for _ in range(n)] for _ in range(m)]
        q = []
        for p in near_pos:
            used[bx][by][p] = True
            q.append([bx, by, p])

        l = 0
        r = len(q)
        res = 0
        while l < r:
            res += 1
            for bx, by, p in q[l : r]:
                next_bx = bx + dx[p]
                next_by = by + dy[p]
                if next_bx == tx and next_by == ty:
                    return res
                if next_bx >= 0 and next_bx < m and next_by >= 0 and next_by < n and grid[next_bx][next_by] != '#':
                    near_pos = self.check_path(grid, m, n, next_bx, next_by, bx, by, dx, dy)
                    for next_p in near_pos:
                        if not used[next_bx][next_by][next_p]:
                            used[next_bx][next_by][next_p] = True
                            q.append([next_bx, next_by, next_p])
            
            l, r = r, len(q)
        
        return -1

    def check_path(self, grid, m, n, bx, by, px, py, dx, dy):
        used = [[False] * n for _ in range(m)]
        used[px][py] = True
        used[bx][by] = True
        q = [[px, py]]
        l = 0
        r = 1
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] != '#' and not used[x][y]:
                    used[x][y] = True
                    q.append([x, y])
                    r += 1

        res = []
        for index in range(4):
            px = bx - dx[index]
            py = by - dy[index]
            if px >= 0 and px < m and py >= 0 and py < n and used[bx - dx[index]][by - dy[index]]:
                res.append(index)
        
        return res
```
