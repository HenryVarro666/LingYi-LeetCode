---
title: "LCP 04. 覆盖"
aliases: ["yiduobo的每日leetcode LCP04.覆盖"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/570268884"
zhihu_id: "570268884"
zhihu_title: "yiduobo的每日leetcode LCP04.覆盖"
question_id: "LCP 04"
question: "覆盖"
problem_url: "https://leetcode.cn/problems/broken-board-dominoes/"
created: "2022-10-03T04:46:03+08:00"
updated: "2022-10-03T04:46:03+08:00"
upvotes: 0
comments: 0
---

# LCP 04. 覆盖

> **[yiduobo的每日leetcode LCP04.覆盖](https://zhuanlan.zhihu.com/p/570268884) · 知乎 · 2022-10-03 · 赞同 0**
> 力扣：[LCP 04. 覆盖](https://leetcode.cn/problems/broken-board-dominoes/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP04.覆盖

[力扣](https://leetcode.cn/problems/broken-board-dominoes/)

看题目的数据规模应该可以使用状态压缩动态规划来做，即f[i][state]表示前i行，最后两行的覆盖状态为state时可以使用的最多骨牌数是多少。接下来就是f[i][state]开始dfs来更新所有的f[i + 1][next_state]。

不过对于本题，更好的做法是使用匹配或者网络流算法。对于棋盘类的问题，一种常见的建模方式是参考国际象棋的棋盘，如下图所示

![](../../_assets/yiduobo/v2-e06393fcadd76f34f3bf3f30a7bf96d8_r.jpg)

可以发现，相邻格子间的颜色都互不相同。如果将棋盘上的格子视为图中的点，在所有相邻格子间都连上一条边，那么最终得到的图中的所有边连接的点都是一黑一白的，这种图有一个专门名称，即二分图。

回到问题本身。题目中的棋盘上有部分破损的格子，那么这些格子就不能参与建图，而对于由其他格子得到的图而言，一块骨牌实际上就相当于图中的一条边，那么现在的问题就变成了如何从图中选择尽量多的边，且这些边不能连接到同一个节点。这是一个经典的二分图最大匹配问题，最常规的算法是匈牙利算法，当然也可以转化成网络流问题，使用最大流来进行求解。

我在这里使用的是网络流，同时由于图中边的容量都是1，因此可以直接bfs来找增广路径。

网络流相关的内容有兴趣的同学可以自行找一些资料，这里就不展开了。

最后附上python代码：

```python
class Solution(object):
    def domino(self, n, m, broken):
        """
        :type n: int
        :type m: int
        :type broken: List[List[int]]
        :rtype: int
        """

        broken_set = set()
        for x, y in broken:
            broken_set.add(x * m + y + 1)
        s = 0
        t = m * n + 1
        c = [[0] * (t + 1) for _ in range(t + 1)]
        
        for i in range(n):
            for j in range(m):
                now = i * m + j + 1
                if now in broken_set:
                    continue
                if (i + j) % 2 == 0:
                    c[s][now] = 1
                    if j < m - 1 and now + 1 not in broken_set:
                        c[now][now + 1] = 1
                    if i < n - 1 and now + m not in broken_set:
                        c[now][now + m] = 1
                else:
                    c[now][t] = 1
                    if j < m - 1 and now + 1 not in broken_set:
                        c[now + 1][now] = 1
                    if i < n - 1 and now + m not in broken_set:
                        c[now + m][now] = 1

        res = 0
        while True:
            pre = [None] * (m * n + 2)
            pre[s] = -1
            head = 0
            tail = 1
            q = [s]
            while head < tail:
                now = q[head]
                head += 1
                for next in range(m * n + 2):
                    if c[now][next] > 0 and pre[next] is None:
                        pre[next] = now
                        q.append(next)
                        tail += 1
            
            if pre[t] is None:
                break
            
            res += 1
            now = t
            while now != s:
                last = pre[now]
                c[last][now] -= 1
                c[now][last] += 1
                now = last
        
        return res
```
