---
title: "1976. 到达目的地的方案数"
aliases: ["yiduobo的每日leetcode 1976.到达目的地的方案数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/dynamic-programming", "leetcode/shortest-path", "题单/动态规划", "题单/图论算法", "题单/动态规划/十三-图-DP", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/496907220"
zhihu_id: "496907220"
zhihu_title: "yiduobo的每日leetcode 1976.到达目的地的方案数"
question_id: "1976"
question: "到达目的地的方案数"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-arrive-at-destination/"
difficulty: "Medium"
rating: 2095
created: "2022-04-12T00:47:45+08:00"
updated: "2022-04-12T00:48:16+08:00"
upvotes: 0
comments: 0
---

# 1976. 到达目的地的方案数

> **[yiduobo的每日leetcode 1976.到达目的地的方案数](https://zhuanlan.zhihu.com/p/496907220) · 知乎 · 2022-04-12 · 赞同 0**
> 力扣：[1976. 到达目的地的方案数](https://leetcode.cn/problems/number-of-ways-to-arrive-at-destination/) · Medium · 灵茶山艾府：[在计算最短路的同时 DP（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1976.到达目的地的方案数

[力扣](https://leetcode-cn.com/problems/number-of-ways-to-arrive-at-destination/)

题目要求找出最短路径的条数，由于图中的边权都是正数，因此可以直接使用dijkstra算法来计算。当然，与常规的处理方法有细微的不同。

一般来说，dijkstra算法每次都是找离得最近的节点，并更新距离，而对于已经更新过的节点将直接跳过。在这里，如果碰到已经更新过的节点，则需要判断当前距离是否等于已知的最短距离，若相等，则更新路径条数。

为了更新路径条数，一方面需要使用一个数组cnt来储存每个节点的最短路径条数，另一方面在dijkstra算法迭代时，除了节点和距离之外，还需要额外维护当前节点的距离是从哪个节点来的，不妨记为prev。当出现距离相等的情况时，则使用cnt[prev]来更新当前节点的cnt。

最后附上python代码：

```python
class Solution(object):
    def countPaths(self, n, roads):
        """
        :type n: int
        :type roads: List[List[int]]
        :rtype: int
        """

        dis = [None] * n
        cnt = [0] * n

        g = {}
        for x, y, t in roads:
            if x not in g:
                g[x] = {}
            if y not in g:
                g[y] = {}
            g[x][y] = t
            g[y][x] = t
        
        mod = 10 ** 9 + 7
        heap = [(0, 0, None)]
        while heap:
            now_t, now_node, pre_node = heapq.heappop(heap)
            if dis[now_node] is None:
                dis[now_node] = now_t
                if pre_node is None:
                    cnt[now_node] = 1
                else:
                    cnt[now_node] = cnt[pre_node]
                for next_node, next_t in g.get(now_node, {}).items():
                    heapq.heappush(heap, [now_t + next_t, next_node, now_node])
            elif dis[now_node] == now_t:
                cnt[now_node] += cnt[pre_node]
                if cnt[now_node] >= mod:
                    cnt[now_node] -= mod
        
        return cnt[-1]
```
