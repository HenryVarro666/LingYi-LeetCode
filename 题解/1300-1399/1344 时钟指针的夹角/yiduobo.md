---
title: "1344. 时钟指针的夹角"
aliases: ["yiduobo的每日leetcode 1344.时钟指针的夹角"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/396807526"
zhihu_id: "396807526"
zhihu_title: "yiduobo的每日leetcode 1344.时钟指针的夹角"
question_id: "1344"
question: "时钟指针的夹角"
problem_url: "https://leetcode.cn/problems/angle-between-hands-of-a-clock/"
difficulty: "Medium"
created: "2021-08-05T22:43:27+08:00"
updated: "2021-08-05T22:43:27+08:00"
upvotes: 0
comments: 0
---

# 1344. 时钟指针的夹角

> **[yiduobo的每日leetcode 1344.时钟指针的夹角](https://zhuanlan.zhihu.com/p/396807526) · 知乎 · 2021-08-05 · 赞同 0**
> 力扣：[1344. 时钟指针的夹角](https://leetcode.cn/problems/angle-between-hands-of-a-clock/) · Medium · 灵茶山艾府：[数学公式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1344.时钟指针的夹角

[力扣](https://leetcode-cn.com/problems/angle-between-hands-of-a-clock/)

为了求解时针和分针的夹角，那么我们可以将其转化为求解时针与十二点整的夹角hour_angle，然后求解分针与十二点整的夹角minute_angle，那么二者的夹角就是角度之差的绝对值。当然，若这个夹角大于180度，那么答案应该改成360度减去二者夹角。

接下来分别求解时针与十二点整的夹角，以及分针与十二点整的夹角。

由于时针会受到分针的影响，那么我们先求解分针与十二点整的夹角。

一个钟一共360度，且一共有60分钟，那么每分钟对应了6度，于是分针与十二点整的夹角就是minutes \* 6。

接下来求解时针与十二点整的夹角。除了本来的hour之外，由于分针走了minutes，那么时针还额外会走minutes / 60个小时，于是现在时针应该指向的是hour + minutes / 60。由于一个小时对应的是30度，那么时针与十二点整的夹角就是(hour + minutes / 60) \* 30。

求出二者之差的绝对值，并根据这个值与180度的大小选择使用哪个方向的夹角。

最后附上python代码：

```python
class Solution(object):
    def angleClock(self, hour, minutes):
        """
        :type hour: int
        :type minutes: int
        :rtype: float
        """

        if hour == 12:
            hour = 0
        
        hour_angle = (hour + minutes / 60.0) * 30
        minutes_angle = minutes * 6
        return min(abs(hour_angle - minutes_angle), 360 - abs(hour_angle - minutes_angle))
```
