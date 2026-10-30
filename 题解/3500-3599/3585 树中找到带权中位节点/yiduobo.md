---
title: "3585. 树中找到带权中位节点"
aliases: ["yiduobo的每日leetcode 3585.树中找到带权中位节点"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/dynamic-programming", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1938733742064666580"
zhihu_id: "1938733742064666580"
zhihu_title: "yiduobo的每日leetcode 3585.树中找到带权中位节点"
question_id: "3585"
question: "树中找到带权中位节点"
problem_url: "https://leetcode.cn/problems/find-weighted-median-node-in-tree/"
difficulty: "Hard"
rating: 2429
created: "2025-08-12T23:05:01+08:00"
updated: "2025-08-12T23:05:01+08:00"
upvotes: 1
comments: 0
---

# 3585. 树中找到带权中位节点

> **[yiduobo的每日leetcode 3585.树中找到带权中位节点](https://zhuanlan.zhihu.com/p/1938733742064666580) · 知乎 · 2025-08-12 · 赞同 1**
> 力扣：[3585. 树中找到带权中位节点](https://leetcode.cn/problems/find-weighted-median-node-in-tree/) · Hard · 灵茶山艾府：[【模板】最近公共祖先 LCA（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3585.树中找到带权中位节点

[3585. 树中找到带权中位节点 - 力扣（LeetCode）](https://leetcode.cn/problems/find-weighted-median-node-in-tree/description/)

题目给处一颗根节点为0的树，树中有n个节点，编号从0到n - 1。另外给出一个长度为n - 1的二维数组edges，表示树中的边，其中edges\[index\] \= \[u\[index\], v\[index\], w\[index\]\]，表示有一条从u\[index\]到v\[index\]的边，取中为w\[index\]。

定义带权中位节点为u到v路径上的第一个节点x，使得从u到x的边权之和大于等于u到v路径总权值的一半。

给出一个二维数组queries，对于queries\[index\] \= \[u\[index\], v\[index\]\]，要求计算u\[index\]到v\[index\]路径上的带权中位节点。

对于每组询问，题目都需要先计算树中两点u到v的路径，在这里就需要先想办法计算u和v的最近公共祖先lca，那么u到v的路径长度，就等于u到lca的路径长度，再加上v到lca的路径长度。接下来，记dis[x]为从根节点出发走到节点x的路径长度，那么u到lca的路径长度就是dis[u] - dis[lca]，同理，v到lca的路径长度就是dis[v] - dis[lca]。

lca可以通过倍增法计算得到，dis则可以在这个过程中顺便计算得到，具体的计算方法可以参考之前的3553题。

[yiduobo的每日leetcode 3553.包含给定路径的最小带权子树II](https://zhuanlan.zhihu.com/p/1909763939262243047)

接下来，记total_dis为u到v的路径总长度，那么当u到lca的距离大于等于total_dis的一半时，最终答案就落在u到lca的路径上，反之答案则会落在v到lca的路径上，此时则可以再次利用倍增的性质，从u或者v开始向上走，并将行走的路径长度累加起来，直到走到这个路径长度超过total_dis的一半为止。需要特别注意的是，从u开始走时，累加的距离必须大于等于total_dis的一半，但是从v开始走时，累加的距离必须刚好小于total_dis的一半，因为题目要找的是从u出发的中位节点。

最后附上python代码：

```python
class Solution(object):
    def findMedian(self, n, edges, queries):
        """
        :type n: int
        :type edges: List[List[int]]
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        g = [[] for _ in range(n)]
        for u, v, w in edges:
            g[u].append((v, w))
            g[v].append((u, w))
        
        dis = [0] * n
        level = [0] * n
        f = [[] for _ in range(n)]
        def dfs(now, fa, f, dis):
            if fa is not None:
                f[now].append(fa)
                while len(f[f[now][-1]]) >= len(f[now]):
                    f[now].append(f[f[now][-1]][len(f[now]) - 1])
            
            for nxt, w in g[now]:
                if nxt == fa:
                    continue
                dis[nxt] = dis[now] + w
                level[nxt] = level[now] + 1
                dfs(nxt, now, f, dis)
        
        def get_lca(x, y):
            high, low = x, y
            if level[high] > level[low]:
                high, low = low, high

            p = len(f[low]) - 1
            while level[low] != level[high]:
                while p > len(f[low]) - 1 or (p > 0 and level[f[low][p]] < level[high]):
                    p -= 1
                low = f[low][p]
            
            p = len(f[low]) - 1
            while low != high:
                while p > len(f[low]) - 1 or (p > 0 and level[f[low][p]] == level[f[high][p]]):
                    p -= 1
                
                low = f[low][p]
                high = f[high][p]
            
            return low

        dfs(0, None, f, dis)
        
        res = []
        for x, y in queries:
            lca = get_lca(x, y)
            total_dis = dis[x] + dis[y] - dis[lca] * 2
            if (dis[x] - dis[lca]) * 2 >= total_dis:
                d = 0
                while d * 2 < total_dis:
                    p = len(f[x]) - 1
                    while p > 0 and (d + dis[x] - dis[f[x][p]]) * 2 >= total_dis:
                        p -= 1
                    
                    d += dis[x] - dis[f[x][p]]
                    x = f[x][p]
                
                res.append(x)
            
            else:
                d = 0
                while d * 2 < total_dis:
                    p = len(f[y]) - 1
                    while p > 0 and (d + dis[y] - dis[f[y][p]]) * 2 > total_dis:
                        p -= 1
                    
                    if (d + dis[y] - dis[f[y][p]]) * 2 <= total_dis:
                        d += dis[y] - dis[f[y][p]]
                        y = f[y][p]
                    else:
                        break
                
                res.append(y)
        
        return res
```
