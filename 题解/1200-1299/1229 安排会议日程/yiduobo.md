---
title: "1229. 安排会议日程"
aliases: ["yiduobo的每日leetcode 1229.安排会议日程"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/613719543"
zhihu_id: "613719543"
zhihu_title: "yiduobo的每日leetcode 1229.安排会议日程"
question_id: "1229"
question: "安排会议日程"
problem_url: "https://leetcode.cn/problems/meeting-scheduler/"
created: "2023-03-13T22:05:15+08:00"
updated: "2023-03-13T22:05:15+08:00"
upvotes: 0
comments: 0
---

# 1229. 安排会议日程

> **[yiduobo的每日leetcode 1229.安排会议日程](https://zhuanlan.zhihu.com/p/613719543) · 知乎 · 2023-03-13 · 赞同 0**
> 力扣：[1229. 安排会议日程](https://leetcode.cn/problems/meeting-scheduler/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1229.安排会议日程

[力扣](https://leetcode.cn/problems/meeting-scheduler/)

由于题目中只有两个人，且单个人的空闲时间是不可能出现重叠的，那么问题就可以理解成给出若干区间，问这些区间之间，最早出现且重叠长度超过duration的区间是什么。

对于区间类问题，排序后直接做常规的合并是可行的，不过在这里也可以利用类似差分数组的处理方法。

使用一个变量cnt记录当前空闲的人数，接下来遍历所有出现的时间点。若当前遍历到的是一个区间的起点，那么就将cnt加上1，否则将cnt减去1。

当某一时刻cnt等于2时，说明从当前时间点开始两个人都有空闲，将最近一次cnt等于2的时间点记为start。当cnt从2回落到1时，说明其中一个人不再空闲，那么从start开始，到当前时间点为止的这一段时间两个人都是空闲的，只需检测这一段时间的长度是否大于等于duration。若满足，那么[start, start + duration]就是最终答案。

在具体实现上，需要先计算区间起点，再计算区间终点。我在这里采用的是经典的起点乘以2、终点乘以2加1的处理方式。

最后附上python代码：

```python
class Solution(object):
    def minAvailableDuration(self, slots1, slots2, duration):
        """
        :type slots1: List[List[int]]
        :type slots2: List[List[int]]
        :type duration: int
        :rtype: List[int]
        """

        timepoints = []
        for x, y in slots1:
            timepoints.append(x + x)
            timepoints.append(y + y + 1)
        
        for x, y in slots2:
            timepoints.append(x + x)
            timepoints.append(y + y + 1)

        timepoints.sort()

        cnt = 0
        start = 0
        for t in timepoints:
            if t % 2 == 0:
                cnt += 1
                if cnt == 2:
                    start = t / 2
            else:
                cnt -= 1
                if cnt == 1:
                    if t / 2 - start >= duration:
                        return [start, start + duration]
        
        return []
```
