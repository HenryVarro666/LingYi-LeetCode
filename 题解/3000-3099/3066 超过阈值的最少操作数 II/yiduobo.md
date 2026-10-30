---
title: "3066. 超过阈值的最少操作数II"
aliases: ["yiduobo的每日leetcode 3066.超过阈值的最少操作数II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/697080943"
zhihu_id: "697080943"
zhihu_title: "yiduobo的每日leetcode 3066.超过阈值的最少操作数II"
question_id: "3066"
question: "超过阈值的最少操作数 II"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-exceed-threshold-value-ii/"
difficulty: "Medium"
rating: 1400
created: "2024-05-11T00:35:00+08:00"
updated: "2024-05-11T00:35:00+08:00"
upvotes: 2
comments: 0
---

# 3066. 超过阈值的最少操作数II

> **[yiduobo的每日leetcode 3066.超过阈值的最少操作数II](https://zhuanlan.zhihu.com/p/697080943) · 知乎 · 2024-05-11 · 赞同 2**
> 力扣：[3066. 超过阈值的最少操作数 II](https://leetcode.cn/problems/minimum-operations-to-exceed-threshold-value-ii/) · Medium · 灵茶山艾府：[最小堆模拟（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3066.超过阈值的最少操作数II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-exceed-threshold-value-ii/description/)

题目每次要求从数组中选出最小的两个数进行操作，是动态的最小值问题，可以使用堆来处理。

具体来说，使用一个堆来储存数组中的数，每一轮执行两次弹出堆顶的操作，分别得到当前数组中的最小值x以及次小值y，接下来将x \* 2 + y重新加回到到堆中。重复此过程直到堆中的最小值大于等于k为止，执行的轮次即为最终荅案。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        heapq.heapify(nums)
        res = 0

        while nums[0] < k:
            x = heapq.heappop(nums)
            y = heapq.heappop(nums)
            heapq.heappush(nums, x * 2 + y)
            res += 1

        return res
```
