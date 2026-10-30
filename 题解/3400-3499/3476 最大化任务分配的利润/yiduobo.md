---
title: "3476. 最大化任务分配的利润"
aliases: ["yiduobo的每日leetcode 3476.最大化任务分配的利润"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1897074675567285307"
zhihu_id: "1897074675567285307"
zhihu_title: "yiduobo的每日leetcode 3476.最大化任务分配的利润"
question_id: "3476"
question: "最大化任务分配的利润"
problem_url: "https://leetcode.cn/problems/maximize-profit-from-task-assignment/"
created: "2025-04-19T23:59:46+08:00"
updated: "2025-04-20T00:00:18+08:00"
upvotes: 0
comments: 0
---

# 3476. 最大化任务分配的利润

> **[yiduobo的每日leetcode 3476.最大化任务分配的利润](https://zhuanlan.zhihu.com/p/1897074675567285307) · 知乎 · 2025-04-19 · 赞同 0**
> 力扣：[3476. 最大化任务分配的利润](https://leetcode.cn/problems/maximize-profit-from-task-assignment/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3476.最大化任务分配的利润

[3476. 最大化任务分配的利润 - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-profit-from-task-assignment/description/)

题目给出一个整数数组workers，其中workers[index]表示index这个工人的技能等级。另外给出一个二维数组tasks，其中tasks[index][0]表示完成index这个任务所需的技能等级，task[index][1]则表示完成index这个任务可以得到的收益。

每个工人最多只能完成一个任务，同时只有当他们的技能等级恰好等于任务的技能要求时才能获取此任务。除此之外，还有一名额外的工人加入，这名工人可以完成任何任务。

问如何分配任务，才能使得最终的收益最大。

由于只有当工人的技能等级恰好与任务的技能要求时才能进行任务分配，那么就可以先按照技能要求将所有任务分组，同时统计每种技能等级对应的工人数量。接下来对于每种技能等级中的任务，显然应该选择收益最大的任务来执行，而可以执行的任务数量就是技能等级恰好为这个技能要求的工人数量，相当于一个top k问题。我在这里采用的是直接暴力排序，然后取最大的k个求和。

除此之外，对于所有没有被执行的任务，则应该从中寻找收益最大的那个，让额外的工人来执行。

最后附上python代码：

```python
class Solution(object):
    def maxProfit(self, workers, tasks):
        """
        :type workers: List[int]
        :type tasks: List[List[int]]
        :rtype: int
        """
        
        task_dict = {}
        for skill, profit in tasks:
            if skill not in task_dict:
                task_dict[skill] = []
            task_dict[skill].append(profit)
        
        skill_cnt = Counter(workers)
        addtional = 0
        res = 0
        for skill in task_dict:
            task_dict[skill].sort(reverse=True)
            res += sum(task_dict[skill][:skill_cnt[skill]])
            if skill_cnt[skill] < len(task_dict[skill]):
                addtional = max(addtional, task_dict[skill][skill_cnt[skill]])
        
        return res + addtional
```
