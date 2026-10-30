---
title: "3559. 给边赋权值的方案数II"
aliases: ["yiduobo的每日leetcode 3559.给边赋权值的方案数II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/depth-first-search", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1909811428136813781"
zhihu_id: "1909811428136813781"
zhihu_title: "yiduobo的每日leetcode 3559.给边赋权值的方案数II"
question_id: "3559"
question: "给边赋权值的方案数 II"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-assign-edge-weights-ii/"
difficulty: "Hard"
rating: 2146
created: "2025-05-27T22:24:36+08:00"
updated: "2025-05-27T22:24:36+08:00"
upvotes: 1
comments: 0
---

# 3559. 给边赋权值的方案数II

> **[yiduobo的每日leetcode 3559.给边赋权值的方案数II](https://zhuanlan.zhihu.com/p/1909811428136813781) · 知乎 · 2025-05-27 · 赞同 1**
> 力扣：[3559. 给边赋权值的方案数 II](https://leetcode.cn/problems/number-of-ways-to-assign-edge-weights-ii/) · Hard · 灵茶山艾府：[【模板】最近公共祖先 LCA（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3559.给边赋权值的方案数II

[3559. 给边赋权值的方案数 II - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-ways-to-assign-edge-weights-ii/description/)

题目给出一颗具有n个节点的无向树，节点从1到n编号，其中1号节点为树的根节点。树由一个长度为n - 1的二维数组edges表示，其中edges\[index\] \= \[u\[index\], v\[index\]\]，表示在节点u\[index\]和v\[index\]之间有一条边。

一开始，树中所有边的权重都为0，可以将每条边的权重设置为1或者2。两个节点u和v之间的路径的代价为链接二者的路径上所有边的权重之和。

现在给出一个二维整数数组queries，对于每个queries\[index\] \= \[u\[index\], v\[index\]\]，计算从u\[index\]到v\[index\]的路径上使得路径代价为奇数的权重分配方案数量。对于单个查询，只考虑路径上的变，忽略其他的边。

上一题的加强版，本题需要计算每组queries中节点间的边权赋值方案数。处理方法类似，也是先计算两点之间边的数量cnt，然后计算cnt的赋值方案数。

其中两点间边的数量，可以先计算两点的最近公共祖先lca，然后分别计算这两个点到lca的距离之和。刚好前不久写过的3553题也需要计算lca以及距离，可以直接参考之前使用的倍增法来进行计算。

[yiduobo：yiduobo的每日leetcode 3553.包含给定路径的最小带权子树II](https://zhuanlan.zhihu.com/p/1909763939262243047)

而对于赋值方案数的计算，则可以直接利用上一题得到的结论，即赋值方案数为2^(cnt - 1)。需要特别注意的是，本题中的u和v可能相同，这种情况下的答案为0，需要对其进行特殊处理。

[yiduobo：yiduobo的每日leetcode 3558.给边赋权值的方案数I](https://zhuanlan.zhihu.com/p/1909807666919872482)

最后附上python代码：

```python
class Solution(object):
    def assignEdgeWeights(self, edges, queries):
        """
        :type edges: List[List[int]]
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        n = len(edges) + 1
        g = [[] for _ in range(n + 1)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        f = [[] for _ in range(n + 1)]
        level = [None] * (n + 1)

        def dfs(now, fa, f, depth):
            level[now] = depth
            if fa is not None:
                f[now].append(fa)
                p = fa
                while len(f[p]) >= len(f[now]):
                    f[now].append(f[p][len(f[now]) - 1])
                    p = f[now][-1]
            
            for nxt in g[now]:
                if nxt != fa:
                    dfs(nxt, now, f, depth + 1)

        def get_lca(x, y):
            if level[x] > level[y]:
                low, high = x, y
            else:
                low, high = y, x
            
            p = len(f[low]) - 1
            while level[low] != level[high]:
                while p >= len(f[low]) or level[f[low][p]] < level[high]:
                    p -= 1
                low = f[low][p]

            p = len(f[low]) - 1
            while low != high:
                while p >= len(f[low]) or (p > 0 and f[low][p] == f[high][p]):
                    p -= 1
                low = f[low][p]
                high = f[high][p]
            
            return low
        
        def quick_pow(p):
            if p == 0:
                return 1
            if p == 1:
                return 2
            
            v = quick_pow(p // 2)
            v = v * v % mod
            if p & 1:
                v = v * 2 % mod
            return v

        dfs(1, None, f, 0)
        mod = 10 ** 9 + 7
        res = []
        for x, y in queries:
            lca = get_lca(x, y)
            length = level[x] + level[y] - level[lca] - level[lca]
            if length == 0:
                res.append(0)
            else:
                res.append(quick_pow(length - 1))
        
        return res
```
