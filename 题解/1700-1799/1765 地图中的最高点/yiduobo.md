---
title: "1765. 地图中的最高点"
aliases: ["yiduobo的每日leetcode 1765.地图中的最高点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/460501248"
zhihu_id: "460501248"
zhihu_title: "yiduobo的每日leetcode 1765.地图中的最高点"
question_id: "1765"
question: "地图中的最高点"
problem_url: "https://leetcode.cn/problems/map-of-highest-peak/"
created: "2022-01-21T22:45:27+08:00"
updated: "2022-01-21T22:45:28+08:00"
upvotes: 0
comments: 0
---

# 1765. 地图中的最高点

> **[yiduobo的每日leetcode 1765.地图中的最高点](https://zhuanlan.zhihu.com/p/460501248) · 知乎 · 2022-01-21 · 赞同 0**
> 力扣：[1765. 地图中的最高点](https://leetcode.cn/problems/map-of-highest-peak/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1765.地图中的最高点

[力扣](https://leetcode-cn.com/problems/map-of-highest-peak/)

题目要求相邻位置的高度差不超过1，那么很明显应该从高度位置等于0的水域开始进行bfs，每次将相邻且未访问过的位置的高度置为当前位置高度加1，这样就能使得最高位置的高度最大。

最后附上python代码：

```python
class Solution(object):
    def highestPeak(self, isWater):
        """
        :type isWater: List[List[int]]
        :rtype: List[List[int]]
        """

        m = len(isWater)
        n = len(isWater[0])
        res = [[-1] * n for _ in range(m)]
        q = []
        for i in range(m):
            for j in range(n):
                if isWater[i][j]:
                    q.append([i, j])
                    res[i][j] = 0
        
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        l = 0
        r = len(q)
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x >= 0 and x < m and y >= 0 and y < n and res[x][y] == -1:
                    res[x][y] = res[nowx][nowy] + 1
                    q.append([x, y])
                    r += 1
        
        return res
```
