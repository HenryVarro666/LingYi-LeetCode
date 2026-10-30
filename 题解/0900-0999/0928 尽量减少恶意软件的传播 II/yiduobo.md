---
title: "928. 尽量减少恶意软件的传播II"
aliases: ["yiduobo的每日leetcode 928.尽量减少恶意软件的传播II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/hash-table", "题单/图论算法", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/356851882"
zhihu_id: "356851882"
zhihu_title: "yiduobo的每日leetcode 928.尽量减少恶意软件的传播II"
question_id: "928"
question: "尽量减少恶意软件的传播 II"
problem_url: "https://leetcode.cn/problems/minimize-malware-spread-ii/"
difficulty: "Hard"
rating: 1985
created: "2021-03-13T16:35:29+08:00"
updated: "2021-03-13T16:35:29+08:00"
upvotes: 0
comments: 0
---

# 928. 尽量减少恶意软件的传播II

> **[yiduobo的每日leetcode 928.尽量减少恶意软件的传播II](https://zhuanlan.zhihu.com/p/356851882) · 知乎 · 2021-03-13 · 赞同 0**
> 力扣：[928. 尽量减少恶意软件的传播 II](https://leetcode.cn/problems/minimize-malware-spread-ii/) · Hard · 灵茶山艾府：[逆向思维（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

928.尽量减少恶意软件的传播II

[力扣](https://leetcode-cn.com/problems/minimize-malware-spread-ii/)

大背景与上一题类似

[yiduobo：yiduobo的每日leetcode 924.尽量减少恶意软件的传播](https://zhuanlan.zhihu.com/p/356456709)

但这一题的去除节点是直接断开该节点所有的边，那么一个自然的想法就是对于初始传播源中的每个节点，考察如果去除该节点，会有哪些节点不再受到感染。

反过来，我们可以从这些传播源开始进行dfs，看看这些节点将会感染到哪些节点。那么对于一个初始没有被感染的节点，若该节点会被两个或以上的传播源感染，那么无论怎么操作，该节点最终必然会被感染，于是我们应该将目标放在那些只会被一个传播源感染的节点。

对于这些节点，我们就可以统计是哪个传播源感染了最多的节点，就可以得到最终答案了。

最后附上python代码：

```python
class Solution(object):
    def minMalwareSpread(self, graph, initial):
        """
        :type graph: List[List[int]]
        :type initial: List[int]
        :rtype: int
        """

        n = len(graph)
        g = {}
        for i in range(n):
            g[i] = set()
            for j in range(n):
                if i != j and graph[i][j] == 1:
                    g[i].add(j)

        initial_set = set(initial)

        connect = [[] for _ in range(n)]

        for i in initial:
            self.dfs(i, i, g, initial_set, connect)

        connect_cnt = [0] * n
        for i in range(n):
            if len(connect[i]) == 1:
                connect_cnt[connect[i][0]] += 1
        
        res = None
        for i in range(n):
            if i in initial_set and (res is None or connect_cnt[i] > connect_cnt[res]):
                res = i
        
        return res

    def dfs(self, now, origin, g, initial_set, connect):
        for next in g[now]:
            if next not in initial_set and (len(connect[next]) == 0 or connect[next][-1] != origin):
                connect[next].append(origin)
                self.dfs(next, origin, g, initial_set, connect)
```
