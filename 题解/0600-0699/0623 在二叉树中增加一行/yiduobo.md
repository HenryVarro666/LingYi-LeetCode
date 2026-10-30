---
title: "623. 在二叉树中增加一行"
aliases: ["yiduobo的每日leetcode 623.在二叉树中增加一行"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/270021919"
zhihu_id: "270021919"
zhihu_title: "yiduobo的每日leetcode 623.在二叉树中增加一行"
question_id: "623"
question: "在二叉树中增加一行"
problem_url: "https://leetcode.cn/problems/add-one-row-to-tree/"
created: "2020-10-29T23:07:30+08:00"
updated: "2020-10-29T23:07:30+08:00"
upvotes: 0
comments: 0
---

# 623. 在二叉树中增加一行

> **[yiduobo的每日leetcode 623.在二叉树中增加一行](https://zhuanlan.zhihu.com/p/270021919) · 知乎 · 2020-10-29 · 赞同 0**
> 力扣：[623. 在二叉树中增加一行](https://leetcode.cn/problems/add-one-row-to-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

623.在二叉树中增加一行<https://leetcode-cn.com/problems/add-one-row-to-tree/>

题目要求在二叉树中的特定深度增加一层节点，那么我们可以从根节点开始，带上当前节点的深度开始递归。若当前节点的深度还不到目标深度d - 1，那么继续往下一层递归。若当前节点的深度为d - 1，说明需要插入的层就是当前节点的下一层，于是可以新建两个节点left和right，将left的左孩子置为当前节点的左孩子，将right的右孩子置为当前节点的右孩子，然后将left和right置为当前节点的左右孩子即可。执行完毕之后，由于再往下的树结构就不会产生变化了，因此无须继续往下递归。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def addOneRow(self, root, v, d):
        """
        :type root: TreeNode
        :type v: int
        :type d: int
        :rtype: TreeNode
        """

        if d == 1:
            tmp = TreeNode(v)
            tmp.left = root
            return tmp

        self.dfs(root, 1, v, d)
        return root

    def dfs(self, now, depth, v, d):
        if depth == d - 1:
            tmp = TreeNode(v)
            tmp.left = now.left
            now.left = tmp
            tmp = TreeNode(v)
            tmp.right = now.right
            now.right = tmp
        else:
            if now.left:
                self.dfs(now.left, depth + 1, v, d)
            if now.right:
                self.dfs(now.right, depth + 1, v, d)
```
