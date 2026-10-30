---
title: "4024. 最近的可用无人机"
aliases: ["yiduobo的每日leetcode 4024.最近的可用无人机"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2073546065173913810"
zhihu_id: "2073546065173913810"
zhihu_title: "yiduobo的每日leetcode 4024.最近的可用无人机"
question_id: "4024"
question: "最近的可用无人机"
problem_url: "https://leetcode.cn/problems/nearest-available-drone/"
difficulty: "Easy"
created: "2026-08-19T23:12:07+08:00"
updated: "2026-08-19T23:12:07+08:00"
upvotes: 0
comments: 0
---

# 4024. 最近的可用无人机

> **[yiduobo的每日leetcode 4024.最近的可用无人机](https://zhuanlan.zhihu.com/p/2073546065173913810) · 知乎 · 2026-08-19 · 赞同 0**
> 力扣：[4024. 最近的可用无人机](https://leetcode.cn/problems/nearest-available-drone/) · Easy · 灵茶山艾府：[遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4024.最近的可用无人机

<https://leetcode.cn/problems/nearest-available-drone/description/>

题目给出一个二维整数数组drones，其中drones\[index\] \= \[x\[index\], y\[index\], range\[index\]\]，表示第index台无人机的横纵坐标以及飞行范围。

另外给出一个整数数组target \= [tx, ty]，表示目标的坐标。

对于一台无人机，若其坐标与目标坐标之间的曼哈顿距离，小于等于这台无人机对应的range，那么这台无人机就可以到达目标。

要求找出可以到达目标，且与目标曼哈顿距离最小的无人机的下标。若存在多个符合条件的无人机，返回其中最小的下标。若没有无人机可以到达目标，则返回-1。

按照题目要求对drones进行一趟遍历，对于第index台无人机，先通过abs(x[index] - tx) + abs(y[index] - ty)计算当前无人机到目标的距离d。若d小于等于这台无人机的range[index]，就使用d以及index更新答案。

最后附上python代码：

```python
class Solution(object):
    def nearestDrone(self, drones, target):
        """
        :type drones: List[List[int]]
        :type target: List[int]
        :rtype: int
        """
        
        res = -1
        min_dis = None
        for index, (x, y, r) in enumerate(drones):
            d = abs(x - target[0]) + abs(y - target[1])
            if d <= r and (res == -1 or min_dis > d):
                res = index
                min_dis = d
        
        return res
```
