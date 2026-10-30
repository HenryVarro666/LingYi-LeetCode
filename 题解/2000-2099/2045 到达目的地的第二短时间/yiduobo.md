---
title: "2045. 到达目的地的第二短时间"
aliases: ["yiduobo的每日leetcode 2045.到达目的地的第二短时间"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/breadth-first-search", "leetcode/graph", "leetcode/shortest-path", "leetcode/bfs", "题单/图论算法", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/510875996"
zhihu_id: "510875996"
zhihu_title: "yiduobo的每日leetcode 2045.到达目的地的第二短时间"
question_id: "2045"
question: "到达目的地的第二短时间"
problem_url: "https://leetcode.cn/problems/second-minimum-time-to-reach-destination/"
difficulty: "Hard"
rating: 2202
created: "2022-05-07T20:09:52+08:00"
updated: "2022-05-07T20:09:53+08:00"
upvotes: 1
comments: 0
---

# 2045. 到达目的地的第二短时间

> **[yiduobo的每日leetcode 2045.到达目的地的第二短时间](https://zhuanlan.zhihu.com/p/510875996) · 知乎 · 2022-05-07 · 赞同 1**
> 力扣：[2045. 到达目的地的第二短时间](https://leetcode.cn/problems/second-minimum-time-to-reach-destination/) · Hard · 灵茶山艾府：[BFS 求次短路，附详细注释](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2045.到达目的地的第二短时间

[力扣](https://leetcode-cn.com/problems/second-minimum-time-to-reach-destination/)

题目引入了一套红绿灯系统，乍一看会对最终答案的求解产生一些影响，但是由于题目中所有的红绿灯都是同一时刻变色，且题目的边权都一样，那么对于图中的两点u和v，若满足dis[u] \<\= dis[v]，那么即使按最短路径到达u因为等红灯耽误了，从u的出发的时间也不会比从v出发的时间更晚。又由于图中边权都一样，因此继续从u开始执行bfs得到的依然还是最短的路径。

有了这个结论，就可以先暂时抛开time和change的影响，将原图视为一个边权为1的无向图，最终目的是从图中找出从1到n的次短路。

对于次短路问题，有一些经典算法，部分算法甚至可以一直推广到k短路问题，但是相对都比较复杂，在这里还是使用bfs来得最方便。

在求解最短路时，常规的bfs在访问过某个点p之后就不再访问p，而对于次短路问题，则可以给每个点两次机会。注意到题目中要求耗时严格大于最短耗时，因此在bfs过程中，若某个节点之前被访问过，且当前这次的时间比之前得到的最短耗时要长，就说明当前时间就是到达该点的第二短时间。此时需要再次将该点加入到bfs队列中，同时设置该点之后不能再次访问。

按照上面的方法求出理论上最短的时间后，还需要根据红绿灯计算到达n的时间时间。由于在图中的行动是按一个time为周期的，每经过一个time就说明走到了某个新的节点，因此可以从0开始逐个累加time。

设当前累加结果的耗时中包含了k个change，当k为奇数时就表示需要等红灯了。红灯变绿的时间为(k + 1) \* change，所以应该将累加的时间更新为(k + 1) \* change，再进行后续累加。

最后附上python代码：

```python
class Solution(object):
    def secondMinimum(self, n, edges, time, change):
        """
        :type n: int
        :type edges: List[List[int]]
        :type time: int
        :type change: int
        :rtype: int
        """

        g = {x : set() for x in range(n)}
        for x, y in edges:
            x -= 1
            y -= 1
            g[x].add(y)
            g[y].add(x)

        first = [None] * n
        second = [None] * n
        first[0] = 0
        q = [(0, 0)]
        l = 0
        r = 1
        while l < r:
            now, t = q[l]
            l += 1
            for next in g[now]:
                next_t = t + 1
                if first[next] is None:
                    first[next] = next_t
                    q.append((next, next_t))
                    r += 1
                elif second[next] is None and first[next] < next_t:
                    second[next] = next_t
                    q.append((next, next_t))
                    r += 1
        
        res = 0
        for index in range(second[-1]):
            if (res / change) % 2 == 1:
                res = (res / change + 1) * change
            res += time

        return res
```
