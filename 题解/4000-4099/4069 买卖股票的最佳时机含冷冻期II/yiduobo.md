---
title: "4069. 买卖股票的最佳时机含冷冻期II"
aliases: ["yiduobo的每日leetcode 4069.买卖股票的最佳时机含冷冻期II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2090597554417317832"
zhihu_id: "2090597554417317832"
zhihu_title: "yiduobo的每日leetcode 4069.买卖股票的最佳时机含冷冻期II"
question_id: "4069"
question: "买卖股票的最佳时机含冷冻期II"
problem_url: "https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-cooldown-ii/"
created: "2026-10-06T00:58:09+08:00"
updated: "2026-10-06T00:58:14+08:00"
upvotes: 0
comments: 0
---

# 4069. 买卖股票的最佳时机含冷冻期II

> **[yiduobo的每日leetcode 4069.买卖股票的最佳时机含冷冻期II](https://zhuanlan.zhihu.com/p/2090597554417317832) · 知乎 · 2026-10-06 · 赞同 0**
> 力扣：[4069. 买卖股票的最佳时机含冷冻期II](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-cooldown-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4069.买卖股票的最佳时机含冷冻期II

<https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-cooldown-ii/description/>

题目给出一个长度为n的整数数组prices，n不超过1500，其中prices[index]表示第index天的股票价格。

同时给出一个整数cooldown以及一个长度为n的整数数组costs，其中costs[k]表示一笔股票恰好持有k天时需要支付的总持有费用。

现在可以进行任意次数的交易，也可以不进行任何交易，但需要满足一下规则：

- 任意时刻最多只能持有一支股票，在再次买入之前，必须先卖出当前持有的股票
- 如果在buy_day这一天卖出股票，那么最早可以在第buy_day + cooldown + 1这一天重新买入股票
- 如果在第buy_day这一天买入股票，并在sell_day这一天卖出，那么持有时长就是sell_day - buy_day天，需要为这笔交易支付手续费costs[sell_day - buy_day]。换言之，这笔交易的利润为prices[sell_day] - prices[buy_day] - costs[sell_day - buy_day]

要求计算可以获得的最大总利润。若不存在任何值得进行的交易，则返回0。

经典股票题的又一个变形。对于本题，由于购买股票与上一次卖出股票的时间之间存在冷却，因此在这里可以考虑使用f[index]表示在第index天没有持有股票时可能得到的最大收益，那么首先就有边界情况f[0] \= 0，接下来对于index > 0的f[index]：

1、首先自然有f[index] \= f[index - 1]，表示维持前一天的状态。

2、另外就是在index这一天把手头的股票卖掉了，因此在这里需要从index - 1开始向前枚举买入的日期buy_day。更进一步的，由于冷却时间，那么如果buy_day可以买入股票，上一次清仓的日子pre_day最晚就是buy_day - cooldown - 1。

若pre_day \<\= 0，说明之前无法进行任何交易，否则就说明在此之前可以进行一些交易，可以获得的最大收益就是f[pre_day]。方便起见，记在最后这次交易之前可以获得的最大收益为pre，那么在这里就可以用pre + prices[index - 1] - prices[buy_day - 1] - costs[index - buy_day]来更新f[index]。

最后附上python代码：

```python
class Solution(object):
    def maxProfit(self, prices, cooldown, costs):
        """
        :type prices: List[int]
        :type cooldown: int
        :type costs: List[int]
        :rtype: int
        """
        
        f = [0]
        for index in range(1, len(prices) + 1):
            f.append(f[-1])
            for buy_day in range(index - 1, 0, -1):
                pre_day = buy_day - cooldown - 1
                if pre_day <= 0:
                    pre = 0
                else:
                    pre = f[pre_day]
                
                f[-1] = max(f[-1], pre + prices[index - 1] - prices[buy_day - 1] - costs[index - buy_day])
        
        return f[-1]
```
