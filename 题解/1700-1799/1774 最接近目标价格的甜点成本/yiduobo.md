---
title: "1774. 最接近目标价格的甜点成本"
aliases: ["yiduobo的每日leetcode 1774.最接近目标价格的甜点成本"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/461879609"
zhihu_id: "461879609"
zhihu_title: "yiduobo的每日leetcode 1774.最接近目标价格的甜点成本"
question_id: "1774"
question: "最接近目标价格的甜点成本"
problem_url: "https://leetcode.cn/problems/closest-dessert-cost/"
created: "2022-01-25T23:20:04+08:00"
updated: "2022-01-25T23:20:04+08:00"
upvotes: 0
comments: 0
---

# 1774. 最接近目标价格的甜点成本

> **[yiduobo的每日leetcode 1774.最接近目标价格的甜点成本](https://zhuanlan.zhihu.com/p/461879609) · 知乎 · 2022-01-25 · 赞同 0**
> 力扣：[1774. 最接近目标价格的甜点成本](https://leetcode.cn/problems/closest-dessert-cost/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1774.最接近目标价格的甜点成本

[力扣](https://leetcode-cn.com/problems/closest-dessert-cost/)

题目要求选出一种底座和若干种配料，使得这些东西的成本最接近目标值。

由于底座只能选择一种，那么自然是想到枚举底座，那么问题就变成了如何搭配配料使得这些配料的成本之和最接近目标值减去底座的成本。这是一个非常典型的背包问题，直接使用经典的f[i]表示能否通过组合配料使得成本为i进行动态规划就行了。

需要注意的有两个地方。

第一个是每种配料最多只能用两次。关于这一点可以在倒序枚举i的时候对使用一次还是使用两次的情况分别进行判断。由于是倒序枚举，因此不会出现在前一次基础上使用相同配料的情况。

第二个是枚举的上限。由于这里的最接近可以超过目标值，那么枚举的上限就应该是目标值target加上成本最高的配料max(cost)，然后再减去一。

动态规划完成后，枚举每种底座，从新的目标值开始分别向上和向下找到第一个f为true的位置，然后对比这两个下标距离新目标值的距离，取较小值更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def closestCost(self, baseCosts, toppingCosts, target):
        """
        :type baseCosts: List[int]
        :type toppingCosts: List[int]
        :type target: int
        :rtype: int
        """

        upperLimit = target + max(toppingCosts) - 1
        f = [False] * (upperLimit + 1)
        f[0] = True
        m = len(toppingCosts)
        for i in range(m):
            for j in range(upperLimit, toppingCosts[i] + toppingCosts[i] - 1, -1):
                if f[j - toppingCosts[i] - toppingCosts[i]] or f[j - toppingCosts[i]]:
                    f[j] = True
            for j in range(min(upperLimit, toppingCosts[i] + toppingCosts[i] - 1), toppingCosts[i] - 1, -1):
                if f[j - toppingCosts[i]]:
                    f[j] = True
                    
        res = baseCosts[0]
        for baseCost in baseCosts:
            if baseCost > target:
                if baseCost - target < abs(res - target):
                    res = baseCost
            else:
                lowerTarget = target - baseCost
                while lowerTarget > 0 and not f[lowerTarget]:
                    lowerTarget -= 1
                
                if target - baseCost - lowerTarget <= abs(res - target):
                    res = baseCost + lowerTarget
                
                upperTarget = target - baseCost
                while upperTarget <= upperLimit and not f[upperTarget]:
                    upperTarget += 1
                
                if upperTarget <= upperLimit and baseCost + upperTarget - target < abs(res - target):
                    res = baseCost + upperTarget
            
        return res
```
