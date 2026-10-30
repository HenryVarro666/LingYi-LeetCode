---
title: "3505. 使K个子数组内元素相等的最少操作数"
aliases: ["yiduobo的每日leetcode 3505.使K个子数组内元素相等的最少操作数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/hash-table", "leetcode/dynamic-programming", "leetcode/sliding-window", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/五-堆-优先队列", "题单/动态规划/五-划分型-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1901792848795402742"
zhihu_id: "1901792848795402742"
zhihu_title: "yiduobo的每日leetcode 3505.使K个子数组内元素相等的最少操作数"
question_id: "3505"
question: "使 K 个子数组内元素相等的最少操作数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-elements-within-k-subarrays-equal/"
difficulty: "Hard"
rating: 2539
created: "2025-05-03T00:32:00+08:00"
updated: "2025-05-03T00:32:00+08:00"
upvotes: 0
comments: 0
---

# 3505. 使K个子数组内元素相等的最少操作数

> **[yiduobo的每日leetcode 3505.使K个子数组内元素相等的最少操作数](https://zhuanlan.zhihu.com/p/1901792848795402742) · 知乎 · 2025-05-03 · 赞同 0**
> 力扣：[3505. 使 K 个子数组内元素相等的最少操作数](https://leetcode.cn/problems/minimum-operations-to-make-elements-within-k-subarrays-equal/) · Hard · 灵茶山艾府：[滑动窗口中位数 + 距离和 + 划分型 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3505.使K个子数组内元素相等的最少操作数

[3505. 使 K 个子数组内元素相等的最少操作数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-make-elements-within-k-subarrays-equal/description/)

题目给出一个整数数组nums以及两个整数x和k，其中nums的长度以及x的大小不超过10^5，k的大小在1到15之间。接下来可以对nums进行一些操作，每次操作可以将nums中的任意元素加1或者减1。

现在需要通过操作使得nums中至少包含k个长度恰好为x，且互不重叠的子数组，对于单个子数组而言，其中的元素必须完全相同。问最少需要执行多少次操作。

对于这类划分类问题，依然还是尝试用动态规划来处理。从题目给出的数据规模来看，使用时间复杂度为O(nk)的算法应该是可行的，那么可以令f[index][p]表示使得nums[0]到nums[index]之间具有p个合法子数组时所需的最少操作数，那么对于f[index][p]：

1、放弃掉nums[index]：

这种情况下，就有f[index][p] \= f[index - 1][p]

2、使用nums[index]：

这种情况下，需要通过操作将nums[index - x + 1]到nums[index]这一段变为元素都相同的子数组，不妨记需要的操作次数为cost[index]，那么就有f[index][p] \= f[index - x][p - 1] + cost[index]

接下来的问题就是如何计算每个cost[index]。

可以发现，这又是经典的贪心问题，将区间中的所有元素变为中位数时所需的操作次数最少。于是可以在执行动态规划之前，先使用一个大小为x的滑动窗口从nums头部开始向后移动，计算窗口的中位数以及所需的操作数。具体实现可以参考之前的3422题或者480题

[yiduobo：yiduobo的每日leetcode 3422.将子数组元素变为相等所需的最小操作数](https://zhuanlan.zhihu.com/p/1888399581827540195)

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums, x, k):
        """
        :type nums: List[int]
        :type x: int
        :type k: int
        :rtype: int
        """
        
        min_heap = []
        max_heap = []
        s_min = 0
        s_max = 0
        max_size = x // 2
        min_size = x - max_size

        for num in nums[:x]:
            heapq.heappush(min_heap, -num)
            s_min += num

        for index in range(x // 2):
            heapq.heappush(max_heap, -min_heap[0])
            s_min += min_heap[0]
            s_max -= min_heap[0]
            heapq.heappop(min_heap)

        n = len(nums)
        cost = [0] * n
        cost[x - 1] = min_size * (-min_heap[0]) - s_min + s_max - max_size * (-min_heap[0])
        del_dict = {}
        for index in range(x, n):

            del_num = nums[index - x]
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
            
            cost[index] = min_size * (-min_heap[0]) - s_min + s_max - max_size * (-min_heap[0])

        
        f = [[0] * (k + 1) for _ in range(n)]
        for p in range(1, k + 1):
            for index in range(p * x - 1, n):
                f[index][p] = f[index - x][p - 1] + cost[index]
                if index > p * x - 1:
                    f[index][p] = min(f[index][p], f[index - 1][p])
        
        return f[-1][-1]
```
