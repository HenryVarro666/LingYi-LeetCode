---
title: "4004. 使循环数组余额非负的最少移动次数II"
aliases: ["yiduobo的每日leetcode 4004.使循环数组余额非负的最少移动次数II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2067738267898884652"
zhihu_id: "2067738267898884652"
zhihu_title: "yiduobo的每日leetcode 4004.使循环数组余额非负的最少移动次数II"
question_id: "4004"
question: "使循环数组余额非负的最少移动次数II"
problem_url: "https://leetcode.cn/problems/minimum-moves-to-balance-circular-array-ii/"
created: "2026-08-03T22:42:44+08:00"
updated: "2026-08-03T22:42:48+08:00"
upvotes: 0
comments: 0
---

# 4004. 使循环数组余额非负的最少移动次数II

> **[yiduobo的每日leetcode 4004.使循环数组余额非负的最少移动次数II](https://zhuanlan.zhihu.com/p/2067738267898884652) · 知乎 · 2026-08-03 · 赞同 0**
> 力扣：[4004. 使循环数组余额非负的最少移动次数II](https://leetcode.cn/problems/minimum-moves-to-balance-circular-array-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4004.使循环数组余额非负的最少移动次数II

<https://leetcode.cn/problems/minimum-moves-to-balance-circular-array-ii/description/>

题目给出一个长度为n的环形数组balance，其中balance[index]是第index个人的净余额。

在一次移动中，一个人可以将正好1单位的余额转移给左边或者右边的邻居。

问至少需要多少次移动才能使得所有人的余额都非负。若无法实现，则返回-1。

相比与之前的3776，本题中余额为负数的人可能不止一个，难度也完全不是一个层级了。

首先，贪心法在这里没法再用了，因为无法简单判断负数余额的人应当接受那些正数余额的人的帮助。另一方面，由于这个转移的数值不定，而这个取值范围也极大，因此也无法通过保留接受帮助的额度的方式来使用动态规划。

不过换一种角度来看，最终达成目标的方式一定是正余额的人给负余额的人提供足量的帮助，因此在这里可以视为一个标准的二分图，两侧分别是正数的下标以及负数的下标。接下来，期间转移的额度之和显然应该恰好等于负数余额之和的绝对值，太少了不够，太多了又浪费了。

基于这个视角，使用费用流是顺理成章的事情：

- 将数组中每个下标视为图中的一个节点，然后额外添加源和汇
- 从源发出边到正余额表示的节点，容量为对应的余额，费用为0
- 从负余额表示的节点向汇发出变，容量为对应余额的绝对值，费用同样为0
- 从正余额的节点向所有负余额的节点发出边，容量为正余额节点对应的余额，费用为节点在原数组中下标的距离，这里的距离需要取环形两侧距离中的较小值

最后，执行费用流就行了。

不过在具体实现上，我才用的是常规的spfa最短路的费用流，第一次提交超时了。分析可以发现，这种建图方式边的规模是O(n^2)的，不过图比较扁平，不确定使用zkw费用流能否通过。

我采用的是另一种方案，就是不直接在正负余额之间连边，而是在下标相邻之间的节点连边，此时边的容量需要为总容量，理由是此时的节点可能作为其他节点的中转，因此边的容量需要放大最大，而费用则为1，因为是相邻移动。基于这种建图，边的规模就是O(n)的，此时直接使用基于spfa最短路的费用流就可以通过了。需要注意，由于连边时需要构建正反边，因此相邻节点间会出现重边，此时需要使用前向星存图而不是邻接表或者邻接矩阵。

不过话又说回来，基于题目给出的数据规模，使用网络流感觉时间复杂度应该是不够的，应该有各种方法构造数据hack掉。

最后附上python代码：

```python
class Solution(object):
    def minMoves(self, balance):
        """
        :type balance: List[int]
        :rtype: int
        """
        
        if sum(balance) < 0:
            return -1
        
        if min(balance) >= 0:
            return 0
        
        n = len(balance)
        s = n
        t = s + 1
        pre = []
        last = [None] * (n + 2)
        edges = []

        def add_edge(x, y, c, cost, pre, last, edges):
            m = len(edges)
            edges.append([y, c, cost])
            pre.append(last[x])
            last[x] = m

            m += 1
            edges.append([x, 0, -cost])
            pre.append(last[y])
            last[y] = m

        tot = 0
        for index, v in enumerate(balance):
            if v > 0:
                add_edge(s, index, v, 0, pre, last, edges)
            elif v < 0:
                add_edge(index, t, -v, 0, pre, last, edges)
                tot -= v

        for index in range(n):
            left = index - 1
            if left < 0:
                left += n
            add_edge(index, left, tot, 1, pre, last, edges)

            right = index + 1
            if right == n:
                right = 0
            add_edge(index, right, tot, 1, pre, last, edges)

        res = 0
        while True:
            dis = [None] * (t + 1)
            edge_idx = [None] * (t + 1)
            used = [False] * (n + 2)
            used[s] = True            
            q = [s]
            head, tail = 0, 1
            dis[s] = 0
            while head < tail:
                now = q[head]
                head += 1
                used[now] = False
                
                index = last[now]
                while index is not None:
                    nxt, c, cost = edges[index]
                    if c > 0 and (dis[nxt] is None or dis[nxt] > dis[now] + cost):
                        dis[nxt] = dis[now] + cost
                        edge_idx[nxt] = index
                        if not used[nxt]:
                            q.append(nxt)
                            tail += 1
                            used[nxt] = True
                    
                    index = pre[index]

            if dis[t] is None:
                return res

            now = t
            flow = tot
            while now != s:
                index = edge_idx[now]
                flow = min(flow, edges[index][1])
                now = edges[index ^ 1][0]

            res += flow * dis[t]
            now = t
            while now != s:
                index = edge_idx[now]
                edges[index][1] -= flow
                edges[index ^ 1][1] += flow
                now = edges[index ^ 1][0]
```
