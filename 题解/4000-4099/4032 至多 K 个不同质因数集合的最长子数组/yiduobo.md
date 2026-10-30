---
title: "4032. 至多K个不同质因数集合的最长子数组"
aliases: ["yiduobo的每日leetcode 4032.至多K个不同质因数集合的最长子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/math", "leetcode/number-theory", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/数学算法", "题单/滑动窗口与双指针/二-不定长滑动窗口", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2077902850705864366"
zhihu_id: "2077902850705864366"
zhihu_title: "yiduobo的每日leetcode 4032.至多K个不同质因数集合的最长子数组"
question_id: "4032"
question: "至多 K 个不同质因数集合的最长子数组"
problem_url: "https://leetcode.cn/problems/longest-subarray-with-at-most-k-distinct-prime-factors/"
difficulty: "Medium"
rating: 1759
created: "2026-08-31T23:49:27+08:00"
updated: "2026-08-31T23:49:27+08:00"
upvotes: 2
comments: 0
---

# 4032. 至多K个不同质因数集合的最长子数组

> **[yiduobo的每日leetcode 4032.至多K个不同质因数集合的最长子数组](https://zhuanlan.zhihu.com/p/2077902850705864366) · 知乎 · 2026-08-31 · 赞同 2**
> 力扣：[4032. 至多 K 个不同质因数集合的最长子数组](https://leetcode.cn/problems/longest-subarray-with-at-most-k-distinct-prime-factors/) · Medium · 灵茶山艾府：[预处理 + 滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4032.至多K个不同质因数集合的最长子数组

<https://leetcode.cn/problems/longest-subarray-with-at-most-k-distinct-prime-factors/description/>

题目给出一个由正整数组成的整数数组nums和一个整数k。nums的长度以及其中元素的大小都不超过10^5。

一个子数组的质因数集合，指的是其所有元素的不同质因数的并集。

要求找出一个尽可能长的子数组，其质因数集合中包含的不同质因子数量不超过k。问这个子数组最长是多少。

首先可以明确的是，对于左边界固定的子数组，其右边界越靠后，其质因数集中可能包含的不同质因子的数目就越多，因此在这里非常适合使用滑动窗口来进行求解。

另一方面，由于数组中的元素不超过10^5，那么其可能拥有的质因数数量就不会超过6个，理由是最小的6个质数相乘2 \* 3 \* 5 \* 7 \* 11 \* 13 \= 30030，再乘以下一个质数就超过10^5了。基于这一点，只需在最开始利用筛法预处理2到max(nums)中每个元素的质因子集，那么接下来就可以在O(1)的时间内更新子数组的质因数集合中不同质因子的数量。

具体来说，就是使用一个哈希表记录窗口中每种质因子出现的次数，那么这个哈希表的长度就是窗口中不同质因子的数量。接下来对于每个左边界，先在之前的基础上尝试扩展窗口的右边界。随着窗口的右边界向右移动，可以使用新加入窗口的那个元素的质因子集合更新哈希表，当然这个前提是哈希表的长度必须不超过k。重复此过程直到无法再继续扩展为止，接下来先更新答案，然后将窗口左边界的元素的质因子从哈希表中减去，再继续考虑下一个窗口左边界即可。

最后附上python代码：

```python
class Solution(object):
    def longestSubarray(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        ma = max(nums)
        f = [[] for _ in range(ma + 1)]

        v = 2
        while v <= ma:
            if not f[v]:
                for x in range(v, ma + 1, v):
                    f[x].append(v)
        
            v += 1
        
        cnt = {}
        p = 0
        res = 0
        for index in range(len(nums)):
            if p < index:
                p = index
                cnt = {}

            while p < len(nums):
                for x in f[nums[p]]:
                    cnt[x] = cnt.get(x, 0) + 1
                if len(cnt) > k:
                    for x in f[nums[p]]:
                        cnt[x] -= 1
                        if cnt[x] == 0:
                            cnt.pop(x)
                    break

                p += 1

            res = max(res, p - index)
            if p > index:
                for x in f[nums[index]]:
                    cnt[x] -= 1
                    if cnt[x] == 0:
                        cnt.pop(x)

        return res
```
