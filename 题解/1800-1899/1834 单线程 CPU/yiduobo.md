---
title: "1834. 单线程CPU"
aliases: ["yiduobo的每日leetcode 1834.单线程CPU"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/heap", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/468392405"
zhihu_id: "468392405"
zhihu_title: "yiduobo的每日leetcode 1834.单线程CPU"
question_id: "1834"
question: "单线程 CPU"
problem_url: "https://leetcode.cn/problems/single-threaded-cpu/"
difficulty: "Medium"
rating: 1798
created: "2022-02-16T23:53:41+08:00"
updated: "2022-02-16T23:53:41+08:00"
upvotes: 0
comments: 0
---

# 1834. 单线程CPU

> **[yiduobo的每日leetcode 1834.单线程CPU](https://zhuanlan.zhihu.com/p/468392405) · 知乎 · 2022-02-16 · 赞同 0**
> 力扣：[1834. 单线程 CPU](https://leetcode.cn/problems/single-threaded-cpu/) · Medium · 灵茶山艾府：[Golang 堆](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1834.单线程CPU

[力扣](https://leetcode-cn.com/problems/single-threaded-cpu/)

没有想到什么特别好的转化方法，只能老老实实按题目描述的工作流程进行模拟。由于CPU每次都将执行当前堆积任务中执行耗时最短的任务，因此在这里需要使用一个堆来维护这些堆积的任务，从而高效地得到任意时刻堆积任务中耗时最短的任务是什么。处理之外，还需要维护一个时间t，表示CPU上一次空闲的时间。

由于题目中的任务进入队列的时间是又先后的，因此需要对所有任务按进入队列的时间为第一关键字，执行耗时为第二关键字，在原始数组中的下标为第三关键字从小到大进行排序。排序完成后一趟遍历，对于当前任务，设其进入队列的时间点为e，执行所需时间为p，在原数组中下标为id，那么：

1、若t \< e，说明在当前任务到达之前CPU还需要处理之前已经堆积的任务。若此时的堆不为空，那么就弹出堆顶的任务并执行，同时更新t和答案，直到t >\= e或者堆为空。

2、若此时的t依然小于等于e且堆为空，说明在当前任务到达时CPU是空闲的，且没有其他任务需要处理。而对于所有在e这一时间点到达的任务而言，由于之前排序的规则，当前任务必然是需要最先执行的，因此在这里可以让CPU直接执行当前任务，此时应该将t更新为e + p，同时将当前任务的编号id加入到答案中。

3、若不满足情况2，那么说明当前任务到达时CPU正在执行别的任务，因此需要将当前任务的耗时以及编号[p, id]加入到堆中。

遍历完成后，依然可能有仍在堆积的任务，此时执行不断弹出堆顶的任务并执行，直到堆为空为止。

最后附上python代码：

```python
class Solution(object):
    def getOrder(self, tasks):
        """
        :type tasks: List[List[int]]
        :rtype: List[int]
        """

        heap = []
        t = 0

        sorted_tasks = sorted([[task[0], task[1], index] for index, task in enumerate(tasks)], key=lambda d:(d[0], d[1], d[2]))
        res = []
        for e, p, id in sorted_tasks:
            while t < e and heap:
                min_p, min_id = heapq.heappop(heap)
                t += min_p
                res.append(min_id)
            
            if t <= e and not heap:
                res.append(id)
                t = e + p
            else:
                heapq.heappush(heap, [p, id])

        while heap:
            min_p, min_id = heapq.heappop(heap)
            res.append(min_id)
        
        return res
```
