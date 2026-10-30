---
title: "3627. 中位数之和的最大值"
aliases: ["yiduobo的每日leetcode 3627.中位数之和的最大值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1945524544380053220"
zhihu_id: "1945524544380053220"
zhihu_title: "yiduobo的每日leetcode 3627.中位数之和的最大值"
question_id: "3627"
question: "中位数之和的最大值"
problem_url: "https://leetcode.cn/problems/maximum-median-sum-of-subsequences-of-size-3/"
difficulty: "Medium"
rating: 1561
created: "2025-08-31T16:45:07+08:00"
updated: "2025-08-31T16:45:07+08:00"
upvotes: 0
comments: 0
---

# 3627. 中位数之和的最大值

> **[yiduobo的每日leetcode 3627.中位数之和的最大值](https://zhuanlan.zhihu.com/p/1945524544380053220) · 知乎 · 2025-08-31 · 赞同 0**
> 力扣：[3627. 中位数之和的最大值](https://leetcode.cn/problems/maximum-median-sum-of-subsequences-of-size-3/) · Medium · 灵茶山艾府：[贪心，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3627.中位数之和的最大值

<https://leetcode.cn/problems/maximum-median-sum-of-subsequences-of-size-3/description/>

题目给出一个整数数组nums，其长度可以被3整除。现在要求通过多轮操作将数组情况，在每一轮操作中，都可以从数组中选择任意三个元素，计算它们的中位数，并将这三个元素从数组中移除。问所有操作得到的中位数之和的最大值。

首先可以明确的是，最小的那三分之一的元素应该逐个分配到每次操作中，理由是每一组中必须有一个最小值，这三分之一的元素来填每一组的最小值是最合适的。证明也很简单，方便期间，记最小的三分之一的元素集合为mi，如果有一组g的最小值不属于mi，那么必然有至少一组具有两个或三个元素属于mi，也就是说这一组的中位数也必然属于mi，记这一组为h。此时将g的最小值与h的最小值交换，g的中位数不变，而h的中位数将会变得更大，也就是说将两个属于mi的元素分到同一组是不优的。

确定了mi中的元素必须逐个分配到每一组之后，剩下的元素就很容易分配了。剩余元素的最大值必然是无法作为中位数的，但是次大值可以分到与最大值同一组中成为中位数。更进一步的，就应该按从大到小的顺序两个两个分到一组中，这样一来浪费掉的大的值是最少的。

基于以上的结论，只需将nums从大到小排序，然后选择其中下标1、3、5、...的元素，一共选择n // 3次，将这些元素之和累加即为最终答案。

最后附上python代码：

```
class Solution(object):
    def maximumMedianSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        res = 0
        nums.sort(reverse=True)
        index = 1
        for _ in range(len(nums) // 3):
            res += nums[index]
            index += 2
        
        return res
```
