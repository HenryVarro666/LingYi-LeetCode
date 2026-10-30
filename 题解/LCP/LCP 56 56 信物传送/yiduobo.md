---
title: "LCP 56. 信物传送"
aliases: ["yiduobo的每日leetcode LCP56.信物传送"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/578392402"
zhihu_id: "578392402"
zhihu_title: "yiduobo的每日leetcode LCP56.信物传送"
question_id: "LCP 56"
question: "信物传送"
problem_url: "https://leetcode.cn/problems/6/"
created: "2022-10-29T02:47:31+08:00"
updated: "2022-10-29T02:47:31+08:00"
upvotes: 0
comments: 0
---

# LCP 56. 信物传送

> **[yiduobo的每日leetcode LCP56.信物传送](https://zhuanlan.zhihu.com/p/578392402) · 知乎 · 2022-10-29 · 赞同 0**
> 力扣：[LCP 56. 信物传送](https://leetcode.cn/problems/6/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP56.信物传送

[力扣](https://leetcode.cn/problems/6UEx57/)

首先，从起点开始进行bfs，找出所有不使用技能可以到达的位置。若其中包含终点，那么就返回当前的施法次数，否则就从这些可以到达的位置出发，向四周还没到达过的位置扩展一步，同时将施法次数加上1。

接下来，以这些扩展出来的位置为起点，重复上面的

从当前可达点开始进行bfs -> 判断是否抵达终点 -> 施法扩展新的可到达位置

直到可以到达终点为止。需要注意的是，每一轮的bfs都只需要考虑上一轮施法新扩展出来的位置。

最后附上python代码：

```python
class Solution(object):
    def conveyorBelt(self, matrix, start, end):
        """
        :type matrix: List[str]
        :type start: List[int]
        :type end: List[int]
        :rtype: int
        """

        m = len(matrix)
        n = len(matrix[0])

        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]
        direct_mapping = {'^': 0, '>': 1, 'v': 2, '<': 3}

        vis = [[False] * n for _ in range(m)]
        vis[start[0]][start[1]] = True
        head = 0
        tail = 1
        q = [start]
        res = 0        

        while True:
            tmp = head
            while head < tail:
                nowx, nowy = q[head]
                head += 1

                x = nowx + dx[direct_mapping[matrix[nowx][nowy]]]
                y = nowy + dy[direct_mapping[matrix[nowx][nowy]]]
                if x >= 0 and x < m and y >= 0 and y < n and not vis[x][y]:
                    q.append([x, y])
                    vis[x][y] = True
                    tail += 1
        
            if vis[end[0]][end[1]]:
                return res
        
            head = tmp

            res += 1

            for nowx, nowy in q[head : tail]:
                for index in range(4):
                    if index != direct_mapping[matrix[nowx][nowy]]:
                        x = nowx + dx[index]
                        y = nowy + dy[index]
                        if x >= 0 and x < m and y >= 0 and y < n and not vis[x][y]:
                            q.append([x, y])
                            vis[x][y] = True
            
            head, tail = tail, len(q)
```
