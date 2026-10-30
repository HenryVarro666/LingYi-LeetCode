---
title: "1519. 子树中标签相同的节点数"
aliases: ["yiduobo的每日leetcode 1519.子树中标签相同的节点数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/421618854"
zhihu_id: "421618854"
zhihu_title: "yiduobo的每日leetcode 1519.子树中标签相同的节点数"
question_id: "1519"
question: "子树中标签相同的节点数"
problem_url: "https://leetcode.cn/problems/number-of-nodes-in-the-sub-tree-with-the-same-label/"
created: "2021-10-14T23:36:42+08:00"
updated: "2021-10-14T23:36:42+08:00"
upvotes: 0
comments: 0
---

# 1519. 子树中标签相同的节点数

> **[yiduobo的每日leetcode 1519.子树中标签相同的节点数](https://zhuanlan.zhihu.com/p/421618854) · 知乎 · 2021-10-14 · 赞同 0**
> 力扣：[1519. 子树中标签相同的节点数](https://leetcode.cn/problems/number-of-nodes-in-the-sub-tree-with-the-same-label/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1519.子树中标签相同的节点数

[力扣](https://leetcode-cn.com/problems/number-of-nodes-in-the-sub-tree-with-the-same-label/)

对于一颗以now为根节点的子树而言，其所有节点的各个标签数可以通过统计以now的各个孩子为根节点的子树中标签数之和，再加上root这个节点本身的标签来计算出来。那么一个自然的想法就是从root开始进行dfs，先递归求解各个子树并统计子树中各个标签数，并计算出当前子树的各个标签数之和。在dfs过程中，也可以顺便将答案更新好。

最后附上python代码：

```python
class Solution(object):
    def countSubTrees(self, n, edges, labels):
        """
        :type n: int
        :type edges: List[List[int]]
        :type labels: str
        :rtype: List[int]
        """

        g = {x : set() for x in range(n)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)
        
        used = set([0])

        res = [0] * n
        final_cnt = self.dfs(0, g, used, res, labels)
        return res
    
    def dfs(self, now, g, used, res, labels):
        now_cnt = {labels[now] : 1}
        for next in g[now]:
            if next not in used:
                used.add(next)
                child_cnt = self.dfs(next, g, used, res, labels)
                for char in child_cnt:
                    now_cnt[char] = now_cnt.get(char, 0) + child_cnt[char]
        
        res[now] = now_cnt[labels[now]]
        return now_cnt
```
