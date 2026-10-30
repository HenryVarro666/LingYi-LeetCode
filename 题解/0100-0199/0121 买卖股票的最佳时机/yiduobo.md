---
title: "121. 买卖股票的最佳时机"
aliases: ["yiduobo的每日leetcode 121.买卖股票的最佳时机"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/bian-li", "题单/常用数据结构", "题单/动态规划", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/常用数据结构/零-常用枚举技巧", "题单/动态规划/六-状态机-DP", "题单/LeetCode-热题-100/贪心算法", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/139526830"
zhihu_id: "139526830"
zhihu_title: "yiduobo的每日leetcode 121.买卖股票的最佳时机"
question_id: "121"
question: "买卖股票的最佳时机"
problem_url: "https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/"
difficulty: "Easy"
created: "2020-05-10T22:17:03+08:00"
updated: "2020-05-10T22:17:03+08:00"
upvotes: 0
comments: 0
---

# 121. 买卖股票的最佳时机

> **[yiduobo的每日leetcode 121.买卖股票的最佳时机](https://zhuanlan.zhihu.com/p/139526830) · 知乎 · 2020-05-10 · 赞同 0**
> 力扣：[121. 买卖股票的最佳时机](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/) · Easy · 灵茶山艾府：[简洁写法：枚举卖出价格，维护买入的最小值（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

121.买卖股票的最佳时机<https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock/>

比较基础的题目。

假设我们在第k天卖出股票，那么我们所能得到的最大收益为

prices[k] - min(prices[0], prices[1], prices[2], ..., prices[k - 1])

于是我们可以从左往右一趟扫描，维护住后面这个min，每次先用prices[k] - min来更新答案，再用prices[k]来更新min即可。

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

        ans = 0
        buy = prices[0]
        for index in range(1, len(prices)):
            ans = max(prices[index] - buy, ans)
            buy = min(buy, prices[index])

        return ans
```
