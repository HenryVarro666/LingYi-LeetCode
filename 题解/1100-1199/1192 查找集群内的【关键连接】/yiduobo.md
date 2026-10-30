---
title: "1192. 查找集群内的【关键连接】"
aliases: ["yiduobo的每日leetcode 1192.查找集群内的【关键连接】"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/380941149"
zhihu_id: "380941149"
zhihu_title: "yiduobo的每日leetcode 1192.查找集群内的【关键连接】"
question_id: "1192"
question: "查找集群内的【关键连接】"
problem_url: "https://leetcode.cn/problems/critical-connections-in-a-network/"
created: "2021-06-15T22:31:34+08:00"
updated: "2021-06-15T22:31:34+08:00"
upvotes: 0
comments: 0
---

# 1192. 查找集群内的【关键连接】

> **[yiduobo的每日leetcode 1192.查找集群内的【关键连接】](https://zhuanlan.zhihu.com/p/380941149) · 知乎 · 2021-06-15 · 赞同 0**
> 力扣：[1192. 查找集群内的【关键连接】](https://leetcode.cn/problems/critical-connections-in-a-network/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1192.查找集群内的【关键连接】

[力扣](https://leetcode-cn.com/problems/critical-connections-in-a-network/)

无向图割边问题，经典的做法是tarjan算法。

简单来说，就是对于一个无向图而言，若从某一点开始进行dfs，那么整个dfs过程中可能遇到两种边，一种是向后延伸，访问还未访问过节点的的dfs边，另一种则是返回某个已经访问过的节点的回边。

可以明确的是，一旦出现某条回边，设回边是从q出发回到p，那么从p开始到q的dfs序列中所有节点之间的边都不会是割边，因为这些节点位于一个环上，两点之间至少存在两条路径。

那么一个自然的想法就是对于当前点q，我们需要设法找出其回边中dfs序最小的那一个，因为这样一来就可以涵盖其他回边的节点，于是我们在dfs过程中使用两个数组dfn和low，分别表示当前节点在dfs过程中访问的顺序，以及从该点出发能访问到的，且不是dfs序中的上一个节点的最早的节点的顺序，那么对于dfs的当前节点now：

1、首先置dfn[now] \= low[now] \= cnt，并将cnt加上1，表示now是第cnt个访问的节点，同时初始化low[now]为cnt

2、遍历now的邻居next，对于next，可能下面三种情况：

2-1）若dfn[next]为空，说明next还未被访问过，那么先递归求解next。那么从now出发，经过next之后可以走到low[next]，因此就有

low[now] \= min(low[now], low[next])

2-2）若next是dfs序列中now的上一个节点，那么直接跳过，因为now就是从next过来的，此时这条边对于计算low[now]没有用处

2-3）若dfn[next]不为空，且next不是dfs序列中now的上一个节点，那么说明now到next这条边就是一条回边，此时就应当使用next的dfs序来更新low[now]，也就是

low[now] \= min(low[now], dfn[next])

得到dfn和low之后，问题就变成了如何判断哪些是割边。根据上面的结论，若p到q之间只有唯一的一条路径，那么路径上的边就都是割边。换言之，割边必然是dfs边而不是回边，也就是说我们可以在dfs中出现情况1时进行判断，若此时的low[next] > dfn[now]，说明next没有方法回到now或者比now更早的节点，也就是说从now到next只有这唯一的一条边，因此这条边必然是割边。

最后提一嘴，这个算法的作者tarjan除了本算法之外，还发明了一系列的算法，不出意外的话之后有可能又要用到“tarjan算法”。

最后附上python代码：

```python
class Solution(object):
    def criticalConnections(self, n, connections):
        """
        :type n: int
        :type connections: List[List[int]]
        :rtype: List[List[int]]
        """

        g = {}
        for x, y in connections:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)
        
        dfn = [None] * n
        low = [None] * n
        res = []
        self.dfs(0, g, dfn, low, None, res, 0)
        return res

    def dfs(self, now, g, dfn, low, fa, res, cnt):
        dfn[now] = low[now] = cnt
        for next in g.get(now, set()):
            if dfn[next] is None:
                self.dfs(next, g, dfn, low, now, res, cnt + 1)
                low[now] = min(low[now], low[next])
                if low[next] > dfn[now]:
                    res.append([now, next])
            elif next != fa:
                low[now] = min(low[now], dfn[next])
```
