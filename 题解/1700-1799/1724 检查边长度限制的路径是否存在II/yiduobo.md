---
title: "1724. 检查边长度限制的路径是否存在II"
aliases: ["yiduobo的每日leetcode 1724.检查边长度限制的路径是否存在II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/620469673"
zhihu_id: "620469673"
zhihu_title: "yiduobo的每日leetcode 1724.检查边长度限制的路径是否存在II"
question_id: "1724"
question: "检查边长度限制的路径是否存在II"
problem_url: "https://leetcode.cn/problems/checking-existence-of-edge-length-limited-paths-ii/"
created: "2023-04-09T04:06:48+08:00"
updated: "2023-04-09T04:06:48+08:00"
upvotes: 0
comments: 0
---

# 1724. 检查边长度限制的路径是否存在II

> **[yiduobo的每日leetcode 1724.检查边长度限制的路径是否存在II](https://zhuanlan.zhihu.com/p/620469673) · 知乎 · 2023-04-09 · 赞同 0**
> 力扣：[1724. 检查边长度限制的路径是否存在II](https://leetcode.cn/problems/checking-existence-of-edge-length-limited-paths-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1724.检查边长度限制的路径是否存在II

[力扣](https://leetcode.cn/problems/checking-existence-of-edge-length-limited-paths-ii/)

之前1697题的加强版。

[yiduobo：yiduobo的每日leetcode 1697.检查边长度限制的路径是否存在](https://zhuanlan.zhihu.com/p/447844384)

在本题中，强制要求使用在线算法，因此之前的离线算法不再适用，但是其中的思路是可以借鉴的。

对于1697题，实际上可以认为是构造了一颗最小生成树，在这个构造过程中检测询问中的点是否处于同一子树中。而对于本题，则需要提前将这颗最小生成树构造出来，然后对于每个询问，需要查询的就是这两个节点间的路径中权重最大的边是否小于limit。而这个问题，则可以转化先找出这两个节点的最近公共祖先LCA，以及这两个节点到LCA的路径上权重最大的边，然后检测边权是否小于limit。

问题到了这里，就需要找到一种高效的LCA求解方法，一种常见的处理方法是利用倍增的动态规划算法。令f[u][level]表示从节点u向上行走2^level步到的节点，以及这个行走路径的最大边权，那么对于f[u][level]：

1、当level \= 0时：

其目标节点就是u的父亲节点，此时可以先通过一次自顶向下的bfs求解出f中所有level为0对应的结果

2、当level > 0时：

从u往上走2^level这个操作，可以拆分成为先从u向上走2^(level - 1)步，来到中间点v，然后从v再向上走2^(level - 1)步，来到原始的目标节点。换言之，这里的f[u][level]就可以通过f[u][level - 1]以及f[v][level - 1]更新得到

计算得到f数组后，计算p和q的LCA就可以遵从一下的规则进行：

1、首先将p和q调整到同一深度，也就是通过上面求得的f数组，从p和q中较深的节点向上行走，直到二者的深度相同

2、接下来让p和q同时通过上面求得的f数组向上行走，每次行走的步长应该选择最大的level，这个level可以等于0，而当level大于0时，则需要保证向上行走2^level步之后p和q不会来到同一个节点

在行走的过程中，若当前行走经过的最大边权超过了limit，那么就返回false。反之若p和q能成功走到一起，那么就返回true。

这里的level是单调递减的，因此行走的轮次最多只有log(h)次，这里的h是树的深度，最坏情况下h \= n，因此这里每次询问的时间复杂度就是O(log(n))。

另外需要特别注意的是，本题的节点可能不连通，那么在这里可以新增一个超级树根，从每条边向这个根节点发出一条长度为10^9 + 1的边，这样一来就可以在不影响结果的情况下将所有节点置于同一颗树中。

最后附上python代码：

```python
class DistanceLimitedPathsExist(object):

    def __init__(self, n, edgeList):
        """
        :type n: int
        :type edgeList: List[List[int]]
        """

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        fa = range(n + 1)
        g = {u : {} for u in range(n + 1)}
        for u, v, d in sorted(edgeList, key=lambda d:d[-1]):
            fa_u = find(u)
            fa_v = find(v)
            if fa_u != fa_v:
                if fa_u < fa_v:
                    fa[fa_u] = fa_v
                else:
                    fa[fa_v] = fa_u
        
                g[u][v] = g[v][u] = d

        max_dis = 10 ** 9 + 1
        for u in range(n):
            fa_u = find(u)
            if fa_u != n:
                g[n][u] = max_dis
                fa[fa_u] = n
        
        self.f = [[] for _ in range(n + 1)]
        self.level = [0] * (n + 1)
        q = [n]
        self.level[n] = 0
        head, tail = 0, 1
        while head < tail:
            for u in q[head : tail]:
                for v in g[u]:
                    if self.level[v] != 0:
                        continue
                    d = g[u][v]
                    self.f[v].append([u, d])
                    q.append(v)
                    self.level[v] = self.level[u] + 1
            
            head, tail = tail, len(q)

        p = 1
        while True:
            flag = True
            for u in range(n):
                if len(self.f[u]) >= p:
                    v = self.f[u][p - 1][0]
                    if len(self.f[v]) >= p:
                        t = self.f[v][p - 1][0]
                        d = max(self.f[u][p - 1][1], self.f[v][p - 1][1])
                        self.f[u].append([t, d])
                        flag = False
            
            if flag:
                break

            p += 1

    def query(self, p, q, limit):
        """
        :type p: int
        :type q: int
        :type limit: int
        :rtype: bool
        """

        if self.level[p] < self.level[q]:
            p, q = q, p

        now = 0
        while self.level[p] != self.level[q]:
            i = len(self.f[p]) - 1
            while self.level[self.f[p][i][0]] < self.level[q]:
                i -= 1

            if self.f[p][i][1] >= limit:
                return False
            p = self.f[p][i][0]

        i = len(self.f[p]) - 1
        while p != q:
            while i >= len(self.f[p]) or (i > 0 and self.f[p][i][0] == self.f[q][i][0]):
                i -= 1
            
            if self.f[p][i][1] >= limit or self.f[q][i][1] >= limit:
                return False
            p = self.f[p][i][0]
            q = self.f[q][i][0]
        
        return True

# Your DistanceLimitedPathsExist object will be instantiated and called as such:
# obj = DistanceLimitedPathsExist(n, edgeList)
# param_1 = obj.query(p,q,limit)
```
