---
title: "2192. 有向无环图中一个节点的所有祖先"
aliases: ["yiduobo的每日leetcode 2192.有向无环图中一个节点的所有祖先"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/graph", "leetcode/recursion", "题单/图论算法", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/537592890"
zhihu_id: "537592890"
zhihu_title: "yiduobo的每日leetcode 2192.有向无环图中一个节点的所有祖先"
question_id: "2192"
question: "有向无环图中一个节点的所有祖先"
problem_url: "https://leetcode.cn/problems/all-ancestors-of-a-node-in-a-directed-acyclic-graph/"
difficulty: "Medium"
rating: 1788
created: "2022-07-05T00:19:54+08:00"
updated: "2022-07-05T00:19:54+08:00"
upvotes: 0
comments: 0
---

# 2192. 有向无环图中一个节点的所有祖先

> **[yiduobo的每日leetcode 2192.有向无环图中一个节点的所有祖先](https://zhuanlan.zhihu.com/p/537592890) · 知乎 · 2022-07-05 · 赞同 0**
> 力扣：[2192. 有向无环图中一个节点的所有祖先](https://leetcode.cn/problems/all-ancestors-of-a-node-in-a-directed-acyclic-graph/) · Medium · 灵茶山艾府：[两种方法：逆向/正向（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2192.有向无环图中一个节点的所有祖先

[力扣](https://leetcode.cn/problems/all-ancestors-of-a-node-in-a-directed-acyclic-graph/)

非常典型的拓扑排序问题。使用f[i]表示i的所有祖先构成的集合，那么对于节点i而言，f[i]就是其所有前置节点对应f的并集，再加上其所有的前置节点，因此需要执行一趟拓扑排序，在过程中计算f就行了。

最后附上python代码：

```python
class Solution(object):
    def getAncestors(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: List[List[int]]
        """

        f = [set() for _ in range(n)]
        g = {}
        ind = [0] * n
        for x, y in edges:
            if x not in g:
                g[x] = set()
            g[x].add(y)
            ind[y] += 1
        
        q = []
        for index in range(n):
            if ind[index] == 0:
                q.append(index)

        l = 0
        r = len(q)
        while l < r:
            now = q[l]
            l += 1
            for next in g.get(now, set()):
                f[next].update(f[now])
                f[next].add(now)
                ind[next] -= 1
                if ind[next] == 0:
                    q.append(next)
                    r += 1

        res = []
        for i in range(n):
            res.append([])
            for j in range(n):
                if j in f[i]:
                    res[-1].append(j)
        
        return res
```
