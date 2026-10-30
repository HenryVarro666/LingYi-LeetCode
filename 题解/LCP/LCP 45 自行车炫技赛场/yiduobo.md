---
title: "LCP 45. 自行车炫技赛场"
aliases: ["yiduobo的每日leetcode LCP45.自行车炫技赛场"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bfs", "题单/网格图", "题单/网格图/五-综合应用"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/576471734"
zhihu_id: "576471734"
zhihu_title: "yiduobo的每日leetcode LCP45.自行车炫技赛场"
question_id: "LCP 45"
question: "自行车炫技赛场"
problem_url: "https://leetcode.cn/problems/kplEvH/"
difficulty: "Medium"
created: "2022-10-23T19:42:52+08:00"
updated: "2022-10-23T19:42:52+08:00"
upvotes: 0
comments: 0
---

# LCP 45. 自行车炫技赛场

> **[yiduobo的每日leetcode LCP45.自行车炫技赛场](https://zhuanlan.zhihu.com/p/576471734) · 知乎 · 2022-10-23 · 赞同 0**
> 力扣：[LCP 45. 自行车炫技赛场](https://leetcode.cn/problems/kplEvH/) · Medium · 灵茶山艾府：[状态设计+BFS ](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP45.自行车炫技赛场

[力扣](https://leetcode.cn/problems/kplEvH/)

一个自然的想法是使用f[x][y][v]表示是否可能存在位于位置(x, y)，且速度为v的情况，然后从(position[0], position[1])，且速度v \= 1开始进行bfs，找出所有可能的状态。但是有一个问题就是如果v的上限很大的话，会导致时空复杂度过高，需要先估一下v的规模。

题设给出的是在凹凸不平的场地里骑车，那么应该是不会出现永动机的情况的。

直观来说，只有从高处往低处走的时候速度才会增加，但是随着自行车的行进，因为有数组o的存在，速度应该是会逐渐衰减的。

严谨的说，从h1走到h2的速度为1 + h1 - h2 - o2，然后从h2走到h3，速度为1 + h1 - h2 - o2 + h2 - h3 - o3 \= 1 + h1 - h3 - o2 - o3。更一般的，走到hk的速度就应该是1 + h1 - hk - o2 - o3 - ... - ok。

由于式子中的h和o都是非负数，那么实际上最大的v就是h1取上限，后面全部取0的情况，也就是101。这个数据规模是完全可行的。

接下来就是按最开始的说法，从(position[0], position[1])，v \= 1开始做bfs。bfs完成后，遍历地图上的每个位置(x, y)，若(x, y)且v \= 1出现在了bfs队列中，那么就将(x, y)加入到答案中。

最后附上python代码：

```python
class Solution(object):
    def bicycleYard(self, position, terrain, obstacle):
        """
        :type position: List[int]
        :type terrain: List[List[int]]
        :type obstacle: List[List[int]]
        :rtype: List[List[int]]
        """

        m = len(terrain)
        n = len(terrain[0])
        max_v = 101

        vis = [[[False] * (max_v + 1) for _ in range(n)] for _ in range(m)]
        vis[position[0]][position[1]][1] = True
        q = [[position[0], position[1], 1]]
        head, tail = 0, 1
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while head < tail:
            nowx, nowy, nowv = q[head]
            head += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                
                if x >= 0 and x < m and y >= 0 and y < n:
                    v = nowv + terrain[nowx][nowy] - terrain[x][y] - obstacle[x][y]
                    if v > 0 and not vis[x][y][v]:
                        q.append([x, y, v])
                        tail += 1
                        vis[x][y][v] = True
        
        res = []
        for x in range(m):
            for y in range(n):
                if (x != position[0] or y != position[1]) and vis[x][y][1]:
                    res.append([x, y])
        
        return res
```
