---
title: "1599. 经营摩天轮的最大利润"
aliases: ["yiduobo的每日leetcode 1599.经营摩天轮的最大利润"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/432309505"
zhihu_id: "432309505"
zhihu_title: "yiduobo的每日leetcode 1599.经营摩天轮的最大利润"
question_id: "1599"
question: "经营摩天轮的最大利润"
problem_url: "https://leetcode.cn/problems/maximum-profit-of-operating-a-centennial-wheel/"
created: "2021-11-13T16:33:14+08:00"
updated: "2021-11-13T16:33:14+08:00"
upvotes: 0
comments: 0
---

# 1599. 经营摩天轮的最大利润

> **[yiduobo的每日leetcode 1599.经营摩天轮的最大利润](https://zhuanlan.zhihu.com/p/432309505) · 知乎 · 2021-11-13 · 赞同 0**
> 力扣：[1599. 经营摩天轮的最大利润](https://leetcode.cn/problems/maximum-profit-of-operating-a-centennial-wheel/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1599.经营摩天轮的最大利润

[力扣](https://leetcode-cn.com/problems/maximum-profit-of-operating-a-centennial-wheel/)

仔细阅读题目可以发现，这老板收了门票之后就不管你是不是可以从摩天轮上下来了，还真是黑心商贩。。

基于这一点，首先可以处理掉边界情况。若每次收4个人的门票钱还抵不上转一次摩天轮的钱，那么就没有开业的必要了，直接返回-1。

接下来则可以进行模拟。对于每一时刻，维护当前剩余游客的数目p。若某一时刻p小于4，那么此时转动摩天轮的收益就是boardingCost \* p - runningCost，此时应该将这个值累加到收益当中，并更新答案，同时将剩余的游客数p置0；若p大于等于4，转动摩天轮的收益则为boardingCost \* 4 - runningCost，同样是将其累加到收益当中并更新答案。此时应该将p减去4。

遍历完所有有新游客加入的时刻之后，若p大于等于4，那么此时必然是尽可能地安排，因此需要再转动p / 4轮，新增的收益为p / 4 \* (boardingCost \* 4 - runningCost)，而剩余的游客数则变为了p % 4。接下来对于剩下的这些游客，若满足p % 4 \* boadingCost大于runningCost，则有必要对这些人再转动一轮摩天轮，此时同样需要更新收益以及答案。

最后附上python代码：

```python
class Solution(object):
    def minOperationsMaxProfit(self, customers, boardingCost, runningCost):
        """
        :type customers: List[int]
        :type boardingCost: int
        :type runningCost: int
        :rtype: int
        """

        if boardingCost * 4 <= runningCost:
            return -1

        max_v = 0
        res = -1
        now = 0
        p = 0
        for index, c in enumerate(customers):
            p += c
            if p < 4:
                now += boardingCost * p - runningCost
                p = 0
            else:
                now += boardingCost * 4 - runningCost
                p -= 4
            if now > max_v:
                max_v = now
                res = index + 1

        tmp = len(customers)
        if p > 0:
            now += p / 4 * (boardingCost * 4 - runningCost)
            tmp += p / 4
            if boardingCost * (p % 4) > runningCost:
                now += boardingCost * (p % 4) - runningCost
                tmp += 1
        
        if now > max_v:
            res = tmp
        
        return res
```
