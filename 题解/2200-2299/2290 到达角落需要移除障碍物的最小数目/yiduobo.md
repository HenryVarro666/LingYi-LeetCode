---
title: "2290. 到达角落需要移除障碍物的最小数目"
aliases: ["yiduobo的每日leetcode 2290.到达角落需要移除障碍物的最小数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/breadth-first-search", "leetcode/graph", "leetcode/shortest-path", "leetcode/bfs", "leetcode/shuang-duan-dui-lie", "题单/网格图", "题单/网格图/三-网格图-0-1-BFS"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/553246685"
zhihu_id: "553246685"
zhihu_title: "yiduobo的每日leetcode 2290.到达角落需要移除障碍物的最小数目"
question_id: "2290"
question: "到达角落需要移除障碍物的最小数目"
problem_url: "https://leetcode.cn/problems/minimum-obstacle-removal-to-reach-corner/"
difficulty: "Hard"
rating: 2138
created: "2022-08-13T01:31:01+08:00"
updated: "2022-08-13T01:31:01+08:00"
upvotes: 0
comments: 0
---

# 2290. 到达角落需要移除障碍物的最小数目

> **[yiduobo的每日leetcode 2290.到达角落需要移除障碍物的最小数目](https://zhuanlan.zhihu.com/p/553246685) · 知乎 · 2022-08-13 · 赞同 0**
> 力扣：[2290. 到达角落需要移除障碍物的最小数目](https://leetcode.cn/problems/minimum-obstacle-removal-to-reach-corner/) · Hard · 灵茶山艾府：[0-1 BFS 线性做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2290.到达角落需要移除障碍物的最小数目

[力扣](https://leetcode.cn/problems/minimum-obstacle-removal-to-reach-corner/)

由于题目的地图中并不存在特殊的道具之类的东西，因此是没有必要两次走到同一个格子上的，因此在这里可以认为移除一个障碍物相当于穿墙走到这个障碍物的格子上。

随着可移除障碍物的增加，可活动的范围也是逐渐增加的。更准确的说法是，当可移除障碍物的数量为k时，可活动的范围可以分成两个部分。第一个部分是当可移除障碍物的数量为k - 1时可以活动的范围，第二个部分则是在上面这个范围的基础上，穿过一个相邻的未走到障碍物之后可到达的范围。

也就是说，在这里可以先从左上角开始进行bfs，找出不移除障碍物时的可活动范围。若不能到达地图右下角，则可以从1开始逐个增加可移除障碍物的数量。每一轮都先找出与上一轮新增的可活动范围相邻，且没有到达过的障碍物，然后从这些障碍物开始进行bfs，确定新增的可活动范围。重复这个过程直到某一轮可以到达地图的右下角为止。

需要注意的是，每一轮只需要找出与上一轮新增的可活动范围相邻的障碍物，而不是所有与当前可活动范围相邻的障碍物，因为除了与上一轮新增的活动范围相邻的障碍物之外，其他的障碍物在之前的轮次就已经被处理过了，所以在这里没必要遍历所有的可活动范围。

最后附上python代码：

```python
class Solution(object):
    def minimumObstacles(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        used = [[False] * n for _ in range(m)]
        used[0][0] = True

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        def bfs(q, used):
            l, r = 0, len(q)
            while l < r:
                nowx, nowy = q[l]
                l += 1
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and not used[x][y] and grid[x][y] == 0:
                        q.append([x, y])
                        r += 1
                        used[x][y] = True
        
        q = [[0, 0]]
        res = 0
        while not used[m - 1][n - 1]:
            bfs(q, used)
            if not used[m - 1][n - 1]:
                res += 1
                next_q = []
                for nowx, nowy in q:
                    for index in range(4):
                        x = nowx + dx[index]
                        y = nowy + dy[index]
                        if x >= 0 and x < m and y >= 0 and y < n and not used[x][y] and grid[x][y] == 1:
                            next_q.append([x, y])
                            used[x][y] = True
                
                q = next_q[:]
        
        return res
```
