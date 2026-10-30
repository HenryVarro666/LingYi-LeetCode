---
title: "3982. 最大数字范围的整数之和"
aliases: ["yiduobo的每日leetcode 3982.最大数字范围的整数之和"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2057220950203045885"
zhihu_id: "2057220950203045885"
zhihu_title: "yiduobo的每日leetcode 3982.最大数字范围的整数之和"
question_id: "3982"
question: "最大数字范围的整数之和"
problem_url: "https://leetcode.cn/problems/sum-of-integers-with-maximum-digit-range/"
difficulty: "Easy"
created: "2026-07-07T21:14:21+08:00"
updated: "2026-07-07T21:14:21+08:00"
upvotes: 0
comments: 0
---

# 3982. 最大数字范围的整数之和

> **[yiduobo的每日leetcode 3982.最大数字范围的整数之和](https://zhuanlan.zhihu.com/p/2057220950203045885) · 知乎 · 2026-07-07 · 赞同 0**
> 力扣：[3982. 最大数字范围的整数之和](https://leetcode.cn/problems/sum-of-integers-with-maximum-digit-range/) · Easy · 灵茶山艾府：[一次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3982.最大数字范围的整数之和

<https://leetcode.cn/problems/sum-of-integers-with-maximum-digit-range/>

题目给出一个整数数组nums。

一个整数的数字范围，定义为其最大数字与最小数字之间的差。

要求返回nums中所有数字范围等于数组中最大数字范围的整数之和。

直接按照题目要求模拟计算即可。一趟遍历，通过模10除以10的方法得到每一位数字，记录其中的最大值和最小值。分离完成后，计算其对应的数字范围，然后对比当前的最大数字范围并更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxDigitRange(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        ma_diff = 0
        res = 0
        for v in nums:
            ma = 0
            mi = 9
            x = v
            while x:
                d = x % 10
                ma = max(ma, d)
                mi = min(mi, d)
                x //= 10

            diff = ma - mi
            if diff > ma_diff:
                ma_diff = diff
                res = 0
            if diff == ma_diff:
                res += v
        
        return res
```
