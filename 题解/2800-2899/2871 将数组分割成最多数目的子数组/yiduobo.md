---
title: "2871. 将数组分割成最多数目的子数组"
aliases: ["yiduobo的每日leetcode 2871.将数组分割成最多数目的子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bit-manipulation", "题单/位运算", "题单/位运算/三-与或-AND/OR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/662531676"
zhihu_id: "662531676"
zhihu_title: "yiduobo的每日leetcode 2871.将数组分割成最多数目的子数组"
question_id: "2871"
question: "将数组分割成最多数目的子数组"
problem_url: "https://leetcode.cn/problems/split-array-into-maximum-number-of-subarrays/"
difficulty: "Medium"
rating: 1750
created: "2023-10-21T04:30:55+08:00"
updated: "2023-10-21T04:30:55+08:00"
upvotes: 0
comments: 0
---

# 2871. 将数组分割成最多数目的子数组

> **[yiduobo的每日leetcode 2871.将数组分割成最多数目的子数组](https://zhuanlan.zhihu.com/p/662531676) · 知乎 · 2023-10-21 · 赞同 0**
> 力扣：[2871. 将数组分割成最多数目的子数组](https://leetcode.cn/problems/split-array-into-maximum-number-of-subarrays/) · Medium · 灵茶山艾府：[利用 AND 性质+一次遍历（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2871.将数组分割成最多数目的子数组

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/split-array-into-maximum-number-of-subarrays/)

题目既要求分割后所有的子数组分数之和最小，有要求在这个前提下让子数组数量尽量多，这本来就是一件矛盾的事情。当子数组的分数为正数时，分得越多分数和就越大，这也就意味着只有当分数为0时才需要尽量多分，而分数大于0时不进行任何划分才能让分数之和最小。

接下来的问题就是如何确定这个最小分数。由于按位与是一种越算越小的运算，即参与运算的数字越多，结果反而会越来越小，于是在这里数组分数的最小值就可以通过计算数组中所有元素的按位与结果得到。若这个结果不为0，那么答案就是1，否则就需要想办法将数组划分为尽量多的分数为0的子数组。

由于每个数字都要用进去，那么就可以从头开始向后遍历，计算当前子数组的分数。若某一时刻子数组的分数为0，那么就将其划分出去。这样做不但保证了划分出去的子数组分数为0，同时为后续剩余数组留下了尽可能多的元素，方便后续的划分。这样操作下来可能会得到若干段分数为0的子数组，以及最后这一段分数和不为0的子数组，此时只需将最后这一段分数和不为0的子数组合并到最后这一段分数和为0的子数组中即可。可以发现，此时划分得到的子数组数目就是遍历过程中当前子数组分数等于0的次数。

最后附上python代码：

```python
class Solution(object):
    def maxSubarrays(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        now = None
        for v in nums:
            if now is None:
                now = v
            else:
                now &= v
            
            if now == 0:
                res += 1
                now = None
        
        if res == 0:
            res = 1
        
        return res
```
