---
title: "2412. 完成所有交易的初始最少钱数"
aliases: ["yiduobo的每日leetcode 2412.完成所有交易的初始最少钱数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/568840276"
zhihu_id: "568840276"
zhihu_title: "yiduobo的每日leetcode 2412.完成所有交易的初始最少钱数"
question_id: "2412"
question: "完成所有交易的初始最少钱数"
problem_url: "https://leetcode.cn/problems/minimum-money-required-before-transactions/"
difficulty: "Hard"
rating: 2092
created: "2022-09-28T02:26:33+08:00"
updated: "2022-09-28T02:26:33+08:00"
upvotes: 0
comments: 0
---

# 2412. 完成所有交易的初始最少钱数

> **[yiduobo的每日leetcode 2412.完成所有交易的初始最少钱数](https://zhuanlan.zhihu.com/p/568840276) · 知乎 · 2022-09-28 · 赞同 0**
> 力扣：[2412. 完成所有交易的初始最少钱数](https://leetcode.cn/problems/minimum-money-required-before-transactions/) · Hard · 灵茶山艾府：[贪心 + 一次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2412.完成所有交易的初始最少钱数

[力扣](https://leetcode.cn/problems/minimum-money-required-before-transactions/)

题目要找的是最坏情况下都能完成所有交易的最少钱数，那么最直观的最坏情况就先把赔钱的买卖都干了，然后接下来马上干赚钱买卖中cost最大的那一个。不过观察题目中的样例一可以发现，可能出现没有赚钱买卖的情况。更进一步的，也可能出现赔钱买卖搞到最后被最后一个赔钱买卖卡住的情况。

其中，赔钱买卖干完然后干赚钱买卖中cost最大的那一个这种情况比较好计算的，需要的初始资金就是所有赔钱买卖赔掉的钱，再加上赚钱买卖中最大的cost。

相对于，被最后一个赔钱买卖卡住的情况则不能简单选择cost最大的赔钱买卖作为最后一个，因为这个买卖可能还赚回来了一些钱，那么在这里就需要枚举所有的赔钱买卖，看看让哪个买卖放在最后是最差的情况。

设所有赔钱买卖一共会赔掉neg_sum的钱，那么对于某个赔钱买卖(cost, callback)，在进行这个买卖之前赔掉的钱就是neg_sum - (cost - callback)，因此能进行这个买卖的最少初始钱数就是neg_sum - (cost - callback) + cost，化简后就是neg_sum + callback。换言之，最差的情况就是赔钱买卖中callback最大的那一个在最后一个进行。

综合上面两种情况，那么只需一趟遍历，对于当前买卖，如果是赔钱买卖，那么就将赔的金额更新到neg_sum中，同时使用当前买卖的callback更新最大的赔钱callback。反之，如果是赚钱买卖，那么就使用当前买卖的cost更新最大的赚钱cost。

遍历完成后，最大的赔钱callback和最大的赚钱cost中的较大值，再加上neg_sum就是最终答案了。

最后附上python代码：

```python
class Solution(object):
    def minimumMoney(self, transactions):
        """
        :type transactions: List[List[int]]
        :rtype: int
        """

        neg_sum = 0
        max_pos = 0
        max_callback = 0
        for cost, callback in transactions:
            if cost > callback:
                neg_sum += cost - callback
                max_callback = max(max_callback, callback)
            else:
                max_pos = max(max_pos, cost)
        
        return neg_sum + max(max_callback, max_pos)
```
