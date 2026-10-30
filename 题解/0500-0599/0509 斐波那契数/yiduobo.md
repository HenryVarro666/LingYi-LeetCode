---
title: "509. 斐波那契数"
aliases: ["yiduobo的每日leetcode 509.斐波那契数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/dynamic-programming", "leetcode/matrix", "题单/动态规划", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/259578419"
zhihu_id: "259578419"
zhihu_title: "yiduobo的每日leetcode 509.斐波那契数"
question_id: "509"
question: "斐波那契数"
problem_url: "https://leetcode.cn/problems/fibonacci-number/"
difficulty: "Easy"
created: "2020-09-27T21:12:41+08:00"
updated: "2020-09-27T21:12:41+08:00"
upvotes: 0
comments: 0
---

# 509. 斐波那契数

> **[yiduobo的每日leetcode 509.斐波那契数](https://zhuanlan.zhihu.com/p/259578419) · 知乎 · 2020-09-27 · 赞同 0**
> 力扣：[509. 斐波那契数](https://leetcode.cn/problems/fibonacci-number/) · Easy · 灵茶山艾府：[三种写法：数组递推/空间优化/矩阵快速幂（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

昨天写好但是似乎没发出来？今天补上这一题。

509.斐波那契数<https://leetcode-cn.com/problems/fibonacci-number/>

经典的斐波那契数列问题，方法也是多种多样，可以直接递推计算，也可以使用通项公式法，或者矩阵乘法加快速幂。

这里介绍一下矩阵乘法加快速幂的方法，这个做法在系数确定的递推问题中都可以使用，可以将一般情况下O(n)的时间复杂度优化到O(nlogn)。

首先介绍一下矩阵乘法的定义。矩阵乘法要求一个m \* n的矩阵与一个n \* p的矩阵相乘，最终得到一个m \* p的矩阵，其中第一个矩阵的列数必须和第二个矩阵的行数相同。

对于结果矩阵中的第i行第j列，其计算方式为：

C[i][j] \= ΣA[i][k] \* B[k][j]

例如C中第2行第3列，其计算方式为：

C[2][3] \= A[2][0] \* B[0][3] + A[2][1] \* B[1][3] + ... + A[n][0] \* B[n][3]

回到这个题目。对于式子f[k] \= f[k - 1] + f[k - 2]，我们构造一个1 \* 2的矩阵，其形式为

A\[k - 1\] \= \[f\[k - 2\], f\[k - 1\]\]

那么对于数列中的下一项，就是

A\[k\] \= \[f\[k - 1\], f\[k\]\]

那么我们现在的目标就是构造一个2 \* 2的矩阵X，使得A[k - 1] \* X \= A[k]

根据矩阵乘法的定义，我们可以写出下面两个式子：

A[k - 1][0][0] \* X[0][0] + A[k - 1][0][1] \* X[1][0] \= A[k][0][0]

A[k - 1][0][0] \* X[0][1] + A[k - 1][0][1] \* X[1][1] \= A[k][0][1]

将f[k - 2], f[k - 1]以及f[k]带入，可以得到

f[k - 2] \* X[0][0] + f[k - 1] \* X[1][0] \= f[k - 1]

f[k - 2] \* X[0][1] + f[k - 1] \* X[1][1] \= f[k]

那么就可以解得

X[0][0] \= 0, X[1][0] \= 1, X[0][1] \= 1, X[1][1] \= 1

即矩阵X为

\[\[0, 1\], \[1, 1\]\]

得到X之后，我们就可以从A\[1\] \= \[f\[0\], f\[1\]\]开始，通过累乘X来计算A\[N\]了。当然，依次累乘的时间复杂度还是O(N)，同时还附带了矩阵乘法的常数在里面，性能还不如直接递推，但是矩阵乘法是满足结合律的，即对于式子

A[N] \= A[1] \* X \* X \* X \* ... \* X

而言，后面这一堆X可以先计算好，即

A[N] \= A[1] \* (X \* X \* X \* ... \* X)

对于括号里面的项，可以视为X的幂，那么就可以使用快速幂来进行优化，这里的时间复杂度为O(logN)。得到括号中的项之后，由于A[1][0][0]为0，因此答案就是幂次矩阵的右下角。

最后附上python代码：

```python
class Solution(object):
    def fib(self, N):
        """
        :type N: int
        :rtype: int
        """

        
        if N == 0:
            return 0
        if N == 1:
            return 1
        
        k = N - 1
        tmp_X = self.quick_pow([[0, 1], [1, 1]], k)
        
        return tmp_X[1][1]

    def quick_pow(self, base, n):
        if n == 1:
            return base
        
        tmp = self.quick_pow(base, n / 2)
        ret = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    ret[i][j] += tmp[i][k] * tmp[k][j]
        
        if n % 2 == 1:
            new_ret = [[0, 0], [0, 0]]
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        new_ret[i][j] += ret[i][k] * base[k][j]
            return new_ret
        
        return ret
```
