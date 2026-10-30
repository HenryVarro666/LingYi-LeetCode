---
title: "4012. 统计每个班次结束后的未完成任务数"
aliases: ["yiduobo的每日leetcode 4012.统计每个班次结束后的未完成任务数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "leetcode/prefix-sum", "题单/二分算法", "题单/二分算法/一-二分查找"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2070330621315092636"
zhihu_id: "2070330621315092636"
zhihu_title: "yiduobo的每日leetcode 4012.统计每个班次结束后的未完成任务数"
question_id: "4012"
question: "统计每个班次结束后的未完成任务数"
problem_url: "https://leetcode.cn/problems/count-of-unfinished-tasks-after-each-shift/"
difficulty: "Medium"
rating: 1736
created: "2026-08-11T02:38:09+08:00"
updated: "2026-08-11T02:38:18+08:00"
upvotes: 1
comments: 0
---

# 4012. 统计每个班次结束后的未完成任务数

> **[yiduobo的每日leetcode 4012.统计每个班次结束后的未完成任务数](https://zhuanlan.zhihu.com/p/2070330621315092636) · 知乎 · 2026-08-11 · 赞同 1**
> 力扣：[4012. 统计每个班次结束后的未完成任务数](https://leetcode.cn/problems/count-of-unfinished-tasks-after-each-shift/) · Medium · 灵茶山艾府：[前缀和 + 二分查找（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4012.统计每个班次结束后未完成任务数

<https://leetcode.cn/problems/count-of-unfinished-tasks-after-each-shift/description/>

题目给出两个正整数数组tasks和shifts，其中tasks[index]表示完成第index个任务所需的时间，shifts[index]则表示第index个班次可用的时间。

任务必须按照从左到右的顺序处理，并遵循下面的规则：

- 若某个任务在当前班次内没有完成，那么下一个班次将会继承之前班次的进度继续处理该任务。
- 若某个班次内完成了所有的任务，那么该班次结束，剩余的事件被丢弃，下一个班次重新从第0个任务开始。

若一个任务没有被全部完成，就认为其是未完成的，这包括正在执行中的任务。

要求返回一个数组ans，其中ans[index]表示第index个班次结束后剩余的未完成任务数量。

由于题目中任务所需的时间都为正数，那么就意味着完成的任务越多，需要的时间就越长，因此可以针对每个班次，通过二分来计算可以完成哪些班次。

由于题目中存在进度继承的规则，因此在这里需要使用两个变量p和r，分别表示下一个班次将从已经执行了r分钟的任务p开始继续向后执行，那么对于当前班次的总时间shifts[index]：

1、若shifts[index] >\= tasks[p] + tasks[p + 1] + ... + tasks[-1] - r，那么就说明这个班次可以完成所有的任务。此时对应的的答案就应该为0，同时需要将p和r重置。

注意到这是一个区间和，那么在这里就可以先计算tasks的前缀和s。方便起见，令s[0] \= 0，然后s[index] \= s[index - 1] + tasks[index - 1]，以上的式子就可以改写为判断shifts[index] + r是否大于等于s[-1] - s[p - 1]。

需要注意，基于s的定义，p的初始值应该从1开始，同时完成所有任务后，p也是重置为1。

2、若无法完成所有任务，则可以通过二分法找到首个无法完成的任务。需要注意，这里是在前缀和数组s中二分呢，因此二分的下界left是p，上界right则为len(s) - 1。

对于二分到的mid，同样是通过shifts[index]与tasks[p] + tasks[p + 1] + ... + tasks[mid] - r来判断能否完成p到mid这些任务，通过前缀和则可以改写为shifts[index] + r是否大于等于s[mid] - s[p - 1]。若满足，则调整二分的下界left为mid + 1，否则调整二分的上界right为mid。

二分结束后，由于s存在1的下标偏移，因此当前的left - 1才是无法完成的任务下标，此时对应的答案就是len(s) - left。接下来，还需要将p置为left，同时计算新的r，即shifts[index] + r - (tasks[p - 1] + tasks[p + 1] + ... + tasks[left - 2])，也就是shifts[index] + r - (s[left - 1] - s[p - 1])。

最后附上python代码：

```python
class Solution(object):
    def countTasks(self, tasks, shifts):
        """
        :type tasks: List[int]
        :type shifts: List[int]
        :rtype: List[int]
        """
        
        s = [0]
        for t in tasks:
            s.append(s[-1] + t)
        
        p, r = 1, 0
        res = []
        for v in shifts:
            v += r
            if v >= s[-1] - s[p - 1]:
                res.append(0)
                p, r = 1, 0
            else:
                left = p
                right = len(s) - 1
                while left < right:
                    mid = (left + right) // 2
                    if s[mid] - s[p - 1] <= v:
                        left = mid + 1
                    else:
                        right = mid

                res.append(len(s) - left)
                r = v - (s[left - 1] - s[p - 1])
                p = left

        return res
```
