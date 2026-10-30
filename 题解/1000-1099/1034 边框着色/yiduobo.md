---
title: "1034. 边框着色"
aliases: ["yiduobo的每日leetcode 1034.边框着色"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/369945130"
zhihu_id: "369945130"
zhihu_title: "yiduobo的每日leetcode 1034.边框着色"
question_id: "1034"
question: "边框着色"
problem_url: "https://leetcode.cn/problems/coloring-a-border/"
created: "2021-05-05T21:38:43+08:00"
updated: "2021-05-05T21:38:43+08:00"
upvotes: 0
comments: 0
---

# 1034. 边框着色

> **[yiduobo的每日leetcode 1034.边框着色](https://zhuanlan.zhihu.com/p/369945130) · 知乎 · 2021-05-05 · 赞同 0**
> 力扣：[1034. 边框着色](https://leetcode.cn/problems/coloring-a-border/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1034.边框着色

[力扣](https://leetcode-cn.com/problems/coloring-a-border/)

题目要求将连通分量的边框染色，判断边框相对来说麻烦一点，不妨换一种思路，从连通分量的内部区域着手。一个很容易得到的性质是对于连通分量的任意内部区域(x, y)而言，其四周，即(x - 1, y)、(x + 1, y)、(x, y - 1)、(x, y + 1)必然与(x, y)同色。那么如果我们按照普通bfs的过程来计算连通分量的话，内部区域将被访问到4次，而非内部区域则不足4次。于是我们可以直接从(r0, c0)开始进行bfs计算连通分量，并记录下bfs过程中每个节点被访问的次数。bfs结束后，对连通分量中访问次数不足4次的节点进行染色即可。

最后附上python代码：

```python
class Solution(object):
    def colorBorder(self, grid, r0, c0, color):
        """
        :type grid: List[List[int]]
        :type r0: int
        :type c0: int
        :type color: int
        :rtype: List[List[int]]
        """

        origin = grid[r0][c0]
        q = [[r0, c0]]
        l = 0
        r = 1
        m = len(grid)
        n = len(grid[0])
        used = [[0] * n for _ in range(m)]
        used[r0][c0] = 1
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == origin:
                    used[x][y] += 1
                    if used[x][y] == 1:
                        q.append([x, y])
                        r += 1
        
        used[r0][c0] -= 1

        for x, y in q:
            if used[x][y] < 4:
                grid[x][y] = color
        
        return grid
```
