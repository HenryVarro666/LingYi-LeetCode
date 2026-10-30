---
title: "2858. 可以到达每一个节点的最少边反转次数"
aliases: ["yiduobo的每日leetcode 2858.可以到达每一个节点的最少边反转次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "题单/动态规划", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/661233896"
zhihu_id: "661233896"
zhihu_title: "yiduobo的每日leetcode 2858.可以到达每一个节点的最少边反转次数"
question_id: "2858"
question: "可以到达每一个节点的最少边反转次数"
problem_url: "https://leetcode.cn/problems/minimum-edge-reversals-so-every-node-is-reachable/"
difficulty: "Hard"
rating: 2295
created: "2023-10-14T04:20:55+08:00"
updated: "2023-10-14T04:20:55+08:00"
upvotes: 0
comments: 0
---

# 2858. 可以到达每一个节点的最少边反转次数

> **[yiduobo的每日leetcode 2858.可以到达每一个节点的最少边反转次数](https://zhuanlan.zhihu.com/p/661233896) · 知乎 · 2023-10-14 · 赞同 0**
> 力扣：[2858. 可以到达每一个节点的最少边反转次数](https://leetcode.cn/problems/minimum-edge-reversals-so-every-node-is-reachable/) · Hard · 灵茶山艾府：[【模板】换根 DP（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2858.可以到达每一个节点的最少边反转次数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-edge-reversals-so-every-node-is-reachable/)

计算单个节点到达其他所有节点所需的边反转次数并不困难，因为题目给出的是一棵树，因此从一个节点到另一个节点只有唯一的路径，也就是说对于路径上的反向边必须都执行反转操作而不能另外找路，因此对于这个只需一次bfs就能处理。

题目中节点数量的规模比较大，不能逐个遍历，因此必须想办法从之前的遍历结果中获取信息。

如果将两个相邻的节点x和y视为一个点，那么从这个点出发到其他节点所需的边反转次数是固定的，也就是说如果仅考虑x和y之外的节点，从x或y出发到达这些节点所需的反转数量是完全相同的。如果在这里已经知道了从x出发到其他节点所需的反转次数，那么只需在这个基础上额外考虑x-y这条边的走向就能计算出y出发到达其他节点所处的反转次数了。更具体的，若这条边是从x出发到y的边，那么从x出发时这条边无需反转，但是从y出发时这条边需要反转，因此res[y] \= res[x] + 1；反之，若这条边是从y出发到x的边，那么从x出发时这条边被反转了，但是从y出发时无需反转，因此res[y] \= res[x] - 1。

有了上面这个结论，就可以先通过一次bfs找出图中某个点到其他点所需的反转次数，然后再从这个点出发进行另一个bfs，通过上面这个相邻点答案的关系将答案一层一层扩展出去就行了。

最后附上python代码：

```python
class Solution(object):
    def minEdgeReversals(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: List[int]
        """

        g = {i : {} for i in range(n)}
        for x, y in edges:
            g[x][y] = 1
            g[y][x] = -1
        
        vis = set([0])
        q = [0]
        head, tail = 0, 1
        res = [0] * n
        while head < tail:
            now = q[head]
            head += 1
            for nxt in g[now]:
                if nxt not in vis:
                    vis.add(nxt)
                    q.append(nxt)
                    tail += 1
                    if g[now][nxt] == -1:
                        res[0] += 1
        
        vis = set([0])
        q = [0]
        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            for nxt in g[now]:
                if nxt not in vis:
                    vis.add(nxt)
                    q.append(nxt)
                    tail += 1
                    res[nxt] = res[now]
                    if g[now][nxt] == 1:
                        res[nxt] += 1
                    else:
                        res[nxt] -= 1
        
        return res
```
