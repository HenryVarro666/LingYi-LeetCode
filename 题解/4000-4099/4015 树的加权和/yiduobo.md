---
title: "4015. 树的加权和"
aliases: ["yiduobo的每日leetcode 4015.树的加权和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2070647519315485808"
zhihu_id: "2070647519315485808"
zhihu_title: "yiduobo的每日leetcode 4015.树的加权和"
question_id: "4015"
question: "树的加权和"
problem_url: "https://leetcode.cn/problems/weighted-sum-of-a-tree/"
difficulty: "Medium"
rating: 1534
created: "2026-08-11T23:14:56+08:00"
updated: "2026-08-11T23:14:59+08:00"
upvotes: 1
comments: 3
---

# 4015. 树的加权和

> **[yiduobo的每日leetcode 4015.树的加权和](https://zhuanlan.zhihu.com/p/2070647519315485808) · 知乎 · 2026-08-11 · 赞同 1**
> 力扣：[4015. 树的加权和](https://leetcode.cn/problems/weighted-sum-of-a-tree/) · Medium · 灵茶山艾府：[两次 DFS / 一次 DFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4015.树的加权和

<https://leetcode.cn/problems/weighted-sum-of-a-tree/>

题目给出一个长度为n的整数数组parent，其表示一颗根节点编号为0、节点编号为0到n - 1的有根树。由于0为根节点，因此parent[0] \= -1，同时对于每个1到n之间的节点u，parent[u]表示u的父节点。

另外给出一个长度为n的整数数组nums，其中nums[u]表示节点u的值。

对于深度为d的节点u，其权重定义为nums[u] \* (h - d + 1)，其中h为树的高度。根节点的深度为1。

要求返回数中所有节点的权重之和。

首先，对于题目给出的权重计算公式，可以先进行一次变形，让计算更加简单。原始的权重之和为

nums[0] \* (h - d[0] + 1) + nums[1] \* (h - d[1] + 1) + ... + nums[n - 1] \* (h - d[n - 1] + 1)

将h + 1和d分离，就有

nums[0] \* (h + 1) + ... + nums[n - 1] \* (h + 1) - nums[0] \* d[0] - nums[1] \* d[1] - ... - nums[n - 1] \* d[n - 1]

前半部分就是nums之和乘以h + 1，而后半部分则是每个节点的节点值乘以其对应的深度，此时就可以先通过parent建树，然后从根节点向下一次bfs计算出这个加和。在这里采用bfs的理由是每一轮bfs的节点对应都是相同的深度，方便最终结果的计算。

最后附上python代码：

```python
class Solution(object):
    def weightedSum(self, parent, nums):
        """
        :type parent: List[int]
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(parent)
        g = [[] for _ in range(n)]
        for x, p in enumerate(parent[1:], 1):
            g[p].append(x)
        
        s = 0
        d = 0
        q = [0]
        head, tail = 0, 1
        while head < tail:
            d += 1
            for x in q[head : tail]:
                s += nums[x] * d
                for y in g[x]:
                    q.append(y)
            
            head, tail = tail, len(q)
        
        return (d + 1) * sum(nums) - s
```
