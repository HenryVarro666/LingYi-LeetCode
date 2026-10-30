---
title: "994. 腐烂的橘子"
aliases: ["yiduobo的每日leetcode 994.腐烂的橘子"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "题单/网格图", "题单/LeetCode-热题-100", "题单/网格图/二-网格图-BFS", "题单/LeetCode-热题-100/图论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/365205793"
zhihu_id: "365205793"
zhihu_title: "yiduobo的每日leetcode 994.腐烂的橘子"
question_id: "994"
question: "腐烂的橘子"
problem_url: "https://leetcode.cn/problems/rotting-oranges/"
difficulty: "Medium"
created: "2021-04-15T22:02:49+08:00"
updated: "2021-04-15T22:02:49+08:00"
upvotes: 0
comments: 0
---

# 994. 腐烂的橘子

> **[yiduobo的每日leetcode 994.腐烂的橘子](https://zhuanlan.zhihu.com/p/365205793) · 知乎 · 2021-04-15 · 赞同 0**
> 力扣：[994. 腐烂的橘子](https://leetcode.cn/problems/rotting-oranges/) · Medium · 灵茶山艾府：[多源 BFS，附变形题（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

994.腐烂的橘子

[力扣](https://leetcode-cn.com/problems/rotting-oranges/)

首先，对于没有好橘子的情况直接返回0，否则就直接使用bfs来模拟腐烂扩散的过程。

初始化bfs队列为所有已经腐烂的橘子，接下来每一轮bfs都让这些腐烂的橘子感染相邻的好橘子。若某一轮好橘子的数量为0，那么当前bfs的轮次即为答案。若bfs完成后依然有好橘子，那么就返回-1。

最后附上python代码：

```python
class Solution(object):
    def orangesRotting(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        q = []
        m = len(grid)
        n = len(grid[0])
        cnt = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    cnt += 1
                elif grid[i][j] == 2:
                    q.append([i, j])

        if cnt == 0:
            return 0
        
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        l, r = 0, len(q)
        step = 0
        while l < r:
            step += 1
            for now_x, now_y in q[l: r]:
                for index in range(4):
                    x = now_x + dx[index]
                    y = now_y + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n:
                        if grid[x][y] == 1:
                            q.append([x, y])
                            cnt -= 1
                            if cnt == 0:
                                return step
                            grid[x][y] = 2
            
            l, r = r, len(q)

        return -1
```
