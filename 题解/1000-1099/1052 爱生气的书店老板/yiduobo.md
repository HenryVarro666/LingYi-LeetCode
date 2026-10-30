---
title: "1052. 爱生气的书店老板"
aliases: ["yiduobo的每日leetcode 1052.爱生气的书店老板"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/371827323"
zhihu_id: "371827323"
zhihu_title: "yiduobo的每日leetcode 1052.爱生气的书店老板"
question_id: "1052"
question: "爱生气的书店老板"
problem_url: "https://leetcode.cn/problems/grumpy-bookstore-owner/"
difficulty: "Medium"
rating: 1418
created: "2021-05-12T22:06:25+08:00"
updated: "2021-05-12T22:06:25+08:00"
upvotes: 0
comments: 0
---

# 1052. 爱生气的书店老板

> **[yiduobo的每日leetcode 1052.爱生气的书店老板](https://zhuanlan.zhihu.com/p/371827323) · 知乎 · 2021-05-12 · 赞同 0**
> 力扣：[1052. 爱生气的书店老板](https://leetcode.cn/problems/grumpy-bookstore-owner/) · Medium · 灵茶山艾府：[定长滑动窗口，附题单！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1052.爱生气的书店老板

[力扣](https://leetcode-cn.com/problems/grumpy-bookstore-owner/)

首先，无论老板是否发动技能，所有grumpy等于0时的顾客都必然是满意的，设这些顾客的总数为origin，那么我们的目标就是找到一个区间，使得这个区间内grumpy等于1时对应的顾客总数最多。

由于老板这个技能是固定连续X分钟，也就是说这个区间的长度固定为X，那么我们可以使用滑动窗口来解决这个问题。

初始化窗口为0到X - 1，同时设now为当前窗口内grumpy等于1时对应的顾客总数。接下来每一轮将窗口的右边界向右移动，若此时新加入的grumpy为1，那么就让now加上对应的顾客数。同时将窗口的左边界收缩，若此时排除窗口的grumpy为1，那么就让now减去对应的顾客数。

滑动过程中最大的now，再加上origin就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxSatisfied(self, customers, grumpy, X):
        """
        :type customers: List[int]
        :type grumpy: List[int]
        :type X: int
        :rtype: int
        """

        origin = 0
        now = 0
        change = 0
        for index in range(X):
            if grumpy[index] == 0:
                origin += customers[index]
            else:
                now += customers[index]
        
        change = now
        for index in range(X, len(customers)):
            if grumpy[index] == 0:
                origin += customers[index]
            else:
                now += customers[index]
            
            if grumpy[index - X] == 1:
                now -= customers[index - X]
            
            change = max(change, now)

        return change + origin
```
