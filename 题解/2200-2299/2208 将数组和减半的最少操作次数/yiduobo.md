---
title: "2208. 将数组和减半的最少操作次数"
aliases: ["yiduobo的每日leetcode 2208.将数组和减半的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/heap", "leetcode/greedy", "leetcode/you-xian-dui-lie", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/539920206"
zhihu_id: "539920206"
zhihu_title: "yiduobo的每日leetcode 2208.将数组和减半的最少操作次数"
question_id: "2208"
question: "将数组和减半的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-halve-array-sum/"
difficulty: "Medium"
rating: 1550
created: "2022-07-10T19:28:37+08:00"
updated: "2022-07-10T19:28:37+08:00"
upvotes: 0
comments: 0
---

# 2208. 将数组和减半的最少操作次数

> **[yiduobo的每日leetcode 2208.将数组和减半的最少操作次数](https://zhuanlan.zhihu.com/p/539920206) · 知乎 · 2022-07-10 · 赞同 0**
> 力扣：[2208. 将数组和减半的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-halve-array-sum/) · Medium · 灵茶山艾府：[避免浮点数的写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2208.将数组和减半的最少操作次数

[力扣](https://leetcode.cn/problems/minimum-operations-to-halve-array-sum/)

为了尽快使得总和减下来，因此每一轮都应该将数组中最大的数减半，因此可以维护一个堆，其中堆顶元素为当前数组中的最大值。每一轮将堆顶弹出，减半后再加回到堆中直到总和减半。

可以证明的是，总的操作次数不会超过n次，因为即使不适用任何策略直接对数组中的每个数操作一次，得到的数组和就已经减半了，此时的操作次数恰好是n次。因此，最终的时间复杂度就是O(nlogn)。

最后附上python代码：

```python
class Solution(object):
    def halveArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        s = sum(nums)
        target = s / 2.0
        
        heap = []
        for num in nums:
            heapq.heappush(heap, -num)
        
        step = 0
        while s > target:
            step += 1
            max_num = -heapq.heappop(heap)
            max_num /= 2.0
            s -= max_num
            heapq.heappush(heap, -max_num)
        
        return step
```
