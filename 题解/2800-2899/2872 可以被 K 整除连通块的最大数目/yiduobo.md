---
title: "2872. 可以被K整除连通块的最大数目"
aliases: ["yiduobo的每日leetcode 2872.可以被K整除连通块的最大数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/math", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/662531964"
zhihu_id: "662531964"
zhihu_title: "yiduobo的每日leetcode 2872.可以被K整除连通块的最大数目"
question_id: "2872"
question: "可以被 K 整除连通块的最大数目"
problem_url: "https://leetcode.cn/problems/maximum-number-of-k-divisible-components/"
difficulty: "Hard"
rating: 1968
created: "2023-10-21T04:45:55+08:00"
updated: "2023-10-21T04:45:55+08:00"
upvotes: 0
comments: 0
---

# 2872. 可以被K整除连通块的最大数目

> **[yiduobo的每日leetcode 2872.可以被K整除连通块的最大数目](https://zhuanlan.zhihu.com/p/662531964) · 知乎 · 2023-10-21 · 赞同 0**
> 力扣：[2872. 可以被 K 整除连通块的最大数目](https://leetcode.cn/problems/maximum-number-of-k-divisible-components/) · Hard · 灵茶山艾府：[判断子树点权和是否为 k 的倍数（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2872.可以被K整除的连通块的最大数目

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-number-of-k-divisible-components/)

题目的数据规模比较大，如果想详细考虑连通块的形态是一件非常困难的事情，不妨换一个角度来思考。题目要求划分出尽量多的连通块，其等价于从树中删去尽量多的边，使得剩下的各个子树中节点之和都是k的倍数，那么在这里就变成了思考一条边是否应该被删除。

题目给出了一个前提条件是树中节点值总和是k的倍数，基于这一点就可以得到一个结论：若某条边两侧的节点值之和都是k的倍数，那么这条边就可以被删掉。在这里可以尝试使用反证法来证明这个结论。

不妨设树中存在某条边连接节点p和q，且p这一侧的节点值之和以及q这一侧的节点值之和都是k的倍数，那么若最终答案中存在连通块m包含了这条边，就要求在p这一侧和q这一侧的其他连通块也必须满足各自的节点值之和是k的倍数。更进一步的，使用p这一侧的节点之和减去p这一侧其他连通块的节点值之和，就得到了连通块m在p这一侧的节点值之和，而这个值必然也是k的倍数，因为这是若干个k的倍数相减得到的。同样的，连通块m在q这一侧的节点值之和也是k的倍数，那么在这里完全可以将m进一步进行划分使得划分的结果更多。

到了这里，就证明了若某条边两侧的节点值之和都是k的倍数，那么这条边就可以被删除，接下来就需要想办法找出这条边。

由于题目给出的是一棵树，那么某个节点以及各个子树的根节点之间的边是很容易检测的，只需检测子树中的节点值之和是否为k的倍数，若是，那么树中其他节点之和也必然是k的倍数，这样一来就得到了一条可以删去的边。于是只需从根节点递归向下处理，对于当前处理的节点now，遍历其所有孩子节点。对于遍历到的child，先递归求解child这棵子树中可以删除的边，同时计算子树中节点值之和v。若v是k的倍数，就说明now和child直接的这条边可以删去。无论v是否是k的倍数，都要将其累加到now这颗子树的节点值之和s中，最后返回s与now的节点值之和供上级节点使用即可。

最后附上python代码：

```python
class Solution(object):
    def maxKDivisibleComponents(self, n, edges, values, k):
        """
        :type n: int
        :type edges: List[List[int]]
        :type values: List[int]
        :type k: int
        :rtype: int
        """

        g = {x : set() for x in range(n)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)

        global res
        res = 0

        def dfs(now, fa):
            global res
            s = 0
            for child in g[now]:
                if child == fa:
                    continue
                v = dfs(child, now)
                if v % k == 0:
                    res += 1
                
                s += v

            return s + values[now]
        
        dfs(0, -1)
        return res + 1
```
