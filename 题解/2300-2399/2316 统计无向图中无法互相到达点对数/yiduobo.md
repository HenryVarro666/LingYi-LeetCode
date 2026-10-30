---
title: "2316. 统计无向图中无法互相到达点对数"
aliases: ["yiduobo的每日leetcode 2316.统计无向图中无法互相到达点对数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/math", "题单/图论算法", "题单/数学算法", "题单/图论算法/一-图的遍历", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/556203902"
zhihu_id: "556203902"
zhihu_title: "yiduobo的每日leetcode 2316.统计无向图中无法互相到达点对数"
question_id: "2316"
question: "统计无向图中无法互相到达点对数"
problem_url: "https://leetcode.cn/problems/count-unreachable-pairs-of-nodes-in-an-undirected-graph/"
difficulty: "Medium"
rating: 1604
created: "2022-08-21T17:06:31+08:00"
updated: "2022-08-21T17:06:31+08:00"
upvotes: 2
comments: 0
---

# 2316. 统计无向图中无法互相到达点对数

> **[yiduobo的每日leetcode 2316.统计无向图中无法互相到达点对数](https://zhuanlan.zhihu.com/p/556203902) · 知乎 · 2022-08-21 · 赞同 2**
> 力扣：[2316. 统计无向图中无法互相到达点对数](https://leetcode.cn/problems/count-unreachable-pairs-of-nodes-in-an-undirected-graph/) · Medium · 灵茶山艾府：[DFS 求连通块大小（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2316.统计无向图中无法互相到达点对数

[力扣](https://leetcode.cn/problems/count-unreachable-pairs-of-nodes-in-an-undirected-graph/)

在无向图中，处于同一个连通块中的点都是可以互相到达的，而处于不同连通块中的点则不能互相到达。设图中有n个节点，那么就会产生n \* (n - 1) / 2组点对。题目需要计算无法互相到达的点对数，那么可以反过来思考，使用n \* (n - 1) / 2减去可以互相到达的点对数。

对于一个大小为k的连通块，其中的点对数目为k \* (k - 1) / 2，也就是说只需要找出所有连通块的大小就可以计算出最终答案了。于是可以使用经典的种子染色法找出图中每一个连通块的大小，然后通过上面的计算方式得出最终的答案。

最后附上python代码：

```python
class Solution(object):
    def countPairs(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: int
        """

        used = set()
        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            
            g[x].add(y)
            g[y].add(x)
        
        res = n * (n - 1) / 2
        for index in range(n):
            if index not in used:
                used.add(index)
                q = [index]
                l = 0
                r = 1
                while l < r:
                    now = q[l]
                    l += 1
                    for next in g.get(now, set()):
                        if next not in used:
                            q.append(next)
                            r += 1
                            used.add(next)
                
                res -= r * (r - 1) / 2
        
        return res
```
