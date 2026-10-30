---
title: "2892. 将相邻元素相乘后得到最小化数组"
aliases: ["yiduobo的每日leetcode 2892.将相邻元素相乘后得到最小化数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/662763883"
zhihu_id: "662763883"
zhihu_title: "yiduobo的每日leetcode 2892.将相邻元素相乘后得到最小化数组"
question_id: "2892"
question: "将相邻元素相乘后得到最小化数组"
problem_url: "https://leetcode.cn/problems/minimizing-array-after-replacing-pairs-with-their-product/"
created: "2023-10-23T01:43:50+08:00"
updated: "2023-10-23T01:43:50+08:00"
upvotes: 0
comments: 0
---

# 2892. 将相邻元素相乘后得到最小化数组

> **[yiduobo的每日leetcode 2892.将相邻元素相乘后得到最小化数组](https://zhuanlan.zhihu.com/p/662763883) · 知乎 · 2023-10-23 · 赞同 0**
> 力扣：[2892. 将相邻元素相乘后得到最小化数组](https://leetcode.cn/problems/minimizing-array-after-replacing-pairs-with-their-product/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2892.将相邻元素相乘后得到最小化数组

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimizing-array-after-replacing-pairs-with-their-product/description/)

题目实际上是要求将数组划分成最少的子数组，要求每个子数组的乘积都不超过k。

首先考虑特殊情况。当数组中存在0时，整个数组的乘积必然为0，满足不超过k，因此无需进行划分，此时的答案就是1。

对于数组中没有0的情况，则可以使用贪心法来求解。使用一个变量now记录当前子数组的乘积，初始情况下初始化now为nums[0]。接下来从下标1开始向后遍历，对于当前遍历到的nums[index]，若其与now相乘的结果不超过k，那么就将其纳入当前子数组，并更新now的值；反之，则需要将当前子数组划分出去，此时应该将答案加上1，并将now更新为nums[index]。这样处理的理由也很简单，因为剩余数组的长度越短，最终可划分的子数组就越少，因此对于nums[index]，应该尽量将其纳入前面的子数组，以使得后续剩余的子数组尽量短。

最后附上python代码：

```python
class Solution(object):
    def minArrayLength(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        res = 1
        if min(nums) == 0:
            return res
        
        now = nums[0]
        for v in nums[1:]:
            if now * v <= k:
                now *= v
            else:
                now = v
                res += 1
        
        return res
```
