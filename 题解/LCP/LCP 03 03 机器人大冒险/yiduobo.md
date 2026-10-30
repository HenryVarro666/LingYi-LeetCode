---
title: "LCP 03. 机器人大冒险"
aliases: ["yiduobo的每日leetcode LCP03.机器人大冒险"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/570268581"
zhihu_id: "570268581"
zhihu_title: "yiduobo的每日leetcode LCP03.机器人大冒险"
question_id: "LCP 03"
question: "机器人大冒险"
problem_url: "https://leetcode.cn/problems/programmable-robot/"
created: "2022-10-03T04:30:25+08:00"
updated: "2022-10-03T04:30:25+08:00"
upvotes: 0
comments: 0
---

# LCP 03. 机器人大冒险

> **[yiduobo的每日leetcode LCP03.机器人大冒险](https://zhuanlan.zhihu.com/p/570268581) · 知乎 · 2022-10-03 · 赞同 0**
> 力扣：[LCP 03. 机器人大冒险](https://leetcode.cn/problems/programmable-robot/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP03.机器人大冒险

[力扣](https://leetcode.cn/problems/programmable-robot/)

由于题目的数据规模比较大，直接模拟显然是不行的，需要想办法找找规律。注意到题目中的坐标范围很大，但是实际上只需要判断机器人能否走到终点，且不会走到任意陷阱点就行了，那么可以从这方面入手。

题目中的机器人总是复读同一段指令，不妨先模拟一个周期，就可以得到在一个周期中走到的所有格子，以及最终再横纵坐标上有多少增量。

记这个增量分别为dx和dy，那么对于题目中给出的终点以及若干个陷阱点，如果机器人最终能走到对应的点上，那么机器人一定是走了k周期的指令，然后在第k + 1个周期的指令中走到对应的点上，也就是

dx \* k + path_x[i] \= target_x

dy \* k + path_y[i] \= target_y

对于上面的这两个式子，target_x, target_y为目标点的横纵坐标，那么k可以通过除法计算得到，接下来就只需要枚举一个周期内机器人走到的所有格子path并检测就行了。

首先检测机器人能否走到终点，若不行，则直接返回false，否则检测机器人是否会走到某个陷阱点，若会，则同样是返回false。需要注意的是，若陷阱点的横坐标或者纵坐标大于终点，那么该陷阱点就无需检测了。

最后附上python代码：

```python
class Solution(object):
    def robot(self, command, obstacles, x, y):
        """
        :type command: str
        :type obstacles: List[List[int]]
        :type x: int
        :type y: int
        :rtype: bool
        """

        points_on_path = []
        nowx = nowy = 0
        for com in command:
            if com == 'U':
                nowy += 1
            else:
                nowx += 1
            points_on_path.append([nowx, nowy])

        def check(x, y):
            pre_round = min(x / points_on_path[-1][0], y / points_on_path[-1][1])
            nowx = points_on_path[-1][0] * pre_round
            nowy = points_on_path[-1][1] * pre_round
            if nowx == x and nowy == y:
                return True
            for dx, dy in points_on_path:
                if nowx + dx == x and nowy + dy == y:
                    return True
            return False

        if not check(x, y):
            return False

        for ox, oy in obstacles:
            if ox > x or oy > y:
                continue
            if check(ox, oy):
                return False
        
        return True
```
