---
title: "947. 移除最多的同行或同列石头"
aliases: ["yiduobo的每日leetcode 947.移除最多的同行或同列石头"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/union-find", "leetcode/graph", "leetcode/hash-table", "题单/常用数据结构", "题单/常用数据结构/七-并查集"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/359103285"
zhihu_id: "359103285"
zhihu_title: "yiduobo的每日leetcode 947.移除最多的同行或同列石头"
question_id: "947"
question: "移除最多的同行或同列石头"
problem_url: "https://leetcode.cn/problems/most-stones-removed-with-same-row-or-column/"
difficulty: "Medium"
rating: 2035
created: "2021-03-22T22:45:19+08:00"
updated: "2021-03-22T22:45:19+08:00"
upvotes: 0
comments: 0
---

# 947. 移除最多的同行或同列石头

> **[yiduobo的每日leetcode 947.移除最多的同行或同列石头](https://zhuanlan.zhihu.com/p/359103285) · 知乎 · 2021-03-22 · 赞同 0**
> 力扣：[947. 移除最多的同行或同列石头](https://leetcode.cn/problems/most-stones-removed-with-same-row-or-column/) · Medium · 灵茶山艾府：[中介并查集（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

947.移除最多的同行或同列石头

[力扣](https://leetcode-cn.com/problems/most-stones-removed-with-same-row-or-column/)

题目要求只有当某块石头的同行或者同列上有石头，才能将其移除，那么我们应该想办法体现出同行或同列之间的联系。

一个自然的想法是将每块石头视为图中的一个点，那么若两块石头同行或者同列，则在这两点之间连一条边。这样一来，就可以得到一张无向图，其中可能存在若干个连通块。对于每个连通块而言，设其中有k个节点，那么至多可以删去k - 1个节点。这里不给出严格的证明，但是一个简单的想法是每次删去当前度最小的节点，这样可以保证不会将剩下的连通块割裂成多个部分。

上面这种做法由于需要建图，因此时间复杂度是O(n^2)的。注意到同一行或同一列这个条件实际上是一个多对多的关系，即同一行或同一列上的多个节点必然属于同一个连通块，因此我们也可以转换一下思路，不再将每个石头看做节点，而是将行和列看做节点。对于一个石头(x, y)，我们可以看做这块石头在行x以及列y之间连上了一条边，而最后依然是每个连通块中将遗留下一个石头。

对于求解连通块的操作，可以建图然后dfs，不过这样做的时间复杂度比较高。一个更简洁的做法是使用并查集，即对于石头(x, y)，我们将横坐标的x与纵坐标的y进行一次合并操作，最终只需要判断每个出现的横纵坐标的最原始父亲是否等于其自身即可。

在这里直接使用x和y作为节点编号将会混淆，注意到这里有x \<\= 10000，那么我们将y加上10001之后就可以避免混淆的问题了。

最后附上python代码：

```python
class Solution(object):
    def removeStones(self, stones):
        """
        :type stones: List[List[int]]
        :rtype: int
        """

        fa = {}

        for row, col in stones:
            self.union(row, col + 10001, fa)

        res = len(stones)
        for x in fa:
            if self.find(x, fa) == x:
                res -= 1

        return res

    def union(self, x, y, fa):
        if x not in fa:
            fa[x] = x
        if y not in fa:
            fa[y] = y
        fa_x = self.find(x, fa)
        fa_y = self.find(y, fa)
        if fa_x < fa_y:
            fa[fa_y] = fa_x
        else:
            fa[fa_x] = fa_y
    
    def find(self, x, fa):
        if x != fa[x]:
            fa[x] = self.find(fa[x], fa)
        
        return fa[x]
```
