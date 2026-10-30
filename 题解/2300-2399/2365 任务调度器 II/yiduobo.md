---
title: "2365. 任务调度器II"
aliases: ["yiduobo的每日leetcode 2365.任务调度器II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/563092765"
zhihu_id: "563092765"
zhihu_title: "yiduobo的每日leetcode 2365.任务调度器II"
question_id: "2365"
question: "任务调度器 II"
problem_url: "https://leetcode.cn/problems/task-scheduler-ii/"
difficulty: "Medium"
created: "2022-09-10T02:01:18+08:00"
updated: "2022-09-10T02:01:18+08:00"
upvotes: 0
comments: 0
---

# 2365. 任务调度器II

> **[yiduobo的每日leetcode 2365.任务调度器II](https://zhuanlan.zhihu.com/p/563092765) · 知乎 · 2022-09-10 · 赞同 0**
> 力扣：[2365. 任务调度器 II](https://leetcode.cn/problems/task-scheduler-ii/) · Medium · 灵茶山艾府：[模拟 + 简洁写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2365.任务调度器II

[力扣](https://leetcode.cn/problems/task-scheduler-ii/)

题目要求所有任务按顺序执行，因此并没有什么掉不掉度一说，就是按顺序执行下来就行了。由于两个相同的任务之间有一段不可用的时间，那么可以使用哈希表disable记录每种任务最晚的不可用时间。

接下来一趟遍历，使用now表示当前的时间戳。对于当前任务t：

若now大于disable[t]，那么说明可以直接执行当前任务。执行完t之后，任务t的在接下来space单位的时间内都是不可用的，因此需要更新disable[t]为now + space，同时更新now为now + 1

若now小于等于disable[t]，那么就必须一直等到disable[t] + 1为止才能开始执行任务t，因此需要更新now为disable[t] + 2。另外，任务t同样是在接下来space单位的时间内都不可用，因此需要更新disable[t]为disable[t] + 1 + space。

遍历完成后，在now的上一时刻所有任务都执行完毕了，因此最终答案就是now - 1。

最后附上python代码：

```python
class Solution(object):
    def taskSchedulerII(self, tasks, space):
        """
        :type tasks: List[int]
        :type space: int
        :rtype: int
        """

        disable = {}
        now = 1
        for t in tasks:
            if disable.get(t, 0) < now:
                disable[t] = now + space
                now += 1
            else:
                now = disable[t] + 2
                disable[t] += space + 1
        
        return now - 1
```
