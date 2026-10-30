---
title: "1353. 最多可以参加的会议数目"
aliases: ["yiduobo的每日leetcode 1353.最多可以参加的会议数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/union-find", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/五-堆-优先队列", "题单/常用数据结构/七-并查集", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/398071134"
zhihu_id: "398071134"
zhihu_title: "yiduobo的每日leetcode 1353.最多可以参加的会议数目"
question_id: "1353"
question: "最多可以参加的会议数目"
problem_url: "https://leetcode.cn/problems/maximum-number-of-events-that-can-be-attended/"
difficulty: "Medium"
rating: 2016
created: "2021-08-09T23:01:48+08:00"
updated: "2021-08-09T23:01:48+08:00"
upvotes: 2
comments: 0
---

# 1353. 最多可以参加的会议数目

> **[yiduobo的每日leetcode 1353.最多可以参加的会议数目](https://zhuanlan.zhihu.com/p/398071134) · 知乎 · 2021-08-09 · 赞同 2**
> 力扣：[1353. 最多可以参加的会议数目](https://leetcode.cn/problems/maximum-number-of-events-that-can-be-attended/) · Medium · 灵茶山艾府：[两种方法：最小堆 / 并查集（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1353.最多可以参加的会议数目

[力扣](https://leetcode-cn.com/problems/maximum-number-of-events-that-can-be-attended/)

由于题目中所有会议的价值都是相同的，那么在某一时刻，若可以参加两个会议，我们就应该选择参加结束时间较早的那个，于是一个做法就是先将所有会议按照起始时间从小到大进行排序，然后从1开始枚举时间t，并使用一个p来表示当前已经开始的会议。

对于t这一天，我们先使用t来更新此时已经开始的会议，并将这些会议的结束时间加入到堆中。由于会议已经按开始时间排过序了，因此我们只需要向后移动p并检测p对应的会议的开始时间与t的大小就可以更新此时已经开始的会议。

接下来我们弹出堆顶的时间，若堆顶的时间大于等于t，说明此时堆顶代表的会议还未结束，那么t这一天就应该参加堆顶代表的会议，此时应该更新答案；若对应的时间小于t，说明堆顶代表的会议已经结束，那么我们需要重复这个过程，直到找出一个未结束的会议，或者堆为空。

若某一时刻p到了数组的末尾，同时堆为空，说明已经没有候选的会议了。

最后附上python代码：

```python
class Solution(object):
    def maxEvents(self, events):
        """
        :type events: List[List[int]]
        :rtype: int
        """

        n = len(events)
        events = sorted(events, key=lambda d:d[0])
        heap = []

        max_t = 0
        for index in range(n):
            max_t = max(max_t, events[index][1])

        t = 1
        p = 0
        res = 0
        while t <= max_t:
            while p < n and events[p][0] <= t:
                heapq.heappush(heap, events[p][1])
                p += 1

            while heap:
                if heap[0] >= t:
                    break
                heapq.heappop(heap)
            
            if heap:
                res += 1
                heapq.heappop(heap)
            else:
                if p == n:
                    break

            t += 1

        return res
```
