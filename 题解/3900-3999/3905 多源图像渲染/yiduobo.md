---
title: "3905. 多源图像渲染"
aliases: ["yiduobo的每日leetcode 3905.多源图像渲染"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/queue", "leetcode/sorting", "题单/网格图", "题单/网格图/二-网格图-BFS"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2029684593570194594"
zhihu_id: "2029684593570194594"
zhihu_title: "yiduobo的每日leetcode 3905.多源图像渲染"
question_id: "3905"
question: "多源图像渲染"
problem_url: "https://leetcode.cn/problems/multi-source-flood-fill/"
difficulty: "Medium"
rating: 1671
created: "2026-04-20T22:21:19+08:00"
updated: "2026-04-20T22:21:22+08:00"
upvotes: 1
comments: 0
---

# 3905. 多源图像渲染

> **[yiduobo的每日leetcode 3905.多源图像渲染](https://zhuanlan.zhihu.com/p/2029684593570194594) · 知乎 · 2026-04-20 · 赞同 1**
> 力扣：[3905. 多源图像渲染](https://leetcode.cn/problems/multi-source-flood-fill/) · Medium · 灵茶山艾府：[排序之后 BFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3905.多源图像渲染

<https://leetcode.cn/problems/multi-source-flood-fill/description/>

题目给出两个整数n和m，表示一个网格的行数和列数。

同时给出一个二维整数数组sources，其中sources\[index\] \= \[r\[index\], c\[index\], color\[index\]\]，表示单元格(r\[index\], c\[index\])初始被涂上颜色color\[index\]。所有其他单元格一开始都是无色，用0表示。

在每一单位时间内，所有已经着色的单元格都会向四个相邻方向扩散，将这四个方向上相邻的无色单元格染色。所有的扩散同时发生，若多个颜色在同一时间到达某个无色单元格，那么这个单元格将被当前到达的所有颜色中具有最大值的颜色染色。

这个过程持续进行，直到整个网格都被染上颜色。

问最终网格的颜色状态是什么样的。

直接以初始有色的单元格作为初始的队列，执行bfs进行染色即可。

需要注意多种颜色同时到达时要取最大的颜色染色，因此在这里需要先将初始队列按照颜色从大到小进行排序，这样一来就能保证在一个扩展的轮次中，较大的颜色先与较小的颜色到达同一单元格，从而保证多种颜色同时到达时，具有较大值的颜色能染上色。

最后附上python代码：

```python
class Solution(object):
    def colorGrid(self, n, m, sources):
        """
        :type n: int
        :type m: int
        :type sources: List[List[int]]
        :rtype: List[List[int]]
        """
        
        res = [[0] * m for _ in range(n)]
        q = []
        for x, y, c in sources:
            q.append((x, y, c))
            res[x][y] = c
        
        q.sort(key=lambda d:-d[2])
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        head, tail = 0, len(q)
        while head < tail:
            for nowx, nowy, c in q[head : tail]:
                for d in range(4):
                    x = nowx + dx[d]
                    y = nowy + dy[d]
                    if 0 <= x < n and 0 <= y < m and res[x][y] == 0:
                        res[x][y] = c
                        q.append((x, y, c))
        
            head, tail = tail, len(q)
        
        return res
```
