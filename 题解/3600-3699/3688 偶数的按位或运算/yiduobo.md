---
title: "3688. 偶数的按位或运算"
aliases: ["yiduobo的每日leetcode 3688.偶数的按位或运算"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li", "题单/位运算", "题单/位运算/四-拆位-/-贡献法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1955344291510617554"
zhihu_id: "1955344291510617554"
zhihu_title: "yiduobo的每日leetcode 3688.偶数的按位或运算"
question_id: "3688"
question: "偶数的按位或运算"
problem_url: "https://leetcode.cn/problems/bitwise-or-of-even-numbers-in-an-array/"
difficulty: "Easy"
created: "2025-09-28T21:34:37+08:00"
updated: "2025-09-28T21:34:39+08:00"
upvotes: 2
comments: 0
---

# 3688. 偶数的按位或运算

> **[yiduobo的每日leetcode 3688.偶数的按位或运算](https://zhuanlan.zhihu.com/p/1955344291510617554) · 知乎 · 2025-09-28 · 赞同 2**
> 力扣：[3688. 偶数的按位或运算](https://leetcode.cn/problems/bitwise-or-of-even-numbers-in-an-array/) · Easy · 灵茶山艾府：[遍历，附思考题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3688.偶数的按位或运算

[3688. 偶数的按位或运算 - 力扣（LeetCode）](https://leetcode.cn/problems/bitwise-or-of-even-numbers-in-an-array/)

题目给出一个整数数组nums，要求返回其中所有偶数的按位或运算结果，若不存在偶数，则返回0。

一趟遍历，按题目要求计算偶数的按位或结果即可。注意不要忘了特别处理第一个偶数以及没有偶数的情况。

最后附上python代码：

```python
class Solution(object):
    def evenNumberBitwiseORs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        res = None
        for v in nums:
            if v % 2 == 0:
                if res is None:
                    res = v
                else:
                    res |= v
        
        if res is None:
            res = 0
        return res
```
