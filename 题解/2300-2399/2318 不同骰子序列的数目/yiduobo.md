---
title: "2318. 不同骰子序列的数目"
aliases: ["yiduobo的每日leetcode 2318.不同骰子序列的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/dp", "leetcode/dp-2", "题单/动态规划", "题单/动态规划/七-其他线性-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/556696362"
zhihu_id: "556696362"
zhihu_title: "yiduobo的每日leetcode 2318.不同骰子序列的数目"
question_id: "2318"
question: "不同骰子序列的数目"
problem_url: "https://leetcode.cn/problems/number-of-distinct-roll-sequences/"
difficulty: "Hard"
rating: 2090
created: "2022-08-23T00:11:47+08:00"
updated: "2022-08-23T00:11:47+08:00"
upvotes: 0
comments: 0
---

# 2318. 不同骰子序列的数目

> **[yiduobo的每日leetcode 2318.不同骰子序列的数目](https://zhuanlan.zhihu.com/p/556696362) · 知乎 · 2022-08-23 · 赞同 0**
> 力扣：[2318. 不同骰子序列的数目](https://leetcode.cn/problems/number-of-distinct-roll-sequences/) · Hard · 灵茶山艾府：[从三维到二维（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2318.不同骰子序列的数目

[力扣](https://leetcode.cn/problems/number-of-distinct-roll-sequences/)

经典的动态规划问题，令f[i][j]表示前i次投掷，其中最后一次投掷的点数为j + 1时合法的序列数目。那么对于f[i][j]，令g_set[j]表示1到6中与j + 1互质的数的集合，那么就有

f[i][j] \= sum(f[i - 1][k]) - count(i - 1, k, j)，其中k + 1属于g_set[j]，count(i - 1, k, j)则表示f[i - 1][k]表示的序列中倒数第二位为j + 1的合法序列数目。

需要注意的是，在这里count(i - 1, k, j)不能简单的用f[i - 2][j]来代替，这里的理由是因为f[i - 1][k]对应的序列，其倒数第三位，也就是第i - 3位上不能为k + 1，因为最后这一位已经是k + 1了。但是对于f[i - 2][j]而言，其对应序列的倒数第二位，同样是第i - 3为上是可以等于k + 1的，因此

count(i - 1, k, j) \= f[i - 2][j] - “f[i - 2][j]表示的序列中倒数第二位上为k + 1的合法序列的数量”

到了这里，似乎就无法使用二维的状态表示来处理这个问题了。在这里一个自然的想法就是将状态改造成三维，令f[i][j][k]表示投掷i次，最后两次的点数分别为j + 1和k + 1时的合法序列数目，对于本题的数据规模也是可行的。

不过在这里，继续沿用二维的状态表示，通过找规律来处理也是可行的。根据上面的结论，最终的f[i][j]应该可以写成

f[i][j] \= f[i - 1][k1] - count(i - 1, k1, j) + f[i - 1][k2] - count(i - 1, k2, j) + ... + f[i - 1][km] - count(i - 1, km, j)

将count(i - 1, k, j) \= f[i - 2][j] - “f[i - 2][j]表示的序列中倒数第二位上为k + 1的合法序列的数量”代入，就有

f[i][j] \= f[i - 1][k1] + f[i - 1][k2] + ... + f[i - 1][km] - f[i - 2][j] \* m +

“f[i - 2][j]表示的序列中倒数第二位上为k1 + 1的合法序列的数量” +

“f[i - 2][j]表示的序列中倒数第二位上为k2 + 1的合法序列的数量” +

... +

“f[i - 2][j]表示的序列中倒数第二位上为km + 1的合法序列的数量”

可以发现，后面这一大堆文字描述刚巧就是一个f[i - 2][j]中的所有序列数量，也就是说上面的式子可以简化成

f[i][j] \= sum(f[i - 1][k]) - f[i - 2][j] \* (len(g_set[j]) - 1)，其中k + 1属于g_set[j]

又由于这里的状态转移只与上两轮有关，同时与上上轮的状态位恰好相同，因此可以使用两个数组f和g来滚动，省去i这一维。

需要特别注意的是，在前几轮有几种特殊情况。对于第二轮而言，只需要考虑不与第一轮重复就行了。而对于第三轮，由于不存在i - 3这一轮，因此上面描述的重复也不会发生，此时就应该直接减去len(g_set[j])个f[i - 2][j]。

另外，对于这种递推式固定的问题，也可以使用矩阵乘法来加速。我在这里偷懒就没有实现了。

最后附上python代码：

```python
class Solution(object):
    def distinctSequences(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n == 1:
            return 6
        elif n == 2:
            return 22
        elif n == 3:
            return 66
        else:
            f = [1] * 6
            g = [f[1] + f[2] + f[3] + f[4] + f[5],
                 f[0] + f[2] + f[4],
                 f[0] + f[1] + f[3] + f[4],
                 f[0] + f[2] + f[4],
                 f[0] + f[1] + f[2] + f[3] + f[5],
                 f[0] + f[4]]
            f = [g[1] + g[2] + g[3] + g[4] + g[5] - 5,
                 g[0] + g[2] + g[4] - 3,
                 g[0] + g[1] + g[3] + g[4] - 4,
                 g[0] + g[2] + g[4] - 3,
                 g[0] + g[1] + g[2] + g[3] + g[5] - 5,
                 g[0] + g[4] - 2]
            
            f, g = g, f
            mod = 10 ** 9 + 7
            for index in range(3, n):
                f[0] = (g[1] + g[2] + g[3] + g[4] + g[5] - 4 * f[0] + 4 * mod) % mod
                f[1] = (g[0] + g[2] + g[4] - 2 * f[1] + 2 * mod) % mod
                f[2] = (g[0] + g[1] + g[3] + g[4] - 3 * f[2] + 3 * mod) % mod
                f[3] = (g[0] + g[2] + g[4] - 2 * f[3] + 2 * mod) % mod
                f[4] = (g[0] + g[1] + g[2] + g[3] + g[5] - 4 * f[4] + 4 * mod) % mod
                f[5] = (g[0] + g[4] - f[5] + mod) % mod
            
                f, g = g, f
            
            return sum(g) % mod
```
