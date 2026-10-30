---
title: "3155. 可升级服务器的最大数量"
aliases: ["yiduobo的每日leetcode 3155.可升级服务器的最大数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/704157501"
zhihu_id: "704157501"
zhihu_title: "yiduobo的每日leetcode 3155.可升级服务器的最大数量"
question_id: "3155"
question: "可升级服务器的最大数量"
problem_url: "https://leetcode.cn/problems/maximum-number-of-upgradable-servers/"
created: "2024-06-19T00:11:24+08:00"
updated: "2024-06-19T00:11:24+08:00"
upvotes: 0
comments: 0
---

# 3155. 可升级服务器的最大数量

> **[yiduobo的每日leetcode 3155.可升级服务器的最大数量](https://zhuanlan.zhihu.com/p/704157501) · 知乎 · 2024-06-19 · 赞同 0**
> 力扣：[3155. 可升级服务器的最大数量](https://leetcode.cn/problems/maximum-number-of-upgradable-servers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3155.可升级服务器的最大数量

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-number-of-upgradable-servers/description/)

题目给出4个长度为n的数组count，upgrade，sell和money，对应到数据中心服务器的升级信息，具体来说：

count[i]表示第i个数据中心服务器的数量

upgrade[i]表示第i个数据中心升级单台服务器的成本

sell[i]表示第i个数据中心出售单台服务器的价格

money[i]表示第i个数据中心初始的资金

问针对每个数据中心可升级的服务器数量。数据中心之间的资金不能混用。

由于数据中心之间的资金不能混用，那么就可以逐个遍历每个数据中心分别求解。

对于第i个数据中心：

1、若其初始资金足够多，即count[i] \* upgrade[i] \<\= money[i]，此时就可以升级全部的服务器

2、反之，则可以选择卖掉部分服务器，用卖服务器的资金加上初始资金来升级其他的服务器。对于这种情况，不妨设最后剩下x个服务器，那么就有

x \* upgrade[i] \<\= (count[i] - x) \* sell[i] + money[i]

将x的项合并，就有

x \* (upgrade[i] + sell[i]) \<\= count[i] \* sell[i] + money[i]

即

x \<\= (count[i] \* sell[i] + money[i]) // (upgrade[i] + sell[i])

对于上面这个式子，另一种理解为先把所有服务器都卖了，换来count[i] \* sell[i]的资金，接下来可以认为赎回来一台服务器并升级的价格为upgrade[i] + sell[i]。

最后附上python代码：

```python
class Solution(object):
    def maxUpgrades(self, count, upgrade, sell, money):
        """
        :type count: List[int]
        :type upgrade: List[int]
        :type sell: List[int]
        :type money: List[int]
        :rtype: List[int]
        """

        res = []

        for c, u, s, m in zip(count, upgrade, sell, money):
            if m >= u * c:
                res.append(c)
            else:
                res.append((m + c * s) // (u + s))
        
        return res
```
