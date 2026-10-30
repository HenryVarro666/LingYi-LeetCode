---
title: "1368. 使网格图至少有一条有效路径的最小代价"
aliases: ["yiduobo的每日leetcode 1368.使网格图至少有一条有效路径的最小代价"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/400471797"
zhihu_id: "400471797"
zhihu_title: "yiduobo的每日leetcode 1368.使网格图至少有一条有效路径的最小代价"
question_id: "1368"
question: "使网格图至少有一条有效路径的最小代价"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid/"
created: "2021-08-16T23:10:13+08:00"
updated: "2021-08-16T23:10:13+08:00"
upvotes: 1
comments: 0
---

# 1368. 使网格图至少有一条有效路径的最小代价

> **[yiduobo的每日leetcode 1368.使网格图至少有一条有效路径的最小代价](https://zhuanlan.zhihu.com/p/400471797) · 知乎 · 2021-08-16 · 赞同 1**
> 力扣：[1368. 使网格图至少有一条有效路径的最小代价](https://leetcode.cn/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1368.使网格图至少有一条有效路径的最小代价

[力扣](https://leetcode-cn.com/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid/)

首先，考虑不修改任何网格的情况。一个自然的想法就是从左上角开始进行一趟bfs，找出所有可以到达的位置。若可以到达右下角，那么答案就是0。

接下来，考虑修改一个网格的情况。此时显然应该修改上一步队列中格子相邻的位置，这样才能有效地扩展可以到达的位置。那么我们可以枚举上一步队列中的所有格子，对于当前处理的格子(nowx, nowy)，我们考察其相邻的四个格子，若某个方向的格子没有被访问过，那么我们可以修改(nowx, nowy)使得对应的格子可以被访问到，于是我们将对应的格子加入到bfs队列中。

此时，bfs队列中扩展出来的这一部分就是修改一个网格可以到达的位置，我们可以从这些格子再开始进行bfs，那么能够到达的格子同样是修改一个网格可以到达的位置。若可以到达右下角，那么答案就是0。

接下来，我们考虑修改两个网格的情况。此时不应该再修改第1步中bfs队列中的格子，因为所有相邻格子已经被处理过了，因此我们只需考察第二步队列中的格子相邻的格子。

更一般的，我们重复这个过程，每次先bfs扩展当前队列，若没有到达终点，那么我们将上一轮队列中的格子的相邻格子加入到队列中，然后重复这个过程直到到达终点为止。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        used = [[False] * n for _ in range(m)]
        used[0][0] = True

        q = [[0, 0]]
        l = 0
        r = 1
        dx = [0, 0, 0, 1, -1]
        dy = [0, 1, -1, 0, 0]
        res = 0
        while not used[-1][-1]:
            last_l = l
            while l < r:
                nowx, nowy = q[l]
                l += 1
                d = grid[nowx][nowy]
                x = nowx + dx[d]
                y = nowy + dy[d]
                if x >= 0 and x < m and y >= 0 and y < n and not used[x][y]:
                    q.append([x, y])
                    used[x][y] = True
                    if used[-1][-1]:
                        return res
                    r += 1

            res += 1

            new_r = r
            for nowx, nowy in q[last_l : r]:
                for index in range(1, 5):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and not used[x][y]:
                        q.append([x, y])
                        used[x][y] = True
                        if used[-1][-1]:
                            return res
                        new_r += 1
            
            r = new_r

        return res
```
