---
title: "3383. 施法所需最低符文数量"
aliases: ["yiduobo的每日leetcode 3383.施法所需最低符文数量"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/graph", "leetcode/recursion", "题单/图论算法", "题单/图论算法/六-强连通分量/双连通分量"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/29559180610"
zhihu_id: "29559180610"
zhihu_title: "yiduobo的每日leetcode 3383.施法所需最低符文数量"
question_id: "3383"
question: "施法所需最低符文数量"
problem_url: "https://leetcode.cn/problems/minimum-runes-to-add-to-cast-spell/"
difficulty: "Hard"
created: "2025-03-12T00:04:56+08:00"
updated: "2025-03-12T00:04:56+08:00"
upvotes: 0
comments: 0
---

# 3383. 施法所需最低符文数量

> **[yiduobo的每日leetcode 3383.施法所需最低符文数量](https://zhuanlan.zhihu.com/p/29559180610) · 知乎 · 2025-03-12 · 赞同 0**
> 力扣：[3383. 施法所需最低符文数量](https://leetcode.cn/problems/minimum-runes-to-add-to-cast-spell/) · Hard · 灵茶山艾府：[强连通分量 + 缩点](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3383.施法所需最低符文数量

[3383. 施法所需最低符文数量 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-runes-to-add-to-cast-spell/)

Alice刚从巫师学校毕业，希望施展一个魔法咒语来庆祝。

魔法咒语包含某些需要集中魔力的焦点，其中一些焦点含有作为咒语能量源的魔法水晶。焦点可以通过有向符文进行连接，这些符文将魔力流从一个焦点传输到另一个焦点。

给出一个整数n表示焦点的数量，以及一个整数数组ctrstals，其中ctrstals[i]表示有魔法水晶的焦点。同时给定两个整数数组flowFrom和flowTo，表示存在的有向符文。第i个符文允许魔力流从焦点flowFrom[i]传输到焦点flowTo[i]。

问Alice至少需要需要添加多少条有向符文，才能使得每个焦点要么包含一个魔力水晶，要么可以从其他焦点接收魔力流。

---

题目描述花里胡哨的一大堆，连有向符文这种词都给造出来了。实际上题目就是给出一个有向图，这张图中某些节点一开始被标记了。问至少需要添加多少条有向边，才能使得图中所有节点要么被标记，要么可以从图中另一个被标记的节点沿有向边抵达。

首先可以明确的是，对于图中入度为0的节点，若其一开始没有被标记，那么就必须新建一条从标记点指向这个点的有向边，而对于其他节点，则有可能从其他被标记节点沿有向边抵达，所以还不能确定是否需要连边。

这里说的不能确定，是因为图中还可能存在规模大于等于2的强连通分量。强连通分量的定义是某个子图，这个子图中的点两两之间都可以互相抵达，那么规模大于等于2的强连通分量中，节点入度都不为0。但是这个强连通分量中没有被标记节点，同时也没有被别的有向边指向，那么就必须从强连通分量中选取一个节点，从被标记节点出发建立有向边指向该节点。

对于强连通相关的问题，一种常见的处理方法是先对有向图执行一次tarjan算法，找出图中所有的强连通分量，然后将强连通分量收缩成一个单独的点。这样一来，整张图就可以转换成有向无环图，此时再从被标记节点，向所有所有入度为0的节点且没有被标记的节点建立有向边就行了。

在我的理解里，tarjan算法是基于dfs序以及dfs树中边的分类性质，通过某个节点的dfs序以及其子树中节点可以访问到的最早dfs序来判断这个节点是否为某个连通分量在dfs树中的起始节点，从而来确定强连通分量的算法。更具体的说明有兴趣的朋友可以自行搜索下，我在这里就不展开了。

最后附上python代码：

```python
class Solution(object):
    def minRunesToAdd(self, n, crystals, flowFrom, flowTo):
        """
        :type n: int
        :type crystals: List[int]
        :type flowFrom: List[int]
        :type flowTo: List[int]
        :rtype: int
        """
        
        g = [[] for _ in range(n)]
        for x, y in zip(flowFrom, flowTo):
            g[x].append(y)
        
        global t, tot
        t = 0
        tot = 0
        low = [0] * n
        dfn = [0] * n
        stack = []
        in_stack = [False] * n
        belong = [-1] * n

        def tarjan(u):
            global t, tot
            t += 1
            low[u] = t
            dfn[u] = t
            stack.append(u)
            in_stack[u] = True

            for v in g[u]:
                if dfn[v] == 0:
                    tarjan(v)
                    low[u] = min(low[u], low[v])
                elif in_stack[v]:
                    low[u] = min(low[u], dfn[v])
            
            if low[u] == dfn[u]:
                v = -1
                while v != u:
                    v = stack.pop()
                    belong[v] = tot
                    in_stack[v] = False
                tot += 1
        
        for x in range(n):
            if dfn[x] == 0:
                tarjan(x)
        
        new_g = [set() for _ in range(tot)]
        ind = [0] * tot
        for x, y in zip(flowFrom, flowTo):
            if belong[x] != belong[y] and belong[y] not in new_g[belong[x]]:
                new_g[belong[x]].add(belong[y])
                ind[belong[y]] += 1

        ctrstals_set = set()
        for x in crystals:
            ctrstals_set.add(belong[x])

        res = 0
        for x in range(tot):
            if x not in ctrstals_set and ind[x] == 0:
                res += 1

        return res
```
