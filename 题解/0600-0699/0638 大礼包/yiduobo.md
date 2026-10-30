---
title: "638. 大礼包"
aliases: ["yiduobo的每日leetcode 638.大礼包"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/272228080"
zhihu_id: "272228080"
zhihu_title: "yiduobo的每日leetcode 638.大礼包"
question_id: "638"
question: "大礼包"
problem_url: "https://leetcode.cn/problems/shopping-offers/"
created: "2020-11-02T23:03:40+08:00"
updated: "2020-11-02T23:03:40+08:00"
upvotes: 0
comments: 0
---

# 638. 大礼包

> **[yiduobo的每日leetcode 638.大礼包](https://zhuanlan.zhihu.com/p/272228080) · 知乎 · 2020-11-02 · 赞同 0**
> 力扣：[638. 大礼包](https://leetcode.cn/problems/shopping-offers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

638.大礼包

[力扣](https://leetcode-cn.com/problems/shopping-offers/)

典型的背包问题，不过这里的状态维度很多，我选择的就是强行做一个7维的动态规划，用记忆化搜索加dict的方式应该会优美一些。

状态f[y0][y1][y2][y3][y4][y5]表示这六样商品分别有y0、y1、y2、y3、y4、y5件最少要多少钱，然后枚举每个单个商品或者礼包进行状态转移。

最后附上python代码：

```python
class Solution(object):
    def shoppingOffers(self, price, special, needs):
        """
        :type price: List[int]
        :type special: List[List[int]]
        :type needs: List[int]
        :rtype: int
        """

        needs = needs + [0] * (6 - len(needs))
        case = []
        cost = []
        for index in range(len(price)):
            tmp = [0] * 6
            tmp[index] = 1
            case.append(tmp)
            cost.append(price[index])
        for index in range(len(special)):
            cost.append(special[index][-1])
            tmp = special[index][:-1]
            tmp += [0] * (6 - len(tmp))
            case.append(tmp)

        f = [[[[[[None] * 7 for _ in range(7)] for _ in range(7)] for _ in range(7)] for _ in range(7)] for _ in range(7)]
        f[0][0][0][0][0][0] = 0
        for index in range(len(case)):
            x0, x1, x2, x3, x4, x5 = case[index]
            for y0 in range(x0, needs[0] + 1):
                for y1 in range(x1, needs[1] + 1):
                    for y2 in range(x2, needs[2] + 1):
                        for y3 in range(x3, needs[3] + 1):
                            for y4 in range(x4, needs[4] + 1):
                                for y5 in range(x5, needs[5] + 1):
                                    if f[y0 - x0][y1 - x1][y2 - x2][y3 - x3][y4 - x4][y5 - x5] is not None:
                                        tmp = f[y0 - x0][y1 - x1][y2 - x2][y3 - x3][y4 - x4][y5 - x5] + cost[index]
                                        if f[y0][y1][y2][y3][y4][y5] is None or f[y0][y1][y2][y3][y4][y5] > tmp:
                                            f[y0][y1][y2][y3][y4][y5] = tmp

        return f[needs[0]][needs[1]][needs[2]][needs[3]][needs[4]][needs[5]]
```
