---
title: "3683. 完成一个任务的最早时间"
aliases: ["yiduobo的每日leetcode 3683.完成一个任务的最早时间"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1953240083521069382"
zhihu_id: "1953240083521069382"
zhihu_title: "yiduobo的每日leetcode 3683.完成一个任务的最早时间"
question_id: "3683"
question: "完成一个任务的最早时间"
problem_url: "https://leetcode.cn/problems/earliest-time-to-finish-one-task/"
difficulty: "Easy"
created: "2025-09-25T22:59:43+08:00"
updated: "2025-09-25T22:59:45+08:00"
upvotes: 0
comments: 0
---

# 3683. 完成一个任务的最早时间

> **[yiduobo的每日leetcode 3683.完成一个任务的最早时间](https://zhuanlan.zhihu.com/p/1953240083521069382) · 知乎 · 2025-09-25 · 赞同 0**
> 力扣：[3683. 完成一个任务的最早时间](https://leetcode.cn/problems/earliest-time-to-finish-one-task/) · Easy · 灵茶山艾府：[遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3683.完成一个任务的最早时间

[3683. 完成一个任务的最早时间 - 力扣（LeetCode）](https://leetcode.cn/problems/earliest-time-to-finish-one-task/)

题目给出一个二维整数数字tasks，其中tasks\[index\] \= \[s\[index\], t\[index\]\]，表示index这个任务在时刻s\[index\]开始，需要执行t\[index\]个时间单位才能完成。要求返回完成至少一个任务的最早时间。

完成至少一个任务的最早时间，也就是说只需要完成一个任务就行了。于是一趟遍历，计算数组中每一组s与t之和，取其中的最小值即可。

最后附上python代码：

```python
class Solution(object):
    def earliestTime(self, tasks):
        """
        :type tasks: List[List[int]]
        :rtype: int
        """
        
        return min([s + t for s, t in tasks])
```
