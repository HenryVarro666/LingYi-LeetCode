---
title: "1109. 航班预订统计"
aliases: ["yiduobo的每日leetcode 1109.航班预订统计"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/374940397"
zhihu_id: "374940397"
zhihu_title: "yiduobo的每日leetcode 1109.航班预订统计"
question_id: "1109"
question: "航班预订统计"
problem_url: "https://leetcode.cn/problems/corporate-flight-bookings/"
created: "2021-05-24T22:25:17+08:00"
updated: "2021-05-24T22:25:17+08:00"
upvotes: 0
comments: 0
---

# 1109. 航班预订统计

> **[yiduobo的每日leetcode 1109.航班预订统计](https://zhuanlan.zhihu.com/p/374940397) · 知乎 · 2021-05-24 · 赞同 0**
> 力扣：[1109. 航班预订统计](https://leetcode.cn/problems/corporate-flight-bookings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1109.航班预订统计

[力扣](https://leetcode-cn.com/problems/corporate-flight-bookings/)

经典的静态区间和问题，一般的做法是使用差分数组。题目描述的飞机订座稍微抽象一点，不妨想象一下这个场景：有一辆公交车，同样有若干区间[l, r, s]，表示有s个人在第l分钟上车，在第r + 1分钟下车，问每一时刻车上的人数。那么最直观的想法就是使用一个变量维护当前车上的人数now，每遇到一个l则将now加上对应的s，遇到一个r + 1则将now减去对应的s。

当然，我们在计算的过程中不可能每次都去扫描数组寻找有没有哪个区间的开始是l或者结束是r，因此我们需要一个数组f来表示每一时刻上下车的人数。对于[l, r, s]，我们需要将f[l]加上s，将f[r + 1]减去s，那么在处理now时，扫描整个时间轴，每次将now加上对应的f即可。

最后附上python代码：

```python
class Solution(object):
    def corpFlightBookings(self, bookings, n):
        """
        :type bookings: List[List[int]]
        :type n: int
        :rtype: List[int]
        """

        res = [0] * (n + 1)
        for start, end, num in bookings:
            res[start] += num
            if end < n:
                res[end + 1] -= num
        
        for index in range(2, n + 1):
            res[index] += res[index - 1]

        return res[1:]
```
