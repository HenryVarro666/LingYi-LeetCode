---
title: "3264. K次乘运算后的最终数组I & 3266. K次乘运算后的最终数组II"
aliases: ["yiduobo的每日leetcode 3264.K次乘运算后的最终数组I && 3266.K次乘运算后的最终数组II", "3264. K次乘运算后的最终数组I", "3266. K次乘运算后的最终数组II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/sorting", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/739145157"
zhihu_id: "739145157"
zhihu_title: "yiduobo的每日leetcode 3264.K次乘运算后的最终数组I && 3266.K次乘运算后的最终数组II"
question_id: ["3264", "3266"]
question: ["K 次乘运算后的最终数组 I", "K 次乘运算后的最终数组 II"]
problem_url: ["https://leetcode.cn/problems/final-array-state-after-k-multiplication-operations-i/", "https://leetcode.cn/problems/final-array-state-after-k-multiplication-operations-ii/"]
difficulty: ["Easy", "Hard"]
rating: ["1178", "2509"]
created: "2024-09-27T23:19:12+08:00"
updated: "2024-09-27T23:19:12+08:00"
upvotes: 1
comments: 0
---

# 3264. K次乘运算后的最终数组I & 3266. K次乘运算后的最终数组II

> **[yiduobo的每日leetcode 3264.K次乘运算后的最终数组I && 3266.K次乘运算后的最终数组II](https://zhuanlan.zhihu.com/p/739145157) · 知乎 · 2024-09-27 · 赞同 1**
> 力扣：[3264. K 次乘运算后的最终数组 I](https://leetcode.cn/problems/final-array-state-after-k-multiplication-operations-i/) · Easy · 灵茶山艾府：[复杂度和 k 无关的做法（Python/Java/C++/Go）](../3264%20K%20次乘运算后的最终数组%20I/灵茶山艾府.md)
> 力扣：[3266. K 次乘运算后的最终数组 II](https://leetcode.cn/problems/final-array-state-after-k-multiplication-operations-ii/) · Hard · 灵茶山艾府：[最小堆模拟+数学公式+优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3264.K次乘运算后的最终数组I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/final-array-state-after-k-multiplication-operations-i/description/)

3266.K次乘运算后的最终数组II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/final-array-state-after-k-multiplication-operations-ii/description/)

题目给出一个整数数组nums以及一个整数k和一个整数multiplier。现在要求对nums数组执行k次操作，每次操作都取当前nums中最小且下标最靠前的元素x，将其乘以multiplier。问执行k次操作后的nums数组是什么样的。

第一题中的k最大为10，可以直接暴力模拟。

第二题的数据规模较大，nums的规模为10^4，k的大小可达10^9，nums中元素的大小可达10^9。

按照题目描述，最直观的做法自然是使用堆来维护nums，每次从中取出元素值和小标最小的元素x，将其乘以multiplier，一共执行k轮。不过本题中k的规模非常大，直接模拟显然是不行的，需要进行优化。

首先还是先考虑特殊情况。

当multiplier为1时，无论怎么操作nums都不会产生变化，此时直接返回nums数组就行了。

接下来是一般情况。方便起见接下来记multiplier为mul

由于题目中每次操作的乘数mul都一样，那么不妨考虑下面的情况：

对于两个数a和b，设a \<\= b且a \* mul > b，那么对于a \* (mul^p[a])与b \* (mul^p[b])这两个数，当p[a]和p[b]相同时，前者一定小于等于后者，此时应该对前者执行一次操作；而当p[a] \= p[b] + 1时，前者一定更大，此时就应该对后者执行一次操作。换言之，一旦来到a和b这种大小关系时，就会出现轮流执行操作的情况。

更进一步的，对于多个数的情况也是如此。记nums中的最大值为ma，那么一旦对于nums中所有的nums[index]都满足nums[index] \<\= ma且nums[index] \* mul > ma，接下来就会轮流执行操作，换言之，从这里开始将出现长度为n的循环操作。

此时的问题就变成了：

1、如何将nums[index]都变为nums[index] \<\= ma且nums[index] \* mul > ma，应该如何具体执行操作，需要执行操作的次数为多少

2、对于n个一轮循环的操作，如何计算乘积

3、对于循环操作后剩下的操作应该如何执行

首先是将nums[index]变为nums[index] \<\= ma且nums[index] \* mul > ma。

对于nums[index]，在这里实际上就是需要计算其对应的p[index]，满足nums[index] \* (mul^p[index]) \<\= ma且nums[index] \* (mul^p[index] + 1) > ma。可以发现，这里的p一定是log(ma)这个量级的，也就是说直接使用堆模拟这些操作的时间复杂度为O(nlogn \* log(ma))，是完全没有问题的。

于是可以将nums[index]以及其下标都加入到堆中，每一列判断堆顶元素乘以mul是否依然小于等于ma，若小于等于，就执行一次操作，直到操作全部用完，或者堆顶元素乘以ma大于ma为止。

接下来就将进入n个一轮循环。

此时的循环轮数rnd就是当前剩余的k整除n，而后续每个元素都将乘以mul^rnd。这里的rnd可能非常大，因此需要使用快速幂来计算这个乘积。

最后是对于循环操作剩下的操作应该如何执行。

此时剩下的操作次数必然小于n，因此依然可以直接对模拟来完成这些剩余的操作，时间复杂度为O(nlogn)。在模拟完成后，将最终结果乘以第二步中快速幂计算的结果即为最终答案。

最后附上python代码：

3264：

```python
class Solution(object):
    def getFinalState(self, nums, k, multiplier):
        """
        :type nums: List[int]
        :type k: int
        :type multiplier: int
        :rtype: List[int]
        """

        for rnd in range(k):
            p = 0
            for index in range(1, len(nums)):
                if nums[index] < nums[p]:
                    p = index

            nums[p] *= multiplier
        
        return nums
```

3266:

```
class Solution(object):
    def getFinalState(self, nums, k, multiplier):
        """
        :type nums: List[int]
        :type k: int
        :type multiplier: int
        :rtype: List[int]
        """

        if multiplier == 1:
            return nums

        n = len(nums)
        ma = max(nums)
        heap = []
        for index, v in enumerate(nums):
            heapq.heappush(heap, [v, index])
        
        while k > 0 and heap[0][0] * multiplier <= ma:
            v, index = heapq.heappop(heap)
            v *= multiplier
            k -= 1
            heapq.heappush(heap, [v, index])
        
        rnd = k // n
        k %= n

        for _ in range(k):
            v, index = heapq.heappop(heap)
            v *= multiplier
            heapq.heappush(heap, [v, index])
        
        def quickPow(base, p, mod):
            if p == 0:
                return 1
            if p == 1:
                return base % mod
            
            x = quickPow(base, p // 2, mod)
            x *= x
            x %= mod
            if p % 2 == 1:
                x *= base
                x %= mod
            
            return x
        
        mod = 10 ** 9 + 7
        mul = quickPow(multiplier, rnd, mod)
        res = [0] * n
        for v, index in heap:
            res[index] = v * mul % mod
        
        return res
```
