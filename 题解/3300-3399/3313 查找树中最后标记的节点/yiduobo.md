---
title: "3313. 查找树中最后标记的节点"
aliases: ["yiduobo的每日leetcode 3313.查找树中最后标记的节点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1711062409"
zhihu_id: "1711062409"
zhihu_title: "yiduobo的每日leetcode 3313.查找树中最后标记的节点"
question_id: "3313"
question: "查找树中最后标记的节点"
problem_url: "https://leetcode.cn/problems/find-the-last-marked-nodes-in-tree/"
created: "2024-10-18T04:34:36+08:00"
updated: "2024-10-18T04:34:50+08:00"
upvotes: 1
comments: 0
---

# 3313. 查找树中最后标记的节点

> **[yiduobo的每日leetcode 3313.查找树中最后标记的节点](https://zhuanlan.zhihu.com/p/1711062409) · 知乎 · 2024-10-18 · 赞同 1**
> 力扣：[3313. 查找树中最后标记的节点](https://leetcode.cn/problems/find-the-last-marked-nodes-in-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3313.查找树中最后标记的节点

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-last-marked-nodes-in-tree/description/)

题目给出一颗有n个节点，编号在0到n - 1之间的无向树，树中的边由数组edges表示，其中edges\[i\] \= \[u\[i\], v\[i\]\]表示在节点u\[i\]到v\[i\]之间有一条边。

最开始，所有节点都未被标记，接下来每一秒，需要标记所有的与已标记节点相邻且还未被标记的节点。

对于树中的每个节点，问假设在时刻0标记了该节点，那么这种情况下树中最后被标记的节点是哪一个。如果有多个可以任选一个作为答案。

本题中每一轮都需要标记相邻节点，那么问题实际上就是问对于树中的每个节点，与这个节点距离最远的节点是哪一个。这与之前的3241题本质上是一样的，差别在于3241计算距离的方式不一样，而本题除了最远距离还需要维护最远节点。

[yiduobo：yiduobo的每日leetcode 3241.标记所有节点需要的时间](https://zhuanlan.zhihu.com/p/721004825)

对于本题，直接按3241相同的方法处理即可，需要注意在处理距离的同时需要一并处理最远节点。

最后附上python代码：

```python
class Solution(object):
    def lastMarkedNodes(self, edges):
        """
        :type edges: List[List[int]]
        :rtype: List[int]
        """

        n = len(edges) + 1

        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        f = [0] * n
        farthest = [None] * n

        def dfs(now, fa):
            farthest[now] = now
            for nxt in g[now]:
                if nxt == fa:
                    continue
                dfs(nxt, now)
                if f[nxt] + 1 > f[now]:
                    f[now] = f[nxt] + 1
                    farthest[now] = farthest[nxt]

        dfs(0, -1)
        
        res = [0] * n

        def calc(now, fa):

            first_dis = second_dis = 0
            first_far = second_far = 0
            for nxt in g[now]:
                cost = f[nxt] + 1
                if cost > first_dis:
                    first_dis, second_dis = cost, first_dis
                    first_far, second_far = farthest[nxt], first_far
                elif cost > second_dis:
                    second_dis = cost
                    second_far = farthest[nxt]

            res[now] = first_far
            f[now] = first_dis
            farthest[now] = first_far

            for nxt in g[now]:
                if nxt == fa:
                    continue
                cost = f[nxt] + 1
                if cost == first_dis and farthest[nxt] == first_far:
                    f[now] = second_dis
                    farthest[now] = second_far
                    calc(nxt, now)
                    f[now] = first_dis
                    farthest[now] = first_far
                else:
                    calc(nxt, now)

        calc(0, -1)
        return res
```
