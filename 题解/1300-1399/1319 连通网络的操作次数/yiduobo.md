---
title: "1319. 连通网络的操作次数"
aliases: ["yiduobo的每日leetcode 1319.连通网络的操作次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/393199587"
zhihu_id: "393199587"
zhihu_title: "yiduobo的每日leetcode 1319.连通网络的操作次数"
question_id: "1319"
question: "连通网络的操作次数"
problem_url: "https://leetcode.cn/problems/number-of-operations-to-make-network-connected/"
created: "2021-07-26T12:26:28+08:00"
updated: "2021-07-26T12:26:28+08:00"
upvotes: 0
comments: 0
---

# 1319. 连通网络的操作次数

> **[yiduobo的每日leetcode 1319.连通网络的操作次数](https://zhuanlan.zhihu.com/p/393199587) · 知乎 · 2021-07-26 · 赞同 0**
> 力扣：[1319. 连通网络的操作次数](https://leetcode.cn/problems/number-of-operations-to-make-network-connected/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1319.连通网络的操作次数

[力扣](https://leetcode-cn.com/problems/number-of-operations-to-make-network-connected/)

题目给出n点和m边，问最少调整多少条边可以使得图成为一个连通图。

首先，对于n个点的图，其至少需要n - 1条边才能成为一个连通图，那么当n - 1 > m时，直接返-1即可。

接下来，由于图中的边可以任意调整，因此我们可以先统计出图中连通分量的数目，设为k，同时设当前这k个连通分量的点数分别为n[1]、n[2]、...、n[k]，那么就有

n[1] + n[2] + ... + n[k] \= n

已知维持一个n个点的连通图需要n - 1条边，那么保持着k个连通分量连通的变数至少需要

n[1] - 1 + n[2] - 1 + ... + n[k] - 1 \= n - k

而这里又有

m >\= n - 1

因此在使用掉n - k条边之后，还至少有k - 1条边可以自由使用。而将k个连通分量连起来至少需要的边数恰好就是k - 1，因此当m >\= n - 1时是必然有解的，而移动边的数量就是k - 1。

于是现在的做法就是先建好图，然后对图进行一次染色，设最终不同颜色的数量为color，那么答案就是color - 1。

最后附上python代码：

```python
class Solution(object):
    def makeConnected(self, n, connections):
        """
        :type n: int
        :type connections: List[List[int]]
        :rtype: int
        """

        if len(connections) < n - 1:
            return -1
        
        g = {}
        for x, y in connections:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)
        
        color = [None] * n
        now_color = 0
        for x in range(n):
            if color[x] is None:
                self.dfs(x, now_color, color, g)
                now_color += 1
        
        return now_color - 1
    
    def dfs(self, now, now_color, color, g):
        color[now] = now_color
        if now not in g:
            return
        for next in g[now]:
            if color[next] is None:
                self.dfs(next, now_color, color, g)
```
