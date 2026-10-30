---
title: "874. 模拟行走机器人"
aliases: ["yiduobo的每日leetcode 874.模拟行走机器人"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/350563193"
zhihu_id: "350563193"
zhihu_title: "yiduobo的每日leetcode 874.模拟行走机器人"
question_id: "874"
question: "模拟行走机器人"
problem_url: "https://leetcode.cn/problems/walking-robot-simulation/"
difficulty: "Medium"
created: "2021-02-15T02:48:42+08:00"
updated: "2021-02-15T02:48:42+08:00"
upvotes: 0
comments: 0
---

# 874. 模拟行走机器人

> **[yiduobo的每日leetcode 874.模拟行走机器人](https://zhuanlan.zhihu.com/p/350563193) · 知乎 · 2021-02-15 · 赞同 0**
> 力扣：[874. 模拟行走机器人](https://leetcode.cn/problems/walking-robot-simulation/) · Medium · 灵茶山艾府：[利用向量数组简化代码（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

874.模拟行走机器人

[力扣](https://leetcode-cn.com/problems/walking-robot-simulation/)

由于这里最多只有4000个指令，那么如果一步一步进行模拟，至多也就36000次操作，因此直接一步一步模拟行走是可行的。

我在这里选择的做法是先对障碍物按行和列进行聚合，然后分别排序。在每次行走之前，先通过二分找到下一个障碍物的位置，然后判断这次指令是否会碰到该障碍物。

最后附上python代码：

```python
class Solution(object):
    def robotSim(self, commands, obstacles):
        """
        :type commands: List[int]
        :type obstacles: List[List[int]]
        :rtype: int
        """

        x_dict = {}
        y_dict = {}
        for x, y in obstacles:
            if x not in x_dict:
                x_dict[x] = []
            if y not in y_dict:
                y_dict[y] = []
            x_dict[x].append(y)
            y_dict[y].append(x)
        
        sorted_x_dict = {}
        sorted_y_dict = {}
        for x in x_dict:
            sorted_x_dict[x] = sorted(x_dict[x])
        for y in y_dict:
            sorted_y_dict[y] = sorted(y_dict[y])
        
        nowx, nowy = 0, 0
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        dpos = 0
        res = 0
        for cmd in commands:
            if cmd == -1:
                dpos = (dpos + 1) % 4
            elif cmd == -2:
                dpos = (dpos + 3) % 4
            else:
                if dpos == 0:
                    delta = self.bisect(sorted_x_dict.get(nowx, []), nowy, True)
                elif dpos == 1:
                    delta = self.bisect(sorted_y_dict.get(nowy, []), nowx, True)
                elif dpos == 2:
                    delta = self.bisect(sorted_x_dict.get(nowx, []), nowy, False)
                else:
                    delta = self.bisect(sorted_y_dict.get(nowy, []), nowx, False)
                if delta is None or delta > cmd:
                    movelen = cmd
                else:
                    movelen = delta - 1
                nowx += dx[dpos] * movelen
                nowy += dy[dpos] * movelen
                res = max(res, nowx ** 2 + nowy ** 2)
        
        return res

    def bisect(self, pos_list, x, bigger_flag):
        if not pos_list:
            return None
        if x >= pos_list[-1]:
            if bigger_flag:
                return None
            elif x == pos_list[-1]:
                if len(pos_list) == 1:
                    return None
                else:
                    return x - pos_list[-2]
            else:
                return x - pos_list[-1]

        l = 0
        r = len(pos_list) - 1
        while l < r:
            mid = (l + r) >> 1
            if pos_list[mid] <= x:
                l = mid + 1
            else:
                r = mid

        if bigger_flag:
            return pos_list[l] - x
        
        if l == 0:
            return None
        
        if x == pos_list[l - 1]:
            if l == 1:
                return None
            else:
                return x - pos_list[l - 2]
        else:
            return x - pos_list[l - 1]
```
