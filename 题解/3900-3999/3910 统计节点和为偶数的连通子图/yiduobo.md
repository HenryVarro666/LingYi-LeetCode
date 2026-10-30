---
title: "3910. 统计节点和为偶数的连通子图"
aliases: ["yiduobo的每日leetcode 3910.统计节点和为偶数的连通子图"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/depth-first-search", "leetcode/breadth-first-search", "leetcode/graph", "leetcode/recursion", "leetcode/enumeration", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2032253553868285479"
zhihu_id: "2032253553868285479"
zhihu_title: "yiduobo的每日leetcode 3910.统计节点和为偶数的连通子图"
question_id: "3910"
question: "统计节点和为偶数的连通子图"
problem_url: "https://leetcode.cn/problems/count-connected-subgraphs-with-even-node-sum/"
difficulty: "Hard"
rating: 1859
created: "2026-04-28T00:31:48+08:00"
updated: "2026-04-28T00:31:48+08:00"
upvotes: 0
comments: 0
---

# 3910. 统计节点和为偶数的连通子图

> **[yiduobo的每日leetcode 3910.统计节点和为偶数的连通子图](https://zhuanlan.zhihu.com/p/2032253553868285479) · 知乎 · 2026-04-28 · 赞同 0**
> 力扣：[3910. 统计节点和为偶数的连通子图](https://leetcode.cn/problems/count-connected-subgraphs-with-even-node-sum/) · Hard · 灵茶山艾府：[枚举子集 + 位运算 BFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3910.统计节点和为偶数的连通子图

<https://leetcode.cn/problems/count-connected-subgraphs-with-even-node-sum/description/>

题目给出一个无向图，其中有n个节点，编号从0到n - 1。n的大小不超过13。

另外给出一个大小为n的数组nums，其中nums[index]表示节点index的值，可以为0或者1。

图中的边由一个二维数组edges给出，其中edges\[index\] \= \[u\[index\], v\[index\]\]，表示在u\[index\]和v\[index\]之间有一条边。

现在考虑图中节点的非空子集s生成的诱导子图：

- 只保留s中的节点
- 只保留两个端点都在s中的边

问有多少个非空子集生成的诱导子图，满足生成的图是连通图，且s中节点值之和为偶数。

题目中n的规模较小，因此可以直接暴力枚举所有的点集，一共是2^n - 1种可能，这里减1是因为空集是不合法的。当n取到最大值13时，也不过八千多种情况，是完全没有性能问题的。

对于当前枚举到的节点集合，先从中任意取出一个节点，然后从这个节点开始执行bfs。需要注意这里bfs扩展队列的条件是相邻节点也必须在当前节点集合中。bfs结束后，若bfs的队列长度与节点集合的大小相同，那么就说明集合中的节点是连通的，此时只需再判断节点值之和是否为偶数，若是，则更新答案。

最后附上python代码：

```python
class Solution(object):
    def evenSumSubgraphs(self, nums, edges):
        """
        :type nums: List[int]
        :type edges: List[List[int]]
        :rtype: int
        """
        
        n = len(nums)
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        res = 0
        for state in range(1, (1 << n)):
            nodes = []
            for index in range(n):
                if state & (1 << index) == (1 << index):
                    nodes.append(index)
            
            nodes_set = set(nodes)
            q = [nodes[0]]
            vis = set([nodes[0]])
            head, tail = 0, 1
            s = 0
            while head < tail:
                for now in q[head : tail]:
                    s += nums[now]
                    for nxt in g[now]:
                        if nxt in nodes_set and nxt not in vis:
                            q.append(nxt)
                            vis.add(nxt)
                
                head, tail = tail, len(q)
            
            if len(q) == len(nodes) and s % 2 == 0:
                res += 1
        
        return res
```
