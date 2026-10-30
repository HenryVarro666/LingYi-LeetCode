---
title: "743. 网络延迟时间"
aliases: ["yiduobo的每日leetcode 743.网络延迟时间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/shortest-path", "leetcode/heap-priority-queue", "题单/图论算法", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/337210889"
zhihu_id: "337210889"
zhihu_title: "yiduobo的每日leetcode 743.网络延迟时间"
question_id: "743"
question: "网络延迟时间"
problem_url: "https://leetcode.cn/problems/network-delay-time/"
difficulty: "Medium"
created: "2020-12-15T23:26:24+08:00"
updated: "2020-12-15T23:26:24+08:00"
upvotes: 0
comments: 0
---

# 743. 网络延迟时间

> **[yiduobo的每日leetcode 743.网络延迟时间](https://zhuanlan.zhihu.com/p/337210889) · 知乎 · 2020-12-15 · 赞同 0**
> 力扣：[743. 网络延迟时间](https://leetcode.cn/problems/network-delay-time/) · Medium · 灵茶山艾府：[两种 Dijkstra 写法，附题单（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

743.网络延迟时间

[力扣](https://leetcode-cn.com/problems/network-delay-time/)

经典的有向图上的单源最短路问题。有图题目保证边的权重非负，那么可以使用dijkstra算法来解决。dijkstra算法是一种贪心算法，其贪心的依据是：

对于当前的源头点p，设点x到p的距离为dis[x]，那么若目前到p距离最短的点为q，那么p到q的距离就必然是dis[q]，而不可能是p先经过某个中间点r，然后从r再到q，因为对于dis[q]而言，现在已知dis[r] >\= dis[q]，而由于图中边的权重非负，因此从r再到q的距离也必然非负，因此有dis[q] \<\= dis[r] + f(r, q)，其中f(r, q)表示r到q的最短距离。

有了上面的结论，我们就可以每次将离p最近的点加入到答案中，然后利用从该点出发的边来更新其他点到p的距离。重复这个过程直到计算出所有点的最短距离或者某些点无法到达为止。一共需要计算n轮，每轮需要找出dis数组中的最小值同时还需要更新dis数组中的部分权重，同时所有的边都将被处理一次，因此最终时间复杂度为O(n^2 + m)。由于图中没有自环以及重边，因此m的上界也就是节点之间两两相连，因此最终时间复杂度就是O(n^2)。

当然，很容易就发现这里每一轮求最小值这个操作是可以用堆进行优化的。使用一个堆维护当前节点以及该到起点的距离（u，dis），那么每一轮操作就从堆中弹出堆顶元素，若堆顶元素中的u已经在答案中，那么就继续弹出，直到堆为空或者u不在答案中。此时，u到起点的最短距离就是对应的dis。将其加入答案后，再遍历所有从u出发的边，对于其中的(v, w)，若v还不在答案中，那么将(v, dis+w)加入到堆中。重复这个过程直到堆为空或者所有节点的最短距离都被求出来。此时对于每一条边至多入堆出堆一次，那么最终的时间复杂度就是O(mlogn)。

以上是dijkstra算法比较常见的实现，当然，还有某种名为斐波那契堆的数据结构可以用来优化这个问题，其实现的思路比较复杂，主要是基于斐波那契数列的规则对堆中的点进行拆分与合并，通过势能法可以证明使用斐波那契堆的数的dijkstra算法最终时间复杂度位O(nlogn)。不过由于其原理与实现起来过于复杂，而且常数很大，因此实际上很少看到有什么地方再用这种数据结构。

最后附上python代码，我采用的是经典的二叉堆的做法：

```python
class Solution(object):
    def networkDelayTime(self, times, N, K):
        """
        :type times: List[List[int]]
        :type N: int
        :type K: int
        :rtype: int
        """

        edge = {}
        for u, v, w in times:
            if u not in edge:
                edge[u] = {}
            edge[u][v] = w
        
        res = {}
        heap = [[0, K]]

        while heap:
            dis, u = heapq.heappop(heap)
            if u not in res:
                res[u] = dis
                for v, w in edge.get(u, {}).items():
                    if v not in res:
                        heapq.heappush(heap, [dis + w, v])

        if len(res) != N:
            return -1
        else:
            return max(res.values())
```
