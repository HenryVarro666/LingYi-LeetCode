---
title: "2815. 数组中的最大数对和"
aliases: ["yiduobo的每日leetcode 2815.数组中的最大数对和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/bian-li", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/658388958"
zhihu_id: "658388958"
zhihu_title: "yiduobo的每日leetcode 2815.数组中的最大数对和"
question_id: "2815"
question: "数组中的最大数对和"
problem_url: "https://leetcode.cn/problems/max-pair-sum-in-an-array/"
difficulty: "Easy"
created: "2023-09-25T23:51:41+08:00"
updated: "2023-09-25T23:51:41+08:00"
upvotes: 0
comments: 1
---

# 2815. 数组中的最大数对和

> **[yiduobo的每日leetcode 2815.数组中的最大数对和](https://zhuanlan.zhihu.com/p/658388958) · 知乎 · 2023-09-25 · 赞同 0**
> 力扣：[2815. 数组中的最大数对和](https://leetcode.cn/problems/max-pair-sum-in-an-array/) · Easy · 灵茶山艾府：[一次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2815.数组中的最大数对和

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/max-pair-sum-in-an-array/)

题目的数据规模较小，可以直接二重循环枚举所有数对，使用符合题目要求的数对之和来更新答案。我的做法是一趟遍历，利用哈希表储存每种最大数位对应的最大值以及次大值，然后再从中选出和最大的那一组就行了。

最后附上python代码：

```python
class Solution(object):
    def maxSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        ma = [[None] * 2 for _ in range(10)]
        for v in nums:
            max_digit = int(max(list(str(v))))
            if ma[max_digit][0] is None or ma[max_digit][0] < v:
                ma[max_digit] = [v, ma[max_digit][0]]
            elif ma[max_digit][1] is None or ma[max_digit][1] < v:
                ma[max_digit][1] = v
        
        res = -1
        for digit in range(1, 10):
            if ma[digit][1] is not None:
                res = max(res, ma[digit][0] + ma[digit][1])

        return res
```
