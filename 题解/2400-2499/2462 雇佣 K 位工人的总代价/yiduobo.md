---
title: "2462. 雇佣K位工人的总代价"
aliases: ["yiduobo的每日leetcode 2462.雇佣K位工人的总代价"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/quickselect", "leetcode/sorting", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/586805654"
zhihu_id: "586805654"
zhihu_title: "yiduobo的每日leetcode 2462.雇佣K位工人的总代价"
question_id: "2462"
question: "雇佣 K 位工人的总代价"
problem_url: "https://leetcode.cn/problems/total-cost-to-hire-k-workers/"
difficulty: "Medium"
rating: 1764
created: "2022-11-26T04:08:03+08:00"
updated: "2022-11-26T04:08:03+08:00"
upvotes: 0
comments: 0
---

# 2462. 雇佣K位工人的总代价

> **[yiduobo的每日leetcode 2462.雇佣K位工人的总代价](https://zhuanlan.zhihu.com/p/586805654) · 知乎 · 2022-11-26 · 赞同 0**
> 力扣：[2462. 雇佣 K 位工人的总代价](https://leetcode.cn/problems/total-cost-to-hire-k-workers/) · Medium · 灵茶山艾府：[两个最小堆模拟（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2462.雇佣K位工人的总代价

[力扣](https://leetcode.cn/problems/total-cost-to-hire-k-workers/)

首先，当candidates \* 2 >\= n时，从最初这一轮开始所有工人都是可以选择的，那么此时只需要将这些工人以cost为第一关键字，下标为第二关键字排序或者加入到堆中，然后按顺序取top k即可。

另一方面，若candidates \* 2 \< n，那么一开始只能从头部或者尾部选择工人，此时则需要使用堆来维护这些工人，同时使用两个变量left和right分别表示当前已经加入堆中的头部工人的最大下标，以及已经加入堆中的尾部工人的最小下标。接下来，若当前这一轮选择的工人的下标小于等于left，那么说明这是一名头部的工人，此时需要将left加入1，然后将left对应的工人加入到堆中。同样的，若选择的工人的下标大于等于right，那么就应该将right减去1，然后将right对应的工人加入到堆中。

重复此过程，直到left与right交汇，也就是所有剩余工人都在堆中，或者已经选出了k名工人为止。对于后面这种情况，返回选择的总代价即可，而对于前面这种情况，则又回到了最开始这种情况，此时从堆中选出剩余的top k即可。

最后附上python代码：

```python
class Solution(object):
    def totalCost(self, costs, k, candidates):
        """
        :type costs: List[int]
        :type k: int
        :type candidates: int
        :rtype: int
        """

        n = len(costs)
        heap = []
        res = 0

        if candidates * 2 < n:
            left = candidates - 1
            right = n - candidates
            for index in range(left + 1):
                heapq.heappush(heap, [costs[index], index])
            for index in range(right, n):
                heapq.heappush(heap, [costs[index], index])

            while left + 1 < right and k > 0:
                min_cost, index = heapq.heappop(heap)
                res += min_cost
                if index <= left:
                    left += 1
                    heapq.heappush(heap, [costs[left], left])
                else:
                    right -= 1
                    heapq.heappush(heap, [costs[right], right])

                k -= 1

        else:
            for index in range(n):
                heapq.heappush(heap, [costs[index], index])

        while k > 0:
            min_cost, index = heapq.heappop(heap)
            res += min_cost
            k -= 1

        return res
```
