---
title: "790. 多米诺和托米诺平铺"
aliases: ["yiduobo的每日leetcode 790.多米诺和托米诺平铺"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/dynamic-programming", "leetcode/matrix", "leetcode/di-tui", "题单/动态规划", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/341377608"
zhihu_id: "341377608"
zhihu_title: "yiduobo的每日leetcode 790.多米诺和托米诺平铺"
question_id: "790"
question: "多米诺和托米诺平铺"
problem_url: "https://leetcode.cn/problems/domino-and-tromino-tiling/"
difficulty: "Medium"
created: "2021-01-02T16:19:28+08:00"
updated: "2021-01-02T16:19:28+08:00"
upvotes: 0
comments: 0
---

# 790. 多米诺和托米诺平铺

> **[yiduobo的每日leetcode 790.多米诺和托米诺平铺](https://zhuanlan.zhihu.com/p/341377608) · 知乎 · 2021-01-02 · 赞同 0**
> 力扣：[790. 多米诺和托米诺平铺](https://leetcode.cn/problems/domino-and-tromino-tiling/) · Medium · 灵茶山艾府：[[灵茶山艾府题解/solutions/0790 多米诺和托米诺平铺 · 【图解】f-n-=2-f-n-1-+f-n-3-（Python-Java-C++-Go）|【图解】f[n]=2*f[n-1]+f[n-3]（Python/Java/C++/Go）]]

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

790.多米诺和托米诺平铺

[力扣](https://leetcode-cn.com/problems/domino-and-tromino-tiling/)

经典的动态规划问题，如果这里的行数稍微多一些，那么就要用到状态压缩动态规划了。这里的行数只有两行，那么我们如果按列来划分状态，那么每一列可能出现的合法状态有三种，分别是该列填满，该列覆盖了第1行的格子，以及该列覆盖了第2行的格子。

为了方便描述，在这里将四种方向的托米诺，根绝其直角开口的方向称作一、二、三、四象限托米诺。

使用三个数组f，g，h分别表示这三种情况，那么：

1、对于f[i]

1-1）可以通过f[i - 1]加上一个竖直的多米诺得到，例如

XXX Y

XXX Y

1-2）可以通过f[i - 2]加上两块横置的多米诺得到，例如

XX YY

XX ZZ

1-3）可以通过g[i - 1]加上一个四象限托米诺得到，例如

XXX Y

XX YY

1-4）可以通过h[i - 1]加上一个三象限托米诺得到，例如

XX YY

XXX Y

于是就有f[i] \= f[i - 1] + f[i - 2] + g[i - 1] + h[i - 1]

2、对于h[i]

2-1）可以通过f[i - 2]加上一个二象限的托米诺得到，例如

XX YY

XX Y

2-2）可以用过g[i - 1]在第一行加上一个横置的多米诺得到，例如

XX YY

XXX

于是有h[i] \= f[i - 2] + g[i - 1]

3、对于g[i]，与h[i]呈对称的状态，于是有g[i] \= f[i - 2] + h[i - 1]

总结一下，得到状态转移方程
f[i] \= f[i - 1] + f[i - 2] + g[i - 1] + h[i - 1]

h[i] \= f[i - 2] + g[i - 1]

g[i] \= f[i - 2] + h[i - 1]

其中边界条件为

f[0] \= f[1] \= 1

h[0] \= h[1] \= 0

g[0] \= g[1] \= 0

注意到状态转移的方式，那么可以使用滚动数组来优化，进一步的，这种形式也可以使用矩阵乘法加上快速幂来进行优化。

在状态转移的过程中，每一轮执行的操作做是将第i - 1轮状态

X\[i - 1\] \= \[f\[i - 2\], f\[i - 1\], g\[i - 1\], h\[i - 1\]\]

通过某种方式转化为

X\[i\] \= \[f\[i - 1\], f\[i\], g\[i\], h\[i\]\]

那么可以假设有一个4\*4的矩阵A，满足X[i - 1] \* A \= X[i]，那么列出乘法过程中的方程：

f[i - 2] \* A[0][0] + f[i - 1] \* A[1][0] + g[i - 1] \* A[2][0] + h[i - 1] \* A[3][0] \= f[i - 1]

f[i - 2] \* A[0][1] + f[i - 1] \* A[1][1] + g[i - 1] \* A[2][1] + h[i - 1] \* A[3][1] \= f[i]

f[i - 2] \* A[0][2] + f[i - 1] \* A[1][2] + g[i - 1] \* A[2][2] + h[i - 1] \* A[3][2] \= g[i]

f[i - 2] \* A[0][3] + f[i - 1] \* A[1][3] + g[i - 1] \* A[2][3] + h[i - 1] \* A[3][3] \= h[i]

根据上面的状态转移方程，可以解得数组A为

\[\[0, 1, 1, 1\],

[1, 1, 0, 0],

[0, 1, 0, 1],

\[0, 1, 1, 0\]\]

有了数组A，我们就可以从边界条件X[1] \= [1, 1, 0, 0]开始，与数组A进行累乘直到计算出X[N]，而答案就是最后的X[N][1]。

由于矩阵的乘法时满足结合律的，那么这里可以写成

X[N] \= X[1] \* A \* A \* ... \* A \= X[1] \* A^(N - 1)

到了这里，对矩阵A执行快速幂算法，就可以在O(logn)的时间内求出X[N]了。不过由于这里的N大小只有1000，而矩阵乘法本身的复杂度是矩阵大小的三次方，在这里也就是64，因此在这里使用矩阵乘法加快速幂实际上比O(n)的动态规划也快不了多少。

求出T \= A^(N - 1)之后，最终答案就是T[0][1] + T[1][1]。因为我们最终的答案为X[N][1]，那么通过X[1] \* T可知

X[N][1] \= X[1][0] \* T[0][1] + X[1][1] \* T[1][1] + X[1][2] \* T[2][1] + X[1][3] \* T[3][1]，其中X的前两项为1后两项为0，因此最终只需要计算T[0][1] + T[1][1]即可。

最后附上python代码：

```python
class Solution(object):
    def numTilings(self, N):
        """
        :type N: int
        :rtype: int
        """

        if N == 1:
            return 1
            
        base = [[0, 1, 1, 1],
                [1, 1, 0, 0],
                [0, 1, 0, 1],
                [0 ,1, 1, 0]]
        
        mod = (10 ** 9 + 7)

        tmp = self.q_pow(N - 1, base, mod)
        return (tmp[0][1] + tmp[1][1]) % mod
        

    def q_pow(self, n, base, mod):
        if n == 1:
            return base[:]
        
        tmp = self.q_pow(n / 2, base, mod)
        ret = []
        for i in range(4):
            ret.append([])
            for j in range(4):
                ret[-1].append(0)
                for k in range(4):
                    ret[-1][-1] += tmp[i][k] * tmp[k][j]
                    ret[-1][-1] %= mod

        if n & 1:
            tmp = []
            for i in range(4):
                tmp.append([])
                for j in range(4):
                    tmp[-1].append(0)
                    for k in range(4):
                        tmp[-1][-1] += ret[i][k] * base[k][j]
                        tmp[-1][-1] %= mod
            return tmp
        
        return ret
```
