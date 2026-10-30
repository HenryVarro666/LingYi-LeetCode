---
title: "1523. 在区间范围内统计奇数数目"
aliases: ["yiduobo的每日leetcode 1523.在区间范围内统计奇数数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "题单/常用数据结构", "题单/数学算法", "题单/常用数据结构/一-前缀和", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/422022096"
zhihu_id: "422022096"
zhihu_title: "yiduobo的每日leetcode 1523.在区间范围内统计奇数数目"
question_id: "1523"
question: "在区间范围内统计奇数数目"
problem_url: "https://leetcode.cn/problems/count-odd-numbers-in-an-interval-range/"
difficulty: "Easy"
rating: 1209
created: "2021-10-15T23:31:21+08:00"
updated: "2021-10-15T23:31:21+08:00"
upvotes: 0
comments: 0
---

# 1523. 在区间范围内统计奇数数目

> **[yiduobo的每日leetcode 1523.在区间范围内统计奇数数目](https://zhuanlan.zhihu.com/p/422022096) · 知乎 · 2021-10-15 · 赞同 0**
> 力扣：[1523. 在区间范围内统计奇数数目](https://leetcode.cn/problems/count-odd-numbers-in-an-interval-range/) · Easy · 灵茶山艾府：[O(1) 数学解（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1523.在区间范围内统计奇数数目

[力扣](https://leetcode-cn.com/problems/count-odd-numbers-in-an-interval-range/)

直接统计[low, high]中奇数数目的话涉及到low和high边界的判断，稍显复杂，那么也可以利用前缀来进行判断，即[low, high]中奇数的数目等于[1, high]中奇数的数目减去[1, low - 1]中奇数的数目。

而对于区间[1, x]中的奇数，则可以写成1 \* 2 - 1，2 \* 2 - 1，...，k \* 2 - 1的形式，只需要找到最大的k，满足k \* 2 - 1 \<\= x，于是有k \= (x + 1) / 2。这里的除法为整除，k即为区间中奇数的数目。

根据上面的结论，最终答案就是(high + 1) / 2 - low / 2

最后附上python代码：

```python
class Solution(object):
    def countOdds(self, low, high):
        """
        :type low: int
        :type high: int
        :rtype: int
        """

        return (high + 1) / 2 - low / 2
```
