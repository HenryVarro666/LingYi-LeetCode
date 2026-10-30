---
title: "2328. 网格图中递增路径的数目"
aliases: ["yiduobo的每日leetcode 2328.网格图中递增路径的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/二-网格图-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/558316587"
zhihu_id: "558316587"
zhihu_title: "yiduobo的每日leetcode 2328.网格图中递增路径的数目"
question_id: "2328"
question: "网格图中递增路径的数目"
problem_url: "https://leetcode.cn/problems/number-of-increasing-paths-in-a-grid/"
difficulty: "Hard"
rating: 2001
created: "2022-08-27T00:10:16+08:00"
updated: "2022-08-27T00:10:16+08:00"
upvotes: 0
comments: 0
---

# 2328. 网格图中递增路径的数目

> **[yiduobo的每日leetcode 2328.网格图中递增路径的数目](https://zhuanlan.zhihu.com/p/558316587) · 知乎 · 2022-08-27 · 赞同 0**
> 力扣：[2328. 网格图中递增路径的数目](https://leetcode.cn/problems/number-of-increasing-paths-in-a-grid/) · Hard · 灵茶山艾府：[记忆化搜索（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2328.网格图中递增路径的数目

[力扣](https://leetcode.cn/problems/number-of-increasing-paths-in-a-grid/)

经典的记忆化搜索问题。

令f[i][j]表示从格子(i, j)出发的递增路径数目，那么对于f[i][j]，可以枚举与(i, j)相邻的四个格子(i + 1, j), (i, j + 1), (i - 1, j), (i, j - 1)。对于当前枚举到的格子(nexti, nextj)，若没有超出边界，且满足grid[nexti][nextj] > grid][i][j]，那么从(i, j)出发的路径就可以选择走到(nexti, nextj)，于是就有f[i][j] +\= f[nexti][nextj]。

遍历完所有相邻的格子后，还需要将f[i][j]额外加上1，因为在(i, j)原地不动也是一条合法的路径。

对于记忆化搜索的启动，通常是在最外部遍历所有可能的状态，若当前遍历到状态还没有被求解过，即对应的f还是初始值，那么就递归求解当前状态。

最后附上python代码：

```python
class Solution(object):
    def countPaths(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        mod = 10 ** 9 + 7
        m = len(grid)
        n = len(grid[0])
        
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        def dfs(x, y, f):
            if f[x][y] == 0:
                for index in range(4):
                    next_x = x + dx[index]
                    next_y = y + dy[index]
                    if next_x >= 0 and next_x < m and next_y >= 0 and next_y < n and grid[next_x][next_y] > grid[x][y]:
                        f[x][y] += dfs(next_x, next_y, f)
                        if f[x][y] >= mod:
                            f[x][y] -= mod
                
                f[x][y] += 1
                if f[x][y] >= mod:
                    f[x][y] -= mod
            
            return f[x][y]

        f = [[0] * n for _ in range(m)]
        res = 0
        for i in range(m):
            for j in range(n):
                res += dfs(i, j, f)
                if res >= mod:
                    res -= mod
        
        return res
```
