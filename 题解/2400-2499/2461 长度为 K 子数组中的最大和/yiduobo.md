---
title: "2461. 长度为K子数组中的最大和"
aliases: ["yiduobo的每日leetcode 2461.长度为K子数组中的最大和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/586805484"
zhihu_id: "586805484"
zhihu_title: "yiduobo的每日leetcode 2461.长度为K子数组中的最大和"
question_id: "2461"
question: "长度为 K 子数组中的最大和"
problem_url: "https://leetcode.cn/problems/maximum-sum-of-distinct-subarrays-with-length-k/"
difficulty: "Medium"
rating: 1553
created: "2022-11-26T03:57:53+08:00"
updated: "2022-11-26T03:57:53+08:00"
upvotes: 0
comments: 0
---

# 2461. 长度为K子数组中的最大和

> **[yiduobo的每日leetcode 2461.长度为K子数组中的最大和](https://zhuanlan.zhihu.com/p/586805484) · 知乎 · 2022-11-26 · 赞同 0**
> 力扣：[2461. 长度为 K 子数组中的最大和](https://leetcode.cn/problems/maximum-sum-of-distinct-subarrays-with-length-k/) · Medium · 灵茶山艾府：[定长滑动窗口（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2461.长度为K子数组中的最大和

[力扣](https://leetcode.cn/problems/maximum-sum-of-distinct-subarrays-with-length-k/)

非常标准的滑动窗口问题。从头开始向后遍历每个长度为k的窗口，利用哈希表维护当前窗口中每种数字出现的次数以及当前窗口中的数字和。题目要求当每种数字都出现一次时才能使用当前窗口数字和来更新答案，那么在这里可以将这个条件对应到哈希表的长度为k，这样每种数字出现的次数就是恰好一次了，此时就可以使用窗口内的数字和来更新答案。

需要注意的是，当窗口向右移动时，如果原来的左边界对应的数字因为这一次移动不再出现在滑动窗口内，也就是哈希表的计数为0时，需要将这个数对应的key从哈希表中移除，才能保证哈希表的长度正确。

最后附上python代码：

```python
class Solution(object):
    def maximumSubarraySum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        cnt = {}
        s = 0
        for num in nums[:k]:
            cnt[num] = cnt.get(num, 0) + 1
            s += num
        
        if len(cnt) == k:
            res = s
        else:
            res = 0
        
        for index in range(k, len(nums)):
            cnt[nums[index]] = cnt.get(nums[index], 0) + 1
            s += nums[index]

            cnt[nums[index - k]] -= 1
            if cnt[nums[index - k]] == 0:
                cnt.pop(nums[index - k])
            s -= nums[index - k]

            if len(cnt) == k:
                res = max(res, s)
        
        return res
```
