---
title: "827. 最大人工岛"
aliases: ["yiduobo的每日leetcode 827.最大人工岛"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/hash-table", "题单/网格图", "题单/网格图/一-网格图-DFS"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/344808967"
zhihu_id: "344808967"
zhihu_title: "yiduobo的每日leetcode 827.最大人工岛"
question_id: "827"
question: "最大人工岛"
problem_url: "https://leetcode.cn/problems/making-a-large-island/"
difficulty: "Hard"
rating: 1934
created: "2021-01-20T22:52:39+08:00"
updated: "2021-01-20T22:52:39+08:00"
upvotes: 0
comments: 0
---

# 827. 最大人工岛

> **[yiduobo的每日leetcode 827.最大人工岛](https://zhuanlan.zhihu.com/p/344808967) · 知乎 · 2021-01-20 · 赞同 0**
> 力扣：[827. 最大人工岛](https://leetcode.cn/problems/making-a-large-island/) · Hard · 灵茶山艾府：[计算岛屿的面积+每个格子属于哪个岛，附变形题（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

827.最大人工岛

[力扣](https://leetcode-cn.com/problems/making-a-large-island/)

之前803题打砖块的低配版本

[yiduobo：yiduobo的每日leetcode 803.打砖块](https://zhuanlan.zhihu.com/p/342955042)

由于这里只需要填充一个格子，因此也不需要用到并查集之类的东西。

首先，将初始地图上连续的部分通过bfs进行染色，并统计当前颜色格子的数量。接下来遍历每个空白的格子，检测这个格子能连接哪些颜色，计算这些颜色格子的总数，再加上表示空白格子的1，就可以得到填充这个格子之后连接起来的岛屿的面积。

需要注意两种特殊情况，一是地图是没有空白的格子，那么答案就是地图面积；二是地图上全是空白的格子，那么答案就是1。

最后附上python代码：

```
class Solution(object):
    def largestIsland(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        color = [[None] * n for _ in range(m)]
        now = 0
        q = []
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        cnt = []
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1 and color[i][j] is None:
                    q = [[i, j]]
                    l = 0
                    r = 1
                    color[i][j] = now
                    while l < r:
                        nowx, nowy = q[l]
                        l += 1
                        for index in range(4):
                            x = nowx + dx[index]
                            y = nowy + dy[index]
                            if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 1 and color[x][y] is None:
                                color[x][y] = now
                                q.append([x, y])
                                r += 1

                    cnt.append(r)    
                    now += 1
        
        if now == 0:
            return 1
        res = max(cnt)
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 0:
                    linked_set = set()
                    for index in range(4):
                        x = i + dx[index]
                        y = j + dy[index]
                        if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 1:
                            linked_set.add(color[x][y])
                    
                    res = max(res, sum(cnt[x] for x in linked_set) + 1)
        
        return res
```
