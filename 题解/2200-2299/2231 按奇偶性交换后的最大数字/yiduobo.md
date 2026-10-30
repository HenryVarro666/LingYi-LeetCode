---
title: "2231. 按奇偶性交换后的最大数字"
aliases: ["yiduobo的每日leetcode 2231.按奇偶性交换后的最大数字"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/543737088"
zhihu_id: "543737088"
zhihu_title: "yiduobo的每日leetcode 2231.按奇偶性交换后的最大数字"
question_id: "2231"
question: "按奇偶性交换后的最大数字"
problem_url: "https://leetcode.cn/problems/largest-number-after-digit-swaps-by-parity/"
difficulty: "Easy"
created: "2022-07-19T23:59:36+08:00"
updated: "2022-07-19T23:59:36+08:00"
upvotes: 0
comments: 0
---

# 2231. 按奇偶性交换后的最大数字

> **[yiduobo的每日leetcode 2231.按奇偶性交换后的最大数字](https://zhuanlan.zhihu.com/p/543737088) · 知乎 · 2022-07-19 · 赞同 0**
> 力扣：[2231. 按奇偶性交换后的最大数字](https://leetcode.cn/problems/largest-number-after-digit-swaps-by-parity/) · Easy · 灵茶山艾府：[三部曲：分组 - 排序 - 填回](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2231.按奇偶性交换后的最大数字

[力扣](https://leetcode.cn/problems/largest-number-after-digit-swaps-by-parity/)

为了使得结果最大，那么就应该让较大的数字放在高位上，于是可以先将每一位数字按奇偶性分到两个数组中，同时使用两个数组分别记录下奇数数字和偶数数字的原始位置。接下来将奇偶两个数组排序，然后按顺序填充到原始位置数组对应的位置上即可。

最后附上python代码：

```python
class Solution(object):
    def largestInteger(self, num):
        """
        :type num: int
        :rtype: int
        """

        digits = [[], []]
        pos = [[], []]

        l = 0
        while num:
            now = num % 10
            num /= 10
            digits[now % 2].append(now)
            pos[now % 2].append(l)
            l += 1
        
        digits[0].sort()
        digits[1].sort()

        res = [0] * l
        for index in range(len(digits[0])):
            res[pos[0][index]] = digits[0][index]
        for index in range(len(digits[1])):
            res[pos[1][index]] = digits[1][index]

        res.reverse()

        return int(''.join([str(x) for x in res]))
```
