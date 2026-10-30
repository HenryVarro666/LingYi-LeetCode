---
title: "1595. 连通两组点的最小成本"
aliases: ["yiduobo的每日leetcode 1595.连通两组点的最小成本"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/bitmask", "题单/动态规划", "题单/图论算法", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/图论算法/八-网络流"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/432304203"
zhihu_id: "432304203"
zhihu_title: "yiduobo的每日leetcode 1595.连通两组点的最小成本"
question_id: "1595"
question: "连通两组点的最小成本"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-connect-two-groups-of-points/"
difficulty: "Hard"
rating: 2538
created: "2021-11-12T19:28:58+08:00"
updated: "2021-11-12T19:28:59+08:00"
upvotes: 2
comments: 2
---

# 1595. 连通两组点的最小成本

> **[yiduobo的每日leetcode 1595.连通两组点的最小成本](https://zhuanlan.zhihu.com/p/432304203) · 知乎 · 2021-11-12 · 赞同 2**
> 力扣：[1595. 连通两组点的最小成本](https://leetcode.cn/problems/minimum-cost-to-connect-two-groups-of-points/) · Hard · 灵茶山艾府：[教你一步步思考动态规划！（附题单）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1595.连通两组点的最小成本

[力扣](https://leetcode-cn.com/problems/minimum-cost-to-connect-two-groups-of-points/)

想不到居然可以在leetcode上看到网络流的题目。按题目的规模来看，可能是想要给出一种状态压缩动态规划的解法，不过还存在效率高得多的做法，也就是网络流。相比于状态压缩的指数级复杂度，网络流是一个多项式复杂度的算法。

先简单说一下网络流是什么，比较常见的就是最大流和费用流这两种。

先说说最大流。举个例子，现在自来水厂架设了一些管道，最终连接到了我家里。现在知道了这些管道在任意时刻可以通过的最大的水流量，问自来水厂开闸后，同一时刻最多能有多少水流到我家。

按图论来对这个问题建模，就是存在一个源点，即自来水厂，以及一个汇点，就是我家，然后图中有若干节点和边，其中所有的边都存在一个流量上限。

对于这个问题，解法大致分为两个种类，一种是增广路径，另一种是预流推进。我只对增广路径相关的解法有所了解，其主要思路就是突出一个反向容量。简单来说就是一开始也并不知道要怎么规划这个流量，于是就先按某种方法规划一道流量，对于这道流量经过的边，若这道流量的大小为k，那么原始图中边的容量已经使用了k，那么剩余的容量就应该减去k。与此同时，还需要在图中架设反向的边，其容量大小则应该加上k。

我个人是非常喜欢这种做法的，大致上算是突出了一种，虽然不知道以后会怎么样，但是先大胆尝试，同时留下后路，万一选错了还可以想办法弥补回来的思路。

关于最大流的具体实现，常见的有dinic和sap算法，在这里就不展开了。

接下来说说费用流。一般常见的问题也就是求最小费用下的最大流。按上面的例子，就是对于每条管道，一单位的水通过就要收取若干的费用，每条管道的收费标准可能各不相同，问最后至少要花多少钱，才能让最多的水流到我家。

按图论来建模与上面的最大流类似，不过此时的边除了容量之外还有费用的属性。只与求解方式呢，依然是增广路径相关，但是为了让费用最少，自然就想到使用最短路来找增广路径了。

最小费用的具体实现呢，一般是用spfa或者dijkstra来找增广路径，同样是不再展开了。

回到本题。不妨设两组中的点数分别为m和n，那么对于两组中的点，每个点都至少需要使用一次，而左侧的点最多使用次数是n，即该点与右侧所有点都进行配对。那么按网络流的思路来看的话，对于每个左侧的点，经过该点的流量下限为1，上限为n，也就是说从源点连接到该点的管道，其流量上限为n，下限为1。

类似的，右侧的点最多的使用次数则为m，那么从该点连接到汇点的管道，其流量上限为m，下限为1。

对于左侧和右侧之间的管道，流量的上限为1，下限为0，表示可用可不用。但是除此之外，这些管道还有费用属性，也就是对应到了题目中的权重。另外，与源汇相连的管道是的费用属性为0。

这样一来，一个有流量下限的最小费用最大流问题的图就构造出来了。这个问题与上面提到的最小费用最大流相比，还存在一个额外条件，就是部分的管道是有流量下限的。对于这个问题，则可以通过对图变形转化为常规的最小费用最大流问题来求解，在这里同样不再展开了。

有兴趣的同学可以先去系统性地了解一下网络的基础知识，之后对于这种改图的操作就会有非常直观的理解，否则我在这里扯一大堆如何操作变形，最后看着还是一头雾水。

最后附上python代码，其中的c为边的容量，v为边的费用，原始图中的源汇分别是s和t：

```python
class Solution(object):
    def connectTwoGroups(self, cost):
        """
        :type cost: List[List[int]]
        :rtype: int
        """

        m = len(cost)
        n = len(cost[0])
        s = m + n
        t = s + 1
        super_s = t + 1
        super_t = super_s + 1

        c = [[0] * (super_t + 1) for _ in range(super_t + 1)]
        v = [[0] * (super_t + 1) for _ in range(super_t + 1)]

        for i in range(m):
            c[s][i] = n - 1
            c[super_s][i] = 1
        
        for j in range(m, m + n):
            c[j][t] = m - 1
            c[j][super_t] = 1

        c[t][super_s] = n
        c[s][super_t] = m - n
        c[super_t][s] = n
        c[t][s] = m * n - n
        c[s][t] = n

        for i in range(m):
            for j in range(n):
                c[i][j + m] = 1
                v[i][j + m] = cost[i][j]
                v[j + m][i] = -cost[i][j]
        
        res = 0
        while True:
            dis = [None] * (super_t + 1)
            prev = [None] * (super_t + 1)
            used = set([super_s])
            dis[super_s] = 0
            now = super_s
            while super_t not in used:
                min_dis = None
                next = None
                for index in range(super_t + 1):
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

            res += dis[super_t]
            now = super_t
            while now != super_s:
                c[now][prev[now]] += 1
                c[prev[now]][now] -= 1
                now = prev[now]
```
