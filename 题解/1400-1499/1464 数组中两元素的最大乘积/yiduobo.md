---
title: "1464. 数组中两元素的最大乘积"
aliases: ["yiduobo的每日leetcode 1464.数组中两元素的最大乘积"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/413288731"
zhihu_id: "413288731"
zhihu_title: "yiduobo的每日leetcode 1464.数组中两元素的最大乘积"
question_id: "1464"
question: "数组中两元素的最大乘积"
problem_url: "https://leetcode.cn/problems/maximum-product-of-two-elements-in-an-array/"
difficulty: "Easy"
created: "2021-09-23T22:13:18+08:00"
updated: "2021-09-23T22:13:18+08:00"
upvotes: 0
comments: 0
---

# 1464. 数组中两元素的最大乘积

> **[yiduobo的每日leetcode 1464.数组中两元素的最大乘积](https://zhuanlan.zhihu.com/p/413288731) · 知乎 · 2021-09-23 · 赞同 0**
> 力扣：[1464. 数组中两元素的最大乘积](https://leetcode.cn/problems/maximum-product-of-two-elements-in-an-array/) · Easy · 灵茶山艾府：[三种做法：排序 / 维护最大次大 / 枚举右维护左（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1464.数组中两元素的最大乘积

[力扣](https://leetcode-cn.com/problems/maximum-product-of-two-elements-in-an-array/)

比较基础的题目。由于这里的数都是整数，因此只需要找到最大的两个数即可。

最后附上python代码:

```python
class Solution(object):
    def maxProduct(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        m1 = m2 = None
        for num in nums:
            if m1 is None:
                m1 = num
            elif num > m1:
                m2 = m1
                m1 = num
            elif m2 is None or num > m2:
                m2 = num

        return (m1 - 1) * (m2 - 1)
```
