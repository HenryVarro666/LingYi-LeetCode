---
title: "2599. 使前缀和数组非负"
aliases: ["yiduobo的每日leetcode 2599.使前缀和数组非负"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/644194722"
zhihu_id: "644194722"
zhihu_title: "yiduobo的每日leetcode 2599.使前缀和数组非负"
question_id: "2599"
question: "使前缀和数组非负"
problem_url: "https://leetcode.cn/problems/make-the-prefix-sum-non-negative/"
created: "2023-07-18T01:14:14+08:00"
updated: "2023-07-18T01:14:14+08:00"
upvotes: 0
comments: 0
---

# 2599. 使前缀和数组非负

> **[yiduobo的每日leetcode 2599.使前缀和数组非负](https://zhuanlan.zhihu.com/p/644194722) · 知乎 · 2023-07-18 · 赞同 0**
> 力扣：[2599. 使前缀和数组非负](https://leetcode.cn/problems/make-the-prefix-sum-non-negative/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2599.使前缀和数组非负

[力扣](https://leetcode.cn/problems/make-the-prefix-sum-non-negative/)

题目中的操作会将某个数移动到数组的末尾，同时题目保证了必然有可行的前缀和生成方式，这也就意味着题目中的操作实际上可以认为是将前缀中的某个数删去。

对于当前的前缀，若前缀和大于等于0，那么就无须执行任何操作。反过来若前缀和小于0，那么至少需要从中删去一个数。很明显，此时应该删去当前前缀中的最小值。

根据这个结论，就可以使用一个堆来维护当前前缀中的所有负数。若某一时刻前缀和小于0，那么就将堆顶元素从前缀中删去，同时更新前缀和以及答案。

最后附上python代码：

```python
class Solution(object):
    def makePrefSumNonNegative(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        now = 0
        res = 0
        heap = []
        for v in nums:
            now += v
            heapq.heappush(heap, v)
            if now < 0:
                now -= heap[0]
                heapq.heappop(heap)
                res += 1
        
        return res
```
