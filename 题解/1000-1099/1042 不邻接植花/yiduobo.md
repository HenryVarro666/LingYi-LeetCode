---
title: "1042. 不邻接植花"
aliases: ["yiduobo的每日leetcode 1042.不邻接植花"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/graph", "leetcode/hash-table", "题单/图论算法", "题单/图论算法/九-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/370784187"
zhihu_id: "370784187"
zhihu_title: "yiduobo的每日leetcode 1042.不邻接植花"
question_id: "1042"
question: "不邻接植花"
problem_url: "https://leetcode.cn/problems/flower-planting-with-no-adjacent/"
difficulty: "Medium"
rating: 1712
created: "2021-05-08T22:30:54+08:00"
updated: "2021-05-08T22:30:54+08:00"
upvotes: 0
comments: 0
---

# 1042. 不邻接植花

> **[yiduobo的每日leetcode 1042.不邻接植花](https://zhuanlan.zhihu.com/p/370784187) · 知乎 · 2021-05-08 · 赞同 0**
> 力扣：[1042. 不邻接植花](https://leetcode.cn/problems/flower-planting-with-no-adjacent/) · Medium · 灵茶山艾府：[两种写法：哈希表（数组）/位运算（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1042.不邻接植花

[力扣](https://leetcode-cn.com/problems/flower-planting-with-no-adjacent/)

由于题目给出的图中每个节点的度最多为3，那么对于任意节点而言，即使其相邻的三个节点都是不同的颜色，那么依然剩下一种颜色可以使用，因此实际上完全不需要什么复杂的策略，依次从每个未染色的节点开始进行dfs，将当前节点染上其相邻节点还未使用过的颜色即可。

最后附上python代码：

```python
class Solution(object):
    def gardenNoAdj(self, n, paths):
        """
        :type n: int
        :type paths: List[List[int]]
        :rtype: List[int]
        """

        g = {}
        for x, y in paths:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)

        color = [0] * (n + 1)
        candidate = [set([1, 2, 3, 4]) for _ in range(n + 1)]
        for x in range(1, n + 1):
            if color[x] == 0:
                self.dfs(x, color, candidate, g)
        
        return color[1:]
    
    def dfs(self, now, color, candidate, g):
        c = candidate[now].pop()
        color[now] = c
        if now in g:
            for next in g[now]:
                if color[next] == 0 and c in candidate[next]:
                    candidate[next].remove(c)
            for next in g[now]:
                if color[next] == 0:
                    self.dfs(next, color, candidate, g)
```
