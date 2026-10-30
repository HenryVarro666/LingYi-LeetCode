---
title: "3013. 将数组分成最小总代价的子数组II"
aliases: ["yiduobo的每日leetcode 3013.将数组分成最小总代价的子数组II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/ordered-set", "leetcode/sliding-window", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/694185060"
zhihu_id: "694185060"
zhihu_title: "yiduobo的每日leetcode 3013.将数组分成最小总代价的子数组II"
question_id: "3013"
question: "将数组分成最小总代价的子数组 II"
problem_url: "https://leetcode.cn/problems/divide-an-array-into-subarrays-with-minimum-cost-ii/"
difficulty: "Hard"
rating: 2540
created: "2024-04-24T02:16:07+08:00"
updated: "2024-04-24T02:16:07+08:00"
upvotes: 0
comments: 0
---

# 3013. 将数组分成最小总代价的子数组II

> **[yiduobo的每日leetcode 3013.将数组分成最小总代价的子数组II](https://zhuanlan.zhihu.com/p/694185060) · 知乎 · 2024-04-24 · 赞同 0**
> 力扣：[3013. 将数组分成最小总代价的子数组 II](https://leetcode.cn/problems/divide-an-array-into-subarrays-with-minimum-cost-ii/) · Hard · 灵茶山艾府：[两个有序集合维护前 k-1 小（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3013.将数组分成最小总代价的子数组II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/divide-an-array-into-subarrays-with-minimum-cost-ii/)

之前3010题的加强版

[yiduobo：yiduobo的每日leetcode 3010.将数组分成最小总代价的子数组I](https://zhuanlan.zhihu.com/p/693763600)

选取最小值作为子数组起点的思路依然不变，但是本题要求选出k个，同时这k个必须要在一个限定的距离内，换言之，本题实际上就是给出一个大小为dist + 1的滑动窗口，问窗口内最小的k个数之和是多少。

对于本题，可以参考之前的480题，使用一个小数堆和一个大数堆来解决。

[yiduobo：yiduobo的每日leetcode 480.滑动窗口中位数](https://zhuanlan.zhihu.com/p/246224986)

与480不同的是，本题中小数堆的大小为k，储存的就是滑动窗口中最小的k个数，而剩下的dist + 1 - k个数则储存在大数堆中。另外，还需要维护一个变量s来储存小数堆中数值之和用来更新答案。需要特别注意的是，s的值随着小堆的更新而更新，但是由于本题中的堆需要采取懒更新的做法，因此在最后弹出已失效元素时，不应该再更新s的值。

除此之外，其他的部分直接照搬480题的做法就行了。

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, nums, k, dist):
        """
        :type nums: List[int]
        :type k: int
        :type dist: int
        :rtype: int
        """

        min_heap = []
        max_heap = []
        k -= 1
        for num in nums[1: 1 + dist + 1]:
            heapq.heappush(max_heap, num)

        for index in range(k):
            heapq.heappush(min_heap, -max_heap[0])
            heapq.heappop(max_heap)

        s = nums[0] - sum(min_heap)
        res = s

        del_dict = Counter()

        for index in range(1 + dist + 1, len(nums)):
            del_num = nums[index - dist - 1]
            del_dict[del_num] += 1

            delta = 0
            if max_heap and del_num >= max_heap[0]:
                delta = 1
            else:
                delta = -1
                s -= del_num

            add_num = nums[index]
            if max_heap and add_num >= max_heap[0]:
                heapq.heappush(max_heap, add_num)
                delta -= 1
            else:
                heapq.heappush(min_heap, -add_num)
                s += add_num
                delta += 1
            
            if delta > 0:
                heapq.heappush(max_heap, -min_heap[0])
                s += min_heap[0]
                heapq.heappop(min_heap)
            elif delta < 0:
                heapq.heappush(min_heap, -max_heap[0])
                s += max_heap[0]
                heapq.heappop(max_heap)

            while max_heap and del_dict.get(max_heap[0], 0) > 0:
                del_dict[max_heap[0]] -= 1
                heapq.heappop(max_heap)

            while min_heap and del_dict.get(-min_heap[0], 0) > 0:
                del_dict[-min_heap[0]] -= 1
                heapq.heappop(min_heap)
            res = min(res, s)

        return res
```
