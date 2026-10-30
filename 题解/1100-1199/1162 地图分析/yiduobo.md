---
title: "1162. 地图分析"
aliases: ["yiduobo的每日leetcode 1162.地图分析"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/378712883"
zhihu_id: "378712883"
zhihu_title: "yiduobo的每日leetcode 1162.地图分析"
question_id: "1162"
question: "地图分析"
problem_url: "https://leetcode.cn/problems/as-far-from-land-as-possible/"
created: "2021-06-07T21:49:56+08:00"
updated: "2021-06-07T21:49:56+08:00"
upvotes: 0
comments: 0
---

# 1162. 地图分析

> **[yiduobo的每日leetcode 1162.地图分析](https://zhuanlan.zhihu.com/p/378712883) · 知乎 · 2021-06-07 · 赞同 0**
> 力扣：[1162. 地图分析](https://leetcode.cn/problems/as-far-from-land-as-possible/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1162.地图分析

[力扣](https://leetcode-cn.com/problems/as-far-from-land-as-possible/)

题目要求离所有1最远的0的曼哈顿距离，那么我们可以从所有的1开始进行bfs染色，每一轮将相邻的格子中的0变成1，同时将其加入bfs队列中，那么最终bfs的轮次就是要求的最远距离。

最后附上python代码：

```python
class Solution(object):
    def maxDistance(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        
        q = []
        n = len(grid)
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 1:
                    q.append([i, j])
        
        l = 0
        r = len(q)
        if r == 0 or r == n * n:
            return -1
        res = 0
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while l < r:
            res += 1
            for nowx, nowy in q[l : r]:
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < n and y >= 0 and y < n and grid[x][y] == 0:
                        q.append([x, y])
                        grid[x][y] = 1
            
            l, r = r, len(q)

        return res - 1
```
