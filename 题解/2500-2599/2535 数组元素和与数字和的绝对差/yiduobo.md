---
title: "2535. 数组元素和与数字和的绝对差"
aliases: ["yiduobo的每日leetcode 2535.数组元素和与数字和的绝对差"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/637303796"
zhihu_id: "637303796"
zhihu_title: "yiduobo的每日leetcode 2535.数组元素和与数字和的绝对差"
question_id: "2535"
question: "数组元素和与数字和的绝对差"
problem_url: "https://leetcode.cn/problems/difference-between-element-sum-and-digit-sum-of-an-array/"
difficulty: "Easy"
created: "2023-06-16T20:12:00+08:00"
updated: "2023-06-16T20:12:00+08:00"
upvotes: 0
comments: 0
---

# 2535. 数组元素和与数字和的绝对差

> **[yiduobo的每日leetcode 2535.数组元素和与数字和的绝对差](https://zhuanlan.zhihu.com/p/637303796) · 知乎 · 2023-06-16 · 赞同 0**
> 力扣：[2535. 数组元素和与数字和的绝对差](https://leetcode.cn/problems/difference-between-element-sum-and-digit-sum-of-an-array/) · Easy · 灵茶山艾府：[利用性质简化代码（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2535.数组元素和与数字和的绝对差

[力扣](https://leetcode.cn/problems/difference-between-element-sum-and-digit-sum-of-an-array/)

比较基础的题目，逐位分离数字，计算元素和，然后计算元素和与原数的绝对值之差即可。

最后附上python代码：

```python
class Solution(object):
    def differenceOfSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        s = sum(nums)
        t = 0
        for x in nums:
            while x:
                t += x % 10
                x /= 10
        
        return abs(s - t)
```
