---
title: "2651. 计算列车到站时间"
aliases: ["yiduobo的每日leetcode 2651.计算列车到站时间"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/647406445"
zhihu_id: "647406445"
zhihu_title: "yiduobo的每日leetcode 2651.计算列车到站时间"
question_id: "2651"
question: "计算列车到站时间"
problem_url: "https://leetcode.cn/problems/calculate-delayed-arrival-time/"
difficulty: "Easy"
created: "2023-08-02T03:22:01+08:00"
updated: "2023-08-02T03:22:01+08:00"
upvotes: 0
comments: 0
---

# 2651. 计算列车到站时间

> **[yiduobo的每日leetcode 2651.计算列车到站时间](https://zhuanlan.zhihu.com/p/647406445) · 知乎 · 2023-08-02 · 赞同 0**
> 力扣：[2651. 计算列车到站时间](https://leetcode.cn/problems/calculate-delayed-arrival-time/) · Easy · 灵茶山艾府：[按题意实现（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2651.计算列车到站时间

[力扣](https://leetcode.cn/problems/calculate-delayed-arrival-time/)

比较基础的题目，计划到站的时间加上延误的时间，再对24取模即可。

最后附上python代码：

```python
class Solution(object):
    def findDelayedArrivalTime(self, arrivalTime, delayedTime):
        """
        :type arrivalTime: int
        :type delayedTime: int
        :rtype: int
        """

        return (arrivalTime + delayedTime) % 24
```
