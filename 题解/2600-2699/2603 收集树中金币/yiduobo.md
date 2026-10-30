---
title: "2603. 收集树中的金币"
aliases: ["yiduobo的每日leetcode 2603.收集树中的金币"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/topological-sort", "题单/链表-二叉树与回溯", "题单/图论算法", "题单/链表-二叉树与回溯/三-一般树", "题单/图论算法/二-拓扑排序"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/644679404"
zhihu_id: "644679404"
zhihu_title: "yiduobo的每日leetcode 2603.收集树中的金币"
question_id: "2603"
question: "收集树中金币"
problem_url: "https://leetcode.cn/problems/collect-coins-in-a-tree/"
difficulty: "Hard"
rating: 2712
created: "2023-07-20T03:50:11+08:00"
updated: "2023-07-20T03:50:11+08:00"
upvotes: 0
comments: 0
---

# 2603. 收集树中的金币

> **[yiduobo的每日leetcode 2603.收集树中的金币](https://zhuanlan.zhihu.com/p/644679404) · 知乎 · 2023-07-20 · 赞同 0**
> 力扣：[2603. 收集树中金币](https://leetcode.cn/problems/collect-coins-in-a-tree/) · Hard · 灵茶山艾府：[拓扑排序（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2603.收集树中的金币

[力扣](https://leetcode.cn/problems/collect-coins-in-a-tree/)

题目中的数据规模非常大，因此不能直接使用暴力算法。另一方面，由于收集金币有一个距离2以内都可以收集的条件，因此通过判断相邻点之间的关系来计算起点变换后需要经过的边数这个做法就非常复杂了，因为起点变化后到某些金币的距离可能会大于2或者跌落2。

另一种思路就是从边处理。

首先，对于没有金币的分叉，是完全没有必要访问的，因此可以先将所有没有金币的叶子节点，也就是度为1且没有金币的节点收集起来，然后从这些节点开始做拓扑排序，每次更新相邻节点的度，若某个节点的度变为了1且这个节点上也没有金币，那么就将其加入到拓扑排序的队列中。

拓扑排序完成后，队列中的所有节点就都是没有必要访问的节点。在具体实现中，并不需要删去这些节点，只需将这些节点标记一下就行了。

接下来，对于剩下的边，设其连接的节点为x和y，那么若x这一侧存在一个距离x大于等于2的金币节点，同时y这一侧也存在一个距离y大于等于2的金币节点，那么x到y这条边就是必须要经过的。这里有一个隐藏条件是题目给出的是一棵树，那么当其中某条边被去掉时，树将被分割成两个子树，而对于上面这种情况，两颗子树上都有金币，且由于金币到分割点的距离都大于等于2，因此就无法在一颗子树中收集到另一颗子树上的金币，即这条边是必须要经过的。

反过来，若某一侧距离最远金币的距离小于2，那么说明这一侧就是一个小分支，此时在这条边的另一侧通过收集距离2以内的金币，就可以将这一侧的金币收集起来了，此时这条边就无须经过。

根据上面的结论，此时就可以使用上面删除没有金币分叉相同的处理方法，从所有金币叶子节点开始，通过拓扑排序找到每个节点向外的分叉中距离最远的金币是多远，并将其记录在数组中。拓扑排序完成后，只需遍历所有的边，检测边两侧对应的f值是否都大于等于2，若满足，那么就将答案加上2，这里加上2的理由是题目要求来回。若不满足，那么则无需进行任何处理。

最后附上python代码：

```python
class Solution(object):
    def collectTheCoins(self, coins, edges):
        """
        :type coins: List[int]
        :type edges: List[List[int]]
        :rtype: int
        """

        n = len(coins)
        g = [[] for _ in range(n)]
        d = [0] * n
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)
            d[x] += 1
            d[y] += 1
        
        q = []
        vis = set()
        for index in range(n):
            if d[index] == 1 and coins[index] == 0:
                q.append(index)
                vis.add(index)
        
        head, tail = 0, len(q)
        while head < tail:
            now = q[head]
            head += 1
            for nxt in g[now]:
                d[nxt] -= 1
                if d[nxt] == 1 and coins[nxt] == 0:
                    q.append(nxt)
                    vis.add(nxt)
                    tail += 1
        
        q = []
        f = [0] * n
        for index in range(n):
            if d[index] == 1 and coins[index] == 1:
                q.append(index)
                f[index] = 0
                vis.add(index)
        
        head, tail = 0, len(q)
        while head < tail:
            now = q[head]
            head += 1
            for nxt in g[now]:
                d[nxt] -= 1
                if d[nxt] == 1 and nxt not in vis:
                    f[nxt] = f[now] + 1
                    q.append(nxt)
                    tail += 1
                    vis.add(nxt)
        
        res = 0
        for x, y in edges:
            if f[x] >= 2 and f[y] >= 2:
                res += 2
        
        return res
```
