---
title: "3026. 最大好子数组和"
aliases: ["yiduobo的每日leetcode 3026.最大好子数组和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/695127282"
zhihu_id: "695127282"
zhihu_title: "yiduobo的每日leetcode 3026.最大好子数组和"
question_id: "3026"
question: "最大好子数组和"
problem_url: "https://leetcode.cn/problems/maximum-good-subarray-sum/"
difficulty: "Medium"
rating: 1817
created: "2024-04-29T02:40:10+08:00"
updated: "2024-04-29T02:40:11+08:00"
upvotes: 1
comments: 0
---

# 3026. 最大好子数组和

> **[yiduobo的每日leetcode 3026.最大好子数组和](https://zhuanlan.zhihu.com/p/695127282) · 知乎 · 2024-04-29 · 赞同 1**
> 力扣：[3026. 最大好子数组和](https://leetcode.cn/problems/maximum-good-subarray-sum/) · Medium · 灵茶山艾府：[前缀和与哈希表（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3026.最大好子数组和

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-good-subarray-sum/description/)

题目要求在数组中找出一组下标(i, j)，满足nums[i]和nums[j]之差的绝对值为k，且i到j这一段的子数组和最大。

对于区间和，第一选择还是尝试转化成前缀和问题进行求解。也就是说，问题变成了给出一个nums[j]，要求找出满足nums[i]与nums[j]之差的绝对值为k，且nums[0] + nums[1] + ... + nums[i - 1]之和最小的下标i。

那么在这里就可以使用一个哈希表best_prefix来储存各种nums[i]对应的最优前缀和。其中best_prefix[v]储存的是对于所有等于v的nums[i]，其上一轮的前缀和，也就是nums[0] + nums[1] + ... + nums[i - 1]的最小值。

接下来只需一趟遍历，先使用上一轮的前缀和s和当前遍历到的数值v更新best_prefix，再将v累加到s中更新前缀和s，最后通过s - best_prefix[v - k]以及s - best_prefix[v + k]来更新答案。

最后附上python代码：

```python
class Solution(object):
    def maximumSubarraySum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        best_prefix = {}
        s = 0
        res = None
        for v in nums:
            if v not in best_prefix or best_prefix[v] > s:
                best_prefix[v] = s
            
            s += v
            if v - k in best_prefix and (res is None or res < s - best_prefix[v - k]):
                res = s - best_prefix[v - k]
            
            if v + k in best_prefix and (res is None or res < s - best_prefix[v + k]):
                res = s - best_prefix[v + k]
        
        if res is None:
            res = 0
        return res
```
