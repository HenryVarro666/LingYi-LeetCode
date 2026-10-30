---
title: "3700. 锯齿形数组的总数II"
aliases: ["yiduobo的每日leetcode 3700.锯齿形数组的总数II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/dynamic-programming", "leetcode/matrix", "题单/动态规划", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1956433954988090443"
zhihu_id: "1956433954988090443"
zhihu_title: "yiduobo的每日leetcode 3700.锯齿形数组的总数II"
question_id: "3700"
question: "锯齿形数组的总数 II"
problem_url: "https://leetcode.cn/problems/number-of-zigzag-arrays-ii/"
difficulty: "Hard"
rating: 2435
created: "2025-10-05T19:09:33+08:00"
updated: "2025-10-05T19:09:34+08:00"
upvotes: 1
comments: 0
---

# 3700. 锯齿形数组的总数II

> **[yiduobo的每日leetcode 3700.锯齿形数组的总数II](https://zhuanlan.zhihu.com/p/1956433954988090443) · 知乎 · 2025-10-05 · 赞同 1**
> 力扣：[3700. 锯齿形数组的总数 II](https://leetcode.cn/problems/number-of-zigzag-arrays-ii/) · Hard · 灵茶山艾府：[两种方法：矩阵快速幂优化 DP / BM+Kitamasa（Python/NumPy/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3700.锯齿形数组的总数II

[3700. 锯齿形数组的总数 II - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-zigzag-arrays-ii/description/)

题目给出三个整数n、l和r。长度为n的锯齿形数组定义如下：

1、数组中所有元素的取值范围都在l到r之间

2、数组中任意两个相邻元素都不相等

3、数组中任意三个元素都不能构成一个严格递增或者严格递减的序列

问可以构造出来的锯齿形数组的总数。

本题中n的取值范围在3到10^9之间，l和r在1到75之间。

本题的题设与上一题类似，不过数据规模产生了变化，之前的常规动态规划就不适用了。

对于这类n特别巨大的问题，要么想办法找通项，要么想办法使用矩阵乘法配合快速幂进行优化。对于本题，很难注意到通项，只能使用后面这种方法。

依然是先将数据范围修改到[0, r - l]，方便期间，计m \= r - l。接下来计算^^^^^形的锯齿形数组，令f[index][v]表示长度为index，且以v结尾的锯齿形数组的数目，index从1开始计数。初始的转移方程与之前一致：

若index为偶数，那么就有

f[index][v] \= f[index - 1][0] + f[index - 1][1] + ... + f[index - 1][v - 1]

若index为奇数，则有

f[index][v] \= f[index - 1][v + 1] + f[index - 1][v + 2] + ... + f[index][m]

在这里可以将所有的f\[index\]都转化为一个1 \* (m + 1)的向量，即\[f\[index\]\[0\], f\[index\]\[1\], ..., f\[index\]\[r - l\]\]，接下来的目标就是找出一个(m + 1) \* (m + 1)的矩阵，可以使得f\[index\]对应的向量，与这个矩阵相乘之后，可以得到f\[index + 1\]。令这个矩阵为base，那么基于矩阵乘法的定义，可以得到如下的方程组：

f[index][0] \* base[0][0] + f[index][1] \* base[1][0] + ... + f[index][m] \* base[m][0] \= f[index + 1][0]

f[index][0] \* base[0][1] + f[index][1] \* base[1][1] + ... + f[index][m] \* base[m][1] \= f[index + 1][1]

...

f[index][0] \* base[0][m] + f[index][1] \* base[1][m] + ... + f[index][m] \* base[m][m] \= f[index + 1][m]

需要注意的是，之前的转移方程需要根据index的奇偶分两种情况，因此也需要构造两个base矩阵，分别记为base1，对应index为偶数的情况，以及base2，对应index为奇数的情况，那么当index为偶数时，其中关于v的项有

f[index][0] \* base1[0][v] + f[index][1] \* base1[1][v] + ... + f[index][m] \* base1[m][v] \= f[index + 1][v]

而根据转移方程，有

f[index + 1][v] \= f[index][0] + f[index][1] + ... + f[index][v - 1]

将这些系数对号入座，可以得到base1[0][v]、base1[1][v]、...、base1[v - 1][v]都为1。更进一步的，可以得到base1为

\[\[0, 1, 1, 1, ..., 1, 1\]

[0, 0, 1, 1, ..., 1, 1]

[0, 0, 0, 1, ..., 1, 1]

...

[0, 0, 0, 0, ..., 0, 1]

\[0, 0, 0, 0, ..., 0, 0\]\]

也就是除对角线之外的右上三角全部为1。

与之对称，base2则应该为除对角线之外的左下三角全部为1。

记ori \= f\[1\] \= \[\[1, 1, 1, 1, ..., 1\]\]，那么最终的f\[n\]就是

ori \* base1 \* base2 \* base1 \* base2 \* ...

最后一项是base1还是base2取决于n是奇数还是偶数。

需要注意的是，矩阵乘法满足结合律，但是不满足交换律，因此在这里还需要先计算base1 \* base2的结果，记为merge，那么最终的式子就可以写作ori \* merge^((n - 1) // 2)，若n为偶数，还需要额外乘上一个base1。

到了这里，就只需要用快速幂来计算merge^((n - 1) // 2)这一项，再计算出最终的矩阵乘法结果。得到结果向量后，将其中的元素累加，乘以2即为最终答案。这样一来，本题的时间复杂度就优化到了O(m^3 \* log(n))，其中m等于r - l。

最后附上python代码：

```python
class Solution(object):
    def zigZagArrays(self, n, l, r):
        """
        :type n: int
        :type l: int
        :type r: int
        :rtype: int
        """
        
        r -= l
        base1 = [[0] * (r + 1) for _ in range(r + 1)]
        base2 = [[0] * (r + 1) for _ in range(r + 1)]
        for i in range(r + 1):
            for j in range(i + 1, r + 1):
                base1[i][j] = 1
            for j in range(i):
                base2[i][j] = 1

        mod = 10 ** 9 + 7

        def mul(a, b):
            m = len(a)
            n = len(a[0])
            t = len(b[0])
            c = [[0] * t for _ in range(m)]
            for i in range(m):
                for j in range(n):
                    for k in range(t):
                        c[i][k] = (c[i][k] + a[i][j] * b[j][k]) % mod
            return c
        
        merge = mul(base1, base2)

        def quick_pow(base, p):
            if p == 1:
                return base
            
            res = quick_pow(base, p // 2)
            res = mul(res, res)
            if p % 2 == 1:
                res = mul(res, base)
            
            return res
        
        ori = [[1] * (r + 1)]
        ori = mul(ori, quick_pow(merge, (n - 1) // 2))
        if n % 2 == 0:
            ori = mul(ori, base1)
        return sum(ori[0]) * 2 % mod
```
