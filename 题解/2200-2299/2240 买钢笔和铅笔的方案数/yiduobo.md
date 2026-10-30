---
title: "2240. 买钢笔和铅笔的方案数"
aliases: ["yiduobo的每日leetcode 2240.买钢笔和铅笔的方案数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/enumeration", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/545102009"
zhihu_id: "545102009"
zhihu_title: "yiduobo的每日leetcode 2240.买钢笔和铅笔的方案数"
question_id: "2240"
question: "买钢笔和铅笔的方案数"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-buy-pens-and-pencils/"
difficulty: "Medium"
created: "2022-07-23T00:52:31+08:00"
updated: "2022-07-23T00:52:31+08:00"
upvotes: 0
comments: 0
---

# 2240. 买钢笔和铅笔的方案数

> **[yiduobo的每日leetcode 2240.买钢笔和铅笔的方案数](https://zhuanlan.zhihu.com/p/545102009) · 知乎 · 2022-07-23 · 赞同 0**
> 力扣：[2240. 买钢笔和铅笔的方案数](https://leetcode.cn/problems/number-of-ways-to-buy-pens-and-pencils/) · Medium · 灵茶山艾府：[枚举买了多少支钢笔（附 O(log) 类欧几里得算法）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2240.买钢笔和铅笔的方案数

[力扣](https://leetcode.cn/problems/number-of-ways-to-buy-pens-and-pencils/)

由于就两种笔，那么完全可以枚举其中一种的数量，然后计算选择另一种笔的可能方案数。具体来说，不妨设当前买了x支钢笔，还剩下的资金就是total - cost1 \* x。使用这笔钱来买铅笔，可以买到的最大数目就是k \= (total - cost1 \* x) / cost2，那么在这里就有0到k这一共k + 1种购买方案数，于是可以将k + 1累加到答案中，然后继续考察购买x + 1支钢笔时的情况，直到cost1 \* x > total为止。

最后附上python代码：

```python
class Solution(object):
    def waysToBuyPensPencils(self, total, cost1, cost2):
        """
        :type total: int
        :type cost1: int
        :type cost2: int
        :rtype: int
        """

        res = 0
        cnt1 = 0
        while cnt1 * cost1 <= total:
            res += (total - cnt1 * cost1) / cost2 + 1
            cnt1 += 1
        
        return res
```
