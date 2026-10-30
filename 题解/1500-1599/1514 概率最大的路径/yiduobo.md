---
title: "1514. 概率最大的路径"
aliases: ["yiduobo的每日leetcode 1514.概率最大的路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/420786310"
zhihu_id: "420786310"
zhihu_title: "yiduobo的每日leetcode 1514.概率最大的路径"
question_id: "1514"
question: "概率最大的路径"
problem_url: "https://leetcode.cn/problems/path-with-maximum-probability/"
created: "2021-10-12T23:44:57+08:00"
updated: "2021-10-12T23:44:57+08:00"
upvotes: 1
comments: 0
---

# 1514. 概率最大的路径

> **[yiduobo的每日leetcode 1514.概率最大的路径](https://zhuanlan.zhihu.com/p/420786310) · 知乎 · 2021-10-12 · 赞同 1**
> 力扣：[1514. 概率最大的路径](https://leetcode.cn/problems/path-with-maximum-probability/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1514.概率最大的路径

[力扣](https://leetcode-cn.com/problems/path-with-maximum-probability/)

注意题目中边上的为概率值，也就是说这些值的范围在0到1之间，那么这里实际上是满足三角形不等式的，因此就可以使用基于贪心算法的dijkstra算法来解决这个问题。

具体来说就是对于当前剩下的所有节点，找出一个从start出发路径概率最大的节点，并使用这个概率更新从start到其他剩余节点的路径概率，直到处理到end为止。

由于每次要找的是剩余节点中路径概率最大的节点，因此可以使用堆来进行优化。

最后附上python代码：

```python
class Solution(object):
    def maxProbability(self, n, edges, succProb, start, end):
        """
        :type n: int
        :type edges: List[List[int]]
        :type succProb: List[float]
        :type start: int
        :type end: int
        :rtype: float
        """

        g = {}
        m = len(edges)
        for index in range(m):
            x, y = edges[index]
            v = succProb[index]
            if x not in g:
                g[x] = {}
            if y not in g:
                g[y] = {}
            g[x][y] = g[y][x] = v
        
        heap = []
        for next, v in g.get(start, {}).items():
            heapq.heappush(heap, [-v, next])
        
        used = set([start])
        while heap:
            v, now = heapq.heappop(heap)
            if now == end:
                return -v

            if now not in used:
                used.add(now)
                for next, w in g.get(now, {}).items():
                    if next not in used:
                        heapq.heappush(heap, [v * w, next])
        
        return 0.0
```
