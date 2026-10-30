---
title: "1601. 最多可达成的换楼请求数目"
aliases: ["yiduobo的每日leetcode 1601.最多可达成的换楼请求数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/432311373"
zhihu_id: "432311373"
zhihu_title: "yiduobo的每日leetcode 1601.最多可达成的换楼请求数目"
question_id: "1601"
question: "最多可达成的换楼请求数目"
problem_url: "https://leetcode.cn/problems/maximum-number-of-achievable-transfer-requests/"
created: "2021-11-14T17:44:08+08:00"
updated: "2021-11-14T17:44:08+08:00"
upvotes: 0
comments: 0
---

# 1601. 最多可达成的换楼请求数目

> **[yiduobo的每日leetcode 1601.最多可达成的换楼请求数目](https://zhuanlan.zhihu.com/p/432311373) · 知乎 · 2021-11-14 · 赞同 0**
> 力扣：[1601. 最多可达成的换楼请求数目](https://leetcode.cn/problems/maximum-number-of-achievable-transfer-requests/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1601.最多可达成的换楼请求数目

[力扣](https://leetcode-cn.com/problems/maximum-number-of-achievable-transfer-requests/)

没想到才隔了没几题就又碰到了网络流的题目。

这一题的建图相对没有那么直观。题目要求从有向图中删去某些边，使得最终图中各个节点的入度和出度一样。

从网络流的角度来看，就是某些节点流入和流出的流量不一致，现在需要通过从源发出流量到某些节点，或者从某些节点发出流量到汇来平衡掉这些不一致的流量。

例如样例中1号楼有两个人想进去一个人想出来，那么就可以认为是2的流量想进入，1的流量想出来。为了达成平衡，其中1的想进入的流量就无处可去，此时则可以安排这份流量是从最终走到了汇。类似的，若某栋楼出来的人比进去的人多，那么这些多出来的人不能凭空产生，因此需要安排这份流量从源走到了该节点。

更抽象化一点，就是对于每个节点，统计其入度和出度。若入度大于出度，那么从该节点到汇点连一条容量为入度减去出度的边；反过来，若出度大于入度，则从源点到该节点连一条容量为出度减取入度的边。

而对于原始request中的边，则需要根据其在request中出现的次数来确定边的容量。

这样一来，在图中执行一次最大流，就相当于这些不平衡流量从原点出发，途经request中的某些边然后走到了汇点。经过的这些边承载了不平衡流量，也就是最终需要删去的边。

题目要求的是保留最多的request，换言之就是要尽可能少地牺牲request，而单纯的执行最大流只是找出了一个可行的方案，并不能保证牺牲掉的request最少。此时可以转换一下思路，将原始request中边的费用置为1，表示牺牲掉一条边代价为1，这样一来只需要在图中跑一次最小费用最大流，求得的最小费用就是最少需要牺牲request中边的数量了，此时只需将request的总数减去这个最小费用就是最终答案。

具体实现上，由于本题的图中费用权重只有0和1两种选项，因此无需使用最短路径，而是使用bfs就能找出每一轮的增广路径了。但是相对的，本题每一轮增广的容量不一定为1，因此需要先遍历增广路径上的所有边，取这些边容量的最小值作为本次的流量大小，根据这个流量大小并修正边的容量。

最后附上python代码：

```python
class Solution(object):
    def maximumRequests(self, n, requests):
        """
        :type n: int
        :type requests: List[List[int]]
        :rtype: int
        """

        s = n
        t = s + 1
        c = [[0] * (t + 1) for _ in range(t + 1)]
        v = [[0] * (t + 1) for _ in range(t + 1)]

        ind = [0] * n
        oud = [0] * n
        for x, y in requests:
            c[x][y] += 1
            v[x][y] = 1
            ind[y] += 1
            oud[x] += 1
        
        for index in range(n):
            if ind[index] > oud[index]:
                c[index][t] = ind[index] - oud[index]
            else:
                c[s][index] = oud[index] - ind[index]
        
        res = len(requests)
        while True:
            dis = [None] * (t + 1)
            prev = [None] * (t + 1)
            used = set([s])
            dis[s] = 0
            now = s
            while t not in used:
                min_dis = None
                next = None
                for index in range(t + 1):
                    if c[now][index] > 0 and (dis[index] is None or dis[index] > dis[now] + v[now][index]):
                        dis[index] = dis[now] + v[now][index]
                        prev[index] = now
                        if index in used:
                            used.remove(index)
                    if index not in used and dis[index] is not None and (min_dis is None or min_dis > dis[index]):
                        next = index
                        min_dis = dis[index]

                if min_dis is None:
                    return res
                
                used.add(next)
                now = next

            now = t
            f = None
            while now != s:
                if f is None or f > c[prev[now]][now]:
                    f = c[prev[now]][now]
                now = prev[now]
            
            res -= dis[t] * f
            now = t
            while now != s:
                c[now][prev[now]] += f
                c[prev[now]][now] -= f
                now = prev[now]
```
