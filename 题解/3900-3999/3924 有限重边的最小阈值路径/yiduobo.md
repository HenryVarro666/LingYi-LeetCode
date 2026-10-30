---
title: "3924. 有限重边的最小阈值路径"
aliases: ["yiduobo的每日leetcode 3924.有限重边的最小阈值路径"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-search", "leetcode/shortest-path", "题单/二分算法", "题单/图论算法", "题单/二分算法/二-二分答案", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2037711095276754938"
zhihu_id: "2037711095276754938"
zhihu_title: "yiduobo的每日leetcode 3924.有限重边的最小阈值路径"
question_id: "3924"
question: "有限重边的最小阈值路径"
problem_url: "https://leetcode.cn/problems/minimum-threshold-path-with-limited-heavy-edges/"
difficulty: "Hard"
rating: 2080
created: "2026-05-13T02:04:29+08:00"
updated: "2026-05-13T02:04:30+08:00"
upvotes: 0
comments: 0
---

# 3924. 有限重边的最小阈值路径

> **[yiduobo的每日leetcode 3924.有限重边的最小阈值路径](https://zhuanlan.zhihu.com/p/2037711095276754938) · 知乎 · 2026-05-13 · 赞同 0**
> 力扣：[3924. 有限重边的最小阈值路径](https://leetcode.cn/problems/minimum-threshold-path-with-limited-heavy-edges/) · Hard · 灵茶山艾府：[二分答案 + 0-1 BFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3924.有限重边的最小阈值路径

<https://leetcode.cn/problems/minimum-threshold-path-with-limited-heavy-edges/description/>

题目给出一张具有n个节点的无向带权图，图中的节点的编号从0到n - 1，且n的大小不超过1000。

这张图由一个二维整数数组edges表示，其中edges\[index\] \= \[u\[index\], v\[index\], w\[index\]\]，表示u\[index\]和v\[index\]之间存在一条权重为w\[index\]的无向边。edges中边的数量不超过1000，且边权最大不超过10^9。

另外给出三个整数source、target以及k。

现在要求确定一个最小的阈值threshold，使得图中存在至少一条从source到target的路径，且这条路径上权重大于threshold的边不超过k条。若找不到这样的threshold，则返回-1。

首先可以明确的是，阈值越大，受到权重限制的边就越少，就越容易找出可行的路径，因此在这里可以二分最终的threshold，将题目转化为判定问题。二分的下界自然为0，而上界则为图中边权的最大值ma。另外为了兼容无解的情况，在这里可以将二分上界设置为ma + 1，若最终二分的结果停留在ma + 1，则说明无解，此时可以返回-1。

接下来对于当前二分到的阈值mid，需要想办法判断是否存在从source到target，且其中权重大于mid的边不超过k条的路径。对于这个问题，可以从source开始贪心向外扩展。

具体来说，每一轮都先从当前source出发，选出那些可以仅通过权重不超过mid的边扩展得到的节点，并进行扩展，同时在这个过程中记录下那些可以到达，但是边权超过了mid的节点，然后从source扩展到前面这部分节点。这是一个非常标准的bfs过程，当bfs执行完成，说明已经找不到任何可以从source出发，不经过任何权重大于mid的边可达的节点。

接下来，从当前bfs队列的这些节点中，沿着边权大于mid的边向外扩展一步，将之前未到达的节点收集起来，接下来，再从这部分节点出发进行bfs，依然是找出不经过任何边权大于mid的边可达的节点，而这一轮bfs到达的节点，就是从source出发，仅经过一条权重大于mid的边可达的所有节点。

按照上述的流程执行k轮，就可以找出所有经过至多k条权重大于mid的边可达的所有节点，若这个过程中到达了target，那么说明最终答案小于等于当前的mid，将二分上界更新为mid，否则说明mid太小，需要将二分下界更新为mid + 1。

具体实现上，可以在有限制的bfs进行过程中，使用一个集合r记录当前可达的所有节点。当某个节点被加入bfs队列时，再将其从r中移除，这样一来，bfs结束后r中所有的节点，就恰好是当前不可达，但是通过一条新的权重大于mid的边就可达的节点了。此时只需要将r转化为下一轮的bfs起始队列，就能很方便地完成整个扩展流程。

最后附上python代码：

```python
class Solution(object):
    def minimumThreshold(self, n, edges, source, target, k):
        """
        :type n: int
        :type edges: List[List[int]]
        :type source: int
        :type target: int
        :type k: int
        :rtype: int
        """

        ma = 0
        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append((y, w))
            g[y].append((x, w))
            ma = max(ma, w)
        
        left = 0
        right = ma + 1
        while left < right:
            mid = (left + right) // 2

            q = [source]
            vis = set([source])
            head, tail = 0, 1
            r = set()
            for _ in range(k + 1):
                vis.update(r)
                r.clear()
                while head < tail:
                    for x in q[head : tail]:
                        for y, w in g[x]:
                            if y in vis:
                                continue
                            if w <= mid:
                                q.append(y)
                                vis.add(y)
                                if y in r:
                                    r.remove(y)
                            elif y not in r:
                                r.add(y)
                    
                    head, tail = tail, len(q)

                if target in vis:
                    break

                q = list(r)
                head, tail = 0, len(q)
                

            if target in vis:
                right = mid
            else:
                left = mid + 1
        
        if left == ma + 1:
            return -1
        return left
```
