---
title: "3244. 新增道路查询后的最短距离II"
aliases: ["yiduobo的每日leetcode 3244.新增道路查询后的最短距离II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/union-find", "leetcode/graph", "leetcode/array", "leetcode/shortest-path", "题单/常用数据结构", "题单/常用数据结构/七-并查集"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/721216875"
zhihu_id: "721216875"
zhihu_title: "yiduobo的每日leetcode 3244.新增道路查询后的最短距离II"
question_id: "3244"
question: "新增道路查询后的最短距离 II"
problem_url: "https://leetcode.cn/problems/shortest-distance-after-road-addition-queries-ii/"
difficulty: "Hard"
rating: 2270
created: "2024-09-20T23:55:47+08:00"
updated: "2024-09-20T23:55:47+08:00"
upvotes: 1
comments: 0
---

# 3244. 新增道路查询后的最短距离II

> **[yiduobo的每日leetcode 3244.新增道路查询后的最短距离II](https://zhuanlan.zhihu.com/p/721216875) · 知乎 · 2024-09-20 · 赞同 1**
> 力扣：[3244. 新增道路查询后的最短距离 II](https://leetcode.cn/problems/shortest-distance-after-road-addition-queries-ii/) · Hard · 灵茶山艾府：[两种方法：区间并查集 / 维护跳转位置（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3244.新增道路查询后的最短距离II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/shortest-distance-after-road-addition-queries-ii/description/)

上一题的修改版。本题中n以及queries的长度都可以到10^5，但是也新增了一个限制条件，对于任意一组queries[i]以及queries[j]，不满足queires[i][0] \< queries[j][0] \< queries[i][1] \< queries[j][1]。

由于数据规模的增大，之前的暴力算法不再使用，此时就需要从新增的这个条件入手，看看能否优化。

题目中新增的条件实际上表明的是两条新增路径之间要么互不相关，要么是完整的包含关系。对于互不相关的路径，自然是全部使用，而对于具有完整包含关系的路径，则应该使用最外层的路径。不妨设内层路径的起点和终点分别为(x1, y1)，外层路径的起点和终点分别为(x2, y2)，那么如果想要使用x1 -> y1的路径的话，因为没有路径与x2 -> y2相交，因此无论怎样操作，想要走到x1必须先走到x2，最好的情况也是x1和x2相同，否则就需要额外的操作先从x2走到x1；同样的道理，从y1向后继续走则必然会经过y2，最好的情况就是y1和y2相同，否则就需要额外的操作从y1走到y2。相比之下，直接从x2走到y2显然是更优的选择。

根据上面的结论，就应该尽量使用外层的路径。在这里可以使用一个数组nxt记录当前节点在最优情况下的下一个节点是什么。在初始状态下，nxt[i]就等于i + 1。当决定使用一条x->y的路径后，就应该将nxt[x]修改为y。另一方面，当某些路径被使用后，中间有部分中继节点将被跳过，同时这些节点后续也不会再用到，因此还需要使用一个集合removed记录哪些节点将被跳过。

在未添加任何道路时，一开始从0走到n - 1的最短路径长度就是n - 1，先将其记录下来。接下来遍历queries，对于queries[i] \= [x, y]，若此时x或y已经在removed中，说明当前路径一定是某条内层路径，无需考虑，此时的最短路径长度就是上一轮的最短路径长度。反之，则需要将x->y的路径添加进来，这种情况下就应该从x出发，沿着nxt[x]一路走到y，期间走过的中继节点都应该被跳过，每跳过一个节点最短路径的长度就应该减1，同时应该将这个节点加入到removed中，然后再将nxt[x]更新为y即可。

最后附上python代码：

```python
class Solution(object):
    def shortestDistanceAfterQueries(self, n, queries):
        """
        :type n: int
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        nxt = []
        for index in range(1, n):
            nxt.append(index)
        nxt.append(None)

        removed = set()
        res = [n - 1]

        for x, y in queries:
            res.append(res[-1])
            if x in removed or y in removed:
                continue
            
            now = x
            while nxt[now] < y:
                now = nxt[now]
                res[-1] -= 1
                removed.add(now)
            nxt[x] = y
        
        return res[1:]
```
