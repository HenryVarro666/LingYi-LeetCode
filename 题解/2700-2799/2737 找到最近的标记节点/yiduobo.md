---
title: "2737. 找到最近的标记节点"
aliases: ["yiduobo的每日leetcode 2737.找到最近的标记节点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/652938372"
zhihu_id: "652938372"
zhihu_title: "yiduobo的每日leetcode 2737.找到最近的标记节点"
question_id: "2737"
question: "找到最近的标记节点"
problem_url: "https://leetcode.cn/problems/find-the-closest-marked-node/"
created: "2023-08-29T02:51:46+08:00"
updated: "2023-08-29T02:51:46+08:00"
upvotes: 0
comments: 0
---

# 2737. 找到最近的标记节点

> **[yiduobo的每日leetcode 2737.找到最近的标记节点](https://zhuanlan.zhihu.com/p/652938372) · 知乎 · 2023-08-29 · 赞同 0**
> 力扣：[2737. 找到最近的标记节点](https://leetcode.cn/problems/find-the-closest-marked-node/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2737.找到最近的标记节点

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/find-the-closest-marked-node/)

题目中边的权重非负，因此可以直接使用dijkstra算法，计算从s出发到图中所有点的最短距离。接下来遍历marked中的点，找出其中离s距离最近的点即可。

另外需要注意的是题目给出的图中可能有重边，因此在建图时应该保留边权较小的边。

最后附上python代码：

```python
class Solution(object):
    def minimumDistance(self, n, edges, s, marked):
        """
        :type n: int
        :type edges: List[List[int]]
        :type s: int
        :type marked: List[int]
        :rtype: int
        """

        dis = [None] * n
        heap = [[0, s]]
        g = {x : {} for x in range(n)}
        for x, y, v in edges:
            if y not in g[x]:
                g[x][y] = v
            else:
                g[x][y] = min(g[x][y], v)
        
        while heap:
            d, now = heapq.heappop(heap)
            if dis[now] is None:
                dis[now] = d
                for nxt in g[now]:
                    if dis[nxt] is None:
                        heapq.heappush(heap, [g[now][nxt] + d, nxt])
        
        res = -1
        for x in marked:
            if dis[x] is not None and (res == -1 or res > dis[x]):
                res = dis[x]
        
        return res
```
