---
title: "LCP 20. 快速公交"
aliases: ["yiduobo的每日leetcode LCP20.快速公交"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/572336720"
zhihu_id: "572336720"
zhihu_title: "yiduobo的每日leetcode LCP20.快速公交"
question_id: "LCP 20"
question: "快速公交"
problem_url: "https://leetcode.cn/problems/me/"
created: "2022-10-11T01:12:47+08:00"
updated: "2022-10-11T01:12:47+08:00"
upvotes: 0
comments: 0
---

# LCP 20. 快速公交

> **[yiduobo的每日leetcode LCP20.快速公交](https://zhuanlan.zhihu.com/p/572336720) · 知乎 · 2022-10-11 · 赞同 0**
> 力扣：[LCP 20. 快速公交](https://leetcode.cn/problems/me/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP20.快速公交

[力扣](https://leetcode.cn/problems/meChtZ/)

题目看上去应该是个动态规划的路子，但是数据规模非常大，不可能保存全部的状态。另一方面，由于走路和坐车的开销杂乱无章，且坐车的乘数也是不规律的，因此也不能通过找规律来进行优化。这种情况下，只能从状态转移出发来寻找一些优化的点。

对于位置x，令f[x]表示到达x所需的最小花销，那么对于f[x]：

1、由于坐车的花销表明，因此头铁全程走路是必须要考虑的一种方案。这种情况下，f[x] \= x \* inc。

2、接下来考虑坐车。在这里可以明确的是，在某次坐车后，设这班车的乘数为jump[i]，那么紧挨着的走路的次数不会大于等于jump[i]，因为对于这种情况，完全可以在坐车前走路，利用坐车乘以jump[i]来放大这次走路，从而节省最终的开销。

例如从p坐车到p \* jump[i]，再紧接着走k步到达x，这里的k >\= jump[i]，即

p \* jump[i] + k \= x，花销为f[p] + cost[i] + k \* inc

在这里如果将k步行走中的y \* jump[i]步提出来，即

(p + y) \* jump[i] + k - (y \* jump[i]) \= x

也就是在坐车钱先走y步，然后坐车，最后再走k - (y \* jump[i])步，花销为f[p] + y \* inc + cost[i] + k - (y \* jump[i]) \* inc。由于题目中的jump[i]总是大于等于2的，因此后面这种先走后坐车的方案一定不会比前面的方案更差。

反过来，坐过站再往回走的情况证明方法也是一样，这里就省略掉了。

根据这个结论，就可以通过贪心法找到坐车之前的位置p。当x恰好是jump[i]的倍数时，p就等于x除以jump[i]，否则p要么是x整数除以jump[i]，坐车之后往前走，要么是x整数除以jump[i]再加上1，坐车之后往回走。

于是就可以枚举每一班车，对于当前这一班车jump[i]：

1、若x是jump\[i\]的倍数，那么就有f\[x\] \= min(f\[x\], f\[x / jump\[i\]\] + cost\[i\])，表示从x / jump\[i\]直接坐车到x

2、若x不是jumps[i]的倍数，那么就有两个起点x / jump[i]以及x / jump[i] + 1

前者的转移方程为f\[x\] \= min(f\[x\], f\[x / jump\[i\]\] + cost\[i\] + (x - x / jump\[i\] \* jump\[i\]) \* inc)，表示从x / jump\[i\]开始坐车，来到x / jump\[i\] \* jump\[i\]，再往前走到x

后者的转移方程为f[x] \= min(f[x], f[x / jump[i] + 1] + cost[i] + ((x / jump[i] + 1) \* jump[i] - x) \* dec)，表示从x / jump[i] + 1开始坐车，来到(x / jump[i] + 1) \* jump[i]，再往回走到x

由于x是呈指数级衰减的，因此总的状态数理论上也不会太多。另一方面，每一个x向下寻找上一个坐车位置的时候，也会出现坐车位置相同的情况，因此使用记忆化搜索应该是可行的。

最后附上python代码：

```python
class Solution(object):
    def busRapidTransit(self, target, inc, dec, jump, cost):
        """
        :type target: int
        :type inc: int
        :type dec: int
        :type jump: List[int]
        :type cost: List[int]
        :rtype: int
        """

        f = {}
        f[1] = inc
        mod = 10 ** 9 + 7

        def dfs(f, now):
            if now in f:
                return f[now]
            
            f[now] = inc * now
            for index in range(len(jump)):
                if now % jump[index] == 0:
                    f[now] = min(f[now], dfs(f, now / jump[index]) + cost[index])
                else:
                    left_pos = now / jump[index] * jump[index]
                    f[now] = min(f[now], dfs(f, now / jump[index]) + cost[index] + inc * (now - left_pos))
                    right_pos = (now / jump[index] + 1) * jump[index]
                    f[now] = min(f[now], dfs(f, now / jump[index] + 1) + cost[index] + dec * (right_pos - now))
            
            return f[now]

        return dfs(f, target) % mod
```
