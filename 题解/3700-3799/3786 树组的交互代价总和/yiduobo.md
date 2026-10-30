---
title: "3786. 树组的交互代价总和"
aliases: ["yiduobo的每日leetcode 3786.树组的交互代价总和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/depth-first-search", "leetcode/math", "leetcode/combinatorics", "leetcode/sorting", "题单/链表-二叉树与回溯", "题单/贪心算法", "题单/链表-二叉树与回溯/三-一般树", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1986228911663772065"
zhihu_id: "1986228911663772065"
zhihu_title: "yiduobo的每日leetcode 3786.树组的交互代价总和"
question_id: "3786"
question: "树组的交互代价总和"
problem_url: "https://leetcode.cn/problems/total-sum-of-interaction-cost-in-tree-groups/"
difficulty: "Hard"
rating: 2139
created: "2025-12-26T01:35:50+08:00"
updated: "2025-12-26T01:35:50+08:00"
upvotes: 3
comments: 0
---

# 3786. 树组的交互代价总和

> **[yiduobo的每日leetcode 3786.树组的交互代价总和](https://zhuanlan.zhihu.com/p/1986228911663772065) · 知乎 · 2025-12-26 · 赞同 3**
> 力扣：[3786. 树组的交互代价总和](https://leetcode.cn/problems/total-sum-of-interaction-cost-in-tree-groups/) · Hard · 灵茶山艾府：[贡献法，附 O(nlogn) 虚树做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3786.树组的交互代价总和

<https://leetcode.cn/problems/total-sum-of-interaction-cost-in-tree-groups/description/>

题目给出一个整数n以及一颗包含n个节点，编号从0到n - 1的无向树。树有一个长度为n - 1的二维数组edges表示，其中edges\[index\] \= \[u\[index\], v\[index\]\]，表示在u\[index\]到v\[index\]之间有一条无向边。n的规模可达10^5。

另外给出一个长度为n的整数数组group，其中group[index]表示分配给节点index的组标签。最多只有20个不同的组。

对于树中的两个节点u和v，若group[u]与group[v]相同，则认为u和v属于同一组，而二者的交互代价为从u到v路径上的边数。

现在要求计算所有满足条件的无序节点对(u, v)的交互代价之和，即u和v不同，且group[u]与group[v]相同。若不存在这样的节点对，则返回0。

题目的数据规模比较大，直接计算显然是不行的。注意到需要计算的是交互代价的总和，那么就可以考虑使用共享法，分别计算每个节点为答案做出的贡献。

在这里不妨考虑以节点now为根节点的树中，组别为g的节点为答案做出的贡献。可以发现，其中的路径可以分为两种，分别是经过根节点now，即从某棵子树中的某个节点出发，走到根节点，然后走到另一颗子树中的某个节点的路径(当然也可以没有最后这一段，也就是根节点也是g这一组的一员)。另一种则是仅在某棵子树内部的路径。

对于后面这种情况，可以通过递归计算子树的方法计算得到，在这里无需考虑，因此在这里主要是分析前面这种情况。不妨设分布在now的不同子树nxt[0]、nxt[1]、...中且组别为g的节点分别为(nxt[0][0]、nxt[0][1]、...、)、(nxt[1][0]、nxt[1][1]、...)、...，那么对于其中的一组不同子树中的节点对，例如(nxt[0][0], nxt[1][0])，其交互代价就是nxt[0][0]到now的距离，再加上nxt[1][0]到now的距离。

方便起见，在这里记d[x][y]为nxt[x][y]到now的距离。

一般来说，会按照一定的顺序遍历这些子树，那么在这里很自然会考虑子树nxt[p]中所有节点与子树nxt[0]、nxt[1]、...、nxt[p - 1]这些子树中的所有节点形成的点对的代价之和。对于nxt[p][0]，则为

(d[p][0] + d[0][0]) + (d[p][0] + d[0][1]) + ... + (d[p][0] + d[1][0]) + (d[p][0] + d[1][1]) + ... + (d[p][0] + d[p - 1][0]) + (d[p][0] + d[p - 1][1]) + ...

将其中的d\[p\]\[0\]提取出来，那么一共有cnt\[nxt\[0\]\]\[g\] + cnt\[nxt\[1\]\]\[g\] + ... + cnt\[nxt\[p - 1\]\]\[g\]个d\[p\]\[0\]，其中cnt\[x\]\[g\]表示子树x中组别为g的节点的数量。

而对于剩下的部分，则为

(d[0][0] + d[0][1] + ... ) + (d[1][0] + d[1][1] + ...) + ... + (d[p - 1][0] + d[p - 1][1] + ...)

记s[x][g]为子树x中组别为g的节点到now的距离之和，那么就可以写成

s\[nxt\[0\]\]\[g\] + s\[nxt\[1\]\]\[g\] + ... + s\[nxt\[p - 1\]\]\[g\]

因此，nxt[p][0]与nxt[0]到nxt[p - 1]中所有节点形成的点对的总代价就是

d\[p\]\[0\] \* (cnt\[nxt\[0\]\]\[g\] + cnt\[nxt\[1\]\]\[g\] + ... + cnt\[nxt\[p - 1\]\]\[g\]) + (s\[nxt\[0\]\]\[g\] + s\[nxt\[1\]\]\[g\] + ... + s\[nxt\[p - 1\]\]\[g\])

同样的，对于nxt[p][k]就是

d\[p\]\[k\] \* (cnt\[nxt\[0\]\]\]\[g\] + cnt\[nxt\[1\]\]\[g\] + ... + cnt\[nxt\[p - 1\]\]\[g\]) + (s\[nxt\[0\]\]\[g\] + s\[nxt\[1\]\]\[g\] + ... + s\[nxt\[p - 1\]\]\[g\])

那么全部加起来就是

(d\[p\]\[0\] + d\[p\]\[1\] + ... + ...) \* (cnt\[nxt\[0\]\]\[g\] + cnt\[nxt\[1\]\]\[g\] + ... + cnt\[nxt\[p - 1\]\]\[g\]) + (s\[nxt\[0\]\]\[g\] + s\[nxt\[1\]\]\[g\] + ... + s\[nxt\[p - 1\]\]\[g\]) \* cnt\[nxt\[p\]\]\[g\]

最开始这一项实际上就是s\[nxt\[p\]\]\[g\]，因此最终可以写成

s\[nxt\[p\]\]\[g\] \* (cnt\[nxt\[0\]\]\[g\] + cnt\[nxt\[1\]\]\[g\] + ... + cnt\[nxt\[p - 1\]\]\[g\]) + (s\[nxt\[0\]\]\[g\] + s\[nxt\[1\]\]\[g\] + ... + s\[nxt\[p - 1\]\]\[g\]) \* cnt\[nxt\[p\]\]\[g\]

现在的问题就是如何计算cnt以及s。

首先cnt是很容易计算的。很明显，cnt\[now\]\[g\]就是cnt\[nxt\[0\]\]\[g\] + cnt\[nxt\[1\]\]\[g\] + ...。另外，若now自身也属于g这一组，那么还需要将cnt\[now\]\[g\]额外加上1。

而对于s\[now\]\[g\]的计算，则应该是(s\[nxt\[0\]\]\[g\] + cnt\[nxt\[0\]\]\[g\]) + (s\[nxt\[1\]\]\[g\] + cnt\[nxt\[1\]\]\[g\]) + ...，这里需要加上cnt\[nxt\[k\]\]\[g\]这一项是因为cnt\[nxt\[k\]\]\[g\]记录的是子树nxt\[k\]中的节点到nxt\[k\]的距离之和，那么到now的距离就需要对其中每个节点的距离都额外加上1，即nxt\[k\]到now的距离。一共是cnt\[nxt\[k\]\]\[g\]个节点，因此一共需要加上cnt\[nxt\[k\]\]\[g\]。

基于以上的结论，就可以从任意节点开始，例如0号节点开始，向下进行dfs。对于当前节点now，先根据其组别更新s\[now\]\[g\]以及cnt\[now\]\[g\]。接下来遍历其所有子树，递归计算子树同时得到对应的s\[nxt\[k\]\]\[g\]以及cnt\[nxt\[k\]\]\[g\]，使用这两个值更新s\[now\]\[g\]以及cnt\[now\]\[g\]，并通过上面的式子计算其与nxt\[0\]到nxt\[k - 1\]中节点的代价之和。

最后附上python代码：

```python
class Solution(object):
    def interactionCosts(self, n, edges, group):
        """
        :type n: int
        :type edges: List[List[int]]
        :type group: List[int]
        :rtype: int
        """
        
        t = [[] for _ in range(n)]
        s = [{} for _ in range(n)]
        cnt = [{} for _ in range(n)]

        for x, y in edges:
            t[x].append(y)
            t[y].append(x)

        def dfs(now, fa):
            s[now][group[now]] = 0
            cnt[now][group[now]] = 1
            res = 0
            for nxt in t[now]:
                if nxt == fa:
                    continue
                res += dfs(nxt, now)
                for g in s[nxt]:
                    s[now][g] = s[now].get(g, 0) + s[nxt][g] + cnt[nxt][g]
                    cnt[now][g] = cnt[now].get(g, 0) + cnt[nxt][g]
                    res += (s[nxt][g] + cnt[nxt][g]) * (cnt[now].get(g, 0) - cnt[nxt][g]) + cnt[nxt][g] * (s[now][g] - s[nxt][g] - cnt[nxt][g])

            return res
        
        return dfs(0, -1)
```
