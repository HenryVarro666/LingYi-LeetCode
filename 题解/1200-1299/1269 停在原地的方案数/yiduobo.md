---
title: "1269. 停在原地的方案数"
aliases: ["yiduobo的每日leetcode 1269.停在原地的方案数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/387607310"
zhihu_id: "387607310"
zhihu_title: "yiduobo的每日leetcode 1269.停在原地的方案数"
question_id: "1269"
question: "停在原地的方案数"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-stay-in-the-same-place-after-some-steps/"
created: "2021-07-07T22:12:09+08:00"
updated: "2021-07-07T22:12:09+08:00"
upvotes: 1
comments: 0
---

# 1269. 停在原地的方案数

> **[yiduobo的每日leetcode 1269.停在原地的方案数](https://zhuanlan.zhihu.com/p/387607310) · 知乎 · 2021-07-07 · 赞同 1**
> 力扣：[1269. 停在原地的方案数](https://leetcode.cn/problems/number-of-ways-to-stay-in-the-same-place-after-some-steps/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1269.停在原地的方案数

[力扣](https://leetcode-cn.com/problems/number-of-ways-to-stay-in-the-same-place-after-some-steps/)

看上去应该可以用组合数学的知识来做，但是没有想出做法，只能老老实实用动态规划来做。

令f[i][j]表示走i步，最后停在位置j的方案数。初始情况下f[0][0] \= 1，其他f[0][k] \= 0。

对于f[i][j]，首先初始f[i][j]为0，接下来有两种情况：

1、若j大于0，那么可以从上一轮的j - 1这个位置走过来，于是有

f[i][j] +\= f[i - 1][j - 1]

2、若j小于n - 1，那么可以从上一轮的j + 1这个位置走过来，于是有

f[i][j] +\= f[i - 1][j + 1]

注意到这里每一轮的状态只与上一轮有关，那么可以使用滚动数组来进行优化。

另外，这里看上去也可以用矩阵乘法，但是矩阵的大小达到了O(n)的规模，因此这里矩阵乘法的复杂度太高，不适合在这里使用。

最后附上python代码：

```python
class Solution(object):
    def numWays(self, steps, arrLen):
        """
        :type steps: int
        :type arrLen: int
        :rtype: int
        """

        if arrLen > steps / 2 + 1:
            arrLen = steps / 2 + 1
        
        f = [0] * arrLen
        g = [0] * arrLen
        f[0] = 1
        mod = 10 ** 9 + 7
        for i in range(1, steps + 1):
            for j in range(arrLen):
                g[j] = f[j]
                if j > 0:
                    g[j] += f[j - 1]
                    g[j] %= mod
                if j < arrLen - 1:
                    g[j] += f[j + 1]
                    g[j] %= mod

            f = g[:]

        return f[0]
```
