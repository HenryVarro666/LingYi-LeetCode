---
title: "3578. 统计极差最大为k的分割方案数"
aliases: ["yiduobo的每日leetcode 3578.统计极差最大为k的分割方案数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/sliding-window", "leetcode/monotonic-queue", "题单/动态规划", "题单/动态规划/五-划分型-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1937508573665006718"
zhihu_id: "1937508573665006718"
zhihu_title: "yiduobo的每日leetcode 3578.统计极差最大为k的分割方案数"
question_id: "3578"
question: "统计极差最大为 K 的分割方式数"
problem_url: "https://leetcode.cn/problems/count-partitions-with-max-min-difference-at-most-k/"
difficulty: "Medium"
rating: 2033
created: "2025-08-09T14:07:39+08:00"
updated: "2025-08-09T14:07:40+08:00"
upvotes: 1
comments: 0
---

# 3578. 统计极差最大为k的分割方案数

> **[yiduobo的每日leetcode 3578.统计极差最大为k的分割方案数](https://zhuanlan.zhihu.com/p/1937508573665006718) · 知乎 · 2025-08-09 · 赞同 1**
> 力扣：[3578. 统计极差最大为 K 的分割方式数](https://leetcode.cn/problems/count-partitions-with-max-min-difference-at-most-k/) · Medium · 灵茶山艾府：[划分型 DP + 单调队列优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3578.统计极差最大为k的分割方案数

[3578. 统计极差最大为 K 的分割方式数 - 力扣（LeetCode）](https://leetcode.cn/problems/count-partitions-with-max-min-difference-at-most-k/description/)

题目给出一个整数数组nums以及一个整数k，nums的长度可达50000。现在要求将nums分割成一个或者多个非空的连续子段，使得每个子段的最大值和最小值之差不超过k。问一共有多少种合法的分割方案。

对于这类划分类问题，没有很直观的贪心方案时可以考虑使用动态规划求解。令f[index]表示分割nums[0]到nums[index]这一段的合法方案数，那么对于f[index]，可以枚举分割点p，若nums[p]到nums[index]这一段的最大值和最小值之差不超过k，那么可以将f[p - 1]累加到f[index]中。

以上算法的状态表示为O(n)，转移时枚举p的复杂度为O(n)，另外还需要考虑如何判断子数组中最大值和最小值之差是否不超过k，在时间复杂度层面显然是不行的，需要进行优化。

首先可以明确的是，在固定了子数组的右边界index后，对于某个合法的左边界p，任意大于p的左边界q也是合法的，理由相比nums[p]到nums[index]而言，nums[q]到nums[index]的最小值必然更大，而nums[q]到nums[index]的最大值则必然更小，因此当p合法时，q必然也合法。

基于这一点，就可以利用变长滑动窗口，在右边界index向右移动的过程中，维护最小的合法左边界p，此时转移方程就变成了f[index] \= f[p - 1] + f[p - 2] + ... + f[index - 1]。这是一个区间和的形式，利用前缀和就可以在O(1)的时间内完成转移。

另一方面，维护这个左边界p则需要知道当前窗口中的最大值和最小值，对于这个问题则可以参考之前滑动窗口最大值的处理方法，使用单调队列或者堆来求解。

其中单调队列的做法是基于随着窗口的移动，可能成为最值的元素必然是单调的。以最大值为例，对于窗口内的两个元素x和y而言，若x >\= y且x在y的右侧，那么y就不可能成为窗口内的最大值，因为x的寿命比y长，而且x的值更大。基于这一点，就可以使用一个双端队列来维护窗口内依然可能成为最大值的元素，这样一来，队列中的元素必然是单调递减的。接下来，每当来了一个新元素，可以先淘汰掉队尾更小的元素，然后将其加入队列，而当队列向后移动时，若队首元素在窗口为，则也应该淘汰掉。

基于堆的方法则比较直观，直接使用堆来维护窗口内的最值，当窗口右边界移动时将新的元素加入堆中，左边界移动时则采取懒删除的方式从堆中删去对应的元素。

最后附上python代码：

```python
class Solution(object):
    def countPartitions(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        f = [1]
        sf = [1, 2]
        ma_heap = [-nums[0]]
        mi_heap = [nums[0]]
        p = 0
        ma_remove = {}
        mi_remove = {}

        mod = 10 ** 9 + 7
        for v in nums[1:]:
            while (ma_heap and -ma_heap[0] - v > k) or (mi_heap and v - mi_heap[0] > k):
                ma_remove[nums[p]] = ma_remove.get(nums[p], 0) + 1
                mi_remove[nums[p]] = mi_remove.get(nums[p], 0) + 1
                p += 1
                while ma_heap and ma_remove.get(-ma_heap[0], 0) > 0:
                    ma_remove[-ma_heap[0]] -= 1
                    heapq.heappop(ma_heap)
                while mi_heap and mi_remove.get(mi_heap[0], 0) > 0:
                    mi_remove[mi_heap[0]] -= 1
                    heapq.heappop(mi_heap)

            heapq.heappush(ma_heap, -v)
            heapq.heappush(mi_heap, v)
            if p == 0:
                f.append(sf[-1])
            else:
                f.append((sf[-1] - sf[p - 1] + mod) % mod)
                
            sf.append(f[-1] + sf[-1])
            if sf[-1] >= mod:
                sf[-1] %= mod

        return f[-1]
```
