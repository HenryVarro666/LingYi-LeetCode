---
title: "2925. 在树上执行操作以后得到的最大分数"
aliases: ["yiduobo的每日leetcode 2925.在树上执行操作以后得到的最大分数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/690070208"
zhihu_id: "690070208"
zhihu_title: "yiduobo的每日leetcode 2925.在树上执行操作以后得到的最大分数"
question_id: "2925"
question: "在树上执行操作以后得到的最大分数"
problem_url: "https://leetcode.cn/problems/maximum-score-after-applying-operations-on-a-tree/"
difficulty: "Medium"
rating: 1940
created: "2024-04-01T00:14:18+08:00"
updated: "2024-04-01T00:14:18+08:00"
upvotes: 2
comments: 0
---

# 2925. 在树上执行操作以后得到的最大分数

> **[yiduobo的每日leetcode 2925.在树上执行操作以后得到的最大分数](https://zhuanlan.zhihu.com/p/690070208) · 知乎 · 2024-04-01 · 赞同 2**
> 力扣：[2925. 在树上执行操作以后得到的最大分数](https://leetcode.cn/problems/maximum-score-after-applying-operations-on-a-tree/) · Medium · 灵茶山艾府：[树形 DP：选或不选（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2925.在树上执行操作以后得到的最大分数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-score-after-applying-operations-on-a-tree/description/)

题目给出一棵树，可以取走树中一些节点的值，要求取走后不能出现一条值全部被取走的路径，问最大的取值之和是多少。

根据样例一的提示，一种可行的想法是基于子树的根节点来进行考虑。更具体的，对于一颗子树，可以选择保留其根节点值，这种情况下，由于树中节点值都是正数，因此就应该将子树中其他的节点值全部取走；另一种选择则是取走根节点值，那么之后的合法性保证则需要下放到当前子树的子树中进行。

综合起来，在这里可以递归求解每颗子树，分别计算保证合法性的前提下的最大值以及树中所有节点值之和。

对于当前子树，不妨设根节点为now，那么在这里可以先递归求解now的所有子树，计算各子树的v和s，并将其累加起来得到tot_v和tot_s。

接下来，若tot_s为0，也就是当前子树实际上是个叶子节点，那么此时必须保留节点now，也就是说合法的最大值为0，节点值之和为values[now]。

反之，若tot_s非0，那么在这里就可以对比上面说到的两种方法。如果保留values[now]，那么合法的最大值就是所有子树节点值之和tot_s；如果取走values[now]，那么子树中可以取的合法的最大值就是tot_v，再加上values[now]就是tot_v + values[now]。综合起来，合法的最大值就是max(tot_v + values[now], tot_s)。另外，无论是哪种情况，子树中所有节点值之和都是tot_s + values[now]。

最后附上python代码：

```python
class Solution(object):
    def maximumScoreAfterOperations(self, edges, values):
        """
        :type edges: List[List[int]]
        :type values: List[int]
        :rtype: int
        """

        n = len(edges) + 1
        g = {index : set() for index in range(n)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)

        def dfs(now, fa):
            tot_v = 0
            tot_s = 0

            for child in g[now]:
                if child == fa:
                    continue
                v, s = dfs(child, now)
                tot_s += s
                tot_v += v

            if tot_s == 0:
                return 0, values[now]
            else:
                return max(tot_v + values[now], tot_s), tot_s + values[now]
        
        return dfs(0, None)[0]
```
