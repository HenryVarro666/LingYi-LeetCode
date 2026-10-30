---
title: "499. 迷宫III & 505. 迷宫II"
aliases: ["yiduobo的每日leetcode 499.迷宫III && 505.迷宫II", "499. 迷宫III", "505. 迷宫II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/600435472"
zhihu_id: "600435472"
zhihu_title: "yiduobo的每日leetcode 499.迷宫III && 505.迷宫II"
question_id: ["499", "505"]
question: ["迷宫III", "迷宫II"]
problem_url: ["https://leetcode.cn/problems/the-maze-iii/", "https://leetcode.cn/problems/the-maze-ii/"]
created: "2023-01-22T02:21:38+08:00"
updated: "2023-01-22T02:21:38+08:00"
upvotes: 0
comments: 0
---

# 499. 迷宫III & 505. 迷宫II

> **[yiduobo的每日leetcode 499.迷宫III && 505.迷宫II](https://zhuanlan.zhihu.com/p/600435472) · 知乎 · 2023-01-22 · 赞同 0**
> 力扣：[499. 迷宫III](https://leetcode.cn/problems/the-maze-iii/)
> 力扣：[505. 迷宫II](https://leetcode.cn/problems/the-maze-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

499.迷宫III && 505.迷宫II

[力扣](https://leetcode.cn/problems/the-maze-iii/)

[力扣](https://leetcode.cn/problems/the-maze-ii/)

两题都是上一篇490题的加强版。

其中505是要求到达终点的最短路径长度，而不是是否可以到达终点。处理方法也很简单，直接在490题的基础上，将最后的bfs改成dijkstra算法计算最短路就行了。

[yiduobo：yiduobo的每日leetcode 490.迷宫](https://zhuanlan.zhihu.com/p/600435015)

而对于499题，需要计算的则是具体的最短路径，同时还有一个变化就是终点从一个常规的空地单元格变成了一种特殊单元格洞。

首先来讨论洞的处理方法。由于球最后会落入洞中，那么就可以将其视为某种特殊的障碍物，不过与常规障碍物不同的是，球遇到常规障碍物将停在障碍物相邻的单元格，而对于洞而言则是会停在洞所在的单元格，因此在预处理球在各个方向上的行进距离时需要对洞进行特殊处理。

接下来是如何计算出具体的路径。最直观的思路还是使用dijkstra算法，不过在这里还需要额外使用一个路径数组path，记录从起点到达每个单元格的最短路径。当最短路径长度被更新时，需要同步更新path数组。另外还有一种情况就是当堆顶弹出的到达某个单元格的距离恰好与到达这个单元格的最短路径长度相等时，也需要更新path数组。

最后附上python代码：

499：

```python
class Solution(object):
    def findShortestWay(self, maze, ball, hole):
        """
        :type maze: List[List[int]]
        :type ball: List[int]
        :type hole: List[int]
        :rtype: str
        """

        m = len(maze)
        n = len(maze[0])

        d = [[[0 for j in range(n)] for i in range(m)] for _ in range(4)]

        def get_len(startx, endx, starty, endy, trans, delta, f):
            if startx < endx:
                deltax = 1
            else:
                deltax = -1

            if starty < endy:
                deltay = 1
            else:
                deltay = -1

            for i in range(startx, endx, deltax):
                cnt = None
                for j in range(starty, endy, deltay):
                    final_i = trans[0] * i + trans[1] * j
                    final_j = trans[0] * j + trans[1] * i
                    if maze[final_i][final_j] == 0:
                        if cnt is None or (final_i == hole[0] and final_j == hole[1]):
                            cnt = 0
                        else:
                            cnt += delta
                            f[final_i][final_j] = cnt
                    else:
                        cnt = None

        get_len(0, m, 0, n, [1, 0], -1, d[0])
        get_len(0, n, 0, m, [0, 1], -1, d[1])
        get_len(0, m, n - 1, -1, [1, 0], 1, d[2])
        get_len(0, n, m - 1, -1, [0, 1], 1, d[3])

        dis = {}
        path = {}
        heap = [[0, ball[0], ball[1], None, None, '']]

        dir_char = ['l', 'u', 'r', 'd']

        while heap:
            nowd, nowx, nowy, prex, prey, choose = heapq.heappop(heap)
            key = (nowx, nowy)

            if key not in dis:
                dis[key] = nowd
                if prex is not None:
                    path[key] = path[(prex, prey)] + choose
                else:
                    path[key] = ''
            else:
                if dis[key] == nowd and prex is not None:
                    new_path = path[(prex, prey)] + choose
                    if new_path < path[key]:
                        path[key] = new_path
                continue
            
            for index in range(4):
                x = nowx
                y = nowy
                if index % 2 == 0:
                    y += d[index][nowx][nowy]
                else:
                    x += d[index][nowx][nowy]
                
                heapq.heappush(heap, [nowd + abs(d[index][nowx][nowy]), x, y, nowx, nowy, dir_char[index]])

        return path.get((hole[0], hole[1]), 'impossible')
```

505：

```
class Solution(object):
    def shortestDistance(self, maze, start, destination):
        """
        :type maze: List[List[int]]
        :type start: List[int]
        :type destination: List[int]
        :rtype: int
        """

        m = len(maze)
        n = len(maze[0])

        d = [[[0 for j in range(n)] for i in range(m)] for _ in range(4)]

        def get_len(startx, endx, starty, endy, trans, delta, f):
            if startx < endx:
                deltax = 1
            else:
                deltax = -1

            if starty < endy:
                deltay = 1
            else:
                deltay = -1

            for i in range(startx, endx, deltax):
                cnt = None
                for j in range(starty, endy, deltay):
                    final_i = trans[0] * i + trans[1] * j
                    final_j = trans[0] * j + trans[1] * i
                    if maze[final_i][final_j] == 0:
                        if cnt is None:
                            cnt = 0
                        else:
                            cnt += delta
                            f[final_i][final_j] = cnt
                    else:
                        cnt = None

        get_len(0, m, 0, n, [1, 0], -1, d[0])
        get_len(0, n, 0, m, [0, 1], -1, d[1])
        get_len(0, m, n - 1, -1, [1, 0], 1, d[2])
        get_len(0, n, m - 1, -1, [0, 1], 1, d[3])

        dis = {}
        path = {}
        heap = [[0, start[0], start[1]]]

        while heap:
            nowd, nowx, nowy = heapq.heappop(heap)
            key = (nowx, nowy)

            if key not in dis:
                dis[key] = nowd
            else:
                continue
            
            for index in range(4):
                x = nowx
                y = nowy
                if index % 2 == 0:
                    y += d[index][nowx][nowy]
                else:
                    x += d[index][nowx][nowy]
                
                heapq.heappush(heap, [nowd + abs(d[index][nowx][nowy]), x, y])

        return dis.get((destination[0], destination[1]), -1)
```
