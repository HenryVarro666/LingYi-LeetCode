---
title: "656. 金币路径"
aliases: ["yiduobo的每日leetcode 656.金币路径"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "leetcode/dp", "题单/动态规划", "题单/动态规划/专题-输出具体方案-打印方案", "题单/动态规划/专题-跳跃游戏"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/603346492"
zhihu_id: "603346492"
zhihu_title: "yiduobo的每日leetcode 656.金币路径"
question_id: "656"
question: "成本最小路径"
problem_url: "https://leetcode.cn/problems/coin-path/"
difficulty: "Hard"
created: "2023-02-04T04:08:46+08:00"
updated: "2023-02-04T04:08:46+08:00"
upvotes: 0
comments: 0
---

# 656. 金币路径

> **[yiduobo的每日leetcode 656.金币路径](https://zhuanlan.zhihu.com/p/603346492) · 知乎 · 2023-02-04 · 赞同 0**
> 力扣：[656. 成本最小路径](https://leetcode.cn/problems/coin-path/) · Hard · 灵茶山艾府：[O(NB) 倒序动态规划](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

656.金币路径

[力扣](https://leetcode.cn/problems/coin-path/)

经典的动态规划问题。令f[i]表示跳到i这个位置时的最小代价，那么对于f[i]：

1、若coins[i] \= -1，那么不可能到达i，在这里也可以置f[i] \= -1，表示无法到达

2、否则就有f[i] \= min(f[j] + coins[j])，其中i - maxJump \<\= j \<\= i - 1，且f[j] !\= -1

这里表示的是从i - maxJump到i - 1中选择一个可以到达的位置j，从j跳到i

对于这个状态转移方程，可以发现实际上代价只与j自身有关，与i无关，因此在更新得到f[j]之后就可以计算从j出发跳到后续位置的代价f[j] + coins[j]了。

另一方面，对于两个位置p和q，满足f[p]和f[q]都不为-1，p > q且f[p] + coins[p] \< f[q] + coins[q]，那么p右侧所有位置都不可能选择从位置q出发，因此可以从q出发必然可以从p出发，且从p出发的代价更小。换言之，在这里可以使用一个单调的双端队列来维护所有可用的f[j] + coins[j]，提供给j后续的位置使用。每当一个位置i更新完毕后，使用f[i] + coins[i]来淘汰掉队列尾部不够好的位置。

在这里之所以选用双端队列而不是单调栈的理由则是由于maxJump的限制，队列头部的位置可能超出可用范围，因此在每一轮的最后都需要将即将出界的位置从队列左侧弹出。

另外，还有一个需要处理的问题就是对于同样代价的情况，需要字典序最小。对于上面描述的这种计算方式，必须额外记录每个f[i]对应的最优路径，不过这样一来就额外多出了路径字典序比较的复杂度。

另外也可以通过反向动态规划来规避掉字典序的影响。反向动态规划可行的理由是对于每个f[i]，计算的实际上是从i到n - 1所需的最小代价，那么在i + 1到i + maxJump这些位置中挑选下一个落脚点时，会优先选择靠前的位置，从而使得字典序最小。不过如果使用反向动态规划，上面单调栈的出界方式也要随之调整。

最后附上python代码：

```python
class Solution(object):
    def cheapestJump(self, coins, maxJump):
        """
        :type coins: List[int]
        :type maxJump: int
        :rtype: List[int]
        """

        if coins[-1] == -1:
            return []

        n = len(coins)
        f = [0]
        next = [-1]

        q = deque()
        q.append([0, n - 1])

        for index in range(n - 2, -1, -1):
            if not q:
                return []
            
            if coins[index] != -1:
                f.append(q[0][0] + coins[index])
                next.append(q[0][1])
                while q and q[-1][0] >= f[-1]:
                    q.pop()
                q.append([f[-1], index])
            else:
                f.append(-1)
                next.append(-1)
            
            while q and q[0][1] >= index + maxJump:
                q.popleft()
        
        next.reverse()
        res = [1]
        now = 0
        while now != n - 1:
            now = next[now]
            res.append(now + 1)

        return res
```
