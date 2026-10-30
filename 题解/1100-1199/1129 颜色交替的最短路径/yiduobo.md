---
title: "1129. 颜色交替的最短路径"
aliases: ["yiduobo的每日leetcode 1129.颜色交替的最短路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/376256782"
zhihu_id: "376256782"
zhihu_title: "yiduobo的每日leetcode 1129.颜色交替的最短路径"
question_id: "1129"
question: "颜色交替的最短路径"
problem_url: "https://leetcode.cn/problems/shortest-path-with-alternating-colors/"
created: "2021-05-29T14:07:57+08:00"
updated: "2021-05-29T14:07:57+08:00"
upvotes: 1
comments: 0
---

# 1129. 颜色交替的最短路径

> **[yiduobo的每日leetcode 1129.颜色交替的最短路径](https://zhuanlan.zhihu.com/p/376256782) · 知乎 · 2021-05-29 · 赞同 1**
> 力扣：[1129. 颜色交替的最短路径](https://leetcode.cn/problems/shortest-path-with-alternating-colors/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1129.颜色交替的最短路径

[力扣](https://leetcode-cn.com/problems/shortest-path-with-alternating-colors/)

题目要求0到其他所有点的交叉颜色的最短路径，由于这里的边上没有权重的，因此可以考虑从0开始进行bfs，当某一轮某个点第一次被访问时，当前轮次就是0到该点的路径长度。

由于边的颜色交替出现，那么每个点就有两种状态，即通过红色边到达以及通过蓝色边到达，需要分别设置访问标记。对于红色边到达的点，其只能发射蓝色边，同样地，通过蓝色边到达的点只能发射红色边。而这里某个点第一次被访问就应该是通过红色边或者通过蓝色边第一次到达该点。

最后附上python代码：

```python
class Solution(object):
    def shortestAlternatingPaths(self, n, red_edges, blue_edges):
        """
        :type n: int
        :type red_edges: List[List[int]]
        :type blue_edges: List[List[int]]
        :rtype: List[int]
        """

        G_r = {}
        for x, y in red_edges:
            if x not in G_r:
                G_r[x] = set()
            G_r[x].add(y)
        
        G_b = {}
        for x, y in blue_edges:
            if x not in G_b:
                G_b[x] = set()
            G_b[x].add(y)

        q = [[0, None]]
        l = 0
        r = 1
        res = [-1] * n
        step = 0
        used_r = [False] * n
        used_b = [False] * n
        while l < r:
            for now, last_c in q[l : r]:
                if res[now] == -1:
                    res[now] = step

                if last_c != 'r' and now in G_r:
                    for next in G_r[now]:
                        if not used_r[next]:
                            q.append([next, 'r'])
                            used_r[next] = True
                
                if last_c != 'b' and now in G_b:
                    for next in G_b[now]:
                        if not used_b[next]:
                            q.append([next, 'b'])
                            used_b[next] = True
            
            l, r = r, len(q)
            step += 1
        
        return res
```
