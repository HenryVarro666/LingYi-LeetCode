---
title: "2608. 图中的最短环"
aliases: ["yiduobo的每日leetcode 2608.图中的最短环"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bfs", "leetcode/tu-jie", "题单/图论算法", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/645299870"
zhihu_id: "645299870"
zhihu_title: "yiduobo的每日leetcode 2608.图中的最短环"
question_id: "2608"
question: "图中的最短环"
problem_url: "https://leetcode.cn/problems/shortest-cycle-in-a-graph/"
difficulty: "Hard"
rating: 1904
created: "2023-07-23T01:15:57+08:00"
updated: "2023-07-23T01:15:57+08:00"
upvotes: 0
comments: 0
---

# 2608. 图中的最短环

> **[yiduobo的每日leetcode 2608.图中的最短环](https://zhuanlan.zhihu.com/p/645299870) · 知乎 · 2023-07-23 · 赞同 0**
> 力扣：[2608. 图中的最短环](https://leetcode.cn/problems/shortest-cycle-in-a-graph/) · Hard · 灵茶山艾府：[【一图秒懂】枚举起点跑 BFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2608.图中的最短环

[力扣](https://leetcode.cn/problems/shortest-cycle-in-a-graph/)

题目给出一张无向图，要求找出其中最小的环。如果是有向图应该是比较好处理的，而对于无向图反倒是没什么比较好的处理办法，不过好在本题的数据规模比较小，可以枚举每一条边，计算包含这条边的最短的环的长度。

对于一条连接节点x和节点y的边，可以先将其从图中删去，然后从x出发，通过bfs寻找到达y的最短路。若最短路存在，那么这个最短路，再加上之前删去的这条边，就构成了一个包含这条边且长度最短的环。于是只需对每条边找出对应的最小环，那么整个图中的最小环就是其中长度最短的那一个。

最后附上python代码：

```python
class Solution(object):
    def findShortestCycle(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: int
        """

        g = {x : set() for x in range(n)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)

        res = 1001
        for x, y in edges:
            g[x].remove(y)
            g[y].remove(x)

            q = [x]
            d = {}
            d[x] = 0
            head, tail = 0, 1
            while head < tail:
                for now in q[head : tail]:
                    for nxt in g[now]:
                        if nxt not in d:
                            d[nxt] = d[now] + 1
                            q.append(nxt)
                
                head, tail = tail, len(q)
                if y in d:
                    res = min(res, d[y] + 1)
                    break

            g[x].add(y)
            g[y].add(x)
        
        if res == 1001:
            res = -1
        return res
```
