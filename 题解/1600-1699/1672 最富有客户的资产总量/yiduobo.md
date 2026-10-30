---
title: "1672. 最富有客户的资产总量"
aliases: ["yiduobo的每日leetcode 1672.最富有客户的资产总量"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/443880475"
zhihu_id: "443880475"
zhihu_title: "yiduobo的每日leetcode 1672.最富有客户的资产总量"
question_id: "1672"
question: "最富有客户的资产总量"
problem_url: "https://leetcode.cn/problems/richest-customer-wealth/"
difficulty: "Easy"
created: "2021-12-11T00:17:23+08:00"
updated: "2021-12-11T00:17:23+08:00"
upvotes: 0
comments: 0
---

# 1672. 最富有客户的资产总量

> **[yiduobo的每日leetcode 1672.最富有客户的资产总量](https://zhuanlan.zhihu.com/p/443880475) · 知乎 · 2021-12-11 · 赞同 0**
> 力扣：[1672. 最富有客户的资产总量](https://leetcode.cn/problems/richest-customer-wealth/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1672.最富有客户的资产总量

[力扣](https://leetcode-cn.com/problems/richest-customer-wealth/)

比较基础的题目，直接枚举每个客户计算account内所有数的和，取其中的最大值作为答案就好了。

最后附上python代码：

```python
class Solution(object):
    def maximumWealth(self, accounts):
        """
        :type accounts: List[List[int]]
        :rtype: int
        """

        res = 0
        for account in accounts:
            res = max(res, sum(account))
        
        return res
```
