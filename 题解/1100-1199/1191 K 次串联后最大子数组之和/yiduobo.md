---
title: "1191. K次串联后的最大子数组之和"
aliases: ["yiduobo的每日leetcode 1191.K次串联后的最大子数组之和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/一-入门-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/380939112"
zhihu_id: "380939112"
zhihu_title: "yiduobo的每日leetcode 1191.K次串联后的最大子数组之和"
question_id: "1191"
question: "K 次串联后最大子数组之和"
problem_url: "https://leetcode.cn/problems/k-concatenation-maximum-sum/"
difficulty: "Medium"
rating: 1748
created: "2021-06-15T22:09:52+08:00"
updated: "2021-06-15T22:09:52+08:00"
upvotes: 1
comments: 0
---

# 1191. K次串联后的最大子数组之和

> **[yiduobo的每日leetcode 1191.K次串联后的最大子数组之和](https://zhuanlan.zhihu.com/p/380939112) · 知乎 · 2021-06-15 · 赞同 1**
> 力扣：[1191. K 次串联后最大子数组之和](https://leetcode.cn/problems/k-concatenation-maximum-sum/) · Medium · 灵茶山艾府：[复用 53 题代码，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1191.K次串联之和的最大子数组之和

[力扣](https://leetcode-cn.com/problems/k-concatenation-maximum-sum/)

题目要求K次串联之和的最大子段和，那么可以分成两种情况进行讨论：

1、最终答案没有跨越多个原始数组：

此时直接在原始数组中执行一次求最大子段和即可

2、最终答案跨越了多个原始数组：

答案的起点显然是第0个原始数组，设终点为第p个原始数组，那么最终答案必然是

sum(arr_0[s:]) + sum(arr_1) + sum(arr_2) + ... + sum(arr_p[:e])

这种形式，即第0个原始数组的某个后缀加上第1到第p - 1个原始数组的全体加上第p个原始数组的前缀。那么有一点可以明确的是，当arr所有元素之和大于0时，才有必要保留第1到第p - 1个原始数组，否则直接取sum(arr_0[s:]) + sum(arr_1[:e])显然是更优的。于是现在又可以分成两种情况讨论：

2-1）当sum(arr) > 0时，p必然等于k，那么此时的答案就是arr的最大后缀加上k - 2个arr全体元素之后再加上arr的最大前缀

2-2）当sum(arr) \<\= 0 时，p等于1，那么此时的答案就是arr的最大后缀加上arr的最大前缀

根据sum(arr)的情况求出情况2下的最大子段和之后，再与情况1的最大子段和取最大值即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def kConcatenationMaxSum(self, arr, k):
        """
        :type arr: List[int]
        :type k: int
        :rtype: int
        """

        mod = 10 ** 9 + 7

        now = 0
        head_max = 0
        for num in arr:
            now += num
            head_max = max(head_max, now)
        
        now = 0
        tail_max = 0
        for index in range(len(arr) - 1, -1, -1):
            now += arr[index]
            tail_max = max(tail_max, now)
        
        now = 0
        res = 0
        s = 0
        for num in arr:
            s += num
            now += num
            if now < 0:
                now = 0
            res = max(res, now)
        
        if k >= 2:
            if s > 0:
                res = max(res, s * (k - 2) + head_max + tail_max) % mod
            else:
                res = max(res, head_max + tail_max) % mod
        
        return res
```
