---
title: "2706. 购买两块巧克力"
aliases: ["yiduobo的每日leetcode 2706.购买两块巧克力"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/650750280"
zhihu_id: "650750280"
zhihu_title: "yiduobo的每日leetcode 2706.购买两块巧克力"
question_id: "2706"
question: "购买两块巧克力"
problem_url: "https://leetcode.cn/problems/buy-two-chocolates/"
difficulty: "Easy"
created: "2023-08-18T02:53:54+08:00"
updated: "2023-08-18T02:53:54+08:00"
upvotes: 0
comments: 0
---

# 2706. 购买两块巧克力

> **[yiduobo的每日leetcode 2706.购买两块巧克力](https://zhuanlan.zhihu.com/p/650750280) · 知乎 · 2023-08-18 · 赞同 0**
> 力扣：[2706. 购买两块巧克力](https://leetcode.cn/problems/buy-two-chocolates/) · Easy · 灵茶山艾府：[O(n) 一次遍历](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2706.购买两块巧克力

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/buy-two-chocolates/)

题目要求购买巧克力的花费最小，那么很明显应该买最便宜的两块。于是只需一趟遍历，找出prices中的最小值以及次小值即可。

最后附上python代码：

```python
class Solution(object):
    def buyChoco(self, prices, money):
        """
        :type prices: List[int]
        :type money: int
        :rtype: int
        """

        a = prices[0]
        b = prices[1]
        if a > b:
            a, b = b, a
        
        for p in prices[2:]:
            if p < a:
                a, b = p, a
            elif p < b:
                b = p
        
        if a + b <= money:
            return money - a - b
        else:
            return money
```
