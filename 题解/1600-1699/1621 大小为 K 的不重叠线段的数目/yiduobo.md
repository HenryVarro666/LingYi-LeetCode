---
title: "1621. 大小为K的不重叠线段的数目"
aliases: ["yiduobo的每日leetcode 1621.大小为K的不重叠线段的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/combinatorics", "题单/数学算法", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/435949477"
zhihu_id: "435949477"
zhihu_title: "yiduobo的每日leetcode 1621.大小为K的不重叠线段的数目"
question_id: "1621"
question: "大小为 K 的不重叠线段的数目"
problem_url: "https://leetcode.cn/problems/number-of-sets-of-k-non-overlapping-line-segments/"
difficulty: "Medium"
rating: 2198
created: "2021-11-21T19:09:20+08:00"
updated: "2021-11-21T19:09:20+08:00"
upvotes: 0
comments: 0
---

# 1621. 大小为K的不重叠线段的数目

> **[yiduobo的每日leetcode 1621.大小为K的不重叠线段的数目](https://zhuanlan.zhihu.com/p/435949477) · 知乎 · 2021-11-21 · 赞同 0**
> 力扣：[1621. 大小为 K 的不重叠线段的数目](https://leetcode.cn/problems/number-of-sets-of-k-non-overlapping-line-segments/) · Medium · 灵茶山艾府：[组合数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1621.大小为K的不重叠线段的数目

[力扣](https://leetcode-cn.com/problems/number-of-sets-of-k-non-overlapping-line-segments/)

最朴素的动态规划是很容易想到的。令f[i][j]表示0到i这些点用j条线段去覆盖，且最后一条线段覆盖住了i这个点的情况总数，那么对于f[i][j]：

1、边界情况，当j \= 1时：

此时仅有一条线段，其右端固定为i，而左端可以选择0到i - 1之间的任意点，因此就有

f[i][j] \= (i - 1) - 0 + 1 \= i

2、对于一般的f[i][j]：

最后一条线段的右端固定为i，而其左边界则取决于前j - 1条线段覆盖区间的右边界cut_pos在什么位置。

对于前j - 1条线段而言，其覆盖的区间的右边界至少为j - 1，而至多则是i - 1，因此需要留下最后一段给第j条线段，因此cut_pos的取值范围在j - 1到i - 1之间。

对于当前的cut_pos，最后一条线段的左边界可以选择cut_pos到i - 1之间的任一点，因此就有

$f[i][j] = \sum_{cutpos = j - 1}^{i - 1}{f[cutpos][j - 1] * (i - cutpos)}$

全部计算完成后，f[k][k] + f[k + 1][k] + ... + f[n - 1][k]就是最终答案。

上面这种做法由于需要枚举cut_pos，因此时间复杂度为O(n^2 \* k)，是比较高的，需要进行优化。

观察上面的转移方程，如果将其全部列出来，就有

f[i][j] \= f[j - 1][j - 1] \* (i - j +1) +

f[j][j - 1] \* (i - j) +

... +

f[i - 1][j - 1]

变形之后可得

f[i][j] \= f[j - 1][j - 1] +

f[j][j - 1] + f[j - 1][j - 1] +

... +

f[i -1][j - 1] + ... + f[j - 1][j - 1]

可以发现这里就变成了某种连续和。令g[i][j] \= f[i][j] + f[i - 1][j] + ... + f[j][j]，那么就有

f[i][j] \= g[j - 1][j - 1] + g[j][j - 1] + ... + g[i - 1][j - 1]

同时又有

f[i - 1][j] \= g[j - 1][j - 1] + g[j][j - 1] + ... + g[i - 2][j - 1]

因此

f[i][j] \= f[i - 1][j] + g[i - 1][j - 1]

而对于g来说，

g[i][j] \= f[i][j] + f[i - 1][j] + ... + f[j][j]

同时又有

g[i - 1][j] \= f[i - 1][j] + f[i - 2][j] + ... + f[j][j]

因此

g[i][j] \= g[i - 1][j] + f[i][j]

综合起来，就是

f[i][j] \= f[i - 1][j] + g[i - 1][j - 1]

g[i][j] \= g[i - 1][j] + f[i][j]

这样一来，就可以省去枚举cut_pos的过程，将整体的时间复杂度降到O(nk)了。除此之外，根据g的定义，在计算完成后g[n - 1][k]就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def numberOfSets(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """

        f = [[0] * (k + 1) for _ in range(n)]
        g = [[0] * (k + 1) for _ in range(n)]
        mod = 10 ** 9 + 7
        for i in range(1, n):
            f[i][1] = i
            g[i][1] = g[i - 1][1] + i 
            for j in range(2, min(i, k) + 1):
                f[i][j] = f[i - 1][j] + g[i - 1][j - 1]
                f[i][j] %= mod

                g[i][j] = g[i - 1][j] + f[i][j]
                g[i][j] %= mod

        return g[-1][-1]

        '''
        f[i][j] = f[j - 1][j - 1] * (i - j + 1) +
                  f[j][j - 1] * (i - j) +
                  ... +
                  f[i - 1][j - 1]

                = f[j - 1][j - 1] +
                  f[j][j - 1] + f[j - 1][j - 1] +
                  ... +
                  f[i - 1][j - 1] + ... + f[j - 1][j - 1]
                
        g[i][j] = f[i][j] + ... + f[j][j]
        g[i][j] = g[i - 1][j] + f[i][j]

        f[i][j] = g[j - 1][j - 1] + g[j][j - 1] + ... + g[i - 1][j - 1]
        f[i][j] = f[i - 1][j] + g[i - 1][j - 1]
        '''
```
