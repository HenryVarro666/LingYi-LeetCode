---
title: "2806. 取整购买后的账户余额"
aliases: ["yiduobo的每日leetcode 2806.取整购买后的账户余额"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/657716006"
zhihu_id: "657716006"
zhihu_title: "yiduobo的每日leetcode 2806.取整购买后的账户余额"
question_id: "2806"
question: "取整购买后的账户余额"
problem_url: "https://leetcode.cn/problems/account-balance-after-rounded-purchase/"
difficulty: "Easy"
created: "2023-09-22T04:04:38+08:00"
updated: "2023-09-22T04:04:38+08:00"
upvotes: 0
comments: 0
---

# 2806. 取整购买后的账户余额

> **[yiduobo的每日leetcode 2806.取整购买后的账户余额](https://zhuanlan.zhihu.com/p/657716006) · 知乎 · 2023-09-22 · 赞同 0**
> 力扣：[2806. 取整购买后的账户余额](https://leetcode.cn/problems/account-balance-after-rounded-purchase/) · Easy · 灵茶山艾府：[避免浮点数的写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2806.取整购买后的账户余额

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/account-balance-after-rounded-purchase/)

题目实际上可以理解成对于整数的个位数在做四舍五入，那么只需通过模10将个位x分离出来，若x小于5，那么抹零，最终答案为100 - (purchaseAmount - x)，反之则是反向抹零，最终答案为100 - (purchaseAmount + 10 - x)。

最后附上python代码：

```python
class Solution(object):
    def accountBalanceAfterPurchase(self, purchaseAmount):
        """
        :type purchaseAmount: int
        :rtype: int
        """

        x = purchaseAmount % 10
        if x < 5:
            return 100 - (purchaseAmount - x)
        else:
            return 100 - (purchaseAmount + 10 - x)
```
