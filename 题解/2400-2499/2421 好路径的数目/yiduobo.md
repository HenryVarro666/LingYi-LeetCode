---
title: "2421. 好路径的数目"
aliases: ["yiduobo的每日leetcode 2421.好路径的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/union-find", "leetcode/sorting", "题单/常用数据结构", "题单/链表-二叉树与回溯", "题单/常用数据结构/七-并查集", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/581676572"
zhihu_id: "581676572"
zhihu_title: "yiduobo的每日leetcode 2421.好路径的数目"
question_id: "2421"
question: "好路径的数目"
problem_url: "https://leetcode.cn/problems/number-of-good-paths/"
difficulty: "Hard"
rating: 2445
created: "2022-11-09T00:44:54+08:00"
updated: "2022-11-09T00:44:54+08:00"
upvotes: 0
comments: 0
---

# 2421. 好路径的数目

> **[yiduobo的每日leetcode 2421.好路径的数目](https://zhuanlan.zhihu.com/p/581676572) · 知乎 · 2022-11-09 · 赞同 0**
> 力扣：[2421. 好路径的数目](https://leetcode.cn/problems/number-of-good-paths/) · Hard · 灵茶山艾府：[并查集（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

由于剑指offer的题大部分都是题库里已经写过的，所以就不另外写题解了。计划先从之前的2421开始继续往后写，把新出来的这部分写完。

2421.好路径的数目

[力扣](https://leetcode.cn/problems/number-of-good-paths/)

题目的数据规模较大，感觉应该需要用到树分治相关的知识，不过在这里也有取巧的做法，即经典的倒推加判断连通的做法。

具体来说，就是先将树清空，然后按照节点值从小到大逐个将其加回到树中。由于是按照值从小到大的顺序加回到树中，那么对于当前加回到树中的值v而言，树中已有节点的值都是小于等于v的，也就是说任意一条两个端点均为v的路径都是要找的好路径。更进一步的，若一个连通块中有k个值为v的节点，那么就一共可以形成k \* (k - 1) / 2条好路径。

接下来要解决的就是如何判断连通。

由于连通是边带来的，因此在加回点的同时也要顺带把边加回去。对于树中的某条边(x, y)而言，可以认为其在x和y中值较大的一方被加回到树中时才生效，因此可以先将边按照两个端点中值较大的那一侧进行聚合，然后在这个值的节点被加回到树中时将这些边也加回到树中。

加回边之后，剩下判断连通的工作就可以交给并查集来处理。使用并查集计算出当前的连通块之后，可以通过查找每个值等于v的节点的父亲来统计每个连通块中包含值为v的节点的数量k，然后利用上面的结论计算每个连通块中好路径的数目并累加到答案中。

另外，不要忘了题目中单个点形成的路径也算是好路径，因此还需要将最后答案加上n。

最后附上python代码：

```python
class Solution(object):
    def numberOfGoodPaths(self, vals, edges):
        """
        :type vals: List[int]
        :type edges: List[List[int]]
        :rtype: int
        """

        n = len(vals)
        edge_set = {}
        node_set = {}
        for index, v in enumerate(vals):
            if v not in edge_set:
                edge_set[v] = set()
            if v not in node_set:
                node_set[v] = set()
            node_set[v].add(index)

        for index in range(n - 1):
            x, y = edges[index]
            if vals[x] > vals[y]:
                edge_set[vals[x]].add(index)
            else:
                edge_set[vals[y]].add(index)
        
        fa = range(n)

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        res = n
        for v in sorted(edge_set.keys()):
            for index in edge_set[v]:
                x, y = edges[index]
                fa_x = find(x)
                fa_y = find(y)

                if vals[fa_x] == v:
                    fa[fa_y] = fa_x
                else:
                    fa[fa_x] = fa_y
        
            cnt = {}
            for x in node_set[v]:
                fa_x = find(x)
                cnt[fa_x] = cnt.get(fa_x, 0) + 1
            
            for k in cnt.values():
                res += k * (k - 1) / 2

        return res
```
