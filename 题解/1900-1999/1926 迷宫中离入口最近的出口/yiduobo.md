---
title: "1926. 迷宫中离入口最近的出口"
aliases: ["yiduobo的每日leetcode 1926.迷宫中离入口最近的出口"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "题单/网格图", "题单/网格图/二-网格图-BFS"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/486379164"
zhihu_id: "486379164"
zhihu_title: "yiduobo的每日leetcode 1926.迷宫中离入口最近的出口"
question_id: "1926"
question: "迷宫中离入口最近的出口"
problem_url: "https://leetcode.cn/problems/nearest-exit-from-entrance-in-maze/"
difficulty: "Medium"
rating: 1638
created: "2022-03-23T23:32:59+08:00"
updated: "2022-03-23T23:32:59+08:00"
upvotes: 1
comments: 0
---

# 1926. 迷宫中离入口最近的出口

> **[yiduobo的每日leetcode 1926.迷宫中离入口最近的出口](https://zhuanlan.zhihu.com/p/486379164) · 知乎 · 2022-03-23 · 赞同 1**
> 力扣：[1926. 迷宫中离入口最近的出口](https://leetcode.cn/problems/nearest-exit-from-entrance-in-maze/) · Medium · 灵茶山艾府：[【模板】网格图 BFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1926.迷宫中离入口最近的出口

[力扣](https://leetcode-cn.com/problems/nearest-exit-from-entrance-in-maze/)

题目要求找出从entrance开始需要走多少步走到迷宫的边界上，非常典型的bfs问题。直接从entrance开始bfs，一轮一轮向外扩展直到抵达迷宫边界。若bfs完成后还没有到达边界，那么就返回-1。

最后附上python代码：

```python
class Solution(object):
    def nearestExit(self, maze, entrance):
        """
        :type maze: List[List[str]]
        :type entrance: List[int]
        :rtype: int
        """

        m = len(maze)
        n = len(maze[0])

        q = [[entrance[0], entrance[1]]]
        l = 0
        r = 1
        used = set()
        used.add(entrance[0] * n + entrance[1])
        step = 0
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        while l < r:
            step += 1
            for nowx, nowy in q[l : r]:
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and maze[x][y] != '+' and x * n + y not in used:
                        if x == 0 or y == 0 or x == m - 1 or y == n - 1:
                            return step
                        q.append([x, y])
                        used.add(x * n + y)
            
            l, r = r, len(q)

        return -1
```
