---
title: "1420. 生成数组"
aliases: ["yiduobo的每日leetcode 1420.生成数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/408014597"
zhihu_id: "408014597"
zhihu_title: "yiduobo的每日leetcode 1420.生成数组"
question_id: "1420"
question: "生成数组"
problem_url: "https://leetcode.cn/problems/build-array-where-you-can-find-the-maximum-exactly-k-comparisons/"
created: "2021-09-07T23:39:04+08:00"
updated: "2021-09-07T23:39:04+08:00"
upvotes: 1
comments: 0
---

# 1420. 生成数组

> **[yiduobo的每日leetcode 1420.生成数组](https://zhuanlan.zhihu.com/p/408014597) · 知乎 · 2021-09-07 · 赞同 1**
> 力扣：[1420. 生成数组](https://leetcode.cn/problems/build-array-where-you-can-find-the-maximum-exactly-k-comparisons/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1420.生成数组

[力扣](https://leetcode-cn.com/problems/build-array-where-you-can-find-the-maximum-exactly-k-comparisons/)

感觉应该可以用组合数学来做，但是并没有想出做法，只能老老实实用动态规划来做了。

首先分析题目给出的代码段。这里的cost说的是若当前元素大于之前元素中的最大值，那么就将cost加1，于是一个自然的想法就是将之前元素的最大值以及当前的cost都维护起来，那么就可以令f[i][j][c]表示长度为i + 1，其中最大值为j，且已经使用题目代码段算法中cost为c的数组的数目。对于f[i][j][c]：

1、首先是枚举的范围，i自然是0到n - 1，j则是1到m，c的下界必然是1，上界则是到i + 1与k之间的较小值

2、接下来考虑边界条件。当i为0时，数组长度为1，且其中的元素必然大于题目代码段中的初始值-1，因此无论怎么选择，f[i][j][c]必然为1

3、最后考虑一般情况。对于i > 0时的f[i][j][c]而言，有两种可能：

3-1）数组的最后一位为j，而之前所有的数都小于j，那么在最后一位这里将产生一次比较的代价，因此就有f[i][j][c] \= f[i][j][c] + f[i - 1][0][c - 1] + f[i - 1][1][c - 1] + ... f[i - 1][j - 1][c - 1]

注意到这里f[i - 1]中的项可以认为是关于j的一个前缀和，因此可以在枚举j的过程中顺便计算出来，这样一来就省去了枚举的复杂度

3-2）数组的最后一位小于等于j，而之前已经有某个数等于j了，那么在最后一位这里不会产生比较的代价，因此就有f[i][j][c] \= f[i][j][c] + f[i - 1][j][c] \* j

这里乘以j的理由是数组的最后一位可以选择1到j之间的任何数，而之前的状态都是f[i - 1][j][c]

动态规划结束后，最后答案就是f[n - 1][1][k] + f[n - 1][2][k] + ... f[n - 1][m][k]

最后附上python代码：

```python
class Solution(object):
    def numOfArrays(self, n, m, k):
        """
        :type n: int
        :type m: int
        :type k: int
        :rtype: int
        """

        mod = 10 ** 9 + 7

        f = [[[0] * (k + 1) for _ in range(m + 1)] for _ in range(n + 1)]
        for i in range(n):
            prefix_s = [0] * (k + 1)
            for j in range(1, m + 1):
                for c in range(1, min(i + 2, k + 1)):
                    if i == 0:
                        f[i][j][c] = 1
                    else:
                        f[i][j][c] = (f[i - 1][j][c] * j % mod + prefix_s[c - 1]) % mod
                    
                    prefix_s[c - 1] = (prefix_s[c - 1] + f[i - 1][j][c - 1]) % mod

        res = 0
        for j in range(1, m + 1):
            res = (res + f[n - 1][j][k]) % mod
        
        return res
```
