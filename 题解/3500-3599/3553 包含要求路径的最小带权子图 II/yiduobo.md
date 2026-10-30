---
title: "3553. 包含给定路径的最小带权子树II"
aliases: ["yiduobo的每日leetcode 3553.包含给定路径的最小带权子树II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1909763939262243047"
zhihu_id: "1909763939262243047"
zhihu_title: "yiduobo的每日leetcode 3553.包含给定路径的最小带权子树II"
question_id: "3553"
question: "包含要求路径的最小带权子图 II"
problem_url: "https://leetcode.cn/problems/minimum-weighted-subgraph-with-the-required-paths-ii/"
difficulty: "Hard"
rating: 2411
created: "2025-05-25T19:22:18+08:00"
updated: "2025-05-25T19:22:18+08:00"
upvotes: 2
comments: 0
---

# 3553. 包含给定路径的最小带权子树II

> **[yiduobo的每日leetcode 3553.包含给定路径的最小带权子树II](https://zhuanlan.zhihu.com/p/1909763939262243047) · 知乎 · 2025-05-25 · 赞同 2**
> 力扣：[3553. 包含要求路径的最小带权子图 II](https://leetcode.cn/problems/minimum-weighted-subgraph-with-the-required-paths-ii/) · Hard · 灵茶山艾府：[【模板】最近公共祖先 LCA（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3553.包含给定路径的最小带权子树II

[3553. 包含给定路径的最小带权子树 II - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-weighted-subgraph-with-the-required-paths-ii/description/)

题目给出一颗具有n个节点的无向带权树，其中编号在0到n - 1之间。这棵树由一个二维整数数组edges表示，长度为n - 1，其中edges\[index\] \= \[u\[index\], v\[index\], w\[index\]\]，表示一条连接u\[index\]与v\[index\]的边，权重为w\[index\]，w的值均为正整数。

另外给出一个二维整数数组queries，其中queries\[index\] \= \[src1\[index\], src2\[index\], dest\[index\]\]。现在要求返回一个与queries长度相同的数组answer，其中answer\[index\]表示一个子树的最小总权重，使用这颗子树的边可以从src1\[index\]和src2\[index\]到达dest\[index\]。

由于树中的边权均为正整数，为了使得子树的总权重最小，就应该包含尽量少的边，也就是说子树中只应该包含src1到dest的最短路径以及src2到dest的最短路径中的边。

对于一组(src1, src2, dest)，从src1到dest的最短路径，就是从src1先走到src1和dest的最近公共祖先lca1，然后再从lca1走到dest。同样的，从src2到dest的最短路径则是从src2走到lca2，再从lca2走到dest。

需要注意的是，这两段路径之间可能存在重叠的部分，因此需要分情况进行讨论。

---

可以明确的是，lca1和lca2要么是同一个节点，要么是互为祖孙的两个节点。理由也很简单，因为lca1和lca2都是dest的祖先节点。

基于这一点，不妨先考虑lca1和lca2是同一个节点这种情况。对于这种情况，从lca1到dest以及从lca2到dest这一段路径只需要计算一次，但是对于从src1到lca1以及src2到lca2的这两段路径，其中依然可能出现重叠的部分，于是可以先计算src1和src2的最近公共祖先lca12，那么从src1到lca1的路径就可以拆分为src1到lca12，再从lca12到lca1，而src2到lca2的路径则可以拆分为src2到lca12，再从lca12到lca2。其中lca12到lca1以及lca12到lca2是同一段路径，只需要计算一次。

综合起来，需要计算的就是

src1到lca12的距离，src2到lca12的距离，lca12到lca1的距离，lca1到dest的距离

接下来考虑lca1和lca2不同的情况。对于这种情况，lca1和lca2可以先分个高下，不妨设这两个节点中深度较深的那个为lca_low，另一个为lca_high，那么从dest到lca_low的这段路径，必然是dest到lca_high这段路径的子路径，因此在这里只需要计算dest到lca_high的路径。另一方面，从src1到lca1以及src2到lca2的路径必然是不重叠的，否则这两个节点都可以通过lca_low走到dest，就不需要lca_high了。

综合起来，需要计算的就是

src1到lca1的距离，src2到lca2的距离，lca1和lca2中较浅的那个节点到dest的距离

---

到了这里，就得到了大致的算法，接下来的问题就是如何高效计算两个节点的lca，以及一组祖孙节点间的距离。后者是很容易计算的，只需要从根节点向下一趟dfs，记录每个节点到根节点的距离，那么一组祖孙节点间的距离就是这两个节点到根节点距离之差。而对于计算两个节点的lca这一问题，则可以通过dfs序配合线段树，或者节点向上行走的倍增算法来解决。我在这里选择的是倍增算法。

具体来说，对于节点now，令f\[now\]\[p\]表示从now开始，向上走2^p步可以到达的节点。那么对于节点now，首先有f\[now\]\[0\]为now的父亲节点，而对于p > 0的情况，f\[now\]\[p\]则可以认为是从now向上走2^(p - 1)走到的节点f\[now\]\[p - 1\]，再往上走2^(p - 1)步，也就是f\[f\[now\]\[p - 1\]\]\[p - 1\]。基于上面的结论，同样只需从根节点向下一趟dfs就可以计算得到f数组了。

有了f数组后，对于一组节点对(x, y)，不妨设其中较浅的节点为high，较深的节点为low，那么就可以先从low出发，利用f数组让low向上走到与high同一层级。

具体来说，就是倒序遍历p，不断选择最大的，且满足f[low][p]深度大于等于high的深度的p向上行走，直到low和high的深度相同。由于p是越来越小的，因此在O(logn)的时间内就可以让low向上走到与high同一深度。

接下来则需要让low和high同时向上行走，直到二者走到同一个节点。此时依然是倒序遍历p，但是选择的p要么为0，要么是最大的，且满足f[low][p]和f[high][p]不同的p。这里对于p > 0的情况要求f[low][p]与f[high][p]不同，是因为选择过大的p可能会走过头。

最后附上python代码：

```python
class Solution(object):
    def minimumWeight(self, edges, queries):
        """
        :type edges: List[List[int]]
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        n = len(edges) + 1
        f = [[] for _ in range(n)]
        level = [None] * n
        dis = [0] * n

        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append((y, w))
            g[y].append((x, w))
        
        def dfs(now, fa, f, depth):
            level[now] = depth
            if fa is not None:
                f[now].append(fa)
                p = fa
                while len(f[p]) >= len(f[now]):
                    f[now].append(f[p][len(f[now]) - 1])
                    p = f[now][-1]
            
            for nxt, w in g[now]:
                if nxt != fa:
                    dis[nxt] = dis[now] + w
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

        dfs(0, None, f, 0)
        res = []
        for src1, src2, dest in queries:
            lca1 = get_lca(src1, dest)
            lca2 = get_lca(src2, dest)
            if lca1 != lca2:
                res.append(dis[src1] + dis[src2] - dis[lca1] - dis[lca2])
                if level[lca1] < level[lca2]:
                    res[-1] += dis[dest] - dis[lca1]
                else:
                    res[-1] += dis[dest] - dis[lca2]

            else:
                lca12 = get_lca(src1, src2)
                res.append(dis[src1] + dis[src2] - dis[lca12] - dis[lca12] + dis[lca12] - dis[lca1] + dis[dest] - dis[lca1])

        return res
```
