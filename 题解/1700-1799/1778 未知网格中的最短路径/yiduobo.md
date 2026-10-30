---
title: "1778. 未知网格中的最短路径"
aliases: ["yiduobo的每日leetcode 1778.未知网格中的最短路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/621206275"
zhihu_id: "621206275"
zhihu_title: "yiduobo的每日leetcode 1778.未知网格中的最短路径"
question_id: "1778"
question: "未知网格中的最短路径"
problem_url: "https://leetcode.cn/problems/shortest-path-in-a-hidden-grid/"
created: "2023-04-12T01:18:52+08:00"
updated: "2023-04-12T01:18:52+08:00"
upvotes: 0
comments: 0
---

# 1778. 未知网格中的最短路径

> **[yiduobo的每日leetcode 1778.未知网格中的最短路径](https://zhuanlan.zhihu.com/p/621206275) · 知乎 · 2023-04-12 · 赞同 0**
> 力扣：[1778. 未知网格中的最短路径](https://leetcode.cn/problems/shortest-path-in-a-hidden-grid/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1778.未知网格中的最短路径

[力扣](https://leetcode.cn/problems/shortest-path-in-a-hidden-grid/)

由于题目中的地图一开始是未知的，那么就必须想办法将整个地图探开，才有最短路径这一说。

不妨设机器人一开始位于坐标(0, 0)，然后向四个方向dfs，将经过的所有坐标都记录下来。同时在dfs过程中利用isTarget判断dfs过程中是否到达过目标位置，若到达过则将其坐标记录为(tx, ty)，否则直接返回-1。在这里需要特别注意的是，执行dfs时需要按照坐标的移动同步移动机器人的位置。

dfs完成后，再从(0, 0)开始进行一次bfs，到达(tx, ty)的轮次即为最终答案。

最后附上python代码：

```python
# """
# This is GridMaster's API interface.
# You should not implement it, or speculate about its implementation
# """
#class GridMaster(object):
#    def canMove(self, direction):
#        """
#        :type direction: str
#        :rtype bool
#        """
#
#    def move(self, direction):
#        """
#        :type direction: str
#        """
#
#    def isTarget(self):
#        """
#        :rtype bool
#        """
#

class Solution(object):
    def findShortestPath(self, master):
        """
        :type master: GridMaster
        :rtype: int
        """

        can_reach = set()
        can_reach.add((0, 0))

        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]
        do = ['U', 'D', 'L', 'R']

        global tx, ty
        tx = ty = None

        def dfs(nowx, nowy):
            global tx, ty
            if master.isTarget():
                tx, ty = nowx, nowy

            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if master.canMove(do[index]) and (x, y) not in can_reach:
                    can_reach.add((x, y))
                    master.move(do[index])
                    dfs(x, y)
                    master.move(do[index ^ 1])
        
        dfs(0, 0)
        
        if tx is None:
            return -1
        
        q = [[0, 0]]
        head, tail = 0, 1
        res = 0
        while head < tail:
            res += 1
            for nowx, nowy in q[head : tail]:
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if (x, y) in can_reach:
                        can_reach.remove((x, y))
                        q.append([x, y])
            
            head, tail = tail, len(q)
            if (tx, ty) not in can_reach:
                break
        
        return res
```
