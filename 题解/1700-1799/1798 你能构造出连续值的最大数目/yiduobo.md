---
title: "1798. 你能构造出连续值的最大数目"
aliases: ["yiduobo的每日leetcode 1798.你能构造出连续值的最大数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/463627921"
zhihu_id: "463627921"
zhihu_title: "yiduobo的每日leetcode 1798.你能构造出连续值的最大数目"
question_id: "1798"
question: "你能构造出连续值的最大数目"
problem_url: "https://leetcode.cn/problems/maximum-number-of-consecutive-values-you-can-make/"
difficulty: "Medium"
rating: 1931
created: "2022-02-02T16:00:42+08:00"
updated: "2022-02-02T16:00:43+08:00"
upvotes: 0
comments: 0
---

# 1798. 你能构造出连续值的最大数目

> **[yiduobo的每日leetcode 1798.你能构造出连续值的最大数目](https://zhuanlan.zhihu.com/p/463627921) · 知乎 · 2022-02-02 · 赞同 0**
> 力扣：[1798. 你能构造出连续值的最大数目](https://leetcode.cn/problems/maximum-number-of-consecutive-values-you-can-make/) · Medium · 灵茶山艾府：[没想明白？一张图秒懂！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1798.你能构造出连续值的最大数目

[力扣](https://leetcode-cn.com/problems/maximum-number-of-consecutive-values-you-can-make/)

不妨设当前的数字能覆盖住区间[0, ma]，那么在加入一个新的数字coin之和，可以覆盖的区间就变成了[0, ma]以及[coin, ma + coin]的并集。为了使得这个区间连续，那么需要满足coin \<\= ma + 1。

为了能够流畅地扩展区间，那么应该让coin尽量小，因此在这里应该按从小到大地顺序将coins中的数加入到区间中。若当前的数值coin满足coin \<\= ma + 1，那么说明ma可以扩展到ma + coin。若不满足，那么在加入coin之和区间不再连续。由于coins中后续的数都大于等于coin，因此后续的数加入到区间后也会使得区间不再连续，因此最终可以覆盖的区间就是[0, ma]，里面一共由ma + 1个数，因此答案就是ma + 1。

最后附上python代码：

```python
class Solution(object):
    def getMaximumConsecutive(self, coins):
        """
        :type coins: List[int]
        :rtype: int
        """

        ma = 0
        for coin in sorted(coins):
            if coin <= ma + 1:
                ma += coin
            else:
                break
        
        return ma + 1
```
