---
title: "1969. 数组元素的最小非零乘积"
aliases: ["yiduobo的每日leetcode 1969.数组元素的最小非零乘积"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/math", "leetcode/kuai-su-mi", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/495435651"
zhihu_id: "495435651"
zhihu_title: "yiduobo的每日leetcode 1969.数组元素的最小非零乘积"
question_id: "1969"
question: "数组元素的最小非零乘积"
problem_url: "https://leetcode.cn/problems/minimum-non-zero-product-of-the-array-elements/"
difficulty: "Medium"
rating: 1967
created: "2022-04-08T23:35:50+08:00"
updated: "2022-04-08T23:35:50+08:00"
upvotes: 0
comments: 0
---

# 1969. 数组元素的最小非零乘积

> **[yiduobo的每日leetcode 1969.数组元素的最小非零乘积](https://zhuanlan.zhihu.com/p/495435651) · 知乎 · 2022-04-08 · 赞同 0**
> 力扣：[1969. 数组元素的最小非零乘积](https://leetcode.cn/problems/minimum-non-zero-product-of-the-array-elements/) · Medium · 灵茶山艾府：[贪心+构造（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1969.数组元素的最小非零乘积

[力扣](https://leetcode-cn.com/problems/minimum-non-zero-product-of-the-array-elements/)

首先，这里一共2^p - 1个数，按位来看，每一位上有2^(p - 1)个1以及2^(p - 1) - 1个0。

对于最后构造的答案中的两个数x和y，若其中只有一个数的第k位为0，那么可以认为是决定这个2^k应该归x还是归y。不妨设x > y，那么二者的乘积对于2^k的归属，可以写成(x + 2^k) \* y以及x \* (y + 2^k)，显然前者要小于后者。这也说明了，最终的构造就是要让一部分数尽可能小，那么最终的构造结果就是

2^(p - 1) - 1个00...0001

2^(p - 1) - 1个11...1110

以及一个11...1111

那么最终的乘积就是(2^p - 2)^(2^(p - 1) - 1) \* (2^p - 1)

式子中有三个部分。

第一个是底数2^p - 2，可以直接通过快速幂求解，记结果为x。

第二个是指数2^(p - 1) - 1。在这里由于mod为10^9 + 7，是一个质数，因此在可以通过费马小定理求解。即通过x^(mod - 1) % mod \= 1，可以先将2^(p - 1) - 1先对(mod - 1)取模得到e，那么就有x^(2^(p - 1) - 1) \= x^e。对于e而言，也是通过快速幂求解，而接下来的x^e，也是通过快速幂求解。

第三个是最后这个乘数2^p - 1，就是第一部分的结果x + 1。

综合起来，只需要执行三次快速幂即可。

最后附上python代码：

```python
class Solution(object):
    def minNonZeroProduct(self, p):
        """
        :type p: int
        :rtype: int
        """

        mod = 10 ** 9 + 7
        x = self.quickPow(2, p, mod)
        res1 = x - 1
        if res1 < 0:
            res1 += mod
        
        e = self.quickPow(2, p - 1, mod - 1)
        e -= 1
        if e < 0:
            e += mod - 1
        
        x -= 2
        if x < 0:
            x += mod
        res2 = self.quickPow(x, e, mod)

        return res1 * res2 % mod
    
    def quickPow(self, base, p, mod):
        if p == 0:
            return 1
        elif p == 1:
            return base
        
        res = self.quickPow(base, p / 2, mod)
        res = res * res % mod
        if p % 2 == 1:
            res = res * base % mod
        
        return res
```
