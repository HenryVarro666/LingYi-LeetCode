---
title: "489. 扫地机器人"
aliases: ["yiduobo的每日leetcode 489.扫地机器人"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/600315651"
zhihu_id: "600315651"
zhihu_title: "yiduobo的每日leetcode 489.扫地机器人"
question_id: "489"
question: "扫地机器人"
problem_url: "https://leetcode.cn/problems/robot-room-cleaner/"
created: "2023-01-20T23:55:59+08:00"
updated: "2023-01-20T23:55:59+08:00"
upvotes: 0
comments: 0
---

# 489. 扫地机器人

> **[yiduobo的每日leetcode 489.扫地机器人](https://zhuanlan.zhihu.com/p/600315651) · 知乎 · 2023-01-20 · 赞同 0**
> 力扣：[489. 扫地机器人](https://leetcode.cn/problems/robot-room-cleaner/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

489.扫地机器人

[力扣](https://leetcode.cn/problems/robot-room-cleaner/)

本题没有给出地图，但是要求对地图进行一次遍历，那么最直观的做法就是dfs。不妨设机器人一开始位于坐标(0, 0），接下来根据机器人的行动计算当前的相对坐标，并使用一个集合vis储存已经访问过的坐标用来去重。

对于4个方向，则可以按照顺时针方向设置坐标增量数组dx和dy，分别为

dx \= [-1, 0, 1, 0]，dy \= [0, 1, 0, -1]

接下来，从位置(0, 0)开始进行dfs，初始方向向上，也就是对应到dx和dy中的下标0。

对于当前处理到的dfs(nowx, nowy, nowd)，从0到3枚举当前机器人的右转次数，并通过当前方向nowd和转向次数计算出最终方向d。在计算过程中，当右转次数大于0时都需要同步对机器人执行右转操作。

接下来，通过nowx + dx[d]和nowy + dy[d]计算出目的地的坐标(x, y)。若其还没有被访问过，也就是没有出现在vis中，那么就尝试让机器人向前移动。若移动成功，那么就执行清洁，并将(x, y)加入到vis中，然后递归计算dfs(x, y, d)。从dfs(x, y, d)回溯后，需要注意需要将机器人退回到(nowx, nowy)这个位置，因此需要将回溯后的机器人转向，也就是执行两次右转操作，然后前进一步，最后再执行两次右转操作，将机器人的方向复原。

枚举完右转次数后，此时机器人应该右转了三次，因此在回溯之前还需要将机器人的方向回正，也就是再执行一次右转操作。

本题与常规搜索回溯题主要有两个不同点。第一个是没有地图，因此需要通过记录访问过的点，配合机器人的move操作来探测地图。第二个是机器人无法方便的回溯，因此在模拟行动时需要记得对机器人进行操作来达到回溯的效果。

最后附上python代码：

```python
# """
# This is the robot's control interface.
# You should not implement it, or speculate about its implementation
# """
#class Robot(object):
#    def move(self):
#        """
#        Returns true if the cell in front is open and robot moves into the cell.
#        Returns false if the cell in front is blocked and robot stays in the current cell.
#        :rtype bool
#        """
#
#    def turnLeft(self):
#        """
#        Robot will stay in the same cell after calling turnLeft/turnRight.
#        Each turn will be 90 degrees.
#        :rtype void
#        """
#
#    def turnRight(self):
#        """
#        Robot will stay in the same cell after calling turnLeft/turnRight.
#        Each turn will be 90 degrees.
#        :rtype void
#        """
#
#    def clean(self):
#        """
#        Clean the current cell.
#        :rtype void
#        """

class Solution(object):
    def cleanRoom(self, robot):
        """
        :type robot: Robot
        :rtype: None
        """

        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]
        vis = set([(0, 0)])
        robot.clean()

        def dfs(nowx, nowy, nowd):
            for index in range(4):
                d = (nowd + index) % 4
                x = nowx + dx[d]
                y = nowy + dy[d]
                if index > 0:
                    robot.turnRight()
                if (x, y) not in vis:
                    vis.add((x, y))
                    if robot.move():
                        robot.clean()
                        dfs(x, y, d)
                        robot.turnRight()
                        robot.turnRight()
                        robot.move()                            
                        robot.turnRight()
                        robot.turnRight()
            robot.turnRight()

        dfs(0, 0, 0)
```
