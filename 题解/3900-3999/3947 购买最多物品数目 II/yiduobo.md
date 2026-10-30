---
title: "3947. 购买最多物品数目II"
aliases: ["yiduobo的每日leetcode 3947.购买最多物品数目II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2044527863207089148"
zhihu_id: "2044527863207089148"
zhihu_title: "yiduobo的每日leetcode 3947.购买最多物品数目II"
question_id: "3947"
question: "购买最多物品数目 II"
problem_url: "https://leetcode.cn/problems/maximum-number-of-items-from-sale-ii/"
difficulty: "Medium"
rating: 2215
created: "2026-05-31T21:41:13+08:00"
updated: "2026-05-31T21:41:13+08:00"
upvotes: 1
comments: 0
---

# 3947. 购买最多物品数目II

> **[yiduobo的每日leetcode 3947.购买最多物品数目II](https://zhuanlan.zhihu.com/p/2044527863207089148) · 知乎 · 2026-05-31 · 赞同 1**
> 力扣：[3947. 购买最多物品数目 II](https://leetcode.cn/problems/maximum-number-of-items-from-sale-ii/) · Medium · 灵茶山艾府：[贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3947.购买最多物品数目II

<https://leetcode.cn/problems/maximum-number-of-items-from-sale-ii/description/>

题目给出一个二维整数数组items，其中items\[i\] \= \[factor\[i\], price\[i\]\]，表示下标为i的物品。另外给出一个整数budget。

每种物品都有无限量供应，现在需要购买一些物品，这些物品的总花费不能超过budget。

购买物品后，可以根据一下规则获取免费的物品：

- 购买的每一份物品i，都最多只能获得一份免费的其他物品j，前提是满足j !\= i，且factor[i]可以整除factor[j]
- 对于每个有序对(i, j)，无论购买了i多少次，都最多只能获得一份免费的j
- 若免费物品j是通过购买不同种类的物品获得的，那么同一种物品j可以被免费获得多次

问总花销不超过budget的前提下，可能获得的最大物品总数是多少，包括买的以及免费获得的。

需要注意，本题和上一题关于赠品的获取条件略有不同。具体来说，对于某个物品，不妨设有cnt件其他物品的factor是当前物品的倍数，那么在前cnt次购买当前物品时，都可以享受买一送一，而超出cnt件的部分则不再享受优惠。

另外可以明确的是，所有超出对应cnt的购买都应该选择买最便宜的那一种物品，方便期间，记其价格为mi_p。更进一步的，对于买一送一的部分，其花费必须小于mi_p \* 2才有购买的价值，否则的话购买两份最便宜的mi_p显然是更优的。

基于上面的结论，就可以将所有价格小于mi_p \* 2的物品价格以及其对应的cnt收集起来，形成数组candidate，然后按照价格从小到大进行排序。接下来在进行购买时，就应该按照价格顺序进行购买。当处理完candidate后，对于budget剩下的部分，则全部用来购买mi_p对应的物品。

最后附上python代码：

```python
class Solution(object):
    def maximumSaleItems(self, items, budget):
        """
        :type items: List[List[int]]
        :type budget: int
        :rtype: int
        """
        
        freq = {}
        mi_p = None
        ma_f = 0
        for f, p in items:
            freq[f] = freq.get(f, 0) + 1
            if mi_p is None or mi_p > p:
                mi_p = p
            ma_f = max(ma_f, f)
        
        cnt = {}
        for f in range(1, ma_f + 1):
            cnt[f] = 0
            for x in range(f, ma_f + 1, f):
                cnt[f] += freq.get(x, 0)

        candidates = []
        for f, p in items:
            if p < mi_p * 2 and cnt[f] > 1:
                candidates.append((p, cnt[f] - 1))

        candidates.sort()
        res = 0
        for p, c in candidates:
            if budget >= p * c:
                budget -= p * c
                res += c * 2
            else:
                res += budget // p * 2
                budget %= p
        
        return res + budget // mi_p
```
