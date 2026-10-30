---
title: "1466. 重新规划路线"
aliases: ["yiduobo的每日leetcode 1466.重新规划路线"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/413704174"
zhihu_id: "413704174"
zhihu_title: "yiduobo的每日leetcode 1466.重新规划路线"
question_id: "1466"
question: "重新规划路线"
problem_url: "https://leetcode.cn/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero/"
created: "2021-09-24T23:55:57+08:00"
updated: "2021-09-24T23:55:57+08:00"
upvotes: 0
comments: 0
---

# 1466. 重新规划路线

> **[yiduobo的每日leetcode 1466.重新规划路线](https://zhuanlan.zhihu.com/p/413704174) · 知乎 · 2021-09-24 · 赞同 0**
> 力扣：[1466. 重新规划路线](https://leetcode.cn/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1466.重新规划路线

[力扣](https://leetcode-cn.com/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero/)

由于题目保证了地图是一棵树，那么如果先不考虑图中边的方向，是一定可以从0号城市出发访问到图中其他城市的，于是可以从0号城市开始进行bfs，只需将bfs过程中的正向边反过来就能保证可以从各个城市都可以访问到0号城市了。

具体实现上，可以先重新建图，将图中的单向边变为无向边，但需要记录下这条边的原始方向。接下来从0号城市开始进行bfs，对于当前的位置now，枚举与其相连且没有被访问过的城市next。若now到next是原始图中的边，那么需要将其反向，此时将答案加上1。

最后附上python代码：

```python
class Solution(object):
    def minReorder(self, n, connections):
        """
        :type n: int
        :type connections: List[List[int]]
        :rtype: int
        """

        g = {}
        for x, y in connections:
            if x not in g:
                g[x] = {}
            if y not in g:
                g[y] = {}
            g[x][y] = 1
            g[y][x] = 0
        
        q = [0]
        l = 0
        r = 1
        used = [False] * n
        used[0] = True
        res = 0
        while l < r:
            now = q[l]
            l += 1
            for next in g[now]:
                if not used[next]:
                    res += g[now][next]
                    q.append(next)
                    used[next] = True
                    r += 1
        
        return res
```
