---
title: "3411. 最长乘积等价子数组"
aliases: ["yiduobo的每日leetcode 3411.最长乘积等价子数组"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/number-theory", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/数学算法", "题单/滑动窗口与双指针/二-不定长滑动窗口", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/32084785447"
zhihu_id: "32084785447"
zhihu_title: "yiduobo的每日leetcode 3411.最长乘积等价子数组"
question_id: "3411"
question: "最长乘积等价子数组"
problem_url: "https://leetcode.cn/problems/maximum-subarray-with-equal-products/"
difficulty: "Easy"
rating: 2300
created: "2025-03-22T21:58:26+08:00"
updated: "2025-03-22T21:58:26+08:00"
upvotes: 1
comments: 0
---

# 3411. 最长乘积等价子数组

> **[yiduobo的每日leetcode 3411.最长乘积等价子数组](https://zhuanlan.zhihu.com/p/32084785447) · 知乎 · 2025-03-22 · 赞同 1**
> 力扣：[3411. 最长乘积等价子数组](https://leetcode.cn/problems/maximum-subarray-with-equal-products/) · Easy · 灵茶山艾府：[两种方法：枚举/滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3411.最长乘积等价子数组

[3411. 最长乘积等价子数组 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-subarray-with-equal-products/description/)

题目给出一个长度不超过100的正整数数组nums，另外定义若某个数组arr满足arr中所有元素的乘积，恰好等于这些元素最小公约数与最大公倍数之积，那么就称arr为乘积等价数组。问nums中最长的乘积等价数组的长度。

题目的数据规模较小，因此可以直接暴力枚举所有子数组的起点start以及终点end，然后检测子数组是否为乘积等价数组。值得一提的是，对于子数组nums[start: end + 1]的乘积、最小公约数以及最大公倍数，都可以在上一个子数组，也就是nums[start: end]的基础上进行计算。

最后附上python代码：

```python
class Solution(object):
    def maxLength(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        def calc(gcd, v, lcm):
            x, y = gcd, v
            while y:
                x, y = y, x % y
            nxt_gcd = x

            x, y = lcm, v
            while y:
                x, y = y, x % y
            nxt_lcm = lcm * v // x

            return nxt_gcd, nxt_lcm

        res = 1
        for start in range(len(nums)):
            mul = nums[start]
            gcd = nums[start]
            lcm = nums[start]
            for end in range(start + 1, len(nums)):
                mul *= nums[end]
                gcd, lcm = calc(gcd, nums[end], lcm)
                if gcd * lcm == mul:
                    res = max(res, end - start + 1)
        
        return res
```
