---
title: "695. 岛屿的最大面积"
aliases: ["yiduobo的每日leetcode 695.岛屿的最大面积"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "题单/网格图", "题单/网格图/一-网格图-DFS"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/312282756"
zhihu_id: "312282756"
zhihu_title: "yiduobo的每日leetcode 695.岛屿的最大面积"
question_id: "695"
question: "岛屿的最大面积"
problem_url: "https://leetcode.cn/problems/max-area-of-island/"
difficulty: "Medium"
created: "2020-11-25T22:51:46+08:00"
updated: "2020-11-25T22:51:46+08:00"
upvotes: 0
comments: 0
---

# 695. 岛屿的最大面积

> **[yiduobo的每日leetcode 695.岛屿的最大面积](https://zhuanlan.zhihu.com/p/312282756) · 知乎 · 2020-11-25 · 赞同 0**
> 力扣：[695. 岛屿的最大面积](https://leetcode.cn/problems/max-area-of-island/) · Medium · 灵茶山艾府：[网格图 DFS（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

695.岛屿的最大面积

[力扣](https://leetcode-cn.com/problems/max-area-of-island/)

比较基础的bfs问题，没有任何特殊变形。直接枚举地图上的每个点，若该点的值为1，那么从该点开始进行bfs，将相邻的值为1的点加入到bfs队列中，同时将其值修改为0。在完成一次bfs之后，这次bfs队列的长度就是这一块岛屿的面积，记录下最大的面积即可。

最后附上python代码:

```python
class Solution(object):
    def maxAreaOfIsland(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        if not grid:
            return 0

        m = len(grid)
        n = len(grid[0])
        res = 0

        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    grid[i][j] = 0
                    q = [[i, j]]
                    l, r = 0, 1
                    while l < r:
                        now_x, now_y = q[l]
                        l += 1
                        for index in range(4):
                            x = now_x + dx[index]
                            y = now_y + dy[index]
                            if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 1:
                                grid[x][y] = 0
                                q.append([x, y])
                                r += 1
                    res = max(res, len(q))
        
        return res
```
