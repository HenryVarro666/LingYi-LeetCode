---
title: "1091. 二进制矩阵中的最短路径"
aliases: ["yiduobo的每日leetcode 1091.二进制矩阵中的最短路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/373384821"
zhihu_id: "373384821"
zhihu_title: "yiduobo的每日leetcode 1091.二进制矩阵中的最短路径"
question_id: "1091"
question: "二进制矩阵中的最短路径"
problem_url: "https://leetcode.cn/problems/shortest-path-in-binary-matrix/"
created: "2021-05-18T22:17:23+08:00"
updated: "2021-05-18T22:17:23+08:00"
upvotes: 0
comments: 0
---

# 1091. 二进制矩阵中的最短路径

> **[yiduobo的每日leetcode 1091.二进制矩阵中的最短路径](https://zhuanlan.zhihu.com/p/373384821) · 知乎 · 2021-05-18 · 赞同 0**
> 力扣：[1091. 二进制矩阵中的最短路径](https://leetcode.cn/problems/shortest-path-in-binary-matrix/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1091.二进制矩阵中的最短路径

[力扣](https://leetcode-cn.com/problems/shortest-path-in-binary-matrix/)

首先判断特殊情况。当起点或终点对应的值为1时，直接返回-1。若边长为1，那么答案为1。

接下来执行传统的bfs，不过需要注意这里有八个方向。若bfs过程中达到了终点，那么轮次即为最终答案，否则说明无法到达终点，此时应该返回-1。

最后附上python代码：

```python
class Solution(object):
    def shortestPathBinaryMatrix(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        n = len(grid)
        if grid[0][0] == 1 or grid[n - 1][n - 1] == 1:
            return -1
        
        if n == 1:
            return 1

        used = [[False] * n for _ in range(n)]
        q = [[0, 0]]
        used[0][0] = True
        dx = [0, 1, 1, 1, 0, -1, -1, -1]
        dy = [1, 1, 0, -1, -1, -1, 0, 1]
        l = 0
        r = 1
        step = 1
        while l < r:
            step += 1
            for nowx, nowy in q[l : r]:
                for index in range(8):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < n and y >= 0 and y < n and grid[x][y] == 0 and not used[x][y]:
                        q.append([x, y])
                        used[x][y] = True
                        if used[n - 1][n - 1]:
                            return step
            l, r = r, len(q)
        
        return -1
```
