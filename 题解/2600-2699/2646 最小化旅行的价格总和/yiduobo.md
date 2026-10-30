---
title: "2646. 最小化旅行的价格总和"
aliases: ["yiduobo的每日leetcode 2646.最小化旅行的价格总和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/dynamic-programming", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/三-一般树", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/647167051"
zhihu_id: "647167051"
zhihu_title: "yiduobo的每日leetcode 2646.最小化旅行的价格总和"
question_id: "2646"
question: "最小化旅行的价格总和"
problem_url: "https://leetcode.cn/problems/minimize-the-total-price-of-the-trips/"
difficulty: "Hard"
rating: 2238
created: "2023-08-01T01:15:28+08:00"
updated: "2023-08-01T01:15:28+08:00"
upvotes: 0
comments: 0
---

# 2646. 最小化旅行的价格总和

> **[yiduobo的每日leetcode 2646.最小化旅行的价格总和](https://zhuanlan.zhihu.com/p/647167051) · 知乎 · 2023-08-01 · 赞同 0**
> 力扣：[2646. 最小化旅行的价格总和](https://leetcode.cn/problems/minimize-the-total-price-of-the-trips/) · Hard · 灵茶山艾府：[两种方法：暴力 DFS / 树上差分（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2646.最小化旅行的价格总和

[力扣](https://leetcode.cn/problems/minimize-the-total-price-of-the-trips/)

题目一开始没有设定根节点，为了方便起见，在这里不妨假设0号节点为根节点，并根据edges中的信息从0开始进行一次bfs，确定每个节点的父亲节点方便后续的计算。

为了使得价格总和最小，在旅行的过程中就不应该经过不需要经过的节点。也就是说，每一次旅程都应该从树中的点x出发，走到x和y的最近公共祖先lca，然后再从lca走到y。由于本题的数据规模比较小，因此可以直接使用暴力法，从x出发向上走到根节点并记录路径上的所有节点，然后从y出发向上走到第一个出现在路径上的节点，该节点就是x和y的lca。得到lca后，将x到lca再到y的这条路径上所有节点的权重加上1。

计算完所有旅程后，就得到了每个节点需要经过的次数，不妨记为weight。那么节点i将产生的费用就是weight[i] \* price[i]。如果使用这个费用作为树中节点的值，那么问题就转化成了给出一棵树，每个节点都带有权重，现在可以将树中不相邻的节点值减半，问树中节点值之和的最小值是多少。

这是一个经典的动态规划问题。令f[i][0]表示不将节点i的值减半时，以i为根节点的子树的最小权重和是多少，而f[i][1]则表示将节点i的值减半时，以i为根节点的子树的最小权重和是多少。

那么对f[i][0]，首先可以初始化其值为weight[i] \* price[i]，接下来遍历i的所有孩子节点。对于这些孩子节点，则可以选择减半或者不减半，因此在这里就有

f[i][0] \= weight[i] \* price[i] + min(f[s0][0], f[s0][1]) + min(f[s1][0], f[s1][1]) + ... + min(f[sk][0], f[sk][1])

其中s0到sk为i的所有孩子节点

而对于f[i][1]，其初始值就应该是price[i] / 2 \* weight[i]，而其所有的孩子节点值都不可以减半，因此就有

f[i][1] \= price[i] / 2 \* weight[i] + f[s0][0] + f[s1][0] + ... + f[sk][0]

接下来只需按照以上方法，自顶向下递归求解f[0][0]以及f[0][1]然后取二者的较小值作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def minimumTotalPrice(self, n, edges, price, trips):
        """
        :type n: int
        :type edges: List[List[int]]
        :type price: List[int]
        :type trips: List[List[int]]
        :rtype: int
        """

        g = {index : set() for index in range(n)}
        fa = {index : None for index in range(n)}

        for x, y in edges:
            g[x].add(y)
            g[y].add(x)
        
        q = [0]
        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            for nxt in g[now]:
                if nxt != fa[now]:
                    q.append(nxt)
                    fa[nxt] = now
                    tail += 1

        weight = [0] * n
        for x, y in trips:
            path = set([x])
            now = x
            while fa[now] is not None:
                now = fa[now]
                path.add(now)
            
            now = y
            while now not in path:
                now = fa[now]
            
            while x != now:
                weight[x] += 1
                x = fa[x]
            
            while y != now:
                weight[y] += 1
                y = fa[y]
        
            weight[now] += 1

        f = [[None] * 2 for _ in range(n)]
        def dfs(now, flag):
            if f[now][flag] is None:
                if flag == 0:
                    f[now][flag] = price[now] * weight[now]
                    for nxt in g[now]:
                        if nxt != fa[now]:
                            dfs(nxt, 0)
                            dfs(nxt, 1)
                            f[now][flag] += min(f[nxt][0], f[nxt][1])
                else:
                    f[now][flag] = price[now] / 2 * weight[now]
                    for nxt in g[now]:
                        if nxt != fa[now]:
                            dfs(nxt, 0)
                            f[now][flag] += f[nxt][0]
            
            return f[now][flag]

        
        dfs(0, 0)
        dfs(0, 1)
        return min(f[0][0], f[0][1])
```
