---
title: "2814. 避免淹死并到达目的地的最短时间"
aliases: ["yiduobo的每日leetcode 2814.避免淹死并到达目的地的最短时间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/658388447"
zhihu_id: "658388447"
zhihu_title: "yiduobo的每日leetcode 2814.避免淹死并到达目的地的最短时间"
question_id: "2814"
question: "避免淹死并到达目的地的最短时间"
problem_url: "https://leetcode.cn/problems/minimum-time-takes-to-reach-destination-without-drowning/"
created: "2023-09-25T23:33:53+08:00"
updated: "2023-09-25T23:33:53+08:00"
upvotes: 0
comments: 0
---

# 2814. 避免淹死并到达目的地的最短时间

> **[yiduobo的每日leetcode 2814.避免淹死并到达目的地的最短时间](https://zhuanlan.zhihu.com/p/658388447) · 知乎 · 2023-09-25 · 赞同 0**
> 力扣：[2814. 避免淹死并到达目的地的最短时间](https://leetcode.cn/problems/minimum-time-takes-to-reach-destination-without-drowning/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2814.避免淹死并到达目的地的最短时间

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-time-takes-to-reach-destination-without-drowning/)

与之前一道火势蔓延的题目有点像，但是忘记题号了。处理方法是差不多的，即让水和人同时开始执行bfs，每一轮先让水进行扩展，然后人再进行扩展，直到人走到目的地或者无路可走为止。

最后附上python代码：

```python
class Solution(object):
    def minimumSeconds(self, land):
        """
        :type land: List[List[str]]
        :rtype: int
        """

        m = len(land)
        n = len(land[0])

        person_pos = []
        water_pos = []
        for i in range(m):
            for j in range(n):
                if land[i][j] == 'S':
                    person_pos.append([i, j])
                elif land[i][j] == '*':
                    water_pos.append([i, j])

        person_head, person_tail = 0, len(person_pos)
        water_head, water_tail = 0, len(water_pos)
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        res = 0
        while person_head < person_tail:
            res += 1

            for nowx, nowy in water_pos[water_head : water_tail]:
                for d in range(4):
                    x = nowx + dx[d]
                    y = nowy + dy[d]
                    if x >= 0 and x < m and y >= 0 and y < n and land[x][y] == '.':
                        land[x][y] = '*'
                        water_pos.append([x, y])
            
            water_head, water_tail = water_tail, len(water_pos)

            for nowx, nowy in person_pos[person_head : person_tail]:
                for d in range(4):
                    x = nowx + dx[d]
                    y = nowy + dy[d]
                    if x >= 0 and x < m and y >= 0 and y < n and (land[x][y] == '.' or land[x][y] == 'D'):
                        if land[x][y] == 'D':
                            return res
                        land[x][y] = '*'
                        person_pos.append([x, y])
            
            person_head, person_tail = person_tail, len(person_pos)
        
        return -1
```
