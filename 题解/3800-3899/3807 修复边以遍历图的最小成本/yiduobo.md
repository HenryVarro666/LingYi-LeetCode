---
title: "3807. 修复边以遍历图的最小成本"
aliases: ["yiduobo的每日leetcode 3807.修复边以遍历图的最小成本"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1996359778415444233"
zhihu_id: "1996359778415444233"
zhihu_title: "yiduobo的每日leetcode 3807.修复边以遍历图的最小成本"
question_id: "3807"
question: "修复边以遍历图的最小成本"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-repair-edges-to-traverse-a-graph/"
created: "2026-01-18T23:42:24+08:00"
updated: "2026-01-18T23:42:24+08:00"
upvotes: 1
comments: 0
---

# 3807. 修复边以遍历图的最小成本

> **[yiduobo的每日leetcode 3807.修复边以遍历图的最小成本](https://zhuanlan.zhihu.com/p/1996359778415444233) · 知乎 · 2026-01-18 · 赞同 1**
> 力扣：[3807. 修复边以遍历图的最小成本](https://leetcode.cn/problems/minimum-cost-to-repair-edges-to-traverse-a-graph/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3807.修复边以遍历图的最小成本

[3807. 修复边以遍历图的最小成本 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-cost-to-repair-edges-to-traverse-a-graph/description/)

题目给出一个由n个节点组成的无向图，这些节点的下标编号从0到n - 1。图中由m条边，由一个二维整数数组edges表示，其中edges\[index\] \= \[u\[index\], v\[index\], w\[index\]\]，表示u\[index\]与v\[index\]之间有一条修复成本为w\[index\]的边。在初始状态下，图中所有边都是损坏的。

另外给出一个整数k，现在要求找出一个最小的非负整数money，使得可以从0号节点出发，经过至多k条修复成本都不超过money的边之后可以到达n - 1。若不存在这样的money，则返回-1。

首先可以明确的是，随着money的增大，就相当于在之前可用边的基础上新增了一些可用边，从0到达n - 1的可能性就越大，因此在这里可以二分答案，将问题转化为对于当前给出的mid，能否只经过最多k条w不超过mid的边从0到达n - 1。

二分的下界自然选择1，而上界则可以选择最大边权ma再加上1，这里取ma + 1的理由是若取ma + 1依然无法到达，说明不存在合法的money。

接下来对于当前的mid，可以从节点0开始做bfs，一共扩展k轮。每一轮都将与当前节点相邻且边权不超过mid的节点加入队列中，若n - 1最终加入到了队列，说明mid够用，此时应该调整二分上界为mid，否则调整二分下界为mid + 1。

二分答案结束后，若最终的left为ma + 1，则说明无解，此时应该返回-1，否则返回left即可。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, n, edges, k):
        """
        :type n: int
        :type edges: List[List[int]]
        :type k: int
        :rtype: int
        """
        
        ma = 0
        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append((y, w))
            g[y].append((x, w))
            ma = max(ma, w)
        
        left = 1
        right = ma + 1

        while left < right:
            mid = (left + right) // 2
            q = [0]
            vis = set([0])
            head, tail = 0, 1
            step = 0
            while head < tail and step < k:
                for x in q[head: tail]:
                    for y, w in g[x]:
                        if w <= mid and y not in vis:
                            vis.add(y)
                            q.append(y)
                if n - 1 in vis:
                    break
                
                head, tail = tail, len(q)
                step += 1

            if n - 1 in vis:
                right = mid
            else:
                left = mid + 1
        
        if left == ma + 1:
            res = -1
        else:
            res = left
        
        return res
```
