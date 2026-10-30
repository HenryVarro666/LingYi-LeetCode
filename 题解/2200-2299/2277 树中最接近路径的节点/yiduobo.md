---
title: "2277. 树中最接近路径的节点"
aliases: ["yiduobo的每日leetcode 2277.树中最接近路径的节点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/629018444"
zhihu_id: "629018444"
zhihu_title: "yiduobo的每日leetcode 2277.树中最接近路径的节点"
question_id: "2277"
question: "树中最接近路径的节点"
problem_url: "https://leetcode.cn/problems/closest-node-to-path-in-tree/"
created: "2023-05-13T01:26:08+08:00"
updated: "2023-05-13T01:26:08+08:00"
upvotes: 0
comments: 0
---

# 2277. 树中最接近路径的节点

> **[yiduobo的每日leetcode 2277.树中最接近路径的节点](https://zhuanlan.zhihu.com/p/629018444) · 知乎 · 2023-05-13 · 赞同 0**
> 力扣：[2277. 树中最接近路径的节点](https://leetcode.cn/problems/closest-node-to-path-in-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2277.树中最接近路径的节点

[力扣](https://leetcode.cn/problems/closest-node-to-path-in-tree/)

题目的数据规模不大，因此可以直接使用暴力算法。对于每个询问(start, end, node)，从start开始bfs直到遍历到end，期间通过记录每个节点的上一个节点就可以得到从start到end的路径。接下来从node开始进行bfs，首个出现在start到end路径中的节点即为对应的答案。

不过本题还有更好的做法。首先，start到end的路径是经典的lca问题，也就是找出start和end的lca，那么start到end的路径就由start到lca以及lca到end这两条树链组成。接下来对于node，其所处位置有三种情况。为了方便区分，在这里记start与end的lca节点为lca_se。

1、node不在以lca_se为根节点的子树中。

这种情况下，start到end的路径上的所有节点都位于以lca为根节点的子树中，因此距离node最近的节点就是lca_se。但是有一个问题是不太好确定node是否不位于以lca_se为根节点的子树中，因此可以先考虑node位于以lca_se为根节点的子树中，然后对于其他情况就可以默认答案为lca_se。

2、node位于以lca_se为根节点的子树中。

这种情况下，又可以按lca_se以及其各子树分为四种情况：

2-1）node就是lca_se：

此时node就是最终答案

2-2）node属于lca_se的各子树中包含start的那一棵

此时node开始向上行走，必然会经过start与node的lca，记为lca_sn，而这个lca_sn恰好就是最终答案。这种情况可以对应到样例1中的节点6。

这种情况需要满足条件lca_sn是lca_se的子孙节点，同时lca_en恰好就是lca_se，这里的lca_en表示end与node的lca。

2-3）node属于lca_se的各子树中包含end的那一棵

此时与情况2-2对称，答案是lca_en。

这种情况需要满足条件lca_en是lca_se的子孙节点，同时lca_sn恰好就是lca_se。

2-4）对于lca_se的各子树，node既不属于start所在的这一棵，也不属于end所在的这一棵

这种情况下其实与大情况1类似，无非是树链的方向有所不同，而对应的答案同样是lca_se。另一方面，这种情况下有lca_se \= lca_sn \= lca_en。

综合上面这些情况，可以发现：

1、若lca_en \= lca_se，那么最终答案就是lca_sn

2、若lca_sn \= lca_se，那么最终答案就是lca_en

3、其他情况下，最终答案都是lca_se

到了这里，就可以通过start、end、node两两之间的lca的关系来确定最终答案，此时问题就变成了如何高效求解lca。对于lca问题，一种经典的处理方法是进行一次dfs，记录下dfs的欧拉序。欧拉序求解方法就是在dfs过程中，每次进入或者回溯到某个节点时，都将这个节点记录下来，dfs完成后记录下来的节点序列就是欧拉序。得到欧拉序之后，对于两个节点x和y的lca，就是x在欧拉序中首次出现的位置，以及y在欧拉序中首次出现的位置，这两个位置之间的区间中各个节点中深度最小的那个。可以发现，通过欧拉序就将lca问题转化成了静态区间最小值问题，可以使用st算法或者线段树来进行求解。

最后附上python代码：

```python
class Solution(object):
    def closestNode(self, n, edges, query):
        """
        :type n: int
        :type edges: List[List[int]]
        :type query: List[List[int]]
        :rtype: List[int]
        """

        global pos
        pos = -1

        f = [None] * 4096
        depth = [None] * n
        first = [None] * n
        g = [[] for _ in range(n)]

        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        def add(node, left, right, pos, now):
            if left == right:
                f[node] = now
                return
            
            if f[node] is None or depth[f[node]] > depth[now]:
                f[node] = now

            mid = (left + right) >> 1
            if pos <= mid:
                add(node + node + 1, left, mid, pos, now)
            else:
                add(node + node + 2, mid + 1, right, pos, now)

        def dfs(now, fa):
            global pos
            pos += 1

            if depth[now] is None:
                if fa is None:
                    depth[now] = 0
                else:
                    depth[now] = depth[fa] + 1
                
                first[now] = pos
            
            add(0, 0, 2047, pos, now)

            for next in g[now]:
                if next != fa:
                    dfs(next, now)
                    pos += 1
                    add(0, 0, 2047, pos, now)

        def get(node, left, right, start, end):
            if left == start and right == end:
                return f[node]
            
            mid = (left + right) >> 1
            if end <= mid:
                return get(node + node + 1, left, mid, start, end)
            elif start > mid:
                return get(node + node + 2, mid + 1, right, start, end)
            else:
                left_res = get(node + node + 1, left, mid, start, mid)
                right_res = get(node + node + 2, mid + 1, right, mid + 1, end)
                if depth[left_res] < depth[right_res]:
                    return left_res
                else:
                    return right_res

        def get_lca(x, y):
            start = first[x]
            end = first[y]
            if start > end:
                start, end = end, start
            
            return get(0, 0, 2047, start, end)

        dfs(0, None)
        res = []
        for start, end, node in query:
            lca_se = get_lca(start, end)
            lca_sn = get_lca(start, node)
            lca_en = get_lca(end, node)
            if lca_se == lca_sn:
                res.append(lca_en)
            elif lca_se == lca_en:
                res.append(lca_sn)
            else:
                res.append(lca_se)
        
        return res
```
