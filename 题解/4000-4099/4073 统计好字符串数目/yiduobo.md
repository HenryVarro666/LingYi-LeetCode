---
title: "4073. 统计好字符串数目"
aliases: ["yiduobo的每日leetcode 4073.统计好字符串数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2090973241556967983"
zhihu_id: "2090973241556967983"
zhihu_title: "yiduobo的每日leetcode 4073.统计好字符串数目"
question_id: "4073"
question: "统计好字符串数目"
problem_url: "https://leetcode.cn/problems/count-good-strings/"
created: "2026-10-07T01:23:14+08:00"
updated: "2026-10-07T01:23:14+08:00"
upvotes: 1
comments: 0
---

# 4073. 统计好字符串数目

> **[yiduobo的每日leetcode 4073.统计好字符串数目](https://zhuanlan.zhihu.com/p/2090973241556967983) · 知乎 · 2026-10-07 · 赞同 1**
> 力扣：[4073. 统计好字符串数目](https://leetcode.cn/problems/count-good-strings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4073.统计好字符串数目

<https://leetcode.cn/problems/count-good-strings/description/>

题目给出一个整数n，其大小在1到10^15之间。

对于一个字符串s，若其仅由'a'以及'b'组成，且满足以下条件之一，那么就称其为好字符串：

- 仅包含一种字符，且其长度为奇数
- 可以写成s \= s1 + s2的形式，其中s1和s2都是非空的好字符串，且s1的最后一个字符与s2的第一个字符不同

问长度为n的好字符串的数量是多少。

题目的数据规模极大，因此在这里要么有O(1)的通项公式，要么有形式非常好的递推式，可以通过矩阵乘法加快速幂在O(logn)的时间内计算得到。

无论是哪一种，都可以先令f[k]表示长度为k的好字符串的数量。那么对于f[k]，其必然是以一个由相同字符串构成且长度为奇数的字符串结尾的，这个字符串的长度可以是1、3、5、...、而对于前面的部分，就是f[k - 1]、f[k - 3]、f[k - 5]、...中任意的，且结尾部分与最后这个奇数长度字符串不同的好字符串之一。由对称性可知，其数量显然就是f[k - 1]、f[k - 3]、f[k - 5]、...的一半。又由于最后这个奇数长度的字符串可以是全a也可以是全b，因此在这里就可以直接写出f[k]的递推式：

f[k] \= f[k - 1] + f[k - 3] + f[k - 5] + ...

更进一步的，由于

f[k - 2] \= f[k - 3] + f[k - 5] + ...

因此上面的式子可以写成

f[k] \= f[k - 1] + f[k - 2]

可以发现，这就是斐波那契数列的递推式，构造经典的\[\[0, 1\], \[1, 1\]\]矩阵配合快速幂就可以在O(logn)的时间内计算出第n项。不过需要特别注意的是，这里的数列的起始项f\[0\] \= 0不变，但是f\[1\]应该是2而不是1，因为长度为1的好字符串可以是'a'或者'b'，有两种情况，因此在计算完成后，还需要将答案再乘以2。

最后附上python代码：

```python
class Solution(object):
    def countGoodStrings(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        def mul(a, b, mod):
            c = [[0, 0], [0, 0]]
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        c[i][j] += a[i][k] * b[k][j]
                        c[i][j] %= mod
            return c

        def quick_pow(base, p, mod):
            if p == 0:
                return [[1, 0], [0, 1]]
            
            if p == 1:
                return base
            
            res = quick_pow(base, p // 2, mod)
            res = mul(res, res, mod)
            if p % 2 == 1:
                res = mul(res, base, mod)
            return res

        mod = 10 ** 9 + 7
        base = [[0, 1], [1, 1]]
        f = quick_pow(base, n - 1, mod)
        return f[1][1] * 2 % mod
```
