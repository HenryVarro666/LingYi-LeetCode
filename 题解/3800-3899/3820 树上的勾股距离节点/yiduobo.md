---
title: "3820. 树上的勾股距离节点"
aliases: ["yiduobo的每日leetcode 3820.树上的勾股距离节点"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/enumeration", "leetcode/sorting", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1998876645646413845"
zhihu_id: "1998876645646413845"
zhihu_title: "yiduobo的每日leetcode 3820.树上的勾股距离节点"
question_id: "3820"
question: "树上的勾股距离节点"
problem_url: "https://leetcode.cn/problems/pythagorean-distance-nodes-in-a-tree/"
difficulty: "Medium"
rating: 1725
created: "2026-01-26T23:11:55+08:00"
updated: "2026-01-26T23:11:55+08:00"
upvotes: 0
comments: 0
---

# 3820. 树上的勾股距离节点

> **[yiduobo的每日leetcode 3820.树上的勾股距离节点](https://zhuanlan.zhihu.com/p/1998876645646413845) · 知乎 · 2026-01-26 · 赞同 0**
> 力扣：[3820. 树上的勾股距离节点](https://leetcode.cn/problems/pythagorean-distance-nodes-in-a-tree/) · Medium · 灵茶山艾府：[计算 x y z 到每个点的距离（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3820.树上的勾股距离节点

<https://leetcode.cn/problems/pythagorean-distance-nodes-in-a-tree/description/>

题目给出一个整数n，以及一颗包含n个节点的树，树中节点的编号从0到n - 1。这棵树由一个长度为n - 1的二维数组edges表示，其中edges\[index\] \= \[u\[index\], v\[index\]\]，表示u\[index\]到v\[index\]之间存在一条无向边。

另外给出三个不同的目标节点x、y、z。对于树中的任意节点u，令dx、dy、dz分别为u到节点x、y、z的距离。若这三个距离构成一个勾股数元组，则称u为特殊节点。

问数中有多少个特殊节点。

为了判断一个节点u是否为特殊节点，需要知道u到x、y、z的距离。反过来，也可以理解成需要直到x、y、z到u的距离。更进一步的，如果想要判断树中每个节点是否为特殊节点，就需要直到x、y、z到树中所有节点的距离，于是可以分别从x、y、z出发，执行三次bfs，计算这三个节点到树中其他节点的距离。接下来只需遍历树中的每个节点，判断x、y、z到这个节点的三个距离能否形成勾股数元组即可。

最后附上python代码：

```python
class Solution(object):
    def specialNodes(self, n, edges, x, y, z):
        """
        :type n: int
        :type edges: List[List[int]]
        :type x: int
        :type y: int
        :type z: int
        :rtype: int
        """
        
        def bfs(start):
            q = [start]
            dis = [-1] * n
            dis[start] = 0

            head, tail = 0, 1
            while head < tail:
                now = q[head]
                head += 1
                for nxt in g[now]:
                    if dis[nxt] == -1:
                        dis[nxt] = dis[now] + 1
                        q.append(nxt)
                        tail += 1
            
            return dis

        g = [[] for _ in range(n)]
        for u, v in edges:
            g[u].append(v)
            g[v].append(u)

        dx = bfs(x)
        dy = bfs(y)
        dz = bfs(z)

        res = 0
        for u in range(n):
            a, b, c = sorted([dx[u], dy[u], dz[u]])
            if a * a + b * b == c * c:
                res += 1
        
        return res
```
