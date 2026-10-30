---
title: "3592. 硬币面值还原"
aliases: ["yiduobo的每日leetcode 3592.硬币面值还原"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/动态规划", "题单/贪心算法", "题单/动态规划/三-背包", "题单/贪心算法/六-构造题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1939841937302614673"
zhihu_id: "1939841937302614673"
zhihu_title: "yiduobo的每日leetcode 3592.硬币面值还原"
question_id: "3592"
question: "硬币面值还原"
problem_url: "https://leetcode.cn/problems/inverse-coin-change/"
difficulty: "Medium"
rating: 1701
created: "2025-08-16T00:23:05+08:00"
updated: "2025-08-16T00:23:05+08:00"
upvotes: 0
comments: 0
---

# 3592. 硬币面值还原

> **[yiduobo的每日leetcode 3592.硬币面值还原](https://zhuanlan.zhihu.com/p/1939841937302614673) · 知乎 · 2025-08-16 · 赞同 0**
> 力扣：[3592. 硬币面值还原](https://leetcode.cn/problems/inverse-coin-change/) · Medium · 灵茶山艾府：[完全背包：反向构造题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3592.硬币面值还原

[3592. 硬币面值还原 - 力扣（LeetCode）](https://leetcode.cn/problems/inverse-coin-change/)

题目给出一个从1开始计数的整数数组numWays，其中numWays[v]表示使用某些固定面值的硬币（每种硬币可以使用无限次）凑出总金额v的方案数。每种硬币的面值都是正整数，且不超过numWays的长度n。

然而，具体的硬币面值已经丢失，现在要求还原出可能生成这个numWays数组的面值集合，并按照面值从小到大返回。若不存在，则返回空数组。

首先可以明确的是，如果答案数组存在，那么numWays中最小的非零元素必须是1，因为必然存在一种面值最小的硬币p，使用一枚这种硬币刚好构成面值p。基于这一点，就可以从1开始向上遍历，找出第一个非零元素的下标p，若numWays[p]不为1，则直接返回空数组，否则就可以确定面值最小的硬币为p。

接下来，由于这个面值为p的硬币可以使用多次，因此可以组合成p、2p、3p、...这些面值。在这里可以使用一个数组f表示当前已经确定了面值的硬币可以组成的面值方案数，可以发现，这是一个非常标准的背包问题。由于可以使用多次，在这里可以直接正序遍历p到n，对于当前遍历到的v，使用f[v] +\= f[v - p]来更新f数组即可。

由于使用面值p已经可以构造f数组中对应的面值，那么接下来就应该从p + 1开始向后遍历，找出第一个numWays与f不同的下标p，若此时numWays[p]刚好比f[p]多1，那么说明下一种面值最小的硬币的面值就是p，否则无解。得到了新的硬币面值后，将其加入答案数组，然后按上面相同的方法更新f数组。

重复此过程，直到f数组与numWays完全相同，或者出现无解的情况为止。

最后附上python代码：

```python
class Solution(object):
    def findCoins(self, numWays):
        """
        :type numWays: List[int]
        :rtype: List[int]
        """
        
        n = len(numWays)
        f = [0] * (n + 1)
        f[0] = 1
        res = []

        p = 1
        while p <= n:
            while p <= n and numWays[p - 1] == f[p]:
                p += 1
            
            if p == n + 1:
                break
                
            if numWays[p - 1] - f[p] != 1:
                return []

            res.append(p)

            for v in range(p, n + 1):
                f[v] += f[v - p]

        return res
```
