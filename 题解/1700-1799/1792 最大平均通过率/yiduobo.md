---
title: "1792. 最大平均通过率"
aliases: ["yiduobo的每日leetcode 1792.最大平均通过率"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/463369317"
zhihu_id: "463369317"
zhihu_title: "yiduobo的每日leetcode 1792.最大平均通过率"
question_id: "1792"
question: "最大平均通过率"
problem_url: "https://leetcode.cn/problems/maximum-average-pass-ratio/"
difficulty: "Medium"
rating: 1818
created: "2022-01-31T18:18:15+08:00"
updated: "2022-01-31T18:18:15+08:00"
upvotes: 0
comments: 0
---

# 1792. 最大平均通过率

> **[yiduobo的每日leetcode 1792.最大平均通过率](https://zhuanlan.zhihu.com/p/463369317) · 知乎 · 2022-01-31 · 赞同 0**
> 力扣：[1792. 最大平均通过率](https://leetcode.cn/problems/maximum-average-pass-ratio/) · Medium · 灵茶山艾府：[转化成 n 个单调递减序列，从中选最大的 k 个数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1792.最大平均通过率

[力扣](https://leetcode-cn.com/problems/maximum-average-pass-ratio/)

首先可以明确的是，对于同一个班级而言，越往里面加入学生，对通过率的提升率是越小的。证明也很简单，不妨设现在有一个班级的通过人数和总人数分别为x和y，那么初始状况下通过率为x/y。加入一个学生后，通过率变为(x + 1) / (y + 1)，提升了(x + 1) / (y + 1) - x / y。再加入一个学生后，则变成了(x + 2) / (y + 2)，提升了(x + 2) / (y + 2) - (x + 1) / (y + 1)

两个式子分别通分，前者为

(y - x) / (y \* (y + 1))

后者为

(y - x) / ((y + 1) \* (y + 2))

前者显然大于后者，也就是说对同一个班级而言，通过率的提升是越来越小的。有了这个结论，就可以使用贪心法。每次都选择一个学生，加入到通过率提升最大的那个班级。由于单个班级加入新学生对通过率的提升是越来越小的，因此不可能出现需要铺垫若干学生才能带来巨大通过率提升的情况。

到了这里，很自然想到使用堆来维护每个班级当前的通过率提升，然后对于每个学生，都选择通过率提升最大的班级，将该学生加入到这个班级中，然后更新堆中的情况，直到每个学生都分配完成。

最后附上python代码：

```python
class Solution(object):
    def maxAverageRatio(self, classes, extraStudents):
        """
        :type classes: List[List[int]]
        :type extraStudents: int
        :rtype: float
        """

        heap = []
        for p, t in classes:
            heap.append([-((p + 1.0) / (t + 1.0) - p * 1.0 / t), p, t])
        heapq.heapify(heap)
        for index in range(extraStudents):
            rate, p, t = heapq.heappop(heap)
            p += 1
            t += 1
            heapq.heappush(heap, [-((p + 1.0) / (t + 1.0) - p * 1.0 / t), p, t])
 
        s = 0
        for rate, p, t in heap:
            s += p * 1.0 / t
        return s / len(heap)
```
