---
title: "3600. 升级后最大生成树稳定性"
aliases: ["yiduobo的每日leetcode 3600.升级后最大生成树稳定性"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/union-find", "leetcode/graph", "leetcode/binary-search", "leetcode/minimum-spanning-tree", "leetcode/sorting", "题单/二分算法", "题单/常用数据结构", "题单/图论算法", "题单/二分算法/二-二分答案", "题单/常用数据结构/七-并查集", "题单/图论算法/四-最小生成树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1941272861735096813"
zhihu_id: "1941272861735096813"
zhihu_title: "yiduobo的每日leetcode 3600.升级后最大生成树稳定性"
question_id: "3600"
question: "升级后最大生成树稳定性"
problem_url: "https://leetcode.cn/problems/maximize-spanning-tree-stability-with-upgrades/"
difficulty: "Hard"
rating: 2301
created: "2025-08-19T23:08:36+08:00"
updated: "2025-08-19T23:08:36+08:00"
upvotes: 1
comments: 0
---

# 3600. 升级后最大生成树稳定性

> **[yiduobo的每日leetcode 3600.升级后最大生成树稳定性](https://zhuanlan.zhihu.com/p/1941272861735096813) · 知乎 · 2025-08-19 · 赞同 1**
> 力扣：[3600. 升级后最大生成树稳定性](https://leetcode.cn/problems/maximize-spanning-tree-stability-with-upgrades/) · Hard · 灵茶山艾府：[两种方法：二分答案 / Kruskal 算法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3600.升级后最大生成树稳定性

[3600. 升级后最大生成树稳定性 - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-spanning-tree-stability-with-upgrades/description/)

题目给出一个整数n，表示有编号从0到n - 1的n个节点。另外给出一个edges列表，其中edges\[index\] \= \[u\[index\], v\[index\], s\[index\], must\[index\]\]，其中u\[index\]和v\[index\]表示这两个节点之间有一条边，s\[index\]为这条边的强度，must\[index\]为一个0或1的整数，若must\[index\]为1，则表示这条边必须包含在生成树中，同时这条边不能升级。

接下来给出一个整数k，表示可以最多k次升级操作。每次操作，可以选择一条must \= 0的边，将其强度翻倍。每条边只能升级一次。

定义一颗生成树的稳定性为其中所有边的最小强度，问可以得到的生成树的最大稳定性。若无法得到合法的生成树，则返回-1。

按照题目的要求，必须先把must为1的边都加入到树中，若在这个过程中出现了环，那么直接返回-1。在处理完这些边之后，对于剩下的边，则可以参考kurskal算法的处理方法，将这些边按照强度从大到小进行排序，然后逐条遍历并尝试加入到树中，直到树中有n - 1条边为止。判断是否可以加入树中则同样可以使用并查集，包括最开始检测是否有环，也可以利用并查集来完成。

对于must为0的变，为了使得最小的边权最大，就应该将可以修改的边中边权最小的k条边翻倍，又由于往树中添加边是按边权从大到小进行的，因此可以使用一个数组记录所有添加到树中且must为0的边，将这个数组反转后将前k个元素翻倍，然后取这个数组中的最小边权。

而对于所有must为1的边，则可以使用一个变量，记录最后一条加入到树中且must为1的边的权重。

得到这两个权重后，取其中的较小值即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxStability(self, n, edges, k):
        """
        :type n: int
        :type edges: List[List[int]]
        :type k: int
        :rtype: int
        """
        
        edges.sort(key=lambda d:(d[-1], d[-2]), reverse=True)
        res = None
        fa = [index for index in range(n)]
        can_update = []
        cnt = 0

        def find(x, fa):
            if fa[x] != x:
                fa[x] = find(fa[x], fa)
            return fa[x]

        for u, v, s, must in edges:
            fa_u = find(u, fa)
            fa_v = find(v, fa)
            if fa_u == fa_v:
                if must == 1:
                    return -1
            else:
                cnt += 1
                if cnt >= n:
                    return -1

                fa[fa_u] = fa_v
                if must == 1:
                    res = s
                else:
                    can_update.append(s)
        
                if cnt == n - 1 and must == 0:
                    break
        
        if cnt < n - 1:
            return -1
        
        can_update.reverse()
        for index in range(min(k, len(can_update))):
            can_update[index] *= 2
        
        if can_update:
            other_min = min(can_update)
            if res is None or res > other_min:
                res = other_min
        
        return res
```
