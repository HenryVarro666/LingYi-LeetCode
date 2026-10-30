---
title: "2061. 扫地机器人清扫过的空间个数"
aliases: ["yiduobo的每日leetcode 2061.扫地机器人清扫过的空间个数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/625791112"
zhihu_id: "625791112"
zhihu_title: "yiduobo的每日leetcode 2061.扫地机器人清扫过的空间个数"
question_id: "2061"
question: "扫地机器人清扫过的空间个数"
problem_url: "https://leetcode.cn/problems/number-of-spaces-cleaning-robot-cleaned/"
created: "2023-04-29T03:30:36+08:00"
updated: "2023-04-29T03:30:36+08:00"
upvotes: 0
comments: 0
---

# 2061. 扫地机器人清扫过的空间个数

> **[yiduobo的每日leetcode 2061.扫地机器人清扫过的空间个数](https://zhuanlan.zhihu.com/p/625791112) · 知乎 · 2023-04-29 · 赞同 0**
> 力扣：[2061. 扫地机器人清扫过的空间个数](https://leetcode.cn/problems/number-of-spaces-cleaning-robot-cleaned/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

2061.扫地机器人清扫过的空间个数

[力扣](https://leetcode.cn/problems/number-of-spaces-cleaning-robot-cleaned/)

由于本题的数据规模不大，因此可以直接模拟机器人在房间内的行动。又由于机器人自身是不会停下的，那么就需要设置一个停下的条件。除了常规的二维空间位置信息外，机器人自身还具备一个方向信息，因此需要将这三个信息综合起来进行去重，接下来就只需要模拟机器人的行动，直到再次走到一个之前出已经现过的状态。

具体实现上，我采用的是二维数组vis来进行去重，其中vis[x][y]为四位二进制，分别记录了机器人是否以向左、向下、向右以及向上这四个方向访问过位置(x, y)。

最后附上python代码：

```python
class Solution(object):
    def numberOfCleanRooms(self, room):
        """
        :type room: List[List[int]]
        :rtype: int
        """

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        
        m = len(room)
        n = len(room[0])
        vis = [[0] * n for _ in range(m)]

        nowx, nowy, nowd = 0, 0, 0
        vis[0][0] = 1
        res = 1
        while True:
            x = nowx + dx[nowd]
            y = nowy + dy[nowd]
            if x < 0 or y < 0 or x >= m or y >= n or room[x][y] == 1:
                nowd = (nowd + 1) % 4
            else:
                nowx, nowy = x, y
            
            if vis[nowx][nowy] & (1 << nowd) == 0:
                if vis[nowx][nowy] == 0:
                    res += 1
                vis[nowx][nowy] |= (1 << nowd)
            else:
                break

        return res
```
