---
title: "123. 买卖股票的最佳时机III"
aliases: ["yiduobo的每日leetcode 123.买卖股票的最佳时机III"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "题单/动态规划", "题单/面试经典-150-题", "题单/动态规划/六-状态机-DP", "题单/动态规划/专题-前后缀分解", "题单/面试经典-150-题/多维动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/139790696"
zhihu_id: "139790696"
zhihu_title: "yiduobo的每日leetcode 123.买卖股票的最佳时机III"
question_id: "123"
question: "买卖股票的最佳时机 III"
problem_url: "https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iii/"
difficulty: "Hard"
created: "2020-05-11T23:18:26+08:00"
updated: "2020-05-11T23:18:26+08:00"
upvotes: 0
comments: 0
---

# 123. 买卖股票的最佳时机III

> **[yiduobo的每日leetcode 123.买卖股票的最佳时机III](https://zhuanlan.zhihu.com/p/139790696) · 知乎 · 2020-05-11 · 赞同 0**
> 力扣：[123. 买卖股票的最佳时机 III](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iii/) · Hard · 灵茶山艾府：[188 题 k=2 的情况（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

123.买卖股票的最佳时机III<https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-iii/submissions/>

上一题的进一步升级版。这里限定了只能进行两次买卖，因此要继续使用贪心法的话似乎就有点复杂了，我在这里选择老老实实写动态规划。

首先状态f[i][j]表示前i天，第j种状态时的最佳收益是多少。这里的j取值为0到4，分别对应：

1、j \= 0，表示刚进行了第一次买进。

2、j \= 1，表示刚进行了第一次卖出。

3、j \= 2，表示刚进行了第二次买进。

4、j \= 3，表示刚进行了第二次卖出。

最后的结果就是max(0, f[n][1], f[n][3])，即最后一天买卖了一次或者买卖了两次中的较大值。

接下来，分别考虑f[i][j]的各个状态。

首先是j \= 0的情况。

当i \= 0时，表示第一天，那么按第一天的价格买进，即f[i][j] \= -prices[i]。

当i不为0时，我们可以对比前面日子里的最优价格以及今天的价格，即f[i][j] \= max(f[i - 1][j], -prices[i])

接下来是j \= 1的情况。

首先需要明确，所有j \= 1的情况都应该是从j \= 0的情况转移过来的，很好理解，先要有第一次的买进才有第一次的卖出。于是，当f[i - 1][0]不存在时，无法计算f[i][j]。

对于f[i][j]，我们可以考虑在今天进行卖出，或者是在之前的某一天就已经卖出，于是有

f[i][j] \= max(f[i - 1][j], f[i - 1][0] + prices[i])

再往后是j \= 2与j \= 3的情况。

与j \= 1的情况类似，也是需要通过前置状态转移过来，因此需要对于j \= 2与j \= 3的而言，分别需要f[i - 1][1]与f[i - 1][2]存在才能计算f[i][j]。

买入卖出也还是今天进行操作或者之前就已经进行过操作这两种情况，因此与上面的做法类似

f[i][2] \= max(f[i - 1][2], f[i - 1][1] - prices[i])

f[i][3] \= max(f[i - 1][3], f[i - 1][2] + prices[i])

在这里我们可以发现，之后对于买卖k次的情况，做法也是相同的，设置k \* 2个状态分别代表买进与卖出，然后在这之间进行状态转移即可。

---

另外，注意到每天的4种状态都只于前一天的4种状态有关，于是可以利用滚动数组。在这里就只需要维护4个变量buy_one、sell_one、buy_two、sell_two，分别代表到今天为止买入一次，卖出一次，买入两次，卖出两次所能得到的最大收益。需要特别注意的是，在更新的过程中需要按

sell_two -> buy_two -> sell_one -> buy_one

这个顺序进行更新。这里也很好理解，例如我们在更新今天的sell_two时，会依赖到昨天的buy_two。但是如果这里先更新过了buy_two，那么buy_two就是今天的buy_two，昨天的buy_two就丢失掉了，无法再正确得到sell_two了。

最后附上python代码：

```python
class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """

        if not prices:
            return 0

        buy_one = -prices[0]
        buy_two = sell_one = sell_two = None

        for i in range(1, len(prices)):
            if buy_two is not None:
                if sell_two is None or sell_two < buy_two + prices[i]:
                    sell_two = buy_two + prices[i]

            if sell_one is not None:
                if buy_two is None or buy_two < sell_one - prices[i]:
                    buy_two = sell_one - prices[i]

            if sell_one is None or sell_one < buy_one + prices[i]:
                sell_one = buy_one + prices[i]

            buy_one = max(buy_one, -prices[i])

        if sell_one is None: sell_one = -1
        if sell_two is None: sell_two = -1
        return max(0, sell_one, sell_two)
```
