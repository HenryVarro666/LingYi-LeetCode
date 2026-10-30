---
title: "539. 最小时间差"
aliases: ["yiduobo的每日leetcode 539.最小时间差"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261207830"
zhihu_id: "261207830"
zhihu_title: "yiduobo的每日leetcode 539.最小时间差"
question_id: "539"
question: "最小时间差"
problem_url: "https://leetcode.cn/problems/minimum-time-difference/"
created: "2020-10-07T22:24:19+08:00"
updated: "2020-10-07T22:24:19+08:00"
upvotes: 0
comments: 0
---

# 539. 最小时间差

> **[yiduobo的每日leetcode 539.最小时间差](https://zhuanlan.zhihu.com/p/261207830) · 知乎 · 2020-10-07 · 赞同 0**
> 力扣：[539. 最小时间差](https://leetcode.cn/problems/minimum-time-difference/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

539.最小时间差<https://leetcode-cn.com/problems/minimum-time-difference/>

注意到一天之内24小时，每小时60分钟，因此最多也就1440种不同的时间表示。

我们用hour \* 60 + minute来表示hour:minute这个时间，将timePoints中的所有时间转换为这个形式，用一个set储存起来。在转换的过程中，如果发现有相同的时间出现，那么直接返回0即可。

转换完成之后，我们从0开始往后扫描，优先找到其中最小的那个，然后继续往后扫描，每次与前一个时间进行比较，选出其中最小的差值。

需要注意的是，还需要对比最大时间与跨天的之后的最小时间，即样例中的第一天的23：59分只与第二天的00：00差一分钟。

最后附上python代码：

```python
class Solution(object):
    def findMinDifference(self, timePoints):
        """
        :type timePoints: List[str]
        :rtype: int
        """

        time_set = set()
        for time in timePoints:
            hour, minute = time.split(':')
            tmp = int(hour) * 60 + int(minute)
            if tmp in time_set:
                return 0
            time_set.add(tmp)

        first_time = 0
        while first_time not in time_set:
            first_time += 1
        
        now = first_time
        res = 1440
        for time in range(first_time + 1, 1441):
            if time in time_set:
                res = min(res, time - now)
                now = time

        return min(res, first_time + 1440 - now)
```
