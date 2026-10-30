---
title: "323. 无向图中连通分量的数目"
aliases: ["yiduobo的每日leetcode 323.无向图中连通分量的数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/596390028"
zhihu_id: "596390028"
zhihu_title: "yiduobo的每日leetcode 323.无向图中连通分量的数目"
question_id: "323"
question: "无向图中连通分量的数目"
problem_url: "https://leetcode.cn/problems/number-of-connected-components-in-an-undirected-graph/"
created: "2023-01-04T03:05:39+08:00"
updated: "2023-01-04T03:05:39+08:00"
upvotes: 1
comments: 0
---

# 323. 无向图中连通分量的数目

> **[yiduobo的每日leetcode 323.无向图中连通分量的数目](https://zhuanlan.zhihu.com/p/596390028) · 知乎 · 2023-01-04 · 赞同 1**
> 力扣：[323. 无向图中连通分量的数目](https://leetcode.cn/problems/number-of-connected-components-in-an-undirected-graph/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

323.无向图中连通分量的数目

[力扣](https://leetcode.cn/problems/number-of-connected-components-in-an-undirected-graph/)

非常标准的利用并查集维护连通性的问题。

一开始图中n个节点将形成n个连通分量，接下来枚举所有的边。对于当前的边(x, y)，若x和y属于不同的连通分量，那么就需要将这两个连通分量合并，此时连通分量的总数应该减去一。所有边都枚举完后，剩下连通分量的数目即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def countComponents(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: int
        """

        res = n
        fa = range(n)

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        for x, y in edges:
            fa_x = find(x)
            fa_y = find(y)
            if fa_x != fa_y:
                fa[fa_x] = fa_y
                res -= 1
        
        return res
```
