---
title: "1857. 有向图中最大颜色值"
aliases: ["yiduobo的每日leetcode 1857.有向图中最大颜色值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/topological-sort", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/图论算法", "题单/动态规划/十三-图-DP", "题单/图论算法/二-拓扑排序"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/472622409"
zhihu_id: "472622409"
zhihu_title: "yiduobo的每日leetcode 1857.有向图中最大颜色值"
question_id: "1857"
question: "有向图中最大颜色值"
problem_url: "https://leetcode.cn/problems/largest-color-value-in-a-directed-graph/"
difficulty: "Hard"
rating: 2313
created: "2022-02-25T23:04:07+08:00"
updated: "2022-02-25T23:04:07+08:00"
upvotes: 0
comments: 0
---

# 1857. 有向图中最大颜色值

> **[yiduobo的每日leetcode 1857.有向图中最大颜色值](https://zhuanlan.zhihu.com/p/472622409) · 知乎 · 2022-02-25 · 赞同 0**
> 力扣：[1857. 有向图中最大颜色值](https://leetcode.cn/problems/largest-color-value-in-a-directed-graph/) · Hard · 灵茶山艾府：[两种方法：记忆化搜索 / 拓扑排序（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1857.有向图中最大颜色值

[力扣](https://leetcode-cn.com/problems/largest-color-value-in-a-directed-graph/)

对于这类有向图中找最长路径相关的问题，通常的做法就是拓扑排序加动态规划。即按照拓扑排序的顺序，按照图中边的方向进行节点的更新。

对于本题，令f[node][color]表示以node这个节点为路径终点时，路径上color这种颜色节点最多有多少个。那么对于f[node][color]而言，其应该等于max(f[prev][color])，其中prev是所有有边指向node的节点。另外，若node本身的颜色就是color，则还需要额外加上1。

那么在这里，依然是先遍历图中的边，建图并统计各个节点的入度。接下来将入度为0的节点选出来，因为这些节点没有任何前置节点，因此更新这部分节点的f\[node\]\[colors\[node\]\]为1，并将这些节点加入到拓扑排序的bfs队列中。

接下来开始bfs。对于当前节点now，枚举其所有可以到达的节点next。对于当前的next，首先枚举f[now]中所有的颜色color，并使用f[now][color]来更新f[next][color]。接下来将next的入度减1，若next的入度变成了0，说明next的所有前置节点已经全部被访问过，f[next]已经更新完毕了，那么就应该将next加入到队列中。另外，此时需要特别注意f[next]还需要加上next本身的颜色，在这里再加上本身颜色的理由是方便f[now][color]来更新f[next][color]，因为在next进入队列之前，f[next]是不会对其他节点产生任何影响的，因此可以将这个本身颜色的加1放到next即将加入队列，也就是f[next]已经被f[now]更新定型的时刻再执行。

拓扑排序结束后，若队列长度不等于节点的个数n，说明图中存在环，部分节点没能参与到拓扑排序中，此时直接返回-1，否则返回f中的最大值即可。

最后附上python代码：

```python
class Solution(object):
    def largestPathValue(self, colors, edges):
        """
        :type colors: str
        :type edges: List[List[int]]
        :rtype: int
        """

        n = len(colors)
        ind = [0] * n
        g = {index : set() for index in range(n)}
        for x, y in edges:
            g[x].add(y)
            ind[y] += 1
        
        f = {index : {} for index in range(n)}
        q = []
        for index in range(n):
            if ind[index] == 0:
                q.append(index)
                f[index][colors[index]] = 1

        l = 0
        r = len(q)
        res = 1
        while l < r:
            now = q[l]
            l += 1
            for next in g[now]:
                for color in f[now]:
                    cnt = f[now][color]
                    f[next][color] = max(f[next].get(color, 0), cnt)

                ind[next] -= 1
                if ind[next] == 0:
                    q.append(next)
                    r += 1
                    f[next][colors[next]] = f[next].get(colors[next], 0) + 1
                    res = max(res, max(f[next].values()))
        
        if len(q) != n:
            return -1
        
        return res
```
