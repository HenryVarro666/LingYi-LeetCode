---
title: "3946. 购买最多物品数目I"
aliases: ["yiduobo的每日leetcode 3946.购买最多物品数目I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/三-背包"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2044522161621225758"
zhihu_id: "2044522161621225758"
zhihu_title: "yiduobo的每日leetcode 3946.购买最多物品数目I"
question_id: "3946"
question: "购买最多物品数目 I"
problem_url: "https://leetcode.cn/problems/maximum-number-of-items-from-sale-i/"
difficulty: "Medium"
rating: 1728
created: "2026-05-31T21:15:34+08:00"
updated: "2026-05-31T21:15:35+08:00"
upvotes: 2
comments: 0
---

# 3946. 购买最多物品数目I

> **[yiduobo的每日leetcode 3946.购买最多物品数目I](https://zhuanlan.zhihu.com/p/2044522161621225758) · 知乎 · 2026-05-31 · 赞同 2**
> 力扣：[3946. 购买最多物品数目 I](https://leetcode.cn/problems/maximum-number-of-items-from-sale-i/) · Medium · 灵茶山艾府：[0-1 背包 + 枚举优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3946.购买最多物品数目I

<https://leetcode.cn/problems/maximum-number-of-items-from-sale-i/description/>

题目给出一个二维整数数组items，其中items\[i\] \= \[factor\[i\], price\[i\]\]，表示下标为i的物品。另外给出一个整数budget。

每种物品都有无限量供应，现在需要购买一些物品，这些物品的总花费不能超过budget。

购买物品后，可以根据一下规则获取免费的物品：

- 若购买了物品i，那么所有满足j !\= i，且factor[i]可以整除factor[j]的物品j都可以免费获得一份
- 重复购买物品i，不能再次获得上述的免费物品
- 若免费物品j是通过购买不同种类的物品获得的，那么同一种物品j可以被免费获得多次

问总花销不超过budget的前提下，可能获得的最大物品总数是多少，包括买的以及免费获得的。

首先，由于多次购买同一个物品并不能多次获取赠品，因此冲着赠品去的购物对每种物品只会执行最多一次。对于这一类购买，相当于花原来的价格，买到了1个原品加上若干的赠品。在不超过总花费budget的前提下使得买到的物品数量最多，是一个非常经典的01背包问题，可以使用动态规划解决。

另外，在这里可以利用倒序遍历，仅保留动态规划的状态表示中budget这个维度，即f[v]表示花费不超过v时可以买到的最多物品数量，那么对于每个物品，先遍历其他的所有物品，通过对应的factor计算购买当前物品可以获得总物品数cnt，然后从budget开始倒序遍历到当前物品的价格p，对于当前遍历到的v，使用f[v - p] + cnt来更新f[v]即可。

而对于没有赠品获取的购物，由于题目要求的是总数最多，因此这个部分就应该只选择最便宜的那种物品，需要注意这里是可以购买多次的，因此只需在之前动态规划的基础上改为正序遍历，仅考虑多次购买这种最便宜的物品就行了。

最后附上python代码：

```python
class Solution(object):
    def maximumSaleItems(self, items, budget):
        """
        :type items: List[List[int]]
        :type budget: int
        :rtype: int
        """
        
        f = [0] * (budget + 1)
        mi_p = None
        for i in range(len(items)):
            cnt = 1
            for j in range(len(items)):
                if i != j and items[j][0] % items[i][0] == 0:
                    cnt += 1

            for v in range(budget, items[i][1] - 1, -1):
                f[v] = max(f[v - items[i][1]] + cnt, f[v])

            if mi_p is None or mi_p > items[i][1]:
                mi_p = items[i][1]

        for v in range(mi_p, budget + 1):
            f[v] = max(f[v - mi_p] + 1, f[v])
        
        return f[-1]
```
