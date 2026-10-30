---
title: "2291. 最大股票收益"
aliases: ["yiduobo的每日leetcode 2291.最大股票收益"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/629167358"
zhihu_id: "629167358"
zhihu_title: "yiduobo的每日leetcode 2291.最大股票收益"
question_id: "2291"
question: "最大股票收益"
problem_url: "https://leetcode.cn/problems/maximum-profit-from-trading-stocks/"
created: "2023-05-13T21:20:25+08:00"
updated: "2023-05-13T21:20:25+08:00"
upvotes: 1
comments: 0
---

# 2291. 最大股票收益

> **[yiduobo的每日leetcode 2291.最大股票收益](https://zhuanlan.zhihu.com/p/629167358) · 知乎 · 2023-05-13 · 赞同 1**
> 力扣：[2291. 最大股票收益](https://leetcode.cn/problems/maximum-profit-from-trading-stocks/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2291.最大股票收益

[力扣](https://leetcode.cn/problems/maximum-profit-from-trading-stocks/)

经典的背包问题，可以使用动态规划求解。令f\[i\]\[j\]表示前i支股票，在初始预算为j时可以得到的最大收益，那么对于f\[i\]\[j\]，有f\[i\]\[j\] \= max(f\[i\]\[j\], f\[i - 1\]\[j - pre\[i - 1\]\] + fu\[i - 1\] - pre\[i - 1\])，这里的j要求满足j >\= pre\[i - 1\]。

求解完成后，f[n - 1][budget]即为最终答案。

另外注意到这里f的每一轮状态都只与上一轮有关，因此可以使用滚动数组优化掉i这一维。

最后附上python代码：

```python
class Solution(object):
    def maximumProfit(self, present, future, budget):
        """
        :type present: List[int]
        :type future: List[int]
        :type budget: int
        :rtype: int
        """

        f = [0] * (budget + 1)
        for pre, fu in zip(present, future):
            if pre > fu or pre > budget:
                continue

            for index in range(budget, pre - 1, -1):
                f[index] = max(f[index], f[index - pre] + fu - pre)

        return f[-1]
```
