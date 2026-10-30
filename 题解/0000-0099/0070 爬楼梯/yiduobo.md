---
title: "70. 爬楼梯"
aliases: ["yiduobo的每日leetcode 70.爬楼梯"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/matrix", "题单/动态规划", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/动态规划/一-入门-DP", "题单/动态规划/十一-优化-DP", "题单/LeetCode-热题-100/动态规划", "题单/面试经典-150-题/一维动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/131626291"
zhihu_id: "131626291"
zhihu_title: "yiduobo的每日leetcode 70.爬楼梯"
question_id: "70"
question: "爬楼梯"
problem_url: "https://leetcode.cn/problems/climbing-stairs/"
difficulty: "Easy"
created: "2020-04-16T23:19:18+08:00"
updated: "2020-04-16T23:19:18+08:00"
upvotes: 1
comments: 0
---

# 70. 爬楼梯

> **[yiduobo的每日leetcode 70.爬楼梯](https://zhuanlan.zhihu.com/p/131626291) · 知乎 · 2020-04-16 · 赞同 1**
> 力扣：[70. 爬楼梯](https://leetcode.cn/problems/climbing-stairs/) · Easy · 灵茶山艾府：[教你一步步思考动态规划：从记忆化搜索到递推到矩阵快速幂（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

70.爬楼梯<https://leetcode-cn.com/problems/climbing-stairs/>

动态规划题目，也可以用数学方法去解决。

令f[i]表示走到第i阶一共有多少种走法，那么因为每次可以走一步或者两步，于是有

f[i] \= f[i - 1] + f[i - 2]

边界条件f[1] \= 1，f[2] \= 2。

仔细一看，这就是斐波那契数列，于是可以直接用通项公式来求解，时间复杂度为O(logn)。

---

当然也可以用快速幂优化的矩阵乘法，矩阵乘法的基本运算规则为

$c[x][y] = \sum_{z}{a[x][z] * b[z][y]}$

具体解释为c中的点c[x，y]是由a中x行的每个点与b中y列对应的每个点的乘积之和得到的。于是执行矩阵乘法的前提是a的列数必须等于b的行数。**一个m行，n列的矩阵与另一个n行，k列的矩阵相乘之后得到将是一个m行，k列的矩阵**。

接下来我们开始构造这个乘法过程：

首先，对于当前某个f[k]，我们可以将其与f[k - 1]组合，形成起始矩阵a。

a的具体形式为\[f\[k - 1\], f\[k\]\]，这个矩阵是1行2列的。

我们的目标就是通过一次乘法得到新的矩阵c，具体形式为\[f\[k\], f\[k +1\]\]，这个矩阵同样是1行2列的。由于我们知道f\[k + 1\] \= f\[k\] + f\[k - 1\]，将其带入c，就是\[f\[k\], f\[k -1\] + f\[k\]\]。

接下来，构造乘数矩阵b。我们从一个1 \* 2的矩阵乘法得到另一个1 \* 2的矩阵，中间的乘数矩阵一定是2 \* 2的。

我们需要求出这个b中每个元素的值，使其满足a \* b \= c。

那么根据矩阵乘法的定义，我们可以知道

c[0][0] \= a[0][0] \* b[0][0] + a[0][1] \* b[1][0]

c[0][1] \= a[0][0] \* b[0][1] + a[0][1] \* b[1][1]

将f值代入其中，得到：

c[0][0] \= f[k]

a[0][0] \* b[0][0] + a[0][1] \* b[1][0] \= f[k - 1] \* b[0][0] + f[k] \* b[1][0]

c[0][1] \= f[k + 1] \= f[k -1] + f[k]

a[0][0] \* b[0][1] + a[0][1] \* b[1][1] \= f[k - 1] \* b[0][1] + f[k] \* b[1][1]

于是就有：

f[k] \= f[k - 1] \* b[0][0] + f[k] \* b[1][0]

f[k -1] + f[k] \= f[k - 1] \* b[0][1] + f[k] \* b[1][1]

可以解出

b[0][0] \= 0

b[1][0] \= 1

b[0][1] \= 1

b[1][1] \= 1

那么b矩阵最终就是

\[\[0, 1\]

\[1, 1\]\]

接下来，例如对于n\=5，我们可以按下面的过程求解。

首先有起始矩阵a \= [1, 2]

接下来a \* b \= [1 \* 0 + 2 \* 1, 1 \* 1 + 2 \* 1] \= [2, 3]

再接下来a \* b \* b \= [2 \* 0 + 3 \* 1, 2 \* 1 + 3 \* 1] \= [3, 5]

最后就是a \* b \* b \* b \= [3 \* 0 + 5 \* 1, 3 \* 1 + 5 \* 1] \= [5, 8]

于是最终结果就是8。可以发现这个过程中一共执行了n - 2次矩阵乘法，而矩阵乘法是满足结合律的，于是也可以变成a \* (b^3)来计算。

对于乘方运算，之前第50题Pow(x, n)（传送门在这里[yiduobo：yiduobo的每日leetcode 50.Pow(x, n)](https://zhuanlan.zhihu.com/p/126359415)）已经给出了一种O(logn)的处理方式，这里只需如法炮制即可。于是，对于一个n，先计算出b^(n - 2)，再执行一次矩阵乘法即可，最终的时间复杂度为O(m^3 \* logn)。这里的m^3为矩阵乘法的复杂度，其中m为矩阵的长度。由于这里m\=2，于是可以认为这里矩阵乘法仅仅是带来了一个大的常数，最终时间复杂度还是O(logn)。

另外，这里b的幂次也是存在一些规律的。印象中有文章已经指出在某些情况下利用b的幂次的规律可以进一步将时间复杂度优化到O(loglogn)，不过具体的做法已经记不清楚了。

实际上，如果n不是特别大，在这里用矩阵快速幂的做法性能并不突出。不过矩阵快速幂在某些动态规划问题的性能优化上是很有意思的，因此这里最终使用的是这个版本。

最后附上python代码：

```python
class Solution(object):
    def climbStairs(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n == 1:
            return 1
        elif n == 2:
            return 2
        else:
            b = [[0, 1], [1, 1]]
            final_b = self.fast_pow(b, n - 2)
            a = [1, 2]
            return a[0] * final_b[0][1] + a[1] * final_b[1][1]

    def fast_pow(self, base_b, n):
        if n == 1:
            return [base_b[0][:], base_b[1][:]]
        
        tmp = self.fast_pow(base_b, n / 2)
        
        res = [[0, 0], [0, 0]]

        res[0][0] = tmp[0][0] * tmp[0][0] + tmp[0][1] * tmp[1][0]
        res[0][1] = tmp[0][0] * tmp[0][1] + tmp[0][1] * tmp[1][1]
        res[1][0] = tmp[1][0] * tmp[0][0] + tmp[1][1] * tmp[1][0]
        res[1][1] = tmp[1][0] * tmp[0][1] + tmp[1][1] * tmp[1][1]

        if n % 2 == 0:
            return res

        tmp[0][0] = res[0][0] * base_b[0][0] + res[0][1] * base_b[1][0]
        tmp[0][1] = res[0][0] * base_b[0][1] + res[0][1] * base_b[1][1]
        tmp[1][0] = res[1][0] * base_b[0][0] + res[1][1] * base_b[1][0]
        tmp[1][1] = res[1][0] * base_b[0][1] + res[1][1] * base_b[1][1]
        return tmp
```
