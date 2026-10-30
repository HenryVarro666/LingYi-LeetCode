---
title: "3565. 顺序网格路径覆盖"
aliases: ["yiduobo的每日leetcode 3565.顺序网格路径覆盖"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1911961272473358798"
zhihu_id: "1911961272473358798"
zhihu_title: "yiduobo的每日leetcode 3565.顺序网格路径覆盖"
question_id: "3565"
question: "顺序网格路径覆盖"
problem_url: "https://leetcode.cn/problems/sequential-grid-path-cover/"
created: "2025-05-31T01:53:39+08:00"
updated: "2025-05-31T01:53:39+08:00"
upvotes: 2
comments: 0
---

# 3565. 顺序网格路径覆盖

> **[yiduobo的每日leetcode 3565.顺序网格路径覆盖](https://zhuanlan.zhihu.com/p/1911961272473358798) · 知乎 · 2025-05-31 · 赞同 2**
> 力扣：[3565. 顺序网格路径覆盖](https://leetcode.cn/problems/sequential-grid-path-cover/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

目前已有的算法部分已经写完了，还是老样子，每日leetcode系列先停更一阵子，囤一些题之后再继续写。

3565.顺序网格路径覆盖

[3565. 顺序网格路径覆盖 - 力扣（LeetCode）](https://leetcode.cn/problems/sequential-grid-path-cover/description/)

题目给出一个大小为m \* n的二维数组grid，其中m和n都不超过6。另外给出一个整数k，表示其中有k个单元格包含从1到k的值，每个值恰好出现一次，其余的单元格的值为0。

现在要求找出一条从任意单元格开始的路径，这条路径经过grid中每个单元格恰好一次，且按顺序访问值为1到k的单元格。若不存在合法的路径，返回空数组。

题目要求从找出一条哈密尔顿路径，同时这条路径还需要满足按顺序访问1到k的值。由于题目的数据规模不小，直接使用状态压缩动态规划的话状态数太大，使用插头动态规划的话则不好处理顺序的问题，到了最后还是只好使用dfs来处理，然后看情况进行剪枝。

本题的数据似乎不强，使用最基本的dfs就可以通过了。需要注意本题中路径的起点不一定是1所在的单元格，例如[0, 1, 2]这种情况，必须从最左侧的0开始。

最后附上python代码：

```python
class Solution(object):
    def findPath(self, grid, k):
        """
        :type grid: List[List[int]]
        :type k: int
        :rtype: List[List[int]]
        """
        
        m = len(grid)
        n = len(grid[0])
        vis = [[False] * n for _ in range(m)]
        path = []

        global found
        found = False
        
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        def dfs(level, now_x, now_y, vis, path, nxt_v):
            global found
            if level == m * n:
                found = True
                return
            
            for d in range(4):
                nxt_x = now_x + dx[d]
                nxt_y = now_y + dy[d]
                if 0 <= nxt_x < m and 0 <= nxt_y < n and not vis[nxt_x][nxt_y] and (grid[nxt_x][nxt_y] == 0 or grid[nxt_x][nxt_y] == nxt_v):
                    vis[nxt_x][nxt_y] = True
                    path.append([nxt_x, nxt_y])
                    if grid[nxt_x][nxt_y] == nxt_v:
                        dfs(level + 1, nxt_x, nxt_y, vis, path, nxt_v + 1)
                    else:
                        dfs(level + 1, nxt_x, nxt_y, vis, path, nxt_v)
                    if found:
                        return
                    path.pop()
                    vis[nxt_x][nxt_y] = False
        
        for i in range(m):
            for j in range(n):
                if grid[i][j] <= 1:
                    vis[i][j] = True
                    path.append([i, j])
                    dfs(1, i, j, vis, path, grid[i][j] + 1)
                    if found:
                        return path
                    path.pop()
                    vis[i][j] = False

        return path
```
