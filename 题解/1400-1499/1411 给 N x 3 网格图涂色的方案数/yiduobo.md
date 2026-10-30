---
title: "1411. 给N x 3网格图涂色的方案数"
aliases: ["yiduobo的每日leetcode 1411.给N x 3网格图涂色的方案数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "leetcode/matrix", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/406650487"
zhihu_id: "406650487"
zhihu_title: "yiduobo的每日leetcode 1411.给N x 3网格图涂色的方案数"
question_id: "1411"
question: "给 N x 3 网格图涂色的方案数"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-paint-n-3-grid/"
difficulty: "Hard"
rating: 1845
created: "2021-09-03T23:43:06+08:00"
updated: "2021-09-03T23:43:06+08:00"
upvotes: 0
comments: 0
---

# 1411. 给N x 3网格图涂色的方案数

> **[yiduobo的每日leetcode 1411.给N x 3网格图涂色的方案数](https://zhuanlan.zhihu.com/p/406650487) · 知乎 · 2021-09-03 · 赞同 0**
> 力扣：[1411. 给 N x 3 网格图涂色的方案数](https://leetcode.cn/problems/number-of-ways-to-paint-n-3-grid/) · Hard · 灵茶山艾府：[三种方法：记忆化搜索/递推/矩阵快速幂（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1411.给N x 3网格图涂色的方案数

[力扣](https://leetcode-cn.com/problems/number-of-ways-to-paint-n-3-grid/)

乍一看感觉是状态压缩动态规划的题目，但是仔细分析可以发现如果利用对称性就可以将题目转化成非常简单的递推问题。

题目非常贴心地给出了N \= 1时所有可行的情况，那么实际上，无论N等于多少，其涂色方案的最后一行都必然是这12种方案中的一种。由于这三种颜色是完全等价的，因此我们可以只考虑以某种颜色开头的所有方案数，在这里我们只考虑最左侧是红色的这四种情况。

进一步地，对于红色的这四种情况，可以发现中间格子是绿色还是黄色也是完全等价的，因此我们就可以考虑前两种颜色确定之后的所有方案数，在这里我们只考虑最左侧是红色，中间是黄色的这两种情况，最后将得到的答案乘以6就是所有的情况数了。

对于这两种情况，如果我们想在后面增加新的1 \* 3的网格，那么：

1、对于红-黄-红这种情况：

1-1）可以在后面添加黄-红-黄、黄-绿-黄、绿-红-绿

1-2）可以在后面添加黄-红-绿、绿-红-黄

2、对于红-黄-绿这种情况：

2-1）可以在后面添加黄-红-黄、黄-绿-黄

2-2）可以在后面添加黄-绿-红、绿-红-黄

综合一下，通过每一种

A - B - A形式的网格可以扩展出3个A - B - A形式的网格，2个A - B - C形式的网格

A - B - C形式的网格则可以扩展出2个A - B - A形式的网格，2个A - B - C形式的网格

不妨设红-黄-红形式的网格数目为x，红-黄-绿形式的网格数目为y，那么新加一行之后一共可以得到：

1、(3x + 2y) \* 6种A - B - A形式的网格

2、(2x + 2y) \* 6种A - B - C形式的网格

这(3x + 2y) \* 6种A - B - A形式的网格会由红-黄-红、红-绿-红、黄-红-黄、黄-绿-黄、绿-红-绿、绿-黄-绿这6中情况平分，因此在新增一行之后，红-黄-红的数目就从x变成了3x + 2y

同样的，红-黄-绿的数目从y变成了2x + 2y

这样一来，就得到了一个非常简单的递推式，即

x[i] \= 3 \* x[i - 1] + 2 \* y[i - 1]

y[i] \= 2 \* x[i - 1] + 2 \* y[i - 1]

当然，在这里也可以构造数组来使用矩阵乘法的快速幂进行优化，即

\[x\[i\], y\[i\]\] \* \[\[3, 2\], \[2, 2\]\] \= \[3 \* x\[i\] + 2 \* y\[i\], 2 \* x\[i\] + 2 \* y\[i\]\] \= \[x\[i + 1\], y\[i + 1\]\]

那么我们对矩阵\[\[3, 2\], \[2, 2\]\]计算n - 1次方，然后对于得到的结果，将\[1, 1\]与其相乘之后计算结果矩阵的元素之和，然后乘以6就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def numOfWays(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n == 1:
            return 12

        mod = 10 ** 9 + 7
        base = [[3, 2], [2, 2]]
        final = self.quick_pow(n - 1, base, mod)
        return ((final[0][0] + final[0][1] + final[1][0] + final[1][1]) % mod * 6) % mod

    def quick_pow(self, n, base, mod):
        if n == 1:
            return base[:]
        
        tmp = self.quick_pow(n / 2, base, mod)
        res = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    res[i][j] += tmp[i][k] * tmp[k][j]
                    res[i][j] %= mod
        
        if n % 2 == 0:
            return res
        
        tmp = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    tmp[i][j] += res[i][k] * base[k][j]
                    tmp[i][j] %= mod
        
        return tmp
```
