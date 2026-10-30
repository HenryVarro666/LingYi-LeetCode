---
title: "156. 上下翻转二叉树"
aliases: ["yiduobo的每日leetcode 156.上下翻转二叉树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/590705751"
zhihu_id: "590705751"
zhihu_title: "yiduobo的每日leetcode 156.上下翻转二叉树"
question_id: "156"
question: "上下翻转二叉树"
problem_url: "https://leetcode.cn/problems/binary-tree-upside-down/"
created: "2022-12-10T03:29:41+08:00"
updated: "2022-12-10T03:29:41+08:00"
upvotes: 0
comments: 0
---

# 156. 上下翻转二叉树

> **[yiduobo的每日leetcode 156.上下翻转二叉树](https://zhuanlan.zhihu.com/p/590705751) · 知乎 · 2022-12-10 · 赞同 0**
> 力扣：[156. 上下翻转二叉树](https://leetcode.cn/problems/binary-tree-upside-down/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

156.上下翻转二叉树

[力扣](https://leetcode.cn/problems/binary-tree-upside-down/)

题目描述中的翻转指的是将当前根节点now的左孩子now.left作为新的根节点，而now.right和now则分别成为now.left的左右孩子。由于题目保证了now.right是孤立的，那么对于now而言，只需优先递归求解now.left，将now.left这颗子树中的翻转操作完成后，再按照上面描述的翻转规则翻转now和now.left以及now.right就行了。

需要注意的是，题目要求返回新的树根，这很明显就是原树中最左侧的节点，那么就可以在递归求解时一层一层往上回传这个最左侧的节点，直到翻转完root这一层之后作为最终结果返回。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def upsideDownBinaryTree(self, root):
        """
        :type root: TreeNode
        :rtype: TreeNode
        """

        if not root:
            return None
        
        if not root.left:
            return root
        
        res = self.upsideDownBinaryTree(root.left)
        root.left.right = root
        root.left.left = root.right
        root.left = root.right = None
        return res
```
