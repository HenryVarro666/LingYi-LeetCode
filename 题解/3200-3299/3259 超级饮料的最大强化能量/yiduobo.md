---
title: "3259. 超级饮料的最大强化能量"
aliases: ["yiduobo的每日leetcode 3259.超级饮料的最大强化能量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/722193050"
zhihu_id: "722193050"
zhihu_title: "yiduobo的每日leetcode 3259.超级饮料的最大强化能量"
question_id: "3259"
question: "超级饮料的最大强化能量"
problem_url: "https://leetcode.cn/problems/maximum-energy-boost-from-two-drinks/"
difficulty: "Medium"
rating: 1484
created: "2024-09-26T02:23:24+08:00"
updated: "2024-09-26T02:23:24+08:00"
upvotes: 0
comments: 0
---

# 3259. 超级饮料的最大强化能量

> **[yiduobo的每日leetcode 3259.超级饮料的最大强化能量](https://zhuanlan.zhihu.com/p/722193050) · 知乎 · 2024-09-26 · 赞同 0**
> 力扣：[3259. 超级饮料的最大强化能量](https://leetcode.cn/problems/maximum-energy-boost-from-two-drinks/) · Medium · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3259.超级饮料的最大强化能力

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-energy-boost-from-two-drinks/description/)

题目给出两个长度为n的数组energyDrinkA和energyDrinkB，分别代表A和B两种不同的能量饮料每小时可以提供的强化能量。

接下来每小时需要引用一种饮料来强化体能，然而如果从一种饮料切换到另一种，之后的一小时无法获得任何能量。问如何引用才能使得n小时内获得的总能量最大。

经典的动态规划问题。令f[index]表示前index个小时，最后这个小时喝了饮料A时可以获得的最大能量值，而g[index]则表示前index个小时，最后这个小时喝了饮料B时可以获得的最大能量值。

那么对于f[index]：

1、首先是边界情况：

f[0] \= energyDrinkA[0]

2、接下来对于index > 0的情况：

如果倒数第二个小时喝的是A，那么就是f[index] \= f[index - 1] + energyDrinkA[index]，这种情况下本小时喝的饮料也可以发挥作用。

反之如果倒数第二个小时喝的是B，那么就是f[index] \= g[index - 1]，这种情况下本小时无法获得能量。

综合起来就是f[index] \= max(f[index - 1] + energyDrinkA[index], g[index - 1])

对于g[index]而言，则是与f[index]完全对称。当index \= 0时，有g[0] \= energyDrinkB[0]，当index > 0时，有g[index] \= max(g[index - 1] + energyDrinkB[index], f[index - 1])

另外注意到f和g每一轮都只与上一轮的f和g有关，因此可以通过变量迭代节省掉数组的空间。

最后附上python代码：

```python
class Solution(object):
    def maxEnergyBoost(self, energyDrinkA, energyDrinkB):
        """
        :type energyDrinkA: List[int]
        :type energyDrinkB: List[int]
        :rtype: int
        """

        f, g = energyDrinkA[0], energyDrinkB[0]

        for a, b in zip(energyDrinkA[1:], energyDrinkB[1:]):
            f, g = max(f + a, g), max(f, g + b)
        
        return max(f, g)
```
