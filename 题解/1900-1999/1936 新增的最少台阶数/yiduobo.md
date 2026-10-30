---
title: "1936. 新增的最少台阶数"
aliases: ["yiduobo的每日leetcode 1936.新增的最少台阶数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/488455074"
zhihu_id: "488455074"
zhihu_title: "yiduobo的每日leetcode 1936.新增的最少台阶数"
question_id: "1936"
question: "新增的最少台阶数"
problem_url: "https://leetcode.cn/problems/add-minimum-number-of-rungs/"
difficulty: "Medium"
created: "2022-03-27T16:36:43+08:00"
updated: "2022-03-27T16:36:44+08:00"
upvotes: 0
comments: 0
---

# 1936. 新增的最少台阶数

> **[yiduobo的每日leetcode 1936.新增的最少台阶数](https://zhuanlan.zhihu.com/p/488455074) · 知乎 · 2022-03-27 · 赞同 0**
> 力扣：[1936. 新增的最少台阶数](https://leetcode.cn/problems/add-minimum-number-of-rungs/) · Medium · 灵茶山艾府：[贪心+上取整](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1936.新增的最少台阶数

[力扣](https://leetcode-cn.com/problems/add-minimum-number-of-rungs/)

由于题目没有最小移动距离的限制，因此对于每次移动，就应该能走多远就走多远。同样的，如果需要添加新的台阶，那也应该添加在极限距离上，尽量走得远一些。

根据上面的思路，就有了一个算法。对于当期位置now以及距离now最近的下一级台阶rungs[p]：

1、如果now + dist >\= rungs[p]，说明还可以在已有的台阶上走，于是可以从p开始向后寻找从now最远能够到达的台阶p'，让now走到rungs[p']的位置，然后更新p为p' + 1

2、如果now + dist \< rungs[p]，说明需要添加台阶。需要添加台阶的数目则可以用过rungs[p] - now与dist的倍数关系计算出来。不妨设添加了cnt个新台阶，那么就应该将答案加上cnt，然后从now开始走过这cnt个新台阶。需要注意的是，本着尽量走得远的原则，在这里now不应该走到rungs[p]，而是到达的这新加的cnt个台阶的最后一个的位置，即now + cnt \* dist

重复上面的过程，直到走到最后一级台阶位置。

最后附上python代码：

```python
class Solution(object):
    def addRungs(self, rungs, dist):
        """
        :type rungs: List[int]
        :type dist: int
        :rtype: int
        """

        now = 0
        res = 0
        p = 0
        while now < rungs[-1]:
            if rungs[p] - now > dist:
                cnt = (rungs[p] - now) / dist
                if (rungs[p] - now) % dist == 0:
                    cnt -= 1
                res += cnt
                now = now + cnt * dist
            else:
                while p < len(rungs) and rungs[p] - now <= dist:
                    p += 1
                now = rungs[p - 1]
        
        return res
```
