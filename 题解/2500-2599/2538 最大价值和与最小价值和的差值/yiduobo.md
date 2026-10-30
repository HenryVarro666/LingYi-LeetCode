---
title: "2538. 最大价值和与最小价值和的差值"
aliases: ["yiduobo的每日leetcode 2538.最大价值和与最小价值和的差值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/depth-first-search", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/三-一般树", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/637378257"
zhihu_id: "637378257"
zhihu_title: "yiduobo的每日leetcode 2538.最大价值和与最小价值和的差值"
question_id: "2538"
question: "最大价值和与最小价值和的差值"
problem_url: "https://leetcode.cn/problems/difference-between-maximum-and-minimum-price-sum/"
difficulty: "Hard"
rating: 2398
created: "2023-06-17T16:46:08+08:00"
updated: "2023-06-17T16:46:08+08:00"
upvotes: 0
comments: 0
---

# 2538. 最大价值和与最小价值和的差值

> **[yiduobo的每日leetcode 2538.最大价值和与最小价值和的差值](https://zhuanlan.zhihu.com/p/637378257) · 知乎 · 2023-06-17 · 赞同 0**
> 力扣：[2538. 最大价值和与最小价值和的差值](https://leetcode.cn/problems/difference-between-maximum-and-minimum-price-sum/) · Hard · 灵茶山艾府：[树形 DP：转换成树上最大路径和（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2538.最大价值和与最小价值和的差值

[力扣](https://leetcode.cn/problems/difference-between-maximum-and-minimum-price-sum/)

首先，注意到题目中所有节点的数值都是正数，因此以某个节点开始的最小价值路径必然只包含该节点自身，而从该节点开始的最大价值路径必然会延伸到某个叶子节点。更进一步的，最终答案必然是从某个叶子节点出发，到另一个叶子节点结束的一条树链的节点值之和，再减去这个叶子自身的节点值。

根据这个结论，就得到了一种递归的算法。

从根节点向下进行dfs，对于当前处理的节点now，计算从now出发的，到某个叶子节点结束且路径上节点值之和最大的树链，以及从now出发到某个叶子节点，但不包含这个叶子结点值的和最大的树链，分别记为ma_s1以及ma_s2。

对于这两个值的求解，就可以遍历now的所有孩子节点child，递归求解child对应的child_s1以及child_s2，这里child_s1与child_s2的含义与ma_s1以及ma_s2类似，不过child这两个值的起点为child而不是now。

得到child_s1和child_s2之后，child_s1与ma_s2组合起来，或者child_s2与ma_s1组合起来，都是从某个叶子节点出发，经过now，然后到另一个叶子节点结束的树链中的节点值之和，再减去其中某个叶子节点值，也就是上面描述的备选答案。此时就应该使用这两个值来更新答案，然后使用child_s1加上now的值来更新ma_s1，使用child_s2加上now的值来更新ma_s2。

遍历完child后，还需要返回ma_s1以及ma_s2供上层节点使用。

最后附上python代码：

```python
class Solution(object):
    def maxOutput(self, n, edges, price):
        """
        :type n: int
        :type edges: List[List[int]]
        :type price: List[int]
        :rtype: int
        """

        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        def dfs(now, fa):
            s1 = price[now]
            s2 = 0

            ma_s1 = price[now]
            ma_s2 = 0

            for child in g[now]:
                if child == fa:
                    continue
                
                child_s1, child_s2 = dfs(child, now)
                global res
                res = max(res, child_s1 + ma_s2, child_s2 + ma_s1)
                
                ma_s1 = max(ma_s1, child_s1 + price[now])
                ma_s2 = max(ma_s2, child_s2 + price[now])

            return ma_s1, ma_s2

        global res
        res = 0
        dfs(0, None)
        return res
```
