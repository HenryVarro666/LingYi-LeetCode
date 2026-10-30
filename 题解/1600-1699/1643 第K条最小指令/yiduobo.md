---
title: "1643. 第K条最小指令"
aliases: ["yiduobo的每日leetcode 1643.第K条最小指令"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/439721758"
zhihu_id: "439721758"
zhihu_title: "yiduobo的每日leetcode 1643.第K条最小指令"
question_id: "1643"
question: "第K条最小指令"
problem_url: "https://leetcode.cn/problems/kth-smallest-instructions/"
created: "2021-11-30T23:39:49+08:00"
updated: "2021-11-30T23:39:49+08:00"
upvotes: 0
comments: 0
---

# 1643. 第K条最小指令

> **[yiduobo的每日leetcode 1643.第K条最小指令](https://zhuanlan.zhihu.com/p/439721758) · 知乎 · 2021-11-30 · 赞同 0**
> 力扣：[1643. 第K条最小指令](https://leetcode.cn/problems/kth-smallest-instructions/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1643.第K条最小指令

[力扣](https://leetcode-cn.com/problems/kth-smallest-instructions/)

首先，从(0, 0)走到(m, n)一共需要执行m次V操作以及n次H操作，总共就是m + n次操作。总的方案数就可以认为是从这m + n次操作当中选择m个位置分给V操作，剩下的留给H操作，因此一共就有C(m + n, m)种可能的指令。对于这些指令而言，如果第一步是执行的V操作，那么之后还需要执行m - 1次V操作以及n次H操作，可能的情况就是C(m + n - 1, m - 1)，换言之，以V开头的指令数目就是C(m + n - 1, m - 1)，而以H开头的指令数目则为C(m + n - 1, n - 1)。

那么总的来说，对于这C(m + n, m)条指令而言，排在前面的C(m + n - 1, n - 1)条指令是以H开头的，而后面剩下的指令则是以V开头。

回到题目，对于k而言，首先可以判断k是否小于等于C(m + n - 1, n - 1)，若小于等于，说明第k小的指令是以H开头的，此时问题就转化成了从(0, 1)走到(m, n)的第K条最小指令是什么。若大于，则说第k小的指令是以V开头的，此时问题就转化成了从(1, 0)走到(m, n)的第K - C(m + n - 1, n - 1)条最小指令是什么。

重复这个过程，直到走到(m, n)为止。

最后附上python代码：

```python
class Solution(object):
    def kthSmallestPath(self, destination, k):
        """
        :type destination: List[int]
        :type k: int
        :rtype: str
        """

        m, n = destination
        c = [[0] * (m + n + 1) for _ in range(m + n + 1)]

        for i in range(m + n + 1):
            for j in range(i + 1):
                if j == 0:
                    c[i][j] = 1
                else:
                    c[i][j] = c[i - 1][j] + c[i - 1][j - 1]
        
        res = []
        l = m + n
        for index in range(l):
            if n > 0 and k <= c[m + n - 1][n - 1]:
                res.append('H')
                n -= 1
            else:
                k -= c[m + n - 1][n - 1]
                res.append('V')
                m -= 1
        
        return ''.join(res)
```
