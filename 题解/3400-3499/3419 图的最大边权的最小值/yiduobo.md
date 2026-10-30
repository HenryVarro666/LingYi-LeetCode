---
title: "3419. 图的最大边权的最小值"
aliases: ["yiduobo的每日leetcode 3419.图的最大边权的最小值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/brainteaser", "leetcode/binary-search", "leetcode/shortest-path", "leetcode/heap-priority-queue", "题单/二分算法", "题单/图论算法", "题单/贪心算法", "题单/二分算法/二-二分答案", "题单/图论算法/三-最短路", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/32740334366"
zhihu_id: "32740334366"
zhihu_title: "yiduobo的每日leetcode 3419.图的最大边权的最小值"
question_id: "3419"
question: "图的最大边权的最小值"
problem_url: "https://leetcode.cn/problems/minimize-the-maximum-edge-weight-of-graph/"
difficulty: "Medium"
rating: 2243
created: "2025-03-25T23:11:27+08:00"
updated: "2025-03-25T23:11:27+08:00"
upvotes: 1
comments: 0
---

# 3419. 图的最大边权的最小值

> **[yiduobo的每日leetcode 3419.图的最大边权的最小值](https://zhuanlan.zhihu.com/p/32740334366) · 知乎 · 2025-03-25 · 赞同 1**
> 力扣：[3419. 图的最大边权的最小值](https://leetcode.cn/problems/minimize-the-maximum-edge-weight-of-graph/) · Medium · 灵茶山艾府：[两种方法：二分答案/Dijkstra（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3419.图的最大边权的最小值

[3419. 图的最大边权的最小值 - 力扣（LeetCode）](https://leetcode.cn/problems/minimize-the-maximum-edge-weight-of-graph/description/)

题目给出两个整数n和threshold，其中n可达10^5，而threshold在1到n - 1之间。同时给出一个n个节点的有向带权图，其中的节点编号为0到n - 1。现在需要从图中删去一些边（也可以不删），要求使得这个图：

1、从其他所有节点出发都可以到达节点0

2、图中剩余边的最大边权值尽可能小

3、每个节点至多有threshold条出去的边

问删除完必要的边之后，最大边权的最小值为多少。如果无法满足所有条件，则返回-1。

对于这类要求最大值最小的问题，第一想法自然还是二分答案。那么对于二分到的最大边权值mid，接下来需要检测其他所有节点能否在保证出度小于等于threshold的前提下到达0号节点。

如果不考虑出度的话，只需使用所有权重小于等于mid的边反向建图，从0号节点开始做bfs，检测能否遍历到所有节点就行了。另一方面，由于是反向建图的bfs，那么最终bfs路径上的每个节点的入度都为1，反过来说在正向图上的出度均为1，必然小于等于threshold，因此实际上完全无需考虑出度这个条件，直接按上面说的二分答案然后根据bfs进行判定就行了。

在具体实现上，不用每次都真正建图，而是通过判断原图中边权与mid的大小决定能否使用这条边。

另外对于-1这种情况的判断，由于正常情况下答案的上限应该是所有边权重的最大值，那么只需将二分的上限设置为这个最大值再加上1。若执行结束后得到的答案是上限，就说明无法抵达，此时返回-1即可。

最后附上python代码：

```python
class Solution(object):
    def minMaxWeight(self, n, edges, threshold):
        """
        :type n: int
        :type edges: List[List[int]]
        :type threshold: int
        :rtype: int
        """
        
        left, right = None, None
        for x, y, w in edges:
            if left is None or w < left:
                left = w
            if right is None or w > right:
                right = w
        
        right += 1
        ma = right
        while left < right:
            mid = (left + right) // 2
            g = [set() for x in range(n)]
            for x, y, w in edges:
                if w > mid:
                    continue
                g[y].add(x)
            
            q = [0]
            head, tail = 0, 1
            vis = set([0])
            while head < tail:
                x = q[head]
                head += 1
                for y in g[x]:
                    if y not in vis:
                        q.append(y)
                        vis.add(y)
                        tail += 1
            
            if tail == n:
                right = mid
            else:
                left = mid + 1
        
        if left == ma:
            return -1
        return left
```
