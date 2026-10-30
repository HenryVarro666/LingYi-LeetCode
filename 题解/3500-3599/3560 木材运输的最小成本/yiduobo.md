---
title: "3560. 木材运输的最小成本"
aliases: ["yiduobo的每日leetcode 3560.木材运输的最小成本"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1910520340364388085"
zhihu_id: "1910520340364388085"
zhihu_title: "yiduobo的每日leetcode 3560.木材运输的最小成本"
question_id: "3560"
question: "木材运输的最小成本"
problem_url: "https://leetcode.cn/problems/find-minimum-log-transportation-cost/"
difficulty: "Easy"
created: "2025-05-28T22:52:28+08:00"
updated: "2025-05-28T22:52:28+08:00"
upvotes: 0
comments: 0
---

# 3560. 木材运输的最小成本

> **[yiduobo的每日leetcode 3560.木材运输的最小成本](https://zhuanlan.zhihu.com/p/1910520340364388085) · 知乎 · 2025-05-28 · 赞同 0**
> 力扣：[3560. 木材运输的最小成本](https://leetcode.cn/problems/find-minimum-log-transportation-cost/) · Easy · 灵茶山艾府：[O(1) 数学公式，一行代码（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3560.木材运输的最小成本

[3560. 木材运输的最小成本 - 力扣（LeetCode）](https://leetcode.cn/problems/find-minimum-log-transportation-cost/description/)

题目给出三个整数n、m、k，表示有两根长度分别为n和m的木材，需要通过三辆卡车来运输。每辆卡车最多只能装载长度不超过k的木材。现在可以将木材切成更小的段，其中将长度为x的木材切分为y和x - y的两段木材所需的成本为cost \= y \* (x - y)。

问将木材装车所需的最小总成本，如果不需要切割，答案为0。题目保证存在装车的方案，n和m都不超过k \* 2。

若某段木材的长度大于k，就需要进行切分。题目要求切分的代价最小，观察cost \= y \* (x - y)这个式子可以发现，切分的两段长度差越大，cost就越小。另一方面，切分出来的两段长度都不能超过k，因此最优的方案就是将切分成k以及x - k这两段。

于是只需分别检测n和m是否大于k，若大于k，就从中切分出一段长度为k的木材，并将代价累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def minCuttingCost(self, n, m, k):
        """
        :type n: int
        :type m: int
        :type k: int
        :rtype: int
        """
        
        res = 0
        if n > k:
            res += k * (n - k)
        if m > k:
            res += k * (m - k)
        return res
```
