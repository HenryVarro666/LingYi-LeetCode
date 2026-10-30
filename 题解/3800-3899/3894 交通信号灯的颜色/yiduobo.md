---
title: "3894. 交通信号灯的颜色"
aliases: ["yiduobo的每日leetcode 3894.交通信号灯的颜色"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2027169305167438569"
zhihu_id: "2027169305167438569"
zhihu_title: "yiduobo的每日leetcode 3894.交通信号灯的颜色"
question_id: "3894"
question: "交通信号灯的颜色"
problem_url: "https://leetcode.cn/problems/traffic-signal-color/"
difficulty: "Easy"
created: "2026-04-13T23:44:32+08:00"
updated: "2026-04-13T23:44:33+08:00"
upvotes: 0
comments: 0
---

# 3894. 交通信号灯的颜色

> **[yiduobo的每日leetcode 3894.交通信号灯的颜色](https://zhuanlan.zhihu.com/p/2027169305167438569) · 知乎 · 2026-04-13 · 赞同 0**
> 力扣：[3894. 交通信号灯的颜色](https://leetcode.cn/problems/traffic-signal-color/) · Easy · 灵茶山艾府：[分类讨论（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3894.交通信号灯的颜色

<https://leetcode.cn/problems/traffic-signal-color/description/>

题目给出一个整数timer，表示交通信号灯上的剩余时间，单位为秒。

信号灯遵循以下规则：

- 若timer为0，那么信号灯为Green
- 若timer为30，那么信号灯为Orange
- 若30 \< timer \<\= 90，那么信号灯为Red

返回当前信号灯的状态，若均不满足以上的条件，则返回Invalid。

比较基础的题目，直接按照题目要求if判断一下就行了。

最后附上python代码：

```python
class Solution(object):
    def trafficSignal(self, timer):
        """
        :type timer: int
        :rtype: str
        """
        
        if timer == 0:
            return "Green"
        if timer == 30:
            return "Orange"
        if 30 < timer <= 90:
            return "Red"
        return "Invalid"
```
