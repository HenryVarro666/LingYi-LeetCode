---
title: "2450. 应用操作后不同二进制字符串的数量"
aliases: ["yiduobo的每日leetcode 2450.应用操作后不同二进制字符串的数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/631989884"
zhihu_id: "631989884"
zhihu_title: "yiduobo的每日leetcode 2450.应用操作后不同二进制字符串的数量"
question_id: "2450"
question: "应用操作后不同二进制字符串的数量"
problem_url: "https://leetcode.cn/problems/number-of-distinct-binary-strings-after-applying-operations/"
created: "2023-05-25T03:16:27+08:00"
updated: "2023-05-25T03:16:27+08:00"
upvotes: 0
comments: 0
---

# 2450. 应用操作后不同二进制字符串的数量

> **[yiduobo的每日leetcode 2450.应用操作后不同二进制字符串的数量](https://zhuanlan.zhihu.com/p/631989884) · 知乎 · 2023-05-25 · 赞同 0**
> 力扣：[2450. 应用操作后不同二进制字符串的数量](https://leetcode.cn/problems/number-of-distinct-binary-strings-after-applying-operations/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2450.应用操作后不同二进制字符串的数量

[力扣](https://leetcode.cn/problems/number-of-distinct-binary-strings-after-applying-operations/)

一个长度为n的字符串中，一共有n - k + 1个长度为k的子串。对于每个子串，都有翻转和不翻转两种可行的操作，另一方面，不可能通过其他子串的翻转来达成某个特定子串的翻转，因此这里就一共有2^(n - k + 1)种可行的方案。

由于n的范围不大，直接一趟遍历计算这个乘方也是可行的，不过更好的处理方法自然是使用快速幂来计算。

最后附上python代码：

```python
class Solution(object):
    def countDistinctStrings(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        mod = 10 ** 9 + 7

        def pow2(x):
            if x == 0:
                return 1
            if x == 1:
                return 2
            
            res = pow2(x / 2)
            res *= res
            res %= mod
            if x % 2 == 1:
                res += res
                if res >= mod:
                    res -= mod
            
            return res
        
        return pow2(len(s) - k + 1)
```
