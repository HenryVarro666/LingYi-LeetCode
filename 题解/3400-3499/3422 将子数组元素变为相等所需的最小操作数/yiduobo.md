---
title: "3422. 将子数组元素变为相等所需的最小操作数"
aliases: ["yiduobo的每日leetcode 3422.将子数组元素变为相等所需的最小操作数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1888399581827540195"
zhihu_id: "1888399581827540195"
zhihu_title: "yiduobo的每日leetcode 3422.将子数组元素变为相等所需的最小操作数"
question_id: "3422"
question: "将子数组元素变为相等所需的最小操作数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-subarray-elements-equal/"
created: "2025-03-27T01:33:41+08:00"
updated: "2025-03-27T01:33:41+08:00"
upvotes: 1
comments: 0
---

# 3422. 将子数组元素变为相等所需的最小操作数

> **[yiduobo的每日leetcode 3422.将子数组元素变为相等所需的最小操作数](https://zhuanlan.zhihu.com/p/1888399581827540195) · 知乎 · 2025-03-27 · 赞同 1**
> 力扣：[3422. 将子数组元素变为相等所需的最小操作数](https://leetcode.cn/problems/minimum-operations-to-make-subarray-elements-equal/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3422.将子数组元素变为相等所需的最小操作数

[3422. 将子数组元素变为相等所需的最小操作数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-make-subarray-elements-equal/description/)

题目给出一个整数数组nums以及一个整数k，可以将nums中的任意元素加上1或者减去1。现在要求通过操作使得nums中至少存在一个长度为k，且所有元素都相等的子数组。问最少需要多少次操作。

由于题目只需要最终数组中有一个长度为k且所有元素都相等的子数组，那么对于这个子数组之外的元素进行操作都是没有必要的，而对于这个子数组，则可以考察数组中所有长度为k的子数组，计算将当前子数组中所有元素都变为相等的操作数是多少。

对于一个数组arr，将arr中所有元素都变为相等的最优方案就是将所有元素都变为arr的中位数。证明也很简单，只需将arr排序后，按大小顺序一大一小进行分组，那么对于每一组的元素(left, right)，如果最终目标target在left到right之间，那么将left和right都变为target的操作次数就是right - left，否则的话需要的操作次数必然大于right - left。接下来对于每一组这样的元素，让target保持在每一组元素之间是最优的选项，那么在这里就应该选择中位数作为target。

换言之，本题实际上就是要计算nums中每个长度为k的子数组的中位数，同时计算将这些子数组的元素都变为对应的中位数所需的操作次数。

对于滑动窗口中位数的问题，可以参考之前的480题，使用两个堆来进行处理。

[yiduobo：yiduobo的每日leetcode 480.滑动窗口中位数](https://zhuanlan.zhihu.com/p/246224986)

而对于操作次数的计算，则只需额外维护这两个堆中元素之和，那么小堆中的元素都变为中位数的操作次数就是小堆中元素的数量乘以中位数，再减去小堆中元素之和，而大堆需要的操作次数则为大堆中元素之和，减去小堆中元素的数量乘以中位数。

另外值得一提的是，之前480还是困难难度，但是本题更加复杂，却只有中等难度了，令人感慨。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        min_heap = []
        max_heap = []
        s_min = 0
        s_max = 0
        max_size = k // 2
        min_size = k - max_size

        for num in nums[:k]:
            heapq.heappush(min_heap, -num)
            s_min += num

        for index in range(k // 2):
            heapq.heappush(max_heap, -min_heap[0])
            s_min += min_heap[0]
            s_max -= min_heap[0]
            heapq.heappop(min_heap)

        res = min_size * (-min_heap[0]) - s_min + s_max - max_size * (-min_heap[0])
        del_dict = {}
        for index in range(k, len(nums)):

            del_num = nums[index - k]
            del_dict[del_num] = del_dict.get(del_num, 0) + 1

            delta = 0
            if max_heap and del_num >= max_heap[0]:
                delta = 1
                s_max -= del_num
            else:
                delta = -1
                s_min -= del_num

            add_num = nums[index]
            if max_heap and add_num >= max_heap[0]:
                heapq.heappush(max_heap, add_num)
                s_max += add_num
                delta -= 1
            else:
                heapq.heappush(min_heap, -add_num)
                s_min += add_num
                delta += 1
            
            if delta > 0:
                heapq.heappush(max_heap, -min_heap[0])
                s_min += min_heap[0]
                s_max -= min_heap[0]
                heapq.heappop(min_heap)
            elif delta < 0:
                heapq.heappush(min_heap, -max_heap[0])
                s_max -= max_heap[0]
                s_min += max_heap[0]
                heapq.heappop(max_heap)

            while max_heap and del_dict.get(max_heap[0], 0) > 0:
                del_dict[max_heap[0]] -= 1
                heapq.heappop(max_heap)

            while min_heap and del_dict.get(-min_heap[0], 0) > 0:
                del_dict[-min_heap[0]] -= 1
                heapq.heappop(min_heap)
            
            res = min(res, min_size * (-min_heap[0]) - s_min + s_max - max_size * (-min_heap[0]))

        return res
```
