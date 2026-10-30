---
title: "3515. 带权树中的最短路径"
aliases: ["yiduobo的每日leetcode 3515.带权树中的最短路径"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/depth-first-search", "leetcode/binary-indexed-tree", "leetcode/recursion", "leetcode/prefix-sum", "题单/常用数据结构", "题单/链表-二叉树与回溯", "题单/常用数据结构/八-树状数组和线段树", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1902537137397699908"
zhihu_id: "1902537137397699908"
zhihu_title: "yiduobo的每日leetcode 3515.带权树中的最短路径"
question_id: "3515"
question: "带权树中的最短路径"
problem_url: "https://leetcode.cn/problems/shortest-path-in-a-weighted-tree/"
difficulty: "Hard"
rating: 2312
created: "2025-05-06T23:19:34+08:00"
updated: "2025-05-06T23:19:34+08:00"
upvotes: 1
comments: 0
---

# 3515. 带权树中的最短路径

> **[yiduobo的每日leetcode 3515.带权树中的最短路径](https://zhuanlan.zhihu.com/p/1902537137397699908) · 知乎 · 2025-05-06 · 赞同 1**
> 力扣：[3515. 带权树中的最短路径](https://leetcode.cn/problems/shortest-path-in-a-weighted-tree/) · Hard · 灵茶山艾府：[DFS 时间戳 + 差分树状数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3515.带权树中的最短路径

[3515. 带权树中的最短路径 - 力扣（LeetCode）](https://leetcode.cn/problems/shortest-path-in-a-weighted-tree/description/)

题目给出一个整数n以及一个根节点编号为1的无向带权树，数中包含n个编号为1到n的节点。这棵树由一个长度为n - 1的二维数组edges表示，其中edges\[index\] \= \[u\[index\], v\[index\], w\[index\]\]，表示在节点u\[index\]和v\[index\]之间有一条权重为w\[index\]的无向边。

另外给出一个二维整数数组queries，长度为q，对于其中的每个queries[index]，有两种可能：

[1, u, v, w']：将节点u和v之间的边权更新为w'，其中(u, v)保证是edges中存在的边

[2, x]：计算根节点1到节点x的最短路径距离

现在要求返回一个整数数组answer，记录了所有的第二种查询的结果。

如果没有修改边权的操作，那么只需从根节点向下一趟dfs，就可以计算出根节点到树中所有节点的距离。而对于修改操作[x, y, w']，不妨设x和y中的孩子节点为p，那么就相当于将以p为根节点的子树中所有节点到根节点的距离都加上w' - w，其中w是这条边的原始边权。

对于这类修改子树中所有节点值的问题，一种常见的处理方法是通过dfs，将树的问题转化为区间的问题，然后使用可以处理区间问题的方法，例如线段树来进行处理。

具体来说，在dfs过程中，可以使用一个数组order记录访问节点的顺序，同时对于每个节点，使用一个哈希表pos记录其在order中下标位置。那么当遍历到节点now时，可以先将now加入到order的末尾，然后记pos[now] \= len(order) - 1，接下来对于now的所有孩子节点进行递归遍历，在遍历完成后，此时order中从pos[now]开始，到order末尾的所有节点就都是以now为根节点的子树中的节点，于是可以记cover[now] \= len(order) - pos[now]，表示now在dfs序数组order中管辖的节点数量为cover[now]。

这样一来，对于某次修改操作(x, y, w)，设p为x和y中的孩子节点，那么以p为根节点的子树中的所有节点对应到order中的下标区间就是pos[p]到pos[p] + cover[p] - 1。这样一来，问题就从树的问题转化为了区间的问题。接下来只需对order建立线段树，树中所有节点值都为0。接下来对于每组修改操作，就可以根据上面的方法计算cover中的对应区间，然后利用线段树执行区间修改操作了。

而对于求值操作，则只需在初始距离的基础上，对线段树进行单点求值操作，将这两个值累加起来即可。

最后附上python代码：

```python
class Solution(object):
    def treeQueries(self, n, edges, queries):
        """
        :type n: int
        :type edges: List[List[int]]
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        g = {x : {} for x in range(1, n + 1)}
        for x, y, w in edges:
            g[x][y] = w
            g[y][x] = w

        pos = {}
        order = []
        length = {}
        cover = {}

        def dfs(pre, now, s, pos, order, length, cover):
            order.append(now)
            pos[now] = len(order) - 1
            length[now] = s

            for nxt in g[now]:
                if nxt == pre:
                    continue
                dfs(now, nxt, s + g[now][nxt], pos, order, length, cover)
            
            cover[now] = len(order) - pos[now]
        
        dfs(0, 1, 0, pos, order, length, cover)
        
        def update(now, left, right, start, end, v):
            if left == start and right == end:
                delta[now] += v
                return
            
            mid = (left + right) // 2
            if end <= mid:
                update(now + now + 1, left, mid, start, end, v)
            elif start > mid:
                update(now + now + 2, mid + 1, right, start, end, v)
            else:
                update(now + now + 1, left, mid, start, mid, v)
                update(now + now + 2, mid + 1, right, mid + 1, end, v)
        
        def get(now, left, right, p):
            if left == right:
                return delta[now]
            
            mid = (left + right) // 2
            if p <= mid:
                return delta[now] + get(now + now + 1, left, mid, p)
            else:
                return delta[now] + get(now + now + 2, mid + 1, right, p)

        n = len(order)
        delta = [0] * (n * 4)
        res = []
        for q in queries:
            if q[0] == 1:
                x, y, w = q[1:]
                if pos[x] < pos[y]:
                    p = y
                else:
                    p = x

                update(0, 0, n - 1, pos[p], pos[p] + cover[p] - 1, w - g[x][y])
                g[x][y] = w
                g[y][x] = w
            else:
                res.append(length[q[1]] + get(0, 0, n - 1, pos[q[1]]))
        
        return res
```
