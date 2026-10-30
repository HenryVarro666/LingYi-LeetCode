---
title: "1723. 完成所有工作的最短时间"
aliases: ["yiduobo的每日leetcode 1723.完成所有工作的最短时间"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/dynamic-programming", "leetcode/bitmask", "leetcode/di-tui", "leetcode/dp-2", "题单/动态规划", "题单/数学算法", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/451867073"
zhihu_id: "451867073"
zhihu_title: "yiduobo的每日leetcode 1723.完成所有工作的最短时间"
question_id: "1723"
question: "完成所有工作的最短时间"
problem_url: "https://leetcode.cn/problems/find-minimum-time-to-finish-all-jobs/"
difficulty: "Hard"
rating: 2284
created: "2021-12-30T23:38:37+08:00"
updated: "2021-12-30T23:38:37+08:00"
upvotes: 1
comments: 0
---

# 1723. 完成所有工作的最短时间

> **[yiduobo的每日leetcode 1723.完成所有工作的最短时间](https://zhuanlan.zhihu.com/p/451867073) · 知乎 · 2021-12-30 · 赞同 1**
> 力扣：[1723. 完成所有工作的最短时间](https://leetcode.cn/problems/find-minimum-time-to-finish-all-jobs/) · Hard · 灵茶山艾府：[如何用 Python 的状压 DP 递推写法通过此题](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1723.完成所有工作的最短时间

[力扣](https://leetcode-cn.com/problems/find-minimum-time-to-finish-all-jobs/)

依然是没能找到可行的网络流建模，只能老老实实用状态压缩动态规划来做。

令f[i][state]表示将state中的工作分配给前i个工人，工作时间最大的工人的最小值是多少。

那么对于f[i][state]而言，需要枚举state的所有子状态sub_state，可以认为将子状态中的工作都交给了最后新来的这个人，那么就有

f[i][state] \= min(f[i][state], max(f[i - 1][state ^ sub_state], cost[sub_state])

其中cost[sub_state]表示完成sub_state中的工作所需的时间，可以实现预处理出来。

理论上来说上面的做法时间复杂度应该是O(n \* 3^n)，在这里还是比较吃紧的，需要做一些剪枝。一个自然的想法就是当工作的数目小于工人的数目时，此时所需的最大时间就是这些工作所需时间的最大值。可以通过这个节省掉一些状态的计算。

另外，由于这里f[i]的状态只与f[i - 1]的状态有关，因此可以通过滚动f节省掉i这一维。不过相对的，由于f[i][state]依赖于f[i - 1][sub_state]，因此在省去i这一维之后需要先从大的state开始计算。

最后附上python代码：

```python
class Solution(object):
    def minimumTimeRequired(self, jobs, k):
        """
        :type jobs: List[int]
        :type k: int
        :rtype: int
        """

        n = len(jobs)
        max_state = 1 << n
        cost = [0] * max_state
        cnt = [0] * max_state
        max_job = [0] * max_state
        for state in range(1, max_state):
            for job in range(n):
                if state & (1 << job):
                    cost[state] = cost[state ^ (1 << job)] + jobs[job]
                    cnt[state] = cnt[state ^ (1 << job)] + 1
                    max_job[state] = max(max_job[state ^ (1 << job)], jobs[job])
                    break

        f = cost[:]
        for index in range(1, k):
            for state in range(max_state - 1, 0, -1):
                if cnt[state] <= index + 1:
                    f[state] = max_job[state]
                else:
                    sub_state = state
                    while sub_state:
                        f[state] = min(f[state], max(f[state ^ sub_state], cost[sub_state]))
                        sub_state = (sub_state - 1) & state
        
        return f[-1]
```
