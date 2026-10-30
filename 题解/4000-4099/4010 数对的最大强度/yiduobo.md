---
title: "4010. 数对的最大强度"
aliases: ["yiduobo的每日leetcode 4010.数对的最大强度"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/enumeration", "leetcode/number-theory", "leetcode/sorting", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2068823507308483307"
zhihu_id: "2068823507308483307"
zhihu_title: "yiduobo的每日leetcode 4010.数对的最大强度"
question_id: "4010"
question: "数对的最大强度"
problem_url: "https://leetcode.cn/problems/maximize-pair-strength-using-gcd/"
difficulty: "Easy"
rating: 1216
created: "2026-08-06T22:21:44+08:00"
updated: "2026-08-06T22:21:45+08:00"
upvotes: 1
comments: 0
---

# 4010. 数对的最大强度

> **[yiduobo的每日leetcode 4010.数对的最大强度](https://zhuanlan.zhihu.com/p/2068823507308483307) · 知乎 · 2026-08-06 · 赞同 1**
> 力扣：[4010. 数对的最大强度](https://leetcode.cn/problems/maximize-pair-strength-using-gcd/) · Easy · 灵茶山艾府：[枚举 + 最优性优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4010.数对的最大强度

<https://leetcode.cn/problems/maximize-pair-strength-using-gcd/description/>

题目给出一个整数数组nums，现在要求从中选出恰好一对不同下标i和j，其强度定义为(nums[i] \* nums[j]) / gcd(nums[i], nums[j])^2。

要求找出所有可能数对中的最大强度。

按照题目描述两两遍历所有下标对，并计算对应的强度即可。

最后附上python代码：

```python
class Solution(object):
    def maxPairStrength(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        res = 0
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                x, y = nums[i], nums[j]
                while y > 0:
                    x, y = y, x % y
                
                res = max(res, nums[i] * nums[j] // x // x)
        
        return res
```
