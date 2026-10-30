---
title: "2492. 两个城市间路径的最小分数"
aliases: ["yiduobo的每日leetcode 2492.两个城市间路径的最小分数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/graph", "leetcode/recursion", "题单/图论算法", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/590393614"
zhihu_id: "590393614"
zhihu_title: "yiduobo的每日leetcode 2492.两个城市间路径的最小分数"
question_id: "2492"
question: "两个城市间路径的最小分数"
problem_url: "https://leetcode.cn/problems/minimum-score-of-a-path-between-two-cities/"
difficulty: "Medium"
rating: 1680
created: "2022-12-08T23:29:06+08:00"
updated: "2022-12-08T23:29:06+08:00"
upvotes: 0
comments: 0
---

# 2492. 两个城市间路径的最小分数

> **[yiduobo的每日leetcode 2492.两个城市间路径的最小分数](https://zhuanlan.zhihu.com/p/590393614) · 知乎 · 2022-12-08 · 赞同 0**
> 力扣：[2492. 两个城市间路径的最小分数](https://leetcode.cn/problems/minimum-score-of-a-path-between-two-cities/) · Medium · 灵茶山艾府：[阅读理解题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2492.两个城市间路径的最小分数

[力扣](https://leetcode.cn/problems/minimum-score-of-a-path-between-two-cities/)

题目中的路径可以经过某条边多次，这也就意味着两个城市间的路径实际上包含了其所在连通块中的所有边，那么在这里只需要遍历所有的边，使用并查集求出图中所有的连通块，并在求解过程中记录每个连通块中值最小的边。求解完成后，1所在连通块中最小边的值即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minScore(self, n, roads):
        """
        :type n: int
        :type roads: List[List[int]]
        :rtype: int
        """

        fa = range(n + 1)
        score = {}

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        for x, y, v in roads:
            fa_x = find(x)
            fa_y = find(y)
            if fa_x != fa_y:
                fa[fa_x] = fa_y
                if fa_x in score:
                    v = min(v, score[fa_x])
            if fa_y in score:
                v = min(v, score[fa_y])
            score[fa_y] = v
        
        return score[find(1)]
```
