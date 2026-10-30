---
title: "4079. 选择质数子集I"
aliases: ["yiduobo的每日leetcode 4079.选择质数子集I"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2094180780683572530"
zhihu_id: "2094180780683572530"
zhihu_title: "yiduobo的每日leetcode 4079.选择质数子集I"
question_id: "4079"
question: "选择质数子集I"
problem_url: "https://leetcode.cn/problems/prime-subset-selection-i/"
created: "2026-10-15T21:48:29+08:00"
updated: "2026-10-15T21:48:29+08:00"
upvotes: 0
comments: 0
---

# 4079. 选择质数子集I

> **[yiduobo的每日leetcode 4079.选择质数子集I](https://zhuanlan.zhihu.com/p/2094180780683572530) · 知乎 · 2026-10-15 · 赞同 0**
> 力扣：[4079. 选择质数子集I](https://leetcode.cn/problems/prime-subset-selection-i/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4079.选择质数子集I

<https://leetcode.cn/problems/prime-subset-selection-i/description/>

题目给出两个正整数n和s，其中n不超过10^6，s不超过10^9。

考虑所有小于等于n的质数，现在要求从中选择出一些质数，满足：

- 所选质数的总和小于等于s
- 所选质数的数量尽量多
- 每个质数最多只能选择一次

要求返回一个包含所选质数的整数数组，按递增顺序排列。若存在多个最优选择，可以任意返回一个。若无法选择，则返回空数组。

题目要求选择的质数尽量多，那么就应该按照大小顺序，从小到大开始选取。

于是可以先通过筛法找出n以内的所有质数，当找到一个质数时，若将其加入答案数组后答案数组之和不超过s，则将其加入答案数组，然后继续考虑下一个质数。反之，后续的质数都更大，因此也无法加入到答案数组中，此时就可以直接返回答案了。

最后附上python代码：

```python
class Solution(object):
    def maxPrimes(self, n, s):
        """
        :type n: int
        :type s: int
        :rtype: List[int]
        """
        
        f = [True] * (n + 1)
        v = 2
        p_s = 0
        res = []
        while v <= n:
            if f[v]:
                if p_s + v > s:
                    break
                res.append(v)
                p_s += v

                for x in range(v + v, n + 1, v):
                    f[x] = False
            v += 1
        
        return res
```
