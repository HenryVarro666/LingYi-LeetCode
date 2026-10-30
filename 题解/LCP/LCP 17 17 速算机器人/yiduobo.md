---
title: "LCP 17. 速算机器人"
aliases: ["yiduobo的每日leetcode LCP17.速算机器人"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/571991404"
zhihu_id: "571991404"
zhihu_title: "yiduobo的每日leetcode LCP17.速算机器人"
question_id: "LCP 17"
question: "速算机器人"
problem_url: "https://leetcode.cn/problems/n/"
created: "2022-10-10T01:12:56+08:00"
updated: "2022-10-10T01:12:56+08:00"
upvotes: 0
comments: 0
---

# LCP 17. 速算机器人

> **[yiduobo的每日leetcode LCP17.速算机器人](https://zhuanlan.zhihu.com/p/571991404) · 知乎 · 2022-10-10 · 赞同 0**
> 力扣：[LCP 17. 速算机器人](https://leetcode.cn/problems/n/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP17.速算机器人

[力扣](https://leetcode.cn/problems/nGK0Fy/)

由于指令长度很短，那么一趟遍历，模拟计算过程就行了。

最后附上python代码：

```python
class Solution(object):
    def calculate(self, s):
        """
        :type s: str
        :rtype: int
        """

        x, y = 1, 0
        for char in s:
            if char == 'A':
                x = x + x + y
            else:
                y = y + y + x
        
        return x + y
```
