---
title: "1730. 获取食物的最短路径"
aliases: ["yiduobo的每日leetcode 1730.获取食物的最短路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/620469998"
zhihu_id: "620469998"
zhihu_title: "yiduobo的每日leetcode 1730.获取食物的最短路径"
question_id: "1730"
question: "获取食物的最短路径"
problem_url: "https://leetcode.cn/problems/shortest-path-to-get-food/"
created: "2023-04-09T04:08:42+08:00"
updated: "2023-04-09T04:08:42+08:00"
upvotes: 0
comments: 0
---

# 1730. 获取食物的最短路径

> **[yiduobo的每日leetcode 1730.获取食物的最短路径](https://zhuanlan.zhihu.com/p/620469998) · 知乎 · 2023-04-09 · 赞同 0**
> 力扣：[1730. 获取食物的最短路径](https://leetcode.cn/problems/shortest-path-to-get-food/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1730.获取食物的最短路径

[力扣](https://leetcode.cn/problems/shortest-path-to-get-food/)

非常标准的bfs问题。从\*所在的位置开始进行bfs，如果能走到\#所在的位置，那么bfs的轮次即为最终答案。若最终无法走到\#所在位置，那么就返回-1。

最后附上python代码：

```python
class Solution(object):
    def getFood(self, grid):
        """
        :type grid: List[List[str]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '*':
                    sx, sy = i, j
                    grid[i][j] = 'X'
        
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        q = [[sx, sy]]
        head, tail = 0, 1
        step = 0
        while head < tail:
            step += 1
            for nowx, nowy in q[head : tail]:
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n:
                        if grid[x][y] == '#':
                            return step
                    
                        if grid[x][y] == 'O':
                            q.append([x, y])
                            grid[x][y] = 'X'
            
            head, tail = tail, len(q)
        
        return -1
```
