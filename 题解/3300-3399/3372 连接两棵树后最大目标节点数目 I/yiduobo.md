---
title: "3372. 连接两棵树后最大目标节点数目I"
aliases: ["yiduobo的每日leetcode 3372.连接两棵树后最大目标节点数目I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/depth-first-search", "leetcode/brainteaser", "leetcode/enumeration", "leetcode/bao-li", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/三-一般树", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/28511516934"
zhihu_id: "28511516934"
zhihu_title: "yiduobo的每日leetcode 3372.连接两棵树后最大目标节点数目I"
question_id: "3372"
question: "连接两棵树后最大目标节点数目 I"
problem_url: "https://leetcode.cn/problems/maximize-the-number-of-target-nodes-after-connecting-trees-i/"
difficulty: "Medium"
rating: 1927
created: "2025-03-07T01:41:07+08:00"
updated: "2025-03-07T01:41:07+08:00"
upvotes: 1
comments: 0
---

# 3372. 连接两棵树后最大目标节点数目I

> **[yiduobo的每日leetcode 3372.连接两棵树后最大目标节点数目I](https://zhuanlan.zhihu.com/p/28511516934) · 知乎 · 2025-03-07 · 赞同 1**
> 力扣：[3372. 连接两棵树后最大目标节点数目 I](https://leetcode.cn/problems/maximize-the-number-of-target-nodes-after-connecting-trees-i/) · Medium · 灵茶山艾府：[脑筋急转弯+暴力枚举+直径优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3372.连接两棵树后最大目标节点数目I

[3372. 连接两棵树后最大目标节点数目 I - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-the-number-of-target-nodes-after-connecting-trees-i/description/)

题目给出两颗无向树，分别具有n和m个节点，n和m都不超过1000。两棵树中的节点编号分别为0到n - 1以及0到m - 1。同时给出两个二维整数数组edges1和edges2，分别表示两棵树中相连的边。

接下来给出一个整数k，若节点u和节点v之间的路径长度小于等于k，那么就称u是v的目标节点。另外一个节点必然是其自身的目标节点。

现在要求返回一个长度为n的数组answer，其中answer[i]表示将第一棵树中的某个节点与第二棵树种的某个节点连接一条边之后，第一棵树中节点i的目标节点的最大值。每次查询都是独立的，也就是说下一次查询时上一次连的边需要被去除掉。

由于题目中每次只能在两课时的节点间添加一条边，因此添加后也不可能形成环，换言之，无论如何添加边，第一棵树中节点间的距离是固定的。因此在这里可以先遍历第一棵树中的每个节点，以当前节点为起点执行最多k轮bfs，找出距离当前节点距离小于等于k的节点数目，也就是当前节点在第一棵树中的目标节点数目。

另一方面，不妨设与第一棵树中节点i相连的节点是第二棵树中的节点j，那么i在第二棵树中的目标节点，都必然需要先经过节点j，再到达节点i，也就是说i在第二棵树中的目标节点，实际上也认为是j在第二棵树中距离为k - 1的目标节点。这个值同样只与第二棵树本身的结构有关，与新添加的边无关，因此对于第一棵树中的每个节点i，都应该与第二棵树中拥有最多的距离为k - 1的目标节点数目的节点j相连。于是可以按相同的方法遍历第二棵树中的每个节点，以当前节点为起点执行最多k - 1轮bfs，找出当前节点在第二棵树中的距离为k - 1的目标节点数目。

综合起来，就是对于第一棵树，以每个节点为起点执行最多k轮bfs，计算每个节点的目标节点数目数组cnt1。接下来对于第二棵树，以每个节点为起点执行最多k - 1轮bfs，计算每个节点的距离为k - 1的目标节点数目数组cnt2。然后取cnt2中的最大值ma，与cnt1中的每个值相加即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxTargetNodes(self, edges1, edges2, k):
        """
        :type edges1: List[List[int]]
        :type edges2: List[List[int]]
        :type k: int
        :rtype: List[int]
        """
        
        def calc(edge, k):
            n = len(edge) + 1
            if k < 0:
                return [0] * n
            elif k == 0:
                return [1] * n

            res = [0] * n

            g = {x : set() for x in range(n)}
            for x, y in edge:
                g[x].add(y)
                g[y].add(x)
            
            for start in range(n):
                q = [start]
                vis = set([start])
                head, tail = 0, 1
                rnd = 0
                while head < tail and rnd < k:
                    rnd += 1
                    for x in q[head : tail]:
                        for y in g[x]:
                            if y not in vis:
                                vis.add(y)
                                q.append(y)
                    
                    head, tail = tail, len(q)
                
                res[start] = tail
            
            return res

        cnt1 = calc(edges1, k)
        cnt2 = calc(edges2, k - 1)
        ma = max(cnt2)
        return [v + ma for v in cnt1]
```
