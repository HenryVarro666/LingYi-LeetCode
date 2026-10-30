---
title: "3376. 破解锁的最少时间I & 3385. 破解锁的最少时间II"
aliases: ["yiduobo的每日leetcode 3376.破解锁的最少时间I && 3385.破解锁的最少时间II", "3376. 破解锁的最少时间I", "3385. 破解锁的最少时间II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/图论算法", "题单/链表-二叉树与回溯/四-回溯", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/图论算法/八-网络流", "leetcode/hard"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/28909853808"
zhihu_id: "28909853808"
zhihu_title: "yiduobo的每日leetcode 3376.破解锁的最少时间I && 3385.破解锁的最少时间II"
question_id: ["3376", "3385"]
question: ["破解锁的最少时间 I", "破解锁的最少时间 II"]
problem_url: ["https://leetcode.cn/problems/minimum-time-to-break-locks-i/", "https://leetcode.cn/problems/minimum-time-to-break-locks-ii/"]
difficulty: ["Medium", "Hard"]
rating: ["1793", "3376"]
created: "2025-03-09T00:38:57+08:00"
updated: "2025-03-09T00:38:57+08:00"
upvotes: 0
comments: 0
---

# 3376. 破解锁的最少时间I & 3385. 破解锁的最少时间II

> **[yiduobo的每日leetcode 3376.破解锁的最少时间I && 3385.破解锁的最少时间II](https://zhuanlan.zhihu.com/p/28909853808) · 知乎 · 2025-03-09 · 赞同 0**
> 力扣：[3376. 破解锁的最少时间 I](https://leetcode.cn/problems/minimum-time-to-break-locks-i/) · Medium · 灵茶山艾府：[三种方法：排列型回溯/状压DP/最小费用流（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3385. 破解锁的最少时间 II](https://leetcode.cn/problems/minimum-time-to-break-locks-ii/) · Hard · 灵茶山艾府：[最小费用流](../3385%20破解锁的最少时间%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3376.破解锁的最少时间I

[3376. 破解锁的最少时间 I - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-time-to-break-locks-i/description/)

3385.破解锁的最少时间II

[3385. 破解锁的最少时间 II - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-time-to-break-locks-ii/description/)

bob被困在一个地窖里，需要破解n个锁才能逃出地窖。每个锁都需要一定的能量才能打开，给出长度为n的数组strength，其中strength[i]表示打开第i个锁所需要的能量。

bob有一把剑，有以下特征：

1、一开始剑的能量为0，同时剑的能量增加因子X一开始为1

2、接下来的每分钟，剑的能量都会增加当前的X值

3、如果想打开第i把锁，剑的能量必须大于等于strength[i]

4、打开一把锁之后，剑的能量归零，X的值则会增加一个给定的常量K

问bob打开n把锁所需的最少时间

两题的题设类似。3376题中n小于等于8，而3385题中的k固定为1，但是n的规模可以到达80。

---

按3385题的数据规模来看，使用状态压缩动态规划肯定是不行的，启发式搜索的话也许可以，但是估计要很多剪枝，必须另想办法。

首先注意到每次开锁后剑的能量都会归零，因此如果目标锁已经确定，那么在能量足够的那一刻就应该立即开锁。另一方面，由于题目中给出的k是固定的，因此可以计算出在打开第j把锁时的能量增加因子X，从而进一步计算出如果打开的第j把锁是编号为i的锁所需的时间。

具体来说，如果目前计划打开的是第j把锁，那么之前打开过(j - 1)把锁，因此当前的X为(j - 1) \* k + 1，而所需的等待时间就是(strength[i] - 1) // X + 1。

更进一步的，如果以全排列中的位置来看待第几个开的锁的话，本题就可以视为有n把锁和n个位置，需要将这些锁分配到这些位置上，每个位置都需要分配一把，而分配的代价就是上面的等待时间，现在要求以最小的代价完成分配。对于这个问题，可以使用费用流求解。

费用流的建图方法如下：

1、从原点s各发射一条边到n把锁对应的每个节点，这些边的容量为1，费用为0，表示每把锁都要开

2、对于每把锁对应的节点i，发射一条边到每个位置对应的节点j，这些边的容量为1，费用则为上面计算的等待时间。在这里需要根据节点编号对下标进行修正，表示可以将第i把锁放在第j个打开，所需的代价为对应的等待时间

3、对于每个位置对应的节点j，都向汇点发射一条边，这些边的容量为1，费用为0，表示每个位置只能开一次

建图完成后，跑一次最小费用最大流，得到的最小费用即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def findMinimumTime(self, strength, K):
        """
        :type strength: List[int]
        :type K: int
        :rtype: int
        """
        
        n = len(strength)
        s = n + n
        t = n + n + 1

        c = [[0] * (t + 1) for _ in range(t + 1)]
        cost = [[0] * (t + 1) for _ in range(t + 1)]

        for i in range(n):
            c[s][i] = 1
        
        for j in range(n, n + n):
            c[j][t] = 1
        
        for i in range(n):
            for j in range(n, n + n):
                c[i][j] = 1
                cost[i][j] = (strength[i] - 1) // (1 + K * (j - n)) + 1
                cost[j][i] = -cost[i][j]
        
        res = 0
        while True:
            dis = [None] * (t + 1)
            prev = [None] * (t + 1)
            used = set([s])
            dis[s] = 0
            now = s
            while t not in used:
                min_dis = None
                nxt = None
                for index in range(t + 1):
                    if c[now][index] > 0 and (dis[index] is None or dis[index] > dis[now] + cost[now][index]):
                        dis[index] = dis[now] + cost[now][index]
                        prev[index] = now
                        if index in used:
                            used.remove(index)
                    if index not in used and dis[index] is not None and (min_dis is None or min_dis > dis[index]):
                        nxt = index
                        min_dis = dis[index]

                if min_dis is None:
                    return res
                
                used.add(nxt)
                now = nxt

            res += dis[t]
            now = t
            while now != s:
                c[prev[now]][now] -= 1
                c[now][prev[now]] += 1
                now = prev[now]
```
