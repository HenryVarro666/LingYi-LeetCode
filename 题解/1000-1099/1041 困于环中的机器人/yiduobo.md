---
title: "1041. 困于环中的机器人"
aliases: ["yiduobo的每日leetcode 1041.困于环中的机器人"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "题单/贪心算法", "题单/贪心算法/八-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/370781185"
zhihu_id: "370781185"
zhihu_title: "yiduobo的每日leetcode 1041.困于环中的机器人"
question_id: "1041"
question: "困于环中的机器人"
problem_url: "https://leetcode.cn/problems/robot-bounded-in-circle/"
difficulty: "Medium"
rating: 1521
created: "2021-05-08T22:26:58+08:00"
updated: "2021-05-08T22:26:58+08:00"
upvotes: 0
comments: 0
---

# 1041. 困于环中的机器人

> **[yiduobo的每日leetcode 1041.困于环中的机器人](https://zhuanlan.zhihu.com/p/370781185) · 知乎 · 2021-05-08 · 赞同 0**
> 力扣：[1041. 困于环中的机器人](https://leetcode.cn/problems/robot-bounded-in-circle/) · Medium · 灵茶山艾府：[结论题，用复数证明（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1041.困于环中的机器人

[力扣](https://leetcode-cn.com/problems/robot-bounded-in-circle/)

首先，如果一轮下来机器人直接走回了原点，那么答案显然为true。

接下来，机器人初始状态下的方向是朝向北方：

1、若一轮下来方向依然是北方，那么不可能走回原点

2、若一轮下来方向变成了朝向南方，那么再一轮之后必然会走回原点

3、若一轮下来方向变成了朝向东方或者西方，那么第二轮之后将朝向南方，接下来的第三轮将抵消掉第一轮同时将方向变为西方或者东方，而第四轮则会抵消掉第二轮，即四轮过后将走回原点

综合起来，就是在一轮之后若走回原点，或者方向不是朝向北方，那么答案就是true，否则就是false

最后附上python代码：

```python
class Solution(object):
    def isRobotBounded(self, instructions):
        """
        :type instructions: str
        :rtype: bool
        """

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        now_d = 0
        x = 0
        y = 0
        for order in instructions:
            if order == 'L':
                now_d -= 1
                if now_d < 0:
                    now_d = 3
            elif order == 'R':
                now_d += 1
                if now_d > 3:
                    now_d = 0
            else:
                x += dx[now_d]
                y += dy[now_d]
        
        if x == 0 and y == 0:
            return True

        return now_d != 0
```
