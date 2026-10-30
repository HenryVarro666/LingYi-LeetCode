---
title: "621. 任务调度器"
aliases: ["yiduobo的每日leetcode 621.任务调度器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/269640283"
zhihu_id: "269640283"
zhihu_title: "yiduobo的每日leetcode 621.任务调度器"
question_id: "621"
question: "任务调度器"
problem_url: "https://leetcode.cn/problems/task-scheduler/"
created: "2020-10-28T23:50:31+08:00"
updated: "2020-10-28T23:50:31+08:00"
upvotes: 0
comments: 0
---

# 621. 任务调度器

> **[yiduobo的每日leetcode 621.任务调度器](https://zhuanlan.zhihu.com/p/269640283) · 知乎 · 2020-10-28 · 赞同 0**
> 力扣：[621. 任务调度器](https://leetcode.cn/problems/task-scheduler/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

621.任务调度器<https://leetcode-cn.com/problems/task-scheduler/>

题目描述中每个任务执行的时间都是一致的，由于冷却时间的存在，我们显然应该优先处理堆积较多的任务。这个堆积数是在动态变化的，因此我们可以使用堆来维护这个任务堆积数。但是这样做有一个问题，就是无法顾及到冷却时间。例如有3个任务A和一个任务B，冷却时间为1，那么我们在做完一个任务A之后，此时堆积的任务A较多，但我们不能立刻执行任务A。

注意到每个任务的冷却时间也是一致的，因此我们可以将执行任务的粒度由一个一个变成一组一组，即对于冷却时间n，我们每轮选择执行n + 1个不同的任务，那么组与组之间相同的任务就不存在冷却时间的问题。而在组内任务的选择上，依然是优先选择堆积较多的任务。

于是现在的做法就是先将所有任务加入堆中，然后从堆中选择前n + 1个任务执行，即从堆顶弹出n + 1次。执行完毕后，将这些任务的堆积数减去1，并重新加入堆中。重复这个选择的过程直到堆为空。

每一轮的执行时间都是n + 1，但是需要特别注意最后一轮的执行时间为剩余的任务数。将执行时间累积即为最后答案。

最后附上python代码：

```python
import heapq

class Solution(object):
    def leastInterval(self, tasks, n):
        """
        :type tasks: List[str]
        :type n: int
        :rtype: int
        """

        task_dict = {}
        for task in tasks:
            task_dict[task] = task_dict.get(task, 0) + 1

        heap = [[-cnt, task] for task, cnt in task_dict.items()]
        heapq.heapify(heap)

        res = 0
        while True:
            round_task = []
            for index in range(n + 1):
                if heap:
                    round_task.append(heapq.heappop(heap))
                    round_task[-1][0] += 1
            
            for cnt, task in round_task:
                if cnt < 0:
                    heapq.heappush(heap, [cnt, task])
            
            if heap:
                res += n + 1
            else:
                return res + len(round_task)
```
