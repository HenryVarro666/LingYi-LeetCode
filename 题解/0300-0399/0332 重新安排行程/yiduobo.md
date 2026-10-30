---
title: "332. 重新安排行程"
aliases: ["yiduobo的每日leetcode 332.重新安排行程"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/161665607"
zhihu_id: "161665607"
zhihu_title: "yiduobo的每日leetcode 332.重新安排行程"
question_id: "332"
question: "重新安排行程"
problem_url: "https://leetcode.cn/problems/reconstruct-itinerary/"
created: "2020-07-19T15:50:18+08:00"
updated: "2020-07-19T15:50:18+08:00"
upvotes: 0
comments: 0
---

# 332. 重新安排行程

> **[yiduobo的每日leetcode 332.重新安排行程](https://zhuanlan.zhihu.com/p/161665607) · 知乎 · 2020-07-19 · 赞同 0**
> 力扣：[332. 重新安排行程](https://leetcode.cn/problems/reconstruct-itinerary/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

332.重新安排行程<https://leetcode-cn.com/problems/reconstruct-itinerary/>

图论中经典的欧拉路径问题，题目在这里保证了存在解，且规定了起点，那么可能存在两种情况：

1、只能形成欧拉路径，那么此时除了起点与终点之外的其他节点入度等于出度，而起点的入度等于出度减一，终点的出度等于入度减一。

2、可以形成欧拉回路，那么此时所有节点的入度应该等于出度，此时的终点就是起点。

于是可以直接进行dfs，第一个开始回溯的点必然是路径的终点。如果将最后到达该点的入边删去的话，那么终点前一个点的出度会相应地减一，那么这里的前一个点可以看做是新的终点。那么我们就可以先dfs找到dfs序，然后从终点开始回溯。当回溯过程中某个点的出度已经消耗完，那么说明这个点是当前欧拉路径的终点，将其记录下来同时删去入度边。重复这个过程直到回溯至起点，且起点的出边被全部删去，那么此时记录下来的序列就是答案的反序。

需要注意的是，由于题目要求字典序最小，因此在dfs时需要先对边进行排序。

最后附上python代码：

```python
class Solution(object):
    def findItinerary(self, tickets):
        """
        :type tickets: List[List[str]]
        :rtype: List[str]
        """

        g = {}
        for x, y in tickets:
            if x not in g:
                g[x] = {}
            if y not in g:
                g[y] = {}
            g[x][y] = g[x].get(y, 0) + 1

        res = []
        self.dfs('JFK', g, res)
        res.reverse()
        return res

    def dfs(self, x, g, res):
        for y in sorted(g[x].keys()):
            if g[x].get(y, 0) > 0:
                g[x][y] -= 1
                self.dfs(y, g, res)
        res.append(x)
```
