---
title: "3613. 最小化连通分量的最大成本"
aliases: ["yiduobo的每日leetcode 3613.最小化连通分量的最大成本"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/union-find", "leetcode/sorting", "题单/二分算法", "题单/常用数据结构", "题单/二分算法/二-二分答案", "题单/常用数据结构/七-并查集"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1943464877554399160"
zhihu_id: "1943464877554399160"
zhihu_title: "yiduobo的每日leetcode 3613.最小化连通分量的最大成本"
question_id: "3613"
question: "最小化连通分量的最大成本"
problem_url: "https://leetcode.cn/problems/minimize-maximum-component-cost/"
difficulty: "Medium"
rating: 1900
created: "2025-08-26T00:19:49+08:00"
updated: "2025-08-26T00:19:49+08:00"
upvotes: 0
comments: 0
---

# 3613. 最小化连通分量的最大成本

> **[yiduobo的每日leetcode 3613.最小化连通分量的最大成本](https://zhuanlan.zhihu.com/p/1943464877554399160) · 知乎 · 2025-08-26 · 赞同 0**
> 力扣：[3613. 最小化连通分量的最大成本](https://leetcode.cn/problems/minimize-maximum-component-cost/) · Medium · 灵茶山艾府：[从小到大合并（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3613.最小化连通分量的最大成本

<https://leetcode.cn/problems/minimize-maximum-component-cost/description/>

题目给出一个无向连通图，其中包含n个节点，编号从0到n - 1。另外给出一个二维整数数组edges，其中edges\[index\] \= \[u\[index\], v\[index\], w\[index\]\]，表示一条连接节点u\[index\]和节点v\[index\]的无向边，权重为w\[index\]。

现在给出一个整数k，要求从图中移除一些边，使得图中最多只包含k个连通分量。连通分量的成本定义为该分量中边权的最大值，若一个连通分量中没有边，那么其代价为0。问移除这些边后，所有连通分量之中的最大成本的最小可能值。

本题与之前的3608题类似，处理方式也差不多。

[yiduobo的每日leetcode 3608.包含k个连通分量需要的最小时间](https://zhuanlan.zhihu.com/p/1942681960557287307)

为了使得最终所有连通块中最大边权最小，在这里就可以将所有的边按权重从小到大进行排序，然后逐条加入到图中，直到图中有k个连通块为止，那么最后一条加入的边的权重即为最终答案。

对于连通性的维护，则依然是通过并查集来进行处理。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, n, edges, k):
        """
        :type n: int
        :type edges: List[List[int]]
        :type k: int
        :rtype: int
        """
        
        if k == n:
            return 0

        edges.sort(key=lambda d:d[2])
        fa = [x for x in range(n)]
        parts = n

        def find(fa, x):
            if fa[x] != x:
                fa[x] = find(fa, fa[x])
            return fa[x]

        for x, y, v in edges:
            fa_x = find(fa, x)
            fa_y = find(fa, y)
            if fa_x != fa_y:
                fa[fa_x] = fa_y
                parts -= 1
                if parts == k:
                    return v
```
