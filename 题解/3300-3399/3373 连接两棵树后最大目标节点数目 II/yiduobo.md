---
title: "3373. 连接两棵树后最大目标节点数目II"
aliases: ["yiduobo的每日leetcode 3373.连接两棵树后最大目标节点数目II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/tree", "leetcode/depth-first-search", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/28750544609"
zhihu_id: "28750544609"
zhihu_title: "yiduobo的每日leetcode 3373.连接两棵树后最大目标节点数目II"
question_id: "3373"
question: "连接两棵树后最大目标节点数目 II"
problem_url: "https://leetcode.cn/problems/maximize-the-number-of-target-nodes-after-connecting-trees-ii/"
difficulty: "Hard"
rating: 2162
created: "2025-03-08T00:19:58+08:00"
updated: "2025-03-08T00:19:58+08:00"
upvotes: 0
comments: 0
---

# 3373. 连接两棵树后最大目标节点数目II

> **[yiduobo的每日leetcode 3373.连接两棵树后最大目标节点数目II](https://zhuanlan.zhihu.com/p/28750544609) · 知乎 · 2025-03-08 · 赞同 0**
> 力扣：[3373. 连接两棵树后最大目标节点数目 II](https://leetcode.cn/problems/maximize-the-number-of-target-nodes-after-connecting-trees-ii/) · Hard · 灵茶山艾府：[黑白染色（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3373.连接两棵树后最大目标节点数目II

[3373. 连接两棵树后最大目标节点数目 II - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-the-number-of-target-nodes-after-connecting-trees-ii/description/)

题目给出两颗无向树，分别具有n和m个节点，n和m的规模可以达到10^5。两棵树中的节点编号分别为0到n - 1以及0到m - 1。同时给出两个二维整数数组edges1和edges2，分别表示两棵树中相连的边。

接下来给出一个整数k，若节点u和节点v之间的路径长度为偶数，那么就称u是v的目标节点。另外一个节点必然是其自身的目标节点。

现在要求返回一个长度为n的数组answer，其中answer[i]表示将第一棵树中的某个节点与第二棵树种的某个节点连接一条边之后，第一棵树中节点i的目标节点的最大值。每次查询都是独立的，也就是说下一次查询时上一次连的边需要被去除掉。

本题与之前3373题类似，但是本题中关于目标节点的定义是距离为偶数，同时数据规模要大得多，因此处理方法也有所不同。

首先依然是想办法考察单独一颗树内的目标节点应该如何计算。由于题目的数据规模较大，因此从每个节点出发进行bfs，那么在这里可以先假设0号节点为根节点，然后从0号节点开始做bfs，不妨设dis[x]为x到0的距离。接下来对于一组节点(x, y)，记二者的最近公共祖先为lca，那么x到lca的距离就是dis[x] - dis[lca]，而y到lca的距离则为dis[y] - dis[lca]，二者之和就是x到y的距离，即dis[x] + dis[y] - dis[lca] \* 2。

可以发现，最后这一项dis[lca] \* 2对距离的奇偶性没有影响，因此只有当dis[x]和dis[y]同奇偶时，二者互为目标节点。根据这个结论，就可以先从第一棵树的节点0开始做bfs，根据距离的奇偶性将树中的节点分为两个部分，其中一个部分与节点0的距离为奇数，另一个部分与节点0的距离为偶数，那么每个节点在第一棵树中的目标节点数目就是其所属部分的节点数目。

另一方面，第二棵树中的节点可以按相同的方法分为两个部分。对于第一棵树中的节点i，只需将其与第二棵树中数量较少的那个部分中的任意节点相连，那么第二棵树中数量较多的那个部分中的所有节点就都是i的目标节点。

最后附上python代码：

```python
class Solution(object):
    def maxTargetNodes(self, edges1, edges2):
        """
        :type edges1: List[List[int]]
        :type edges2: List[List[int]]
        :rtype: List[int]
        """
        
        def calc(edges):
            n = len(edges) + 1
            cnt = [0] * 2
            mark = [-1] * n

            g = {x : set() for x in range(n)}
            for x, y in edges:
                g[x].add(y)
                g[y].add(x)
            
            q = [0]
            vis = set([0])
            mark[0] = 0

            head, tail = 0, 1
            cnt[0] += 1
            now = 0
            while head < tail:
                now = 1 - now
                for x in q[head : tail]:
                    for y in g[x]:
                        if y not in vis:
                            vis.add(y)
                            mark[y] = now
                            q.append(y)
                            cnt[now] += 1
                
                head, tail = tail, len(q)
            
            return [cnt[mark[x]] for x in range(n)]
        
        cnt1 = calc(edges1)
        cnt2 = calc(edges2)
        ma = max(cnt2)
        return [v + ma for v in cnt1]
```
