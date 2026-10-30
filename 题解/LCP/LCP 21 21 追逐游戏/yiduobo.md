---
title: "LCP 21. 追逐游戏"
aliases: ["yiduobo的每日leetcode LCP21.追逐游戏"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/572693981"
zhihu_id: "572693981"
zhihu_title: "yiduobo的每日leetcode LCP21.追逐游戏"
question_id: "LCP 21"
question: "追逐游戏"
created: "2022-10-12T02:06:33+08:00"
updated: "2022-10-12T02:06:33+08:00"
upvotes: 0
comments: 0
---

# LCP 21. 追逐游戏

> **[yiduobo的每日leetcode LCP21.追逐游戏](https://zhuanlan.zhihu.com/p/572693981) · 知乎 · 2022-10-12 · 赞同 0**
> 力扣：LCP 21. 追逐游戏

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP21.追逐游戏

[力扣](https://leetcode.cn/problems/Za25hA/)

题目给出一张n个点、n条边的连通图，并给出小力和小扣的初始位置，问两人都在最优的策略下小力需要多少回合才能抓到小扣。

在对二人的行动策略进行分析之前，可以先分析一下这张图的形态。已知n个点，n - 1条边的连通图是一颗树，那么在数中增加一条边，得到的将会是一个环，以及与环相邻的若干条链。形象点来说，就是类似于简笔画的太阳，环就是太阳中心的圆，并且有若干条链从环上的某些节点向外发出。

接下来分析二人的行动策略。

通过题目给出的两个样例可以发现，由于图中存在环，那么有一种可能就是小扣随着小力的移动在环上绕圈，使得小力永远都抓不住小扣。可以发现，要达成这种情况需要满足两个条件：

1、环的长度必须大于3，否则一旦小力来到环上，环上剩余的两个节点就都会与小力相邻

2、设小扣最少需要k步走到环上的某个节点entrance，那么一旦小力捷足先登，在k - 1步之内就能来到entrance，那么小扣就没有机会能成功走到环上

对于上面两种情况，需要知道：

1、图中哪些节点在环上

2、小扣最少需要多少步才能来到环上，将会来到环上的哪个点

3、小力最少需要多少步才能走到小扣最快到达环上的那个点

接下来分别进行考虑。

首先是图中哪些点在环上。根据前面的描述，不妨从简笔画太阳的各个链入手，因为这些链的端点只与图中另一个节点相连，即度为1。而将这些节点删去之后，链上新的端点的度也变成了1，那么只需重复这个过程，就可以将所有链上的节点全部删去，剩下的就是环了。

具体实现上，可以使用类似拓扑排序的做法，先将度为1的节点加入到队列，然后开始bfs。每次将当前节点相邻节点的度减去1，若这个相邻节点的度变为了1，那么也将其加入到bfs队列中。bfs完成后，没有被加入队列中的节点就是环上的节点了。

接下来是需要小扣最少需要多少步才能走到环上。这一步比较简单，直接从小扣的起始位置开始bfs，直到某一时刻走到环上为止。在这里不妨把小扣走到图中每个位置所需的最少步数都计算出来，方便后面使用。

记小扣需要k步走到环上的某个节点entrance，那么最后一步，计算小力需要多少步才能走到entrance，同样只需要从小力的起始位置开始进行bfs就行了。在这里不妨也把小力走到图中每个位置所需的最少步数也计算出来，方便后面使用。

到了这里，就可以通过环的长度，以及小力和小扣走到entrance所需的时间来判读是否会出现小力永远都追不上小扣的情况。如果是，那么直接返回-1就行了。

如果最终小力可以追上小扣，那么小扣的目标就是尽量躲远一点，让小力没那么快追上小扣。这种情况下，只需要从小扣的起始位置开始进行bfs，寻找所有小扣有机会到达的位置，然后从中选出小力到达该位置所需时间最大的那一个即可。这里所说的小扣有机会到达的位置，指的是在对于某个位置p，小力来到p的时间x相比小扣来到p的时间y，满足x - y > 1，这样才能保证小扣不会在来到p这个位置时立即被小力抓住。

最后附上python代码：

```python
class Solution(object):
    def chaseGame(self, edges, startA, startB):
        """
        :type edges: List[List[int]]
        :type startA: int
        :type startB: int
        :rtype: int
        """

        g = {}
        d = {}
        n = len(edges)
        for x, y in edges:
            d[x] = d.get(x, 0) + 1
            d[y] = d.get(y, 0) + 1
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)
        
        if startB in g[startA]:
            return 1
        
        q = []
        chain = set()
        for index in range(1, n + 1):
            if d[index] == 1:
                q.append(index)
                chain.add(index)
        
        head, tail = 0, len(q)
        while head < tail:
            now = q[head]
            head += 1
            for next in g[now]:
                d[next] -= 1
                if d[next] == 1:
                    q.append(next)
                    tail += 1
                    chain.add(next)
        
        def bfs(start, dis):
            dis[start] = 0
            q = [start]
            head, tail = 0, 1
            while head < tail:
                now = q[head]
                head += 1
                for next in g[now]:
                    if dis[next] is None:
                        dis[next] = dis[now] + 1
                        q.append(next)
                        tail += 1
        
        disA = [None] * (n + 1)
        bfs(startA, disA)
        disB = [None] * (n + 1)
        bfs(startB, disB)

        if n - len(chain) > 3:
            entrance = None
            b_to_circle = None
            for index in range(1, n + 1):
                if index not in chain and (b_to_circle is None or b_to_circle > disB[index]):
                    b_to_circle = disB[index]
                    entrance = index
            
            if disA[entrance] > b_to_circle + 1:
                return -1
        
        q = [startB]
        head, tail = 0, 1
        vis = set([startB])
        while head < tail:
            now = q[head]
            head += 1
            for next in g[now]:
                if disA[next] - 1 > disB[next] and next not in vis:
                    q.append(next)
                    vis.add(next)
                    tail += 1
        
        res = 0
        for index in vis:
            res = max(res, disA[index])
        return res
```
