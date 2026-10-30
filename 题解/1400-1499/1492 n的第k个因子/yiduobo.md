---
title: "1492. n的第k个因子"
aliases: ["yiduobo的每日leetcode 1492.n的第k个因子"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/416791599"
zhihu_id: "416791599"
zhihu_title: "yiduobo的每日leetcode 1492.n的第k个因子"
question_id: "1492"
question: "n的第k个因子"
problem_url: "https://leetcode.cn/problems/the-kth-factor-of-n/"
created: "2021-10-04T09:06:44+08:00"
updated: "2021-10-04T09:06:44+08:00"
upvotes: 0
comments: 0
---

# 1492. n的第k个因子

> **[yiduobo的每日leetcode 1492.n的第k个因子](https://zhuanlan.zhihu.com/p/416791599) · 知乎 · 2021-10-04 · 赞同 0**
> 力扣：[1492. n的第k个因子](https://leetcode.cn/problems/the-kth-factor-of-n/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1492.n的第k个因子

[力扣](https://leetcode-cn.com/problems/the-kth-factor-of-n/)

由于这里n的规模并不大，那么可以直接从1到sqrt(n)枚举n的所有因此。对于当前值now，若n模now等于0，说明now是n的一个因子。除此之外，也说明n / now同样是n的一个因子，那么还需要使用一个数组将这些大于sqrt(n)的因子储存起来。需要特别注意的是，当now是完全平方数时，sqrt(n)就等于n / sqrt(n)，不能重复计算。

若计算过程中就找到了第k个因子，那么直接返回，否则需要对比记录较大那部分因子的数组的长度以及当前剩下k的大小。若数组长度不够k，那么返回-1，否则倒序返回数组中的第k - 1个因子。

最后附上python代码：

```python
class Solution(object):
    def kthFactor(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """
        
        q = []
        now = 1
        while now * now <= n:
            if n % now == 0:
                k -= 1
                if k == 0:
                    return now

                if n / now != now:
                    q.append(n / now)
                
            now += 1
        
        if len(q) < k:
            return -1

        q.reverse()
        return q[k - 1]
```
