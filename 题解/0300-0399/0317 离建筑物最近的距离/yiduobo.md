---
title: "317. 离建筑物最近的距离"
aliases: ["yiduobo的每日leetcode 317.离建筑物最近的距离"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/596116525"
zhihu_id: "596116525"
zhihu_title: "yiduobo的每日leetcode 317.离建筑物最近的距离"
question_id: "317"
question: "离建筑物最近的距离"
problem_url: "https://leetcode.cn/problems/shortest-distance-from-all-buildings/"
created: "2023-01-03T01:22:04+08:00"
updated: "2023-01-03T01:22:04+08:00"
upvotes: 0
comments: 2
---

# 317. 离建筑物最近的距离

> **[yiduobo的每日leetcode 317.离建筑物最近的距离](https://zhuanlan.zhihu.com/p/596116525) · 知乎 · 2023-01-03 · 赞同 0**
> 力扣：[317. 离建筑物最近的距离](https://leetcode.cn/problems/shortest-distance-from-all-buildings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

317.离建筑物最近的距离

[力扣](https://leetcode.cn/problems/shortest-distance-from-all-buildings/)

本题看上去与之前的296题很像，但是本题的建筑物是无法通过的，而且还可能存在障碍单元格，因此不能使用之前的贪心法。

注意到题目的数据规模不大，因此可以枚举答案的位置然后进行bfs，或者从每一栋建筑开始进行bfs，找出所有建筑都可以到达且距离之和最近的单元格。我在这里采用的是后面这种做法，因为当建筑较少时，后面的算法需要执行bfs的总次数较少，而建筑较多时，由于建筑自身会堵路，因此地图会比较拥挤，使得单次bfs执行的轮次较短。综合来看，采用后面这种做法的效率更好。

最后附上python代码：

```python
class Solution(object):
    def shortestDistance(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        
        dis = []

        def bfs(x, y):
            q = [[x, y]]
            dis.append([[-1 for j in range(n)] for i in range(m)])
            head, tail = 0, 1
            vis = set([x * n + y])
            step = 0
            dx = [0, 1, 0, -1]
            dy = [1, 0, -1, 0]

            while head < tail:
                step += 1
                for nowx, nowy in q[head : tail]:
                    for index in range(4):
                        x = nowx + dx[index]
                        y = nowy + dy[index]
                        if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 0 and x * n + y not in vis:
                            vis.add(x * n + y)
                            q.append([x, y])
                            dis[-1][x][y] = step
                
                head, tail = tail, len(q)

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    bfs(i, j)

        res = -1
        for i in range(m):
            for j in range(n):
                tot = 0
                for p in range(len(dis)):
                    if dis[p][i][j] == -1:
                        tot = -1
                        break
                    else:
                        tot += dis[p][i][j]
                
                if tot != -1 and (res == -1 or res > tot):
                    res = tot
        
        return res
```
