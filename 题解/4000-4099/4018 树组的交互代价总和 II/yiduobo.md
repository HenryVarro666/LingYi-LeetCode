---
title: "4018. 树组的交互代价总和II"
aliases: ["yiduobo的每日leetcode 4018.树组的交互代价总和II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/combinatorics", "leetcode/lowest-common-ancestor", "leetcode/sorting", "leetcode/binary-lifting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2071993980879999965"
zhihu_id: "2071993980879999965"
zhihu_title: "yiduobo的每日leetcode 4018.树组的交互代价总和II"
question_id: "4018"
question: "树组的交互代价总和 II"
problem_url: "https://leetcode.cn/problems/total-sum-of-interaction-cost-in-tree-groups-ii/"
difficulty: "Hard"
created: "2026-08-15T17:15:31+08:00"
updated: "2026-08-15T17:15:31+08:00"
upvotes: 1
comments: 0
---

# 4018. 树组的交互代价总和II

> **[yiduobo的每日leetcode 4018.树组的交互代价总和II](https://zhuanlan.zhihu.com/p/2071993980879999965) · 知乎 · 2026-08-15 · 赞同 1**
> 力扣：[4018. 树组的交互代价总和 II](https://leetcode.cn/problems/total-sum-of-interaction-cost-in-tree-groups-ii/) · Hard · 灵茶山艾府：[虚树](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4018.树组的交互代价总和II

<https://leetcode.cn/problems/total-sum-of-interaction-cost-in-tree-groups-ii/description/>

题目给出一个整数n以及一颗包含n个节点，编号从0到n - 1的无向树。树有一个长度为n - 1的二维数组edges表示，其中edges\[index\] \= \[u\[index\], v\[index\]\]，表示在u\[index\]到v\[index\]之间有一条无向边。n的规模可达10^5。

另外给出一个长度为n的整数数组group，其中group[index]表示分配给节点index的组标签。不同组的数量不超过n。

对于树中的两个节点u和v，若group[u]与group[v]相同，则认为u和v属于同一组，而二者的交互代价为从u到v路径上的边数。

现在要求计算所有满足条件的无序节点对(u, v)的交互代价之和，即u和v不同，且group[u]与group[v]相同。若不存在这样的节点对，则返回0。

之前3786题的加强版

[yiduobo的每日leetcode 3786.树组的交互代价总和](https://zhuanlan.zhihu.com/p/1986228911663772065)

本题中不同组别的数目的范围从20扩大到了n，那么之前的做法就不可行了。

沿着之前计算经过每个点的同组点对数目的思路继续往下，没找到什么特别好的思路，因为组别的枚举是必须要做的，但是不同点之间不太方便批量计算总和，所以卡住了。

那么不妨就换一个视角，重新考虑计算方式，然后再考虑优化。

之前是以经过某个点的视角展开的，那么在这里不妨改为计算经过某条边的视角展开：对于某条边和某个组别c，若其两侧组别为c的点的数目分别为x和y，那么这条边在这个组别上的贡献就是x \* y。更进一步的，x和y必然是父子关系，那么在这里不妨设x是y的父亲，那么这条边的贡献就是，以y为根节点的子树中，该组别的节点数量cnt[c][y]，乘以其他所有节点中组别为c的节点数目，也就是cnt[c][root] - cnt[c][y]。换言之，在这里可以通过计算所有子树中特定组别节点的数目来计算得到最终答案。

不过需要注意的是，以上算法的时间复杂度依然为O(n^2)，因为还是需要枚举所有的边以及组别。不过在这里就有优化的空间的，因为对于某种特定的组别，树中的某些边是无需考虑的，而某些边则是可以一同考虑的。

例如以下形态的树

A - B - x - C - D

|

E - F - y

其中x和y是组别为c的节点，那么对于c这个组别，A-B、B-x、x-C、C-D这些边都是没有必要计算的，因为这些边只有一侧存在组别为c的节点。而对于x-E、E-F以及F-y这三条边，则可以一同计算，因为这三边两侧的具有组别为c的节点的树结构实际上是相同的。

换言之，在这里就可以通过虚树来处理这个问题。所谓的虚树，指的是组别为c的所有节点，以及原树中连通这些节点的分岔点。

对于分岔点，一个自然的想法就是计算节点间的lca。不妨设组别为c的节点一共有k个，那么直观来看，这里需要O(k^2)的时间来两两枚举这些节点对，然后使用O(logn)的时间计算lca，时间复杂度依然很高。但是实际上，这些lca中大部分都是重复的。例如根节点root具备左右两颗子树，左子树中组别为c的节点有x个，右子树中组别为c的节点有y个，那么这x \* y组点对的lca都是root，产生了大量的重复计算。

对于这个问题，则可以利用dfs序来辅助计算，即在这里可以将这k个点先按照dfs排序，然后接下来只需要计算排序后相邻节点间的lca就行了。这样做的理由是同一子树中的节点在dfs序中是连续的，因此对于以上不同子树的节点对之间重复计算的问题，则可以通过前一颗子树中最后的节点与后一颗子树中最前的节点的单次计算得到。这样一来，找出分岔点的复杂度就优化到了O(klogn)。

接下来，只需将这最多2k - 1个节点建树，然后在这颗虚树中使用上面的贡献法计算最终答案即可。需要注意，虚树中的边是经过压缩的，因此对于某条边x - y，其贡献的计算出了最开始的cnt[y] \* (cnt[root] - cnt[y])之外，还需要额外乘以x到y中压缩的边的数量，即depth[y] - depth[x]。注意，这里只需要聚焦于组别c，因此cnt变为了一维，而整体的计算复杂度则变为了虚树的规模，即O(k)。

最后还有一个问题就是如何建树。在这里同样是利用dfs序，先将所有组别为c的节点，以及所有的lca节点按照dfs序排列。依照dfs序的性质，若排序后的数组中，某个节点与其左侧的另一个节点为lca就是这个左侧的节点，那么说明二者存在父子或者祖孙关系，否则说明当前节点已经是另一颗子树中的节点，左侧那个节点所在的子树已经建立完成。基于这一点，就可以利用栈来辅助建树。

首先将dfs序最靠前的节点作为根节点，并加入栈中。接下来对于剩下的节点，若当前节点与栈顶节点的lca不是栈顶节点，就弹出栈顶节点，理由是当前节点已经是另一颗子树中的节点了，栈顶节点对应的子树已经处理完毕了，因此可以将其弹出。重复此过程直到当前节点与栈顶节点的lca就是栈顶节点为止。接下来，建立栈顶节点到当前节点的边，将当前节点加入栈中，然后继续考虑后续节点即可。由于虚树中节点的数目不超过2k - 1个，因此建树的复杂度为O(klogn)。

对于每种颜色，找出lca以及建树的复杂度都是O(klogn)，计算结果的复杂度则为O(k)，因此总的时间复杂度就是O(nlogn)。

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
        
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)
        
        order = []
        depth = [0] * n
        nodes = {}
        f = [[] for _ in range(n)]

        def dfs(now, fa, d):
            order.append(now)
            f[now].append(fa)
            depth[now] = d
            if group[now] not in nodes:
                nodes[group[now]] = []
            nodes[group[now]].append(now)

            for nxt in g[now]:
                if nxt == fa:
                    continue
                dfs(nxt, now, d + 1)
        
        def lca(u, v):
            if depth[u] != depth[v]:
                if depth[u] < depth[v]:
                    u, v = v, u

                while depth[u] != depth[v]:
                    p = len(f[u]) - 1
                    while p > 0 and depth[u] - (1 << p) < depth[v]:
                        p -= 1
                    
                    u = f[u][p]
            
            while u != v:
                p = min(len(f[u]), len(f[v])) - 1
                while p > 0 and f[u][p] == f[v][p]:
                    p -= 1
                u = f[u][p]
                v = f[v][p]
            
            return u

        def calc(now, fa, t, c):
            global res

            cnt = 0
            for nxt in t.get(now, []):
                cnt += calc(nxt, now, t, c)
            
            if c == group[now]:
                cnt += 1

            if fa != -1:
                res += (depth[now] - depth[fa]) * (len(nodes[c]) - cnt) * cnt

            return cnt

        dfs(0, -1, 0)
        dfn = [0] * n
        for u in range(n):
            dfn[order[u]] = u

        updated = True
        p = 0
        while updated:
            updated = False
            p += 1
            for u in range(n):
                if len(f[u]) >= p and f[u][-1] != -1:
                    v = f[u][p - 1]
                    if len(f[v]) >= p and f[v][-1] != -1:
                        f[u].append(f[v][p - 1])
                        updated = True

        global res
        res = 0
        for c in nodes:
            if len(nodes[c]) < 2:
                continue
            
            t_set = set(nodes[c])
            for index in range(1, len(nodes[c])):
                u = lca(nodes[c][index], nodes[c][index - 1])
                if u not in t_set:
                    t_set.add(u)
            
            t_list = sorted(list(t_set), key=lambda d:dfn[d])
            
            t_root = t_list[0]
            stack = [t_list[0]]
            t = {}
            for u in t_list[1:]:
                while lca(stack[-1], u) != stack[-1]:
                    stack.pop()

                if stack[-1] not in t:
                    t[stack[-1]] = []
                t[stack[-1]].append(u)
                stack.append(u)
            
            calc(t_root, -1, t, c)
        
        return res
```
