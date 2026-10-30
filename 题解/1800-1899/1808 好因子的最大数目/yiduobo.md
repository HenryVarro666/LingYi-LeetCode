---
title: "1808. 好因子的最大数目"
aliases: ["yiduobo的每日leetcode 1808.好因子的最大数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/464715031"
zhihu_id: "464715031"
zhihu_title: "yiduobo的每日leetcode 1808.好因子的最大数目"
question_id: "1808"
question: "好因子的最大数目"
problem_url: "https://leetcode.cn/problems/maximize-number-of-nice-divisors/"
created: "2022-02-07T21:58:49+08:00"
updated: "2022-02-07T21:58:49+08:00"
upvotes: 0
comments: 0
---

# 1808. 好因子的最大数目

> **[yiduobo的每日leetcode 1808.好因子的最大数目](https://zhuanlan.zhihu.com/p/464715031) · 知乎 · 2022-02-07 · 赞同 0**
> 力扣：[1808. 好因子的最大数目](https://leetcode.cn/problems/maximize-number-of-nice-divisors/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1808.好因子的最大数目

[力扣](https://leetcode-cn.com/problems/maximize-number-of-nice-divisors/)

题目描述看上去比较复杂，不过仔细分析可以发现最终问题能转化成一个经典的数学问题。

首先考虑特殊情况。当primeFactors为1时，说明n本身就是一个质数，那么此时答案必然为1。

接下来考虑一般情况。按照题目意思，将最终答案的n分解质因数后可以写成

n \= (p[0]^k[0]) \* (p[1]^k[1]) \* ... \* (p[m]^k[m])

这里的p[i]都是质数，而k[i]都大于等于1

根据题目对于好因子的定义，其必然可以写成下面这种形式

f \= p[0] \* p[1] \* ... \* p[m] \* (p[0]^h[0]) \* (p[1]^h[1]) \* ... \* (p[m]^h[m])

在这里0 \<\= h[i] \<\= k[i] - 1

可以发现，对于h[i]一共有0到k[i] - 1这一共k[i]种合法的选项，因此在这里对于n而言，其好因子的数目就是

k[0] \* k[1] \* ... \* k[m]

另一方面，n所有质因子的总数恰好是

k[0] + k[1] + ... + k[m]

那么到了这里，问题就转化成了将找出一组k，使得其满足k[0] + k[1] + ... + k[m] \<\= primeFactors，且k[0] \* k[1] \* ... \* k[m]最大。这就是经典的拆3问题，即如何拆分一个整数，使得拆分结果的乘积最大，做法就是尽量拆3。当然，这样做可能会遇到剩下1或者剩下2的情况。对于剩下1的情况，应该拿回一个3，然后拆成两个2。对于剩下2的情况则保留这个2。

拆三正确性的具体的证明应该可以使用归纳法来做，在这里就不展开了。

回到题目。既然明确了就是对primeFactors做拆3，那么可以先通过除以3以及模3的余数来得到拆出来3的数目。由于这里的primeFactors规模较大不能直接暴力计算，因此还需要通过快速幂或者逆元来计算最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxNiceDivisors(self, primeFactors):
        """
        :type primeFactors: int
        :rtype: int
        """

        if primeFactors == 1:
            return 1

        mod = 10 ** 9 + 7
        p = primeFactors / 3
        if primeFactors % 3 == 1:
            p -= 1
            base = 4
        elif primeFactors % 3 == 2:
            base = 2
        else:
            base = 1
        
        return self.quickPow(p, mod) * base % mod
    
    def quickPow(self, p, mod):
        if p == 0:
            return 1
        elif p == 1:
            return 3
        
        tmp = self.quickPow(p / 2, mod) ** 2 % mod
        if p % 2 == 1:
            tmp = tmp * 3 % mod
        return tmp
```
