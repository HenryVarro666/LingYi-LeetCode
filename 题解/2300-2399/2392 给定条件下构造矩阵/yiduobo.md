---
title: "2392. 给定条件下构造矩阵"
aliases: ["yiduobo的每日leetcode 2392.给定条件下构造矩阵"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/breadth-first-search", "leetcode/graph", "leetcode/topological-sort", "leetcode/queue", "leetcode/bfs", "leetcode/you-xiang-tu", "leetcode/gou-zao", "题单/图论算法", "题单/图论算法/二-拓扑排序"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/566151601"
zhihu_id: "566151601"
zhihu_title: "yiduobo的每日leetcode 2392.给定条件下构造矩阵"
question_id: "2392"
question: "给定条件下构造矩阵"
problem_url: "https://leetcode.cn/problems/build-a-matrix-with-conditions/"
difficulty: "Hard"
rating: 1961
created: "2022-09-20T02:24:03+08:00"
updated: "2022-09-20T02:24:03+08:00"
upvotes: 0
comments: 0
---

# 2392. 给定条件下构造矩阵

> **[yiduobo的每日leetcode 2392.给定条件下构造矩阵](https://zhuanlan.zhihu.com/p/566151601) · 知乎 · 2022-09-20 · 赞同 0**
> 力扣：[2392. 给定条件下构造矩阵](https://leetcode.cn/problems/build-a-matrix-with-conditions/) · Hard · 灵茶山艾府：[拓扑排序 + 构造（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2392.给定条件下构造矩阵

[力扣](https://leetcode.cn/problems/build-a-matrix-with-conditions/)

首先，注意到题目中的行和列是互补影响的，那么可以将行和列分开来考虑。

在这里不妨先考虑行。题目给出了一系列的上下关系(above, below)，要求above所在的行在below所在的行的的上面。对于这种有多重依赖关系，要求给出某种符合一来关系的序列的问题，通常的做法就是拓扑排序。在这里可以将每个数视为图中的一个节点，而对于一组上下关系(above, below)，则可以视为从above想below发出一条有向边。接下来在这个图中进行拓扑排序，得到的拓扑序对应的就是最终答案中每个数所在的行了。这样做可行的原因是对于任意一组上下关系，above的拓扑序必然是小于below的拓扑序的，因此above所在的行就必然在below所在行的上方，符合题目要求。

对于列也可以如法炮制，将每一组左右关系(left, right)视为从left向right发出的有向边，然后同样是执行拓扑排序确定每个数对应的列。

需要注意的是，如果行或者列进行拓扑排序后，bfs的队列长度不足k，说明对应的有向图中出现了环，也就是说无法构造出符合题目要求的矩阵，此时直接返回空矩阵即可。

最后附上python代码：

```python
class Solution(object):
    def buildMatrix(self, k, rowConditions, colConditions):
        """
        :type k: int
        :type rowConditions: List[List[int]]
        :type colConditions: List[List[int]]
        :rtype: List[List[int]]
        """

        def get_order(edges):
            g = {num : set() for num in range(1, k + 1)}
            ind = [0] * (k + 1)

            for x, y in edges:
                if y not in g[x]:
                    g[x].add(y)
                    ind[y] += 1
            
            q = []
            for num in range(1, k + 1):
                if ind[num] == 0:
                    q.append(num)
            
            l, r = 0, len(q)
            while l < r:
                now = q[l]
                l += 1
                for next in g[now]:
                    ind[next] -= 1
                    if ind[next] == 0:
                        q.append(next)
                        r += 1

            if len(q) < k:
                return []

            res = [0] * (k + 1)
            for index in range(k):
                res[q[index]] = index
            
            return res
        
        x = get_order(rowConditions)
        y = get_order(colConditions)

        if len(x) < k or len(y) < k:
            return []

        res = [[0] * k for _ in range(k)]
        for num in range(1, k + 1):
            res[x[num]][y[num]] = num
        
        return res
```
