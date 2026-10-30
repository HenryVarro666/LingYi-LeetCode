---
title: "1559. 二维网格图中探测环"
aliases: ["yiduobo的每日leetcode 1559.二维网格图中探测环"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "题单/网格图", "题单/网格图/一-网格图-DFS"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/426983068"
zhihu_id: "426983068"
zhihu_title: "yiduobo的每日leetcode 1559.二维网格图中探测环"
question_id: "1559"
question: "二维网格图中探测环"
problem_url: "https://leetcode.cn/problems/detect-cycles-in-2d-grid/"
difficulty: "Medium"
rating: 1838
created: "2021-10-29T20:11:17+08:00"
updated: "2021-10-29T20:11:17+08:00"
upvotes: 0
comments: 0
---

# 1559. 二维网格图中探测环

> **[yiduobo的每日leetcode 1559.二维网格图中探测环](https://zhuanlan.zhihu.com/p/426983068) · 知乎 · 2021-10-29 · 赞同 0**
> 力扣：[1559. 二维网格图中探测环](https://leetcode.cn/problems/detect-cycles-in-2d-grid/) · Medium · 灵茶山艾府：[网格图 DFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1559.二维网格图中探测环

[力扣](https://leetcode-cn.com/problems/detect-cycles-in-2d-grid/)

根据题目的定义，环的长度要大于等于4，且路径的首尾相连。由于这是一个二维平面，因此可以直接使用bfs来找环。只要bfs队列的长度大于等于4，且当前处理的格子的相邻格子中有已经处理过的格子，并且满足当前格子不是由这个处理过的格子扩展得到的，那么就说明找到了一个环。

于是可以直接遍历整个地图，若当前格子没有被处理过，那么从当前格子开始新一轮的bfs，在bfs过程中判断是否能形成环并更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def containsCycle(self, grid):
        """
        :type grid: List[List[str]]
        :rtype: bool
        """

        m = len(grid)
        n = len(grid[0])
        color = [[0] * n for _ in range(m)]

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        now_color = 0
        for i in range(m):
            for j in range(n):
                if color[i][j] == 0:
                    v = grid[i][j]
                    now_color += 1
                    color[i][j] = 1
                    q = [[i, j, None, None]]
                    l, r = 0, 1
                    while l < r:
                        nowx, nowy, lastx, lasty = q[l]
                        l += 1
                        for index in range(4):
                            x = nowx + dx[index]
                            y = nowy + dy[index]
                            if x >= 0 and x < m and y >= 0 and y < n and (x != lastx or y != lasty) and grid[x][y] == v:
                                if color[x][y] == 0:
                                    q.append([x, y, nowx, nowy])
                                    r += 1
                                    color[x][y] = now_color
                                elif l >= 4:
                                    return True
        
        return False
```
