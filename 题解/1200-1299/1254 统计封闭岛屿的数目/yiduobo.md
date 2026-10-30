---
title: "1254. 统计封闭岛屿的数目"
aliases: ["yiduobo的每日leetcode 1254.统计封闭岛屿的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/graph", "leetcode/recursion", "题单/网格图", "题单/网格图/一-网格图-DFS"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/386283764"
zhihu_id: "386283764"
zhihu_title: "yiduobo的每日leetcode 1254.统计封闭岛屿的数目"
question_id: "1254"
question: "统计封闭岛屿的数目"
problem_url: "https://leetcode.cn/problems/number-of-closed-islands/"
difficulty: "Medium"
rating: 1659
created: "2021-07-03T13:43:02+08:00"
updated: "2021-07-03T13:43:02+08:00"
upvotes: 0
comments: 0
---

# 1254. 统计封闭岛屿的数目

> **[yiduobo的每日leetcode 1254.统计封闭岛屿的数目](https://zhuanlan.zhihu.com/p/386283764) · 知乎 · 2021-07-03 · 赞同 0**
> 力扣：[1254. 统计封闭岛屿的数目](https://leetcode.cn/problems/number-of-closed-islands/) · Medium · 灵茶山艾府：[两种思路：先外后内/出界标记（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1254.统计封闭岛屿的数目

[力扣](https://leetcode-cn.com/problems/number-of-closed-islands/)

题目描述中的封闭岛屿要求所有相邻区域都是水域，因此与地图边缘相邻的连通块就不可能是最终的答案。因此我们可以先枚举地图的边缘，记录下其中0的位置，然后从这些位置开始进行bfs，并将遍历到的格子置为1。

接下来，我们枚举地图中的每个格子，若当前格子值为0，就从这个格子开始进行bfs，并将bfs到的位置进行染色。

扫描完成后，最终染色的数目就是最终答案了。

最后附上python代码：

```python
class Solution(object):
    def closedIsland(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        q = []
        for i in range(n):
            if grid[0][i] == 0:
                q.append([0, i])
                grid[0][i] = 1
            if grid[m - 1][i] == 0:
                q.append([m - 1, i])
                grid[m - 1][i] = 1
        
        for i in range(m):
            if grid[i][0] == 0:
                q.append([i, 0])
                grid[i][0] = 1
            if grid[i][n - 1] == 0:
                q.append([i, n - 1])
                grid[i][n - 1] = 1

        l = 0
        r = len(q)
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 0:
                    grid[x][y] = 1
                    q.append([x, y])
                    r += 1
        
        now_color = 2
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 0:
                    grid[i][j] = now_color
                    q = [[i, j]]
                    l = 0
                    r = 1
                    while l < r:
                        nowx, nowy = q[l]
                        l += 1
                        for index in range(4):
                            x = nowx + dx[index]
                            y = nowy + dy[index]
                            if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 0:
                                grid[x][y] = now_color
                                q.append([x, y])
                                r += 1
                    
                    now_color += 1
        
        return now_color - 2
```
