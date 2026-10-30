---
title: "2898. 最大线性股票得分"
aliases: ["yiduobo的每日leetcode 2898.最大线性股票得分"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/663387893"
zhihu_id: "663387893"
zhihu_title: "yiduobo的每日leetcode 2898.最大线性股票得分"
question_id: "2898"
question: "最大线性股票得分"
problem_url: "https://leetcode.cn/problems/maximum-linear-stock-score/"
created: "2023-10-26T03:10:44+08:00"
updated: "2023-10-26T03:10:45+08:00"
upvotes: 1
comments: 0
---

# 2898. 最大线性股票得分

> **[yiduobo的每日leetcode 2898.最大线性股票得分](https://zhuanlan.zhihu.com/p/663387893) · 知乎 · 2023-10-26 · 赞同 1**
> 力扣：[2898. 最大线性股票得分](https://leetcode.cn/problems/maximum-linear-stock-score/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2898.最大线性股票得分

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-linear-stock-score/)

对于这类与下标相关的等式，一种常见的处理思路是将所有下标相同的项集中起来看看会不会得到什么结论。本题恰好适用。

题目中的式子为

prices\[indexes\[j\]\] - prices\[indexes\[j - 1\]\] \=\= indexes\[j\] - indexes\[j - 1\]

变形后就是

prices\[indexes\[j\]\] - indexes\[j\] \= prices\[indexes\[j - 1\]\] - indexes\[j - 1\]

也就是说，如果将数组中每个数都减去自身的下标，那么题目就变成了数组中出现次数最多的数的下标之和是多少。于是可以一趟遍历，利用哈希表记录所有减去自身下标后相等的值的下标之和，然后取其中的最大值作为答案就行了。

最后附上python代码：

```python3
class Solution(object):
    def maxScore(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """

        cnt = {}
        for index, v in enumerate(prices):
            cnt[v - index] = cnt.get(v - index, 0) + v
        
        return max(cnt.values())
```
