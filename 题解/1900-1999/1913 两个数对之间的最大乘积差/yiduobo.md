---
title: "1913. 两个数对之间的最大乘积差"
aliases: ["yiduobo的每日leetcode 1913.两个数对之间的最大乘积差"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/483487091"
zhihu_id: "483487091"
zhihu_title: "yiduobo的每日leetcode 1913.两个数对之间的最大乘积差"
question_id: "1913"
question: "两个数对之间的最大乘积差"
problem_url: "https://leetcode.cn/problems/maximum-product-difference-between-two-pairs/"
difficulty: "Easy"
created: "2022-03-19T00:12:42+08:00"
updated: "2022-03-19T00:12:42+08:00"
upvotes: 1
comments: 0
---

# 1913. 两个数对之间的最大乘积差

> **[yiduobo的每日leetcode 1913.两个数对之间的最大乘积差](https://zhuanlan.zhihu.com/p/483487091) · 知乎 · 2022-03-19 · 赞同 1**
> 力扣：[1913. 两个数对之间的最大乘积差](https://leetcode.cn/problems/maximum-product-difference-between-two-pairs/) · Easy · 灵茶山艾府：[贪心，取最大两个与最小两个相减](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1913.两个数对之间的最大乘积差

<https://leetcode-cn.com/problems/maximum-product-difference-between-two-pairs/>

由于题目给出的数都是正数，那么最大的乘积显然是数组中最大的两个数相乘得到的，而最小的乘积则是数组中最小的两个数相乘得到。于是可以一趟扫描，找到这四个数，然后用最大乘积减去最小乘积即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxProductDifference(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        ma1 = ma2 = 0
        mi1 = mi2 = 10001
        for num in nums:
            if num > ma1:
                ma1, ma2 = num, ma1
            elif num > ma2:
                ma2 = num

            if num < mi1:
                mi1, mi2 = num, mi1
            elif num < mi2:
                mi2 = num
        
        return ma1 * ma2 - mi1 * mi2
```
