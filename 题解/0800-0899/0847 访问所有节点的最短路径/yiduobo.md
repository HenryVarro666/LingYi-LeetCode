---
title: "847. 访问所有节点的最短路径"
aliases: ["yiduobo的每日leetcode 847.访问所有节点的最短路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/348061930"
zhihu_id: "348061930"
zhihu_title: "yiduobo的每日leetcode 847.访问所有节点的最短路径"
question_id: "847"
question: "访问所有节点的最短路径"
problem_url: "https://leetcode.cn/problems/shortest-path-visiting-all-nodes/"
created: "2021-01-30T10:18:42+08:00"
updated: "2021-01-30T10:18:42+08:00"
upvotes: 2
comments: 2
---

# 847. 访问所有节点的最短路径

> **[yiduobo的每日leetcode 847.访问所有节点的最短路径](https://zhuanlan.zhihu.com/p/348061930) · 知乎 · 2021-01-30 · 赞同 2**
> 力扣：[847. 访问所有节点的最短路径](https://leetcode.cn/problems/shortest-path-visiting-all-nodes/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

847.访问所有节点的最短路径

[力扣](https://leetcode-cn.com/problems/shortest-path-visiting-all-nodes/)

邮递员问题的简化版。原版的邮递员问题是一个np难的问题，目前也只存在一些精度比较好的近似解。不过注意到本题的点数非常少，因此可以使用状态压缩动态规划来解决。

设f[state][x]表示当前已经访问过了state这些点，最后处于x这一点上所需的最少步数。这里的state为二进制的01串，其中从低到高第k位表示编号为k的点是否被访问过。

由于这里所有的边长度都为1，因此可以直接进行bfs。对于f[state][x]，我们可以枚举与x相邻的所有节点next，那么如果我们此时从x走到next，访问过的节点状态就从state变成了new_state \= state | (1 \<\< next)，此时就是f[new_state][next]。若该状态未出现过，那么就有f[new_state][next] \= f[state][x] + 1，同时将该状态加入到bfs队列中即可。

若某次行动后的new_state包含了所有节点，就可以直接返回对应的f[new_state][next]。

最后附上python代码：

```python
class Solution(object):
    def shortestPathLength(self, graph):
        """
        :type graph: List[List[int]]
        :rtype: int
        """

        n = len(graph)
        f = [[None] * n for _ in range(1 << n)]
        q = []
        for i in range(n):
            f[1 << i][i] = 0
            q.append([1 << i, i])
        
        l = 0
        r = len(q)
        while l < r:
            for index in range(l, r):
                state, x = q[index]
                for next in graph[x]:
                    next_state = state | (1 << next)
                    if f[next_state][next] is None:
                        f[next_state][next] = f[state][x] + 1
                        q.append([next_state, next])
                        if next_state == (1 << n) - 1:
                            return f[next_state][next]
            
            l, r = r, len(q)

        return 0
```
