---
title: "1617. 统计子树中城市之间最大距离"
aliases: ["yiduobo的每日leetcode 1617.统计子树中城市之间最大距离"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/tree", "leetcode/depth-first-search", "leetcode/dynamic-programming", "leetcode/backtracking", "leetcode/enumeration", "leetcode/dfs", "leetcode/dp-on-trees", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/数学算法", "题单/链表-二叉树与回溯/三-一般树", "题单/链表-二叉树与回溯/四-回溯", "题单/动态规划/十二-树形-DP", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/435758152"
zhihu_id: "435758152"
zhihu_title: "yiduobo的每日leetcode 1617.统计子树中城市之间最大距离"
question_id: "1617"
question: "统计子树中城市之间最大距离"
problem_url: "https://leetcode.cn/problems/count-subtrees-with-max-distance-between-cities/"
difficulty: "Hard"
rating: 2309
created: "2021-11-20T23:33:30+08:00"
updated: "2021-11-20T23:33:30+08:00"
upvotes: 0
comments: 0
---

# 1617. 统计子树中城市之间最大距离

> **[yiduobo的每日leetcode 1617.统计子树中城市之间最大距离](https://zhuanlan.zhihu.com/p/435758152) · 知乎 · 2021-11-20 · 赞同 0**
> 力扣：[1617. 统计子树中城市之间最大距离](https://leetcode.cn/problems/count-subtrees-with-max-distance-between-cities/) · Hard · 灵茶山艾府：[【图解】回溯/二进制枚举/O(n^3)枚举直径端点（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1617.统计子树中城市之间最大距离

[力扣](https://leetcode-cn.com/problems/count-subtrees-with-max-distance-between-cities/)

首先，有一个定义叫做树的直径，其代表的就是一颗树中最长路径。那么在这里，题目就是给出一棵树，要求统计所有可能的子树的直径。

由于数据规模非常小，指数级算法是很容想到的。直接枚举树中有哪些节点，然后求这些点构成的子树的直径。

对于树的直径的求法，一种经典做法是从树中任选一个节点x开始bfs，找出距离x最远的节点u。接下来再从u开始进行bfs，找出离u最远的节点v，那么u到v之间的路径就是树的直径了。

关于这个做法的正确性证明这里就不展开了，因为需要分情况讨论，情况比较多。简单来说就是反证，若存在一条更长的路径pq，那么u里x最远以及v里u最远这两个前提必然有一个是不成立的。

在这里使用上面的做法还需要注意执行完从x出发的bfs后，需要优先判断是有遍历到了选择的所有节点，若没有，说明选出来的节点不连通形成不了树，那么自然也没有直径这一说了。

上面的做法时间复杂度位O(n \* 2^n)，但是总觉得应该存在多项式时间的算法，不过没有想出来。统计树中各个路径的长度是比较容易的，但是将这些路径合并成树同时还要去重，这里就没什么好的思路了。

最后附上python代码：

```python
class Solution(object):
    def countSubgraphsForEachDiameter(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: List[int]
        """

        res = [0] * (n - 1)
        g = {index : set() for index in range(n)}
        print g
        for x, y in edges:
            x -= 1
            y -= 1
            g[x].add(y)
            g[y].add(x)

        for state in range(1, 1 << n):
            node_set = set()
            for index in range(n):
                if state & (1 << index):
                    node_set.add(index)
                    s = index

            if len(node_set) == 1:
                continue
            
            node_set.remove(s)
            q = [s]
            l = 0
            r = 1
            while l < r:
                new_r = r
                for node in q[l : r]:
                    for next in g[node]:
                        if next in node_set:
                            node_set.remove(next)
                            q.append(next)
                            new_r += 1
                
                l, r = r, new_r
            
            if len(node_set) > 0:
                continue
            
            u = q[-1]
            node_set = set(q)
            node_set.remove(u)
            step = 0
            q = [u]
            l = 0
            r = 1
            while l < r:
                new_r = r
                step += 1
                for node in q[l : r]:
                    for next in g[node]:
                        if next in node_set:
                            node_set.remove(next)
                            q.append(next)
                            new_r += 1
                
                l, r = r, new_r

            res[step - 2] += 1
        
        return res
```
