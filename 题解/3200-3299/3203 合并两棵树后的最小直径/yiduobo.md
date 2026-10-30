---
title: "3203. 合并两棵树后的最小直径"
aliases: ["yiduobo的每日leetcode 3203.合并两棵树后的最小直径"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/dynamic-programming", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/三-一般树", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/707552416"
zhihu_id: "707552416"
zhihu_title: "yiduobo的每日leetcode 3203.合并两棵树后的最小直径"
question_id: "3203"
question: "合并两棵树后的最小直径"
problem_url: "https://leetcode.cn/problems/find-minimum-diameter-after-merging-two-trees/"
difficulty: "Hard"
rating: 2266
created: "2024-07-07T23:36:36+08:00"
updated: "2024-07-07T23:36:36+08:00"
upvotes: 0
comments: 0
---

# 3203. 合并两棵树后的最小直径

> **[yiduobo的每日leetcode 3203.合并两棵树后的最小直径](https://zhuanlan.zhihu.com/p/707552416) · 知乎 · 2024-07-07 · 赞同 0**
> 力扣：[3203. 合并两棵树后的最小直径](https://leetcode.cn/problems/find-minimum-diameter-after-merging-two-trees/) · Hard · 灵茶山艾府：[连接直径中点（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3203.合并两棵树后的最小直径

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-minimum-diameter-after-merging-two-trees/description/)

题目给出两颗节点数目分别为n和m的无向树，要求从这两颗树中分别找出一个节点，并将这个节点连接起来形成一颗新的树，问这颗新的树的最小直径是多少。

新形成的树中的最长路径可能经过新添加的边，也可能不经过新添加的边。当不经过新添加的边时，树的直径就可以认为是原始两颗树的直径的较大值，这两个值与选取哪两个节点连接起来无关。反之，当经过新添加的边时，为了使得路径长度尽量小，就应该分别选择两颗树中距离其他节点最大距离最小的点，也就是原始两颗树中最长路径的中点，而最长的距离则是原始两颗树的直径除以2向上取整。

根据上面的结论，只需使用双bfs法分别计算原始两颗树的直径d1和d2，那么当新的树的最长路径不经过新添加的边时，新的树的直径就是max(d1, d2)；当经过新添加的边时，分别选择d1和d2对应路径的中点进行连接，得到的最长路径就是(d1 + 1) // 2 + (d2 + 1) // 2 + 1。以上二者取较大值即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minimumDiameterAfterMerge(self, edges1, edges2):
        """
        :type edges1: List[List[int]]
        :type edges2: List[List[int]]
        :rtype: int
        """

        def calc(edges):

            def bfs(x):
                q = [x]
                head, tail = 0, 1
                vis = set([x])
                rnd = 0
                while head < tail:
                    rnd += 1
                    for x in q[head : tail]:
                        for y in g.get(x, set()):
                            if y not in vis:
                                vis.add(y)
                                q.append(y)
                    
                    head, tail = tail, len(q)
                
                return q[-1], rnd

            g = {}
            for x, y in edges:
                if x not in g:
                    g[x] = set()
                if y not in g:
                    g[y] = set()
                g[x].add(y)
                g[y].add(x)
            
            p, _ = bfs(0)
            q, d = bfs(p)

            return d - 1

        d1 = calc(edges1)
        d2 = calc(edges2)
        return max(d1, d2, (d1 + 1) // 2 + (d2 + 1) // 2 + 1)
```
