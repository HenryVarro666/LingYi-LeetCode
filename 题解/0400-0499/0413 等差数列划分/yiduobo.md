---
title: "413. 等差数列划分"
aliases: ["yiduobo的每日leetcode 413.等差数列划分"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/188733012"
zhihu_id: "188733012"
zhihu_title: "yiduobo的每日leetcode 413.等差数列划分"
question_id: "413"
question: "等差数列划分"
problem_url: "https://leetcode.cn/problems/arithmetic-slices/"
created: "2020-08-18T21:35:17+08:00"
updated: "2020-08-18T21:35:17+08:00"
upvotes: 0
comments: 0
---

# 413. 等差数列划分

> **[yiduobo的每日leetcode 413.等差数列划分](https://zhuanlan.zhihu.com/p/188733012) · 知乎 · 2020-08-18 · 赞同 0**
> 力扣：[413. 等差数列划分](https://leetcode.cn/problems/arithmetic-slices/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

413.等差数列划分<https://leetcode-cn.com/problems/arithmetic-slices/>

对于一个长度为k的等差数列：

1\~3，2\~4，3\~5，...，k - 2 \~ k项拎出来也必然是等差数列，那么就有k - 2种长度为3的等差数列

1\~4，2\~5，3\~6，...，k - 3 \~ k项拎出来也必然是等差数列，那么就有k - 3种长度为4的等差数列

更一般的，1\~m，2\~m + 1，3\~m + 2，...，k - m + 1 \~ k项拎出来必然是长度为m的等差数列，一共有k - m + 1种可能。

那么对于一个长度为k的等差数列，算上其所有子数列的话就一共会存在

(k - 2) + (k - 3) + (k - 4) + ... + 2 + 1种可能的等差数列，即(1 + k - 2) \* (k - 2) / 2

于是我们可以从头到尾一趟扫描，每次都尽可能长地找等差数列，然后使用上面的求和公式就能一次性求出当前等差数列中的这些数可能形成的等差数列的总数。

最后附上python代码：

```python
class Solution(object):
    def numberOfArithmeticSlices(self, A):
        """
        :type A: List[int]
        :rtype: int
        """

        if len(A) < 3:
            return 0

        res = 0
        start = 0
        end = 2
        while end < len(A):
            diff = A[end - 1] - A[end - 2]
            while end < len(A) and A[end] - A[end - 1] == diff:
                end += 1
            
            length = end - start
            res += (1 + length - 2) * (length - 2) / 2
            start = end - 1
            end = end + 1

        return res
```
