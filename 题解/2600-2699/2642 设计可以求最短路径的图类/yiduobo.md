---
title: "2642. 设计可以求最短路径的图类"
aliases: ["yiduobo的每日leetcode 2642.设计可以求最短路径的图类"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/graph", "leetcode/dynamic-programming", "leetcode/shortest-path", "题单/图论算法", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/646798116"
zhihu_id: "646798116"
zhihu_title: "yiduobo的每日leetcode 2642.设计可以求最短路径的图类"
question_id: "2642"
question: "设计可以求最短路径的图类"
problem_url: "https://leetcode.cn/problems/design-graph-with-shortest-path-calculator/"
difficulty: "Hard"
rating: 1811
created: "2023-07-30T01:14:00+08:00"
updated: "2023-07-30T01:14:00+08:00"
upvotes: 1
comments: 0
---

# 2642. 设计可以求最短路径的图类

> **[yiduobo的每日leetcode 2642.设计可以求最短路径的图类](https://zhuanlan.zhihu.com/p/646798116) · 知乎 · 2023-07-30 · 赞同 1**
> 力扣：[2642. 设计可以求最短路径的图类](https://leetcode.cn/problems/design-graph-with-shortest-path-calculator/) · Hard · 灵茶山艾府：[两种方法：Dijkstra / Floyd（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2642.设计可以求最短路径的图类

[力扣](https://leetcode.cn/problems/design-graph-with-shortest-path-calculator/)

题目给出一张有向图以及若干操作，每次操作可能在图中新加一条边，或者询问某两点之间的最短距离。

想要在新增边之后以较低的复杂度更新所有点对之间的距离是比较困难的事情，不过本题的数据规模比较小，同时边权都是正数，因此可以在每次询问时对询问中的一个点执行一次dijkstra算法，计算出该点到其他所有点的最短路径，从而得知该点到询问中的另一个点的最短距离。

另外，由于本题的图中边的规模达到了点规模的平方，因此在这里可以直接使用临接矩阵来储存这张图，同时不应该使用二叉堆优化，而是应该使用最原始的dijkstra算法来求最短路。

最后附上python代码：

```python
class Graph(object):

    def __init__(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        """
        self.n = n
        self.g = [[-1] * n for _ in range(n)]
        for x, y, v in edges:
            self.g[x][y] = v

    def addEdge(self, edge):
        """
        :type edge: List[int]
        :rtype: None
        """
        x, y, v = edge
        self.g[x][y] = v

    def shortestPath(self, node1, node2):
        """
        :type node1: int
        :type node2: int
        :rtype: int
        """

        dis = self.g[node1][:]
        dis[node1] = 0
        vis = [False] * self.n
        vis[node1] = True

        while True:
            p = -1
            mi = -1
            for i in range(self.n):
                if not vis[i] and dis[i] != -1 and (mi == -1 or mi > dis[i]):
                    p = i
                    mi = dis[i]
            
            if p == -1:
                break
            
            vis[p] = True
            for i in range(self.n):
                if self.g[p][i] != -1 and (dis[i] == -1 or dis[i] > dis[p] + self.g[p][i]):
                    dis[i] = dis[p] + self.g[p][i]

        return dis[node2]

# Your Graph object will be instantiated and called as such:
# obj = Graph(n, edges)
# obj.addEdge(edge)
# param_2 = obj.shortestPath(node1,node2)
```
