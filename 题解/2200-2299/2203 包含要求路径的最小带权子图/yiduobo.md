---
title: "2203. 得到要求路径的最小带权子图"
aliases: ["yiduobo的每日leetcode 2203.得到要求路径的最小带权子图"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/graph", "leetcode/enumeration", "leetcode/shortest-path", "leetcode/heap-priority-queue", "题单/图论算法", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/539399325"
zhihu_id: "539399325"
zhihu_title: "yiduobo的每日leetcode 2203.得到要求路径的最小带权子图"
question_id: "2203"
question: "包含要求路径的最小带权子图"
problem_url: "https://leetcode.cn/problems/minimum-weighted-subgraph-with-the-required-paths/"
difficulty: "Hard"
rating: 2364
created: "2022-07-08T23:06:10+08:00"
updated: "2022-07-08T23:06:10+08:00"
upvotes: 0
comments: 0
---

# 2203. 得到要求路径的最小带权子图

> **[yiduobo的每日leetcode 2203.得到要求路径的最小带权子图](https://zhuanlan.zhihu.com/p/539399325) · 知乎 · 2022-07-08 · 赞同 0**
> 力扣：[2203. 包含要求路径的最小带权子图](https://leetcode.cn/problems/minimum-weighted-subgraph-with-the-required-paths/) · Hard · 灵茶山艾府：[枚举三条最短路的交汇点（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2203.得到要求路径的最小带权子图

[力扣](https://leetcode.cn/problems/minimum-weighted-subgraph-with-the-required-paths/)

题目要求从有向图中找出从src1到dest的一条路径以及从src2到dest的一条路径，这两条路径上所有边的权重之和最小，其中出现两次的边权重也只计算一次。

本题麻烦的地方就在于这个出现两次的边权重只计算一次，需要想办法去重。

不妨设这两条路径上最早重复的点为t，那么最终答案就可以拆分成三个部分，分别为src1到t的最短路，src2到t的最短路，以及从t到dest的最短路。

一个自然的想法是枚举这个t，计算这三条最短路长度之和的最小值。由于题目中n的规模比较大，那么就需要能高效的知道上面三个最短路的长度。对于src1到t和src2到t的最短路，分别用src1和src2为源执行dijkstra就行了，而对于t到dest的最短路，则可以将原图中的所有边反向，在这个反向图上从dest开始执行一次dijkstra。于是现在就得到了一种做法：

1、通过题目给出的edges分别建立正向图g和反向图reverse_g

2、在g上分别以src1和src2为源执行dijkstra，得到两个距离数组dis_s1和dis_s2

3、在reverse_g上以dest为源执行dijkstra，得到距离数组dis_d

4、枚举中继点t，计算dis_s1[t] + dis_s2[t] + dis_d[t]，其中最小的即为最终答案

最后附上python代码：

```python
class Solution(object):
    def minimumWeight(self, n, edges, src1, src2, dest):
        """
        :type n: int
        :type edges: List[List[int]]
        :type src1: int
        :type src2: int
        :type dest: int
        :rtype: int
        """

        dis_s1 = [None] * n
        dis_s2 = [None] * n
        dis_d = [None] * n

        g = {}
        reverse_g = {}
        for x, y, w in edges:
            if x not in g:
                g[x] = {}
            if y not in g[x]:
                g[x][y] = w
            else:
                g[x][y] = min(g[x][y], w)
            
            if y not in reverse_g:
                reverse_g[y] = {}
            if x not in reverse_g[y]:
                reverse_g[y][x] = w
            else:
                reverse_g[y][x] = min(reverse_g[y][x], w)

        def dijkstra(s, g, dis):
            dis[s] = 0
            heap = []
            for next in g.get(s, {}):
                heapq.heappush(heap, [g[s][next], next])
            
            while heap:
                d, now = heapq.heappop(heap)
                if dis[now] is None:
                    dis[now] = d
                    for next in g.get(now, {}):
                        heapq.heappush(heap, [d + g[now][next], next])
            
        dijkstra(src1, g, dis_s1)
        dijkstra(src2, g, dis_s2)
        dijkstra(dest, reverse_g, dis_d)

        res = -1
        for t in range(n):
            if dis_s1[t] is not None and dis_s2[t] is not None and dis_d[t] is not None:
                if res == -1 or res > dis_s1[t] + dis_s2[t] + dis_d[t]:
                    res = dis_s1[t] + dis_s2[t] + dis_d[t]
        
        return res
```
