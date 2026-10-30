---
title: "1175. 质数排列"
aliases: ["yiduobo的每日leetcode 1175.质数排列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/379726471"
zhihu_id: "379726471"
zhihu_title: "yiduobo的每日leetcode 1175.质数排列"
question_id: "1175"
question: "质数排列"
problem_url: "https://leetcode.cn/problems/prime-arrangements/"
created: "2021-06-10T23:48:29+08:00"
updated: "2021-06-10T23:48:29+08:00"
upvotes: 0
comments: 0
---

# 1175. 质数排列

> **[yiduobo的每日leetcode 1175.质数排列](https://zhuanlan.zhihu.com/p/379726471) · 知乎 · 2021-06-10 · 赞同 0**
> 力扣：[1175. 质数排列](https://leetcode.cn/problems/prime-arrangements/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1175.质数排列

[力扣](https://leetcode-cn.com/problems/prime-arrangements/)

设1-n中一共有p个质数，那么合数的数量为n - p。这p个质数可以在p个质数索引上任意放置，因此一共有p！种放置方法。同理，剩下的n - p个非质数可以在n - p个非质数索引上任意放置，因此一共有(n - p)！种放置方法，因此最终一共就有p！\* (n - p)！种可行的方案。

那么我们只需求出1到n中质数的数量p，然后计算阶乘求出最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def numPrimeArrangements(self, n):
        """
        :type n: int
        :rtype: int
        """

        f = [True] * 101
        f[1] = False
        now = 2
        while now * now <= n:
            tmp = now + now
            while tmp <= n:
                f[tmp] = False
                tmp += now
            
            now += 1
        
        p = q = 0
        for index in range(1, n + 1):
            if f[index]:
                p += 1
            else:
                q += 1

        now = 1
        res = 1
        mod = 10 ** 9 + 7
        for index in range(2, max(p, q) + 1):
            now = now * index % mod
            if index == p:
                res = res * now % mod
            if index == q:
                res = res * now % mod
        
        return res
```
