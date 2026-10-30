---
title: "3772. 子图的最大得分"
aliases: ["yiduobo的每日leetcode 3772.子图的最大得分"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/tree", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1981142324273763268"
zhihu_id: "1981142324273763268"
zhihu_title: "yiduobo的每日leetcode 3772.子图的最大得分"
question_id: "3772"
question: "树中子图的最大得分"
problem_url: "https://leetcode.cn/problems/maximum-subgraph-score-in-a-tree/"
difficulty: "Hard"
rating: 2235
created: "2025-12-11T20:58:47+08:00"
updated: "2025-12-11T20:58:48+08:00"
upvotes: 2
comments: 0
---

# 3772. 子图的最大得分

> **[yiduobo的每日leetcode 3772.子图的最大得分](https://zhuanlan.zhihu.com/p/1981142324273763268) · 知乎 · 2025-12-11 · 赞同 2**
> 力扣：[3772. 树中子图的最大得分](https://leetcode.cn/problems/maximum-subgraph-score-in-a-tree/) · Hard · 灵茶山艾府：[换根 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3772.子图的最大得分

[3772. 子图的最大得分 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-subgraph-score-in-a-tree/description/)

题目给出一个无向树，包含n个节点，编号为0到n - 1。其中n的大小不超过10^5。树由一个长度为n - 1的二维整数数组edges描述，其中edges\[index\] \= \[a\[index\], b\[index\]\]，表示在a\[index\]和b\[index\]之间由一条边。

另外给出一个长度为n的整数数组good，其中good[index]为1，表示第index个节点为好节点，为0则表示其为坏节点。

定义子图的得分为子图中好节点的数量减去坏节点的数量。

对于每个节点index，找到包含index的所有连通子图中可能的最大得分。

要求返回一个长度为n的整数数组，表示每个节点对应的最大得分。

首先，一颗树中的连通子图显然也是一棵树，那么本题实际上就是要找出包含每个节点的最优的树对应的最大得分是什么。对于这类问题，一种常见的处理方法是换根dp。

不妨设0号节点为整棵树的根节点，那么包含0号节点的最大得分是比较好计算的。

令f[x]为以x为根节点的子树中，包含x的子树的最大得分，那么对于f[x]，首先可以根据g[x]的值初始化其为1或者-1。接下来对于x的所有孩子节点y，先递归求解f[y]，接下来若f[y] > 0，那么就将f[y]累加到x中，表示选择了以y为根节点的子树中的某个包含y的子树，得到了f[y]的分数；反之，则跳过y，表示放弃掉以y为根节点的子树中的所有节点。

从0号结点开始向下递归计算，最终的f[0]就是0号节点对应的最大得分。

方便期间，在这里记最终答案为res，那么就有res[0] \= f[0]。

接下来不妨考虑某个非0节点y，令其父亲节点为x。对于y而言，其最终的得分可以拆分为两个部分，分别是：

1、以y为根节点的子树中，包含y的最大得分：

这个部分的得分就是之前计算得到的f[y]

2、整棵树去除掉以y为根节点的子树后剩下的部分中，包含y的父亲节点x的子树的最大得分，不妨记为pa[y]：

这里必须包含y的父亲节点x，因为这样才能保证两个部分是连通的。

另一方面，这个得分还可以再进行拆分，也就是

2-1)以x为根节点的子树中，包含x，且不包含y的最优子树的最大得分

这个部分是很好计算的。注意上面关于f的计算，若f[y] > 0，才将f[y]累加到f[x]中。也就是说在这里只需要跳过以y为根节点的子树，也就是让f[x]减去max(0, f[y])，就可以得到以x为根节点的子树中，包含x且不包含y的最优子树的最大得分。

2-2)整棵树去掉以x为根节点的子树后剩下的部分中，包含x的父亲节点的子树的最大得分：

可以发现，这里实际上就是pa[x]，且根据上面的定义，有res[x] \= pa[x] + f[x]，因此可以直接通过res[x] - f[x]计算出当前的pa[x]。

这样一来，就可以得到pa[y] \= max(0, pa[x] + f[x] - max(0, f[y]))，接下来就可以使用pa[y] + f[y]得到对应的res[y]了。

基于上面的结论，考虑到已知0号节点对应的res[0]为f[0]，因此可以从0号节点开始，向下再次进行递归计算，得到树中所有节点的res。

最后附上python代码：

```python
class Solution(object):
    def maxSubgraphScore(self, n, edges, good):
        """
        :type n: int
        :type edges: List[List[int]]
        :type good: List[int]
        :rtype: List[int]
        """
        
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)
        
        f = [0] * n
        def dfs(now, fa, f):
            if good[now]:
                f[now] = 1
            else:
                f[now] = -1
            
            for child in g[now]:
                if child == fa:
                    continue
                f[now] += max(0, dfs(child, now, f))
            
            return f[now]
        
        dfs(0, -1, f)

        res = [0] * n
        res[0] = f[0]

        def calc(now, fa, res):
            pa = res[now] - f[now]
            for child in g[now]:
                if child == fa:
                    continue
                
                other = f[now] - max(0, f[child])
                res[child] = f[child] + max(0, pa + other)
                calc(child, now, res)

        calc(0, -1, res)

        return res
```
