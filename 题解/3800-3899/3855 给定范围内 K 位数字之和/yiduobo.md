---
title: "3855. 给定范围内K位数字之和"
aliases: ["yiduobo的每日leetcode 3855.给定范围内K位数字之和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/combinatorics", "leetcode/number-theory", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2011515184158623326"
zhihu_id: "2011515184158623326"
zhihu_title: "yiduobo的每日leetcode 3855.给定范围内K位数字之和"
question_id: "3855"
question: "给定范围内 K 位数字之和"
problem_url: "https://leetcode.cn/problems/sum-of-k-digit-numbers-in-a-range/"
difficulty: "Hard"
rating: 2085
created: "2026-03-06T23:02:05+08:00"
updated: "2026-03-06T23:02:05+08:00"
upvotes: 0
comments: 0
---

# 3855. 给定范围内K位数字之和

> **[yiduobo的每日leetcode 3855.给定范围内K位数字之和](https://zhuanlan.zhihu.com/p/2011515184158623326) · 知乎 · 2026-03-06 · 赞同 0**
> 力扣：[3855. 给定范围内 K 位数字之和](https://leetcode.cn/problems/sum-of-k-digit-numbers-in-a-range/) · Hard · 灵茶山艾府：[贡献法，数学公式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3855.给定范围内K位数字之和

<https://leetcode.cn/problems/sum-of-k-digit-numbers-in-a-range/description/>

题目给出三个整数l、r以及k，其中0 \<\= l \<\= r \<\= 9，而k的取值范围则在1到10^9之间。

现在要求从[l, r]中独立选择k次，组成一个k位的整数。若这个范围内包含0，则这个k位整数允许出现前导0。

问所有可以组合出来的整数之和是多少，答案要求对10^9 + 7取模。

由于k的取值范围很大，因此只能考虑用数学方法来求解这个问题。方便起见，记n \= r - l + 1。

首先不妨考虑个位上的数。对于某个满足l \<\= x \<\= r的数x，一共有n^(k - 1)个以x作为个位数的数，理由是对于从十位开始到最高位这一共k - 1位，每一位上都可以填充l到r这一共n个数，因此一共有n^(k - 1)个数。

这些数的个位都是x，因此累加起来就是x \* n^(k - 1)。更进一步的，这里的x取值范围在l到r，因此所有数的个位之和就是l \* n^(k - 1) + (l + 1) \* n^(k - 1) + ... + r \* n^(k - 1)，即(l + r) \* n // 2 \* n^(k - 1)。方便起见，在这里记s \= (l + r) \* n // 2，那么这里的和就是s \* n^(k - 1)。

接下来对于十位上的数，同样是考虑l \<\= x \<\= r的数x，以x作为十位数的数也是n^(k - 1)个，因此这些数累加起来就是(l \* 10) \* n^(k - 1) + ((l + 1) \* 10) \* n^(k - 1) + ... + (r \* 10) \* n^(k - 1)。将里面的10提出来，就是10 \* s \* n^(k - 1)。

以此类推，就能得到最终结果为(1 + 10 + 100 + ... + 10^(k - 1)) \* s \* n^(k - 1)。

对于这个式子，其中的s是很容易计算的，而最后的n^(k - 1)也可以通过快速幂很方便的得到，剩下的问题就是第一个括号中的值应该如何计算。

很明显，第一个括号内的式子就是111...1111，一共k个1。简单算了一些k比较小的情况，发现这个全1的数对10^9取模没有很明显的规律，因此在这里需要进行一些转化。我在这里采用的方法是将其视为999...9999除以9，而999...9999则可以视为10^k - 1，那么在这里就也可以通过快速幂计算出10^k对10^9取模的结果，而除以9则需要计算9的乘法逆元，在这里可以直接通过费马小定理计算，也就是计算9^(10^9 + 5)对10^9 + 7取模的结果即可。

整理一下，就得到了以下步骤。方便期间，记10^9 + 7为mod：

- 计算n \= r - l + 1
- 计算s \= (l + r) \* n // 2
- 利用快速幂计算n^(k - 1)对mod取模的结果，记为c
- 计算全9对mod取模的结果，也就是先利用快速幂计算10^k对mod取模的结果，然后减去1再对mod取模，记为all9
- 计算9的逆元，也就是利用快速幂计算9^(mod - 2)对mod取模的结果，记为rev9
- 通过all9乘以rev9，得到全1对mod的取模结果，记为all1
- 最后，先将all1乘以s，再乘以c，最后对mod取模的结果即为最终答案

最后附上python代码：

```python
class Solution(object):
    def sumOfNumbers(self, l, r, k):
        """
        :type l: int
        :type r: int
        :type k: int
        :rtype: int
        """
        
        mod = 10 ** 9 + 7

        def quick_pow(base, p):
            if p == 0:
                return 1
            if p == 1:
                return base
            
            res = quick_pow(base, p // 2)
            res = res * res % mod
            if p & 1:
                res = res * base % mod
            return res

        n = r - l + 1
        s = n * (l + r) // 2
        c = quick_pow(n, k - 1)
        all9 = (quick_pow(10, k) - 1 + mod) % mod
        rev9 = quick_pow(9, mod - 2)
        all1 = all9 * rev9
        
        return s * all1 % mod * c % mod
```
