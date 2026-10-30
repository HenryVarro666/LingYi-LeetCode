---
title: "3672. 子数组中加权众数的总和"
aliases: ["yiduobo的每日leetcode 3672.子数组中加权众数的总和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1952804402302812438"
zhihu_id: "1952804402302812438"
zhihu_title: "yiduobo的每日leetcode 3672.子数组中加权众数的总和"
question_id: "3672"
question: "子数组中加权众数的总和"
problem_url: "https://leetcode.cn/problems/sum-of-weighted-modes-in-subarrays/"
created: "2025-09-20T18:45:49+08:00"
updated: "2025-09-20T18:45:49+08:00"
upvotes: 0
comments: 0
---

# 3672. 子数组中加权众数的总和

> **[yiduobo的每日leetcode 3672.子数组中加权众数的总和](https://zhuanlan.zhihu.com/p/1952804402302812438) · 知乎 · 2025-09-20 · 赞同 0**
> 力扣：[3672. 子数组中加权众数的总和](https://leetcode.cn/problems/sum-of-weighted-modes-in-subarrays/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3672.子数组中加权众数的总和

[3672. 子数组中加权众数的总和 - 力扣（LeetCode）](https://leetcode.cn/problems/sum-of-weighted-modes-in-subarrays/description/)

题目给出一个整数数组nums以及一个整数k。

对于每个长度为k的子数组，定义其权重为子数组中的重数mode，乘以mode在子数组中出现的次数。若子数组中存在多个众数，则取其中最小的那个。

问所有长度为k的子数组的权重之和。

题目实际上要计算的就是滑动窗口的众数，对于这个问题，只需要使用一个哈希表记录窗口内每种元素出现的次数，另外使用一个堆，使用懒更新的策略来维护窗口中的这些元素以及出现次数就行了。

最后附上python代码：

```python
class Solution(object):
    def modeWeight(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        heap = []
        freq = {}
        for v in nums[:k]:
            freq[v] = freq.get(v, 0) + 1
        
        for v in freq:
            heapq.heappush(heap, (-freq[v], v))
        
        res = -heap[0][0] * heap[0][1]
        for index, v in enumerate(nums[k:]):
            if nums[index] != v:
                freq[nums[index]] -= 1
                if freq[nums[index]] > 0:
                    heapq.heappush(heap, (-freq[nums[index]], nums[index]))
                freq[v] = freq.get(v, 0) + 1
                heapq.heappush(heap, (-freq[v], v))
                while freq[heap[0][1]] != -heap[0][0]:
                    heapq.heappop(heap)

            res += -heap[0][0] * heap[0][1]
        
        return res
```
