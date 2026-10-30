---
title: "1922. 统计好数字的数目"
aliases: ["yiduobo的每日leetcode 1922.统计好数字的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/combinatorics", "题单/数学算法", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/485031343"
zhihu_id: "485031343"
zhihu_title: "yiduobo的每日leetcode 1922.统计好数字的数目"
question_id: "1922"
question: "统计好数字的数目"
problem_url: "https://leetcode.cn/problems/count-good-numbers/"
difficulty: "Medium"
rating: 1675
created: "2022-03-21T22:48:56+08:00"
updated: "2022-03-21T22:48:56+08:00"
upvotes: 0
comments: 0
---

# 1922. 统计好数字的数目

> **[yiduobo的每日leetcode 1922.统计好数字的数目](https://zhuanlan.zhihu.com/p/485031343) · 知乎 · 2022-03-21 · 赞同 0**
> 力扣：[1922. 统计好数字的数目](https://leetcode.cn/problems/count-good-numbers/) · Medium · 灵茶山艾府：[乘法原理+快速幂（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1922.统计好数字的数目

[力扣](https://leetcode-cn.com/problems/count-good-numbers/)

对于题目中的每个偶数位，都有0、2、4、6、8一共5种可能，而对于奇数位而言，则有2、3、5、7一共4种可能，那么综合起来就是没两位可以提供20种可能性，于是最终一共有20^(n / 2)种可能性。另外，若n位奇数，那么答案还需要再乘以5。

注意到题目的n非常大，因此在这里需要使用快速幂来计算20的幂次。

另外，根据题目的样例来看，并不需要关注前缀0的情况，因此直接按上面方法计算就行了。

最后附上python代码：

```python
class Solution(object):
    def countGoodNumbers(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n == 1:
            return 5

        mod = 10 ** 9 + 7

        res = self.quickPow(20, n / 2, mod)
        if n & 1:
            res = res * 5 % mod
        
        return res
    
    def quickPow(self, base, p, mod):
        if p == 1:
            return base
        
        tmp = self.quickPow(base, p / 2, mod)
        tmp = tmp * tmp % mod
        if p & 1:
            tmp = tmp * base % mod
        
        return tmp
```
