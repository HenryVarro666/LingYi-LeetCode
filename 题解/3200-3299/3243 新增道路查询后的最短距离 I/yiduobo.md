---
title: "3243. 新增道路查询后的最短距离I"
aliases: ["yiduobo的每日leetcode 3243.新增道路查询后的最短距离I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/graph", "leetcode/dynamic-programming", "leetcode/shortest-path", "题单/动态规划", "题单/图论算法", "题单/动态规划/十三-图-DP", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/721215880"
zhihu_id: "721215880"
zhihu_title: "yiduobo的每日leetcode 3243.新增道路查询后的最短距离I"
question_id: "3243"
question: "新增道路查询后的最短距离 I"
problem_url: "https://leetcode.cn/problems/shortest-distance-after-road-addition-queries-i/"
difficulty: "Medium"
rating: 1568
created: "2024-09-20T23:35:29+08:00"
updated: "2024-09-20T23:35:29+08:00"
upvotes: 0
comments: 0
---

# 3243. 新增道路查询后的最短距离I

> **[yiduobo的每日leetcode 3243.新增道路查询后的最短距离I](https://zhuanlan.zhihu.com/p/721215880) · 知乎 · 2024-09-20 · 赞同 0**
> 力扣：[3243. 新增道路查询后的最短距离 I](https://leetcode.cn/problems/shortest-distance-after-road-addition-queries-i/) · Medium · 灵茶山艾府：[两种方法：BFS / DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3243.新增道路查询后的最短距离I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/shortest-distance-after-road-addition-queries-i/description/)

题目给出一个整数n，表示有n个城市，编号分别为0到n - 1。在一开始，每个城市i都有一条通向城市i + 1的单向道路。接下来给出一个二维整数数组queries，其中queries\[i\] \= \[u\[i\], v\[i\]\]，其中u\[i\] \< v\[i\]，表示新增了一条从u\[i\]到v\[i\]的单向道路。现在要求计算每新增一条queries中的道路后，从0出发到达n - 1的最短路径长度。

题目中n和queries的规模都很小，因此可以直接暴力计算。具体来说，先建立一张包含n个节点的有向图，其中一开始只有节点i通向节点i + 1的边。接下来遍历queries，对于queries[i]，新增一条u[i]到v[i]的边，然后从0号节点开始做bfs，记录到达n - 1所需的轮次，即为对应的最短路径长度。

最后附上python代码：

```python
class Solution(object):
    def shortestDistanceAfterQueries(self, n, queries):
        """
        :type n: int
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        g = [[] for _ in range(n)]
        for index in range(n - 1):
            g[index].append(index + 1)
        
        res = []
        for x, y in queries:
            g[x].append(y)
            q = [0]
            dis = [None] * n
            dis[0] = 0
            head, tail = 0, 1
            while head < tail:
                for now in q[head : tail]:
                    for nxt in g[now]:
                        if dis[nxt] is None:
                            dis[nxt] = dis[now] + 1
                            q.append(nxt)
                
                head, tail = tail, len(q)
            
            res.append(dis[n - 1])
        
        return res
```
