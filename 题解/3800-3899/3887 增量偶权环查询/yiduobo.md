---
title: "3887. 增量偶权环查询"
aliases: ["yiduobo的每日leetcode 3887.增量偶权环查询"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/union-find", "leetcode/graph", "题单/常用数据结构", "题单/常用数据结构/七-并查集"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2023527214591811632"
zhihu_id: "2023527214591811632"
zhihu_title: "yiduobo的每日leetcode 3887.增量偶权环查询"
question_id: "3887"
question: "增量偶权环查询"
problem_url: "https://leetcode.cn/problems/incremental-even-weighted-cycle-queries/"
difficulty: "Hard"
rating: 2128
created: "2026-04-03T22:48:32+08:00"
updated: "2026-04-03T22:48:32+08:00"
upvotes: 0
comments: 0
---

# 3887. 增量偶权环查询

> **[yiduobo的每日leetcode 3887.增量偶权环查询](https://zhuanlan.zhihu.com/p/2023527214591811632) · 知乎 · 2026-04-03 · 赞同 0**
> 力扣：[3887. 增量偶权环查询](https://leetcode.cn/problems/incremental-even-weighted-cycle-queries/) · Hard · 灵茶山艾府：[带权并查集（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3887.增量偶权环查询

<https://leetcode.cn/problems/incremental-even-weighted-cycle-queries/description/>

题目给出一个正整数n。

有一个由n个节点组成的无向图，节点的编号从0到n - 1。最初，这个图中没有任何边。

另外给出一个二维整数数组edges，其中edges\[index\] \= \[u\[index\], v\[index\], w\[index\]\]，表示一条连接u\[index\]和v\[index\]的边，权重为w\[index\]。w的值要么为0，要么为1。

现在要求按照给定顺序处理edges中的每一条边。对于每条边，若其添加到图中后，图中的每个环的边权和依然是偶数，那么就将其添加到图中，否则将其舍弃。

问最终添加到图中的边的数量。

首先可以明确的是，若两个点u和v是环上的两点，那么u到v的所有简单路径的权重和的奇偶性必然相同。理由是任取两条简单路径，都可以形成一个环，而题目要求环的权重和为偶数，也就意味着这两条简单路径边权和的奇偶性相同。

基于这一点，就可以通过带权并查集，一边维护连通性与距离的奇偶性，一边往里面添加边了。

具体来说，在常规并查集的基础上，使用一个数组xor，其中xor[x]记录的是从x到x的最高祖先的路径上边权和的奇偶性，那么对于一条边(x, y, v)：

1、先通过并查集找出x和y的最高祖先fa_x以及fa_y，同时更新它们到fa_x以及fa_y的边权和的奇偶性xor[x]以及xor[y]

2、若fa_x与fa_y相同，说明x和y本来就在一个连通块里，新增这条边将会产生环。

此时只有在需要满足x到fa_x的边权和，加上y到fa_y的边权和，在加上v，得到的总和为偶数时，才可以连边。更具体的，在这里可以写成当xor[x] ^ xor[y] \= v，才添加这条边

3、若fa_x与fa_y不同，说明x和y本来不在一个连通块里，那么必然可以连上这条边。

连上边之后，可以统一让x这一侧的节点接到y这一侧上，也就是将fa_x的父亲设置为fa_y进行合并，此时可能会影响到fa_x这颗树上(并查集的本质是一棵树)所有节点到fa_y的奇偶性。

为了适配这个奇偶性，在这里可以直接修改xor[fa_x]，因为在此次合并之后，fa_x这颗树上所有节点在查询最高祖先时都必须主动或者被动经过xor[fa_x]，因此在这里只需要修正xor[fa_x]就可以了。

由于路径边权和的奇偶性是对称的，也就是a到b的路径的边权和的奇偶性，与b到a的路径的边权和的奇偶性相同，那么在连接x与y之后，fa_x到fa_y的路径，就是fa_x到x，再到y，最后到fa_y，这三段路径的奇偶性分别为xor[x]、v、xor[y]，将这三者异或起来，即为xor[fa_x]。

最后附上python代码：

```python
class Solution(object):
    def numberOfEdgesAdded(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: int
        """
        
        fa = [index for index in range(n)]
        xor = [0] * n

        def find(fa, xor, x):
            if fa[x] != x:
                ori = fa[x]
                fa[x] = find(fa, xor, fa[x])
                xor[x] ^= xor[ori]
            return fa[x]

        res = 0
        for x, y, v in edges:
            fa_x = find(fa, xor, x)
            fa_y = find(fa, xor, y)
            if fa_x == fa_y:
                if xor[x] ^ xor[y] == v:
                    res += 1
            else:
                res += 1
                fa[fa_x] = fa_y
                xor[fa_x] = xor[x] ^ xor[y] ^ v

        return res
```
