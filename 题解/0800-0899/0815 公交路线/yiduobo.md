---
title: "815. 公交路线"
aliases: ["yiduobo的每日leetcode 815.公交路线"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/breadth-first-search", "leetcode/graph", "leetcode/queue", "题单/图论算法", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/343828108"
zhihu_id: "343828108"
zhihu_title: "yiduobo的每日leetcode 815.公交路线"
question_id: "815"
question: "公交路线"
problem_url: "https://leetcode.cn/problems/bus-routes/"
difficulty: "Hard"
rating: 1964
created: "2021-01-14T22:57:26+08:00"
updated: "2021-01-14T22:57:26+08:00"
upvotes: 0
comments: 0
---

# 815. 公交路线

> **[yiduobo的每日leetcode 815.公交路线](https://zhuanlan.zhihu.com/p/343828108) · 知乎 · 2021-01-14 · 赞同 0**
> 力扣：[815. 公交路线](https://leetcode.cn/problems/bus-routes/) · Hard · 灵茶山艾府：[【图解】BFS 线性做法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

815.公交路线

[力扣](https://leetcode-cn.com/problems/bus-routes/)

题目要求最少的换乘次数，那么很自然想到了bfs。对于当前处理的节点now，我们遍历还没有使用过的公交路线，对于这些公交路线上的所有车站，若该车站还没有加入到bfs队列中，则将其加入到队列中。若目标车站以及加入到了队列中，那么返回当前bfs的轮次。

若bfs自然结束，说明目标车站无法到达，那么返回-1。

最后附上python代码，其中unuse_route_set表示未使用过的公交路线，unreach_set表示未加入到队列中的车站，route_dict表示当前车站可以搭乘哪些公交路线：

```python
class Solution(object):
    def numBusesToDestination(self, routes, S, T):
        """
        :type routes: List[List[int]]
        :type S: int
        :type T: int
        :rtype: int
        """

        if S == T:
            return 0

        n = len(routes)
        unuse_route_set = set(range(n))
        unreach_set = set()
        route_dict = {}
        for index, route in enumerate(routes):
            for num in route:
                unreach_set.add(num)
                if num not in route_dict:
                    route_dict[num] = set()
                route_dict[num].add(index)
        
        unreach_set.add(T)
        unreach_set.remove(S)
        q = [S]
        l = 0
        r = 1
        res = 0
        while l < r:
            res += 1
            for index in range(l, r):
                now = q[index]
                if now not in route_dict:
                    continue
                for route in route_dict[now]:
                    if route not in unuse_route_set:
                        continue
                    unuse_route_set.remove(route)
                    for num in routes[route]:
                        if num == T:
                            return res
                        if num in unreach_set:
                            unreach_set.remove(num)
                            q.append(num)
            l, r = r, len(q)
        
        return -1
```
