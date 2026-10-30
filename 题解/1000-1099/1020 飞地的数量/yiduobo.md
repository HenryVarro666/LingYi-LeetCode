---
title: "1020. 飞地的数量"
aliases: ["yiduobo的每日leetcode 1020.飞地的数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/368644897"
zhihu_id: "368644897"
zhihu_title: "yiduobo的每日leetcode 1020.飞地的数量"
question_id: "1020"
question: "飞地的数量"
problem_url: "https://leetcode.cn/problems/number-of-enclaves/"
created: "2021-04-28T21:53:50+08:00"
updated: "2021-04-28T21:53:50+08:00"
upvotes: 1
comments: 0
---

# 1020. 飞地的数量

> **[yiduobo的每日leetcode 1020.飞地的数量](https://zhuanlan.zhihu.com/p/368644897) · 知乎 · 2021-04-28 · 赞同 1**
> 力扣：[1020. 飞地的数量](https://leetcode.cn/problems/number-of-enclaves/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1020.飞地的数量

[力扣](https://leetcode-cn.com/problems/number-of-enclaves/)

经典的bfs题目。题目中所说的飞地实际上指的是不与四条边上相连的点，那么我们可以反过来从四条边上的点开始进行bfs，那么最后没有被遍历到的点就是飞地。

首先将四条边上所有值为1的点加入到bfs队列中，并将这些点的值置为2。

接下来开始执行bfs，每次将当前点周围值为1的点加入到bfs队列中，同时也将这些新加入的点的值置为2。

当bfs结束时，地图中剩余值为1的点的数量就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def numEnclaves(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        q = []
        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            if grid[i][0] == 1:
                grid[i][0] = 2
                q.append([i, 0])
            if grid[i][n - 1] == 1:
                grid[i][n - 1] = 2
                q.append([i, n - 1])
        
        for j in range(n):
            if grid[0][j] == 1:
                grid[0][j] = 2
                q.append([0, j])
            if grid[m - 1][j] == 1:
                grid[m - 1][j] = 2
                q.append([m - 1, j])
        
        l = 0
        r = len(q)
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x > 0 and x < m - 1 and y > 0 and y < n - 1 and grid[x][y] == 1:
                    q.append([x, y])
                    r += 1
                    grid[x][y] = 2

        res = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    res += 1
        
        return res
```
