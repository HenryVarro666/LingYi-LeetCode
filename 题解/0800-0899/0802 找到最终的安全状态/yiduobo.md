---
title: "802. 找到最终的安全状态"
aliases: ["yiduobo的每日leetcode 802.找到最终的安全状态"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/342954179"
zhihu_id: "342954179"
zhihu_title: "yiduobo的每日leetcode 802.找到最终的安全状态"
question_id: "802"
question: "找到最终的安全状态"
problem_url: "https://leetcode.cn/problems/find-eventual-safe-states/"
created: "2021-01-08T23:54:42+08:00"
updated: "2021-01-08T23:54:42+08:00"
upvotes: 1
comments: 0
---

# 802. 找到最终的安全状态

> **[yiduobo的每日leetcode 802.找到最终的安全状态](https://zhuanlan.zhihu.com/p/342954179) · 知乎 · 2021-01-08 · 赞同 1**
> 力扣：[802. 找到最终的安全状态](https://leetcode.cn/problems/find-eventual-safe-states/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

802.找到最终的安全状态

[力扣](https://leetcode-cn.com/problems/find-eventual-safe-states/)

题目给出一张有向图，要求找出图中所有不在环上的点。对于有向图中找环的问题，一个经典的做法是拓扑排序。对于一个节点而言，若该节点的出度为0，或者以该节点为起点的所有边对应的终点要么出度为0，要么也满足这个性质，那么这个节点就不是环上的。

有了这个结论，就可以将图的边全部反向之后执行拓扑排序，此时由于边全部反向，因此每个点的入度与出度互换，那么前面所说的出度为0反向之后恰好是拓扑排序的起始条件，而另一个条件也恰好满足拓扑排序扩展bfs的条件。

执行完拓扑排序之后，队列中的所有点即为题目答案。

最后附上python代码：

```python
class Solution(object):
    def eventualSafeNodes(self, graph):
        """
        :type graph: List[List[int]]
        :rtype: List[int]
        """

        n = len(graph)
        oud = [0] * n
        g = {}
        for x, next_list in enumerate(graph):
            for y in next_list:
                if y not in g:
                    g[y] = set()
                g[y].add(x)
                oud[x] += 1
        
        q = []
        for x in range(n):
            if oud[x] == 0:
                q.append(x)
        
        l = 0
        r = len(q)
        while l < r:
            now = q[l]
            l += 1
            for prev in g.get(now, set()):
                oud[prev] -= 1
                if oud[prev] == 0:
                    q.append(prev)
                    r += 1
        
        res = []
        for x in range(n):
            if oud[x] == 0:
                res.append(x)
    
        return res
```
