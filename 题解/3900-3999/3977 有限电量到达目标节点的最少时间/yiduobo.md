---
title: "3977. 有限电量到达目标节点的最少时间"
aliases: ["yiduobo的每日leetcode 3977.有限电量到达目标节点的最少时间"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/graph", "leetcode/dynamic-programming", "leetcode/shortest-path", "leetcode/heap-priority-queue", "题单/动态规划", "题单/图论算法", "题单/动态规划/十三-图-DP", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2054654228757472647"
zhihu_id: "2054654228757472647"
zhihu_title: "yiduobo的每日leetcode 3977.有限电量到达目标节点的最少时间"
question_id: "3977"
question: "有限电量到达目标节点的最少时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-reach-target-with-limited-power/"
difficulty: "Hard"
rating: 2103
created: "2026-06-29T21:31:49+08:00"
updated: "2026-06-29T21:31:49+08:00"
upvotes: 1
comments: 0
---

# 3977. 有限电量到达目标节点的最少时间

> **[yiduobo的每日leetcode 3977.有限电量到达目标节点的最少时间](https://zhuanlan.zhihu.com/p/2054654228757472647) · 知乎 · 2026-06-29 · 赞同 1**
> 力扣：[3977. 有限电量到达目标节点的最少时间](https://leetcode.cn/problems/minimum-time-to-reach-target-with-limited-power/) · Hard · 灵茶山艾府：[两种方法：Dijkstra / DAG DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3977.有限电量到达目标节点的最少时间

<https://leetcode.cn/problems/minimum-time-to-reach-target-with-limited-power/>

题目给出一个有n个节点的有向加权图，节点标号从0到n - 1。n的大小不超过1000。

图由一个二维整数数组edges表示，其中edges\[index\] \= \[u\[index\], v\[index\], t\[index\]\]，表示一条从u\[index\]到v\[index\]的有向边，通过这条边需要花费t\[index\]秒。edges的长度不超过1000，其中的t都为正整数。

同时给出一个整数power，表示初始电量，其大小不超过1000。另外给出一个长度为n的整数数组cost，其中cost[u]表示从u通过任意一条出边所需的电量。换言之，若处于u时，剩余的电量不足cost[u]，那么就不能继续往下走。

最后给出两个整数source和target。在时刻0从source出发，拥有power单位的电量，问到达target的最短时间，以及使得时间最短时可能保有的最大电量。

从题目的数据规模来看，分层图的dijkstra是非常适合的。具体来说，将原图复制power + 1份，第p层表示当前剩余电量为p。若原图中有一条u到v的边，那么对于第cost[u]到第power层中的节点u，都建立一条到当前层p减去cost[u]对应层的v的边，即第p层的u，到第p - cost[u]层的v。

接下来，从第power层的source开始做dijkstra，计算到达任意层的target的最短路径。若存在多个最短路径，则选择最高那一层作为最终答案。

另外在具体实现上，不需要真实建图，只需要将p额外纳入到状态中就行了。

最后附上python代码：

```python
class Solution(object):
    def minTimeMaxPower(self, n, edges, power, cost, source, target):
        """
        :type n: int
        :type edges: List[List[int]]
        :type power: int
        :type cost: List[int]
        :type source: int
        :type target: int
        :rtype: List[int]
        """
        
        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append((y, w))

        dis = [[None] * (power + 1) for _ in range(n)]
        heap = [(0, source, power)]

        best_dis = -1
        best_power = -1

        while heap:
            d, x, p = heapq.heappop(heap)
            if best_dis != -1 and d > best_dis or (d == best_dis and p <= best_power):
                continue

            if dis[x][p] is None:
                dis[x][p] = d
                if x == target:
                    best_dis = d
                    best_power = p
                    continue

                if p < cost[x]:
                    continue

                p -= cost[x]

                for y, w in g[x]:
                    if dis[y][p] is None:
                        heapq.heappush(heap, (d + w, y, p))
        
        return [best_dis, best_power]
```
