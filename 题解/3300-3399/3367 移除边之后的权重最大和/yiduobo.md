---
title: "3367. 移除边之后的权重最大和"
aliases: ["yiduobo的每日leetcode 3367.移除边之后的权重最大和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/tree", "leetcode/depth-first-search", "leetcode/dynamic-programming", "leetcode/sorting", "题单/动态规划", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/27993899299"
zhihu_id: "27993899299"
zhihu_title: "yiduobo的每日leetcode 3367.移除边之后的权重最大和"
question_id: "3367"
question: "移除边之后的权重最大和"
problem_url: "https://leetcode.cn/problems/maximize-sum-of-weights-after-edge-removals/"
difficulty: "Hard"
rating: 2602
created: "2025-03-05T00:34:48+08:00"
updated: "2025-03-05T00:34:48+08:00"
upvotes: 0
comments: 0
---

# 3367. 移除边之后的权重最大和

> **[yiduobo的每日leetcode 3367.移除边之后的权重最大和](https://zhuanlan.zhihu.com/p/27993899299) · 知乎 · 2025-03-05 · 赞同 0**
> 力扣：[3367. 移除边之后的权重最大和](https://leetcode.cn/problems/maximize-sum-of-weights-after-edge-removals/) · Hard · 灵茶山艾府：[树形 DP + 贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3367.移除边之后的权重最大和

[3367. 移除边之后的权重最大和 - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-sum-of-weights-after-edge-removals/description/)

题目给出一颗具有n个节点，且编号为0到n - 1的无向树。另外给出一个长度为n - 1的数组edges，其中edges\[i\] \= \[u\[i\], v\[i\], w\[i\]\]表示u\[i\]到v\[i\]之间边的权重为w\[i\]。

现在要求从树中移除若干条边，使得每个节点至多与k个其他节点直接相连，这里的k是给定的整数。

问在执行完移除操作后，剩下边权的最大和是多少。

对于树中的某个节点now，其与父亲节点之间有一条边，与每个孩子节点各有一条边。由于题目中至多与有k个其他节点直接相连这一条件，那么在这里就可以令f[now]表示选取now与孩子节点中至多k - 1条边时，以now为根节点的子树中剩下边权的最大和。另一方面，令g[now]表示选择now与孩子节点中至多k条边时，以now为根节点的子树中剩下边权的最大和。

这样设计的理由是对于now的父亲节点，如果想要选择与now相连的边，就可以利用f[now]来更新答案；而如果不想要，则可以通过h[now]来更新答案。

---

具体来说，对于节点now，遍历其所有的孩子节点child。先递归计算f[child]以及h[child]，接下来若f[child]与now与child之间边权weight之和大于h[child]，即f[child] + weight > h[child]时，就可以尝试保留weight这条边。这样做的理由是若f[child] + weight \<\= h[child]，那么就没有理由保留weight这条边了，因为此时选择不保留的话不仅边权之和更高，同时还为now节省了一条边的份额。

记保留的收益diff \= f[child] + weight - h[child]，那么在这里就应该选取其中diff最大的k条边。这是一个经典的top k问题，那么在这里就可以使用一个大小为k的堆，用来记录最大的k个diff，表示选择收益最大的k条边。每次选择一条边时，先将diff累加到额外收益和s中，然后将diff加入到堆中。若堆的大小超过了k，那么就需要去掉之前选择的一条边，也就是让s减去堆顶元素。

无论是否选择当前的变，都应该将当前的h[child]累加到f[now]以及h[now]中。

遍历完所以孩子节点后，就可以将s累加到f[now]以及h[now]中。这些diff之和补充进去就相当于将本来是通过h[child]累加得到的f[now]和h[now]，修正成由一部分h[child]，与另一部分f[child]以及child对应的边权weight累加得到的f[now]和h[now]。若此时堆的大小等于k，还需从f[now]中减去堆顶元素，因为f的定义是只能选k - 1条边，所以还需要从中去掉一条已经选择的边。

从节点0开始向下递归求解，最终答案就是h[0]。

最后附上python代码：

```python
class Solution(object):
    def maximizeSumOfWeights(self, edges, k):
        """
        :type edges: List[List[int]]
        :type k: int
        :rtype: int
        """
        
        n = len(edges) + 1
        g = {x : [] for x in range(n)}
        for x, y, w in edges:
            g[x].append((y, w))
            g[y].append((x, w))

        f = [0] * n
        h = [0] * n

        def dfs(now, fa):
            heap = []
            s = 0
            for child, weight in g[now]:
                if child == fa:
                    continue

                dfs(child, now)

                if f[child] + weight > h[child]:
                    diff = f[child] + weight - h[child]
                    heapq.heappush(heap, diff)
                    s += diff
                    if len(heap) > k:
                        s -= heapq.heappop(heap)
                f[now] += h[child]
                h[now] += h[child]

            f[now] += s
            h[now] += s
            if len(heap) == k:
                f[now] -= heap[0]
        
        dfs(0, -1)

        return h[0]
```
