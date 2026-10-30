---
title: "924. 尽量减少恶意软件的传播"
aliases: ["yiduobo的每日leetcode 924.尽量减少恶意软件的传播"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/graph", "leetcode/recursion", "题单/图论算法", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/356456709"
zhihu_id: "356456709"
zhihu_title: "yiduobo的每日leetcode 924.尽量减少恶意软件的传播"
question_id: "924"
question: "尽量减少恶意软件的传播"
problem_url: "https://leetcode.cn/problems/minimize-malware-spread/"
difficulty: "Hard"
rating: 1869
created: "2021-03-11T23:34:37+08:00"
updated: "2021-03-11T23:34:37+08:00"
upvotes: 1
comments: 0
---

# 924. 尽量减少恶意软件的传播

> **[yiduobo的每日leetcode 924.尽量减少恶意软件的传播](https://zhuanlan.zhihu.com/p/356456709) · 知乎 · 2021-03-11 · 赞同 1**
> 力扣：[924. 尽量减少恶意软件的传播](https://leetcode.cn/problems/minimize-malware-spread/) · Hard · 灵茶山艾府：[只包含一个被感染节点的最大连通块（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

924.尽量减少恶意软件的传播

[力扣](https://leetcode-cn.com/problems/minimize-malware-spread/)

首先，题目给出的是一个无向图，那么对于无向图中的某个连通子图而言，若其中某个节点是传播源，那么整个连通子图的节点最终都将被感染。更进一步地，若某个连通子图中有两个或者更多的传播源，那么即使去掉其中某一个，这个连通子图中的节点最终也还是会被感染。那么现在就可以明确，我们应该将目标锁定在那些只有一个传播源的连通子图上。显然，我们应该选择节点数量最多的连通子图，去除掉其中唯一的传播源之后整个子图的节点都将不会受到感染。

那么现在的问题就变成了如何确定连通子图。一个经典的做法是对当前未被访问过的节点进行dfs染色，每次将相邻的无色节点染成当前的颜色然后递归继续进行染色。全部节点处理完成后，所有同一颜色的节点就处在同一个连通子图当中。

最后附上python代码：

```python
class Solution(object):
    def minMalwareSpread(self, graph, initial):
        """
        :type graph: List[List[int]]
        :type initial: List[int]
        :rtype: int
        """

        n = len(graph)
        color = [None] * n
        g = {}
        for i in range(n):
            g[i] = set()
            for j in range(n):
                if i != j and graph[i][j] == 1:
                    g[i].add(j)
        
        now_color = 0
        for i in range(n):
            if color[i] is None:
                self.dfs(i, now_color, color, g)
                now_color += 1
        
        color_cnt = [0] * now_color
        for i in range(n):
            color_cnt[color[i]] += 1
        
        color_flag = [0] * now_color
        for i in initial:
            color_flag[color[i]] += 1
        
        res = None
        remove_cnt = None
        for i in initial:
            if color_flag[color[i]] == 1:
                now_remove = color_cnt[color[i]]
            else:
                now_remove = 0
            if res is None or now_remove > remove_cnt or (now_remove == remove_cnt and res > i):
                res = i
                remove_cnt = now_remove

        return res

    def dfs(self, now, now_color, color, g):
        color[now] = now_color
        for next in g[now]:
            if color[next] is None:
                self.dfs(next, now_color, color, g)
```
