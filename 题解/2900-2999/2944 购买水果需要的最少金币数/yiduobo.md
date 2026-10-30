---
title: "2944. 购买水果需要的最少金币数"
aliases: ["yiduobo的每日leetcode 2944.购买水果需要的最少金币数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/monotonic-queue", "题单/动态规划", "题单/动态规划/七-其他线性-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/691605733"
zhihu_id: "691605733"
zhihu_title: "yiduobo的每日leetcode 2944.购买水果需要的最少金币数"
question_id: "2944"
question: "购买水果需要的最少金币数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-coins-for-fruits/"
difficulty: "Medium"
rating: 1709
created: "2024-04-10T00:26:50+08:00"
updated: "2024-04-10T00:26:50+08:00"
upvotes: 1
comments: 0
---

# 2944. 购买水果需要的最少金币数

> **[yiduobo的每日leetcode 2944.购买水果需要的最少金币数](https://zhuanlan.zhihu.com/p/691605733) · 知乎 · 2024-04-10 · 赞同 1**
> 力扣：[2944. 购买水果需要的最少金币数](https://leetcode.cn/problems/minimum-number-of-coins-for-fruits/) · Medium · 灵茶山艾府：[动态规划：从 O(n^2) 到 O(n)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2944.购买水果需要的最少金币数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-number-of-coins-for-fruits/description/)

题目给出一个价格数组price，可以通过price[i]购买第i到第i + i这一段水果，问购买所有水果的最少代价。

这是非常经典的动态规划问题，不过本题是用过代价price[i]购买i为起点的区间，看着有点别扭，不妨将price倒转过来，那么问题就变成了price[i]购买第(i - 1) - (n - i + 1) + 1到i这一段水果，问购买所有水果的最少代价。

令f[i]表示购买前i种水果的最小代价，那么对于f[i]，必须购买price[i]，而f[i]则可以从f[i - 1]到f[(i - 1) - (n - i + 1) + 1]中的最小值转移过来。全部计算完成后，最终答案就是f[n]。

最后附上python代码：

```python
class Solution(object):
    def minimumCoins(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """

        n = len(prices)
        free = n

        prices.reverse()
        f = [0]
        for i in range(n):
            mi = None
            for j in range(i, max(-1, i - free - 1), -1):
                if mi is None or mi > f[j]:
                    mi = f[j]
            f.append(mi + prices[i])
            free -= 1

        return f[-1]
```
