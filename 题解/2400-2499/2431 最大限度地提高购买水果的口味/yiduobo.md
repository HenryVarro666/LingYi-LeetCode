---
title: "2431. 最大限度地提高购买水果的口味"
aliases: ["yiduobo的每日leetcode 2431.最大限度地提高购买水果的口味"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/631415096"
zhihu_id: "631415096"
zhihu_title: "yiduobo的每日leetcode 2431.最大限度地提高购买水果的口味"
question_id: "2431"
question: "最大限度地提高购买水果的口味"
problem_url: "https://leetcode.cn/problems/maximize-total-tastiness-of-purchased-fruits/"
created: "2023-05-23T02:53:24+08:00"
updated: "2023-05-23T02:53:24+08:00"
upvotes: 0
comments: 0
---

# 2431. 最大限度地提高购买水果的口味

> **[yiduobo的每日leetcode 2431.最大限度地提高购买水果的口味](https://zhuanlan.zhihu.com/p/631415096) · 知乎 · 2023-05-23 · 赞同 0**
> 力扣：[2431. 最大限度地提高购买水果的口味](https://leetcode.cn/problems/maximize-total-tastiness-of-purchased-fruits/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2431.最大限度地提高购买水果的口味

[力扣](https://leetcode.cn/problems/maximize-total-tastiness-of-purchased-fruits/)

背包问题的变种。如果不考虑优惠券的情况，那么就是常规的f[k][i]表示前k种水果糖，使用i的代价最多可以买到的水果味道是多少。而对于优惠券，最直观的处理方法就是令f[k][i][j]表示前k种水果糖，使用i的代价以及j次优惠券最多可以买到的水果味道是多少。

那么对于f[k][i][j]，考虑第k种水果糖的选取：

1、若不适用优惠券，那么当i >\= price[k - 1]时，就有

f\[k\]\[i\]\[j\] \= max(f\[k\]\[i\]\[j\], f\[k - 1\]\[i - price\[k - 1\]\]\[j\] + tastiness\[k - 1\])

2、若使用优惠券，那么当i >\= price[k - 1] / 2，且j > 0时，就有

f[k][i][j] \= max(f[k][i][j], f[k - 1][i - price[k - 1] / 2][j - 1] + tastiness[k - 1])

而最终答案则为max(f[n][maxAmount])。

注意到这里的每一轮状态只与上一轮有关，那么可以利用倒序执行原地状态转移来省去k这一维。

最后附上python代码：

```python
class Solution(object):
    def maxTastiness(self, price, tastiness, maxAmount, maxCoupons):
        """
        :type price: List[int]
        :type tastiness: List[int]
        :type maxAmount: int
        :type maxCoupons: int
        :rtype: int
        """

        f = [[0] * (maxCoupons + 1) for _ in range(maxAmount + 1)]
        for p, t in zip(price, tastiness):
            for j in range(maxCoupons, -1, -1):
                mi = p
                if j > 0:
                    mi /= 2
                
                for i in range(maxAmount, mi - 1, -1):
                    if i >= p:
                        f[i][j] = max(f[i - p][j] + t, f[i][j])
                    if j > 0:
                        f[i][j] = max(f[i - p / 2][j - 1] + t, f[i][j])

        return max(f[-1])
```
