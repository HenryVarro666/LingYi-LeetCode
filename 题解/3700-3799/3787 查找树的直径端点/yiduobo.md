---
title: "3787. 查找树的直径端点"
aliases: ["yiduobo的每日leetcode 3787.查找树的直径端点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1987698123712266550"
zhihu_id: "1987698123712266550"
zhihu_title: "yiduobo的每日leetcode 3787.查找树的直径端点"
question_id: "3787"
question: "查找树的直径端点"
problem_url: "https://leetcode.cn/problems/find-diameter-endpoints-of-a-tree/"
created: "2025-12-26T01:52:20+08:00"
updated: "2025-12-26T01:52:20+08:00"
upvotes: 2
comments: 0
---

# 3787. 查找树的直径端点

> **[yiduobo的每日leetcode 3787.查找树的直径端点](https://zhuanlan.zhihu.com/p/1987698123712266550) · 知乎 · 2025-12-26 · 赞同 2**
> 力扣：[3787. 查找树的直径端点](https://leetcode.cn/problems/find-diameter-endpoints-of-a-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3787.查找树的直径端点

[3787. 查找树的直径端点 - 力扣（LeetCode）](https://leetcode.cn/problems/find-diameter-endpoints-of-a-tree/description/)

题目给出一颗编号为0到n - 1的有n个节点的无向树。另外给出一个长度为n - 1的二维整数数组edges，其中edges\[index\] \= \[a\[index\], b\[index\]\]，表示a\[index\]和b\[index\]之间有一条边。

若一个节点是树的任意直径的端点，则称其为特殊节点。

现在要求判断数中每个节点是否为特殊节点。

回忆一下计算树直径的经典方法：先从树中任意节点出发，通过一趟bfs或者dfs，走到某个最远的节点，然后从这个最远的节点出发，再进行一趟bfs或者dfs，走到另一个最远的节点，这两个节点间的路径就是树的直径。

基于以上的方法，可以发现，两趟bfs或者dfs到达的所有最远节点都必然是直径的端点。更进一步的，应该不存在其他的端点。具体的证明可以参考上面计算树的之间的经典方法的证明，在这里就不展开了。

最后附上python代码：

```python
class Solution(object):
    def findSpecialNodes(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: str
        """
        
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)
        
        q = [0]
        dis = [-1] * n
        dis[0] = 0
        head, tail = 0, 1
        while head < tail:
            for now in q[head: tail]:
                for nxt in g[now]:
                    if dis[nxt] == -1:
                        dis[nxt] = dis[now] + 1
                        q.append(nxt)
            
            head, tail = tail, len(q)
        
        t = set()
        for x in range(n):
            if dis[x] == dis[q[-1]]:
                t.add(x)

        q = [q[-1]]
        dis = [-1] * n
        dis[q[0]] = 0
        head, tail = 0, 1
        while head < tail:
            for now in q[head: tail]:
                for nxt in g[now]:
                    if dis[nxt] == -1:
                        dis[nxt] = dis[now] + 1
                        q.append(nxt)
            
            head, tail = tail, len(q)
        
        for x in range(n):
            if dis[x] == dis[q[-1]]:
                t.add(x)

        res = []
        for x in range(n):
            if x in t:
                res.append('1')
            else:
                res.append('0')
        
        return ''.join(res)
```
