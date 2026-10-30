---
title: "2065. 最大化一张图中的路径价值"
aliases: ["yiduobo的每日leetcode 2065.最大化一张图中的路径价值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/graph", "leetcode/backtracking", "leetcode/shortest-path", "leetcode/jian-zhi", "题单/图论算法", "题单/图论算法/九-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/514706906"
zhihu_id: "514706906"
zhihu_title: "yiduobo的每日leetcode 2065.最大化一张图中的路径价值"
question_id: "2065"
question: "最大化一张图中的路径价值"
problem_url: "https://leetcode.cn/problems/maximum-path-quality-of-a-graph/"
difficulty: "Hard"
rating: 2178
created: "2022-05-15T14:19:23+08:00"
updated: "2022-05-15T14:19:23+08:00"
upvotes: 0
comments: 0
---

# 2065. 最大化一张图中的路径价值

> **[yiduobo的每日leetcode 2065.最大化一张图中的路径价值](https://zhuanlan.zhihu.com/p/514706906) · 知乎 · 2022-05-15 · 赞同 0**
> 力扣：[2065. 最大化一张图中的路径价值](https://leetcode.cn/problems/maximum-path-quality-of-a-graph/) · Hard · 灵茶山艾府：[暴搜+最短路剪枝（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2065.最大化一张图中的路径价值

[力扣](https://leetcode.cn/problems/maximum-path-quality-of-a-graph/)

乍一看感觉没有什么好的做法，可能会用到桥和连通分量缩点之类的东西，感觉非常复杂。不过注意到题目中给出了一个条件，就是10 \<\= time[j], maxTime \<\= 100，也就是说从0出发走一圈再回到0，经过的边的条数最多为10条。另一方面，题目有保证了每个节点的度最多为4，那么完全可以从0开始执行dfs，最终可能出现的状态数最多只有4^10种，规模大概在一百万左右，是完全可以承受的。

具体实现上就是常规的dfs，不过在这里对于访问过的点可以再次访问，但不能将其对应的价值加入到当前的路径价值当中。

最后附上python代码：

```python
class Solution(object):
    def maximalPathQuality(self, values, edges, maxTime):
        """
        :type values: List[int]
        :type edges: List[List[int]]
        :type maxTime: int
        :rtype: int
        """

        g = {}

        for x, y, time in edges:
            if x not in g:
                g[x] = {}
            g[x][y] = time

            if y not in g:
                g[y] = {}
            g[y][x] = time

        self.res = 0
        used = set([0])

        def dfs(now, used, v, t):
            if now == 0:
                self.res = max(self.res, v)
            
            for next, time in g.get(now, {}).items():
                if time + t <= maxTime:
                    if next in used:
                        dfs(next, used, v, t + time)
                    else:
                        used.add(next)
                        dfs(next, used, v + values[next], t + time)
                        used.remove(next)

        dfs(0, used, values[0], 0)
        return self.res
```
