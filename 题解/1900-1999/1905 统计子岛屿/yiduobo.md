---
title: "1905. 统计子岛屿"
aliases: ["yiduobo的每日leetcode 1905.统计子岛屿"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "题单/网格图", "题单/网格图/一-网格图-DFS"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/481626015"
zhihu_id: "481626015"
zhihu_title: "yiduobo的每日leetcode 1905.统计子岛屿"
question_id: "1905"
question: "统计子岛屿"
problem_url: "https://leetcode.cn/problems/count-sub-islands/"
difficulty: "Medium"
rating: 1679
created: "2022-03-15T23:56:31+08:00"
updated: "2022-03-15T23:56:31+08:00"
upvotes: 0
comments: 0
---

# 1905. 统计子岛屿

> **[yiduobo的每日leetcode 1905.统计子岛屿](https://zhuanlan.zhihu.com/p/481626015) · 知乎 · 2022-03-15 · 赞同 0**
> 力扣：[1905. 统计子岛屿](https://leetcode.cn/problems/count-sub-islands/) · Medium · 灵茶山艾府：[不存在水域即为子岛屿](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1905.统计子岛屿

[力扣](https://leetcode-cn.com/problems/count-sub-islands/)

如果在这里不考虑grid1，只考虑如何找出grid2中的所有岛屿的话，可以使用经典的floodfill算法来处理。具体来说就是遍历地图上的每一个格子，若当前格子没有被访问过，那么就从当前格子开始bfs。本次bfs可以触达到的所有格子就是一个岛屿。

回到本题，现在需要判断grid2中的岛屿是否被grid1中的同一个岛屿完全包含，那么最简单的想法的就是判断grid2中各个岛屿的每个格子在grid1中是否都是1。恰好floodfill将遍历grid2中的每个格子，那么这个判断就可以在floodfill执行的过程中顺便进行。

对于当前处理的岛屿，若在bfs过程中存在某个格子，其在grid1中对应的格子不为1，那么说明当前的岛屿不是grid1的子岛屿。反之，则说明当前岛屿是grid1的子岛屿。

最后附上python代码：

```python
class Solution(object):
    def countSubIslands(self, grid1, grid2):
        """
        :type grid1: List[List[int]]
        :type grid2: List[List[int]]
        :rtype: int
        """

        m = len(grid1)
        n = len(grid1[0])

        used = [[False] * n for _ in range(m)]
        res = 0
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        for i in range(m):
            for j in range(n):
                if grid2[i][j] == 1 and not used[i][j]:
                    q = [[i, j]]
                    used[i][j] = True
                    if grid1[i][j] == 1:
                        flag = True
                    else:
                        flag = False
                    l = 0
                    r = 1
                    while l < r:
                        nowx, nowy = q[l]
                        l += 1
                        for index in range(4):
                            x = nowx + dx[index]
                            y = nowy + dy[index]
                            if x >= 0 and x < m and y >= 0 and y < n and grid2[x][y] == 1 and not used[x][y]:
                                q.append([x, y])
                                used[x][y] = True
                                r += 1
                                if grid1[x][y] == 0:
                                    flag = False
                    
                    if flag:
                        res += 1
        
        return res
```
