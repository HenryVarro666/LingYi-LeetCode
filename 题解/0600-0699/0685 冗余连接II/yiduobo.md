---
title: "685. 冗余连接II"
aliases: ["yiduobo的每日leetcode 685.冗余连接II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/304597823"
zhihu_id: "304597823"
zhihu_title: "yiduobo的每日leetcode 685.冗余连接II"
question_id: "685"
question: "冗余连接II"
problem_url: "https://leetcode.cn/problems/redundant-connection-ii/"
created: "2020-11-21T17:59:15+08:00"
updated: "2020-11-22T14:24:05+08:00"
upvotes: 1
comments: 0
---

# 685. 冗余连接II

> **[yiduobo的每日leetcode 685.冗余连接II](https://zhuanlan.zhihu.com/p/304597823) · 知乎 · 2020-11-21 · 赞同 1**
> 力扣：[685. 冗余连接II](https://leetcode.cn/problems/redundant-connection-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

685.冗余连接II

[力扣](https://leetcode-cn.com/problems/redundant-connection-ii/)

相比上一题，这一题从无向图变为了有向图。使用并查集依然可以做，但是相对复杂一点，我在这里利用了一些图论的知识来解决问题。

在有向图中，每个节点都有入度和出度的概念，入度表示有多少条边指向该节点，出度则表示有多少条边以该节点为起点。对于一颗树而言，其根节点的入度为0，而其余所有的节点的入度为1，出度则没有限制。

那么对于题目给出的图，可能存在以下几种情况：

1、某个点p的入度为2：

此时有两条边指向p，分别设为e1和e2，显然，我们需要删去其中的某条边，此时又可以分为两种情况：

e1或e2在环上：

1 -> 2

^ |

| v

4 \<- 3 \<- 5

此时3号点入度为2，有(2, 3)以及(5, 3)这两条边指向3号点，其中(2, 3)处于环上，因此此时应该删去环上的边(2, 3)

e1和e2都不在环上：

1 -> 2

| |

v v

4 -> 3

此时3号点入度为2，有(2, 3)以及(4, 3)这两条边指向3号点。此时删去(2, 3)与(4, 3)都能得到一棵树，因此按题目要求应该删去(2, 3)和(4, 3)中较晚出现的那一条边。

2、所有点的入度都为1：

1 -> 2

^ |

| v

4 \<- 3 -> 5

此时删去环上的任意一条边都可以形成树，因此应该删去环上最晚出现的那条边。

接下来的问题就变成了如何找环。我在这里采用的方法对于每个节点，记录其入边的起始节点，对于特殊的入度为2的节点则记录下其两条入边的起始节点。

在情况1中，从入度为2的点p开始，先尝试从e1的方向不断往其入边的起始节点走，直到走回p或者无法继续走为止。若走回了p，说明找到了环，那么答案为e1，否则尝试从e2的方向走，直到走回p或者无法继续走。若走回了p，那么答案就是e2，否则就是e1和e2中较晚出现的那一条。

在情况2中，从任意节点开始往入边的起始节点走，直到走到某个已经走过我的节点q为止。接下来从q开始往入编的起始节点走，直到走回q，期间最晚出现的边为最后的答案。

最后附上python代码：

```python
class Solution(object):
    def findRedundantDirectedConnection(self, edges):
        """
        :type edges: List[List[int]]
        :rtype: List[int]
        """

        edge_dict = {}
        n = len(edges)
        fa = [None] * n
        p = q = None
        for index, edge in enumerate(edges):
            x, y = edge
            x -= 1
            y -= 1
            edge_dict[(x, y)] = index
            if fa[y] is not None:
                p = y
                q = fa[y]
            fa[y] = x

        if p is not None:
            now = q
            while now != p and fa[now] is not None:
                now = fa[now]
            if now == p:
                return [q + 1, p + 1]
            
            now = p
            while fa[now] is not None:
                now = fa[now]
                if now == p:
                    return [fa[p] + 1, p + 1]

            if edge_dict[(q, p)] < edge_dict[(fa[p], p)]:
                return [fa[p] + 1, p + 1]
            else:
                return [q + 1, p + 1]

        p = 0
        used = [False] * n
        used[0] = True

        while True:
            p = fa[p]
            if used[p]:
                break
            used[p] = True

        now = p
        res = None
        while True:
            if res is None or edge_dict[(fa[res], res)] < edge_dict[(fa[now], now)]:
                res = now
            now = fa[now]
            if now == p:
                break

        return [fa[res] + 1, res + 1]
```
