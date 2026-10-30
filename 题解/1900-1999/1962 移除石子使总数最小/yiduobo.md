---
title: "1962. 移除石子使总数最小"
aliases: ["yiduobo的每日leetcode 1962.移除石子使总数最小"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/494120860"
zhihu_id: "494120860"
zhihu_title: "yiduobo的每日leetcode 1962.移除石子使总数最小"
question_id: "1962"
question: "移除石子使总数最小"
problem_url: "https://leetcode.cn/problems/remove-stones-to-minimize-the-total/"
difficulty: "Medium"
rating: 1419
created: "2022-04-07T00:23:36+08:00"
updated: "2022-04-07T00:23:36+08:00"
upvotes: 0
comments: 0
---

# 1962. 移除石子使总数最小

> **[yiduobo的每日leetcode 1962.移除石子使总数最小](https://zhuanlan.zhihu.com/p/494120860) · 知乎 · 2022-04-07 · 赞同 0**
> 力扣：[1962. 移除石子使总数最小](https://leetcode.cn/problems/remove-stones-to-minimize-the-total/) · Medium · 灵茶山艾府：[原地堆化 O(1) 空间（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1962.移除石子使总数最小

[力扣](https://leetcode-cn.com/problems/remove-stones-to-minimize-the-total/)

为了使得剩余的石子数最小，那么就应该选择当前剩余石子数最多的那一堆，移除其中的一半。于是在这里可以使用一个大顶堆来维护每一堆剩余的石子数量，然后执行k轮，每轮弹出堆顶，移除一半，然后再将剩余的重新加入到堆中。

最后附上python代码：

```python
class Solution(object):
    def minStoneSum(self, piles, k):
        """
        :type piles: List[int]
        :type k: int
        :rtype: int
        """

        heap = [-x for x in piles]
        heapq.heapify(heap)
        res = sum(piles)
        for _ in range(k):
            max_n = -heapq.heappop(heap)
            res -= max_n / 2
            max_n = (max_n + 1) / 2
            heapq.heappush(heap, -max_n)

        return res
```
