---
title: "285. 二叉搜索树中的中序后继"
aliases: ["yiduobo的每日leetcode 285.二叉搜索树中的中序后继"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/594541357"
zhihu_id: "594541357"
zhihu_title: "yiduobo的每日leetcode 285.二叉搜索树中的中序后继"
question_id: "285"
question: "二叉搜索树中的中序后继"
problem_url: "https://leetcode.cn/problems/inorder-successor-in-bst/"
created: "2022-12-26T23:03:43+08:00"
updated: "2022-12-26T23:03:43+08:00"
upvotes: 0
comments: 0
---

# 285. 二叉搜索树中的中序后继

> **[yiduobo的每日leetcode 285.二叉搜索树中的中序后继](https://zhuanlan.zhihu.com/p/594541357) · 知乎 · 2022-12-26 · 赞同 0**
> 力扣：[285. 二叉搜索树中的中序后继](https://leetcode.cn/problems/inorder-successor-in-bst/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

285.二叉搜索树中的中序后继

[力扣](https://leetcode.cn/problems/inorder-successor-in-bst/)

由于题目给出的是二叉搜索树，那么当p存在右孩子时，下一个比p大的节点就必然是p右子树中最左侧的那个节点，此时只需从p的右孩子开始不断向左侧迭代就行了。若p不存在右孩子，那么下一个比p大的节点就是比p大的祖先节点中离p最近的那一个，因为p一定是位于比p大的祖先节点的左子树中，因此离p较近的祖先节点必然也位于离p较远的祖先节点的左子树中，其数值与p的差距也相对较小。在这种情况下，只需从根节点向下迭代找到p，迭代过程中最后一个数值大于p的节点即为所求。另外，当不存在比p大的节点时，则需要返回空。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def inorderSuccessor(self, root, p):
        """
        :type root: TreeNode
        :type p: TreeNode
        :rtype: TreeNode
        """

        if p.right:
            res = p.right
            while res.left:
                res = res.left
            return res
        
        res = None
        now = root
        while now != p:
            if now.val > p.val:
                res = now
                now = now.left
            else:
                now = now.right
        
        return res
```
