---
title: "1030. 距离顺序排列矩阵单元格"
aliases: ["yiduobo的每日leetcode 1030.距离顺序排列矩阵单元格"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/369603641"
zhihu_id: "369603641"
zhihu_title: "yiduobo的每日leetcode 1030.距离顺序排列矩阵单元格"
question_id: "1030"
question: "距离顺序排列矩阵单元格"
problem_url: "https://leetcode.cn/problems/matrix-cells-in-distance-order/"
created: "2021-05-03T22:35:04+08:00"
updated: "2021-05-03T22:35:04+08:00"
upvotes: 0
comments: 0
---

# 1030. 距离顺序排列矩阵单元格

> **[yiduobo的每日leetcode 1030.距离顺序排列矩阵单元格](https://zhuanlan.zhihu.com/p/369603641) · 知乎 · 2021-05-03 · 赞同 0**
> 力扣：[1030. 距离顺序排列矩阵单元格](https://leetcode.cn/problems/matrix-cells-in-distance-order/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1030.距离顺序排列矩阵单元格

[力扣](https://leetcode-cn.com/problems/matrix-cells-in-distance-order/)

题目要求按照与(r0, c0)的曼哈顿距离从小到大返回矩阵中所有点的坐标，那么我们可以从(r0, c0)开始进行bfs，其中第k轮的bfs处理的点距离(r0, c0)的曼哈顿距离恰好为k，因此bfs完成后，最终的bfs队列就是答案。

最后附上python代码：

```python
class Solution(object):
    def allCellsDistOrder(self, R, C, r0, c0):
        """
        :type R: int
        :type C: int
        :type r0: int
        :type c0: int
        :rtype: List[List[int]]
        """

        q = [[r0, c0]]
        l = 0
        r = 1
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        used = [[False] * C for _ in range(R)]
        used[r0][c0] = True
        while l < r:
            for nowx, nowy in q[l : r]:
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < R and y >= 0 and y < C and not used[x][y]:
                        used[x][y] = True
                        q.append([x, y])
            
            l, r = r, len(q)
        
        return q
```
