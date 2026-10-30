---
title: "261. 以图判树"
aliases: ["yiduobo的每日leetcode 261.以图判树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/593244479"
zhihu_id: "593244479"
zhihu_title: "yiduobo的每日leetcode 261.以图判树"
question_id: "261"
question: "以图判树"
problem_url: "https://leetcode.cn/problems/graph-valid-tree/"
created: "2022-12-20T22:25:38+08:00"
updated: "2022-12-20T22:25:38+08:00"
upvotes: 1
comments: 0
---

# 261. 以图判树

> **[yiduobo的每日leetcode 261.以图判树](https://zhuanlan.zhihu.com/p/593244479) · 知乎 · 2022-12-20 · 赞同 1**
> 力扣：[261. 以图判树](https://leetcode.cn/problems/graph-valid-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

261.以图判树

[力扣](https://leetcode.cn/problems/graph-valid-tree/)

首先，如果给出的图是一棵树，那么图中边的数量必须恰好等于节点数量减去1，因此可以先检测数组edges的长度是否恰好等于n - 1，若不等于，那么直接返回false。

接下来，只需要图中不存在环，就可以确定这是一颗树了。对于这个问题，则可以构图后bfs或dfs，或者直接枚举每条边，然后通过并查集来维护节点的连通情况。若某条边两侧节点的在并查集中的父亲节点是同一个，那么就说明这两个节点以及连通了，此时加入这条边就会形成环，那么返回false。若能顺利遍历完成，那么就说明这是一颗树。

最后附上python代码：

```python
class Solution(object):
    def validTree(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: bool
        """

        if len(edges) != n - 1:
            return False
        
        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        fa = range(n)
        for x, y in edges:
            fa_x = find(x)
            fa_y = find(y)
            if fa_x == fa_y:
                return False
            fa[fa_x] = fa_y
        
        return True
```
