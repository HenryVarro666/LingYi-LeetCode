---
title: "2656. K个元素的最大和"
aliases: ["yiduobo的每日leetcode 2656.K个元素的最大和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/brainteaser"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/647883956"
zhihu_id: "647883956"
zhihu_title: "yiduobo的每日leetcode 2656.K个元素的最大和"
question_id: "2656"
question: "K 个元素的最大和"
problem_url: "https://leetcode.cn/problems/maximum-sum-with-exactly-k-elements/"
difficulty: "Easy"
created: "2023-08-04T04:15:32+08:00"
updated: "2023-08-04T04:15:32+08:00"
upvotes: 1
comments: 0
---

# 2656. K个元素的最大和

> **[yiduobo的每日leetcode 2656.K个元素的最大和](https://zhuanlan.zhihu.com/p/647883956) · 知乎 · 2023-08-04 · 赞同 1**
> 力扣：[2656. K 个元素的最大和](https://leetcode.cn/problems/maximum-sum-with-exactly-k-elements/) · Easy · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2656.K个元素的最大和

[力扣](https://leetcode.cn/problems/maximum-sum-with-exactly-k-elements/)

题目中的每次操作都会使得被操作的元素变得更大，那么为了使得和最大，就应该不断操作数组中最大的元素。不妨设数组中最大的元素为ma，那么经过k轮操作，操作的数就分别是ma、ma + 1、ma + 2、...、ma + k - 1，那么求和后答案就是ma \* k + (1 + 2 + ... + k - 1) \= ma \* k + (k - 1) \* k / 2

最后附上python代码：

```python
class Solution(object):
    def maximizeSum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        return max(nums) * k + (k - 1) * k / 2
```
