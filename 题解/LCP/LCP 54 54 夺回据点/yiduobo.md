---
title: "LCP 54. 夺回据点"
aliases: ["yiduobo的每日leetcode LCP54.夺回据点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/578035922"
zhihu_id: "578035922"
zhihu_title: "yiduobo的每日leetcode LCP54.夺回据点"
question_id: "LCP 54"
question: "夺回据点"
problem_url: "https://leetcode.cn/problems/s5kip/"
created: "2022-10-28T04:09:54+08:00"
updated: "2022-10-28T04:09:54+08:00"
upvotes: 0
comments: 0
---

# LCP 54. 夺回据点

> **[yiduobo的每日leetcode LCP54.夺回据点](https://zhuanlan.zhihu.com/p/578035922) · 知乎 · 2022-10-28 · 赞同 0**
> 力扣：[LCP 54. 夺回据点](https://leetcode.cn/problems/s5kip/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP54.夺回据点

[力扣](https://leetcode.cn/problems/s5kipK/)

从题目描述来看，由于魔物不能被分割成多个连通块，那么就意味着图中的割点需要在其某一侧完全被占据之后才能被占据。从样例1来分析，则可以发现：

1、单独将一个图中的双连通分量拎出来，可以从任意位置出发进行占据

2、如果这个双连通分量中存在一个割点，那么不能从这个割点出发，而是需要从非割点的某个点出发，先占据完其他点，最后再占据割点

更进一步的，如果某个双连通分量里面存在两个割点，那么在这两个割点的其他侧节点被占据之前，都不应该从双连通分量这一侧去占据这两个割点。换言之，对于这种情况，一开始就不应该占据双连通分量中的点。

更形象化的描述，可以发现如果将连通分量进行缩点操作，最后将会得到一颗树，其中仅有一个割点的连通分量为树的叶子节点，而其他的则为非叶子节点。对于这颗树来说，可以占据任意叶子节点，但是非叶子节点只能等其相邻节点被占据到只剩一个还没有被占据时，该节点才能被占据。

综合上面的结论，就可以先进行一趟dfs，利用tarjan算法计算出图中所有的割点以及双连通分量。tarjan算法在之前的很多题中都使用过，具体的算法细节这里就不展开了。

接下来，对于割点数仅为1个的双连通分量，需要占据这个双连通分量中值最小，且不是割点的一个点。

不过这样做的话存在一个问题就是浪费掉了一个节点，因为对于一个割点而言，只要将其除某一侧之外的其他节点全部占据，就可以先占据这个割点再去占据最后没有被情况的这一侧的点，也就是说这一侧并不需要一开始就被占据某个节点。因此，在这里可以找出占据点中值最大的点，选择放弃一开始就占据该点。

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, cost, roads):
        """
        :type cost: List[int]
        :type roads: List[List[int]]
        :rtype: int
        """

        n = len(cost)
        if n == 1:
            return cost[0]
        
        g = {}
        for x, y in roads:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)
        
        cut_pos = set()
        dfn = [None] * n
        low = [None] * n
        dcc = []
        stack = []

        global cnt
        cnt = 0

        def dfs(now):
            global cnt
            cnt += 1
            dfn[now] = low[now] = cnt
            stack.append(now)
            child_cnt = 0
            for next in g.get(now, set()):
                if dfn[next] is None:
                    dfs(next)
                    low[now] = min(low[now], low[next])
                    if low[next] >= dfn[now]:
                        child_cnt += 1
                        if now != 0 or child_cnt > 1:
                            cut_pos.add(now)
                        
                        dcc.append([])
                        while stack[-1] != next:
                            dcc[-1].append(stack[-1])
                            stack.pop()
                        dcc[-1].append(next)
                        stack.pop()
                        dcc[-1].append(now)
                    
                else:
                    low[now] = min(low[now], dfn[next])
        
        dfs(0)

        if len(dcc) == 1:
            return min(cost)

        ma_cost = 0
        res = 0
        for node_list in dcc:
            cnt = 0
            min_cost = None
            for now in node_list:
                if now in cut_pos:
                    cnt += 1
                elif min_cost is None or cost[now] < min_cost:
                    min_cost = cost[now]
            if cnt == 1:
                res += min_cost
                ma_cost = max(ma_cost, min_cost)

        return res - ma_cost
```
