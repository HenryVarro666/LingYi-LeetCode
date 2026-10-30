---
title: "629. K个逆序对数组"
aliases: ["yiduobo的每日leetcode 629.K个逆序对数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/270432560"
zhihu_id: "270432560"
zhihu_title: "yiduobo的每日leetcode 629.K个逆序对数组"
question_id: "629"
question: "K个逆序对数组"
problem_url: "https://leetcode.cn/problems/k-inverse-pairs-array/"
created: "2020-10-31T00:04:11+08:00"
updated: "2020-10-31T00:04:11+08:00"
upvotes: 0
comments: 0
---

# 629. K个逆序对数组

> **[yiduobo的每日leetcode 629.K个逆序对数组](https://zhuanlan.zhihu.com/p/270432560) · 知乎 · 2020-10-31 · 赞同 0**
> 力扣：[629. K个逆序对数组](https://leetcode.cn/problems/k-inverse-pairs-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

629.K个逆序对数组<https://leetcode-cn.com/problems/k-inverse-pairs-array/>

感觉用组合数学或者母函数的方法可以做，但是没有想出来，最后还是选择了动态规划。使用f[i][j]表示1到i这i个数形成的排列中，有j个逆序对的排列数量。

对于f[i][j]，我们可以认为是在f[i - 1][p]的基础上插入数字i，在p个逆序对的基础上再形成几组逆序对最终得到j，那么就有：

1、如果将i添加到最后:

不会形成新的逆序对，那么就有f[i][j] +\= f[i - 1][j]

2、如果将i添加到倒数第二位:

i将与最后一位形成一组新的逆序对，那么就有f[i][j] +\= f[i - 1][j - 1]

3、如果将i添加到倒数第三位：

i将与最后一位以及倒数第二位形成两组新的逆序对，那么就有f[i][j] +\= f[i - 1][j - 2]

i、此时将i添加到第一位：

i将会和后面的所有i - 1个数都形成逆序对，共i - 1组，那么就有f[i][j] +\= f[i - 1][j - i + 1]

综上所述，最后就有

f[i][j] \= f[i - 1][j] + f[i - 1][j - 1] + ... + f[i - 1][j - i + 1]

不过这个做法最终的时间复杂度是O(n^3)，效率不太行。

注意到这里f[i][j]是某种区间和的形式，那么就可以使用前缀和来进行优化。

另外，又由于这里的f[i][j - 1] \= f[i - 1][j - 1] + f[i - 1][j - 2] + ... + f[i - 1][j - i]，那么我们在f[i][j - 1]的基础上加上f[i - 1][j]再减去f[i - 1][j - i]，就直接可以得到f[i][j]，没有必要再计算前缀和了。

最后附上python代码：

```python
class Solution(object):
    def kInversePairs(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """

        f = [[0] * (k + 1) for _ in range(n + 1)]
        mod = 10 ** 9 + 7
        for i in range(1, n + 1):
            for j in range(min(k + 1, (i * (i - 1) / 2 + 1))):
                if j == 0:
                    f[i][j] = 1
                else:
                    f[i][j] = f[i][j - 1] + f[i - 1][j]
                    if j >= i:
                        f[i][j] -= f[i - 1][j - i]
                    f[i][j] %= mod

        return f[n][k]
```
