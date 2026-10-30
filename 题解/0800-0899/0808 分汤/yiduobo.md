---
title: "808. 分汤"
aliases: ["yiduobo的每日leetcode 808.分汤"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "leetcode/probability-and-statistics", "题单/动态规划", "题单/数学算法", "题单/动态规划/十五-概率-DP-期望-DP", "题单/数学算法/三-概率期望"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/343553001"
zhihu_id: "343553001"
zhihu_title: "yiduobo的每日leetcode 808.分汤"
question_id: "808"
question: "分汤"
problem_url: "https://leetcode.cn/problems/soup-servings/"
difficulty: "Medium"
rating: 2397
created: "2021-01-11T21:49:28+08:00"
updated: "2021-01-11T21:49:28+08:00"
upvotes: 1
comments: 1
---

# 808. 分汤

> **[yiduobo的每日leetcode 808.分汤](https://zhuanlan.zhihu.com/p/343553001) · 知乎 · 2021-01-11 · 赞同 1**
> 力扣：[808. 分汤](https://leetcode.cn/problems/soup-servings/) · Medium · 灵茶山艾府：[概率 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

808.分汤

[力扣](https://leetcode-cn.com/problems/soup-servings/)

感觉应该有组合数学的方法，不过这里是四项式，应该也没有四项式定理这种东西存在。相比之下，动态规划的做法是很容易想到的。令f[i][j]表示从A类有i毫升，B类有j毫升开始分汤，最终要求的概率是多少。注意到每次操作都是25ml的倍数，那么可以将N除上25向上取整，同时将四种操作分别变为A4、A3B1、A2B2以及A1B3。

那么对于f[i][j]：

1、若i \<\= 0，j \<\= 0：

此时为0.5

2、若i \<\= 0，j > 0：

此时为1

3、若i > 0，j \<\= 0：

此时为0

4、若i > 0，j > 0：

由于四种分法的概率相等，那么就有

f[i][j] \= 0.25 \* (f[i - 4][j] + f[i - 3][j - 1] + f[i - 2][j - 2] + f[i - 1][j - 3])

这样做有一个问题就是N的范围太大了，这种平方的做法肯定是跑不出结果的。不过有意思的是，在写完动态规划，测试N\=5000的时候，发现答案就是1，还一度以为代码写的有问题。简单分析一下可以得知由于四种操作都是等概率的，那么A先分完的概率应该是高于B的，那么在若干轮之后这个答案就一定是1了。不太确定这里的若干轮具体是多少，不过这个5000就可以作为一个可行的边界。当N>\=5000时，直接返回1，否则老老实实做动态规划，此时的时间复杂度也就(5000/25)^2，完全可以接受。

最后附上python代码：

```python
class Solution(object):
    def soupServings(self, N):
        """
        :type N: int
        :rtype: float
        """

        if N >= 5000:
            return 1.0
        
        if N % 25 == 0:
            N = N / 25
        else:
            N = N / 25 + 1
        f = [[None] * (N + 1) for _ in range(N + 1)]
        return self.dfs(N, N, f)

    def dfs(self, A, B, f):
        if A <= 0:
            if B <= 0:
                return 0.5
            else:
                return 1.0
        elif B <= 0:
            return 0.0
        
        if f[A][B] is None:
            f[A][B] = 0.25 * (self.dfs(A - 4, B, f) + self.dfs(A - 3, B - 1, f) + self.dfs(A - 2, B - 2, f) + self.dfs(A - 1, B - 3, f))
            
        return f[A][B]
```
