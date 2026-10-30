---
title: "3958. 拆分到1的最小总代价II"
aliases: ["yiduobo的每日leetcode 3958.拆分到1的最小总代价II"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2048542161872992160"
zhihu_id: "2048542161872992160"
zhihu_title: "yiduobo的每日leetcode 3958.拆分到1的最小总代价II"
question_id: "3958"
question: "拆分到 1 的最小总代价 II"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-split-into-ones-ii/"
difficulty: "Medium"
created: "2026-06-11T23:11:45+08:00"
updated: "2026-06-11T23:12:20+08:00"
upvotes: 1
comments: 0
---

# 3958. 拆分到1的最小总代价II

> **[yiduobo的每日leetcode 3958.拆分到1的最小总代价II](https://zhuanlan.zhihu.com/p/2048542161872992160) · 知乎 · 2026-06-11 · 赞同 1**
> 力扣：[3958. 拆分到 1 的最小总代价 II](https://leetcode.cn/problems/minimum-cost-to-split-into-ones-ii/) · Medium · 灵茶山艾府：[等价转化，O(1) 公式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3958.拆分到1的最小总代价II

<https://leetcode.cn/problems/minimum-cost-to-split-into-ones-ii/description/>

题目给出一个整数n，其大小在1到5 \* 10^7之间。

在每次操作中，可以将一个整数x，拆分为两个正整数a和b，满足a + b \= x，此次操作的代价为a \* b。

问将n拆分为n个1所需的最小总代价。

本题与之前的3857题题设相同，但是数据规模较大。不过之前已经通过找规律以及归纳法得到了O(1)的算法，直接沿用就行了。

[yiduobo的每日leetcode 3857.拆分到1的最小总代价](https://zhuanlan.zhihu.com/p/2013642660959777510)

最后附上python代码：

```python
class Solution(object):
    def minCost(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        return n * (n - 1) // 2
```
