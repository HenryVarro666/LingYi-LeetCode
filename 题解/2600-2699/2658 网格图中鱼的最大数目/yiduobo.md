---
title: "2658. 网格图中鱼的最大数目"
aliases: ["yiduobo的每日leetcode 2658.网格图中鱼的最大数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "题单/网格图", "题单/网格图/一-网格图-DFS"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/648110996"
zhihu_id: "648110996"
zhihu_title: "yiduobo的每日leetcode 2658.网格图中鱼的最大数目"
question_id: "2658"
question: "网格图中鱼的最大数目"
problem_url: "https://leetcode.cn/problems/maximum-number-of-fish-in-a-grid/"
difficulty: "Medium"
rating: 1490
created: "2023-08-05T00:29:37+08:00"
updated: "2023-08-05T00:29:37+08:00"
upvotes: 1
comments: 0
---

# 2658. 网格图中鱼的最大数目

> **[yiduobo的每日leetcode 2658.网格图中鱼的最大数目](https://zhuanlan.zhihu.com/p/648110996) · 知乎 · 2023-08-05 · 赞同 1**
> 力扣：[2658. 网格图中鱼的最大数目](https://leetcode.cn/problems/maximum-number-of-fish-in-a-grid/) · Medium · 灵茶山艾府：[网格图 DFS 模板（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2658.网格图中鱼的最大数目

[力扣](https://leetcode.cn/problems/maximum-number-of-fish-in-a-grid/)

经典的网格图找连通块的问题，常规做法是使用floodfill来处理。具体来说就是从左上角开始向右下角遍历每个单元格，若当前单元格是水域，且之前没有被访问过，那么就从当前单元格开始进行bfs，找出与当前单元格连通的所有单元格，并使用这些单元格的数值之和更新答案。

最后附上python代码：

```python
class Solution(object):
    def findMaxFish(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        vis = [[False] * n for _ in range(m)]

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        res = 0
        for i in range(m):
            for j in range(n):
                if not vis[i][j] and grid[i][j] > 0:
                    vis[i][j] = True
                    q = [[i, j]]
                    s = grid[i][j]
                    head, tail = 0, 1
                    while head < tail:
                        nowx, nowy = q[head]
                        head += 1
                        for index in range(4):
                            x = nowx + dx[index]
                            y = nowy + dy[index]
                            if x >= 0 and x < m and y >= 0 and y < n and not vis[x][y] and grid[x][y] > 0:
                                vis[x][y] = True
                                q.append([x, y])
                                tail += 1
                                s += grid[x][y]
                    
                    res = max(res, s)
        
        return res
```
