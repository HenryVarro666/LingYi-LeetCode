---
title: "3711. 不出现负余额的最大交易"
aliases: ["yiduobo的每日leetcode 3711.不出现负余额的最大交易"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1961543517005412231"
zhihu_id: "1961543517005412231"
zhihu_title: "yiduobo的每日leetcode 3711.不出现负余额的最大交易"
question_id: "3711"
question: "不出现负余额的最大交易"
problem_url: "https://leetcode.cn/problems/maximum-transactions-without-negative-balance/"
created: "2025-10-14T21:44:29+08:00"
updated: "2025-10-14T21:44:29+08:00"
upvotes: 0
comments: 0
---

# 3711. 不出现负余额的最大交易

> **[yiduobo的每日leetcode 3711.不出现负余额的最大交易](https://zhuanlan.zhihu.com/p/1961543517005412231) · 知乎 · 2025-10-14 · 赞同 0**
> 力扣：[3711. 不出现负余额的最大交易](https://leetcode.cn/problems/maximum-transactions-without-negative-balance/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3711.不出现负越的最大交易

[3711. 不出现负余额的最大交易额 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-transactions-without-negative-balance/)

题目给出一个整数数组transcations，其中transacations[i]表示的是第i笔交易的总额，其中正数表示收到的钱，负数表示支出的钱。

账户的初始金额为0，且余额必须始终保持非负。交易必须按照指定的顺序进行，但是可以跳过其中某些交易。问在保证余额非负的前提下，最多可以执行多少笔交易。

题目要求在余额非负的前提下进行尽量多的交易，那么对于金额非负的交易就应该无条件执行交易，而对于金额为负数的交易，则可以先尝试执行，如果执行后金额变成了负数，则必须取消之前已经进行的某次交易。很明显，在这里就应该取消掉金额负得最多的那一次交易，这样一来就可以在保证交易次数最多的前提下让余额最大。

基于上面的结论，就可以一趟遍历，使用一个堆维护所有执行了负值交易，并使用一个变量s记录交易总额。

接下来对于每笔交易，先尝试执行，将交易额累加到s中，若交易额为负，则还需要将其加入到堆中。

若此时的交易额变成了负数，说明需要取消掉之前的某次交易，于是可以将堆顶元素弹出，并从s中减去这个值，表示取消掉了负的最多的那一笔交易。由于此时进行了一次交易，又取消了一次交易，因此答案不变。反之，若总额非负，则应该将答案加上1，表示相比之前多进行了一笔交易。

最后附上python代码：

```python
class Solution(object):
    def maxTransactions(self, transactions):
        """
        :type transactions: List[int]
        :rtype: int
        """
        
        s = 0
        neg = []
        res = 0
        for t in transactions:
            s += t
            if t < 0:
                heapq.heappush(neg, t)
            if s < 0:
                s -= heapq.heappop(neg)
            else:
                res += 1
        
        return res
```
