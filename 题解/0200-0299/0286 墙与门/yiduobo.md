---
title: "286. 墙与门"
aliases: ["yiduobo的每日leetcode 286.墙与门"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/594786503"
zhihu_id: "594786503"
zhihu_title: "yiduobo的每日leetcode 286.墙与门"
question_id: "286"
question: "墙与门"
problem_url: "https://leetcode.cn/problems/walls-and-gates/"
created: "2022-12-27T22:06:59+08:00"
updated: "2022-12-27T22:06:59+08:00"
upvotes: 0
comments: 0
---

# 286. 墙与门

> **[yiduobo的每日leetcode 286.墙与门](https://zhuanlan.zhihu.com/p/594786503) · 知乎 · 2022-12-27 · 赞同 0**
> 力扣：[286. 墙与门](https://leetcode.cn/problems/walls-and-gates/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

286.墙与门

[力扣](https://leetcode.cn/problems/walls-and-gates/)

从地图上的所有门开始向四周进行bfs，对于某个单元格，其首先被访问到的轮次就是其到达最近的门的距离了。

最后附上python代码：

```python
class Solution(object):
    def wallsAndGates(self, rooms):
        """
        :type rooms: List[List[int]]
        :rtype: None Do not return anything, modify rooms in-place instead.
        """

        m = len(rooms)
        n = len(rooms[0])

        q = []
        for i in range(m):
            for j in range(n):
                if rooms[i][j] == 0:
                    q.append([i, j])
        
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        head, tail = 0, len(q)
        while head < tail:
            for nowx, nowy in q[head : tail]:
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and rooms[x][y] > rooms[nowx][nowy] + 1:
                        rooms[x][y] = rooms[nowx][nowy] + 1
                        q.append([x, y])
            
            head, tail = tail, len(q)

        return rooms
```
