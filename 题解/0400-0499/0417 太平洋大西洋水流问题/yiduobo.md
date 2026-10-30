---
title: "417. 太平洋大西洋水流问题"
aliases: ["yiduobo的每日leetcode 417.太平洋大西洋水流问题"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "题单/网格图", "题单/贪心算法", "题单/网格图/一-网格图-DFS", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/191624895"
zhihu_id: "191624895"
zhihu_title: "yiduobo的每日leetcode 417.太平洋大西洋水流问题"
question_id: "417"
question: "太平洋大西洋水流问题"
problem_url: "https://leetcode.cn/problems/pacific-atlantic-water-flow/"
difficulty: "Medium"
rating: 1900
created: "2020-08-20T22:08:33+08:00"
updated: "2020-08-20T22:08:33+08:00"
upvotes: 0
comments: 0
---

# 417. 太平洋大西洋水流问题

> **[yiduobo的每日leetcode 417.太平洋大西洋水流问题](https://zhuanlan.zhihu.com/p/191624895) · 知乎 · 2020-08-20 · 赞同 0**
> 力扣：[417. 太平洋大西洋水流问题](https://leetcode.cn/problems/pacific-atlantic-water-flow/) · Medium · 灵茶山艾府：[逆向思维（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

417.太平洋大西洋水流问题<https://leetcode-cn.com/problems/pacific-atlantic-water-flow/>

我这里采用的是两次dfs的做法，分别从太平洋和大西洋开始进行dfs，判断地图上的每个点是否能到太平洋和大西洋。具体的dfs过程则是类似于种子染色法。

为了方便起见，对地图上能到太平洋的点或上1，能到大西洋的点或上2，那么最后值为3的点就能同时到两个大洋了。

最后附上python代码：

```python
class Solution(object):
    def pacificAtlantic(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[List[int]]
        """

        if not matrix:
            return []

        m = len(matrix)
        n = len(matrix[0])

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        f = [[0] * n for _ in range(m)]

        used = [[False] * n for _ in range(m)]
        for index in range(m):
            f[index][0] |= 1
            used[index][0] = True
        for index in range(n):
            f[0][index] |= 1
            used[0][index] = True

        for index in range(1, m):
            self.dfs(index, 0, used, matrix, 1, f, dx, dy)
        for index in range(1, n):
            self.dfs(0, index, used, matrix, 1, f, dx, dy)

        used = [[False] * n for _ in range(m)]
        for index in range(m):
            f[index][n - 1] |= 2
            used[index][n - 1] = True
        for index in range(n):
            f[m - 1][index] |= 2
            used[m - 1][index] = True
        
        for index in range(m - 1):
            self.dfs(index, n - 1, used, matrix, 2, f, dx, dy)
        for index in range(n - 1):
            self.dfs(m - 1, index, used, matrix, 2, f, dx, dy)

        res = []
        for i in range(m):
            for j in range(n):
                if f[i][j] == 3:
                    res.append([i, j])
        return res

    def dfs(self, nowx, nowy, used, matrix, val, f, dx, dy):
        for index in range(4):
            x = nowx + dx[index]
            y = nowy + dy[index]
            if x >= 0 and x < len(matrix) and y >= 0 and y < len(matrix[0]) and not used[x][y] and matrix[x][y] >= matrix[nowx][nowy]:
                f[x][y] |= val
                used[x][y] = True
                self.dfs(x, y, used, matrix, val, f, dx, dy)
```
