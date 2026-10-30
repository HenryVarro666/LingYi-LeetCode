---
title: "1650. 二叉树的最近公共祖先III"
aliases: ["yiduobo的每日leetcode 1650.二叉树的最近公共祖先III"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/619225629"
zhihu_id: "619225629"
zhihu_title: "yiduobo的每日leetcode 1650.二叉树的最近公共祖先III"
question_id: "1650"
question: "二叉树的最近公共祖先III"
problem_url: "https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree-iii/"
created: "2023-04-03T22:30:47+08:00"
updated: "2023-04-03T22:30:47+08:00"
upvotes: 1
comments: 0
---

# 1650. 二叉树的最近公共祖先III

> **[yiduobo的每日leetcode 1650.二叉树的最近公共祖先III](https://zhuanlan.zhihu.com/p/619225629) · 知乎 · 2023-04-03 · 赞同 1**
> 力扣：[1650. 二叉树的最近公共祖先III](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree-iii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1650.二叉树的最近公共祖先III

[力扣](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree-iii/)

本题中的节点具有父亲节点指针，那么就可以从p开始不断向上迭代直到来到根节点为止，同时使用一个集合记录这个路径上的所有节点。接下来从q开始不断向上迭代，首次出现在集合中的节点即为最终答案。

最后附上python代码：

```python
"""
# Definition for a Node.
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None
"""

class Solution(object):
    def lowestCommonAncestor(self, p, q):
        """
        :type node: Node
        :rtype: Node
        """

        node_set = set()
        while p:
            node_set.add(p)
            p = p.parent
        
        while q not in node_set:
            q = q.parent
        
        return q
```
