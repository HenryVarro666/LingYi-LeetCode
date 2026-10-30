---
title: "2069. 模拟行走机器人II"
aliases: ["yiduobo的每日leetcode 2069.模拟行走机器人II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/515346588"
zhihu_id: "515346588"
zhihu_title: "yiduobo的每日leetcode 2069.模拟行走机器人II"
question_id: "2069"
question: "模拟行走机器人 II"
problem_url: "https://leetcode.cn/problems/walking-robot-simulation-ii/"
difficulty: "Medium"
created: "2022-05-16T20:14:05+08:00"
updated: "2022-05-16T20:14:05+08:00"
upvotes: 0
comments: 0
---

# 2069. 模拟行走机器人II

> **[yiduobo的每日leetcode 2069.模拟行走机器人II](https://zhuanlan.zhihu.com/p/515346588) · 知乎 · 2022-05-16 · 赞同 0**
> 力扣：[2069. 模拟行走机器人 II](https://leetcode.cn/problems/walking-robot-simulation-ii/) · Medium · 灵茶山艾府：[分类讨论，O(1) 时间复杂度（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2069.模拟行走机器人II

[力扣](https://leetcode.cn/problems/walking-robot-simulation-ii/)

由于每一轮行走的步数高达100000，可能执行的次数也有1000次，那么直接模拟肯定是不行的。

注意到题目中的机器人只会贴着网格的边走，因此走完一圈的步数就固定下来了，为(width + height - 2) \* 2，那么对于每次行走操作，可以先让num对这个值取模，而对于剩下的步数则可以直接模拟，或者通过判断这个余数属于哪个区间来得到机器人最终停留的位置，然后通过这个位置判断机器人最后的朝向。

另外需要注意的是，当机器人来到拐角的时候，朝向是没有变化的，必须等到下一步行走时才会进行拐弯，所以在判断朝向时要特别注意拐角的情况。

最后附上python代码：

```python
class Robot(object):

    def __init__(self, width, height):
        """
        :type width: int
        :type height: int
        """
        self.w = width
        self.h = height
        self.x = self.y = self.d = 0

    def step(self, num):
        """
        :type num: int
        :rtype: None
        """

        if self.d == 0:
            num += self.x
        elif self.d == 1:
            num += self.w + self.y - 1
        elif self.d == 2:
            num += self.w + self.h - 2 + self.w - self.x - 1
        else:
            num += self.w + self.h + self.w - 3 + self.h - self.y - 1
        
        num %= (self.w + self.h + self.w + self.h - 4)
        if num < self.w:
            self.x = num
            self.y = 0
        elif self.w <= num < self.w + self.h - 1:
            self.x = self.w - 1
            self.y = num - self.w + 1
        elif self.w + self.h - 1 <= num < self.w + self.h - 2 + self.w:
            self.x = self.w - (num - self.w - self.h + 2) - 1
            self.y = self.h - 1
        else:
            self.x = 0
            self.y = self.h - (num - self.w - self.h - self.w + 3) - 1

        if self.y == 0 and 1 <= self.x < self.w:
            self.d = 0
        elif self.x == self.w - 1 and 1 <= self.y < self.h:
            self.d = 1
        elif self.y == self.h - 1 and 0 <= self.x < self.w - 1:
            self.d = 2
        else:
            self.d = 3

    def getPos(self):
        """
        :rtype: List[int]
        """
        return [self.x, self.y]

    def getDir(self):
        """
        :rtype: str
        """
        if self.d == 0:
            return "East"
        elif self.d == 1:
            return "North"
        elif self.d == 2:
            return "West"
        else:
            return "South"

# Your Robot object will be instantiated and called as such:
# obj = Robot(width, height)
# obj.step(num)
# param_2 = obj.getPos()
# param_3 = obj.getDir()
```
