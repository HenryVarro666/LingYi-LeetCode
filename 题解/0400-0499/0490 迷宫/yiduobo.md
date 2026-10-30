---
title: "490. 迷宫"
aliases: ["yiduobo的每日leetcode 490.迷宫"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/600435015"
zhihu_id: "600435015"
zhihu_title: "yiduobo的每日leetcode 490.迷宫"
question_id: "490"
question: "迷宫"
problem_url: "https://leetcode.cn/problems/the-maze/"
created: "2023-01-22T02:12:33+08:00"
updated: "2023-01-22T02:12:33+08:00"
upvotes: 0
comments: 1
---

# 490. 迷宫

> **[yiduobo的每日leetcode 490.迷宫](https://zhuanlan.zhihu.com/p/600435015) · 知乎 · 2023-01-22 · 赞同 0**
> 力扣：[490. 迷宫](https://leetcode.cn/problems/the-maze/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

490.迷宫

[力扣](https://leetcode.cn/problems/the-maze/)

当球往某个方向踢出去时，其停下的位置也随之确定了。在这里为了提高效率，可以提前预处理出球从每个空格向四个方向踢出去后停下的位置。例如向左侧踢球时，其停下的位置一定是其原始位置左侧最近的障碍物或者墙壁的右侧这个单元格，更具体的计算方式可以参考之前361题的处理方法：

[yiduobo：yiduobo的每日leetcode 361.轰炸敌人](https://zhuanlan.zhihu.com/p/597861507)

预处理完成后，从起点位置开始进行bfs。每轮都尝试向四个方向踢球，并将没有到达过的单元格加入到bfs队列中。bfs完成后，只需检测终点是否在bfs队列中即可。

最后附上python代码：

```python
class Solution(object):
    def hasPath(self, maze, start, destination):
        """
        :type maze: List[List[int]]
        :type start: List[int]
        :type destination: List[int]
        :rtype: bool
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

        vis = set([(start[0], start[1])])
        q = [start]
        head, tail = 0, 1
        while head < tail:
            nowx, nowy = q[head]
            head += 1
            
            for index in range(4):
                if d[index][nowx][nowy] != 0:
                    x = nowx
                    y = nowy
                    if index % 2 == 0:
                        y += d[index][nowx][nowy]
                    else:
                        x += d[index][nowx][nowy]

                    if (x, y) not in vis:
                        vis.add((x, y))
                        q.append([x, y])
                        tail += 1
                    
                    if (destination[0], destination[1]) in vis:
                        return True

        return False
```
