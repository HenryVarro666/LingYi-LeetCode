---
title: "2530. 执行K次操作后的最大分数"
aliases: ["yiduobo的每日leetcode 2530.执行K次操作后的最大分数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/636898534"
zhihu_id: "636898534"
zhihu_title: "yiduobo的每日leetcode 2530.执行K次操作后的最大分数"
question_id: "2530"
question: "执行 K 次操作后的最大分数"
problem_url: "https://leetcode.cn/problems/maximal-score-after-applying-k-operations/"
difficulty: "Medium"
rating: 1386
created: "2023-06-14T00:21:41+08:00"
updated: "2023-06-14T00:21:41+08:00"
upvotes: 0
comments: 0
---

# 2530. 执行K次操作后的最大分数

> **[yiduobo的每日leetcode 2530.执行K次操作后的最大分数](https://zhuanlan.zhihu.com/p/636898534) · 知乎 · 2023-06-14 · 赞同 0**
> 力扣：[2530. 执行 K 次操作后的最大分数](https://leetcode.cn/problems/maximal-score-after-applying-k-operations/) · Medium · 灵茶山艾府：[O(1) 空间做法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2530.执行K次操作后的最大分数

[力扣](https://leetcode.cn/problems/maximal-score-after-applying-k-operations/)

题目中的各个整数间互不影响，因此只需每一轮都选择当前数组中的最大值进行操作，一共选择k轮就行了。为了高效获取到当前数组中的最大值，则需要使用一个堆来维护当前数组中的数。

另外需要注意的是本题的操作中，操作数除以3之后需要向上取整，而常规的整除操作则是向下取整，需要进行特殊处理。

最后附上python代码：

```python
class Solution(object):
    def maxKelements(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        heap = []
        for x in nums:
            heapq.heappush(heap, -x)
        
        res = 0
        for _ in range(k):
            ma = -heapq.heappop(heap)
            res += ma
            if ma % 3 == 0:
                ma /= 3
            else:
                ma = ma / 3 + 1
            
            heapq.heappush(heap, -ma)

        return res
```
