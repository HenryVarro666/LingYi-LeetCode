---
title: "657. 机器人能否返回原点"
aliases: ["yiduobo的每日leetcode 657.机器人能否返回原点"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/281968289"
zhihu_id: "281968289"
zhihu_title: "yiduobo的每日leetcode 657.机器人能否返回原点"
question_id: "657"
question: "机器人能否返回原点"
problem_url: "https://leetcode.cn/problems/robot-return-to-origin/"
difficulty: "Easy"
created: "2020-11-09T23:05:01+08:00"
updated: "2020-11-09T23:05:01+08:00"
upvotes: 0
comments: 0
---

# 657. 机器人能否返回原点

> **[yiduobo的每日leetcode 657.机器人能否返回原点](https://zhuanlan.zhihu.com/p/281968289) · 知乎 · 2020-11-09 · 赞同 0**
> 力扣：[657. 机器人能否返回原点](https://leetcode.cn/problems/robot-return-to-origin/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

657.机器人能否返回原点

[力扣](https://leetcode-cn.com/problems/robot-return-to-origin/)

在机器人的行动序列中，1个D可以认为是-1个U，而1个R则可以认为是-1个L，于是我们最后只需要遍历整个行动序列，统计其中U和L的数目，若二者都为0，说明走回了原点。

最后附上python代码：

```python
class Solution(object):
    def judgeCircle(self, moves):
        """
        :type moves: str
        :rtype: bool
        """

        U = L = 0
        for move in moves:
            if move == 'U':
                U += 1
            elif move == 'D':
                U -= 1
            elif move == 'L':
                L += 1
            else:
                L -= 1
        
        if U == 0 and L == 0:
            return True

        return False
```
