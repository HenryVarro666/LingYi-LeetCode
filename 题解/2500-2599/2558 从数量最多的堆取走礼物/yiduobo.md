---
title: "2558. 从数量最多的堆取走礼物"
aliases: ["yiduobo的每日leetcode 2558.从数量最多的堆取走礼物"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/simulation", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/639994176"
zhihu_id: "639994176"
zhihu_title: "yiduobo的每日leetcode 2558.从数量最多的堆取走礼物"
question_id: "2558"
question: "从数量最多的堆取走礼物"
problem_url: "https://leetcode.cn/problems/take-gifts-from-the-richest-pile/"
difficulty: "Easy"
rating: 1277
created: "2023-06-27T21:02:02+08:00"
updated: "2023-06-27T21:02:02+08:00"
upvotes: 1
comments: 0
---

# 2558. 从数量最多的堆取走礼物

> **[yiduobo的每日leetcode 2558.从数量最多的堆取走礼物](https://zhuanlan.zhihu.com/p/639994176) · 知乎 · 2023-06-27 · 赞同 1**
> 力扣：[2558. 从数量最多的堆取走礼物](https://leetcode.cn/problems/take-gifts-from-the-richest-pile/) · Easy · 灵茶山艾府：[原地堆化 O(1) 空间（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2558.从数量最多的堆取走礼物

[力扣](https://leetcode.cn/problems/take-gifts-from-the-richest-pile/)

题目都把大顶堆写在明面上了，那么就按照题目意思，使用一个堆来维护这些礼物，然后执行k轮，每轮都对堆顶的礼物进行相应的操作即可。

最后附上python代码：

```python
class Solution(object):
    def pickGifts(self, gifts, k):
        """
        :type gifts: List[int]
        :type k: int
        :rtype: int
        """

        heap = []
        for v in gifts:
            heapq.heappush(heap, -v)
        
        for _ in range(k):
            v = -heapq.heappop(heap)
            v = int(sqrt(v))
            heapq.heappush(heap, -v)
        
        return -sum(heap)
```
