---
title: "2467. 树上最大得分和路径"
aliases: ["yiduobo的每日leetcode 2467.树上最大得分和路径"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/tree", "leetcode/depth-first-search", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/587222716"
zhihu_id: "587222716"
zhihu_title: "yiduobo的每日leetcode 2467.树上最大得分和路径"
question_id: "2467"
question: "树上最大得分和路径"
problem_url: "https://leetcode.cn/problems/most-profitable-path-in-a-tree/"
difficulty: "Medium"
rating: 2053
created: "2022-11-27T23:19:33+08:00"
updated: "2022-11-27T23:19:33+08:00"
upvotes: 0
comments: 0
---

# 2467. 树上最大得分和路径

> **[yiduobo的每日leetcode 2467.树上最大得分和路径](https://zhuanlan.zhihu.com/p/587222716) · 知乎 · 2022-11-27 · 赞同 0**
> 力扣：[2467. 树上最大得分和路径](https://leetcode.cn/problems/most-profitable-path-in-a-tree/) · Medium · 灵茶山艾府：[两遍 DFS（视频讲解）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2467.树上最大得分和路径

[力扣](https://leetcode.cn/problems/most-profitable-path-in-a-tree/)

如果没有bob的存在，本题就是常规的bfs或者dfs，计算从根节点到当前节点的路径和，然后找出其中路径和最大的叶子节点，其对应的路径和就是最终答案。

接下来考虑如何消除bob的影响。

对于alice走的路径上的节点，若其没有在bob到根节点的路径上，那么其不会受到bob的影响，也就是说需要考虑的就是从bob到根节点路径上的节点，而对于这些节点，如果alice捷足先登，那么bob实际上也不会产生什么影响，因此实际上bob影响到的只有bob到根节点路径上前半部分节点的值。

由于alice不经过这些节点的话也不会受到这些节点变更的影响，那么就可以直接修改原树中节点的值，将bob到根节点路径上前半部分节点的值修改为0。这里需要特别注意的是，如果路径长度为奇数，那么正中间节点的值应该折半而不是变为0。

具体实现上，由于本题的节点是无法直接访问其父亲节点的，因此还是需要从根节点向下进行bfs或者dfs，记录每个节点的父亲节点。遍历完成后，从bob所在位置不断向上回溯直到回到根节点为止，期间的路径就是bob到根节点的路径，接下来执行上面的修改工作，这样一来就消除了bob的影响。

最后，只需要再进行一次常规的bfs或dfs找出最终答案就行了。

最后附上python代码：

```python
class Solution(object):
    def mostProfitablePath(self, edges, bob, amount):
        """
        :type edges: List[List[int]]
        :type bob: int
        :type amount: List[int]
        :rtype: int
        """

        n = len(edges) + 1
        g = {index : set() for index in range(n)}

        for x, y in edges:
            g[x].add(y)
            g[y].add(x)

        q = [bob]
        vis = set([bob])
        prev = {}
        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            for next in g[now]:
                if next not in vis:
                    vis.add(next)
                    prev[next] = now
                    q.append(next)
                    tail += 1
        
        bob_path = []
        now = 0
        while now != bob:
            bob_path.append(now)
            now = prev[now]
        bob_path.append(bob)
        
        left = 0
        right = len(bob_path) - 1
        while left < right:
            amount[bob_path[right]] = 0
            left += 1
            right -= 1

        if left == right:
            amount[bob_path[right]] /= 2
        
        res = None
        q = [[0, amount[0]]]
        head, tail = 0, 1
        vis = set([0])
        while head < tail:
            now, v = q[head]
            if now != 0 and len(g[now]) == 1 and (res is None or res < v):
                res = v

            head += 1
            for next in g[now]:
                if next not in vis:
                    vis.add(next)
                    q.append([next, v + amount[next]])
                    tail += 1

        return res
```
