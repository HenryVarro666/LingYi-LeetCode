---
title: "879. 盈利计划"
aliases: ["yiduobo的每日leetcode 879.盈利计划"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/350657867"
zhihu_id: "350657867"
zhihu_title: "yiduobo的每日leetcode 879.盈利计划"
question_id: "879"
question: "盈利计划"
problem_url: "https://leetcode.cn/problems/profitable-schemes/"
created: "2021-02-17T00:19:48+08:00"
updated: "2021-02-17T00:19:48+08:00"
upvotes: 1
comments: 0
---

# 879. 盈利计划

> **[yiduobo的每日leetcode 879.盈利计划](https://zhuanlan.zhihu.com/p/350657867) · 知乎 · 2021-02-17 · 赞同 1**
> 力扣：[879. 盈利计划](https://leetcode.cn/problems/profitable-schemes/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

879.盈利计划

[力扣](https://leetcode-cn.com/problems/profitable-schemes/)

经典的背包问题，使用动态规划来解决。令f[k][i][j]表示前k中工作，一共有多少种组合方式满足使用i的代价达成j的收益。

首先，如果不选择第k种工作，那么就有f[k][i][j] \= f[k - 1][i][j]

接下考虑选择第k种工作的情况。这里收益的上限为minProfit，因此状态转移时需要对此进行讨论:

若j + profit[k] >\= minProfit，那么有

f\[k\]\[i+group\[k\]\]\[minProfit\] +\= f\[k - 1\]\[i\]\[j\]

否则就是

f\[k\]\[i+group\[k\]\]\[j+profit\[k\]\] +\= f\[k - 1\]\[i\]\[j\]

注意到这里的状态转移只与上一轮的状态有关，因此可以省去k这一维。

最后附上python代码：

```python
class Solution(object):
    def profitableSchemes(self, n, minProfit, group, profit):
        """
        :type n: int
        :type minProfit: int
        :type group: List[int]
        :type profit: List[int]
        :rtype: int
        """

        m = len(group)
        f = [[0] * (minProfit + 1) for _ in range(n + 1)]
        f[0][0] = 1
        mod = 10**9 + 7
        for cost, w in zip(group, profit):
            for i in range(n - cost, -1, -1):
                for j in range(minProfit, -1, -1):
                    if j + w >= minProfit:
                        f[i + cost][minProfit] = (f[i + cost][minProfit] + f[i][j]) % mod
                    else:
                        f[i + cost][j + w] = (f[i + cost][j + w] + f[i][j]) % mod
        
        res = 0
        for i in range(n + 1):
            res = (res + f[i][-1]) % mod
        return res
```
