---
title: "3430. 最多K个元素的子数组的最值之和"
aliases: ["yiduobo的每日leetcode 3430.最多K个元素的子数组的最值之和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/monotonic-stack", "题单/单调栈", "题单/单调栈/三-贡献法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1890194821982962071"
zhihu_id: "1890194821982962071"
zhihu_title: "yiduobo的每日leetcode 3430.最多K个元素的子数组的最值之和"
question_id: "3430"
question: "最多 K 个元素的子数组的最值之和"
problem_url: "https://leetcode.cn/problems/maximum-and-minimum-sums-of-at-most-size-k-subarrays/"
difficulty: "Hard"
rating: 2645
created: "2025-04-01T00:34:37+08:00"
updated: "2025-04-01T00:34:37+08:00"
upvotes: 0
comments: 0
---

# 3430. 最多K个元素的子数组的最值之和

> **[yiduobo的每日leetcode 3430.最多K个元素的子数组的最值之和](https://zhuanlan.zhihu.com/p/1890194821982962071) · 知乎 · 2025-04-01 · 赞同 0**
> 力扣：[3430. 最多 K 个元素的子数组的最值之和](https://leetcode.cn/problems/maximum-and-minimum-sums-of-at-most-size-k-subarrays/) · Hard · 灵茶山艾府：[贡献法+单调栈，两种计算子数组的方法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3430.最多K个元素的子数组的最值之和

[3430. 最多 K 个元素的子数组的最值之和 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-and-minimum-sums-of-at-most-size-k-subarrays/description/)

题目给出一个整数数组nums以及一个正整数k，要求计算nums中所有长度不超过k的非空子数组中的最大元素以及最小元素之和。

本题描述与之前的3428题类似，大体上依然是通过贡献法，计算nums中每个元素作为子数组中最大值以及最小值时的合法子数组数量，累加起来得到最终答案。不过本题要求找的是子数组而不是子序列，计算方法上完全不同。

首先需要考虑去重的问题。若某个子数组中的最大值或者最小值出现了多次，在这里是不应该多次计算的。为了防止这种情况出现，可以先约定若子数组中的最大值或者最小值如果出现了多次，那么只对首次出现的元素进行计算，其他元素不算。

由于作为最大值和最小值时处理方法是一样的，在这里先针对nums[index]作为子数组中最大值时如何计算合法子数组的数量来进行分析。

如果不考虑子数组长度小于等于k的限制，那么对于nums[index]，其往右可以扩展到第一个严格大于nums[index]的下标right_ma[index]的前一个位置，而往左则可以扩展到第一个大于等于nums[index]的下标left_ma[index]的后一个位置。

对于right_ma以及left_ma的计算，可以通过单调栈，正反两次遍历nums分别计算得到。

接下来考虑长度k这一限制。

将index本身考虑进去，那么就是可以从index向左扩展left \= index - left_ma[index]个元素，向右扩展right \= right_ma[index] - index个元素。由于超出k的部分都是没有用的，因此可以先将left和right分别修正为min(left, k)以及min(right, k)，那么包含nums[index]的子数组数目一共是left \* right的。不过其中可能包含某些长度大于k的子数组，需要将这些子数组减去。

对于这些子数组，最长的自然包含所有元素的，长度为left + right - 1的这个子数组，接下来对于长度为left + right - 2的子数组一共是两个，更一般的，对于长度为left + right - p的子数组，一共是p个。记max_length \= left + right - 1，那么当max_length > k时，所有长度大于k的子数组的数量为

1 + 2 + ... + (max_length - k) \= (max_length - k + 1) \* (max_length - k) // 2

那么这些子数组是否都包含nums[index]？答案是肯定的。因为有一个隐藏条件是left和right都小于等于k，那么对于长度大于k的子数组，其必然会包含中心位置的nums[index]。

这样一来，使用子数组的总数减去长度超过k的子数组的数目，就是合法子数组的数目。

对于nums[index]作为子数组中最小值的计算方法类似，先正反两趟遍历计算出含义与right_ma以及left_ma对称的right_mi以及left_mi，然后通过相同的方法计算出合法子数组的数目即可。

最后附上python代码：

```python
class Solution(object):
    def minMaxSubarraySum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        n = len(nums)

        ma_stack = []
        mi_stack = []
        right_ma = [n] * n
        right_mi = [n] * n
        for index in range(n):
            while ma_stack and nums[index] > nums[ma_stack[-1]]:
                right_ma[ma_stack.pop()] = index
            while mi_stack and nums[index] < nums[mi_stack[-1]]:
                right_mi[mi_stack.pop()] = index
            ma_stack.append(index)
            mi_stack.append(index)
        
        ma_stack = []
        mi_stack = []
        left_ma = [-1] * n
        left_mi = [-1] * n
        for index in range(n - 1, -1, -1):
            while ma_stack and nums[index] >= nums[ma_stack[-1]]:
                left_ma[ma_stack.pop()] = index
            while mi_stack and nums[index] <= nums[mi_stack[-1]]:
                left_mi[mi_stack.pop()] = index
            ma_stack.append(index)
            mi_stack.append(index)
        
        def calc(left, right):
            left = min(left, k)
            right = min(right, k)
            cnt = left * right
            max_length = left + right - 1
            if max_length > k:
                cnt -= (max_length - k + 1) * (max_length - k) // 2
            return cnt

        res = 0
        for index, v in enumerate(nums):
            res += v * (calc(index - left_ma[index], right_ma[index] - index) + calc(index - left_mi[index], right_mi[index] - index))
    
        return res
```
