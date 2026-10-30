---
title: "2714. 找到最短路径的K次跨越"
aliases: ["yiduobo的每日leetcode 2714.找到最短路径的K次跨越"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/651484195"
zhihu_id: "651484195"
zhihu_title: "yiduobo的每日leetcode 2714.找到最短路径的K次跨越"
question_id: "2714"
question: "找到最短路径的K次跨越"
problem_url: "https://leetcode.cn/problems/find-shortest-path-with-k-hops/"
created: "2023-08-22T03:21:40+08:00"
updated: "2023-08-22T03:21:40+08:00"
upvotes: 0
comments: 0
---

# 2714. 找到最短路径的K次跨越

> **[yiduobo的每日leetcode 2714.找到最短路径的K次跨越](https://zhuanlan.zhihu.com/p/651484195) · 知乎 · 2023-08-22 · 赞同 0**
> 力扣：[2714. 找到最短路径的K次跨越](https://leetcode.cn/problems/find-shortest-path-with-k-hops/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2714.找到最短路径的K次跨越

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/find-shortest-path-with-k-hops/)

经典的分层图最短路问题，由于题目的数据规模不大，因此可以直接使用dijkstra算法来求解。

具体来说，就是将问题视为给出了一张k层的图，而对于图中的某条边(x, y, v)，既可以花费v的代价，从当前层的x出发走到当前层的y，也可以不花费任何代价，从当前层的x出发走到下一层的y。在这里使用dis[i][j]表示从第0层的s出发，走到第j层的节点i的最短路径，那么dis[d]中的最小值就是最终答案。

具体实现时，并不需要真正将这k层图建立出来，而是只需遍历原图中的边，分走到当前层的目标节点以及走到下一层的目标节点这两种情况分别更新dis就行了。

最后附上python代码：

```python
class Solution(object):
    def shortestPathWithHops(self, n, edges, s, d, k):
        """
        :type n: int
        :type edges: List[List[int]]
        :type s: int
        :type d: int
        :type k: int
        :rtype: int
        """

        g = {}
        for x, y, w in edges:
            if x not in g:
                g[x] = {}
            if y not in g:
                g[y] = {}
            g[x][y] = g[y][x] = w            

        dis = [[None] * (k + 1) for _ in range(n)]
        heap = [[0, s, 0]]
        while heap:
            nowd, now, level = heapq.heappop(heap)
            if dis[now][level] is None:
                dis[now][level] = nowd
                if now in g:
                    for nxt in g[now]:
                        if level < k and dis[nxt][level + 1] is None:
                            heapq.heappush(heap, [nowd, nxt, level + 1])
                        
                        if dis[nxt][level] is None:
                            heapq.heappush(heap, [nowd + g[now][nxt], nxt, level])

        return min(dis[d])
```
