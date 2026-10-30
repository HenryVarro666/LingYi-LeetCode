---
title: "3622. 判断整除性"
aliases: ["yiduobo的每日leetcode 3622.判断整除性"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1944893226302563753"
zhihu_id: "1944893226302563753"
zhihu_title: "yiduobo的每日leetcode 3622.判断整除性"
question_id: "3622"
question: "判断整除性"
problem_url: "https://leetcode.cn/problems/check-divisibility-by-digit-sum-and-product/"
difficulty: "Easy"
created: "2025-08-29T22:48:28+08:00"
updated: "2025-08-29T22:48:28+08:00"
upvotes: 3
comments: 0
---

# 3622. 判断整除性

> **[yiduobo的每日leetcode 3622.判断整除性](https://zhuanlan.zhihu.com/p/1944893226302563753) · 知乎 · 2025-08-29 · 赞同 3**
> 力扣：[3622. 判断整除性](https://leetcode.cn/problems/check-divisibility-by-digit-sum-and-product/) · Easy · 灵茶山艾府：[遍历数位，不用字符串（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3622.判断整除性

[3622. 判断整除性 - 力扣（LeetCode）](https://leetcode.cn/problems/check-divisibility-by-digit-sum-and-product/description/)

题目给出一个正整数n，请判断n是否可以被n的数字和与n的数字积整除。数字和与数字积分别指的是n每个数位上的数字之和以及数字之积。

通过模10除10的方法分离出n的每一位，在这个过程中顺便计算数字和s以及数字积m，计算完成后判断n是否为s与m之和的倍数即可。

最后附上python代码：

```python
class Solution(object):
    def checkDivisibility(self, n):
        """
        :type n: int
        :rtype: bool
        """
        
        s = 0
        m = 1
        x = n
        while x:
            d = x % 10
            s += d
            m *= d
            x //= 10
        
        return n % (s + m) == 0
```
