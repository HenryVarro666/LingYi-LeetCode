---
title: "3558. 给边赋权值的方案数I"
aliases: ["yiduobo的每日leetcode 3558.给边赋权值的方案数I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/tree", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/math", "leetcode/combinatorics", "题单/链表-二叉树与回溯", "题单/数学算法", "题单/链表-二叉树与回溯/三-一般树", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1909807666919872482"
zhihu_id: "1909807666919872482"
zhihu_title: "yiduobo的每日leetcode 3558.给边赋权值的方案数I"
question_id: "3558"
question: "给边赋权值的方案数 I"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-assign-edge-weights-i/"
difficulty: "Medium"
rating: 1845
created: "2025-05-27T22:24:15+08:00"
updated: "2025-05-27T22:24:15+08:00"
upvotes: 1
comments: 0
---

# 3558. 给边赋权值的方案数I

> **[yiduobo的每日leetcode 3558.给边赋权值的方案数I](https://zhuanlan.zhihu.com/p/1909807666919872482) · 知乎 · 2025-05-27 · 赞同 1**
> 力扣：[3558. 给边赋权值的方案数 I](https://leetcode.cn/problems/number-of-ways-to-assign-edge-weights-i/) · Medium · 灵茶山艾府：[从 k 个数中选奇数个数的方案数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3558.给边赋权值的方案数I

[3558. 给边赋权值的方案数 I - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-ways-to-assign-edge-weights-i/description/)

题目给出一颗具有n个节点的无向树，节点从1到n编号，其中1号节点为树的根节点。树由一个长度为n - 1的二维数组edges表示，其中edges\[index\] \= \[u\[index\], v\[index\]\]，表示在节点u\[index\]和v\[index\]之间有一条边。

一开始，树中所有边的权重都为0，可以将每条边的权重设置为1或者2。两个节点u和v之间的路径的代价为链接二者的路径上所有边的权重之和。

现在要求从树中选择任意一个深度最大的节点x，计算从1到x的路径中，权重之和为奇数的赋值方案数量。需要注意，仅计算这条路径上的边赋值的方案，忽略掉其他不在路径上的边。

题目分为两个部分，先计算从1到树中最深节点x的路径中边的数量cnt，然后计算为这cnt条边赋值的方案数量。

对于cnt的计算，只需从1号节点开始执行bfs，使用一个数组level记录每个节点的层级。由于1号节点的level为0，那么level中的最大值就是cnt。

接下来是计算对于cnt条边的赋值方案数量。

首先考虑特殊情况

为了使得边权之和为奇数，那么就需要从cnt中选出奇数条边赋值为1，其余的边赋值为2，因此一共有

C(cnt, 1) + C(cnt, 3) + C(cnt, 5) + ...

若cnt为奇数，那么就是

C(cnt, 1) + C(cnt, 3) + C(cnt, 5) + ... + C(cnt, cnt)

对于以上的组合数，可以通过C(m, n) \= C(m - 1, n - 1) + C(m - 1, n)来拆解，得到

C(cnt, 1) \= C(cnt - 1, 0) + C(cnt - 1, 1)

C(cnt, 3) \= C(cnt - 1, 2) + C(cnt - 1, 3)

C(cnt, 5) \= C(cnt - 1, 4) + C(cnt - 1, 5)

...

C(cnt, cnt - 1) \= C(cnt - 1, cnt - 2) + C(cnt - 1, cnt - 1)

C(cnt, cnt) \= C(cnt - 1, cnt - 1)

可以发现，原式之和恰好是C(cnt - 1, 0)到C(cnt - 1, cnt - 1)这些项之和，等于2^(cnt - 1)

若cnt为偶数，那么就是

C(cnt, 1) + C(cnt, 3) + C(cnt, 5) + ... + C(cnt, cnt - 1)

同样是进行拆解，得到的也恰好是C(cnt - 1, 0)到C(cnt - 1, cnt - 1)这些项之和，等于2^(cnt - 1)

综合上面两种情况，答案就是2^(cnt - 1)，那么在这里只需使用快速幂计算2^(cnt - 1)就行了。

最后附上python代码：

```python
class Solution(object):
    def assignEdgeWeights(self, edges):
        """
        :type edges: List[List[int]]
        :rtype: int
        """
        
        n = len(edges) + 1
        g = [[] for _ in range(n + 1)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        level = [None] * (n + 1)
        q = deque()
        q.append(1)
        level[1] = 0
        while q:
            x = q.popleft()
            for y in g[x]:
                if level[y] is None:
                    q.append(y)
                    level[y] = level[x] + 1
        
        mod = 10 ** 9 + 7
        def quick_pow(p):
            if p == 0:
                return 1
            if p == 1:
                return 2
            
            v = quick_pow(p // 2)
            v = v * v % mod
            if p & 1:
                v = v * 2 % mod
            return v

        return quick_pow(max(level) - 1)
```
