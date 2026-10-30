---
title: "3543. K条边路径的最大边权和"
aliases: ["yiduobo的每日leetcode 3543.K条边路径的最大边权和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/depth-first-search", "leetcode/graph", "leetcode/topological-sort", "leetcode/hash-table", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十三-图-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1907591238657483497"
zhihu_id: "1907591238657483497"
zhihu_title: "yiduobo的每日leetcode 3543.K条边路径的最大边权和"
question_id: "3543"
question: "K 条边路径的最大边权和"
problem_url: "https://leetcode.cn/problems/maximum-weighted-k-edge-path/"
difficulty: "Medium"
rating: 2110
created: "2025-05-20T21:47:36+08:00"
updated: "2025-05-20T21:47:36+08:00"
upvotes: 1
comments: 0
---

# 3543. K条边路径的最大边权和

> **[yiduobo的每日leetcode 3543.K条边路径的最大边权和](https://zhuanlan.zhihu.com/p/1907591238657483497) · 知乎 · 2025-05-20 · 赞同 1**
> 力扣：[3543. K 条边路径的最大边权和](https://leetcode.cn/problems/maximum-weighted-k-edge-path/) · Medium · 灵茶山艾府：[三种方法，图中有环也能做（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3543.K条边路径的最大边权和

[3543. K 条边路径的最大边权和 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-weighted-k-edge-path/description/)

题目给出一个整数n以及一个包含n个节点的有向无环图，图中节点的编号为0到n - 1。该图由二维数组edges表示，其中edges\[index\] \= \[u\[index\], v\[index\], w\[index\]\]，表示有一条从u\[index\]出发到v\[index\]的有向边，权重为w\[index\]。节点数量n以及边的数量都不超过300。

另外给出两个整数k和t，其中k不超过300，t不超过600。现在要求找出图中一条边权和尽可能大的路径，这条路径中恰好包含k条边，同时边权之和必须小于t。问这个最大边权和为多少，若不存在，则返回-1。

对于这类有向图无环图中路径有关的问题，一种常见的处理方法就是记录从每个节点出发且满足某种条件的最优路径，这是一种天然的状态划分。

不过需要注意的是，对于有限制的最大值问题，一般的最大值状态表示是不可行的。例如使用f[now][k]表示从now出发，经过k条边后可以得到的不超过t的最大边权和，这种状态表示就不行，因为从某个节点出发的最优路径不一定可以更新其前置节点的最优路径。

例如现在存在一条节点0到节点1，边权为3的边，另外存在两条从节点1出发的边，其中一条到节点2，边权为4，另一条到节点3，边权为6。现在要求找出恰好包含两条边，且边权之和小于8的最大边权和。

按照上面f[now][k]的定义，可以得到f[1][1] \= 6，表示从1开始，经过1条边的最大权重为6，也就是1走到3这条边。但是对于f[0][2]而言，其不能使用f[1][1]更新，因为6 + 3 > 8，但是如果选择0->1->2的路径，其权重和为3 + 4 \= 7，是符合条件的。

基于这一点，就只能把所有可行的路径都记录下来。令f[now][k]表示从now出发，经过k条边可以得到的合法路径边权集合，那么对于f[now][k]，若k为0，那么f[now][k]中只有元素0，否则就需要枚举从now出发的所有边。对于当前枚举到的节点nxt以及边权w，先递归计算f[nxt][k - 1]，然后对于f[nxt][k - 1]中的所有元素v，若v + w小于t，就可以将v + w加入到f[now][k]中。

这样一来，只需遍历所有节点x，分别计算从每个节点出发对应的f[x][k]，取每种f[x][k]中包含的最大值更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxWeight(self, n, edges, k, t):
        """
        :type n: int
        :type edges: List[List[int]]
        :type k: int
        :type t: int
        :rtype: int
        """

        f = [[None for _ in range(k + 1)] for _ in range(n)]

        g = [[] for _ in range(n)]
        ind = [0] * n
        for x, y, w in edges:
            g[x].append((y, w))
        
        def dfs(now, k, f):
            if f[now][k] is None:
                f[now][k] = set()
                if k == 0:
                    f[now][k].add(0)
                else:
                    for nxt, w in g[now]:
                        dfs(nxt, k - 1, f)
                        for v in f[nxt][k - 1]:
                            if v + w < t:
                                f[now][k].add(v + w)

        res = -1
        for x in range(n):
            dfs(x, k, f)
            if f[x][k]:
                res = max(res, max(f[x][k]))
        
        return res
```
