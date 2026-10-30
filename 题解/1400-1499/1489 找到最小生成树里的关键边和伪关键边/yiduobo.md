---
title: "1489. 找到最小生成树里的关键边和伪关键边"
aliases: ["yiduobo的每日leetcode 1489.找到最小生成树里的关键边和伪关键边"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/416690837"
zhihu_id: "416690837"
zhihu_title: "yiduobo的每日leetcode 1489.找到最小生成树里的关键边和伪关键边"
question_id: "1489"
question: "找到最小生成树里的关键边和伪关键边"
problem_url: "https://leetcode.cn/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/"
created: "2021-10-03T20:16:06+08:00"
updated: "2021-10-03T20:16:06+08:00"
upvotes: 0
comments: 0
---

# 1489. 找到最小生成树里的关键边和伪关键边

> **[yiduobo的每日leetcode 1489.找到最小生成树里的关键边和伪关键边](https://zhuanlan.zhihu.com/p/416690837) · 知乎 · 2021-10-03 · 赞同 0**
> 力扣：[1489. 找到最小生成树里的关键边和伪关键边](https://leetcode.cn/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1489.找到最小生成树里的关键边和伪关键边

[力扣](https://leetcode-cn.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/)

题目是与边有关的最小生成树问题，那么很自然想到使用kruskal算法来进行求解。

先回顾一下常规的做法：

首先，将边按照权重从小到大进行排序，接下来枚举每一条边。

对于当前边连接的x和y，通过并查集判断x和y当前属于那一个连通分量，若二者属于不同的连通分量，那么就将这两个连通分量连接成一个，并修改并查集中相应的父亲；若二者属于同一条边，那么就忽略这条边。

对于本题，需要找出不可替代的边以及可以被替代的边。根据上面的算法，那么将两个不同连通分量连接起来的这一类边，可能是关键边，也可能是伪关键边；而本身连接的是同一个连通分量的边，则可能是伪关键边，或者是完全就不需要的边。

那么在这里首先想办法剔除掉完全不需要的边。对于常规做法而言，这里不太好区分的地方是对于当前边(x, y, w)，若x和y属于同一个连通分量，那么说明之前有另一条边(x', y', w')将二者连通在了一起。若这里的w等于w'，那么这两条边都是可替代的伪关键边；若这里的w大于w'，那么当前边(x, y, w)就是完全不需要的边了。

但是在这里，由于是通过并查集这种轻量级的数据结构表示的连通性，那么无法判别在加入当前变之后，哪些边是可有可无的。

这里可以简单举出两个例子。一个是

1 - 2 - 3 - 4

这张图中，设所有边的权重都是1。接下来加入1到4的一条边，权重也是1，这样一来图中所有边都是伪关键边了。

考虑到上面这种情况，一种思路就是保存当前图中权值最大的边，但是这样的做法则有可能将无关的边牵扯进来。还是

1 - 2 - 3 - 4

这张图中，设所有边的权重都是1。接下来加入1到3的一条边，权重也是1，这样一来图中1到2、1到3以及2到3的这些边是伪关键边，而3到4则是关键边。但是如果通过保存当前连通分量中边的权值来确定哪些可能成为伪关键边的话，就可能误伤到3到4这条边。

对于以上的几种情况，都是由于当前边加入之前，就有同样权重的边已经加入图中，并改变了图的连通性，那么在这里可以修改一下做法，不再一条条边进行处理，而是对于权值相同的边一组组来进行处理。

这样一来，若当前边(x, y, w)中的x和y属于同一个连通分量时，就可以确定当前这个连通分量内的边权重必然小于w，因此当前边就是完全不需要的边，可以剔除了。

根据上面的分组做法，就可以有效剔除掉完全不需要的边，而接下来则需要分析哪些边是必不可少的。还是同样的问题，由于无法根据并查集确定边对图连通性的影响，因此在这里需要另想办法。

对于无向图中的关键边，另一种称呼为桥，而经典的求解方式就是tarjan算法。与连通性相关的tarjan算法都是一个路子，即从图中某一点开始进行dfs，并记录下dfs序。由于图中可能出现往回走的边，因此可以在dfs过程中也记录下可以访问到的dfs序最小的节点。接下来就可以通过对比当前的dfs序以及通过回边所能访问到的最小dfs序来确定当前节点或边是否是关键的节点或边了。

回到本题。在分组执行kruskal算法的过程中，首先剔除掉了完全不需要的边，接下来可以当前组里面剩下的边建图。需要注意的是建图时对于边(x, y, index)，连接的对象应该是fa[x]以及fa[y]，即二者所属的连通分量。建图完毕后，执行tarjan算法求解其中哪些边是桥。这样一来就可以区分出关键边和伪关键边了。

在时间复杂度方面，首先排序的时间复杂度为O(mlogm)。如果将并查集时间复杂度视为常数，那么分组kruskal的时间复杂度就是O(m)。而对于tarjan算法的执行而言，虽然看上去是循环套dfs是个平方的复杂度，但是实际上每次建图的大小上限是当前组中边的数目，每条边只会被处理一次，因此最终时间复杂度就是O(m)。

最后附上python代码：

```python
class Solution(object):
    def findCriticalAndPseudoCriticalEdges(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: List[List[int]]
        """

        edges = sorted([[x, y, w, index] for index, [x, y, w] in enumerate(edges)], key=lambda d:d[2])
        m = len(edges)
        l = 0
        fa = range(n)
        critical = []
        pseudo = []
        while l < m:
            r = l + 1
            while r < m and edges[r][2] == edges[l][2]:
                r += 1

            candidate = []
            cnt = 0
            g = {}
            node_mapping = {}
            self.pseudo_edge = set()
            for x, y, w, index in edges[l : r]:
                fa_x = self.find(x, fa)
                fa_y = self.find(y, fa)

                if fa_x != fa_y:
                    candidate.append([x, y, index])

                    if fa_x not in node_mapping:
                        node_mapping[fa_x] = cnt
                        cnt += 1
                    node_x = node_mapping[fa_x]
                    if node_x not in g:
                        g[node_x] = {}

                    if fa_y not in node_mapping:
                        node_mapping[fa_y] = cnt
                        cnt += 1
                    node_y = node_mapping[fa_y]
                    if node_y not in g:
                        g[node_y] = {}

                    if node_y in g[node_x]:
                        self.pseudo_edge.add(g[node_x][node_y])
                        self.pseudo_edge.add(index)
                    else:
                        g[node_x][node_y] = g[node_y][node_x] = index

            self.cut_edge = set()
            self.dfs_order = 0
            low = [None] * cnt
            dfn = [None] * cnt
            for now in range(cnt):
                if dfn[now] is None:
                  self.tarjan(now, None, g, low, dfn)

            for x, y, index in candidate:
                if index in self.cut_edge:
                    critical.append(index)
                else:
                    pseudo.append(index)
                
                fa_x = self.find(x, fa)
                fa_y = self.find(y, fa)
                if fa_x < fa_y:
                    fa[fa_y] = fa_x
                else:
                    fa[fa_x] = fa_y
            
            l = r

        return [critical, pseudo]
                
    def tarjan(self, now, fa, g, low, dfn):
        low[now] = dfn[now] = self.dfs_order
        self.dfs_order += 1
        for next, index in g[now].items():
            if dfn[next] is None:
                self.tarjan(next, index, g, low, dfn)
                low[now] = min(low[now], low[next])
                if low[next] > dfn[now] and index not in self.pseudo_edge:
                    self.cut_edge.add(index)
            elif index != fa:
                low[now] = min(low[now], dfn[next])

    def find(self, x, fa):
        if x != fa[x]:
            fa[x] = self.find(fa[x], fa)
        return fa[x]
```
